import os
import time
import json
import uvicorn
from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.memory import HumanMessage, AIMessage, SystemMessage
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union
from sse_starlette.sse import EventSourceResponse

os.environ["EB_AGENT_ACCESS_TOKEN"] = "<your access token>"
os.environ["EB_AGENT_LOGGING_LEVEL"] = "info"

app = FastAPI()  # 创建 api 对象


##请求入参
class DeltaMessage(BaseModel):
    role: Optional[Literal["user", "assistant", "system"]] = None
    content: Optional[str] = None


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length"]]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal["stop", "length"]


# 创建参数对象
class ChatCompletionResponse(BaseModel):
    model: str
    object: Literal["chat.completion", "chat.completion.chunk"]
    choices: List[Union[ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice]]
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))


# 返回体
class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_length: Optional[int] = None
    stream: Optional[bool] = False


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest):
    # 封装对话
    messages = []
    # 获取最近一个用户问题
    if request.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail="Invalid request")
    query = request.messages[-1].content
    # 获取system 提示词
    prev_messages = request.messages[:-1]
    if len(prev_messages) > 0 and prev_messages[0].role == "system":
        system_message = SystemMessage(content=prev_messages.pop(0).content)
    else:
        system_message = SystemMessage(content='')

    # 追加历史记录
    if len(prev_messages) % 2 == 0:
        for i in range(0, len(prev_messages), 2):
            if prev_messages[i].role == "user" and prev_messages[i + 1].role == "assistant":
                messages.append(HumanMessage(content=prev_messages[i].content))
                messages.append(AIMessage(content=prev_messages[i + 1].content))

    # 指定模型
    model = ERNIEBot(model=request.model)

    # 添加最新用户问题
    messages.append(HumanMessage(content=query))
    # AI回答 请求模型

    # 流式调用
    if request.stream:
        generate = predict(system_message.content, messages, request.model)
        return EventSourceResponse(generate, media_type="text/event-stream")

    # 非流式调用
    if system_message.content != '':
        ai_message = await model.chat(messages=messages, system=system_message.content)
    else:
        ai_message = await model.chat(messages=messages)

    choice_data = ChatCompletionResponseChoice(
        index=0,
        message=ChatMessage(role="assistant", content=ai_message.content),
        finish_reason="stop"
    )
    return ChatCompletionResponse(model=request.model, choices=[choice_data], object="chat.completion")


async def predict(system: str, messages: List[List[str]], model_id: str):
    choice_data = ChatCompletionResponseStreamChoice(
        index=0,
        delta=DeltaMessage(role="assistant"),
        finish_reason=None
    )
    chunk = ChatCompletionResponse(model=model_id, choices=[choice_data], object="chat.completion.chunk")
    # yield "{}".format(chunk.json(exclude_unset=True, ensure_ascii=False))
    yield json.dumps(chunk.dict(exclude_unset=True), ensure_ascii=False)

    model = ERNIEBot(model=model_id)

    if system:
        ai_message = await model.chat(system=system, messages=messages, stream=True)
    else:
        ai_message = await model.chat(messages=messages, stream=True)

    async for chunk in ai_message:
        # result += chunk.content
        choice_data = ChatCompletionResponseStreamChoice(
            index=0,
            delta=DeltaMessage(content=chunk.content),
            finish_reason=None
        )
        chunk = ChatCompletionResponse(model=model_id, choices=[choice_data], object="chat.completion.chunk")
        print(chunk)
        # yield "{}".format(chunk.json(exclude_unset=True, ensure_ascii=False))
        yield json.dumps(chunk.dict(exclude_unset=True), ensure_ascii=False)

    choice_data = ChatCompletionResponseStreamChoice(
        index=0,
        delta=DeltaMessage(),
        finish_reason="stop"
    )
    chunk = ChatCompletionResponse(model=model_id, choices=[choice_data], object="chat.completion.chunk")
    # yield "{}".format(chunk.json(exclude_unset=True, ensure_ascii=False))
    yield json.dumps(chunk.dict(exclude_unset=True), ensure_ascii=False)
    yield '[DONE]'


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000, workers=1)

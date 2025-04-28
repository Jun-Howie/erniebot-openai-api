# erniebot-openai-api
erniebot兼容openai的API调用方式，支持流式，非流式调用 ，支持system提示词

# 快速使用

```bash

conda create -n enbot python=3.10.6

git clone https://github.com/Jun-Howie/erniebot-openai-api.git

cd erniebot-openai-api

pip install -r requirements.txt

python erniebot-openai-api.py

```

# docker

```bash
# 替换YOU_ACCESS_TOKEN
docker run -e EB_AGENT_ACCESS_TOKEN=YOU_ACCESS_TOKEN -e EB_AGENT_LOGGING_LEVEL=info -p 8000:8000 amberyu/enbot


阿里云镜像
docker run -d -e EB_AGENT_ACCESS_TOKEN=YOU_ACCESS_TOKEN -e EB_AGENT_LOGGING_LEVEL=info -p 8000:8000 registry.cn-shanghai.aliyuncs.com/chatpet/enbot

```



# 调用测试
curl --location --request POST 'http://127.0.0.1:8000/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data-raw '{
  "model": "ernie-4.0",
  "messages": [
    {
      "role": "user",
      "content": "百度公关一号位"
    }
  ]
}'


# 测试结果
{
    "model": "ernie-4.0",
    "object": "chat.completion",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "百度公关一号位指的是**百度副总裁璩静**。璩静毕业于外交学院，曾任新华社中央新闻采访中心记者，华为公共及政府事务部副总裁、中国媒体事务部部长。2021年8月入职百度担任公关副总裁（VP），负责集团公众沟通部工作。\n\n近期，璩静开设了名为“我是璩静”的抖音账号，并因发布的内容引发了争议和关注。其中，包括“员工闹分手提离职我秒批”、“为什么要考虑员工的家庭”、“举报信洒满工位”等视频内容在网络上广泛传播。这些视频在短短几天内就吸引了大量粉丝，使璩静成为了互联网媒体公关圈的热议话题。\n\n以上信息仅供参考，建议查阅相关新闻报道获取更多信息。"
            },
            "finish_reason": "stop"
        }
    ],
    "created": 1715152014
}
# 使用飞桨平台调用ernie-4.0 / PS:toknes 比千帆便宜

[飞桨ai studio星河社区](https://aistudio.baidu.com/) <br />
[ERNIE Bot文档](https://ernie-bot-agent.readthedocs.io/zh-cn/latest/sdk/) <br />
![cd8dd2724b821c3004e51a1facb0b66](https://github.com/Jun-Howie/erniebot-openai-api/assets/62869005/9c489a0c-2c7f-4045-bc3e-7c35c4cc2721)

![image](https://github.com/Jun-Howie/erniebot-openai-api/assets/62869005/b4f1957b-6dd3-4ac6-983f-b31eb088b9e0)

# 感谢
感谢[lixiaoxiangzhi](https://github.com/lixiaoxiangzhi) 帮助解决流式异步编程问题 <br />
感谢[ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B/blob/main/openai_api.py) 提供原始兼容openai-api的封装思路 <br />









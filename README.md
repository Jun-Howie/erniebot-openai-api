# erniebot-openai-api
erniebot兼容openai的API调用方式，支持流式，非流式调用 ，支持system提示词

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

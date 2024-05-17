# 使用官方的Python基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到工作目录中
COPY . /app

# 安装必要的依赖
RUN pip install --no-cache-dir -r requirements.txt

# 环境变量设置
ENV EB_AGENT_ACCESS_TOKEN=""
ENV EB_AGENT_LOGGING_LEVEL=""

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
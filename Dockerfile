FROM python:3.10-slim

# 设置工作目录
WORKDIR /app
# 安装 uv
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
# 使用 uv sync
RUN uv sync

# 复制项目源码
COPY . .
# 复制启动脚本并赋予执行权限
COPY start.sh ./
RUN chmod +x start.sh
# 暴露端口
EXPOSE 5520
# 运行启动脚本
CMD ["./start.sh"]

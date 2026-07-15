# AI-API

基于 Flask 的 Prompt 驱动 AI 微服务框架 —— 只需添加一个 `.md` Prompt 文件，即可自动生成对应的 AI API 接口。

## 项目特色

### 🚀 Prompt 即 API

这是本项目最核心的设计理念：**添加 Prompt 文件 = 添加 API 接口**。

只需在 `prompts/` 目录下放一个 `.md` 文件，系统会自动将其注册为 `/api/service/<文件名>` 的 API 端点，无需写任何业务代码。

```
prompts/
  ├── pinyin.md       →  POST /api/service/pinyin    (汉字转拼音)
  └── translate.md    →  POST /api/service/translate (翻译服务)
```

### 🧩 蓝图自动发现

`api/` 目录下的 Python 模块会被自动扫描和注册，新增蓝图模块无需手动 import，开箱即用。

### 🔧 技术栈

| 组件 | 技术 |
|------|------|
| Web 框架 | Flask 3.x |
| AI 调用 | OpenAI SDK (兼容多厂商) |
| 生产部署 | Gunicorn + Docker |
| 包管理 | uv (Python 包管理器) |
| 运行环境 | Python ≥ 3.12 |

## 项目结构

```
ai-api/
├── main.py                # 应用入口，Flask 实例创建与 CORS 配置
├── pyproject.toml         # 项目依赖与 uv 配置
├── uv.lock                # 依赖锁定文件
├── .env.example           # 环境变量模板
├── .python-version        # Python 版本声明 (3.12)
├── Dockerfile             # Docker 镜像构建
├── start.sh               # Gunicorn 生产启动脚本
│
├── api/                   # API 蓝图模块（自动发现注册）
│   ├── __init__.py        # 蓝图自动扫描注册 + JSON 中文不转义
│   ├── index.py           # 根路径健康检查 (GET /api/)
│   └── service.py         # Prompt 服务路由 (/api/service/<name>)
│
├── utils/                 # 工具模块
│   ├── AITool.py          # OpenAI 客户端封装，支持系统 Prompt
│   └── EnvironTool.py     # 环境变量统一管理 (.env + os.environ)
│
└── prompts/               # Prompt 模板目录（添加 .md 即添加 API）
    └── pinyin.md          # 示例：汉字转拼音 Prompt
```

## 快速开始

### 1. 环境准备

```bash
# 确保 Python >= 3.12
python --version

# 安装 uv（如未安装）
pip install uv
```

### 2. 安装依赖

```bash
uv sync
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 AI 服务配置：

```env
API_HOST=https://your-llm-api-host/v1
API_KEY=your-api-key
MODEL_NAME=your-model-name
DEBUG=false
```

### 4. 启动服务

**开发模式**（Flask 内置服务器）：

```bash
# 直接运行（DEBUG=true 时开启热重载）
python main.py
```

**生产模式**（Gunicorn）：

```bash
./start.sh
gunicorn -w 2 -b 0.0.0.0:5520 main:app
```

## Docker 部署

```bash
docker build -t ai-api .
docker run -p 5520:5520 --env-file .env ai-api
```

服务默认运行在 `http://localhost:5520`。

## API 接口

### 健康检查

```bash
GET /api/
```

响应：

```json
{
  "code": 0,
  "msg": "API is running...",
  "data": null
}
```

### 获取可用服务列表

```bash
GET /api/service/
```

响应：

```json
{
  "code": 1,
  "msg": "please select a service",
  "data": ["pinyin.md"]
}
```

### 查看服务信息

```bash
GET /api/service/pinyin
```

响应：

```json
{
  "code": 0,
  "msg": "service: pinyin is running, use post method to send data",
  "data": null
}
```

### 调用 AI 服务

```bash
POST /api/service/pinyin
Content-Type: application/x-www-form-urlencoded

input=你好世界
```

响应：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "response": "nǐ hǎo shì jiè"
  }
}
```

## 添加新服务

只需两步：

1. 在 `prompts/` 目录下创建 `xxx.md`，编写 Prompt
2. 直接调用 `POST /api/service/xxx`，无需重启

## 响应

所有接口统一返回格式：

```json
{
  "code": 0,       // 0 = 成功, 1 = 失败
  "msg": "...",    // 状态描述
  "data": null     // 响应数据
}
```

- JSON 输出中文不转义（`ensure_ascii = False`）
- 默认配置：全局 CORS 允许跨域访问

## 许可证

MIT

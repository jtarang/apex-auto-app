# Apex Auto MCP

A FastAPI application wrapped with **FastMCP 2.0** for use as a Model Context Protocol (MCP) server with **LM Studio**.

---

## 🚀 Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (modern Python package and environment manager)
- LM Studio (latest version)

---

## 🧩 Dev Setup Instructions

### 1. Clone the Repository

```shell
git clone https://github.com/yourusername/apex-auto-app.git
cd apex-auto-app
```

### 2. Create and Activate the Virtual Environment

```shell
uv venv
source .venv/bin/activate
```

### 3. Install Dependencies

```shell
uv pip install -r pyproject.toml
```

---

## ⚡ Running the API Server and MCP Server

### Docker Compose

```shell
docker compose up
```

- MCP Server Address: `https://localhost:8100/sse`
- API Server Address `https://localhost:8000/docs`

### MCP Config

#### LM Studio
```shell
{
  "servers": {
    "apex-sse-server": {
      "transport": {
        "type": "sse",
        "url": "http://127.0.0.1:8100/sse"
      }
    }
  }
}
```
---

## 📚 References

- [FastMCP Docs](https://gofastmcp.com)
- [MCP SDK](https://modelcontextprotocol.io)

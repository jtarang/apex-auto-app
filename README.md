# Apex Auto MCP

A FastAPI application wrapped with **FastMCP 2.0** for use as a Model Context Protocol (MCP) server with **LM Studio**.

---

## 🚀 Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (modern Python package and environment manager)
- LM Studio (latest version)

---

## 🧩 Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/yourusername/apex-auto-app.git
cd apex-auto-app
```

### 2. Create and Activate the Virtual Environment

```
uv venv
source .venv/bin/activate
```

### 3. Install Dependencies

```
uv pip install -r pyproject.toml
```

---

## ⚡ Running the MCP Server

### Option 1: Run with Python

```
python main.py
```

You should see output similar to:

```
Server name:     apex-auto-mcp
Transport:       Streamable-HTTP
Server URL:      http://127.0.0.1:8000/mcp
FastMCP version: 2.12.4
MCP SDK version: 1.16.0
```

---

## 📚 References

- [FastMCP Docs](https://gofastmcp.com)
- [MCP SDK](https://modelcontextprotocol.io)

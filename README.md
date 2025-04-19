# 🧠 s6eagv1 – Agentic AI Architecture with MCP + Pydantic Cognitive Layers

`s6eagv1` is an experimental Agentic AI system built using a cognitive-layered architecture. It leverages MCP, `pydantic` models, and a tool-augmented LLM interface to enable dynamic task planning and reasoning.
[Demo](https://www.youtube.com/watch?v=tvMTwsWqekE)
---

## ✨ Features

- 🔁 Cognitive Layer Design: Perception → Memory → Decision → Action
- 🛠️ Tool-augmented reasoning using structured `FUNCTION_CALL`s
- 🧩 MCP-compatible tool registration and execution
- 🧠 LLM-as-a-Perception engine via Gemini (or other LLMs)
- 📐 Typed task planning with Pydantic schemas
- 🖼️ Visual rendering via browser-based paint tool (like jspaint.app)
- 🔍 Dynamic tool description generation from local or remote sources

---

## 🧠 Cognitive Layer Breakdown

| Layer       | Responsibility                                                  |
|-------------|------------------------------------------------------------------|
| Perception  | Parse natural language into structured `PerceptionModel`        |
| Memory      | Cache tool responses for reuse and validation                   |
| Decision    | Plan tool sequence based on current state and goal              |
| Action      | Execute tool calls, visualize output, and finalize task         |

---

## 📦 Installation

```bash
git clone https://github.com/piygr/s6eagv1.git
cd s6eagv1
python -m venv .veag1
source .veag1/bin/activate
pip install -r requirements.txt
```

## Project structure
```
s6eagv1/
├── perception.py         # Perception layer using Gemini & structured models
├── agent.py              # Main agent Layer logic
├── memory.py              # Memory Layer
├── decision.py            # Decision Layer making next decision to take
├── action.py              # Action Layer to execute the decision
├── mcp_server.py         # MCP tool server with @mcp.tool()s
├── main.py              # Global logger with colored console output
├── client.py             # LLM + MCP session orchestration
├── model.py              # Pydantic-based schemas for mcp tools' input/output
└── README.md
```




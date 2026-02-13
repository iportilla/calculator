# Cloud MCP Calculator: Student & Instructor Guide

This repository contains a cloud-deployable math tool server using the **Model Context Protocol (MCP)** via **Server-Sent Events (SSE)**. This architecture allows students to connect their local local LLM agents (via VS Code Continue) to a centralized, instructor-managed tool.

## Distributed Architecture

The following diagram shows how the system is distributed between the instructor's cloud infrastructure and the students' local machines.

```mermaid
graph TB
    subgraph "Cloud Infrastructure (Instructor)"
        VM[Cloud Virtual Machine]
        Docker[Docker Container]
        Uvicorn[Uvicorn / SSE Server]
        CalcTool[Calculator Logic]
        
        VM --> Docker
        Docker --> Uvicorn
        Uvicorn --> CalcTool
    end

    subgraph "Student Machine"
        VSCode[VS Code + Continue]
        LLM[Local LLM / Ollama]
        NB[01_math_agent.ipynb]
    end

    VSCode -- "HTTP-SSE / Port 8000" --> Uvicorn
    NB -- "Standard Logic" --> OpenAI[OpenAI / API]
```

## Protocol Interaction Flow

When a student asks a math question, the following exchange occurs via the SSE protocol:

```mermaid
sequenceDiagram
    participant S as Student (VS Code)
    participant C as Cloud server (VM)
    participant T as Calculator Tool

    S->>C: GET /sse (Connect)
    C-->>S: SSE Stream Opened
    S->>C: POST /sse?sessionId=... (Initialize)
    C-->>S: JSON-RPC (Capabilites & ServerInfo)
    S->>C: POST /sse (tools/call: calculate)
    C->>T: eval(expression)
    T-->>C: Result (e.g., "42")
    C-->>S: JSON-RPC Result
    S->>S: Display "The answer is 42."
```

## Student Setup (config.yaml)

To connect to the cloud tool, update your `~/.continue/config.yaml` as follows:

```yaml
mcpServers:
  - name: cloud-calc
    type: sse
    url: http://<YOUR-VM-PUBLIC-IP>:8000/sse

experimental:
  autoExecuteTools: true
```

## Instructor Setup (Makefile)

Use the provided [Makefile](./Makefile) on your VM to manage the service easily:

| Command | Action |
| :--- | :--- |
| `make build` | Builds the `mcp-calculator` Docker image. |
| `make run` | Starts the server in background (detached) on port 8000. |
| `make logs` | Follows the live server logs (useful for debugging student connections). |
| `make stop` | Gracefully stops and removes the running container. |

### VM Security Note:
Ensure your VM's Cloud Firewall (Security Group) allows **Inbound TCP traffic on Port 8000**.

from fastapi import FastAPI, WebSocket
from agent_runtime import AgentRuntime

app = FastAPI()

agent_runtime = AgentRuntime("agent_001")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    print("Simulator Client conectado!")

    while True:

        message = await websocket.receive_text()

        print("Mensagem recebida:", message)

        perception = {
            "location": "office",
            "nearby": [
                "chair_1",
                "chair_2",
                "kitchen"
            ]
        }

        decision = agent_runtime.decide(perception)

        print("Decisão do agente:", decision)

        await websocket.send_json({
            "type": "command",
            "agent_id": agent_runtime.agent_id,
            "action": decision["action"]
        })

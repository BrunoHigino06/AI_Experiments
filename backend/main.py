from fastapi import FastAPI, WebSocket, WebSocketDisconnect


app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    print("Simulator Client conectado!")

    try:
        await websocket.send_json({
            "type": "command",
            "data": {
                "agent_id": "agent_001",
                "action": "move",
                "target": "kitchen"
            }
        })

        while True:
            message = await websocket.receive_text()

            print("Mensagem recebida:", message)

            await websocket.send_json({
                "type": "ack",
                "message": "Estado recebido"
            })
    except WebSocketDisconnect:
        print("Simulator Client desconectado!")
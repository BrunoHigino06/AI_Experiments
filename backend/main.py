from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    print("Simulator Client conectado!")

    try:
        while True:
            message = await websocket.receive_text()

            print("Mensagem recebida:", message)

            await websocket.send_text(
                f"Backend recebeu: {message}"
            )

    except WebSocketDisconnect:
        print("Simulator Client desconectado!")
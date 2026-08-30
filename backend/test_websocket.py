import asyncio
import websockets


async def main():
    uri = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(uri) as websocket:
        print("Conectado ao backend!")

        await websocket.send("hello backend")

        response = await websocket.recv()

        print("Resposta:", response)


asyncio.run(main())
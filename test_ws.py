# import asyncio
# import websockets

# TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMDY5YjY1YjYtYzRkZS00N2U3LWJhZTItNjBiZTcxZjEzYTA3In0.slOGR8mN60BE4UZYzXCBhqRXn9jP_nI5SE09vXskSag"

# async def test():
#     uri = f"ws://localhost:8000/ws?token={TOKEN}"

#     async with websockets.connect(uri) as websocket:
#         print("Connected!")

#         while True:
#             msg = await websocket.recv()
#             print(msg)

# asyncio.run(test())

import asyncio
import websockets

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzljZjg5NDAtYWQzYS00ZjA2LWE0ZjktMmUzYTUxODZmNTBhIn0.cjBeJFBtOCMKzzYPLdpOAypniyi6XKdpMUSUeoGZy2o"

async def test():
    uri = f"ws://localhost:8000/ws?token={TOKEN}"

    async with websockets.connect(uri) as websocket:

        print("Connected!")

        while True:
            msg = await websocket.recv()
            print("Received:", msg)

asyncio.run(test())
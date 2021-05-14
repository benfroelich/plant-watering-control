import time
import hardware
import asyncio
import os

HOST = "127.0.0.1"
PORT = os.environ["MANUAL_CONTROL_PORT"]

input_message = ""
status_output = ""

##### section for controlling hardware

#####

class TcpHandler:
    async def handle_tcp_packet(self, reader, writer):
        global input_message
        global status_output
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        if message.startswith("start"):
            input_message = message
            self.request_event.set()

        print(f"Received {message!r} from {addr!r}")

        print(f"Send: {message!r}")
        writer.write(status_output.encode())
        await writer.drain()

        print("Close the connection")
        writer.close()

#async def tcp_server():
#    server = await asyncio.start_server(
#                   handle_tcp_packet, '127.0.0.1', 
#                   os.environ["MANUAL_CONTROL_PORT"])
#
#    addr = server.sockets[0].getsockname()
#    print(f'Serving on {addr}')
#
#    async with server:
#        await server.serve_forever()

#def serve_tcp()
    
async def nag(request_event):
    global input_message
    global status_output
    while True:
        await request_event.wait()
        status_output = f'nag saw {input_message}'
        request_event.clear()

async def serve(request_event):
    handler = TcpHandler()
    handler.request_event = request_event
    server = await asyncio.start_server(
                   handler.handle_tcp_packet, '127.0.0.1', 
                   os.environ["MANUAL_CONTROL_PORT"])

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    await server.serve_forever()

async def main():
    request_event = asyncio.Event()
    server_task = asyncio.create_task(serve(request_event))
    nag_task = asyncio.create_task(nag(request_event))

    await server_task
    await nag_task

if __name__ == "__main__":
    asyncio.run(main())




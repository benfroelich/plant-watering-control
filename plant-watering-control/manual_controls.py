import time
import hardware
import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    print('Send: {message!r}'.format(message))
    writer.write(message.encode())

    data = await reader.read(100)
    print('Received: {data.decode()!r}'.format(data.decode()))

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client('Hello World!'))

def requested():
    print("checking for a request for manual controls")

def run():
    print("running manual controls")
    time.sleep(2)
    print("ending manual controls")




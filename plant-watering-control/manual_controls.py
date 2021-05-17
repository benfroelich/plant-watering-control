import time
import datetime
import hardware
import asyncio
import os
import json

HOST = "127.0.0.1"
PORT = os.environ["MANUAL_CONTROL_PORT"]

##### section for controlling hardware

    #hardware.relay_chs[relay_ch].on()
#####

class TcpHandler:
    async def handle_tcp_packet(self, reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        
        await self.process_request(message),
        status_output = await self.get_status()

        print(f'Received {message!r} from {addr!r}')

        print(f'Send: {message!r}')
        writer.write(status_output.encode())
        await writer.drain()
        writer.close()

    async def get_status(self):
        status_output = f'time is {datetime.datetime.now()}'
        return status_output
        
    async def process_request(self, request):
        print(f'process_request: {request}')
        if request.startswith('start'):
            self.pause_schedule_event.set()
            print('pausing schedule')
        if request.startswith('stop'):
            self.pause_schedule_event.clear()
            print('unpausing schedule')
        print(f'process_request done')

async def serve(pause_schedule_event):
    handler = TcpHandler()
    handler.pause_schedule_event = pause_schedule_event
    server = await asyncio.start_server(
                   handler.handle_tcp_packet, '127.0.0.1', 
                   os.environ["MANUAL_CONTROL_PORT"])

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    await server.serve_forever()

async def nag(pause_event):
    while True:
        await asyncio.sleep(1)
        if pause_event.is_set(): print('not running sched')
        else: print('running sched')

async def main():
    pause_schedule_event = asyncio.Event()
    await asyncio.gather(
        serve(pause_schedule_event),
        nag(pause_schedule_event)
    )

if __name__ == "__main__":
    asyncio.run(main())




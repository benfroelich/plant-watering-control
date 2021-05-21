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
    # TODO: only allow relays to turn on/off when scheduler is paused
    # or just pause the scheduler first
    async def handle_tcp_packet(self, reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        
        resp = await self.process_request(message),
        status_output = await self.get_status(resp)

        print(f'received {message!r} from {addr!r}')

        writer.write(status_output.encode())
        await writer.drain()
        writer.close()

    async def get_status(self, resp):
        status_output = f'status: {resp}'
        return status_output
        
    async def process_request(self, message):
        resp = 'no response'
        try:
            request = json.loads(message)
        except json.decoder.JSONDecodeError:
            print("deflecting json decoding error")
            resp = f'could not decode JSON \'{message}\''
        else:
            if request['action'] == 'start':
                self.pause_schedule_event.set()
                resp = 'pausing scheduler'
            elif request['action'] == 'stop':
                self.pause_schedule_event.clear()
                resp = 'unpausing scheduler'
            elif request['action'] == 'output':
                if 'ch' in request and 'state' in request:
                    rly = hardware.relay_chs[request['ch']]
                    if request['state'] == 'on': rly.on()
                    if request['state'] == 'off': rly.off()
                    resp = f'ch {request["ch"]} {request["state"]}'
                else: resp = f'''could not proccess \'{request}\': action == 
                             output requires ch and state'''
        return resp

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




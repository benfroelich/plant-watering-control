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
        
        resp = await self.process_request(message)
        print(resp)

        print(f'received {message!r} from {addr!r}')

        writer.write(resp.encode())
        await writer.drain()
        writer.close()
        
    async def process_request(self, message):
        m = hardware.relay_chs[0]
        if m.is_lit: m.off()
        else: m.on()
        resp = {}
        try:
            request = json.loads(message)
        except json.decoder.JSONDecodeError:
            print("deflecting json decoding error")
            resp['result'] = f'could not decode JSON \'{message}\''
        else:
            if request['action'] == 'start':
                self.pause_schedule_event.set()
                resp['result'] = 'paused scheduler'
            elif request['action'] == 'stop':
                self.pause_schedule_event.clear()
                resp['result'] = 'unpaused scheduler'
            elif request['action'] == 'output':
                if 'ch' in request and 'state' in request:
                    try:
                        ch = int(request['ch'])
                        rly = hardware.relay_chs[ch]
                    except ValueError:
                        resp['result'] = f'invalid channel string \'{request["ch"]}\''
                    except IndexError:
                        resp['result'] = f'channel {request["ch"]} out of bounds'
                    else:
                        if request['state'] == 'on': rly.on()
                        if request['state'] == 'off': rly.off()
                        resp['result'] = f'ch {request["ch"]} {request["state"]}'
                else: resp['result'] = f'''could not proccess \'{request}\': 
                                           action == output requires ch and state'''
            elif request['action'] == 'get-status':
                resp['result'] = 'returning current status'
                resp['output'] = {}
                for i,ch in enumerate(hardware.relay_chs):
                    resp['output'][f'ch{i}'] = 'on' if ch.is_lit else 'off'
                resp['moisture'] = {}
                for i,ch in enumerate(hardware.moisture_chs):
                    resp['moisture'][f'ch{i}'] = f'{ch.read_moisture()} %'
                resp['reservoir'] = f'{hardware.reservoir_ch.read_moisture()} %'

        return json.dumps(resp)

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




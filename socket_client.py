import asyncio


class SocketAsyncClient(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
    async def run(self, number):
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        outcome_message = 'Test message from socket {0}'.format(number).encode()
        writer.write(outcome_message)
        await writer.drain()
        income_message = await reader.read(1024)
        if outcome_message == income_message:
            print('{0} successeded!'.format(number))
        else:
            print('False')
        writer.close()
        await writer.wait_closed()


if __name__ == '__main__':
    socket_client = SocketAsyncClient('127.0.0.1', 8888)
    for num in range(5):
        asyncio.run(socket_client.run(num))
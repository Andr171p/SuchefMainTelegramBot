import aiohttp

import asyncio

from backend.server1C.webhook_api import WebHookRequestsHeaders
from backend.server1C.webhook_api import WebHookAPI

from misc.format_data import format_phone_number


class Server1CRequests:
    def __init__(self):
        self.url = WebHookRequestsHeaders.url
        self.headers = WebHookRequestsHeaders.headers
        self.webhook_api_commands = WebHookAPI

    async def post_request(self, data, timeout=30):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=self.url,
                        headers=self.headers,
                        json=data,
                        timeout=timeout
                ) as response:
                    print(response.status)
                    if self.is_OK(response):
                        return await response.json()
        except Exception as _ex:
            print(f"ERROR FROM SERVER: {_ex}")

    @staticmethod
    def is_OK(response):
        response_status = response.status
        if response_status == 200:
            return True
        else:
            return False

    async def get_order_response(self, phone_number):
        telefon = format_phone_number(
            phone_number=phone_number
        )
        data = {
            'command': f'{self.webhook_api_commands.order_status_command}',
            'telefon': f'{telefon}'
        }
        response = await self.post_request(
            data=data
        )
        return response

    async def get_orders_response(self):
        data = {
            'command': f'{self.webhook_api_commands.all_orders_status_command}',
            'active': 'true'
        }
        response = await self.post_request(
            data=data
        )
        return response

    async def get_flyer_response(self, phone_number):
        telefon = format_phone_number(
            phone_number=phone_number
        )
        data = {
            'command': f'{self.webhook_api_commands.flyer_command}',
            'telefon': f'{telefon}',
            'project': 'Сушеф.рф'
        }
        response = await self.post_request(
            data=data
        )
        return response

    async def get_orders_history(self, phone_number):
        telefon = format_phone_number(
            phone_number=phone_number
        )
        data = {
            'command': f'{self.webhook_api_commands.orders_history_command}',
            'telefon': f'{telefon}',
            'project': 'Сушеф.рф'
        }
        response = await self.post_request(
            data=data
        )
        return response


r = asyncio.run(Server1CRequests().get_orders_response())
print(r)
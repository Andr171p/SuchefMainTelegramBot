import json

from backend.server1C.webhook_exchange import WebHookRequests1C


class MyFlyerStatus:
    def __init__(self, client_phone_number):
        # client phone number:
        self.client_phone_number = client_phone_number
        # response flyer status:
        self.response = None

    def data_from_json_response(self):
        flyer_json = json.dumps(
            self.response,
            ensure_ascii=False
        )
        flyer_dict = json.loads(flyer_json)


wh = WebHookRequests1C()
print(wh.get_flyer_response(phone_number='9224870400'))
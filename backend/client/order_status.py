import asyncio

import json

from backend.server1C.webhook_exchange import Server1CRequests

from misc.format_data import format_phone_number, format_order_number
from misc.format_data import format_order_date, format_order_time, format_trade_card


class TriggerOrdersStatus:
    trigger_order_status = [
        "Принят оператором",
        "Передан курьеру",
        "Готов для выдачи"
    ]


class PrettyStatus:
    def __init__(self, order):
        self.status = order['status']
        self.number = order['number']
        self.delivery_time_from = order['delivery_time_from']
        self.delivery_time_to = order['delivery_time_to']
        self.amount = order['amount']
        self.pay_status = order['pay_status']
        self.cooking_time_to = order['cooking_time_to']
        self.trade_point = order['trade_point']
        self.delivery_method = order['delivery_method']
        self.date = order['date']
        self.trade_point_card = order['trade_point_card']
        self.delivery_adress = order['delivery_adress']

    def pretty_pay_status(self):
        if self.pay_status == 'CONFIRMED':
            return 'оплачен'
        else:
            return 'не оплачен'

    def message(self):
        match self.status:
            case StatusMessage.accepted_operator:
                if self.delivery_method == 'Курьер':
                    message = (f"Ваш заказ №{self.number} принят и будет\n"
                               f"доставлен {self.date} с {self.delivery_time_from} до {self.delivery_time_to} по адресу\n"
                               f"{self.delivery_adress}."
                               f"Сумма: {self.amount} руб.")
                    return message
                else:
                    message = (f"Ваш заказ №{self.number} принят и будет\n"
                               f"готов к выдаче {self.date} с {self.delivery_time_from} до {self.delivery_time_to} по адресу {self.trade_point}.")
                    return message
            case StatusMessage.transferred_to_the_kitchen:
                message = (f"Ваш заказ №{self.number} {self.pretty_pay_status()} и\n"
                           f"передан на кухню")
                return message
            case StatusMessage.prepare:
                message = (f"Ваш заказ №{self.number} {self.pretty_pay_status()} и\n"
                           f"уже готовиться. Время готовности {self.cooking_time_to}")
                return message
            case StatusMessage.cooked:
                message = (f"Ваш заказ №{self.number} {self.pretty_pay_status()}\n"
                           f"и уже приготовлен. Мы начинаем его готовить к отправке.")
                return message
            case StatusMessage.staffed:
                message = (f"Ваш заказ №{self.number} {self.pretty_pay_status()} и\n"
                           f"готов к отправке.")
                return message
            case StatusMessage.sent_to_courier:
                message = (f"Ваш заказ №{self.number} {self.pretty_pay_status()}\n"
                           f"и передан курьеру. Ожидайте доставку с {self.delivery_time_from} до {self.delivery_time_to}\n"
                           f"по адресу:\n"
                           f"{self.delivery_adress}")
                return message
            case StatusMessage.delivered:
                message = (f"Ваш заказ №{self.number} доставлен курьером.\n"
                           f"Спасибо, сто воспользовались услугами нашего сервиса.")
                return message
            case StatusMessage.ready_for_pickup:
                message = (f"Ваш заказ {self.number} {self.pretty_pay_status()}\n"
                           f"ожидает вас по адресу: {self.trade_point}\n"
                           f"{self.trade_point_card}")
                return message
            case StatusMessage.finished:
                message = (f"Ваш заказ №{self.number} успешно завершен. Спасибо,  что\n"
                           f"воспользовались услугами нашего сервиса.\n"
                           f"\n"
                           f"Мы очень старались оставить о нас приятное впечатление\n"
                           f"и будем признательны, если Вы оставите честный отзыв о\n"
                           f"нашей работе в 2ГИС {self.trade_point_card}. Никаких бонусов и\n"
                           f"подарков мы не предлагаем, нам важна справедливая оценка. ")
                return message
            case StatusMessage.canceled:
                message = (f"Ваш заказ №{self.number} отменен. Нам очень жаль. Надеемся,\n"
                           f"на скорую встречу.")
                return message


class StatusMessage:
    accepted_operator = "Принят оператором"
    transferred_to_the_kitchen = "Передан на кухню"
    prepare = "Готовится"
    cooked = "Приготовлен"
    staffed = "Укомплектован"
    ready_for_pickup = "Готов для выдачи"
    sent_to_courier = "Передан курьеру"
    delivered = "Доставлен"
    finished = "Завершен"
    canceled = "Отменен"


class OrdersAtTheMoment:
    def __init__(self):
        self.response = None

    async def response_from_server(self):
        self.response = await Server1CRequests().get_orders_response()

    def extract_data_from_json(self):
        if self.response is not None:
            _json = json.dumps(self.response, ensure_ascii=False)
            _dict = json.loads(_json)
            orders = _dict['data']['orders']
            return orders
        else:
            return -1

    @staticmethod
    def filter_project(orders, project='Дисконт Суши'):
        _orders = orders.copy()
        result = []
        for order in _orders:
            if order['project'] != project:
                order['phones'] = order['phones'][0]
                # format dict:
                phone_number = order.pop('phones')
                final = {
                    'phone_number': phone_number
                }
                final.update(order)
                result.append(final)
        return result

    @staticmethod
    def format_data(data):
        for order in data:
            order['phone_number'] = format_phone_number(order['phone_number'])
            order['number'] = format_order_number(order['number'])
            order['date'] = format_order_date(order['date'])
            order['cooking_time_from'] = format_order_time(order['cooking_time_from'])
            order['cooking_time_to'] = format_order_time(order['cooking_time_to'])
            order['delivery_time_from'] = format_order_time(order['delivery_time_from'])
            order['delivery_time_to'] = format_order_time(order['delivery_time_to'])
            order['trade_point_card'] = format_trade_card(order['trade_point_card'])
        return data

    async def orders_at_the_moment(self):
        await self.response_from_server()
        orders = self.extract_data_from_json()
        if orders != -1:
            result = self.filter_project(orders=orders)
            result = self.format_data(data=result)
            print("********************************************************************")
            print(result)
            return result


'''async def main():
    o = OrdersAtTheMoment()
    result = await o.orders_at_the_moment()
    print(result)


asyncio.run(main())'''


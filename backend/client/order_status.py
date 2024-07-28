import asyncio
import json

from backend.server1C.webhook_exchange import Server1CRequests
# from backend.database.today_orders_db.db_orders_manage import OrdersEngineDB


class OrdersData:
    def __init__(self):
        self.orders_data = {
            'phone_number': [],
            'client': [],
            'number': [],
            'date': [],
            'status': [],
            'amount': [],
            'pay_link': [],
            'pay_status': [],
            'cooking_time_from': [],
            'cooking_time_to': [],
            'delivery_time_from': [],
            'delivery_time_to': [],
            'project': [],
            'trade_point': [],
            'trade_point_card': [],
            'delivery_method': [],
            'delivery_adress': []
        }

    def clear_values(self):
        for value in self.orders_data.values():
            del value[:]

    def is_empty(self):
        states = []
        for value in self.orders_data.values():
            if value:
                states.append(0)
            else:
                states.append(1)
        if len(self.orders_data) == sum(states):
            return True
        else:
            return False

    def add_order_parameters(self, order):
        self.orders_data['client'].append(order['client'])
        self.orders_data['number'].append(order['number'])
        self.orders_data['date'].append(order['date'])
        self.orders_data['status'].append(order['status'])
        self.orders_data['amount'].append(order['amount'])
        self.orders_data['pay_link'].append(order['pay_link'])
        self.orders_data['pay_status'].append(order['pay_status'])
        self.orders_data['cooking_time_from'].append(order['cooking_time_from'])
        self.orders_data['cooking_time_to'].append(order['cooking_time_to'])
        self.orders_data['delivery_time_from'].append(order['delivery_time_from'])
        self.orders_data['delivery_time_to'].append(order['delivery_time_to'])
        self.orders_data['project'].append(order['project'])
        self.orders_data['trade_point'].append(order['trade_point'])
        self.orders_data['trade_point_card'].append(order['trade_point_card'])
        self.orders_data['delivery_method'].append(order['delivery_method'])
        self.orders_data['delivery_adress'].append(order['delivery_adress'])

    def add_phones_order_data(self, order):
        phones = order['phones']
        length = len(phones)
        if length != 1:
            for i in range(length):
                self.orders_data['phone_number'].append(phones[i])
                self.add_order_parameters(
                    order=order
                )
        else:
            self.orders_data['phone_number'].append(phones[0])
            self.add_order_parameters(
                order=order
            )


class TriggerOrdersStatus:
    trigger_order_status = [
        "Принят оператором",
        "Передан курьеру",
        "Готов для выдачи"
    ]


class PrettyStatus:
    def __init__(self,
                 status,
                 number,
                 delivery_time_from,
                 delivery_time_to,
                 amount,
                 pay_status,
                 cooking_time_to,
                 trade_point,
                 delivery_method,
                 date,
                 trade_point_card,
                 delivery_adress
                 ):
        self.status = status
        self.number = number
        self.delivery_time_from = delivery_time_from
        self.delivery_time_to = delivery_time_to
        self.amount = amount,
        self.pay_status = pay_status
        self.cooking_time_to = cooking_time_to
        self.trade_point = trade_point
        self.delivery_method = delivery_method
        self.date = date
        self.trade_point_card = trade_point_card
        self.delivery_adress = delivery_adress

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


def pretty_message_from_response(order_data):
    pretty_status = PrettyStatus(
        status=order_data['status'],
        number=order_data['number'],
        delivery_time_from=order_data['delivery_time_from'],
        delivery_time_to=order_data['delivery_time_to'],
        amount=order_data['amount'],
        pay_status=order_data['pay_status'],
        cooking_time_to=order_data['cooking_time_to'],
        trade_point=order_data['trade_point'],
        delivery_method=order_data['delivery_method'],
        date=order_data['date'],
        trade_point_card=order_data['trade_point_card'],
        delivery_adress=order_data['delivery_adress']
    )

    message = pretty_status.message()

    return message


class OrdersAtTheMoment:
    def __init__(self):
        self.response = None

    async def response_from_server(self):
        self.response = await Server1CRequests().get_orders_response()

    def extract_data_from_json(self):
        _json = json.dumps(self.response, ensure_ascii=False)
        _dict = json.loads(_json)
        orders = _dict['data']['orders']
        return orders

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

    async def orders_at_the_moment(self):
        await self.response_from_server()
        orders = self.extract_data_from_json()
        result = self.filter_project(
            orders=orders
        )
        return result


async def main():
    o = OrdersAtTheMoment()
    result = await o.orders_at_the_moment()
    print(result)


asyncio.run(main())


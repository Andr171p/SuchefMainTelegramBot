class RowWrapper:
    def __init__(self, data):
        self.data = data
        self.keys = list(data[0].keys())
        '''self.keys.pop(0)
        self.keys.pop(-1)
        self.keys.insert(0, 'phone_number')'''

    def create_tuple(self, row):
        _tuple = tuple()
        for i in range(len(self.keys)):
            _tuple += (row[self.keys[i]],)
        return _tuple

    def create_matrix(self):
        matrix = [
            self.create_tuple(
                row=row
            ) for row in self.data
        ]
        return matrix


d = [{'phone_number': '9088777711', 'client': 'Савельева Любовь', 'number': 'БТ-074232', 'date': '2024-07-26T00:00:00', 'status': 'Принят оператором', 'amount': 1880, 'pay_link': 'https://securepayments.tinkoff.ru/TRHWK9LI', 'pay_status': 'NEW', 'cooking_time_from': '0001-01-01T00:00:00', 'cooking_time_to': '0001-01-01T13:25:00', 'delivery_time_from': '0001-01-01T13:30:00', 'delivery_time_to': '0001-01-01T14:00:00', 'project': 'Сушеф.рф', 'trade_point': 'Московский тракт, 87к1', 'trade_point_card': "MockoBcku'u TpakT 87 k.1 https://go.2gis.com/pdacd", 'delivery_method': 'Самовывоз', 'delivery_adress': ''}, {'phone_number': '9829714372', 'client': 'Ольга', 'number': '00НФ-007378', 'date': '2024-07-26T00:00:00', 'status': 'Принят оператором', 'amount': 1854, 'pay_link': 'https://securepayments.tinkoff.ru/1MxM8zIK', 'pay_status': 'FORM_SHOWED', 'cooking_time_from': '0001-01-01T00:00:00', 'cooking_time_to': '0001-01-01T09:50:00', 'delivery_time_from': '0001-01-01T09:55:00', 'delivery_time_to': '0001-01-01T10:00:00', 'project': 'Сушеф.рф', 'trade_point': 'Московский тракт, 87к1', 'trade_point_card': "MockoBcku'u TpakT 87 k.1 https://go.2gis.com/pdacd", 'delivery_method': 'Самовывоз', 'delivery_adress': ''}, {'phone_number': '9829878254', 'client': 'Юлия', 'number': 'БТ-074093', 'date': '2024-07-28T00:00:00', 'status': 'Принят оператором', 'amount': 1537, 'pay_link': 'https://securepayments.tinkoff.ru/RZr49tBu', 'pay_status': 'DEADLINE_EXPIRED', 'cooking_time_from': '0001-01-01T00:00:00', 'cooking_time_to': '0001-01-01T13:40:00', 'delivery_time_from': '0001-01-01T14:00:00', 'delivery_time_to': '0001-01-01T14:20:00', 'project': 'Сушеф.рф', 'trade_point': 'Велижанская, 66 к1', 'trade_point_card': 'BeJIu}I{aHcka9I 66 k.1 https://go.2gis.com/eg0zzr', 'delivery_method': 'Самовывоз', 'delivery_adress': ''}]
r = RowWrapper(data=d)
print(r.keys)
print(len(r.keys))
print(r.create_matrix())

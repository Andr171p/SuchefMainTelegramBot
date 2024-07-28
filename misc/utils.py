class DataUtils:
    @staticmethod
    def values_from_key(data, key):
        values = {row[key] for row in data}
        return values

    def intersection_list(self, data, new_data, key):
        old_values_from_key = self.values_from_key(
            data=data,
            key=key
        )
        result = [row for row in new_data if row[key] in old_values_from_key]
        return result

    def subtract_list(self, data, new_data, key):
        old_values_from_key = self.values_from_key(
            data=data,
            key=key
        )
        result = [row for row in new_data if row[key] not in old_values_from_key]
        return result


arr = [
    {'n': '123', 'h': 45},
    {'n': '567', 'h': 111}
]
new_arr = [
    {'n': '123', 'h': 47},
    {'n': '56', 'h': 111},
    {'n': '123', 'h': 77}
]
print(DataUtils().subtract_list(data=new_arr, new_data=arr, key='n'))
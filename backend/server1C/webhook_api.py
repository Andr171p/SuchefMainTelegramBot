class WebHookRequestsHeaders:
    url = 'https://noname-sushi.online/web/hs/hook?token=NTAxNGVhNWMtZTUwYi00NTdjLTk5NTctNmIyMmM2N2U5NzRh'
    headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }


class WebHookAPI:
    order_status_command = 'status'
    all_orders_status_command = 'statuses'
    flyer_command = 'bonus'
    orders_history_command = 'history'

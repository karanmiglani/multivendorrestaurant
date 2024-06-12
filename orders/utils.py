import datetime


def generate_order_number(request,pk):
    current_date_time = datetime.datetime.now().strftime('%Y%m%d%M%S')
    order_number = current_date_time + str(pk) + str(request.user.id)
    return order_number


def generate_transaxtion_id(request):
    current_date_time = datetime.datetime.now().strftime('%Y%m%d%M%S')
    txn_id = 'TXN-' + current_date_time + '-' + str(request.user.id)
    return txn_id
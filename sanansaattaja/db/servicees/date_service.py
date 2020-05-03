def get_date(datetime):
    months = ['January', 'February', 'March', 'April',
              'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December']
    date = months[datetime.month - 1] + ' ' + str(datetime.day) + ', ' + str(datetime.year)
    time = ' at ' + str(datetime.hour) + ':' + str(datetime.minute)
    return date + time
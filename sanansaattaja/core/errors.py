class ClientError(Exception):
    def __init__(self, msg='Client Error', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = msg

    def __str__(self):
        return self.msg


class IdError(ClientError):
    def __init__(self, msg='Wrong ID', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = msg

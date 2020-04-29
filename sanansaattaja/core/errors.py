class BaseError(Exception):
	def __init__(self, msg='Error', *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.msg = msg

	def __str__(self):
		return self.msg


class UserError(BaseError):
	def __init__(self, msg='User error', *args, **kwargs):
		super().__init__(msg=msg, *args, **kwargs)


class PhotoError(BaseError):
	def __init__(self, msg='Photo error', *args, **kwargs):
		super().__init__(msg=msg, *args, **kwargs)
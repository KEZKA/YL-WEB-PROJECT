from sanansaattaja.core.errors import PhotoError
from sanansaattaja.website.forms.users_filter_form import FilterForm

MAX_FILE_SIZE = 1024 ** 2


def get_photo_from_request(request):
    if request.files['photo']:
        filename = request.files['photo'].filename
        if filename.split('.')[-1].lower() not in ('jpg', 'png', 'gif'):
            raise PhotoError(msg="Invalid extension of image")
        file = request.files['photo'].read(MAX_FILE_SIZE)
        if len(file) == MAX_FILE_SIZE:
            return PhotoError(msg="File size is too large")
    else:
        file = None
    return file


def get_data_from_filter_form(form: FilterForm):
    params = ['filter=True']
    if form.email.data != '':
        params.append(f'email={form.email.data}')
    if form.name.data != '':
        params.append(f'name={form.name.data}')
    if form.surname.data != '':
        params.append(f'surname={form.surname.data}')
    if form.sex.data != 'all':
        params.append(f'sex={form.sex.data}')
    if form.age.data is not None:
        params.append(f'age={form.age.data}')
    if len(params) == 1:
        return 'filter=False'
    return '&'.join(params)

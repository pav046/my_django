
menu = [
        {'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'addpage'},
        {'title': 'Обратная связь', 'url_name': 'contact'}
    ]

class DataMixin:
    paginate_by = 5
    title = None
    cat_id = None
    extra_context = {}

    def __init__(self):
        self.extra_context.clear()
        if self.title:
            self.extra_context['title'] = self.title
        if self.cat_id is not None:
            self.extra_context['cat_id'] = self.cat_id


    def get_mixin_context(self, context, **kwargs):
        context['title'] = kwargs['title'] if 'title' in kwargs else self.title
        context['cat_id'] = kwargs['cat_id'] if 'cat_id' in kwargs else self.cat_id
        context.update(kwargs)
        return context
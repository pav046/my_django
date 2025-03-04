from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from women.utils import DataMixin
from women.forms import AddMyPostForm, AddFilesForm
from women.models import Women, TagPost

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'addpage'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'}
]

# def write_file(file):
#     with open(f"uploads/{file.name.split('.')[0]}_{datetime.now().strftime('%d.%m.%Y_%H-%M-%S')}.{file.name.split('.')[1]}", "wb+") as my_file:
#         for chunk in file.chunks():
#             my_file.write(chunk)

# def index(request, cat_id=0):
#     # t = render_to_string('women/index.html')
#     post = Women.published.all().select_related('cat')
#     data = {'title': 'Главная страница',
#             'menu': menu,
#             # 'data_bd': data_bd,
#             'cat_id': cat_id,
#             'post': post
#             }
#
#     return render(request, 'women/index.html', data)


class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    # model = Women
    context_object_name = 'post'
    title = 'Главная страница'
    cat_id = 0

    # extra_context = {
    #         'title': 'Главная страница',
    #         'menu': menu,
    #         'cat_id': 0,
    #         }

    def get_queryset(self):
        return Women.published.all().select_related('cat')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['post'] = Women.published.all().select_related('cat')
    #     context['cat_id'] = int(self.request.GET.get('cat_id', 0))
    #     return context


def about(request):
    if request.method == 'POST':
        form = AddFilesForm(request.POST, request.FILES)
        if form.is_valid():
            # fp = UploadFiles(file=form.cleaned_data['file'])
            form.save()
    else:
        form = AddFilesForm()
    data = {'title': 'О сайте', 'describe': 'О нас', 'menu': menu, 'form': form}
    return render(request, 'women/about.html', data)

# def post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     data = {'title': f'{post.title}',
#             'menu': menu,
#             'post': post,
#             'cat_id': None
#             }
#     return render(request, 'women/post.html', data)

class ShowPost(DetailView):
    template_name = 'women/post.html'
    # model = Women
    # slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs['post_slug'])



def contact(request):
    return HttpResponse(f"Контактная информация")

# def addpage(request):
#     if request.method == 'POST':
#         form = AddMyPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #     print(form.cleaned_data)
#             #     try:
#             #         Women.objects.create(**form.cleaned_data)
#                     return redirect('home')
#             #     except:
#             #         form.add_error(None, "Ошибка добавления поста")
#             form.save()
#             return redirect('home')
#     else:
#         form = AddMyPostForm()
#
#     data = {
#         'title': 'Добавить статью',
#         'menu': menu,
#         'form': form
#     }
#     return render(request, 'women/addpage.html', data)


# class AddPage(View):
#     def get(self, request):
#         form = AddMyPostForm()
#         data = {
#             'title': 'Добавить статью',
#             'menu': menu,
#             'form': form
#         }
#         return render(request, 'women/addpage.html', data)
#
#     def post(self, request):
#         if request.method == 'POST':
#             form = AddMyPostForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 return redirect('home')
#             data = {
#                 'title': 'Добавить статью',
#                 'menu': menu,
#                 'form': form
#             }
#             return render(request, 'women/addpage.html', data)

# class AddPage(FormView):
#     form_class = AddMyPostForm
#     template_name = 'women/addpage.html'
#     success_url = reverse_lazy('home')
#     extra_context = {'title': 'Добавить статью', 'menu': menu}
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

class AddPage(CreateView):
    form_class = AddMyPostForm
    model = Women
    # fields = '__all__'
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Добавить статью', 'menu': menu}





class UpdatePage(UpdateView):
    # form_class = AddMyPostForm
    model = Women
    fields = ['title', 'content', 'slug', 'cat', 'photo', 'is_published']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Редактировать статью', 'menu': menu}


class DeletePage(DeleteView):
    model = Women
    success_url = reverse_lazy('home')
    template_name = 'women/addpage.html'
    extra_context = {'title': 'Удалить статью', 'menu': menu}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удалить статью {Women.objects.get(slug=self.kwargs["slug"]).title}?'
        return context



# def categories(request, cat_slug):
#     category = Category.objects.get(slug=cat_slug)
#     post = Women.published.filter(cat_id=category.id).select_related('cat')
#     data = {
#         'title': f"Рубрика {category.name}",
#         'post': post,
#         'menu': menu,
#         'cat_id': category.id
#     }
#     return render(request, 'women/index.html', data)


class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'post'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['post'][0].cat
        context['title'] = f"Категория - {cat.name}"
        context['menu'] = menu
        context['cat_id'] = cat.pk
        return context


# def tag(request, tag_slug):
#     cur_tag = get_object_or_404(TagPost, slug=tag_slug)
#     post = cur_tag.your_tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
#     data = {
#         'title': f'Тег: {cur_tag.tag}',
#         'post': post,
#         'menu': menu,
#         'cat_id': None
#     }
#     return render(request, 'women/index.html', data)

class WomenTag(ListView):
    template_name = 'women/index.html'
    context_object_name = 'post'
    allow_empty = False

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        cur_tag = get_object_or_404(TagPost, slug=tag_slug)
        return cur_tag.your_tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['tag_slug']
        cur_tag = get_object_or_404(TagPost, slug=tag_slug)
        context['title'] = f"Тег: {cur_tag.tag}"
        context['menu'] = menu
        context['cat_id'] = None
        return context


def login(request):
    return HttpResponse(f"Войти")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страничечка не найдена :((</h1>")
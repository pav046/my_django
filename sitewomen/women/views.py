from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView, FormView
from django.core.cache import cache

from women.utils import DataMixin
from women.forms import AddMyPostForm, ContactForm
from women.models import Women, TagPost


class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'post'
    title = 'Главная страница'
    cat_id = 0

    def get_queryset(self):
        w_lst = cache.get('women_posts')
        if not w_lst:
            w_lst = Women.published.all().select_related('cat')
            cache.set('women_posts', w_lst, 1)
        return w_lst


@login_required(login_url='users:login')
def about(request):
    qs = Women.published.all()
    paginator = Paginator(qs, 3)
    page = paginator.page(request.GET.get('page', 1))
    page_range = paginator.page_range

    data = {'title': 'О сайте', 'describe': 'О нас', 'page': page, 'page_range': page_range}
    return render(request, 'women/about.html', data)


class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs['post_slug'])



# @permission_required(perm='women.view_women', raise_exception=True)
# def contact(request):
#     return HttpResponse(f"Контактная информация")

class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = "women/contact.html"
    success_url = reverse_lazy("home")
    title_page = "Обратная связь"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)



class AddPage(PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddMyPostForm
    model = Women
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title = 'Добавить статью'
    permission_required = ['women.add_women']

    def form_valid(self, form):
        m = form.save(commit=False)
        m.author = self.request.user
        return super().form_valid(form)



class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'slug', 'cat', 'photo', 'is_published']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title = 'Редактировать статью'
    permission_required = 'women.change_women'


class DeletePage(DataMixin, DeleteView):
    model = Women
    success_url = reverse_lazy('home')
    template_name = 'women/addpage.html'
    title = 'Удалить статью'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f'Удалить статью {Women.objects.get(slug=self.kwargs["slug"]).title}?')


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'post'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['post'][0].cat
        return self.get_mixin_context(context, title=f"Категория - {cat.name}", cat_id=cat.pk)


class WomenTag(DataMixin, ListView):
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
        return self.get_mixin_context(context, title=f"Тег: {cur_tag.tag}")

def login(request):
    return HttpResponse(f"Войти")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страничечка не найдена :((</h1>")
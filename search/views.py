import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Post
from .forms import SearchForm, PostForm
from django.db.models import Q
from django.shortcuts import render, redirect, reverse

logger = logging.getLogger('development')


class IndexView(LoginRequiredMixin, generic.ListView):

    paginate_by = 5
    template_name = 'search/index.html'
    model = Post

    def post(self, request, *args, **kwargs):

        form_value = [
            self.request.POST.get('title', None),
            self.request.POST.get('text', None),
        ]
        request.session['form_value'] = form_value

        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        title = ''
        text = ''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            title = form_value[0]
            text = form_value[1]

        default_data = {'title': title,  # タイトル
                        'text': text,  # 内容
                        }

        test_form = SearchForm(initial=default_data) # 検索フォーム
        context['test_form'] = test_form

        return context

    def get_queryset(self):

        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            title = form_value[0]
            text = form_value[1]

            # 検索条件
            condition_title = Q()
            condition_text = Q()

            if len(title) != 0 and title[0]:
                condition_title = Q(title__icontains=title)
            if len(text) != 0 and text[0]:
                condition_text = Q(text__contains=text)

            return Post.objects.select_related().filter(condition_title & condition_text)
        else:
            # 何も返さない
            return Post.objects.none()


class CreateView(generic.CreateView):
    # 登録画面
    model = Post
    form_class = PostForm

    def get_success_url(self):  # 詳細画面にリダイレクトする。
        return reverse('search:detail', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['initial'] = {'author': self.request.user}  # フォームに初期値を設定する。
        return form_kwargs


class DetailView(generic.DetailView):
    # 詳細画面
    model = Post
    template_name = 'search/detail.html'

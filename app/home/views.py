from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View
from .models import Procedure, Tag, CustomUser, User
from .forms import QuestionsForm, CustomUserEditForm, UserEditForm, CustomUserCreateForm, UserCreateForm


class ProcedureView(ListView):
    """Список процедур"""
    model = Procedure
    queryset = Procedure.objects.filter(unpublished=False)

    # template_name = "home/procedure_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Главная страница'
        context['active_tab'] = "procedures"
        return context


class ProcedureOldView(View):
    """Список процедур старая версия"""

    def get(self, request):
        procedures = Procedure.objects.all()
        data = dict()
        data['title'] = 'Главная страница'
        data['active_tab'] = request.session.get('active_tab')
        data['procedures'] = procedures
        return render(request, 'home/procedure_list.html', data)


class ProcedureDetailView(DetailView):
    """Полное описание процедуры"""
    model = Procedure
    slug_field = "url"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Информация о процедуре'
        context['active_tab'] = "procedures"
        return context


class ProcedureOLDDetailView(View):
    """Полное описание процедуры СТАРАЯ"""

    def get(self, request, slug):
        procedure = Procedure.objects.get(url=slug)
        data = dict()
        data['title'] = 'Информация о процедуре'
        data['active_tab'] = request.session.get('active_tab')
        data['procedure'] = procedure
        return render(request, 'home/procedure_detail.html', data)


def index(request):
    request.session['active_tab'] = "home"
    return render(request, 'home/index.html', context={
        'title': 'Главная страница',
        'active_tab': request.session.get('active_tab'),
    })


class AddQuestion(View):
    """Добавление отзыва"""

    def post(self, request, pk):
        form = QuestionsForm(request.POST)
        pr = Procedure.objects.get(id=pk)
        if form.is_valid():

            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.procedure = pr
            form.save()
        return redirect(pr.get_absolute_url())


class TagView(DetailView):
    """Вывод процедуры по тэгу"""
    model = Tag
    slug_field = "url"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Поиск по тэгу'
        context['active_tab'] = "tag"
        return context


def SignUpView(request):
    if request.method == 'GET':
        return render(request, "home/register.html", {
            'user_form': UserCreateForm,
            'customer_form': CustomUserCreateForm
        })

    elif request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        customer_form = CustomUserCreateForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            new_user = user_form.save(commit=False)
            # new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            customer_form.save()
            reverse_lazy("homepage")
        else:
            return render(request, "home/register.html", {
                'user_form': user_form,
                'customer_form': customer_form
            })




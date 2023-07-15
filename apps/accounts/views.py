from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.accounts.models import CustomUser
from apps.accounts.forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(
                "employee:employee_list"
            )  # перенаправьте на вашу страницу после успешного входа
        else:
            # обработка ошибки входа в систему
            return self.form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("employee:employee_list")

    def logout(self, request):
        # Add any custom logic you need before logging out the user
        super().logout(request)

    # def dispatch(self, request, *args, **kwargs):
    #     self.logout(request)
    #     response = super().dispatch(request, *args, **kwargs)
    #     self.terminate_session(request)
    #     return response

    def terminate_session(self, request):
        request.session.flush()

    def get_next_page(self):
        return self.next_page


class CustomUserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")

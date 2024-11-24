from django.urls import path
import auth_system.views as auth_views

urlpatterns = [
	path("user-info/<int:pk>", auth_views.user_info, name="user-info"),
    path("register/", auth_views.register_user, name="register"),
    path("login/", auth_views.login_user, name="login"),
    path("logout/", auth_views.logout_user, name="logout"),
    path("edit-user/<int:user_id>", auth_views.edit_user, name="edit-user"),
    path("change-password/<int:user_id>", auth_views.change_password, name="change-password"),
]

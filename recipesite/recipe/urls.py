from django.urls import path
from . import views

urlpatterns=[
    path('addrecipe/',views.create_recipes, name="AddRecipe"),
    path('getallrecipes/',views.get_all_recipes, name="GetAllRecipes"),
    path('delete-recipe/<id>/', views.delete_recipe, name="DeleteRecipe"),
    path('update-recipe/<id>/', views.update_recipe, name="UpdateRecipe"),
    path('login/', views.login_page, name="Login"),
    path('register/', views.register_page, name="Register"),
    path('logout/', views.logout_page, name="Logout")

]
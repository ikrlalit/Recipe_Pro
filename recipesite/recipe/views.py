from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout, login
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def create_recipes(request):
    if request.method == "POST":
        try:
            data = request.POST
            recipe_name = data.get('recipe_name')
            recipe_description = data.get('recipe_description')
            recipe_image = request.FILES.get('recipe_image')

            Recipe.objects.create(recipe_name=recipe_name,
                                  recipe_description=recipe_description,
                                  recipe_image=recipe_image)
            
            messages.success(request, 'Recipe added successfully.')
            return redirect("GetAllRecipes") 
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect("GetAllRecipes")
    else:
        return render(request, 'recipes.html')
    
@login_required(login_url="/login/")
def get_all_recipes(request):
    if request.method == "GET":
        recipes = Recipe.objects.all()
        if request.GET.get('search'):
            recipes=recipes.filter(recipe_name__icontains= request.GET.get('search'))
        context = {'recipes': recipes}
        return render(request, 'recipelist.html', context)
    
@login_required(login_url="/login/")
def delete_recipe(request,id):
    recipe= Recipe.objects.get(id=id)
    recipe.delete()
    return redirect("GetAllRecipes")

@login_required(login_url="/login/")
def update_recipe(request,id):
    if request.method=="GET":
        recipe= Recipe.objects.get(id=id)
        context={'recipe':recipe}
        return render(request,'updaterecipe.html',context)
    else:
        data = request.POST
        recipe= Recipe.objects.get(id=id)
        recipe.recipe_name = data.get('recipe_name')
        recipe.recipe_description = data.get('recipe_description')
        if 'recipe_image' in request.FILES:
            recipe.recipe_image = request.FILES['recipe_image']

        recipe.save()

        return redirect("GetAllRecipes")
    

def login_page(request):
    if request.method=="POST":
        data=request.POST
        username=data.get('username')
        password=data.get('password')

        if User.objects.filter(username=username).exists():
            user= authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('GetAllRecipes')
            else:
                messages.error(request,'Invalid Password')
                return redirect('Login')
        else:
            messages.error(request,'Invalid username')
            return redirect('Login')

    else:
        return render(request,'login.html')

def register_page(request):
    if request.method=="POST":
        data=request.POST

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username is already taken.')
            return redirect('Register')

        user=User.objects.create(first_name=first_name,
                                 last_name=last_name,
                                 username=username)
        user.set_password(password)
        user.save()
        messages.info(request,"Account created successfully.")
        return redirect('Register')
    else:
        return render(request,'register.html')

def logout_page(request):
    logout(request)
    return redirect('Login') 
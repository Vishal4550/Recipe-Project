from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipes

def home(request):
    return render(request, 'home.html')

#  Recipe view – only for logged-in users
@login_required(login_url='login_user')
def recipe(request):
    if request.method == "POST":
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        # Create a recipe with the logged-in user
        Recipes.objects.create(
            user=request.user,
            recipe_image=recipe_image,
            recipe_name=recipe_name,
            recipe_description=recipe_description,
        )
        return redirect('recipe')

    # Filter only recipes for the logged-in user
    queryset = Recipes.objects.filter(user=request.user)

    # Search by name if query is present
    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains=request.GET.get('search'))

    context = {
        'recipe': queryset,
        'is_new_user': not queryset.exists()
    }
    return render(request, 'receipe.html', context)

#Delete recipe – only allow if it belongs to the user
@login_required(login_url='login_user')
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipes, id=id, user=request.user)
    recipe.delete()
    return redirect('recipe')

#Update recipe – only allow if it belongs to the user
@login_required(login_url='login_user')
def update_recipe(request, id):
    recipe = get_object_or_404(Recipes, id=id, user=request.user)

    if request.method == 'POST':
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe.recipe_name = data.get('recipe_name')
        recipe.recipe_description = data.get('recipe_description')

        if recipe_image:
            recipe.recipe_image = recipe_image

        recipe.save()
        return redirect('recipe')

    context = {'recipe': recipe}
    return render(request, 'update_receipe.html', context)

#Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login_user')

    return render(request, 'signup.html')

#Login view
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('recipe')
        else:
            messages.error(request, "Invalid credentials.")
            return render(request, 'login.html')

    return render(request, 'login.html')

#Logout view
@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')

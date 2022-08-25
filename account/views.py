from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model,login, logout, authenticate

User = get_user_model()

def signup(request):

    if request.method == "POST":
        #traitement de donne envoyé par le formulaire
        username = request.POST.get("username")
        password = request.POST.get("password")
        user     =  User.objects.create_user(username = username,
                                 password = password)
        #connecte le user  
        login(request,user)
        return redirect('index')
    return render(request,'account/signup.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            return redirect('index')

    return render(request, 'account/login.html')

def logout_user(request):
    logout(request)
    return redirect('index')
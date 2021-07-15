from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Github
from django.contrib import messages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.decorators import login_required

PATH = '/usr/bin/chromedriver'
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(PATH, chrome_options=options)

# Create your views here.

@login_required(login_url='login')
def index(request):
    if request.method == 'POST':
        data = request.POST
        githubuser = data['githubuser']
        user = data['user']
        url = 'https://github.com/' + githubuser
        print(url)
        image = ""
        try:
            driver.get(url)
            container = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//img[@class='avatar avatar-user width-full border color-bg-primary']"))
            )
            image = container.get_attribute('src')
            print(image)
            if not Github.objects.filter(username=user, imagelink=image).exists():
                new_user = Github.objects.create(githubuser=githubuser, imagelink=image, username=user)
                new_user.save()
            else:
                messages.info(request, "Existe déjà")
            return render(request,'base.html')
        finally:
            if image=='':
                messages.info(request, 'Not found !!!')
            return render(request, 'base.html')
    else:
        return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        email = data['email']
        password = data['password']
        password2 = data['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully")
                return redirect('login')
        else:
            messages.info(request, 'passwords are not the same !!!')
            return redirect('register')
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        data = request.POST
        user_mail = data['username_email']
        password = data['password']
        username_auth = auth.authenticate(username=user_mail, password=password)
        mail_auth = auth.authenticate(email=user_mail, password=password)
        if username_auth is not None:
            auth.login(request, username_auth)
            return redirect('/')
        elif mail_auth is not None:
            auth.login(request, mail_auth)
            return redirect('/')
        else:
            messages.info(request, 'Infos Incorrect !!!')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def show_images(request):
    username = request.user
    images = Github.objects.filter(username=username)
    link = 'https://github.com/'
    dico = {'images': images, 'link':link}
    return render(request, 'images.html', dico)
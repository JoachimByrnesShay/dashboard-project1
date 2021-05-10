from django.shortcuts import render, redirect
import requests, os
from dotenv import load_dotenv
from github import Github, GithubException
import pygal
from django import forms
import random

load_dotenv()


class RepoForm(forms.Form):
    #domain = forms.CharField(max_length=100, label='domain')
    #domain = 'github.com'
    domain= forms.CharField(initial='github.com', disabled=True)
    #user_name = forms.CharField(max_length=100, label='user_name')
    #repo_name = forms.CharField(max_length=100, label='repo_name')
    user_name = forms.CharField(initial='JoachimByrnesShay')
    repo_name=forms.CharField(initial='djangogirls_tute1')
    # def __init__(self, data, **kwargs):
    #     initial = kwargs.get('initial', {})
    #     data = {**initial, **data}
    #     super().__init__(data, **kwargs)

def home(request):
    context = {}
    return render(request, 'pages/home.html', context)


def get_repos(username='JoachimByrnesShay'):
    url = "https://api.github.com/users/{username}/repos"
    token = os.getenv('GH_ACCESS_TOKEN')
    g = Github(token)
    user = g.get_user()
    login = user.login
    return user.get_repos()

def get_repo(user, repo):
    
    url = "https://api.github.com/users/%s/repos" % user
    #print(url)
    token = os.getenv('GH_ACCESS_TOKEN')
    g = Github(token)
   
    #login = user.login
    #print(user)

    try:
        user = g.get_user(user)
        repo = user.get_repo(repo)
    except:
        repo = None
    #print(repo.GithubException)
    #print('hello')
    #request = requests.get("https://api.github.com/users/%s/repos" % user)
    #json = request.json()
   # print(repo)
    #print(json)
    return repo
    #repo = g.get_repo(repo)
   # print(repo)

def table(request):
    context = {}
    context['repos'] = get_repos()
 
    return render(request, 'pages/table.html', context)


def bar_chart(request):
    context = {}
    line_chart = pygal.HorizontalBar(truncate_label=30)
    line_chart = pygal.Bar(truncate_label=30)
    line_chart.title = 'Repos by size'
    repos = get_repos()
   
    for repo in repos:
        line_chart.add(repo.name, repo.size)

    chart_svg = line_chart.render_data_uri()
    context['chart_render']= chart_svg

    return render(request, 'pages/bar.html', context)



# NOTES:   get_repo and get repos need to use request and search
# PIE chart fucntionality contingent upon this

def pie_chart(request):
    context = {}
    context['pie_render'] = None
    pie_chart = pygal.Pie()
    #print(request.POST)
    if request.POST:
        print(request.POST)
        form = RepoForm(request.POST)
       #print(form['domain'])
        #print('hope')
        if form.is_valid():
            domain = form.cleaned_data['domain']
            user_name = form.cleaned_data['user_name']
            repo_name = form.cleaned_data['repo_name']
            #form['user_name'] = user_name
            #form['repo_name'] = repo_name
            # print(user_name)
            # print(repo_name)
            g= Github(user_name)

            repo = get_repo(user_name, repo_name)
            print(repo)
            pie_chart.title = "hi its a pie chart"
            if repo:
                languages = requests.get(repo.languages_url).json()
                for lang in languages:
                    print(lang)
                    size = languages[lang]
                    pie_chart.add(lang, size)
                pie = pie_chart.render()

                context['pie_render'] = pie
            context['form'] = form
        else: 
            form = RepoForm(None)
            domain = ''
            user_name = ''
            repo_name = ''

            # # # print(pie)
            # print(context['pie_render'])
            return render(request, 'pages/pie.html', context)
    else:
        default_user = 'JoachimByrnesShay'
        repo = get_repos()[1].name
        #setup = {'domain': 'github.com', 'user_name': default_user, 'repo_name': repo}
        #setup.update(request.POST)
        form = RepoForm()
        print(form)
        # if form.is_valid():
        #     domain = form.cleaned_data['domain']
        #     user_name = form.cleaned_data['user_name']
        #     repo_name = form.cleaned_data['repo_name']
       # form = RepoForm(initial={'domain': 'github.com', 'user_name': default_user, 'repo_name': repo})
         
        #context['user_name'] = default_user
        #context['repo'] = repo
        # form.initial['user_name'] = default_user
        
        # form.initial['repo'] = default_user
             #form = RepoForm()
        #print(form)
    #print(form.user_name)
    context['form'] = form

    
    return render(request, 'pages/pie.html', context)
     


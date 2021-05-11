from django.shortcuts import render, redirect
import requests, os
from dotenv import load_dotenv
from github import Github, GithubException
import pygal
from django import forms
import random

load_dotenv()


class RepoForm(forms.Form):
    domain= forms.CharField(max_length=10,initial='github.com', disabled=True)
    user_name = forms.CharField(initial='JoachimByrnesShay')
    repo_name=forms.CharField(initial='djangogirls_tute1')

class BlankRepoForm(forms.Form):
    domain= forms.CharField(initial='github.com', disabled=True)
    user_name = forms.CharField(max_length=100, label='user_name', widget=forms.TextInput(attrs={'placeholder': 'must exist on github'}))
    repo_name = forms.CharField(max_length=100, label='repo_name', widget=forms.TextInput(attrs={'placeholder': 'must exist on github'}))

def home(request):
    context = {}
    context['home_active'] = 'active'
    return render(request, 'pages/home.html', context)


def get_repos(username='JoachimByrnesShay'):
    url = "https://api.github.com/users/{username}/repos"
    token = os.getenv('GH_ACCESS_TOKEN')
    g = Github(token)
    user = g.get_user()
    login = user.login
    return user.get_repos()

def user_exists(user):
    token = os.getenv('GH_ACCESS_TOKEN')
    g = Github(token)
    try:
        user = g.get_user(user)
    except:
        user = None
    return user

def repo_exists(user, repo):
    try: 
        repo = user.get_repo(repo)
    except:
        repo = None
    return repo

def get_repo(user, repo):
    
    url = "https://api.github.com/users/%s/repos" % user
    token = os.getenv('GH_ACCESS_TOKEN')
    g = Github(token)
   
    try:
        user = g.get_user(user)
        repo = user.get_repo(repo)
    except:
        repo = None
    return repo


def lower_case(e):
    return capitalize(str(e.name))

def table(request):
    context = {}
   # context['repos'] = get_repos().sort(my_names(e))
    stuff =  get_repos()
    things =  sorted(stuff, key=lambda k: k.name.lower())
    context['repos'] = things
    context['table_active'] = 'active'
    return render(request, 'pages/table.html', context)


def bar_chart(request):
    from pygal.style import Style
    from pygal.style import DarkStyle, DarkSolarizedStyle, LightStyle

    custom_style = Style(
      background='#EDDCD2',
      #background='#a4aced9',
     # plot_background='#EDF6F9',
      #plot_background="#F0EFCB",
      #plot_background='#FEFAE0',
      #plot_background='#FEEAFA',
      plot_background='#EDF2FB',
      
      foreground='#370617',
      foreground_srrong='#FFFFFF',
      foreground_subtle='#000000',
      opacity='1',
      opacity_hover='0.3',
      title_font_size=30,
      transition='400ms ease-in')
    context = {}
    
    #line_chart = pygal.Bar(truncate_label=30, style=custom_style)
    line_chart = pygal.Bar(truncate_label=30, style=custom_style)
    line_chart.title = 'Repos by size'
    repos = get_repos()
   
    for repo in repos:
        line_chart.add(repo.name, repo.size)

    chart_svg = line_chart.render_data_uri()
    context['chart_render']= chart_svg
    context['bar_chart_active'] = 'active'
    return render(request, 'pages/bar.html', context)



# NOTES:   get_repo and get repos need to use request and search
# PIE chart fucntionality contingent upon this

def pie_chart(request):
    from pygal.style import Style
    custom_style = Style(
      background='#343A40',
      plot_background="#FEFFE9",
      foreground='#FFFFFF',
      foreground_strong='#FFFFFF',
      foreground_subtle='#000000',
      opacity='1',
      opacity_hover='1',
      title_font_size=24,
      transition='400ms ease-in')
      #colors=('#1A535C', '#4ECDC4', '#F7FFF7', '#FF6B6B', '#FFE66D'))

    context = {}
    context['pie_render'] = None
    pie_chart = pygal.Pie(style=custom_style)
    if request.POST:
        print(request.POST)
        form = RepoForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data['domain']
            user_name = form.cleaned_data['user_name']
            repo_name = form.cleaned_data['repo_name']
            g= Github(user_name)

            repo = get_repo(user_name, repo_name)
            pie_chart.title = "Languages used in this repository"
            if repo:
                languages = requests.get(repo.languages_url).json()
                for lang in languages:
                    print(lang)
                    size = languages[lang]
                    pie_chart.add(lang, size)
                pie = pie_chart.render()

                context['pie_render'] = pie
                context['form'] = form
                return render(request, 'pages/pie.html', context)
        
        initial = {}
        if user_exists(user_name):
            initial['user_name'] = user_name
        if repo_exists(user_name,repo_name):
            initial['repo_name'] = repo_name
        form = BlankRepoForm(initial=initial)
        context['form'] = form
        return render(request, 'pages/pie.html', context)
    else:
        default_user = 'JoachimByrnesShay'
        repo = get_repos()[1].name
        form = RepoForm()
    context['pie_chart_active'] = 'active'
    context['form'] = form
    return render(request, 'pages/pie.html', context)
     


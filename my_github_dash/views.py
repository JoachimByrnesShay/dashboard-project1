from django.shortcuts import render, redirect
import requests, os
from dotenv import load_dotenv
from github import Github, GithubException
import pygal
from django import forms

load_dotenv()


class RepoForm(forms.Form):
    domain = 'github.com'
    user_name = forms.CharField(max_length=100, label='username')
    repo_name = forms.CharField(max_length=100, label='repo_name')
    # def __init__(self, *args, **kwargs):
    #     domain= 'github.com'
# Create your views here.
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
    user = g.get_user()
    login = user.login
    print(user)
   # print(repo)
    #repo = g.get_repo(repo)
   # print(repo)

def table(request):
    context = {}
    context['repos'] = get_repos()
 
    return render(request, 'pages/table.html', context)


def bar_chart(request):
    context = {}
    line_chart = pygal.HorizontalBar(truncate_label=30)
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
    pie_chart = pygal.Pie()
    if request.method == 'POST':
        form = RepoForm(request.POST)
    
        if form.is_valid():
       
            user_name = form.cleaned_data['user_name']
            repo_name = form.cleaned_data['repo_name']
            
            print(user_name)
            print(repo_name)
        else:
            form = RepoForm()

        context['form'] = form
        get_repo(user_name, repo_name)
        return redirect('/', context)
    else:
        form = RepoForm()

    return render(request, 'pages/pie.html', context)
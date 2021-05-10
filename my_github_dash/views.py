from django.shortcuts import render
import requests, os
from dotenv import load_dotenv
from github import Github, GithubException
load_dotenv()

#token = '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'

# Create your views here.
def home(request):
    context = {}
    return render(request, 'pages/home.html', context)

def table(request):
    #headers = {'Authorization': 'token ' + os.getenv('GH_ACCESS_TOKEN')}
    #print(headers)
    username = 'JoachimByrnesShay'
    #password = os.getenv('GH_PASSWORD')
    g = Github(username, os.getenv('GH_ACCESS_TOKEN'))
    #print(Github().get_rate_limit())
   
    context = {}
    user = g.get_user()
    login = user.login
    repos = user.get_repos()
    print(user.get_repo(repos[0].name).git_url)
 
    return render(request, 'pages/table.html', context)
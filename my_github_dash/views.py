"""imports of libraries, functions, and modules needed for views.py"""
from django.shortcuts import render
from dotenv import load_dotenv
"""from modules/*, custom modules containing utility fnctions and form classes"""
from .modules import custom_utils
from .modules import custom_forms

"""load any needed env variables"""
load_dotenv()


"""simple landing page view.  main content consists of additional button links for the repository data pages"""
def home(request):
    context = {}
    # 'home_active' is a templated variable in template. set to 'active' to set home page nav link to active class
    context['home_active'] = 'active'
    return render(request, 'pages/home.html', context)


"""tabular and sortable presentation of github repo data including name, repo size in kb or mb, 
   date and time repo created, and primary programming language of repo. sortable for each """
def table(request):
    context = {}
    # get_repos() is a utility function using pygithub to get all repos via api for a specified user, or for the defaultuser (see custom_utils) if no argument s passed
    ## imported from modules/custom_utils.py
    repos = custom_utils.get_repos()
    if request.POST:
        # the table template contains a simple form containing a series of buttons of type 'submit' each with a hard-coded value for the repo attribute to sort_by as well as one radio button pair which
        # specify the hard-coded values of either 'asc' or 'desc' which are utilied only if the sortby value is 'name' (repo.name).  
        sortby_value = request.POST['sortby']
        # if the radio button with value 'desc' was checked on submit AND the user has requested to sort by repo.name, assign rerverse_order = True, which will be passsed to the sorted function
        if request.POST['alpha_order'] == 'desc' and sortby_value =='name':
            reverse_order = True
        else:
            reverse_order = False
      
        if sortby_value == 'name':
            repos = sorted(repos, key=lambda repo_data: (repo_data.name.casefold(), repo_data.name), reverse=reverse_order)
        else:
            # any other value for sortby requires one less parameter and will be handlled by the sortby_data function which aggregates functionality int and string cases
            # sortby_data() is a utility function imported from modules/custom_utils.py
            repos= sorted(repos, key=lambda repo_data: custom_utils.sortby_data(repo_data, sortby_value))

    context['repos'] = repos
    # 'table_active' is a templated variable in template. set to 'active' to set table page nav link to active class
    context['table_active'] = 'active'
    return render(request, 'pages/table.html', context)


"""barchart presentation of relative repo sizes in owners github account.  not configurable"""  
def bar_chart(request):
    context = {}
    chart_svg = custom_utils.get_repos_size_barchart()
    context['chart_render']= chart_svg
    # 'bar_chart_active' is a templated variable in template. set to 'active' to set barchart page nav link to active class
    context['bar_chart_active'] = 'active'
    return render(request, 'pages/bar.html', context)


"""configurable repo selection.  piechart presentation of proportional usage of programming languages used per a single repo.
Any existing public github repository can be viewed by entering user and repo name in form"""  
def pie_chart(request): 
    context = {}
    context['chart_render'] = None
    
    if request.POST:
        form = custom_forms.GetRepoForm(request.POST)
        
        if form.is_valid():
            # validate input based form data
            domain = form.cleaned_data['domain']
            user_name = form.cleaned_data['user_name']
            repo_name = form.cleaned_data['repo_name']
            # get_repo returns a valid repo object if repo of user_name and repo_name exist, else returns None
            repo = custom_utils.get_repo(user_name, repo_name)
            
            if repo:
                # get_repo_languages_piechart() returns svg piechart using json object derived from languages list data at repo.languages_url
                context['chart_render'] = custom_utils.get_repo_languages_piechart(repo)
                context['form'] = form
                # return and render if we have reached this point
                return render(request, 'pages/pie.html', context)
        
        # nonexistent_repo_piechart_form() returns a new repo request form for the piechart template which will show placeholder content 
        # in repo_name field but retains POST data in user_name field if latter exists but former does not, or placeholder in both fields if at least user_name does not exist
        form = custom_utils.nonexistent_repo_piechart_form(user_name, repo_name)
    else:
        # if there was neither a successful POST submit nor a failed POSST submit for which placeholder content is specialized, create default repo request form using default initial values
        form = custom_forms.GetRepoForm()

    # pie_chart_active' is a templated variable in template. set to 'active' to set pie_chart page nav link to active class
    context['pie_chart_active'] = 'active'
    context['form'] = form
    return render(request, 'pages/pie.html', context)
 
from django import forms

"""a form which prepares necessary data for accessing github repo """
class GetRepoForm(forms.Form):
    domain= forms.CharField(max_length=10,initial='github.com', disabled=True)
    user_name = forms.CharField(initial='JoachimByrnesShay')
    repo_name=forms.CharField(initial='djangogirls_tute1')

"""a version of the GetRepoForm which is employed if the repo request in POST does not exist.  if user_name exists on github, POST user_name will still 
populate this new form, while placeholder 'must exist on github' will display in repo_name field.  If neither user_name nor repo_name exist,
both fields with display the placeholder"""
class BlankGetRepoForm(forms.Form):
    domain= forms.CharField(initial='github.com', disabled=True)
    user_name = forms.CharField(max_length=100, label='user_name', widget=forms.TextInput(attrs={'placeholder': 'must exist on github'}))
    repo_name = forms.CharField(max_length=100, label='repo_name', widget=forms.TextInput(attrs={'placeholder': 'must exist on github'}))


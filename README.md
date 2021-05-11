### backend django HW1, kickstartcoding
### May 10, 2021
#### joachim byrnes-shay
#### dashboard app
#### heroku url:  https://dashboard-project1.herokuapp.com/ 
#### github url:  https://github.com/JoachimByrnesShay/dashboard_project1

a presentation of github repository statistics

pygal charts and sorting functionality included

homepage

/table, displays tabular and button sortable data for owner repos, incl repo.name, repo size, date repo created, main repo language

/bar, displays vertical barchart using pygal built from owner repos size data

/pie, provides user form pre-populated with owner repo example (username and repo_name), user can override and enter choice of github user_name and github repo_name to request a chart for a single repo.  valid form entry results in creation of piechart based on proportional date re programming languages used in the repo

features addressed: the above + programming language icons displayed on barchart page;  sorting on table page allows to sort either asc or desc in the case of repo.name (only).  All other fields are strictly sorted by asc 
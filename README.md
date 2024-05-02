# AI-For-Work-Scrapper
A script that scrapes all the prompts from all the available links using selenium in python

## TASK
goto https://www.aiforwork.co/ select a department and a role and the prompt title will be shown and the user have to select one and will be redirect to the page which will give the prompt text that is needed to scrape.
however if the user is not logged in then the prompt text will be blocked by not login dialog box

## APPROACH
first I scrapped all the links of department then iterate it and scrape all the login from those department and again iterat the roles to get the prompt texts and noticed that the prompt text are just commented so we donot have to login. then after all the items are scrapped I store them to 'result.csv'
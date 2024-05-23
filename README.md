# bdo-code-redeem
(In progress) 
Automatically redeems the gift codes for the game Black Desert Online NA (Asia in progress)


### Required
    PyYAML==6.0.1
    selenium==4.20.0
    Firefox Browser

Unix Cron Job document only for now, haven't tried on Windows yet:
To utilize this script, please configure the config.yml file accordingly. There will be two log in options suported, Steam login and Pearl Abyss Login. Please follow the tips in the config.yml file to selection your options correctly.

### Pearl Abyss Loging
Follow the config.yml file. 
Please look at CronJob section next

#### Steam Logins
To address the steam guard issue, we will first require the user to manually authenticate the firefox browser by logging in once. Now, there are cookies saved for this authentication so we will have to use the current firefox profile to make this script work.

Please type the following into the browser address bar to navigate to profile management page
```
about:profiles
```
Look for the comment that says : "This is the profile in use and it cannot be deleted."
Copy the Root Directory Path and add it into the config.yml file, so now the script will be able to use the cookies to bypass the Steam Guard issue

More info about profiles can be found [here](https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles 'Profile Manager - Create, remove or switch Firefox profiles | Firefox Help')


#### Cron job (Unix systems)
Cron command is a job scheduler that will schedule our script to run automatically at some time
please refer to https://crontab.guru/ for how often you want the script to be executed

Please type the following into a terminal
```
crontab -e
```
Press i on you keyboard for input mode. Here is a sample 
```
5 8 * * 0  /path/to/python /path/to/bdoMainWeb.py >~/Desktop/stdout.log 2>~/Desktop/stderr.log
```
Press esc key to exit insert mode. Type :wq and hit Enter to save and quit
This runs once everyweek on Sunday at 8:05am. 
Output of file will be in stdout.log (generally not too useflu)
Error of script will be in stderr.log (Needed for debugging)
Feel free to change the log file location





### In progress:
    1. Add Asia Support: Completed May 23
    2. Add a GUI
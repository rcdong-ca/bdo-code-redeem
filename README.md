# bdo-code-redeem

Automatically redeems the gift codes for the game Black Desert Online NAEU and ASIA


### Required
    PyQt6==6.7.0
    PyYAML==6.0.1
    scheduler==0.8.7
    selenium==4.22.0
    Firefox Browser


### Running the GUI

![screenshot](/docs/images/gui.png)
This GUI is split into 3 sections:
1. Configuration Section:
Here the user should put their user information. This allows the application to log in to the account to redeem any codes obtained from [Garmoth.com](https://Garmoth.com). The user can save the configurations so they do not have to re-type it all again. The Run button will execute the script once.

2. The Job Scheduler section:
The user can set how often they want the code redeem script to run. The user should set a start date. The days and hours will tell when the next job from the start date should run
ex. Days = 3, hours = 0. The script will run every 3 days from the start date user has set.

3. The log section:
While running the script, any logs and errors output will be directed to the large text box on the right side. This will tell the user if jobs has been scheduled correctly, if the script was able to execute successfuly, as well as the codes redeemed.

Note: This app can be minimized into system tray so it can run in the background without too much visual interferance. This app can only be closed by clicking on the tray icon and clicking the quit option



### Utilzing Cron job

To utilize this script, please configure the config.yml file accordingly. There will be two log in options suported, Steam login and Pearl Abyss Login. Please follow the tips in the config.yml file to selection your options correctly.

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


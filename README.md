# bdo-code-redeem
(In progress) Automatically redeems the gift codes for the game bdo (Never missing those high cron codes again)


### Required
    PyYAML==6.0.1
    selenium==4.20.0
    Firefox Browser

Unix Cron Job document only for now, haven't tried on Windows yet:
To utilize this script, please configure the config.yml file accordingly. There will be two log in options suported, Steam login and Pearl Abyss Login. Please follow the tips in the config.yml file to selection your options correctly.

### Pearl Abyss Loging
Follow the config.yml file. I do not believe it requires 2faa, (not in my side) so this is the easiest to set up
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










### Design:
    1. Idea is to utilize garmoth.com as the website where we will obtain the codes. Credits to them. The information is stored as HTML so we will use beautiful soup to obtain the information.
        - note: As the plan is to run this as a cron job, we want to check
        for codes that have already been redeemed. Perhaps we will keep a 
        local file to track this informatino

    2. The code redemption will be on BDO's official website. One will require user account information (My usage is on Steam) to access the code redemption option. This step will require more interaction, so I believe selenium will be required to achieve this,
        - note: Steam Guard may be trouble some to handle. Browers uses a cookie to make it so we don't have to do passcode repeatedly. Look into how this can be accomplished for this script


Apr19: Obtained codes from garmoth.com

Apr 22: Met a blocking phase, once you redeem a code, you will navigate to a unique page,
a page whose url I forgot to save. This perhaps may lead to limited testing practices as
we can only redeem a code once.
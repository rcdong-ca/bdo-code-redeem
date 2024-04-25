# bdo-code-redeem
(In progress) Automatically redeems the gift codes for the game bdo (Never missing those high cron codes again)



Design:
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
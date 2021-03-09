# Alexei Pacholuk
# 3/1/21


# This program accesses Twitter's API through tweepy 
# and looks for mentions of @YoureNotYourBud.  
# When it finds mentions, it will look for incorrect 
# uses of "your" and respond with "*you're"

# It also follows back any users that are following

#----------------------------------------------------
#----------------------------------------------------
#Imports

# Import tweepy for use w/twitter api
import tweepy as tw
import credentials # API credentials
import time
from gingerit.gingerit import GingerIt # For grammar checking


#-----------------------------------------------------
# Constants
REPLY_MESSAGE = "*you're"
NUMBER_OF_MENTIONS = 4

# API Constants
API_KEY = credentials.API_KEY
API_SECRET_KEY = credentials.API_SECRET_KEY
ACCESS_TOKEN = credentials.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = credentials.ACCESS_TOKEN_SECRET
#-----------------------------------------------------
# Main
def main():
    api = authenticateToTwitter(
        API_KEY, API_SECRET_KEY, 
        ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    run = True
    while run==True:                # Infinite loop
        testCredentials(api)
        replyToMentions(
            returnMentionList(api, NUMBER_OF_MENTIONS),
            REPLY_MESSAGE)
        followBack(api)
        time.sleep(3600)             # Sleep for 1 hour

#----------------------------------------------------
# Authenticate to twitter, return API object if limit not exceded
def authenticateToTwitter(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
    auth = tw.OAuthHandler(
        API_KEY, 
        API_SECRET_KEY) # Create an OAuthHandler object used for API calls

    auth.set_access_token(
        ACCESS_TOKEN, 
        ACCESS_TOKEN_SECRET)    # Get access token
        
    api = tw.API(auth, wait_on_rate_limit=True,     # Create an api object/instance  
        wait_on_rate_limit_notify=True) #print message and wait if limit exceded.
    return api

#----------------------------------------------------
# Tests credentials for calling API
def testCredentials(api):
    try:
        api.verify_credentials()
        print("Authentication OK") # Prints "Authentication OK"
    except:
        print("Error during authentication")

#----------------------------------------------------
# Return list of 5 recent tweet mentions
def returnMentionList(api, NUMBER_OF_MENTIONS):
    print("Returning list of mentions...")
    
    mentions = api.mentions_timeline(
        tweet_mode='extended')     # API call for mentions
    return mentions[:NUMBER_OF_MENTIONS]

#----------------------------------------------------
# Look for @YoureNotYourBud mentions and reply if "your" missuse found
def replyToMentions(mentions, REPLY_MESSAGE):
    print("Replying to mentions...")

    for mention in mentions:    # Loop through mentions                                                         
        replyToMessage = False      # Reset replyToMessage? as False

        
        gingeredMention = GingerIt().parse(
            mention.full_text.lower())  # Grammar checked mention

        if ("'correct': \"you're\"") in str(gingeredMention):
            print("Mention with error - " + mention.full_text.lower())
            replyToMessage = True
        else:
            continue

        mentionID = str(mention.id) # Store string of mention status ID
        screenName = mention.user.screen_name   # Retrieves screen-name/@

        if replyToMessage == True:    

            # This section needs to talk to a database
            # or datastructure to read and write tweet ID's
            # it has replied to so it doesn't reply multiple times.
            # Once that's done it can go live online.
            try:
                api.update_status(
                    status=("@"+screenName+ " " + REPLY_MESSAGE), 
                            in_reply_to_status_id=mentionID)    # try to reply with "*you're"
            except:
                print("Error. Could not reply to tweet ID# " 
                        + mentionID+"\n")   # Error replying (usually means it's already been replied to)
            else:
                print("Replied to mention.\n")  # Replied to a mention with a grammar correction
        else:
            continue

#--------------------------------------------------
# Follow back followers
def followBack(api):
    myFollowers = api.followers()

    for follower in myFollowers:    # Loop through my followers
        followerName = follower.screen_name
        
        followersFollowers = api.followers(screen_name=followerName) # Get follower's followers
        listOfFollowersFollowers = []   # Empty list of follower's Followers

        for followersFollower in followersFollowers:
            listOfFollowersFollowers.append(
                followersFollower.screen_name) # Add follower's followers to list
        
        if "YoureNotYourBud" in listOfFollowersFollowers:   # Catches followers already being 
            print("Already following "+followerName)    
        else:
            api.create_friendship(screen_name=(followerName))   # Follows followers not being followed
            print("Followed "+followerName)

#--------------------------------------------------
# Test stuff in here


#----------------------------------------------------
main()
# -*- coding: utf-8 -*-
# Singing Windows Twitter Bot
ver="2.1"
# This code uses the Twitter for Python API (https://python-twitter.readthedocs.io/en/latest/) to search for tweets matching a certain hashtag, and sends them to a Photon
# The Photon is an Internet of Things device that controls the Singing Windows light display by reading the text sent to it at the end of this code.

# Version 2.0:  Requires data file with keys stored in
#               Checks for excessive tweet length
#               Tweets reply to initial tweeter
#               Issues identified in GitHub Issue "Improvements 201808"
#
# Version 2:1:  Fixes Unicode Warning Issue upon script execution

# Begin code

# Attempting to import required modules

try:

    import requests # can be installed with easy_install or pip from command line
    import time # default Python package

except:

    print('The requests/time modules are not installed')
    quit()


try:
    import twitter # can be installed with easy_install or pip from command line
    
except:

    print('No twitter module is installed for this version of Python')
    quit()

# If it reaches this point then all the modules have loaded successfully
    
print('Welcome to the Twitter Singing Windows bot!')

# Attempt to load all those dead secret key things from file
# These must be kept in the file keys.txt in the same directory as
# this script. The keys must be in the right order!

try:
    with open("keys.txt", mode='r') as keyfile:
        consumer_key=keyfile.readline().strip(" \n") # must strip newline character from end of each string
        consumer_secret=keyfile.readline().strip(" \n")
        access_token_key=keyfile.readline().strip(" \n")
        access_token_secret=keyfile.readline().strip(" \n")
        photon_id_1=keyfile.readline().strip(" \n")
        particle_access_token_1=keyfile.readline().strip(" \n")
except:
    print('Unable to load access keys')
    quit()


# Attempts to verify Twitter credentials

try:

    api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)  

    api.VerifyCredentials()

    print('Credentials verified')

except:

    # In the case of errors verifying credentials with Twitter - eg network issues or incorrect keys

    print('\nThere appears to be a problem connecting to Twitter')
    print('Ensure your consumer key/secret and access token key/secret are correct')
    print('Ensure this device has an internet connection')
    quit()



    # Searches for all terms featuring the hashtag in the string below. Change this to replace the search term to match

num_to_get=1 # only get one tweet at a time
last_id=0 # used to store the id of the last tweet we uploaded to SW
success=False # updated when we get a successful response to a tweet

while True: # lovely infinite loop

    try:

        # searches for latest tweet including the hashtag #dcsingingwindows
        hash_searches = api.GetSearch(term="#dcsingingwindows",count=num_to_get) # Searches for the string featured and returns the data of most recent tweet

        # doing this slightly differently to before
        # put text of tweet, numeric id of tweet and name of tweet into arrays
        # size of one! If there's a better way of doing this please let me know
        tweet_array=[s.text for s in hash_searches]
        idArray = [s.id for s in hash_searches]
        nameArray = [s.user.screen_name for s in hash_searches]
        
        # there is only one of each!        
        tweet_txt=tweet_array[0]
        name=nameArray[0]
        tweet_id=idArray[0]

        # find where in the text the hashtag is. Used to remove it
        hash_start=tweet_txt.lower().find("#dcsingingwindows")
        hash_stop=hash_start+17
        tweet_txt_list = []

        # remove hashtag and replace problem characters “, ” and \ 
        for c in range(0, len(tweet_txt)):
            if (c<hash_start or c>hash_stop):
                if (tweet_txt[c].encode('utf-8') == '”' or tweet_txt[c].encode('utf-8') == '“'):
                    tweet_txt_list += '"'
                elif (tweet_txt[c].encode('utf-8') != "\\"):
                    tweet_txt_list += tweet_txt[c]

        # The code above deals with "smart quotes" featured on iPhones - these are directional and the Photon does not detect these
        # To deal with these, it searches through the array for these "smart quotes" and replaces them with normal quotes
        # These "smart quotes" are their own UNICODE characters and so UTF-8 must be used to deal with these

        # create string from array of characters
        tweet_txt = ''.join(tweet_txt_list)

        tweet_txt = tweet_txt.strip() # get rid of any leading and trailing spaces
        
        print(tweet_txt) # Outputs the string to be sent

        tweet_back="" # the message we will tweet back to the tweeter

        # we'll only do this if we've just started the program or got a new tweet
        if tweet_id>last_id:

            # check text which is not too long, if so then send it to the photon
            if len(tweet_txt)<64:

                print("updating")

                # Send tweet through a POST request to a Photon which controls the display
                request = requests.post("https://api.particle.io/v1/devices/" + photon_id_1 + "/led?access_token=" + particle_access_token_1, data={'value': tweet_txt})
                
                print(request.status_code, request.reason) # Outputs the POST status and reason - full list of these can be found online

                # 200 means the photon has responded to the request, success!
                if request.status_code==200:
                    success=True

                    # if this is a tweet sent since the program started we can tweet back
                    if last_id>0:
                        tweet_back="@" + name + " Thank you for tweeting Singing Windows. Your request has been sent successfully! :-)"

                    last_id=tweet_id # ensures we don't enter this bit of the loop again


                # Another error code means no reponse from the photon
                # tweet back to say sorry, but only do this once i.e. if the last request was a success
                elif success==True:    

                    tweet_back="@" + name + " Thank you for tweeting Singing Windows. Unfortunately your request has been delayed for now :-("

                    success=False # don't send tweet reply twice

                    # we don't update last_id here to ensure we try again
                    
            else: # tweet was too long

                success=True # looks odd but ensures that a tweet is sent if next message is delayed

                if last_id>0: # and don't do it if the program has just started! 
                    tweet_back="@" + name + " Thank you for tweeting Singing Windows. Unfortunately your tweet is too long: max 80 characters :-("

                last_id=tweet_id # ensures we don't enter this bit of the loop again
                
            if tweet_back != "": # if we have a tweet to send, then post it as a reply to the original

                print("Sending tweet: " + tweet_back)
                status = api.PostUpdate(tweet_back, in_reply_to_status_id=tweet_id)

    # We've generated an error in the above code, possibly due to a network outage            
    except:
        print('Network error')

    time.sleep(6) # moved from higher up in the code. prevents reaching Twitter's API search rate limit

# End code

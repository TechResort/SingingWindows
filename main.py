# -*- coding: utf-8 -*-

# This code uses the Twitter for Python API (https://python-twitter.readthedocs.io/en/latest/) to search for tweets matching a certain hashtag, and sends them to a Photon
# The Photon is an Internet of Things device that controls the Singing Windows light display by reading the text sent to it at the end of this code.

# Begin code

# Attempting to import required modules

try:

    import requests # can be installed with easy_install or pip from command line
    import time # default Python package

except:

    print('The reqeusts/time modules are not installed')
    quit()


try:
    import twitter
    
except:

    print('No twitter module is installed for this version of Python')
    quit()

# If it reaches this point then all the modules have loaded successfully
    
print('Welcome to the Twitter colour bot!')

# Attempts to verify Twitter credentials
# Replace the values provided with your own, provided by Twitter once you have set up API access

try:

    api = twitter.Api(consumer_key='your_consumer_key_here',
                  consumer_secret='your_consumer_secret_here,
                  access_token_key='your_access_token_key',
                  access_token_secret='your_access_token_secret')

    api.VerifyCredentials()

    print('Credentials verified')

except:

    # In the case of errors verifying credentials with Twitter - eg network issues or incorrect keys

    print('\nThere appears to be a problem connecting to Twitter')
    print('Ensure your consumer key/secret and access token key/secret are correct')
    print('Ensure this device has an internet connection')
    quit()



while True:

    # Searches for all terms featuring the hashtag in the string below. Change this to replace the search term to match

    hash_searches = api.GetSearch(term="#dcsingingwindows",count=1) # Searches for the string featured and returns the data of most recent tweet

    time.sleep(6) # Waits 6 seconds - prevents reaching Twitter's API search rate limit

    # Finds the index of where the "Text" section of the returned data - what the user tweeted. This is then stored in the array "tweet_txt_list"
    
    text_index = hash_searches_string.find("Text")
    tweet_txt = hash_searches_string[text_index+6:-3]
    tweet_txt_list = []

    for char in tweet_txt:
        tweet_txt_list += char


    # The code below deals with "smart quotes" featured on iPhones - these are directional and the Photon does not detect these
    # To deal with these, it searches through the array for these "smart quotes" and replaces them with normal quotes
    # These "smart quotes" are their own UNICODE characters and so UTF-8 must be used to deal with these

    for i in range(0,len(tweet_txt_list)):
        if tweet_txt_list[i] == '“':
            tweet_txt_list[i] = '"'
        elif tweet_txt_list[i] == '”':
            tweet_txt_list[i] = '"'

    # Converts tweet from array to string

    tweet_txt = ''.join(tweet_txt_list)


    print(tweet_txt) # Outputs the string to be sent


    request = requests.post("https://api.particle.io/v1/devices/your_photon_id_here",data={'value': tweet_txt}) # Sends tweet through a POST request to a Photon which controls the display
    
    print(request.status_code, request.reason) # Outputs the POST status and reason - full list of these can be found online


# End code



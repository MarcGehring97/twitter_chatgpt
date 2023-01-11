"""
https://docs.tweepy.org/en/stable/client.html
https://www.jcchouinard.com/python-automation-with-cron-on-mac/
https://crontab.guru/

sudo
crontab -e > i > enter text > esc > :wq > enter
crontab -r, contab -l
* * * * * python3 /Users/Marc/Documents/GitHub/twitter_chatgpt/chatgpt.py
"""

def chatgpt(prompt, key):

    import openai
    openai.api_key = key

    # generate a response
    completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.5)
    response = completion.choices[0].text
    
    return response

def get_tweets(user_id, client, max_results=100):

    response = client.get_users_tweets(user_id, max_results=max_results)
    tweets = []
    ids = []
    for tweet in response.data:
        tweets.append(tweet.text)
        ids.append(tweet.id)
    
    return (tweets, ids)

def tweet(text, client):

    # create a tweet and return the tweet URL
    response = client.create_tweet(text=text)
    print(f"https://twitter.com/user/status/{response.data['id']}")

def main(text=""):

    import os
    if text == "":
        os.system("pip3 install random >/dev/null 2>&1")
        os.system("pip3 install tweepy >/dev/null 2>&1")
        os.system("pip3 install json >/dev/null 2>&1")
        os.system("pip3 install openai >/dev/null 2>&1")

    import random, tweepy, json, time

    keys = json.load(open("/Users/Marc/Desktop/Past Affairs/Past Universities/SSE Courses/Master Thesis/twitter_keys.json"))
    client1 = tweepy.Client(consumer_key=keys["consumer_key"], consumer_secret=keys["consumer_secret"], access_token=keys["access_token"], access_token_secret=keys["access_token_secret"])

    # using the twitter enterprise API bearer token
    bearer_token = str(open("/Users/Marc/Desktop/Past Affairs/Past Universities/SSE Courses/Master Thesis/twitter_bearer_token.txt").read())
    # some methods require enterprise access
    client2 = tweepy.Client(bearer_token=bearer_token)

    # the user ID of my actual account
    user_id = "1221912421566046210"
    # find out the user ID at https://tweeterid.com/
    tweets = get_tweets(user_id, client2)[0]
    
    # create a random subsample of 10 tweets
    tweet_subsample = random.sample(tweets, 5)
    multi_tweets = ""
    for i in range(len(tweet_subsample)):
        multi_tweets += "Tweet " + str(i + 1) + ": " + tweet_subsample[i] + ", "
    multi_tweets = multi_tweets[:-2]

    key = str(open("/Users/Marc/Desktop/Past Affairs/Past Universities/SSE Courses/Master Thesis/openai_key.txt").read())
    prompt = "Look at the following tweets and write another totally new tweet: " + multi_tweets
    # make the tweet sound good
    
    # a more simple prompt
    # random_tweet = random.choice(tweets)
    # prompt = "Write another tweet of the topic of this tweet: " + random_tweet
    
    try:
        if text == "":
            text = chatgpt(prompt, key)
        
        try:
            # refining the text with a second prompt
            new_prompt = "Write a new coherent tweet out of this text, but don't make it a quote and also not only hashtags: " + text
            text = chatgpt(new_prompt, key)
            # removing hidden characters
            text = text.replace("\n", "")
            text = text.replace("\\n", "")
            text = text.replace("\\", "")
            text = text.lstrip()
            text = repr(text)

            # removing leading and trailing 's
            if text[0] == "'" and text[-1] == "'":
                text = text[1:]
                text = text[:-1]

            # removing leading and trailing "s
            if text[0] == '"' and text[-1] == '"':
                text = text[1:]
                text = text[:-1]

            # stopping the program from posting incoherent tweets
            if text[0] == "," or text[0] == "-" or text[0] == "." or text[:6] == "Tweet6" or text[0] == "#"or text[-1] == '"' or text[0] == "'":
                raise KeyError
            
            # you can uncomment this and the commented section below to write a comment to the posted tweet with a thread
            # https://stackoverflow.com/questions/9322465/reply-to-tweet-with-tweepy-python
            # comment = chatgpt("Write a twitter thread to illustrate the meaning of the following tweet: " + text, key)

        except Exception:
            print("The server is overloaded or is not ready yet. The program will run again.")
            # reusing the old text
            main(text)

    except Exception:
        print("The server is overloaded or is not ready yet. The program will run again.")
        main()

    text += " #beepboop #R2D2"   
    tweet(text, client1)
    raise SystemExit(0)

    """
    time.sleep(15)

    # getting the ID of the this tweet for commeting
    user_id = "1612802398442897411"
    tweet_id = get_tweets(user_id, client2, max_results=5)[1][0]

    # cleaning the comment
    comment = comment.replace("\n", "")
    comment = comment.replace("\\n", "")
    comment = comment.lstrip()
    comment = repr(comment)

    # removing leading and trailing 's
    if comment[0] == "'" and comment[-1] == "'":
        comment = comment[1:]
        comment = comment[:-1]

    # removing leading and trailing "s
    if comment[0] == '"' and comment[-1] == '"':
        comment = comment[1:]
        comment = comment[:-1]

    print(comment)

    thread = []
    # j is the start index
    j = 0
    # every tweet can be a maximum of 280 chars long and we need some extra char spaces for the number of threads counter
    i = j + 270

    while True:

        # the old start index
        temp = j

        if i > len(comment):
            thread.append(comment[temp:j])
            break
        
        message = comment[j:i]
        # goes from index j to i - 1
        j = i - 1

        # find the index of the space and save it in j
        for char in reversed(message):
            if char == " ":
                break
            j -= 1
        
        # adding all words up until the sapce, but excluding it
        thread.append(comment[temp:j])

        # j is the new starting index but needs to be incremented to skip the space
        j += 1
        i = j + 270

    print(thread)

    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    api = tweepy.API(auth)

    i = 1
    for message in thread:
        message += " (" + str(i) + "/" + len(thread) + ")"
        print(message)
        api.update_status(status=message, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
        time.sleep(5)
        i += 1
    
    """

main()
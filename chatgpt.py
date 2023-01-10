"""



https://docs.tweepy.org/en/stable/client.html
"""

def chatgpt(prompt, key):

    import openai
    openai.api_key = key

    # Generate a response
    completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.5)
    response = completion.choices[0].text
    
    return response

def get_tweets(user_id, client):

    response = client.get_users_tweets(user_id, max_results=100)
    tweets = []
    for tweet in response.data:
        tweets.append(tweet.text)
    
    return tweets

def tweet(text, client):

    # create a tweet and return the tweet URL
    response = client.create_tweet(text=text)
    print(f"https://twitter.com/user/status/{response.data['id']}")

def main(text=""):

    import random, tweepy, json, openai
    keys = json.load(open("/Users/Marc/Desktop/Past Affairs/Past Universities/SSE Courses/Master Thesis/twitter_keys.json"))
    client1 = tweepy.Client(consumer_key=keys["consumer_key"], consumer_secret=keys["consumer_secret"], access_token=keys["access_token"], access_token_secret=keys["access_token_secret"])

    # using the twitter enterprise API bearer token
    bearer_token = str(open("/Users/Marc/Desktop/Past Affairs/Past Universities/SSE Courses/Master Thesis/twitter_bearer_token.txt").read())
    # some methods require enterprise access
    client2 = tweepy.Client(bearer_token=bearer_token)

    # the user ID of my actual account
    user_id = "1221912421566046210"
    # find out the user ID at https://tweeterid.com/
    tweets = get_tweets(user_id, client2)
    
    # create a random subsample of 10 tweets
    tweet_subsample = random.sample(tweets, 5)
    multi_tweets = ""
    for i in range(len(tweet_subsample)):
        multi_tweets += "Tweet " + str(i + 1) + ": " + tweet_subsample[i] + ", "
    multi_tweets = multi_tweets[:-2]

    key = str(open("/Users/Marc/Desktop/Past Affairs/Past Universities/SSE Courses/Master Thesis/openai_key.txt").read())
    prompt = "Get inspired by the following tweets and write another totally new tweet: " + multi_tweets
    # make the tweet sound good
    
    # a more simple prompt
    # random_tweet = random.choice(tweets)
    # prompt = "Write another tweet of the topic of this tweet: " + random_tweet
    
    try:
        if text == "":
            text = chatgpt(prompt, key)
        
        try:
            # refining the text with a second prompt
            new_prompt = "Write a new coherent tweet out of this tweet: " + text
            text = chatgpt(new_prompt, key)
        except Exception:
            print("The server is overloaded or not ready yet. The program will run again.")
            # reusing the old text
            main(text)

    except Exception:
        print("The server is overloaded or not ready yet. The program will run again.")
        main("")
    
    # stopping the program from contuing tweets    
    if text[0] == ",":
        return

    tweet(text, client1)

for i in range(3):
    main()
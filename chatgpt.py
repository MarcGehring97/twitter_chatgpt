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

def main():

    while True:

        try:

            import os
            
            # with ">/dev/null 2>&1" the warning do not appear in the terminal
            os.system("pip3 install random >/dev/null 2>&1")
            os.system("pip3 install tweepy >/dev/null 2>&1")
            os.system("pip3 install json >/dev/null 2>&1")
            os.system("pip3 install openai >/dev/null 2>&1")

            import random, tweepy, json, time

            # you will need elevated access
            keys = json.load(open("/Users/Marc/Desktop/Past Affairs/Past Universities/SSE Courses/Master Thesis/twitter_keys.json"))
            client1 = tweepy.Client(consumer_key=keys["consumer_key"], consumer_secret=keys["consumer_secret"], access_token=keys["access_token"], access_token_secret=keys["access_token_secret"])
            bearer_token_bot = str(open("/Users/Marc/Desktop/Past Affairs/Past Universities/SSE Courses/Master Thesis/twitter_bearer_token.txt").read())
            client2 = tweepy.Client(bearer_token=bearer_token_bot)
            auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
            auth.set_access_token(keys["access_token"], keys["access_token_secret"])
            api = tweepy.API(auth)

            # the user ID
            # can also be any other user
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

            text = chatgpt(prompt, key)
            
            # refining the text with a second prompt
            new_prompt = "Write a new coherent tweet out of this text, but don't make it a quote and don't mention weekdays: " + text
            text = chatgpt(new_prompt, key)

            # removing hidden characters
            text = text.replace("\n", "")
            text = text.replace("\\n", "")
            text = text.replace("\\", "")
            text = text.lstrip()
            # text = repr(text)

            # removing leading and trailing 's
            if text[0] == "'" and text[-1] == "'":
                text = text[1:]
                text = text[:-1]

            # removing leading and trailing "s
            if text[0] == '"' and text[-1] == '"':
                text = text[1:]
                text = text[:-1]

            # start over when tweet includes weekdays
            if "Monday" in text or "monday" in text or "Tuesday" in text or "tuesday" in text or "Wednesday" in text or "wednesday" in text or "Thursday" in text or "thursday" in text or "Friday" in text or "friday" in text or "Saturday" in text or "saturday" in text or "Sunday" in text or "sunday" in text:
                raise Exception

            # stopping the program from posting incoherent tweets
            if text[0] == "," or text[0] == "-" or text[0] == "." or text[:6] == "Tweet6" or text[:5] == "Tweet" or text[0] == "#"or text[-1] == '"' or text[0] == "'" or len(text) < 50:
                raise Exception
            
            comment = chatgpt("Write a twitter thread to illustrate the meaning of the following tweet: " + text, key)

            text += " #BeepBoop #R2D2"   
            
            tweet(text, client1)
            
            time.sleep(20)

            # making sure the tweet wasn't posted twice

            user_id = "1612802398442897411"
            tweet_and_id = get_tweets(user_id, client2, max_results=5)

            if tweet_and_id[0][0][0] == "#":
                api.destroy_status(tweet_and_id[1][0])

            # cleaning the comment
            comment = comment.replace("\n", "")
            comment = comment.replace("\\n", "")
            comment = comment.lstrip()
            # comment = repr(comment)

            # removing leading and trailing 's
            if comment[0] == "'" and comment[-1] == "'":
                comment = comment[1:]
                comment = comment[:-1]

            # removing leading and trailing "s
            if comment[0] == '"' and comment[-1] == '"':
                comment = comment[1:]
                comment = comment[:-1]

            # removing the word "thread"
            if comment[:8] == "Thread: ":
                comment = comment[8:]

            # the starting indices of the actual text
            indices = []

            for i in range(len(comment) - 1):
                pair = comment[i:i + 2]
                if pair in ["1.", "2.", "3.", "4.", "5.", "6.", "7." "8.", "9.", "10."]:
                    indices.append(i + 3)

            thread = []
            for i in range(len(indices)):
                if i != len(indices) - 1:
                    thread.append(comment[indices[i]:indices[i + 1] - 3])
                else:
                    # for the final index
                    thread.append(comment[indices[i]:])

            # the number of items in the thread
            n = sum(1 for message in thread if len(message) < 270)

            for message in thread:
                # making sure the thread does't include the original tweet
                if message == text or message[:10] == text[:10]:
                    n -= 1

            text = text[:len(text) - text[::-1].rfind("#") - 2]

            # getting the ID of the this tweet for commeting
            user_id = "1612802398442897411"
            tweet_id = get_tweets(user_id, client2, max_results=5)[1][0]

            i = 1
            for message in thread:
                # the character limit for tweets is 270 => this requirement is most likely satisfied by the individual messages
                if len(message) < 270 and message != text and message[:10] != text[:10]:
                    tweet_id = get_tweets(user_id, client2, max_results=5)[1][0]
                    # remove the trailing hashtags
                    if message.rfind("#") != -1:
                        # remove all text after the first "#"
                        message = message[:len(message) - message[::-1].rfind("#") - 2]
                    message += " (" + str(i) + "/" + str(n) + ")"
                    api.update_status(status=message, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
                    i += 1
                    time.sleep(random.randint(40, 50))
            break

        except Exception:
            print("Error. The process will start over.")
            continue

if __name__ == '__main__':
    main()
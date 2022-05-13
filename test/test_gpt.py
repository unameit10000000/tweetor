import datetime, config, openai


gpt_prompt = "Tweet something awesome about blockchain"
tweetor_message = "Add your own message here.."
gpt_prompt_topic = "blockchain"

openai.api_key = config.GPT_API_KEY
engines = openai.Engine.list()
completion = openai.Completion.create(engine="text-davinci-002", prompt=gpt_prompt)
gpt_msg = f"\n[ gpt-3 👾 generated message - topic: {gpt_prompt_topic[:12]}.. ]\n\n..."+(completion.choices[0].text).replace('\n',' ')+" ..."

dt = datetime.datetime.now()
my_tweet = f"[ auto tweet 🐦 : {dt}  ]\n\n"
my_tweet = my_tweet+tweetor_message+gpt_msg
print(my_tweet)
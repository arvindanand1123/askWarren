import twitter
api = twitter.Api(consumer_key='ij2831NqHVPMmZIPnzR3FQbNq',
                  consumer_secret='2OFP5x73t1GLsDMVLmuGjc0O8Ra3ORayaxv64Smm9FG9xAAptZ',
                  access_token_key='1337787710-fuwH0pzdF8sMEEpaG2t7oNi7rYbqwDcHvEwswba',
                  access_token_secret='MIIU9uNBgiMLvpTY3x31qYgX0pfnHgML8ZKDRFMkKrAX5')

for i in range(0, 29):
	num = 2018 - i
	results = api.GetSearch(
	    raw_query="q=aapl%20since%3A" + str(num-2) + "-09-22%20until%3A" + str(num) + "-09-22&src=typd&count=100")
	for r in results:
		print(r.text)
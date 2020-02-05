import feedparser
import re

#function to get the wordcounts in a feed
# reutns the individual word count with titles
def getwordcount(url):
    wordcounts = {}
    individual_words = []
    titles = []
    d =  feedparser.parse(url)
    for e in d['items']:
        wc = {}
        required_blog_content_for_spliting = e.title + e.content[0].value
        words = get_words(required_blog_content_for_spliting)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
        individual_words.append(wc)
        titles.append(e.title)
    return individual_words, titles


#used in the getwordcount function
#remove html tags
#split words by non-alpha charecters
#return it as a lowercased list
def get_words(html):
    txt = re.sub('<[^>]*>', '', html)
    words = re.split(r'[^A-Z^a-z]', txt)
    return [word.lower() for word in words if word!='']



apcount = {}
wordscount = {}
wc = {}
titles = []
data = []
individual_blog_word_count = []
# elixir_feeds = ["https://medium.com/feed/@minatsilvester", "https://medium.com/feed/@qertoip",
# "https://medium.com/feed/@stueccles", "https://medium.com/feed/@anton.mishchuk"]
#format of api
#called with a keyword(required) and a list of user read feed.
#pass an empty list if no user read feed is available
def get_blogs(keyword, user_read_urls, feed_urls):
    #check if the inputs are in required formats
    print(type(user_read_urls))
    if type(user_read_urls) is list and type(keyword) is str:
        #get the names of all declared variable
        # variables = globals()
        # variable = 0
        #match the feed_url with the required_feed_urls by comparing
        # for variable in variables:
        #         if keyword in variable:
        #             print(variable)
        #             feed_urls = variables[variable]

        if user_read_urls != []:
            for user_read_url in user_read_urls:
                split_user_read_url = user_read_url.split("/")
                for split_part in split_user_read_url:
                    if ".com" in split_part:
                        blog_domain = split_part
                for split_part in split_user_read_url:
                    if "@" in split_part:
                        user_name = split_part
                required_feed_url = "https://" + domain + "/feed/" + user_name
                d = feedparser.parse(required_feed_url)
                for e in d['items']:
                        if keyword in e.title:
                            required_content_for_splitting = e.title + e.content[0].value
                            words = get_words(required_content_for_splitting)
                            for word in words:
                                wc.setdefault(word, 0)
                                wc[word] += 1
                wordscount["user_read_blogs"] = wc
                for word, count in wc.items():
                    apcount.setdefault(word, 0)
                    if count > 1:
                        apcount[word] += 1

        for feedurl in feed_urls:
            individual_words, titles = getwordcount(feedurl)
            for index in range(len(titles)):
                wordscount[titles[index]] = individual_words[index]
            for individual_data in individual_words:
                for word, count in individual_data.items():
                    apcount.setdefault(word, 0)
                    if count > 1:
                        apcount[word] += 1


        wordlist = []
        for w,bc in apcount.items():
            frac = float(bc)/len(titles)
            if frac >= 0 and frac < 0.1: wordlist.append(w)


        for blog, wc in wordscount.items():
            individual_blog_word_count = []
            titles.append(blog)
            for word in wordlist:
                if word in wc: individual_blog_word_count.append(float(wc[word]))
                else: individual_blog_word_count.append(0.0)
            data.append(individual_blog_word_count)


        print(data)
        for d in data:
            print(len(d))

        # out = open('blogdata.txt', 'w')
        # out.write('Blog')
        # for word in wordlist: out.write("\t%s" % word)
        # out.write("\n")
        # for blog, wc in wordscount.items():
        #     out.write(blog)
        #     for word in wordlist:
        #         if word in wc: out.write("\t%d" % wc[word])
        #         else:  out.write('\t0')
        #     out.write("\n")
        return titles, data



# get_blogs("elixir", [])

import urllib.request
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import sent_tokenize, word_tokenize
from bs4 import BeautifulSoup
import requests
import ssl


def web_crawler():
    # starter url in wiki page for la la land
    starter_url = "https://en.wikipedia.org/wiki/La_La_Land"

    # requestion to get the url
    r = requests.get(starter_url)

    # make the beautiful soup to crawl
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    # make the queues to visit and have visited and list to hold relevant urls found
    visited = []
    to_visit = []
    relevant_urls = []

    # first add all the links from the starter page to the queue
    for link in soup.find_all('a'):
        # link_str = str(link.get('href'))
        to_visit.append(link)

    # loop through the queue
    for url in to_visit:

        # check to see if 15 relevant articles have been found
        if len(relevant_urls) == 15:
            # if so print message and return them
            print("Found 15 relevant urls")
            return relevant_urls

        # check if the url has already been visited
        if url not in visited:
            # add url to visited list and remove it from to visit queue
            visited.append(url)
            to_visit.remove(url)

            # check that url starts with http
            link_str = str(url.get('href'))
            if link_str.startswith('http'):
                try:
                    # try to get all the links from the page and add them all to the end of the queue
                    r = requests.get(str(url.get('href')))
                    soup = BeautifulSoup(r.text, "html.parser")
                    for l in soup.find_all('a'):
                        to_visit.append(l)

                    # if la la land is in string it passed relevant check and check some more things
                    if 'la-la-land' in link_str:
                        if link_str.startswith('/url?q='):
                            link_str = link_str[7:]
                        if '&' in link_str:
                            i = link_str.find('&')
                            link_str = link_str[:i]
                        # found some faulty web pages so don't add those to relevant list
                        if link_str.startswith('http') and 'web.archive.org' not in link_str and 'bbfc' not in link_str:
                            relevant_urls.append(link_str)
                            print("Number of relevant links: ",len(relevant_urls))
                except requests.exceptions.ConnectionError and requests.exceptions.TooManyRedirects:
                    pass

def clean_files():
    # open file to hold all the sentences from each page
    sent_file = open("sent_file.txt","w")

    # loop through each file
    for x in range(15):
        # open corresponding file to url and read the lines
        file_read = open("file_"+str(x+1)+".txt","r")
        output = file_read.read()

        # replace the newlines and tabs
        clean = output.replace('\n',' ')
        clean = clean.replace('\t', ' ')

        # tokenize into sentences and write to new file for url and for all urls
        sentences = sent_tokenize(clean)
        file_write = open("clean_file_"+str(x+1)+".txt","w")
        file_write.write(" ".join(str(line) for line in sentences))
        sent_file.write(" ".join(str(line) for line in sentences))

def important_words():
    # make lemmatizer and list to hold lemmas
    wnl = WordNetLemmatizer()
    lemmas = []

    # loop through each file
    for x in range(15):
        # open it for reading
        file_read = open("clean_file_" + str(x+1) + ".txt", "r")

        # read the text and tokenize then do some preprocessing (get rid of stop words and non alphas)
        raw_text = file_read.read()
        tokens = word_tokenize(raw_text)
        tokens2 = [t.lower() for t in tokens]
        tokens3 = [t for t in tokens2 if t.isalpha() and t not in stopwords.words('english')]
        for t in tokens3:
            lemmas.append(wnl.lemmatize(t))

    # make dict of count of each token and print the top 40 terms
    lemmas_unique = list(set(lemmas))
    counts = {t: lemmas.count(t) for t in lemmas_unique}
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("Top 40 terms:")
    for i in range(40):
        print(sorted_counts[i])


def scrape(urls):

    # for each url link
    for link in urls:
        # open file to write the text to
        f = open("file_"+str(urls.index(link) + 1)+".txt", "w")

        # was having issues with request and opening the url so added this line to fix it
        context = ssl._create_unverified_context()

        # open url
        html = urllib.request.urlopen(link, context=context)
        soup = BeautifulSoup(html, "html.parser")

        # write all the text to the file
        for p in soup.select('p'):
            f.write(p.get_text())


def knowledge_base():
    # manually made list of top 10 terms
    top_terms = ['Stone','movie','musical','Chazelle','Gosling','La','Land','Hollywood','love','Mia']

    # open the file with all the sentences
    file = open("sent_file.txt","r")

    # tokenize the sentences
    sents = sent_tokenize(file.read())

    # make dictionary with each top term a key
    kb = {}
    for t in top_terms:
        kb[t] = []

    # for each sentence
    for sent in sents:
        # tokenize it
        tokens = word_tokenize(sent)
        # if a top term is in the sentence add the sentence to the list under the key to make knowledge base
        for t in top_terms:
            if t in tokens:
                kb[t].append(sent)

    print("Knowledge Base:")
    for x in kb:
        print(x)
        print(kb[x], '\n')


def main():
    # call web crawler function to get the relevant urls and print them
    relevant_urls = web_crawler()
    print(*relevant_urls, sep="\n")

    # call function to scrape the 15 relevant urls
    scrape(relevant_urls)

    # call function to clean the files
    clean_files()

    # call function to find important words
    important_words()

    # call function to build knowledge base
    knowledge_base()


if __name__ == "__main__":
    main()


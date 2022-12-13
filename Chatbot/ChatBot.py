import os.path
import pickle
import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import string

# open file with knowledge base
f = open('La La Land.txt','r')
file = f.read()

# tokenize the sentences in the knowledge base and make function remove stopwords
sentences = nltk.sent_tokenize(file)
words = nltk.word_tokenize(file)
words = [w.lower() for w in words if w.isalpha()]
stop_wprds = set(stopwords.words('english'))
def remove_stopwords(sent):
    result = [w for w in sent if not w.lower() in stop_wprds]
    return " ".join(result)

# make knowlede base dictionary
top_terms = ['Stone','movie','musical','Chazelle','Gosling','Land','Hollywood','love','Mia']
kb = {}
# loop through the sentence in knowledge base and make dictionary with top terms
#file2 = open('KBfile.txt','w')
for t in top_terms:
    kb[t] = []
for sent in sentences:
    # tokenize it
    remove_stopwords(sent)
    sent = sent.replace("\n"," ")
    tokens = nltk.word_tokenize(sent)
    # if a top term is in the sentence add the sentence to the list under the key to make knowledge base
    for t in top_terms:
        if t in tokens:
            kb[t].append(sent)


# tuples to hold some key phrases
Greeting_in = ('hello','hi','hey')
Greeting_out = ('welcome','hello','hi there','*silent acknowledgement of presence*')
Opinion_in = ['you']
Likes_Dislikes = ('i like',"i don't like", "i dislike", 'i think', "i'm", 'i want')

# functions to lemmatize the words
lemmatizer = nltk.WordNetLemmatizer()
def Lemmatize(tokens):
    return [lemmatizer.lemmatize(t) for t in tokens]

# replace all the punctuation
rem = dict((ord(p),None) for p in string.punctuation)

def lem(text):
    return Lemmatize(nltk.word_tokenize(text.lower().translate(rem)))

# chooses a greeting a random for bot to respond
def greeting(user_input):
    for word in user_input.split():
        if word.lower() in Greeting_in:
            return random.choice(Greeting_out)

# function to get bot response
def response(user_input):
    # fit and transform the sentences in knowledge base
    bot_response = ''
    tfidvector = TfidfVectorizer(tokenizer=Lemmatize)
    tfidf = tfidvector.fit_transform(sentences)

    # go through each sentence and find cosine similarity to input sentence
    vals = cosine_similarity(tfidf[-1],tfidf)
    index = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    required = flat[-2]
    if required == 0:
        # if no similar sentence return empty string
        bot_response += ""
        return bot_response
    else:
        # return most similar sentence
        bot_response += sentences[index]
        return bot_response

# opening statement from bot
print("Bot: Hello! If you want to talk about La La Land the movie you came to the right place. When you want to exit say Bye. ")
inputName = input("Bot: First, what's your name?\n")


#   USE A PICKLE TO SAVE
# check if there is already user model file
if os.path.isfile("Chatbot_userFile.p") and os.stat("Chatbot_userFile.p").st_size != 0:
    user_model = pickle.load(open("Chatbot_userFile.p","rb+"))
    # for k,v in user_model.items():
    #    print(k,": ",v)
    # check if the user is known
    if inputName in user_model:
        print("Welcome back", inputName, "! What do you want to talk about this time?")
    else:
        print("Hey", inputName, "! Let's get started!")
        user_model[inputName] = []
else:
    user_model = {}
    print("Hey", inputName, "! Let's get started!")
    user_model[inputName] = []


# while loop that runs the chatbot
flag = True
while flag:
    # flag to determine if input is asking about chatbot opinion
    op = False
    # get the input from the user
    responseInput = input().lower()

    # check if the input is asking about chatbot, if it is set flag to true
    for w in responseInput.split():
        if w in Opinion_in:
            op = True

    # check if the input is about the user, if it is add to user model
    for str in Likes_Dislikes:
        if str in responseInput:
            user_model[inputName].append(responseInput)

    # if user says bye, set flag to end while loop
    if responseInput == "bye":
        flag = False
        print("Bot: Bye!")
    else:
        # check if input is greeting
        if greeting(responseInput) != None:
            print("Bot: ",greeting(responseInput))
        # check flag for asking about chatbot
        elif op:
            print("Bot: I'm not sure, how about you?")
        else:
            # get the bot response
            sentences.append(responseInput)
            words.append(nltk.word_tokenize(responseInput))
            answer = response(responseInput)
            if answer == "":
                if user_model:
                    topic = random.choice(user_model[inputName])
                    print("Bot: You said this ealier '",topic,"' let's expand on that.")
                else:
                    print("Bot: Im not too familiar with that topic, ask something else please")
            else:
                print("Bot: ",answer)
            sentences.remove(responseInput)

# dump user model to file
with open("Chatbot_userFile.p", 'wb') as file:
    pickle.dump(user_model,file)

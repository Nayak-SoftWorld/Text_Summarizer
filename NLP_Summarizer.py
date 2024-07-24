import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
# from sklearn.metrics import precision_score, recall_score, f1_score
# import matplotlib.pyplot as plt

from rouge import Rouge

text = """
There are broadly two types of extractive summarization tasks depending on what the summarization program focuses on. 
The first is generic summarization, which focuses on obtaining a generic summary or abstract of the collection (whether documents, or sets of images, or videos, news stories etc.). 
The second is query relevant summarization, sometimes called query-based summarization, which summarizes objects specific to a query. Summarization systems are able to create both query relevant text summaries and generic machine-generated summaries depending on what the user needs. 
An example of a summarization problem is document summarization, which attempts to automatically produce an abstract from a given document. 
Sometimes one might be interested in generating a summary from a single source document, while others can use multiple source documents (for example, a cluster of articles on the same topic). 
This problem is called multi-document summarization. A related application is summarizing news articles. Imagine a system, which automatically pulls together news articles on a given topic (from the web), and concisely represents the latest news as a summary. 
Image collection summarization is another application example of automatic summarization. It consists in selecting a representative set of images from a larger set of images.[3] A summary in this context is useful to show the most representative images of results in an image collection exploration system. 
Video summarization is a related domain, where the system automatically creates a trailer of a long video. This also has applications in consumer or personal videos, where one might want to skip the boring or repetitive actions. 
Similarly, in surveillance videos, one would want to extract important and suspicious activity, while ignoring all the boring and redundant frames captured.
"""
 
#text = '''The terms “machine learning” and “artificial intelligence” first appeared in 1952 and 1956, respectively. Fast-forward to over a half-century later, and in 2010, researchers George Dahl and Abdel-rahman Mohamed proved that deep learning speech recognition tools could beat the contemporary state-of-the-art industry solutions. At the same time, Google announced its self-driving automobile project, now called Waymo. Finally, DeepMind, a pioneer in the fields of AI and deep learning, was established in September 2010. We will hear more about them later. In 2011, AI put humanity's mental dominance in jeopardy when Watson, IBM’s question and answer system, defeated reigning Jeopardy! champions Brad Rutter and Ken Jennings. No doubt Watson’s “ancestor” Deep Blue, the computer that defeated Russian chess grandmaster Garry Kasparov in 1997, would have been proud! While IBM machines were showing up human intellects, Apple introduced Siri, its virtual assistant. Siri uses speech recognition, a natural language user interface, and convolutional neural networks. The technology enables users to conduct searches, make recommendations, answer questions, and perform tasks via internet services. Everybody knows that the internet and cats share a deep and abiding relationship. So, it was unsurprising that this entertaining partnership experienced a major milestone in 2012. The Google Brain Team, led by Jeff Dean and Andrew Ng, developed a neural network that recognized cats on YouTube by watching unlabeled images from video frames. 2012 was also the year Oculus VR was incorporated and used Kickstarter to fund its first Oculus Rift virtual reality headset. The technology was so exciting that Facebook acquired the company only two years later. The Oculus Rift is used in many applications beyond VR gaming, including industrial visualization and design, education, and media. In 2013, Boston Dynamics, maker of the 4-legged robot BigDog, created Atlas. Six feet tall and humanoid in form, Atlas has since evolved to operate both indoors and outdoors and can carry out a variety of human activities, like driving a vehicle, opening and closing doors, climbing a ladder, and attaching and operating a fire hose. Its purpose is to perform search and rescue operations in environments too dangerous for humans. Also in 2013, Google introduced a beta test version of Google Glass. Google Glass is a heads-up display mounted on eyeglasses and supports AR and AI applications, including facial recognition and text translation. Over time, Google Glass has transitioned from a consumer product to an industrial tool, while some AR applications have been integrated into Android phones as Google Lens. Google turned heads again in 2014 when it bought the earlier-mentioned DeepMind for a whopping $500 million. Meanwhile, Facebook researchers revealed their work on DeepFace, a neural network system that identifies faces with over 97 percent accuracy. Machine Vs. Machine Finally, 2014 saw the invention of generative adversarial networks, a machine learning system where two neural networks compete against each other to create better solutions to problems. This competition artificially creates new, original content. In 2015, AI continued its mastery in games when AlphaGo, powered by DeepMind, beat a human professional Go master for the first time. Google, meanwhile, demonstrated its driverless car, powered by the Waymo model. 2016 saw the world's greatest Go player, Lee Sedol, lose to AlphaGo. Also, that year, the Face2Face program enabled users to create deepfake videos. Deepfake, a mix of the terms “deep learning” and “fake,” uses AI and ML techniques to create or manipulate audio and video footage. This development has drawn its share of controversy since technology can manipulate videos and create fraudulent or libelous content.'''

def summarizer(rawdocs,sum_perc):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(rawdocs)
    tokens = [token.text for token in doc]
    #print(tokens)
    #punctuation = punctuation + "\n"
    #punctuation
    print("summary percentage" , sum_perc)
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
                    
    #print(word_frequencies)

    max_frequency = max(word_frequencies.values())
    #print(max_frequency)

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    #print(word_frequencies)

    sentence_tokens = [sent for sent in doc.sents]
    #print(sentence_tokens)

    sentence_score  = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_score[sent] += word_frequencies[word.text.lower()]
    #sentence_score

    select_length = int(len(sentence_tokens)*sum_perc/100)
    #print(select_length)

    summary = nlargest(select_length, sentence_score, key = sentence_score.get)
    #print(summary)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    '''print("Original Text: \n",text)
    print("\nHere is your summary: \n",summary)

    print("Length of originl text: ",len(text.split(' ')))
    print("Length of summarized text: ",len(summary.split(' ')))'''

    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))




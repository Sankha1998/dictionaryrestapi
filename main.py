from flask import Flask,jsonify
import requests
import bs4
from bs4 import BeautifulSoup as bs
import lxml
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.config['JSON_SORT_KEYS'] = False

def wordMeaning(url,headers):
    response = requests.get(url, headers=headers).text
    soup = bs(response, 'lxml')
    data = soup.find_all('div', class_="definition-wrapper")
    meaning = []
    c = 0
    for i in data:
        if (c < 5):
            meaning.append(i.text.strip(''))
            c += 1
        else:
            pass
    return meaning


def wordSynonyms(url,headers):
    response = requests.get(url, headers=headers).text
    soup = bs(response, 'lxml')
    data = soup.find_all('div', class_='synonym-link-wrapper')
    synonyms = []
    c = 0
    for i in data:
        if (c < 5):
            synonyms.append(i.text.strip(''))
            c += 1
        else:
            pass

    return synonyms


def WordSentences(url,headers):
    response = requests.get(url, headers=headers).text
    soup = bs(response, 'lxml')
    data = soup.find_all('div', class_='sentence component')
    sentences = []
    c = 0
    for i in data:
        if (c < 10):
            sentences.append(i.text.strip(''))
            c += 1
        else:
            pass
    return sentences



@app.route('/api/<string:word>')
def data(word):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = 'https://www.yourdictionary.com/{}'.format(word)
    url1 = 'https://thesaurus.yourdictionary.com/{}'.format(word)
    url2 = 'https://sentence.yourdictionary.com/{}'.format(word)

    meanings = wordMeaning(url,headers)
    synonyms = wordSynonyms(url1,headers)
    sentences = WordSentences(url2,headers)

    result = {
        'word': word,
        'meaning':meanings,
        'synonyms':synonyms,
        'sentences':sentences
    }
    return jsonify(result)





if __name__=="__main__":
    app.run(debug=True)
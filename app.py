from flask import Flask, render_template, request
from transformers import *
import requests
from bs4 import BeautifulSoup

app = Flask('summary_app')
model = pipeline("summarization", model="facebook/bart-large-cnn")

#map url / to fuction show_index()
@app.route('/')
def show_index():
    return render_template('index.html')

#url /results is now mapped to results() function
@app.route('/resultArt', methods=['POST'])
def result1():
    if request.method == 'POST':
        lst = [x for x in request.form.values()]
        ARTICLE = lst[0]
        minln = int(request.form.get("length"))
        maxln = int(1.2*minln)
        result = model(ARTICLE, max_length=maxln, min_length=minln, do_sample=False)
        return render_template('index.html',fin_summary = result[0]["summary_text"])

@app.route('/resultLink', methods=['POST'])
def result2():
    if request.method == 'POST':
        lst = [x for x in request.form.values()]
        LINK = lst[0]
        minln = int(request.form.get("length"))
        maxln = int(1.2*minln)
        page = requests.get(LINK)
        soup = BeautifulSoup(page.content, 'html.parser')
        p_tags = soup.find_all('p')
        p_tags_text = [tag.get_text().strip() for tag in p_tags]

        # Filter out sentences that contain newline characters '\n' or don't contain periods.
        sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
        sentence_list = [sentence for sentence in sentence_list if '.' in sentence]

        content = ' '.join(sentence_list)

        # keeping in range.
        arr = content.split(' ')
        len(arr)
        f1k=" "
        for i in range(600):
            f1k += (arr[i]+" ")
        result = model(f1k, max_length=maxln, min_length=minln, do_sample=False)
        return render_template('index.html',fin_summary = result[0]["summary_text"])
app.run("localhost", debug=True)
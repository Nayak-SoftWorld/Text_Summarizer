from flask import Flask, render_template, request
#hello!
from NLP_Summarizer import summarizer
app = Flask(__name__)

@app.route('/')

def index():
    return render_template("index.html")

@app.route ('/analyze', methods=['GET','POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        sum_perc=int(request.form.get("Summ_Percent"))
        print(sum_perc)
        summary, original_txt, len_original_txt, len_summary = summarizer(rawtext,sum_perc)

    return render_template('summary.html', summary = summary, original_txt = original_txt, len_original_txt = len_original_txt, len_summary = len_summary)
if __name__ == "__main__":
    app.run(debug = True)

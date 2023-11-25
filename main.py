from flask import Flask, request
from flask_cors import CORS, cross_origin
from parser_fun import extract_article
from summary_generator import SummaryGenerator

summary_generator_obj = SummaryGenerator("sumarizer")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/generate", methods = ["GET", "POST"])
@cross_origin()
def generate():
    if request.method == "POST":
        url = request.json["url"]
        word_count = request.json["word_count"]

        text = extract_article(url)

        summary = summary_generator_obj.sumarize(text, max_length=word_count)

        return {
            "summary" : summary
        }

app.run()
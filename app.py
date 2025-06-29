from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

with open("celebrities.json") as f:
    celebrities = json.load(f)

questions = [
    ("gender", "Is the celebrity male or female?"),
    ("occupation", "Are they a singer, actor, sportsperson, scientist, or host?"),
    ("origin", "Are they American, Indian, German, or Portuguese?"),
    ("status", "Are they alive or dead?"),
    ("age", "Are they under or over 40?")
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        answers = request.form.to_dict()
        guessed = filter_celebrities(answers)
        return render_template("result.html", guess=guessed)
    return render_template("index.html", questions=questions)

def filter_celebrities(answers):
    filtered = celebrities
    mapping = {
        "gender": lambda c: answers["gender"] in c["traits"],
        "occupation": lambda c: answers["occupation"] in c["traits"],
        "origin": lambda c: answers["origin"].lower() in c["traits"],
        "status": lambda c: answers["status"] in c["traits"],
        "age": lambda c: answers["age"] in c["traits"]
    }
    for key, rule in mapping.items():
        filtered = list(filter(rule, filtered))
    return filtered[0]["name"] if filtered else "No match found"

if __name__ == "__main__":
    app.run(debug=True)

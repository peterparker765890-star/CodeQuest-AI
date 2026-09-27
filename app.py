from flask import Flask, render_template, jsonify

app = Flask(__name__)

# -----------------------------
# CODEQUEST AI - V0.1
# -----------------------------

subjects = [
    {
        "name": "💻 Computer Basics",
        "description": "Start from zero and understand computers.",
        "level": "Beginner"
    },
    {
        "name": "📝 MS Word",
        "description": "Learn documents, formatting and practical skills.",
        "level": "Beginner"
    },
    {
        "name": "📊 MS Excel",
        "description": "Learn formulas, functions, charts and data.",
        "level": "Beginner"
    },
    {
        "name": "📑 MS Office",
        "description": "Master essential office productivity tools.",
        "level": "Beginner"
    },
    {
        "name": "🧠 Programming Fundamentals",
        "description": "Build programming logic before learning a language.",
        "level": "Beginner"
    },
    {
        "name": "🔵 C Language",
        "description": "Learn C from your first program to advanced concepts.",
        "level": "Beginner → Master"
    },
    {
        "name": "🟣 C++",
        "description": "Learn C++ and object-oriented programming.",
        "level": "Beginner → Master"
    },
    {
        "name": "🧩 OOP Concepts",
        "description": "Understand classes, objects, inheritance and polymorphism.",
        "level": "Intermediate"
    },
    {
        "name": "🐍 Python",
        "description": "Learn Python from basics to projects.",
        "level": "Beginner → Master"
    },
    {
        "name": "☕ Java",
        "description": "Learn Java and object-oriented programming.",
        "level": "Beginner → Master"
    }
]


@app.route("/")
def home():
    return render_template(
        "index.html",
        subjects=subjects
    )


@app.route("/api/subjects")
def get_subjects():
    return jsonify(subjects)


@app.route("/api/status")
def status():
    return jsonify({
        "app": "CodeQuest AI",
        "version": "0.1",
        "status": "online"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
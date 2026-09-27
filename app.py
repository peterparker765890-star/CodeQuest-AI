from flask import Flask, render_template, jsonify

app = Flask(__name__)

# =========================================================
# CODEQUEST AI — V0.2
# Learn • Practice • Play • Build
# =========================================================

courses = {

    "Computer Basics": {
        "icon": "💻",
        "level": "Beginner",
        "description": "Start from zero and understand computers.",
        "chapters": [
            "What is a Computer?",
            "Hardware and Software",
            "Input and Output Devices",
            "Operating Systems",
            "Files and Folders",
            "Internet Basics",
            "Computer Safety",
            "Practical Computer Skills"
        ]
    },

    "MS Word": {
        "icon": "📝",
        "level": "Beginner",
        "description": "Create professional documents from scratch.",
        "chapters": [
            "Introduction to MS Word",
            "Creating and Saving Documents",
            "Text Formatting",
            "Paragraph Formatting",
            "Tables",
            "Images and Shapes",
            "Headers and Footers",
            "Page Layout",
            "References",
            "Mail Merge",
            "Practical Document Project"
        ]
    },

    "MS Excel": {
        "icon": "📊",
        "level": "Beginner → Advanced",
        "description": "Learn spreadsheets, formulas, data and charts.",
        "chapters": [
            "Introduction to Excel",
            "Cells, Rows and Columns",
            "Data Entry",
            "Basic Formulas",
            "Functions",
            "IF and Logical Functions",
            "Sorting and Filtering",
            "Charts",
            "Conditional Formatting",
            "Data Analysis",
            "Practical Excel Project"
        ]
    },

    "MS Office": {
        "icon": "📑",
        "level": "Beginner → Advanced",
        "description": "Master essential Microsoft Office skills.",
        "chapters": [
            "Introduction to MS Office",
            "Word Basics",
            "Excel Basics",
            "PowerPoint Basics",
            "Creating Presentations",
            "Office Productivity",
            "File Management",
            "Professional Office Skills",
            "Mini Office Project"
        ]
    },

    "Programming Fundamentals": {
        "icon": "🧠",
        "level": "Beginner",
        "description": "Build programming logic before learning languages.",
        "chapters": [
            "What is Programming?",
            "Algorithms",
            "Flowcharts",
            "Variables",
            "Data Types",
            "Operators",
            "Conditions",
            "Loops",
            "Functions",
            "Problem Solving",
            "Introduction to Debugging"
        ]
    },

    "C Language": {
        "icon": "🔵",
        "level": "Beginner → Master",
        "description": "Learn C from your first program to advanced concepts.",
        "chapters": [
            "Introduction to C",
            "Structure of a C Program",
            "Variables and Data Types",
            "Input and Output",
            "Operators",
            "if and else",
            "switch",
            "for Loop",
            "while Loop",
            "do while Loop",
            "Arrays",
            "Strings",
            "Functions",
            "Recursion",
            "Pointers",
            "Structures",
            "Unions",
            "File Handling",
            "Dynamic Memory",
            "Advanced C",
            "C Mini Projects",
            "Final C Challenge"
        ]
    },

    "C++": {
        "icon": "🟣",
        "level": "Beginner → Master",
        "description": "Learn C++ and modern object-oriented programming.",
        "chapters": [
            "Introduction to C++",
            "Basic Syntax",
            "Variables and Data Types",
            "Input and Output",
            "Operators",
            "Conditions",
            "Loops",
            "Arrays and Strings",
            "Functions",
            "Classes and Objects",
            "Constructors",
            "Inheritance",
            "Polymorphism",
            "Encapsulation",
            "Abstraction",
            "Templates",
            "STL Basics",
            "File Handling",
            "C++ Projects",
            "Final C++ Challenge"
        ]
    },

    "OOP Concepts": {
        "icon": "🧩",
        "level": "Intermediate",
        "description": "Understand the core ideas behind object-oriented programming.",
        "chapters": [
            "What is OOP?",
            "Classes",
            "Objects",
            "Constructors",
            "Encapsulation",
            "Inheritance",
            "Polymorphism",
            "Abstraction",
            "Method Overloading",
            "Method Overriding",
            "Real World OOP",
            "OOP Mini Project"
        ]
    },

    "Python": {
        "icon": "🐍",
        "level": "Beginner → Master",
        "description": "Learn Python from your first program to real projects.",
        "chapters": [
            "Introduction to Python",
            "Python Syntax",
            "Variables",
            "Data Types",
            "Input and Output",
            "Operators",
            "if and else",
            "Loops",
            "Lists",
            "Tuples",
            "Sets",
            "Dictionaries",
            "Functions",
            "Lambda Functions",
            "Modules",
            "File Handling",
            "Exception Handling",
            "Object-Oriented Python",
            "Libraries",
            "Python Projects",
            "Final Python Challenge"
        ]
    },

    "Java": {
        "icon": "☕",
        "level": "Beginner → Master",
        "description": "Learn Java and object-oriented programming.",
        "chapters": [
            "Introduction to Java",
            "Java Syntax",
            "Variables and Data Types",
            "Input and Output",
            "Operators",
            "Conditions",
            "Loops",
            "Arrays",
            "Strings",
            "Methods",
            "Classes and Objects",
            "Constructors",
            "Inheritance",
            "Polymorphism",
            "Interfaces",
            "Exception Handling",
            "Collections",
            "File Handling",
            "Java Projects",
            "Final Java Challenge"
        ]
    }
}


# =========================================================
# QUIZ ARENA
# =========================================================

quiz_questions = [

    {
        "question": "Which language is known for its simplicity and readability?",
        "options": ["C", "Python", "Assembly", "Machine Code"],
        "answer": 1,
        "explanation": "Python is designed with simple and readable syntax."
    },

    {
        "question": "Which symbol is commonly used to end a statement in C?",
        "options": [".", ",", ";", ":"],
        "answer": 2,
        "explanation": "C statements normally end with a semicolon (;)."
    },

    {
        "question": "Which component is known as the brain of a computer?",
        "options": ["RAM", "CPU", "Keyboard", "Monitor"],
        "answer": 1,
        "explanation": "The CPU processes instructions and performs calculations."
    },

    {
        "question": "Which Excel function is commonly used to calculate a total?",
        "options": ["TOTAL()", "SUM()", "ADD()", "PLUS()"],
        "answer": 1,
        "explanation": "SUM() adds numbers together in Excel."
    },

    {
        "question": "Which OOP concept allows one class to acquire properties of another?",
        "options": [
            "Encapsulation",
            "Inheritance",
            "Abstraction",
            "Compilation"
        ],
        "answer": 1,
        "explanation": "Inheritance allows a class to derive properties and behaviour from another class."
    },

    {
        "question": "What does HTML mainly describe?",
        "options": [
            "Database queries",
            "Web page structure",
            "Computer hardware",
            "Operating systems"
        ],
        "answer": 1,
        "explanation": "HTML defines the structure of web pages."
    }
]


# =========================================================
# CODE CHALLENGES
# =========================================================

code_challenges = [

    {
        "language": "C",
        "question": "What will this program print?",
        "code": """#include <stdio.h>

int main() {
    int a = 5;
    int b = 3;

    printf("%d", a + b);

    return 0;
}""",
        "options": ["2", "8", "15", "53"],
        "answer": 1,
        "explanation": "5 + 3 = 8."
    },

    {
        "language": "Python",
        "question": "What will this program print?",
        "code": """a = 10
b = 2

print(a * b)""",
        "options": ["12", "20", "102", "5"],
        "answer": 1,
        "explanation": "10 × 2 = 20."
    },

    {
        "language": "C++",
        "question": "What will this program print?",
        "code": """#include <iostream>
using namespace std;

int main() {
    cout << 10 - 4;
    return 0;
}""",
        "options": ["6", "14", "104", "Error"],
        "answer": 0,
        "explanation": "10 - 4 = 6."
    }
]


# =========================================================
# ERROR FINDER
# =========================================================

error_challenges = [

    {
        "language": "C",
        "question": "Find the error:",
        "code": """#include <stdio.h>

int main() {
    int age = 18
    printf("%d", age);
    return 0;
}""",
        "options": [
            "Missing semicolon after 18",
            "printf is wrong",
            "main cannot return 0",
            "No error"
        ],
        "answer": 0,
        "explanation": "The statement int age = 18 needs a semicolon."
    },

    {
        "language": "Python",
        "question": "Find the error:",
        "code": """age = 20

if age >= 18
    print("Adult")""",
        "options": [
            "Missing colon after the condition",
            "age cannot be 20",
            "print is invalid",
            "No error"
        ],
        "answer": 0,
        "explanation": "Python requires a colon (:) after an if condition."
    }
]


# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def home():
    return render_template(
        "index.html",
        courses=courses
    )


@app.route("/api/courses")
def get_courses():
    return jsonify(courses)


@app.route("/api/course/<course_name>")
def get_course(course_name):

    if course_name not in courses:
        return jsonify({
            "error": "Course not found"
        }), 404

    return jsonify(courses[course_name])


@app.route("/api/quiz")
def get_quiz():
    return jsonify(quiz_questions)


@app.route("/api/code-challenges")
def get_code_challenges():
    return jsonify(code_challenges)


@app.route("/api/error-finder")
def get_error_challenges():
    return jsonify(error_challenges)


@app.route("/api/status")
def status():
    return jsonify({
        "app": "CodeQuest AI",
        "version": "0.2",
        "status": "online",
        "features": [
            "Learning",
            "Quiz Arena",
            "Code Challenges",
            "Error Finder",
            "AI Career Assistant",
            "Online Compiler",
            "Progress Tracking"
        ]
    })


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
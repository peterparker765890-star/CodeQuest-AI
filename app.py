from flask import Flask, render_template, jsonify, request, session
from functools import wraps
from datetime import datetime, timezone
import os
import random
import secrets
import time

app = Flask(__name__)

# =========================================================
# CODEQUEST AI
# Learn • Practice • Play • Build
# =========================================================

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    secrets.token_hex(32)
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("RENDER") == "true"


# =========================================================
# COURSES
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
            "Memory and Storage",
            "Operating Systems"
        ]
    },

    "MS Word": {
        "icon": "📝",
        "level": "Beginner",
        "description": "Learn document creation and formatting.",
        "chapters": [
            "Introduction to MS Word",
            "Creating Documents",
            "Text Formatting",
            "Tables and Images",
            "Page Layout"
        ]
    },

    "MS Excel": {
        "icon": "📊",
        "level": "Beginner",
        "description": "Learn spreadsheets, formulas and data.",
        "chapters": [
            "Introduction to Excel",
            "Cells and Worksheets",
            "Formulas",
            "Functions",
            "Charts"
        ]
    },

    "MS PowerPoint": {
        "icon": "📽️",
        "level": "Beginner",
        "description": "Create professional presentations.",
        "chapters": [
            "Introduction to PowerPoint",
            "Creating Slides",
            "Themes and Design",
            "Images and Media",
            "Animations and Transitions"
        ]
    },

    "MS Office": {
        "icon": "📦",
        "level": "Beginner",
        "description": "Understand the Microsoft Office ecosystem.",
        "chapters": [
            "What is MS Office?",
            "Word",
            "Excel",
            "PowerPoint",
            "Office Productivity"
        ]
    },

    "Programming Fundamentals": {
        "icon": "🧠",
        "level": "Beginner",
        "description": "Build your programming foundation.",
        "chapters": [
            "What is Programming?",
            "Algorithms",
            "Variables",
            "Data Types",
            "Operators",
            "Conditional Statements",
            "Loops",
            "Functions",
            "Arrays"
        ]
    },

    "C Language": {
        "icon": "©️",
        "level": "Intermediate",
        "description": "Learn the fundamentals of C programming.",
        "chapters": [
            "Introduction to C",
            "Variables and Data Types",
            "Operators",
            "if and else",
            "Loops",
            "Functions",
            "Arrays",
            "Pointers"
        ]
    },

    "C++": {
        "icon": "⚙️",
        "level": "Intermediate",
        "description": "Learn C++ and object-oriented programming.",
        "chapters": [
            "Introduction to C++",
            "Variables and Data Types",
            "Functions",
            "Classes and Objects",
            "Inheritance",
            "Polymorphism"
        ]
    },

    "OOP Concepts": {
        "icon": "🧩",
        "level": "Intermediate",
        "description": "Understand object-oriented programming.",
        "chapters": [
            "What is OOP?",
            "Classes and Objects",
            "Encapsulation",
            "Inheritance",
            "Polymorphism",
            "Abstraction"
        ]
    },

    "Python": {
        "icon": "🐍",
        "level": "Beginner",
        "description": "Learn Python from basics to practical programming.",
        "chapters": [
            "Introduction to Python",
            "Variables",
            "Data Types",
            "Conditions",
            "Loops",
            "Functions",
            "Lists and Dictionaries",
            "Modules"
        ]
    },

    "Java": {
        "icon": "☕",
        "level": "Intermediate",
        "description": "Learn Java programming.",
        "chapters": [
            "Introduction to Java",
            "Variables",
            "Data Types",
            "Conditions",
            "Loops",
            "Classes and Objects",
            "Inheritance"
        ]
    },

    "HTML": {
        "icon": "🌐",
        "level": "Beginner",
        "description": "Build the structure of websites.",
        "chapters": [
            "What is HTML?",
            "HTML Elements",
            "Headings and Paragraphs",
            "Links and Images",
            "Tables",
            "Forms"
        ]
    },

    "CSS": {
        "icon": "🎨",
        "level": "Beginner",
        "description": "Style and design modern websites.",
        "chapters": [
            "What is CSS?",
            "Selectors",
            "Colors and Fonts",
            "Box Model",
            "Flexbox",
            "Responsive Design"
        ]
    },

    "JavaScript": {
        "icon": "⚡",
        "level": "Intermediate",
        "description": "Add logic and interactivity to websites.",
        "chapters": [
            "Introduction to JavaScript",
            "Variables",
            "Functions",
            "Conditions",
            "Loops",
            "DOM",
            "Events"
        ]
    },

    "SQL": {
        "icon": "🗄️",
        "level": "Intermediate",
        "description": "Learn databases and SQL queries.",
        "chapters": [
            "What is a Database?",
            "SQL Basics",
            "SELECT",
            "INSERT",
            "UPDATE",
            "DELETE",
            "Joins"
        ]
    },

    "Data Structures": {
        "icon": "🌳",
        "level": "Intermediate",
        "description": "Learn how data is organized and processed.",
        "chapters": [
            "Introduction to Data Structures",
            "Arrays",
            "Stacks",
            "Queues",
            "Linked Lists",
            "Trees",
            "Searching and Sorting"
        ]
    },

    "Git and GitHub": {
        "icon": "🐙",
        "level": "Intermediate",
        "description": "Learn version control and GitHub.",
        "chapters": [
            "What is Git?",
            "Git Installation",
            "Repositories",
            "Commit and Push",
            "Branches",
            "GitHub"
        ]
    },

    "Computer Networks": {
        "icon": "🌐",
        "level": "Intermediate",
        "description": "Understand computer networking.",
        "chapters": [
            "What is a Network?",
            "LAN and WAN",
            "IP Addresses",
            "Protocols",
            "Network Devices",
            "Internet"
        ]
    },

    "Cybersecurity Fundamentals": {
        "icon": "🔐",
        "level": "Intermediate",
        "description": "Learn the fundamentals of cybersecurity.",
        "chapters": [
            "What is Cybersecurity?",
            "Threats and Vulnerabilities",
            "Passwords and Authentication",
            "Encryption",
            "Phishing",
            "Safe Computing"
        ]
    }
}


# =========================================================
# LESSON GENERATOR
# =========================================================

def create_lesson(chapter, course_name):

    lessons = {

        "What is a Computer?": {
            "title": "What is a Computer?",
            "content": """
A computer is an electronic device that accepts data,
processes it according to instructions, stores information,
and produces useful output.

The basic working cycle is:

Input → Processing → Output → Storage
""",
            "points": [
                "Accepts input",
                "Processes data",
                "Produces output",
                "Stores information"
            ],
            "example": """input_data = 10 + 20
result = input_data
print(result)"""
        },

        "What is Programming?": {
            "title": "What is Programming?",
            "content": """
Programming is the process of writing instructions that
tell a computer how to perform a task.

A programming language allows humans to communicate
instructions to a computer.
""",
            "points": [
                "Programs contain instructions",
                "Programming solves problems",
                "Different languages are used for different tasks"
            ],
            "example": """marks = [80, 70, 90]
average = sum(marks) / len(marks)
print(average)"""
        },

        "Algorithms": {
            "title": "Algorithms",
            "content": """
An algorithm is a step-by-step procedure used to solve
a particular problem.

A good algorithm should be clear, finite and effective.
""",
            "points": [
                "Step-by-step solution",
                "Clear instructions",
                "Must eventually finish",
                "Used before writing programs"
            ],
            "example": """a = 10
b = 20
largest = max(a, b)
print(largest)"""
        },

        "Variables": {
            "title": "Variables",
            "content": """
A variable is a named location used to store data.

The value stored in a variable can change during program
execution.
""",
            "points": [
                "Stores data",
                "Has a name",
                "Value can change"
            ],
            "example": """age = 18
print(age)"""
        },

        "Introduction to C": {
            "title": "Introduction to C",
            "content": """
C is a general-purpose programming language widely used
for system programming, embedded systems and learning
programming fundamentals.
""",
            "points": [
                "Created by Dennis Ritchie",
                "Fast and efficient",
                "Supports structured programming"
            ],
            "example": """#include <stdio.h>

int main() {
    printf("Hello World");
    return 0;
}"""
        },

        "Introduction to Python": {
            "title": "Introduction to Python",
            "content": """
Python is a high-level programming language known for
its simple syntax and wide range of applications.
""",
            "points": [
                "Easy to learn",
                "Readable syntax",
                "Used in AI, web development and automation"
            ],
            "example": """print("Hello World")"""
        },

        "Introduction to C++": {
            "title": "Introduction to C++",
            "content": """
C++ is a powerful programming language that supports both
procedural and object-oriented programming.
""",
            "points": [
                "High performance",
                "Supports OOP",
                "Used in games and software"
            ],
            "example": """#include <iostream>
using namespace std;

int main() {
    cout << "Hello World";
    return 0;
}"""
        },

        "What is OOP?": {
            "title": "What is OOP?",
            "content": """
Object-Oriented Programming is a programming approach
based on objects and classes.

The major concepts include encapsulation, inheritance,
polymorphism and abstraction.
""",
            "points": [
                "Classes",
                "Objects",
                "Encapsulation",
                "Inheritance",
                "Polymorphism",
                "Abstraction"
            ],
            "example": """class Student:
    def __init__(self, name):
        self.name = name

student = Student("Joe")
print(student.name)"""
        },

        "What is HTML?": {
            "title": "What is HTML?",
            "content": """
HTML stands for HyperText Markup Language.

It is used to create the structure of web pages.
""",
            "points": [
                "Creates webpage structure",
                "Uses elements and tags",
                "Works with CSS and JavaScript"
            ],
            "example": """<!DOCTYPE html>
<html>
<body>
    <h1>Hello World</h1>
</body>
</html>"""
        },

        "What is CSS?": {
            "title": "What is CSS?",
            "content": """
CSS stands for Cascading Style Sheets.

It is used to control the appearance and layout of
HTML elements.
""",
            "points": [
                "Controls colors",
                "Controls fonts",
                "Controls spacing",
                "Creates responsive layouts"
            ],
            "example": """body {
    background: black;
    color: white;
}"""
        },

        "What is Cybersecurity?": {
            "title": "What is Cybersecurity?",
            "content": """
Cybersecurity is the practice of protecting computers,
networks, applications and data from unauthorized access,
damage and attacks.
""",
            "points": [
                "Protects information",
                "Prevents unauthorized access",
                "Uses authentication and encryption"
            ],
            "example": """import hashlib

data = b"demo"
print(hashlib.sha256(data).hexdigest())"""
        },

        "What is a Database?": {
            "title": "What is a Database?",
            "content": """
A database is an organized collection of information
that can be stored, managed and retrieved efficiently.
""",
            "points": [
                "Stores structured information",
                "Allows searching",
                "Allows updating",
                "Used by applications"
            ],
            "example": """CREATE TABLE students (
    id INT,
    name VARCHAR(50)
);"""
        }
    }

    if chapter in lessons:
        return lessons[chapter]

    # -----------------------------------------------------
    # Course-specific examples
    # -----------------------------------------------------

    examples = {

        "Python": """numbers = [1, 2, 3, 4, 5]

for number in numbers:
    print(number)""",

        "C Language": """#include <stdio.h>

int main() {
    int a = 10;
    printf("%d", a);
    return 0;
}""",

        "C++": """#include <iostream>
using namespace std;

int main() {
    int a = 10;
    cout << a;
    return 0;
}""",

        "Java": """public class Main {
    public static void main(String[] args) {
        int age = 18;
        System.out.println(age);
    }
}""",

        "JavaScript": """let message = "Hello World";
console.log(message);""",

        "HTML": """<!DOCTYPE html>
<html>
<body>
    <h1>Hello World</h1>
</body>
</html>""",

        "CSS": """body {
    margin: 0;
    padding: 20px;
}""",

        "SQL": """SELECT *
FROM students;""",

        "Git and GitHub": """git init
git add .
git commit -m "Initial commit"
git push""",

        "MS Excel": """=SUM(A1:A5)""",

        "Computer Networks": """ip_address = "192.168.1.10"
print(ip_address)""",

        "Data Structures": """numbers = [10, 20, 30]
numbers.append(40)
print(numbers)"""
    }

    example = examples.get(
        course_name,
        """name = "CodeQuest AI"
print(name)"""
    )

    return {
        "title": chapter,
        "content": f"""
{chapter} is an important topic in {course_name}.

Understanding this concept will help you build a strong
foundation and apply programming knowledge to real-world
problems.
""",
        "points": [
            f"Understand the basics of {chapter}",
            "Learn the important concepts",
            "Practice with examples",
            "Apply the concept to problems"
        ],
        "example": example
    }


# =========================================================
# QUIZ DATABASE
# =========================================================

quiz_questions = [

    {
        "id": "q001",
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Computer Personal Unit",
            "Central Program Utility",
            "Computer Processing Utility"
        ],
        "answer": 0,
        "explanation": "CPU stands for Central Processing Unit."
    },

    {
        "id": "q002",
        "question": "Which language is known for its simple syntax?",
        "options": [
            "Python",
            "Machine Code",
            "Assembly",
            "Binary"
        ],
        "answer": 0,
        "explanation": "Python is known for its readable and simple syntax."
    },

    {
        "id": "q003",
        "question": "Which symbol is commonly used for comments in Python?",
        "options": [
            "#",
            "//",
            "/*",
            "<!--"
        ],
        "answer": 0,
        "explanation": "Python uses # for single-line comments."
    },

    {
        "id": "q004",
        "question": "HTML is mainly used for?",
        "options": [
            "Webpage structure",
            "Database management",
            "Operating systems",
            "Network routing"
        ],
        "answer": 0,
        "explanation": "HTML defines the structure of web pages."
    },

    {
        "id": "q005",
        "question": "Which language is used to style HTML pages?",
        "options": [
            "CSS",
            "SQL",
            "C",
            "Python"
        ],
        "answer": 0,
        "explanation": "CSS controls the visual appearance of HTML."
    },

    {
        "id": "q006",
        "question": "Which data structure follows LIFO?",
        "options": [
            "Stack",
            "Queue",
            "Array",
            "Tree"
        ],
        "answer": 0,
        "explanation": "A stack follows Last In, First Out."
    },

    {
        "id": "q007",
        "question": "Which data structure follows FIFO?",
        "options": [
            "Queue",
            "Stack",
            "Tree",
            "Graph"
        ],
        "answer": 0,
        "explanation": "A queue follows First In, First Out."
    },

    {
        "id": "q008",
        "question": "Which SQL command is used to retrieve data?",
        "options": [
            "SELECT",
            "DELETE",
            "DROP",
            "REMOVE"
        ],
        "answer": 0,
        "explanation": "SELECT retrieves data from a database."
    },

    {
        "id": "q009",
        "question": "What is an algorithm?",
        "options": [
            "Step-by-step solution",
            "Computer hardware",
            "Programming language",
            "Database"
        ],
        "answer": 0,
        "explanation": "An algorithm is a step-by-step procedure for solving a problem."
    },

    {
        "id": "q010",
        "question": "Which keyword creates a class in Python?",
        "options": [
            "class",
            "object",
            "define",
            "struct"
        ],
        "answer": 0,
        "explanation": "The class keyword defines a class in Python."
    },

    {
        "id": "q011",
        "question": "Which protocol is commonly used for secure websites?",
        "options": [
            "HTTPS",
            "FTP",
            "HTTP",
            "SMTP"
        ],
        "answer": 0,
        "explanation": "HTTPS encrypts communication between browser and server."
    },

    {
        "id": "q012",
        "question": "What does OOP stand for?",
        "options": [
            "Object-Oriented Programming",
            "Open Operating Program",
            "Object Operating Process",
            "Online Object Programming"
        ],
        "answer": 0,
        "explanation": "OOP stands for Object-Oriented Programming."
    },

    {
        "id": "q013",
        "question": "Which device connects computers in a local network?",
        "options": [
            "Switch",
            "Keyboard",
            "Monitor",
            "Printer"
        ],
        "answer": 0,
        "explanation": "A network switch connects devices in a LAN."
    },

    {
        "id": "q014",
        "question": "Which technology is used to store user progress in CodeQuest?",
        "options": [
            "Cloud Firestore",
            "HTML",
            "CSS",
            "Gunicorn"
        ],
        "answer": 0,
        "explanation": "Cloud Firestore is used for persistent user progress."
    },

    {
        "id": "q015",
        "question": "Which command creates a Git commit?",
        "options": [
            "git commit",
            "git save",
            "git store",
            "git upload"
        ],
        "answer": 0,
        "explanation": "git commit creates a new commit."
    }
]


# =========================================================
# CODE CHALLENGES
# =========================================================

code_challenges = [

    {
        "id": "c001",
        "title": "Hello World",
        "language": "Python",
        "code": """x = 10
y = 20
print(x + y)""",
        "answer": "30"
    },

    {
        "id": "c002",
        "title": "Variable Challenge",
        "language": "Python",
        "code": """name = "Joe"
print("Hello " + name)""",
        "answer": "Hello Joe"
    },

    {
        "id": "c003",
        "title": "Loop Challenge",
        "language": "Python",
        "code": """total = 0

for i in range(1, 4):
    total += i

print(total)""",
        "answer": "6"
    },

    {
        "id": "c004",
        "title": "Condition Challenge",
        "language": "Python",
        "code": """age = 18

if age >= 18:
    print("Adult")
else:
    print("Minor")""",
        "answer": "Adult"
    }
]


# =========================================================
# ERROR FINDER
# =========================================================

error_finder = [

    {
        "id": "e001",
        "title": "Find the Error",
        "code": """print("Hello World")""",
        "answer": "no error"
    },

    {
        "id": "e002",
        "title": "Fix the Variable",
        "code": """name = "Joe"
print(name)""",
        "answer": "no error"
    },

    {
        "id": "e003",
        "title": "Find the Syntax Problem",
        "code": """if 10 > 5
    print("Yes")""",
        "answer": "colon"
    }
]


# =========================================================
# FIREBASE CONFIGURATION
# =========================================================

@app.route("/api/firebase-config")
def firebase_config():

    config = {
        "apiKey": os.environ.get("FIREBASE_API_KEY", ""),
        "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN", ""),
        "projectId": os.environ.get("FIREBASE_PROJECT_ID", ""),
        "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.environ.get(
            "FIREBASE_MESSAGING_SENDER_ID", ""
        ),
        "appId": os.environ.get("FIREBASE_APP_ID", ""),
        "measurementId": os.environ.get(
            "FIREBASE_MEASUREMENT_ID", ""
        )
    }

    required = [
        "apiKey",
        "authDomain",
        "projectId",
        "storageBucket",
        "messagingSenderId",
        "appId"
    ]

    configured = all(config.get(key) for key in required)

    return jsonify({
        "configured": configured,
        "config": config if configured else {}
    })


# =========================================================
# SECURITY HEADERS
# =========================================================

@app.after_request
def security_headers(response):

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"

    response.headers[
        "Referrer-Policy"
    ] = "strict-origin-when-cross-origin"

    response.headers[
        "Permissions-Policy"
    ] = "camera=(), microphone=(), geolocation=()"

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' "
        "https://www.gstatic.com "
        "https://apis.google.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: "
        "https://*.googleusercontent.com "
        "https://lh3.googleusercontent.com; "
        "font-src 'self' data:; "
        "connect-src 'self' "
        "https://*.googleapis.com "
        "https://*.firebaseio.com "
        "https://securetoken.googleapis.com "
        "https://identitytoolkit.googleapis.com "
        "https://firestore.googleapis.com "
        "https://www.googleapis.com; "
        "frame-src 'self' "
        "https://*.firebaseapp.com "
        "https://accounts.google.com; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self';"
    )

    return response


# =========================================================
# MAIN PAGE
# =========================================================

@app.route("/")
def index():
    return render_template(
        "index.html",
        courses=courses
    )


# =========================================================
# STATUS
# =========================================================

@app.route("/api/status")
def api_status():

    return jsonify({
        "status": "online",
        "app": "CodeQuest AI",
        "version": "0.4",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


# =========================================================
# COURSES
# =========================================================

@app.route("/api/courses")
def get_courses():

    return jsonify(courses)


@app.route("/api/course/<course_name>")
def get_course(course_name):

    course = courses.get(course_name)

    if not course:
        return jsonify({
            "error": "Course not found"
        }), 404

    return jsonify({
        "name": course_name,
        **course
    })


@app.route("/api/course/<course_name>/lessons")
def course_lessons(course_name):

    course = courses.get(course_name)

    if not course:
        return jsonify({
            "error": "Course not found"
        }), 404

    lessons = []

    for chapter in course["chapters"]:
        lesson = create_lesson(
            chapter,
            course_name
        )

        lessons.append({
            "chapter": chapter,
            "lesson": lesson
        })

    return jsonify(lessons)


@app.route("/api/lesson/<path:chapter>")
def get_lesson(chapter):

    course_name = request.args.get(
        "course",
        "Programming Fundamentals"
    )

    if course_name not in courses:
        course_name = "Programming Fundamentals"

    return jsonify(
        create_lesson(
            chapter,
            course_name
        )
    )


# =========================================================
# QUIZ
# =========================================================

@app.route("/api/quiz")
def get_quiz():

    questions = []

    for question in quiz_questions:
        questions.append({
            "id": question["id"],
            "question": question["question"],
            "options": question["options"]
        })

    return jsonify({
        "questions": questions
    })


@app.route("/api/quiz/check", methods=["POST"])
def check_quiz():

    data = request.get_json(
        silent=True
    ) or {}

    answers = data.get(
        "answers",
        {}
    )

    correct = 0

    results = []

    for question in quiz_questions:

        selected = answers.get(
            question["id"]
        )

        is_correct = (
            selected is not None
            and int(selected) == question["answer"]
        )

        if is_correct:
            correct += 1

        results.append({
            "id": question["id"],
            "correct": is_correct,
            "answer": question["answer"],
            "explanation": question["explanation"]
        })

    return jsonify({
        "correct": correct,
        "total": len(quiz_questions),
        "score": round(
            correct / len(quiz_questions) * 100
        ),
        "results": results
    })


# =========================================================
# CODE CHALLENGES
# =========================================================

@app.route("/api/code-challenges")
def get_code_challenges():

    public_challenges = []

    for challenge in code_challenges:

        public_challenges.append({
            "id": challenge["id"],
            "title": challenge["title"],
            "language": challenge["language"],
            "code": challenge["code"]
        })

    return jsonify({
        "challenges": public_challenges
    })


@app.route("/api/code-challenges/check", methods=["POST"])
def check_code_challenge():

    data = request.get_json(
        silent=True
    ) or {}

    challenge_id = data.get("id")
    answer = str(
        data.get("answer", "")
    ).strip()

    challenge = next(
        (
            item
            for item in code_challenges
            if item["id"] == challenge_id
        ),
        None
    )

    if not challenge:
        return jsonify({
            "error": "Challenge not found"
        }), 404

    correct = (
        answer.lower()
        == challenge["answer"].lower()
    )

    return jsonify({
        "correct": correct,
        "expected": challenge["answer"]
    })


# =========================================================
# ERROR FINDER
# =========================================================

@app.route("/api/error-finder")
def get_error_finder():

    public_errors = []

    for item in error_finder:

        public_errors.append({
            "id": item["id"],
            "title": item["title"],
            "code": item["code"]
        })

    return jsonify({
        "challenges": public_errors
    })


@app.route("/api/error-finder/check", methods=["POST"])
def check_error_finder():

    data = request.get_json(
        silent=True
    ) or {}

    item_id = data.get("id")

    answer = str(
        data.get("answer", "")
    ).strip().lower()

    item = next(
        (
            x
            for x in error_finder
            if x["id"] == item_id
        ),
        None
    )

    if not item:
        return jsonify({
            "error": "Question not found"
        }), 404

    correct = (
        answer == item["answer"].lower()
        or (
            item["answer"].lower() == "colon"
            and "colon" in answer
        )
    )

    return jsonify({
        "correct": correct,
        "expected": item["answer"]
    })


# =========================================================
# CAREER GUIDE
# =========================================================

@app.route("/api/career", methods=["POST"])
def career_guide():

    data = request.get_json(
        silent=True
    ) or {}

    question = str(
        data.get("question", "")
    ).strip().lower()

    if not question:
        return jsonify({
            "answer": "Ask me a career question and I'll help you."
        })

    if "python" in question:
        answer = (
            "Python is useful for software development, "
            "automation, data science, AI and backend development. "
            "Start with syntax, functions, data structures and projects."
        )

    elif "web" in question:
        answer = (
            "For web development, learn HTML, CSS and JavaScript "
            "first. Then explore a backend technology and databases."
        )

    elif "cyber" in question:
        answer = (
            "For cybersecurity, build strong networking and "
            "Linux fundamentals first, then learn authentication, "
            "encryption, vulnerabilities and defensive security."
        )

    elif "data" in question:
        answer = (
            "For data-related careers, learn Python, SQL, "
            "statistics and data structures. Then build projects "
            "using real datasets."
        )

    elif "job" in question:
        answer = (
            "Build a portfolio with practical projects, keep your "
            "GitHub updated, practice programming problems and "
            "prepare a clear resume."
        )

    else:
        answer = (
            "A good IT learning path is: programming fundamentals → "
            "data structures → databases → web/software development → "
            "projects → GitHub → internship/job preparation."
        )

    return jsonify({
        "answer": answer
    })


# =========================================================
# SECURE TEST SYSTEM
# =========================================================

TEST_DURATION = 10 * 60
TEST_SIZE = 10


def test_active():
    return (
        "test" in session
        and session["test"].get("active") is True
    )


@app.route("/api/test/start", methods=["POST"])
def test_start():

    selected = random.sample(
        quiz_questions,
        min(
            TEST_SIZE,
            len(quiz_questions)
        )
    )

    session["test"] = {
        "active": True,
        "started_at": time.time(),
        "questions": [
            question["id"]
            for question in selected
        ],
        "answers": {},
        "violations": 0
    }

    return jsonify({
        "started": True,
        "duration": TEST_DURATION,
        "questions": [
            {
                "id": question["id"],
                "question": question["question"],
                "options": question["options"]
            }
            for question in selected
        ]
    })


@app.route("/api/test/answer", methods=["POST"])
def test_answer():

    if not test_active():
        return jsonify({
            "error": "No active test"
        }), 400

    data = request.get_json(
        silent=True
    ) or {}

    question_id = data.get("id")
    answer = data.get("answer")

    test = session["test"]

    if question_id not in test["questions"]:
        return jsonify({
            "error": "Invalid question"
        }), 400

    test["answers"][question_id] = answer

    session["test"] = test

    return jsonify({
        "saved": True
    })


@app.route("/api/test/violation", methods=["POST"])
def test_violation():

    if not test_active():
        return jsonify({
            "error": "No active test"
        }), 400

    test = session["test"]

    test["violations"] += 1

    session["test"] = test

    return jsonify({
        "violations": test["violations"]
    })


@app.route("/api/test/status")
def test_status():

    if not test_active():
        return jsonify({
            "active": False
        })

    test = session["test"]

    elapsed = int(
        time.time()
        - test["started_at"]
    )

    remaining = max(
        0,
        TEST_DURATION - elapsed
    )

    return jsonify({
        "active": True,
        "remaining": remaining,
        "violations": test["violations"]
    })


@app.route("/api/test/finish", methods=["POST"])
def test_finish():

    if not test_active():
        return jsonify({
            "error": "No active test"
        }), 400

    test = session["test"]

    correct = 0
    total = len(test["questions"])

    for question in quiz_questions:

        if question["id"] not in test["questions"]:
            continue

        selected = test["answers"].get(
            question["id"]
        )

        if (
            selected is not None
            and int(selected) == question["answer"]
        ):
            correct += 1

    score = round(
        correct / total * 100
    ) if total else 0

    violations = test["violations"]

    session.pop("test", None)

    return jsonify({
        "finished": True,
        "correct": correct,
        "total": total,
        "score": score,
        "violations": violations
    })


# =========================================================
# PROGRESS
# =========================================================

@app.route("/api/progress")
def progress():

    return jsonify({
        "server_storage": "Firebase Firestore",
        "message": (
            "Progress is stored client-side through "
            "Firebase Firestore after Google login."
        )
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Resource not found"
    }), 404


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "error": "Internal server error"
    }), 500


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
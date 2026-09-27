from flask import Flask, render_template, jsonify, request, session
import secrets
import time
import random

app = Flask(__name__)

# =========================================================
# CODEQUEST AI V0.4 — SECURITY EDITION
# =========================================================

# IMPORTANT:
# A normal browser cannot reliably detect whether a student
# specifically opened ChatGPT/Gemini.
#
# This version instead uses:
# • Server-side answer validation
# • Randomized questions
# • Server-side exam sessions
# • Exam timer
# • Tab/window switching detection from the frontend
# • Exam termination after a security violation
#
# For production, use a permanent SECRET_KEY from an
# environment variable and store exam attempts in Redis/DB.
# =========================================================

app.secret_key = secrets.token_hex(32)


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
            "Operating Systems",
            "Files and Folders",
            "Internet Basics",
            "Computer Safety",
            "Cybersecurity Basics",
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
            "Debugging Basics",
            "Introduction to Git",
            "Programming Mini Project"
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
            "Preprocessor",
            "Command Line Arguments",
            "C Mini Projects",
            "Final C Challenge"
        ]
    },

    "C++": {
        "icon": "🟣",
        "level": "Beginner → Master",
        "description": "Learn C++ and object-oriented programming.",
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
            "References",
            "Classes and Objects",
            "Constructors",
            "Destructors",
            "Inheritance",
            "Polymorphism",
            "Encapsulation",
            "Abstraction",
            "Templates",
            "STL Basics",
            "Exception Handling",
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
            "Destructors",
            "Encapsulation",
            "Inheritance",
            "Polymorphism",
            "Abstraction",
            "Method Overloading",
            "Method Overriding",
            "Interfaces",
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
            "Packages",
            "File Handling",
            "Exception Handling",
            "Object-Oriented Python",
            "Virtual Environments",
            "Libraries",
            "APIs",
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
            "Generics",
            "File Handling",
            "Java Projects",
            "Final Java Challenge"
        ]
    },

    "Web Development": {
        "icon": "🌐",
        "level": "Beginner → Advanced",
        "description": "Build modern websites from HTML to backend APIs.",
        "chapters": [
            "How the Web Works",
            "HTML Basics",
            "Semantic HTML",
            "Forms",
            "CSS Basics",
            "Flexbox",
            "Grid",
            "Responsive Design",
            "JavaScript Basics",
            "DOM",
            "Events",
            "Fetch API",
            "JSON",
            "Flask Basics",
            "REST APIs",
            "Authentication Basics",
            "Web Security Basics",
            "Web Project"
        ]
    },

    "Cybersecurity Fundamentals": {
        "icon": "🛡️",
        "level": "Beginner → Intermediate",
        "description": "Learn defensive cybersecurity and safe security practices.",
        "chapters": [
            "What is Cybersecurity?",
            "CIA Triad",
            "Threats and Vulnerabilities",
            "Authentication",
            "Passwords and Hashing",
            "MFA",
            "Phishing Awareness",
            "Social Engineering",
            "Network Basics",
            "Firewalls",
            "HTTPS and TLS",
            "Secure Coding",
            "Input Validation",
            "XSS Basics",
            "SQL Injection Concepts",
            "Access Control",
            "Logging and Monitoring",
            "Incident Response",
            "Ethical and Legal Security",
            "Cybersecurity Mini Project"
        ]
    },

    "Git and GitHub": {
        "icon": "🐙",
        "level": "Beginner → Intermediate",
        "description": "Learn version control and publish your projects.",
        "chapters": [
            "What is Git?",
            "Repositories",
            "git init",
            "git add and commit",
            "Branches",
            "Merging",
            "GitHub",
            "Push and Pull",
            "README Files",
            "Issues",
            "Pull Requests",
            "Project Portfolio"
        ]
    }
}


# =========================================================
# LESSON DATABASE
# =========================================================

lessons = {

    "What is a Computer?": {
        "title": "What is a Computer?",
        "explanation":
            "A computer is an electronic device that accepts data, "
            "processes it, stores it and produces useful information.",
        "example":
            "Example: When you type 10 + 20 into a calculator, "
            "the computer processes the values and produces 30.",
        "tip":
            "Remember: Input → Processing → Output → Storage",
        "question":
            "Which part of a computer processes instructions?",
        "options":
            ["Keyboard", "CPU", "Monitor", "Mouse"],
        "answer": 1
    },

    "Hardware and Software": {
        "title": "Hardware and Software",
        "explanation":
            "Hardware refers to physical computer components. "
            "Software refers to programs and instructions.",
        "example":
            "Hardware: keyboard, monitor, CPU. "
            "Software: Windows, Chrome, Python.",
        "tip":
            "Hardware can be touched. Software cannot be physically touched.",
        "question":
            "Which of these is software?",
        "options":
            ["Keyboard", "RAM", "Windows", "Monitor"],
        "answer": 2
    },

    "What is Programming?": {
        "title": "What is Programming?",
        "explanation":
            "Programming is the process of writing instructions "
            "that tell a computer how to perform a task.",
        "example":
            "Python, C, C++ and Java are programming languages "
            "used to create programs.",
        "tip":
            "Think of a program as instructions given to a computer.",
        "question":
            "What is programming?",
        "options": [
            "Repairing a monitor",
            "Writing instructions for a computer",
            "Typing documents",
            "Browsing websites"
        ],
        "answer": 1
    },

    "Algorithms": {
        "title": "Algorithms",
        "explanation":
            "An algorithm is a step-by-step procedure used "
            "to solve a problem or complete a task.",
        "example":
            "To make tea: boil water → add tea → add milk → "
            "add sugar → serve.",
        "tip":
            "Algorithm = step-by-step solution.",
        "question":
            "What does an algorithm provide?",
        "options": [
            "A step-by-step solution",
            "Computer hardware",
            "Internet connection",
            "A programming language"
        ],
        "answer": 0
    },

    "Variables": {
        "title": "Variables",
        "explanation":
            "A variable is a named storage location used "
            "by a program to store a value.",
        "example":
            "In Python: age = 18. Here, age is a variable containing 18.",
        "tip":
            "Variable = name + stored value.",
        "question":
            "What is a variable used for?",
        "options": [
            "Storing data",
            "Displaying a monitor",
            "Connecting Wi-Fi",
            "Printing paper"
        ],
        "answer": 0
    },

    "Introduction to C": {
        "title": "Introduction to C",
        "explanation":
            "C is a general-purpose programming language developed "
            "by Dennis Ritchie. It is widely used for system programming "
            "and learning programming fundamentals.",
        "example": """#include <stdio.h>

int main() {
    printf("Hello World");
    return 0;
}""",
        "tip":
            "C programs commonly use main() as the starting point.",
        "question":
            "Who developed the C programming language?",
        "options": [
            "James Gosling",
            "Dennis Ritchie",
            "Guido van Rossum",
            "Bjarne Stroustrup"
        ],
        "answer": 1
    },

    "Structure of a C Program": {
        "title": "Structure of a C Program",
        "explanation":
            "A basic C program normally contains header files, "
            "the main() function, statements and a return statement.",
        "example": """#include <stdio.h>

int main() {
    printf("Hello");
    return 0;
}""",
        "tip":
            "Execution normally begins from main().",
        "question":
            "Where does execution normally begin in a C program?",
        "options": [
            "printf()",
            "main()",
            "include()",
            "return()"
        ],
        "answer": 1
    },

    "Variables and Data Types": {
        "title": "Variables and Data Types",
        "explanation":
            "C provides different data types such as int, float, "
            "char and double to store different kinds of values.",
        "example": """int age = 18;
float mark = 85.5;
char grade = 'A';""",
        "tip":
            "Choose a data type according to the kind of value "
            "you want to store.",
        "question":
            "Which data type stores an integer in C?",
        "options": [
            "float",
            "char",
            "int",
            "string"
        ],
        "answer": 2
    },

    "Introduction to Python": {
        "title": "Introduction to Python",
        "explanation":
            "Python is a high-level programming language known "
            "for its readable syntax and wide range of applications.",
        "example": """name = "Joe"
print(name)""",
        "tip":
            "Python programs can often be written with fewer lines of code.",
        "question":
            "Which language is known for readable and simple syntax?",
        "options": [
            "Machine Code",
            "Python",
            "Assembly",
            "Binary"
        ],
        "answer": 1
    },

    "Python Syntax": {
        "title": "Python Syntax",
        "explanation":
            "Python syntax defines how Python code must be written. "
            "Indentation is important because it defines blocks of code.",
        "example": """age = 18

if age >= 18:
    print("Adult")""",
        "tip":
            "Python uses indentation to organize blocks of code.",
        "question":
            "What is especially important for Python code blocks?",
        "options": [
            "Indentation",
            "Semicolon",
            "Brackets only",
            "Colon only"
        ],
        "answer": 0
    },

    "Introduction to C++": {
        "title": "Introduction to C++",
        "explanation":
            "C++ is a general-purpose programming language that "
            "supports procedural and object-oriented programming.",
        "example": """#include <iostream>
using namespace std;

int main() {
    cout << "Hello";
    return 0;
}""",
        "tip":
            "C++ extends many concepts of the C language.",
        "question":
            "Which language is C++ closely related to?",
        "options": [
            "C",
            "HTML",
            "SQL",
            "CSS"
        ],
        "answer": 0
    }
}


# =========================================================
# FALLBACK LESSON GENERATOR
# =========================================================

def create_fallback_lesson(chapter):

    return {
        "title": chapter,

        "explanation":
            f"This lesson introduces the important concepts of "
            f"{chapter}. Study the topic, understand the key terms "
            f"and practice what you learn.",

        "example":
            f"Practice {chapter} by writing notes, creating a "
            f"small example or solving a related problem.",

        "tip":
            "Understand the concept first, then practice it "
            "before moving to the next chapter.",

        "question":
            f"Which statement best describes {chapter}?",

        "options": [
            "It is an important computer/IT concept",
            "It is only a computer game",
            "It is a type of hardware cable",
            "None of these"
        ],

        "answer": 0
    }


# =========================================================
# QUIZ BANK
# =========================================================
# IMPORTANT:
# Correct answers stay on the Flask server.
# They are NEVER included in the question sent to browser.
# =========================================================

quiz_questions = [

    {
        "question":
            "Which language is known for simplicity and readability?",

        "options": [
            "C",
            "Python",
            "Assembly",
            "Machine Code"
        ],

        "answer": 1,

        "explanation":
            "Python is designed with readable syntax."
    },

    {
        "question":
            "Which symbol commonly ends a C statement?",

        "options": [
            ".",
            ",",
            ";",
            ":"
        ],

        "answer": 2,

        "explanation":
            "C statements normally end with a semicolon."
    },

    {
        "question":
            "Which component is commonly called the brain of a computer?",

        "options": [
            "RAM",
            "CPU",
            "Keyboard",
            "Monitor"
        ],

        "answer": 1,

        "explanation":
            "The CPU processes instructions."
    },

    {
        "question":
            "Which Excel function commonly calculates a total?",

        "options": [
            "TOTAL()",
            "SUM()",
            "ADD()",
            "PLUS()"
        ],

        "answer": 1,

        "explanation":
            "SUM() adds numbers in Excel."
    },

    {
        "question":
            "Which OOP concept allows one class to acquire "
            "properties of another?",

        "options": [
            "Encapsulation",
            "Inheritance",
            "Abstraction",
            "Compilation"
        ],

        "answer": 1,

        "explanation":
            "Inheritance derives a class from another class."
    },

    {
        "question":
            "What does HTML mainly describe?",

        "options": [
            "Database queries",
            "Web page structure",
            "Computer hardware",
            "Operating systems"
        ],

        "answer": 1,

        "explanation":
            "HTML defines web page structure."
    },

    {
        "question":
            "What does MFA add to authentication?",

        "options": [
            "More than one verification factor",
            "A faster CPU",
            "A larger monitor",
            "A new programming language"
        ],

        "answer": 0,

        "explanation":
            "MFA uses multiple authentication factors."
    },

    {
        "question":
            "Which protocol is commonly used to securely browse websites?",

        "options": [
            "HTTP",
            "HTTPS",
            "FTP",
            "SMTP"
        ],

        "answer": 1,

        "explanation":
            "HTTPS protects web traffic using TLS."
    },

    {
        "question":
            "Which Git command creates a new local repository?",

        "options": [
            "git init",
            "git start",
            "git make",
            "git repo"
        ],

        "answer": 0,

        "explanation":
            "git init initializes a repository."
    },

    {
        "question":
            "What is an algorithm?",

        "options": [
            "A step-by-step solution",
            "A monitor",
            "A database cable",
            "A compiler brand"
        ],

        "answer": 0,

        "explanation":
            "An algorithm is a step-by-step procedure for solving a problem."
    },

    {
        "question":
            "Which Python collection stores key-value pairs?",

        "options": [
            "List",
            "Tuple",
            "Dictionary",
            "String"
        ],

        "answer": 2,

        "explanation":
            "Python dictionaries store key-value pairs."
    },

    {
        "question":
            "What does SQL injection target?",

        "options": [
            "Database queries",
            "Monitor pixels",
            "Keyboard drivers",
            "Power supply"
        ],

        "answer": 0,

        "explanation":
            "SQL injection abuses unsafe database query construction."
    }
]


# =========================================================
# CODE CHALLENGES
# =========================================================

code_challenges = [

    {
        "language": "C",

        "question":
            "What will this program print?",

        "code":
            '#include <stdio.h>\n'
            'int main(){\n'
            '    int a=5,b=3;\n'
            '    printf("%d",a+b);\n'
            '    return 0;\n'
            '}',

        "options": [
            "2",
            "8",
            "15",
            "53"
        ],

        "answer": 1,

        "explanation":
            "5 + 3 = 8."
    },

    {
        "language": "Python",

        "question":
            "What will this program print?",

        "code":
            "a=10\n"
            "b=2\n"
            "print(a*b)",

        "options": [
            "12",
            "20",
            "102",
            "5"
        ],

        "answer": 1,

        "explanation":
            "10 × 2 = 20."
    },

    {
        "language": "C++",

        "question":
            "What will this program print?",

        "code":
            '#include <iostream>\n'
            'using namespace std;\n'
            'int main(){\n'
            '    cout << 10-4;\n'
            '    return 0;\n'
            '}',

        "options": [
            "6",
            "14",
            "104",
            "Error"
        ],

        "answer": 0,

        "explanation":
            "10 - 4 = 6."
    }
]


# =========================================================
# ERROR FINDER
# =========================================================

error_challenges = [

    {
        "language": "C",

        "question":
            "Find the error:",

        "code":
            '#include <stdio.h>\n'
            'int main(){\n'
            '    int age=18\n'
            '    printf("%d",age);\n'
            '    return 0;\n'
            '}',

        "options": [
            "Missing semicolon after 18",
            "printf is wrong",
            "main cannot return 0",
            "No error"
        ],

        "answer": 0,

        "explanation":
            "The declaration needs a semicolon."
    },

    {
        "language": "Python",

        "question":
            "Find the error:",

        "code":
            "age=20\n"
            "if age >= 18\n"
            "    print('Adult')",

        "options": [
            "Missing colon after the condition",
            "age cannot be 20",
            "print is invalid",
            "No error"
        ],

        "answer": 0,

        "explanation":
            "Python requires a colon after an if condition."
    }
]


# =========================================================
# SECURE EXAM SYSTEM
# =========================================================

EXAM_DURATION = 5 * 60

EXAM_LENGTH = 8

attempts = {}


def cleanup_attempts():

    now = time.time()

    expired = []

    for token, attempt in attempts.items():

        if (
            now - attempt["created"]
            > EXAM_DURATION + 120
        ):

            expired.append(token)

    for token in expired:

        attempts.pop(token, None)


def current_attempt():

    cleanup_attempts()

    token = session.get("exam_token")

    if not token:

        return None

    if token not in attempts:

        return None

    return attempts[token]


def public_question(question, index, total):

    # IMPORTANT:
    # answer and explanation are NOT sent here.

    return {

        "id": index,

        "question":
            question["question"],

        "options":
            question["options"],

        "number":
            index + 1,

        "total":
            total
    }


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        courses=courses
    )


# =========================================================
# COURSE API
# =========================================================

@app.route("/api/courses")
def get_courses():

    return jsonify(courses)


@app.route("/api/course/<course_name>")
def get_course(course_name):

    if course_name not in courses:

        return jsonify({
            "error": "Course not found"
        }), 404

    return jsonify(
        courses[course_name]
    )


# =========================================================
# LESSON API
# =========================================================

@app.route("/api/lesson/<path:chapter>")
def get_lesson(chapter):

    lesson = lessons.get(chapter)

    if lesson:

        return jsonify(lesson)

    # Instead of failing for expanded syllabus chapters,
    # provide a safe fallback lesson.

    return jsonify(
        create_fallback_lesson(chapter)
    )


# =========================================================
# START SECURE EXAM
# =========================================================

@app.post("/api/exam/start")
def exam_start():

    cleanup_attempts()

    # Prevent multiple simultaneous attempts
    if current_attempt():

        return jsonify({
            "error":
                "An exam is already active. "
                "Finish it or wait until it expires."
        }), 409

    # Randomly choose questions
    questions = random.sample(
        quiz_questions,
        min(
            EXAM_LENGTH,
            len(quiz_questions)
        )
    )

    # Create unpredictable server-side token
    token = secrets.token_urlsafe(32)

    attempts[token] = {

        "created":
            time.time(),

        "questions":
            questions,

        "current":
            0,

        "score":
            0,

        "violations":
            0,

        "finished":
            False
    }

    session["exam_token"] = token

    return jsonify({

        "duration":
            EXAM_DURATION,

        "total":
            len(questions),

        "question":
            public_question(
                questions[0],
                0,
                len(questions)
            )
    })


# =========================================================
# SUBMIT EXAM ANSWER
# =========================================================

@app.post("/api/exam/answer")
def exam_answer():

    attempt = current_attempt()

    if not attempt:

        return jsonify({
            "error": "No active exam."
        }), 400

    if attempt["finished"]:

        return jsonify({
            "error": "Exam already finished."
        }), 400

    # Server-side timer
    if (
        time.time() -
        attempt["created"]
        > EXAM_DURATION
    ):

        attempt["finished"] = True

        return jsonify({

            "finished": True,

            "reason":
                "time_expired",

            "score":
                attempt["score"],

            "total":
                len(attempt["questions"])
        })


    data = request.get_json(
        silent=True
    ) or {}


    try:

        question_id = int(
            data.get("question_id")
        )

        selected = int(
            data.get("answer")
        )

    except (
        TypeError,
        ValueError
    ):

        return jsonify({
            "error": "Invalid answer."
        }), 400


    # Prevent answering an old/future question
    if (
        question_id !=
        attempt["current"]
    ):

        return jsonify({
            "error":
                "Invalid question sequence."
        }), 409


    question = attempt[
        "questions"
    ][attempt["current"]]


    correct = (
        selected ==
        question["answer"]
    )


    if correct:

        attempt["score"] += 1


    attempt["current"] += 1


    # Exam finished
    if (
        attempt["current"]
        >= len(attempt["questions"])
    ):

        attempt["finished"] = True

        return jsonify({

            "finished":
                True,

            "correct":
                correct,

            "score":
                attempt["score"],

            "total":
                len(attempt["questions"])
        })


    # Return next question
    return jsonify({

        "finished":
            False,

        "correct":
            correct,

        "question":
            public_question(
                attempt["questions"][
                    attempt["current"]
                ],

                attempt["current"],

                len(
                    attempt["questions"]
                )
            )
    })


# =========================================================
# SECURITY VIOLATION
# =========================================================

@app.post("/api/exam/violation")
def exam_violation():

    attempt = current_attempt()

    if not attempt:

        return jsonify({
            "ok": False
        }), 400

    if attempt["finished"]:

        return jsonify({
            "ok": False
        })


    attempt["violations"] += 1

    attempt["finished"] = True


    return jsonify({

        "ok":
            True,

        "finished":
            True,

        "reason":
            "security_violation",

        "message":
            "Exam terminated because the exam page was left."
    })


# =========================================================
# MANUAL FINISH
# =========================================================

@app.post("/api/exam/finish")
def exam_finish():

    attempt = current_attempt()

    if not attempt:

        return jsonify({
            "error": "No active exam."
        }), 400


    attempt["finished"] = True


    return jsonify({

        "finished":
            True,

        "score":
            attempt["score"],

        "total":
            len(
                attempt["questions"]
            )
    })


# =========================================================
# EXAM STATUS
# =========================================================

@app.get("/api/exam/status")
def exam_status():

    attempt = current_attempt()

    if not attempt:

        return jsonify({
            "active": False
        })


    remaining = max(
        0,
        EXAM_DURATION -
        int(
            time.time() -
            attempt["created"]
        )
    )


    return jsonify({

        "active":
            not attempt["finished"],

        "score":
            attempt["score"],

        "current":
            attempt["current"],

        "total":
            len(
                attempt["questions"]
            ),

        "remaining":
            remaining
    })


# =========================================================
# CODE CHALLENGES
# =========================================================

@app.route("/api/code-challenges")
def get_code_challenges():

    return jsonify(
        code_challenges
    )


# =========================================================
# ERROR FINDER
# =========================================================

@app.route("/api/error-finder")
def get_error_challenges():

    return jsonify(
        error_challenges
    )


# =========================================================
# STATUS
# =========================================================

@app.route("/api/status")
def status():

    return jsonify({

        "app":
            "CodeQuest AI",

        "version":
            "0.4",

        "status":
            "online",

        "features": [

            "Learning",

            "Interactive Lessons",

            "Secure Quiz Arena",

            "Server-side Answer Validation",

            "Randomized Exam Questions",

            "Exam Timer",

            "Security Violation Detection",

            "Code Challenges",

            "Error Finder",

            "Progress Tracking",

            "Cybersecurity Fundamentals"

        ],

        "security_note":
            "Quiz answers are validated on the server "
            "and are not sent to the browser."
    })


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
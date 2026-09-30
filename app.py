from flask import Flask, render_template, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, date, timedelta
import sqlite3
import os
import json
import random
import uuid
import urllib.request
import urllib.error

# ============================================================
# CODEQUEST AI
# LEARN • PRACTICE • PLAY • BUILD
# Production-style Flask backend
# ============================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key-in-render"
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

if os.environ.get("COOKIE_SECURE", "false").lower() == "true":
    app.config["SESSION_COOKIE_SECURE"] = True


# ============================================================
# DATABASE
# ============================================================

# For Render:
# Set DATABASE_PATH to a location on your persistent disk.
#
# Example:
# DATABASE_PATH=/var/data/codequest.db
#
# Local development:
# codequest.db

DATABASE_PATH = os.environ.get(
    "DATABASE_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "codequest.db")
)


def get_db():
    db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            firebase_uid TEXT UNIQUE,
            created_at TEXT NOT NULL,
            last_login TEXT
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            user_id INTEGER PRIMARY KEY,
            xp INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            last_active TEXT,
            completed_lessons TEXT DEFAULT '[]',
            achievements TEXT DEFAULT '[]',
            quizzes_completed INTEGER DEFAULT 0,
            quizzes_passed INTEGER DEFAULT 0,
            best_quiz_score INTEGER DEFAULT 0,
            malpractice_events INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            total INTEGER,
            xp_earned INTEGER,
            terminated INTEGER DEFAULT 0,
            reason TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            event_type TEXT,
            details TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    db.commit()
    db.close()


# ============================================================
# COURSE CONTENT
# ============================================================

def chapter(title, lesson, sample, difficulty="Beginner"):
    return {
        "title": title,
        "lesson": lesson,
        "sample": sample,
        "difficulty": difficulty
    }


courses = [

    {
        "id": "computer-basics",
        "title": "Computer Basics",
        "icon": "💻",
        "level": "Beginner",
        "description": "Understand computers from absolute zero.",
        "chapters": [

            chapter(
                "What is a Computer?",
                "A computer is an electronic machine that accepts input, processes data, stores information and produces output.",
                """#include <stdio.h>

int main() {
    printf("Hello, CodeQuest AI!");
    return 0;
}"""
            ),

            chapter(
                "Hardware and Software",
                "Hardware is the physical part of a computer. Software is a set of instructions that tells hardware what to do.",
                """#include <stdio.h>

int main() {
    printf("Hardware: Keyboard, CPU, RAM");
    printf("\\nSoftware: Windows, Python, Chrome");
    return 0;
}"""
            ),

            chapter(
                "CPU",
                "The CPU executes instructions and performs calculations. It is commonly called the brain of the computer.",
                """#include <stdio.h>

int main() {
    int a = 10;
    int b = 20;

    printf("Result = %d", a + b);

    return 0;
}"""
            ),

            chapter(
                "RAM and Storage",
                "RAM temporarily stores data being actively used. Storage such as SSD keeps data for long-term use.",
                """#include <stdio.h>

int main() {
    int numbers[3] = {10, 20, 30};

    printf("%d", numbers[1]);

    return 0;
}"""
            ),

            chapter(
                "Operating System Basics",
                "An operating system manages hardware and provides an environment for applications.",
                """#include <stdio.h>

int main() {
    printf("Operating systems manage computer resources.");
    return 0;
}"""
            )
        ]
    },


    {
        "id": "ms-office",
        "title": "MS Office & Productivity",
        "icon": "📊",
        "level": "Beginner",
        "description": "Learn practical Word, Excel and PowerPoint skills.",
        "chapters": [

            chapter(
                "MS Word Basics",
                "Learn documents, formatting, headings, tables and professional document creation.",
                """# Simple productivity example

name = "CodeQuest AI"
print("Project:", name)
"""
            ),

            chapter(
                "Excel Basics",
                "Excel is useful for calculations, tables, data analysis and charts.",
                """marks = [80, 75, 90, 85]

average = sum(marks) / len(marks)

print("Average:", average)
"""
            ),

            chapter(
                "Excel Formulas",
                "Formulas allow spreadsheets to automatically calculate values.",
                """marks = [80, 75, 90]

total = sum(marks)
average = total / len(marks)

print("Total:", total)
print("Average:", average)
"""
            ),

            chapter(
                "PowerPoint",
                "PowerPoint is used to create presentations using slides, text, images, diagrams and charts.",
                """topics = [
    "Introduction",
    "Problem",
    "Solution",
    "Conclusion"
]

for topic in topics:
    print("Slide:", topic)
"""
            )
        ]
    },


    {
        "id": "git-github",
        "title": "Git & GitHub",
        "icon": "🐙",
        "level": "Beginner",
        "description": "Learn version control and real project workflow.",
        "chapters": [

            chapter(
                "What is Git?",
                "Git is a version control system used to track changes in source code.",
                """git init
git status
git add .
git commit -m "Initial commit"
"""
            ),

            chapter(
                "What is GitHub?",
                "GitHub is a platform where developers store, collaborate on and share software projects.",
                """git remote add origin YOUR_REPOSITORY_URL
git branch -M main
git push -u origin main
"""
            ),

            chapter(
                "Branches",
                "Branches allow developers to work on features without directly changing the main branch.",
                """git checkout -b feature-login

git add .
git commit -m "Add login feature"
"""
            ),

            chapter(
                "Pull Requests",
                "Pull requests allow developers to propose and review changes before merging them.",
                """# Typical workflow

git checkout -b feature
git add .
git commit -m "Add feature"
git push origin feature
"""
            )
        ]
    },


    {
        "id": "c-programming",
        "title": "C Programming",
        "icon": "⚙️",
        "level": "Beginner",
        "description": "Build strong programming fundamentals with C.",
        "chapters": [

            chapter(
                "C Hello World",
                "Every C program starts with a main function. printf() displays output.",
                """#include <stdio.h>

int main() {
    printf("Hello World");
    return 0;
}"""
            ),

            chapter(
                "Variables",
                "Variables store values that a program can use and modify.",
                """#include <stdio.h>

int main() {
    int age = 18;
    float height = 5.8;

    printf("%d\\n", age);
    printf("%.1f", height);

    return 0;
}"""
            ),

            chapter(
                "Input and Output",
                "scanf() can receive input from the user while printf() displays output.",
                """#include <stdio.h>

int main() {
    int age;

    printf("Enter age: ");
    scanf("%d", &age);

    printf("Age = %d", age);

    return 0;
}"""
            ),

            chapter(
                "If Else",
                "Conditional statements allow programs to make decisions.",
                """#include <stdio.h>

int main() {
    int mark = 75;

    if (mark >= 50) {
        printf("Pass");
    } else {
        printf("Fail");
    }

    return 0;
}"""
            ),

            chapter(
                "Loops",
                "Loops repeat a block of code multiple times.",
                """#include <stdio.h>

int main() {
    for (int i = 1; i <= 5; i++) {
        printf("%d\\n", i);
    }

    return 0;
}"""
            ),

            chapter(
                "Functions",
                "Functions divide a program into reusable blocks.",
                """#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    printf("%d", add(10, 20));
    return 0;
}"""
            ),

            chapter(
                "Arrays",
                "Arrays store multiple values of the same type.",
                """#include <stdio.h>

int main() {
    int marks[] = {80, 75, 90};

    for (int i = 0; i < 3; i++) {
        printf("%d\\n", marks[i]);
    }

    return 0;
}"""
            ),

            chapter(
                "Pointers",
                "Pointers store memory addresses and are an important part of C.",
                """#include <stdio.h>

int main() {
    int value = 50;
    int *ptr = &value;

    printf("Value = %d\\n", value);
    printf("Pointer value = %d", *ptr);

    return 0;
}"""
            )
        ]
    },


    {
        "id": "cpp",
        "title": "C++ Programming",
        "icon": "🚀",
        "level": "Beginner",
        "description": "Move from C fundamentals into modern C++.",
        "chapters": [

            chapter(
                "C++ Basics",
                "C++ supports procedural, object-oriented and generic programming.",
                """#include <iostream>
using namespace std;

int main() {
    cout << "Hello C++";
    return 0;
}"""
            ),

            chapter(
                "Classes and Objects",
                "Classes define objects and their properties and behaviours.",
                """#include <iostream>
using namespace std;

class Student {
public:
    string name;

    void show() {
        cout << "Student: " << name;
    }
};

int main() {
    Student s;
    s.name = "Joe";
    s.show();

    return 0;
}"""
            ),

            chapter(
                "Inheritance",
                "Inheritance allows one class to reuse properties and behaviour from another class.",
                """#include <iostream>
using namespace std;

class Animal {
public:
    void eat() {
        cout << "Eating";
    }
};

class Dog : public Animal {
};

int main() {
    Dog d;
    d.eat();

    return 0;
}"""
            )
        ]
    },


    {
        "id": "python",
        "title": "Python Programming",
        "icon": "🐍",
        "level": "Beginner",
        "description": "Learn Python from basics to practical programming.",
        "chapters": [

            chapter(
                "Python Basics",
                "Python is a high-level programming language known for readable syntax.",
                """print("Hello CodeQuest AI")"""
            ),

            chapter(
                "Variables and Data Types",
                "Python variables can store numbers, strings, lists and many other values.",
                """name = "CodeQuest"
age = 18
score = 95.5

print(name)
print(age)
print(score)
"""
            ),

            chapter(
                "Conditions",
                "if, elif and else allow Python programs to make decisions.",
                """mark = 82

if mark >= 50:
    print("Pass")
else:
    print("Fail")
"""
            ),

            chapter(
                "Loops",
                "Loops repeat instructions efficiently.",
                """for i in range(1, 6):
    print(i)
"""
            ),

            chapter(
                "Functions",
                "Functions are reusable blocks of code.",
                """def add(a, b):
    return a + b

result = add(10, 20)
print(result)
"""
            ),

            chapter(
                "Lists and Dictionaries",
                "Lists store ordered collections while dictionaries store key-value pairs.",
                """student = {
    "name": "Joe",
    "department": "IT",
    "year": 1
}

print(student["name"])
"""
            )
        ]
    },


    {
        "id": "web-development",
        "title": "Web Development",
        "icon": "🌐",
        "level": "Beginner",
        "description": "Build websites and understand frontend development.",
        "chapters": [

            chapter(
                "HTML",
                "HTML defines the structure of a web page.",
                """<!DOCTYPE html>
<html>
<body>

<h1>Hello CodeQuest AI</h1>
<p>My first webpage.</p>

</body>
</html>"""
            ),

            chapter(
                "CSS",
                "CSS controls the appearance and layout of webpages.",
                """body {
    background: #111827;
    color: white;
    font-family: Arial;
}

h1 {
    color: #a855f7;
}"""
            ),

            chapter(
                "JavaScript",
                "JavaScript adds logic and interactivity to webpages.",
                """const button = document.querySelector("#btn");

button.addEventListener("click", () => {
    alert("Hello CodeQuest!");
});
"""
            ),

            chapter(
                "DOM",
                "The Document Object Model allows JavaScript to read and modify HTML elements.",
                """document.getElementById("title").textContent =
    "CodeQuest AI";
"""
            ),

            chapter(
                "Fetch API",
                "Fetch allows a webpage to communicate with backend APIs.",
                """fetch("/api/stats")
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
"""
            )
        ]
    },


    {
        "id": "dbms",
        "title": "DBMS & SQL",
        "icon": "🗄️",
        "level": "Beginner",
        "description": "Understand databases and SQL.",
        "chapters": [

            chapter(
                "What is DBMS?",
                "A database management system stores, organizes and retrieves structured information.",
                """CREATE TABLE students (
    id INTEGER,
    name TEXT,
    department TEXT
);"""
            ),

            chapter(
                "SQL SELECT",
                "SELECT retrieves information from database tables.",
                """SELECT *
FROM students;"""
            ),

            chapter(
                "WHERE",
                "WHERE filters rows according to a condition.",
                """SELECT *
FROM students
WHERE department = 'IT';"""
            ),

            chapter(
                "INSERT",
                "INSERT adds new records to a table.",
                """INSERT INTO students
(id, name, department)
VALUES
(1, 'Joe', 'IT');"""
            ),

            chapter(
                "JOIN",
                "JOIN combines related information from multiple tables.",
                """SELECT students.name, courses.course_name
FROM students
JOIN courses
ON students.id = courses.student_id;"""
            )
        ]
    },


    {
        "id": "dsa",
        "title": "Data Structures & Algorithms",
        "icon": "🧠",
        "level": "Intermediate",
        "description": "Develop problem-solving and coding interview skills.",
        "chapters": [

            chapter(
                "Algorithm Basics",
                "An algorithm is a finite sequence of steps used to solve a problem.",
                """def find_largest(numbers):
    largest = numbers[0]

    for number in numbers:
        if number > largest:
            largest = number

    return largest

print(find_largest([10, 25, 7, 30]))
"""
            ),

            chapter(
                "Arrays",
                "Arrays provide indexed access to collections of values.",
                """numbers = [10, 20, 30, 40]

print(numbers[0])
print(numbers[2])
"""
            ),

            chapter(
                "Stack",
                "A stack follows LIFO: Last In, First Out.",
                """stack = []

stack.append("A")
stack.append("B")
stack.append("C")

print(stack.pop())
"""
            ),

            chapter(
                "Queue",
                "A queue generally follows FIFO: First In, First Out.",
                """from collections import deque

queue = deque()

queue.append("A")
queue.append("B")

print(queue.popleft())
"""
            ),

            chapter(
                "Searching",
                "Searching algorithms locate values inside data structures.",
                """numbers = [10, 20, 30, 40]

target = 30

if target in numbers:
    print("Found")
else:
    print("Not found")
"""
            ),

            chapter(
                "Sorting",
                "Sorting arranges data according to a chosen order.",
                """numbers = [5, 2, 8, 1, 3]

numbers.sort()

print(numbers)
"""
            )
        ]
    },


    {
        "id": "operating-systems",
        "title": "Operating Systems",
        "icon": "🖥️",
        "level": "Intermediate",
        "description": "Understand processes, memory and operating system concepts.",
        "chapters": [

            chapter(
                "Processes",
                "A process is a program that is currently being executed.",
                """# Conceptual Python example

import os

print("Current process ID:", os.getpid())
"""
            ),

            chapter(
                "Threads",
                "Threads allow multiple execution paths inside a process.",
                """import threading

def task():
    print("Running task")

thread = threading.Thread(target=task)
thread.start()
thread.join()
"""
            ),

            chapter(
                "Memory Management",
                "Operating systems manage memory allocation and protection.",
                """numbers = [10, 20, 30]

print("Memory-managed collection:", numbers)
"""
            )
        ]
    },


    {
        "id": "computer-networks",
        "title": "Computer Networks",
        "icon": "🌍",
        "level": "Intermediate",
        "description": "Learn networking from basic concepts to practical web communication.",
        "chapters": [

            chapter(
                "Network Basics",
                "A computer network connects devices so they can exchange information.",
                """import socket

print(socket.gethostname())
"""
            ),

            chapter(
                "IP Address",
                "An IP address identifies a device/interface on a network.",
                """import socket

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

print("Host:", hostname)
print("IP:", ip)
"""
            ),

            chapter(
                "HTTP",
                "HTTP is a protocol used for communication between web clients and servers.",
                """from urllib.request import urlopen

response = urlopen("https://example.com")

print(response.status)
"""
            ),

            chapter(
                "Client and Server",
                "Clients request resources or services while servers respond to those requests.",
                """# Client concept

import requests

response = requests.get(
    "https://example.com"
)

print(response.status_code)
"""
            )
        ]
    },


    {
        "id": "cybersecurity",
        "title": "Cybersecurity",
        "icon": "🔐",
        "level": "Intermediate",
        "description": "Learn safe and responsible cybersecurity fundamentals.",
        "chapters": [

            chapter(
                "Cybersecurity Basics",
                "Cybersecurity protects systems, networks and information from unauthorized access and damage.",
                """password = "example"

if len(password) >= 8:
    print("Password length is acceptable")
else:
    print("Use a longer password")
"""
            ),

            chapter(
                "Password Security",
                "Strong passwords should be long, unique and difficult to guess.",
                """import hashlib

password = "example-password"

hashed = hashlib.sha256(
    password.encode()
).hexdigest()

print(hashed)
"""
            ),

            chapter(
                "Phishing Awareness",
                "Phishing attempts to trick users into revealing sensitive information.",
                """message = "Urgent! Click this unknown link!"

if "unknown" in message.lower():
    print("Be careful: verify the source")
"""
            )
        ]
    },


    {
        "id": "ai-ml",
        "title": "AI & Machine Learning",
        "icon": "🤖",
        "level": "Intermediate",
        "description": "Understand artificial intelligence and machine learning concepts.",
        "chapters": [

            chapter(
                "What is AI?",
                "Artificial intelligence refers to computer systems performing tasks that normally require aspects of human intelligence.",
                """print("Input data")
print("AI model")
print("Prediction")
"""
            ),

            chapter(
                "Machine Learning",
                "Machine learning allows systems to learn patterns from data.",
                """data = [10, 20, 30, 40]

average = sum(data) / len(data)

print("Simple learned statistic:", average)
"""
            ),

            chapter(
                "Training Data",
                "Training data is used by a machine learning algorithm to learn patterns.",
                """training_data = [
    {"hours": 2, "score": 50},
    {"hours": 4, "score": 70},
    {"hours": 6, "score": 90}
]

for item in training_data:
    print(item)
"""
            ),

            chapter(
                "AI Projects",
                "Practical projects are one of the best ways to understand AI concepts.",
                """project = {
    "name": "Student Assistant",
    "input": "Question",
    "output": "Answer"
}

print(project)
"""
            )
        ]
    },


    {
        "id": "cloud-devops",
        "title": "Cloud & DevOps",
        "icon": "☁️",
        "level": "Intermediate",
        "description": "Learn deployment, cloud concepts and software delivery.",
        "chapters": [

            chapter(
                "Cloud Computing",
                "Cloud computing provides computing resources over networks instead of requiring everything to run locally.",
                """import os

port = os.environ.get("PORT", "10000")

print("Application port:", port)
"""
            ),

            chapter(
                "Environment Variables",
                "Environment variables allow configuration to remain outside source code.",
                """import os

secret = os.environ.get("SECRET_KEY")

if secret:
    print("Secret configured")
else:
    print("Secret not configured")
"""
            ),

            chapter(
                "Deployment Basics",
                "Deployment makes an application available for real users.",
                """# Typical production command

gunicorn app:app
"""
            )
        ]
    },


    {
        "id": "software-development",
        "title": "Software Development",
        "icon": "🛠️",
        "level": "Intermediate",
        "description": "Understand how real software projects are planned and built.",
        "chapters": [

            chapter(
                "Software Development Life Cycle",
                "The SDLC includes requirements, design, development, testing, deployment and maintenance.",
                """stages = [
    "Requirements",
    "Design",
    "Development",
    "Testing",
    "Deployment"
]

for stage in stages:
    print(stage)
"""
            ),

            chapter(
                "APIs",
                "APIs allow different software systems to communicate.",
                """fetch("/api/courses")
    .then(response => response.json())
    .then(data => console.log(data));
"""
            ),

            chapter(
                "Debugging",
                "Debugging is the process of finding and fixing problems in software.",
                """def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"

    return a / b

print(divide(10, 2))
print(divide(10, 0))
"""
            ),

            chapter(
                "Testing",
                "Testing checks whether software behaves as expected.",
                """def add(a, b):
    return a + b

assert add(2, 3) == 5

print("Test passed")
"""
            )
        ]
    }
]


# ============================================================
# EXTENDED ROADMAP
# ============================================================

roadmap = [
    {
        "id": "fundamentals",
        "title": "Computer Fundamentals",
        "icon": "💻",
        "description": "Computer architecture, hardware, software and operating systems."
    },
    {
        "id": "productivity",
        "title": "Productivity Tools",
        "icon": "📊",
        "description": "Word, Excel, PowerPoint and professional digital skills."
    },
    {
        "id": "git",
        "title": "Git & GitHub",
        "icon": "🐙",
        "description": "Version control, repositories, branches and collaboration."
    },
    {
        "id": "c",
        "title": "C Programming",
        "icon": "⚙️",
        "description": "Programming fundamentals and memory concepts."
    },
    {
        "id": "cpp",
        "title": "C++",
        "icon": "🚀",
        "description": "Object-oriented and modern C++ programming."
    },
    {
        "id": "python",
        "title": "Python",
        "icon": "🐍",
        "description": "Python programming and practical automation."
    },
    {
        "id": "web",
        "title": "Web Development",
        "icon": "🌐",
        "description": "HTML, CSS, JavaScript, DOM and APIs."
    },
    {
        "id": "backend",
        "title": "Backend Development",
        "icon": "🧩",
        "description": "Servers, APIs, authentication and databases."
    },
    {
        "id": "sql",
        "title": "DBMS & SQL",
        "icon": "🗄️",
        "description": "Relational databases and SQL."
    },
    {
        "id": "dsa",
        "title": "DSA",
        "icon": "🧠",
        "description": "Data structures, algorithms and problem solving."
    },
    {
        "id": "oop",
        "title": "Object-Oriented Programming",
        "icon": "🧱",
        "description": "Classes, objects, inheritance and polymorphism."
    },
    {
        "id": "os",
        "title": "Operating Systems",
        "icon": "🖥️",
        "description": "Processes, threads, memory and file systems."
    },
    {
        "id": "networks",
        "title": "Computer Networks",
        "icon": "🌍",
        "description": "Networking, HTTP, TCP/IP and client-server systems."
    },
    {
        "id": "cyber",
        "title": "Cybersecurity",
        "icon": "🔐",
        "description": "Security fundamentals and safe development."
    },
    {
        "id": "cloud",
        "title": "Cloud Computing",
        "icon": "☁️",
        "description": "Deployment and cloud infrastructure fundamentals."
    },
    {
        "id": "devops",
        "title": "DevOps",
        "icon": "♾️",
        "description": "CI/CD, deployment and software delivery."
    },
    {
        "id": "ai",
        "title": "Artificial Intelligence",
        "icon": "🤖",
        "description": "AI concepts, models and practical projects."
    },
    {
        "id": "ml",
        "title": "Machine Learning",
        "icon": "📈",
        "description": "Data, training, evaluation and prediction."
    },
    {
        "id": "testing",
        "title": "Software Testing",
        "icon": "🧪",
        "description": "Unit testing, debugging and quality assurance."
    },
    {
        "id": "career",
        "title": "Career Preparation",
        "icon": "🎯",
        "description": "Resume, GitHub, projects, internships and interviews."
    }
]


# ============================================================
# QUIZ QUESTIONS
# ============================================================

quiz_questions = [

    {
        "id": 1,
        "topic": "Computer Basics",
        "level": "Beginner",
        "question": "What is the main processing unit of a computer?",
        "options": ["CPU", "RAM", "SSD", "Monitor"],
        "answer": "CPU"
    },

    {
        "id": 2,
        "topic": "Computer Basics",
        "level": "Beginner",
        "question": "Which memory is temporary?",
        "options": ["RAM", "SSD", "Hard Disk", "DVD"],
        "answer": "RAM"
    },

    {
        "id": 3,
        "topic": "Programming",
        "level": "Beginner",
        "question": "Which symbol is commonly used to end a C statement?",
        "options": [";", ":", "#", "@"],
        "answer": ";"
    },

    {
        "id": 4,
        "topic": "Python",
        "level": "Beginner",
        "question": "Which function displays output in Python?",
        "options": ["print()", "display()", "show()", "output()"],
        "answer": "print()"
    },

    {
        "id": 5,
        "topic": "Web",
        "level": "Beginner",
        "question": "Which language structures a webpage?",
        "options": ["HTML", "CSS", "SQL", "C"],
        "answer": "HTML"
    },

    {
        "id": 6,
        "topic": "Web",
        "level": "Beginner",
        "question": "Which language styles webpages?",
        "options": ["CSS", "HTML", "C++", "SQL"],
        "answer": "CSS"
    },

    {
        "id": 7,
        "topic": "Web",
        "level": "Beginner",
        "question": "Which language adds interactivity to webpages?",
        "options": ["JavaScript", "HTML", "SQL", "C"],
        "answer": "JavaScript"
    },

    {
        "id": 8,
        "topic": "Git",
        "level": "Beginner",
        "question": "Which command creates a Git repository?",
        "options": ["git init", "git start", "git create", "git new"],
        "answer": "git init"
    },

    {
        "id": 9,
        "topic": "SQL",
        "level": "Beginner",
        "question": "Which SQL command retrieves data?",
        "options": ["SELECT", "GET", "READ", "OPEN"],
        "answer": "SELECT"
    },

    {
        "id": 10,
        "topic": "DSA",
        "level": "Beginner",
        "question": "Which data structure follows LIFO?",
        "options": ["Stack", "Queue", "Array", "Graph"],
        "answer": "Stack"
    },

    {
        "id": 11,
        "topic": "DSA",
        "level": "Beginner",
        "question": "Which data structure normally follows FIFO?",
        "options": ["Queue", "Stack", "Tree", "Heap"],
        "answer": "Queue"
    },

    {
        "id": 12,
        "topic": "AI",
        "level": "Beginner",
        "question": "What does AI stand for?",
        "options": [
            "Artificial Intelligence",
            "Automatic Internet",
            "Advanced Input",
            "Application Interface"
        ],
        "answer": "Artificial Intelligence"
    },

    {
        "id": 13,
        "topic": "AI",
        "level": "Beginner",
        "question": "What does a trained machine-learning model commonly produce?",
        "options": [
            "Predictions",
            "Keyboard",
            "Operating System",
            "Hard Disk"
        ],
        "answer": "Predictions"
    },

    {
        "id": 14,
        "topic": "Cybersecurity",
        "level": "Beginner",
        "question": "What should you do with a suspicious link?",
        "options": [
            "Verify it first",
            "Open immediately",
            "Share your password",
            "Disable security"
        ],
        "answer": "Verify it first"
    },

    {
        "id": 15,
        "topic": "Networking",
        "level": "Beginner",
        "question": "What does IP identify in a network?",
        "options": [
            "A network interface/device",
            "A keyboard",
            "A programming language",
            "A document"
        ],
        "answer": "A network interface/device"
    },

    {
        "id": 16,
        "topic": "C",
        "level": "Beginner",
        "question": "Which function is the starting point of a normal C program?",
        "options": ["main()", "start()", "run()", "begin()"],
        "answer": "main()"
    },

    {
        "id": 17,
        "topic": "C",
        "level": "Beginner",
        "question": "Which header provides printf()?",
        "options": ["stdio.h", "stdlib.h", "string.h", "math.h"],
        "answer": "stdio.h"
    },

    {
        "id": 18,
        "topic": "Python",
        "level": "Beginner",
        "question": "Which symbol begins a Python comment?",
        "options": ["#", "//", "/*", "$"],
        "answer": "#"
    },

    {
        "id": 19,
        "topic": "Programming",
        "level": "Beginner",
        "question": "What is a variable used for?",
        "options": [
            "Storing a value",
            "Displaying a monitor",
            "Connecting Wi-Fi",
            "Formatting a disk"
        ],
        "answer": "Storing a value"
    },

    {
        "id": 20,
        "topic": "Software",
        "level": "Beginner",
        "question": "What is debugging?",
        "options": [
            "Finding and fixing software problems",
            "Buying hardware",
            "Creating a presentation",
            "Formatting a drive"
        ],
        "answer": "Finding and fixing software problems"
    }
]


# ============================================================
# CAREER GUIDE
# ============================================================

career_guide = [

    {
        "title": "🎓 Internships",
        "content": """
Start building your portfolio early.

1. Learn one programming language properly.
2. Build 2–4 useful projects.
3. Put projects on GitHub.
4. Write a clean one-page resume.
5. Apply consistently instead of waiting for one perfect opportunity.
6. Learn how to explain your projects clearly.
7. Participate in college technical events and hackathons.

A small working project that you understand completely is more useful in an interview than a large project you cannot explain.
"""
    },

    {
        "title": "💼 Placements",
        "content": """
A practical placement preparation plan:

• Programming fundamentals
• Data Structures & Algorithms
• SQL
• OOP
• Operating Systems
• Computer Networks
• Basic system design
• Aptitude where required
• Communication
• Resume projects
• Mock interviews

Practice regularly rather than trying to complete everything immediately before interviews.
"""
    },

    {
        "title": "🚀 Software Developer",
        "content": """
A common beginner roadmap:

Year 1:
Programming + Git + basic projects

Year 2:
DSA + web/backend + databases

Year 3:
Internships + advanced projects + interview preparation

Year 4:
Placement preparation + specialization + professional portfolio

Choose one main development direction and become comfortable building real applications.
"""
    },

    {
        "title": "🐙 GitHub Portfolio",
        "content": """
Your GitHub should show evidence of your skills.

Good project README files should explain:

• Problem
• Solution
• Features
• Technologies
• Screenshots
• Installation
• How to use
• Future improvements

Avoid filling GitHub with copied projects that you cannot explain.
"""
    },

    {
        "title": "📄 Resume",
        "content": """
Keep your student resume simple.

Recommended structure:

1. Name and contact
2. Education
3. Technical skills
4. Projects
5. Experience/internships
6. Certifications
7. Achievements

For projects, explain what YOU built and what technologies YOU used.
"""
    },

    {
        "title": "🧠 Interview Preparation",
        "content": """
Practice explaining:

• Your strongest project
• Why you selected the technology
• Problems you faced
• How you fixed bugs
• Database design
• Authentication
• APIs
• Basic DSA
• OOP
• SQL

A strong project explanation should be understandable without reading your source code.
"""
    },

    {
        "title": "🔥 Smart Career Strategy",
        "content": """
There is no guaranteed shortcut into a job.

The practical strategy is:

Learn → Build → Publish → Explain → Practice → Apply → Improve

Use college time to build evidence of your ability instead of only collecting certificates.
"""
    }
]


# ============================================================
# ACHIEVEMENTS
# ============================================================

ACHIEVEMENTS = {
    "first_lesson": {
        "title": "🌱 First Step",
        "description": "Complete your first lesson."
    },

    "five_lessons": {
        "title": "🔥 Fast Learner",
        "description": "Complete 5 lessons."
    },

    "ten_lessons": {
        "title": "🚀 Knowledge Builder",
        "description": "Complete 10 lessons."
    },

    "hundred_xp": {
        "title": "⚡ XP Hunter",
        "description": "Earn 100 XP."
    },

    "quiz_master": {
        "title": "🏆 Quiz Master",
        "description": "Score at least 80% in a quiz."
    },

    "three_day_streak": {
        "title": "🔥 3-Day Streak",
        "description": "Maintain a 3-day learning streak."
    },

    "five_hundred_xp": {
        "title": "💎 XP Collector",
        "description": "Earn 500 XP."
    }
}


# ============================================================
# GENERAL HELPERS
# ============================================================

def clean_email(email):
    if not isinstance(email, str):
        return ""
    return email.strip().lower()


def valid_email(email):
    return (
        isinstance(email, str)
        and "@" in email
        and "." in email.split("@")[-1]
        and len(email) <= 254
    )


def now_iso():
    return datetime.utcnow().isoformat(timespec="seconds")


def get_user_by_id(user_id):
    db = get_db()

    user = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    db.close()
    return user


def get_progress(user_id):
    db = get_db()

    row = db.execute(
        "SELECT * FROM progress WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    if row is None:
        db.execute("""
            INSERT INTO progress (
                user_id,
                xp,
                points,
                streak,
                last_active,
                completed_lessons,
                achievements
            )
            VALUES (?, 0, 0, 0, ?, '[]', '[]')
        """, (user_id, date.today().isoformat()))

        db.commit()

        row = db.execute(
            "SELECT * FROM progress WHERE user_id = ?",
            (user_id,)
        ).fetchone()

    db.close()

    return row


def progress_json(row):
    return {
        "xp": row["xp"],
        "points": row["points"],
        "streak": row["streak"],
        "completed_lessons": json.loads(row["completed_lessons"] or "[]"),
        "achievements": json.loads(row["achievements"] or "[]"),
        "quizzes_completed": row["quizzes_completed"],
        "quizzes_passed": row["quizzes_passed"],
        "best_quiz_score": row["best_quiz_score"],
        "malpractice_events": row["malpractice_events"]
    }


def calculate_level(xp):
    levels = [
        "Code Explorer",
        "Bug Hunter",
        "Logic Builder",
        "Code Warrior",
        "System Architect",
        "AI Pathfinder",
        "CodeQuest Master"
    ]

    index = min(xp // 100, len(levels) - 1)

    return {
        "number": int(xp // 100) + 1,
        "name": levels[index],
        "next_xp": ((xp // 100) + 1) * 100,
        "progress": xp % 100
    }


def add_activity(user_id, event_type, details=""):
    db = get_db()

    db.execute("""
        INSERT INTO activity_log (
            user_id,
            event_type,
            details,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        event_type,
        details,
        now_iso()
    ))

    db.commit()
    db.close()


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        user_id = session.get("user_id")

        if not user_id:
            return jsonify({
                "success": False,
                "message": "Please login first."
            }), 401

        return function(*args, **kwargs)

    return wrapper


# ============================================================
# AUTHENTICATION
# ============================================================

@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = clean_email(data.get("email", ""))
    password = str(data.get("password", ""))

    if not name:
        return jsonify({
            "success": False,
            "message": "Please enter your name."
        }), 400

    if not valid_email(email):
        return jsonify({
            "success": False,
            "message": "Please enter a valid email address."
        }), 400

    if len(password) < 6:
        return jsonify({
            "success": False,
            "message": "Password must contain at least 6 characters."
        }), 400

    db = get_db()

    existing = db.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if existing:
        db.close()

        return jsonify({
            "success": False,
            "message": "An account with this email already exists."
        }), 409

    created = now_iso()

    cursor = db.execute("""
        INSERT INTO users (
            name,
            email,
            password_hash,
            created_at,
            last_login
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        email,
        generate_password_hash(password),
        created,
        created
    ))

    user_id = cursor.lastrowid

    db.execute("""
        INSERT INTO progress (
            user_id,
            xp,
            points,
            streak,
            last_active,
            completed_lessons,
            achievements
        )
        VALUES (?, 0, 0, 1, ?, '[]', '[]')
    """, (
        user_id,
        date.today().isoformat()
    ))

    db.commit()
    db.close()

    session.clear()

    session["user_id"] = user_id
    session["user"] = {
        "id": user_id,
        "name": name,
        "email": email
    }

    return jsonify({
        "success": True,
        "message": "Account created successfully.",
        "user": session["user"]
    }), 201


@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    email = clean_email(data.get("email", ""))
    password = str(data.get("password", ""))

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400

    db = get_db()

    user = db.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if not user:
        db.close()

        return jsonify({
            "success": False,
            "message": "Account not found. Please register first."
        }), 401

    if not user["password_hash"]:
        db.close()

        return jsonify({
            "success": False,
            "message": "This account uses Google login."
        }), 401

    if not check_password_hash(user["password_hash"], password):
        db.close()

        return jsonify({
            "success": False,
            "message": "Incorrect password."
        }), 401

    db.execute(
        "UPDATE users SET last_login = ? WHERE id = ?",
        (now_iso(), user["id"])
    )

    db.commit()
    db.close()

    session.clear()

    session["user_id"] = user["id"]

    session["user"] = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "user": session["user"]
    })


@app.route("/api/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    })


@app.route("/api/me")
def current_user():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "logged_in": False,
            "user": None
        })

    user = get_user_by_id(user_id)

    if not user:
        session.clear()

        return jsonify({
            "logged_in": False,
            "user": None
        })

    progress = get_progress(user_id)

    return jsonify({
        "logged_in": True,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        },
        "progress": progress_json(progress),
        "level": calculate_level(progress["xp"])
    })


# ============================================================
# FIREBASE GOOGLE LOGIN HOOK
# ============================================================

firebase_admin = None
firebase_auth = None

try:
    import firebase_admin
    from firebase_admin import credentials, auth as firebase_auth

    firebase_service_account = os.environ.get(
        "FIREBASE_SERVICE_ACCOUNT_JSON"
    )

    if firebase_service_account:

        credential_data = json.loads(firebase_service_account)

        firebase_admin.initialize_app(
            credentials.Certificate(credential_data)
        )

except Exception as firebase_error:

    firebase_admin = None
    firebase_auth = None


@app.route("/api/firebase-login", methods=["POST"])
def firebase_login():

    if firebase_auth is None:

        return jsonify({
            "success": False,
            "message": (
                "Firebase Admin is not configured on the server. "
                "Your existing Firebase client login can still be used, "
                "but server-side account synchronization requires "
                "FIREBASE_SERVICE_ACCOUNT_JSON."
            )
        }), 503

    data = request.get_json(silent=True) or {}

    id_token = str(data.get("idToken", "")).strip()

    if not id_token:

        return jsonify({
            "success": False,
            "message": "Firebase ID token is required."
        }), 400

    try:

        decoded = firebase_auth.verify_id_token(id_token)

        uid = decoded.get("uid")
        email = clean_email(decoded.get("email", ""))

        name = (
            decoded.get("name")
            or decoded.get("email")
            or "CodeQuest User"
        )

        if not uid or not email:

            return jsonify({
                "success": False,
                "message": "Firebase account information is incomplete."
            }), 400

        db = get_db()

        user = db.execute(
            "SELECT * FROM users WHERE firebase_uid = ?",
            (uid,)
        ).fetchone()

        if not user:

            user = db.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            ).fetchone()

        if user:

            db.execute("""
                UPDATE users
                SET name = ?,
                    email = ?,
                    firebase_uid = ?,
                    last_login = ?
                WHERE id = ?
            """, (
                name,
                email,
                uid,
                now_iso(),
                user["id"]
            ))

            user_id = user["id"]

        else:

            cursor = db.execute("""
                INSERT INTO users (
                    name,
                    email,
                    password_hash,
                    firebase_uid,
                    created_at,
                    last_login
                )
                VALUES (?, ?, NULL, ?, ?, ?)
            """, (
                name,
                email,
                uid,
                now_iso(),
                now_iso()
            ))

            user_id = cursor.lastrowid

            db.execute("""
                INSERT INTO progress (
                    user_id,
                    xp,
                    points,
                    streak,
                    last_active,
                    completed_lessons,
                    achievements
                )
                VALUES (?, 0, 0, 1, ?, '[]', '[]')
            """, (
                user_id,
                date.today().isoformat()
            ))

        db.commit()
        db.close()

        session.clear()

        session["user_id"] = user_id

        session["user"] = {
            "id": user_id,
            "name": name,
            "email": email
        }

        return jsonify({
            "success": True,
            "message": "Google login successful.",
            "user": session["user"]
        })

    except Exception:

        return jsonify({
            "success": False,
            "message": "Invalid or expired Firebase login token."
        }), 401


# ============================================================
# COURSES
# ============================================================

@app.route("/api/courses")
def get_courses():

    return jsonify(courses)


@app.route("/api/course/<course_id>")
def get_course(course_id):

    for course in courses:

        if course["id"] == course_id:
            return jsonify(course)

    return jsonify({
        "success": False,
        "message": "Course not found."
    }), 404


@app.route("/api/roadmap")
def get_roadmap():

    return jsonify({
        "total": len(roadmap),
        "roadmap": roadmap
    })


@app.route("/api/stats")
def stats():

    total_chapters = sum(
        len(course["chapters"])
        for course in courses
    )

    return jsonify({

        "courses": len(courses),

        "chapters": total_chapters,

        "quiz_questions": len(quiz_questions),

        "career_topics": len(career_guide),

        "roadmap_topics": len(roadmap),

        "features": [
            "Learning",
            "Quiz Arena",
            "XP System",
            "Achievements",
            "Career Guide",
            "C Compiler",
            "Progress Tracking",
            "Google Login"
        ]
    })


# ============================================================
# PROGRESS / XP
# ============================================================

@app.route("/api/progress")
@login_required
def get_user_progress():

    user_id = session["user_id"]

    progress = get_progress(user_id)

    return jsonify({
        "success": True,
        "progress": progress_json(progress),
        "level": calculate_level(progress["xp"])
    })


@app.route("/api/progress/lesson", methods=["POST"])
@login_required
def complete_lesson():

    user_id = session["user_id"]

    data = request.get_json(silent=True) or {}

    course_id = str(data.get("course_id", "")).strip()
    chapter_title = str(data.get("chapter_title", "")).strip()

    if not course_id or not chapter_title:

        return jsonify({
            "success": False,
            "message": "Course and chapter are required."
        }), 400

    lesson_key = f"{course_id}::{chapter_title}"

    db = get_db()

    row = db.execute(
        "SELECT * FROM progress WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    completed = json.loads(
        row["completed_lessons"] or "[]"
    )

    if lesson_key in completed:

        db.close()

        return jsonify({
            "success": True,
            "already_completed": True,
            "message": "Lesson already completed.",
            "progress": progress_json(row),
            "level": calculate_level(row["xp"])
        })

    completed.append(lesson_key)

    new_xp = row["xp"] + 20
    new_points = row["points"] + 20

    achievements = json.loads(
        row["achievements"] or "[]"
    )

    def unlock(key):
        if key not in achievements:
            achievements.append(key)

    unlock("first_lesson")

    if len(completed) >= 5:
        unlock("five_lessons")

    if len(completed) >= 10:
        unlock("ten_lessons")

    if new_xp >= 100:
        unlock("hundred_xp")

    if new_xp >= 500:
        unlock("five_hundred_xp")

    today = date.today()
    last_active = row["last_active"]

    streak = row["streak"] or 0

    if last_active:

        try:

            previous = date.fromisoformat(last_active)

            if previous == today:
                pass

            elif previous == today - timedelta(days=1):

                streak += 1

            else:

                streak = 1

        except ValueError:

            streak = 1

    else:

        streak = 1

    if streak >= 3:
        unlock("three_day_streak")

    db.execute("""
        UPDATE progress
        SET xp = ?,
            points = ?,
            streak = ?,
            last_active = ?,
            completed_lessons = ?,
            achievements = ?
        WHERE user_id = ?
    """, (
        new_xp,
        new_points,
        streak,
        today.isoformat(),
        json.dumps(completed),
        json.dumps(achievements),
        user_id
    ))

    db.commit()

    updated = db.execute(
        "SELECT * FROM progress WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    db.close()

    add_activity(
        user_id,
        "lesson_completed",
        lesson_key
    )

    return jsonify({
        "success": True,
        "message": "Lesson completed!",
        "xp_earned": 20,
        "progress": progress_json(updated),
        "level": calculate_level(updated["xp"])
    })


# ============================================================
# QUIZ
# ============================================================

@app.route("/api/quiz")
def get_quiz():

    safe_questions = []

    for question in quiz_questions:

        safe_questions.append({
            "id": question["id"],
            "topic": question["topic"],
            "level": question["level"],
            "question": question["question"],
            "options": question["options"]
        })

    return jsonify({
        "total": len(safe_questions),
        "questions": safe_questions
    })


@app.route("/api/quiz/submit", methods=["POST"])
@login_required
def submit_quiz():

    user_id = session["user_id"]

    data = request.get_json(silent=True) or {}

    answers = data.get("answers", [])

    terminated = bool(data.get("terminated", False))

    termination_reason = str(
        data.get("termination_reason", "")
    )[:500]

    if not isinstance(answers, list):

        return jsonify({
            "success": False,
            "message": "Invalid quiz submission."
        }), 400

    score = 0
    total = len(answers)

    question_map = {
        str(q["id"]): q
        for q in quiz_questions
    }

    for submitted in answers:

        question_id = str(
            submitted.get("id", "")
        )

        selected = submitted.get("answer")

        question = question_map.get(question_id)

        if question and selected == question["answer"]:

            score += 1

    xp_earned = 0

    if not terminated:

        xp_earned = score * 10

        if total > 0:

            percentage = int(
                (score / total) * 100
            )

            if percentage >= 80:

                xp_earned += 30

    db = get_db()

    row = db.execute(
        "SELECT * FROM progress WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    new_xp = row["xp"] + xp_earned
    new_points = row["points"] + xp_earned

    achievements = json.loads(
        row["achievements"] or "[]"
    )

    if (
        not terminated
        and total > 0
        and score / total >= 0.8
        and "quiz_master" not in achievements
    ):

        achievements.append("quiz_master")

    db.execute("""
        UPDATE progress
        SET xp = ?,
            points = ?,
            quizzes_completed = quizzes_completed + 1,
            quizzes_passed = quizzes_passed + ?,
            best_quiz_score = MAX(best_quiz_score, ?),
            achievements = ?,
            malpractice_events =
                malpractice_events + ?
        WHERE user_id = ?
    """, (
        new_xp,
        new_points,
        1 if (
            not terminated
            and total > 0
            and score / total >= 0.5
        ) else 0,
        int(
            (score / total) * 100
        ) if total else 0,
        json.dumps(achievements),
        1 if terminated else 0,
        user_id
    ))

    db.execute("""
        INSERT INTO quiz_attempts (
            user_id,
            score,
            total,
            xp_earned,
            terminated,
            reason,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        score,
        total,
        xp_earned,
        1 if terminated else 0,
        termination_reason,
        now_iso()
    ))

    db.commit()

    updated = db.execute(
        "SELECT * FROM progress WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    db.close()

    add_activity(
        user_id,
        "quiz_completed",
        f"{score}/{total}"
    )

    return jsonify({
        "success": True,
        "score": score,
        "total": total,
        "percentage": int(
            (score / total) * 100
        ) if total else 0,
        "xp_earned": xp_earned,
        "terminated": terminated,
        "message": (
            "Quiz terminated because of a violation."
            if terminated
            else "Quiz completed successfully."
        ),
        "progress": progress_json(updated),
        "level": calculate_level(updated["xp"])
    })


# ============================================================
# MALPRACTICE / QUIZ SECURITY
# ============================================================

@app.route("/api/quiz/violation", methods=["POST"])
@login_required
def quiz_violation():

    user_id = session["user_id"]

    data = request.get_json(silent=True) or {}

    reason = str(
        data.get("reason", "Unknown violation")
    )[:500]

    db = get_db()

    db.execute("""
        UPDATE progress
        SET malpractice_events =
            malpractice_events + 1
        WHERE user_id = ?
    """, (user_id,))

    db.commit()
    db.close()

    add_activity(
        user_id,
        "quiz_violation",
        reason
    )

    return jsonify({
        "success": True,
        "message": "Quiz violation recorded."
    })


# ============================================================
# ACHIEVEMENTS
# ============================================================

@app.route("/api/achievements")
def get_achievements():

    return jsonify({
        "achievements": [
            {
                "id": key,
                **value
            }
            for key, value in ACHIEVEMENTS.items()
        ]
    })


# ============================================================
# CAREER GUIDE
# ============================================================

@app.route("/api/careers")
def get_careers():

    return jsonify(career_guide)


@app.route("/api/career-roadmap")
def career_roadmap():

    return jsonify({

        "steps": [

            {
                "step": 1,
                "title": "Build Fundamentals",
                "description": "Learn programming, Git, databases and computer science basics."
            },

            {
                "step": 2,
                "title": "Build Projects",
                "description": "Create practical projects that solve real problems."
            },

            {
                "step": 3,
                "title": "Build GitHub",
                "description": "Publish projects with clean README files and screenshots."
            },

            {
                "step": 4,
                "title": "Prepare Resume",
                "description": "Present skills, projects and achievements clearly."
            },

            {
                "step": 5,
                "title": "Practice Interviews",
                "description": "Practice DSA, SQL, OOP, projects and communication."
            },

            {
                "step": 6,
                "title": "Apply Consistently",
                "description": "Apply to internships and entry-level opportunities while continuing to improve."
            }

        ]

    })


# ============================================================
# PROJECT IDEAS
# ============================================================

@app.route("/api/projects")
def project_ideas():

    projects = [

        {
            "title": "📚 Student Study Assistant",
            "level": "Beginner",
            "description": "Track subjects, assignments and study sessions."
        },

        {
            "title": "💰 Expense Tracker",
            "level": "Beginner",
            "description": "Record expenses and visualize monthly spending."
        },

        {
            "title": "📝 Online Quiz Platform",
            "level": "Intermediate",
            "description": "Create quizzes with scores, timer and progress."
        },

        {
            "title": "🔐 Secure Notes",
            "level": "Intermediate",
            "description": "Build a notes application with authentication."
        },

        {
            "title": "🤖 AI Student Assistant",
            "level": "Intermediate",
            "description": "Build an educational assistant around useful student workflows."
        },

        {
            "title": "🚀 Full Stack College Portal",
            "level": "Advanced",
            "description": "Combine authentication, database, APIs and dashboards."
        }

    ]

    return jsonify(projects)


# ============================================================
# C COMPILER
# ============================================================

"""
The browser should POST:

{
    "code": "#include <stdio.h> ...",
    "input": "..."
}

to:

/api/compile

This backend does NOT execute arbitrary C code directly on the
Flask server. That would be unsafe.

Instead, configure an external sandbox/execution service using:

JUDGE0_URL
JUDGE0_API_KEY       optional depending on your provider
JUDGE0_HOST          optional
"""

JUDGE0_URL = os.environ.get(
    "JUDGE0_URL",
    ""
).strip().rstrip("/")

JUDGE0_API_KEY = os.environ.get(
    "JUDGE0_API_KEY",
    ""
).strip()

JUDGE0_HOST = os.environ.get(
    "JUDGE0_HOST",
    ""
).strip()


def judge0_request(code, stdin_data):

    if not JUDGE0_URL:

        return {
            "success": False,
            "configured": False,
            "error": (
                "C compiler backend is not configured yet. "
                "Set JUDGE0_URL on the server."
            )
        }

    payload = {
        "source_code": code,
        "language_id": 50,
        "stdin": stdin_data
    }

    body = json.dumps(payload).encode("utf-8")

    url = (
        JUDGE0_URL +
        "/submissions?wait=true"
    )

    headers = {
        "Content-Type": "application/json"
    }

    if JUDGE0_API_KEY:
        headers["X-Auth-Token"] = JUDGE0_API_KEY

    if JUDGE0_HOST:
        headers["X-RapidAPI-Host"] = JUDGE0_HOST
        headers["X-RapidAPI-Key"] = JUDGE0_API_KEY

    request_object = urllib.request.Request(
        url,
        data=body,
        headers=headers,
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request_object,
            timeout=20
        ) as response:

            raw = response.read().decode(
                "utf-8",
                errors="replace"
            )

            result = json.loads(raw)

            stdout = result.get("stdout") or ""
            stderr = result.get("stderr") or ""
            compile_output = (
                result.get("compile_output")
                or ""
            )

            message = result.get("message") or ""

            if compile_output:

                return {
                    "success": False,
                    "status": result.get("status"),
                    "output": stdout,
                    "error": compile_output,
                    "message": message
                }

            if stderr:

                return {
                    "success": False,
                    "status": result.get("status"),
                    "output": stdout,
                    "error": stderr,
                    "message": message
                }

            return {
                "success": True,
                "status": result.get("status"),
                "output": stdout,
                "error": "",
                "message": message
            }

    except urllib.error.HTTPError as error:

        try:
            details = error.read().decode(
                "utf-8",
                errors="replace"
            )
        except Exception:
            details = ""

        return {
            "success": False,
            "error": (
                f"Compiler service returned HTTP "
                f"{error.code}."
            ),
            "details": details[:1000]
        }

    except Exception as error:

        return {
            "success": False,
            "error": (
                "Unable to connect to the compiler service."
            ),
            "details": str(error)[:500]
        }


@app.route("/api/compile", methods=["POST"])
@login_required
def compile_code():

    data = request.get_json(silent=True) or {}

    code = str(
        data.get("code", "")
    )

    stdin_data = str(
        data.get("input", "")
    )

    if not code.strip():

        return jsonify({
            "success": False,
            "error": "Please enter C code."
        }), 400

    if len(code) > 50000:

        return jsonify({
            "success": False,
            "error": "Code is too large."
        }), 413

    if len(stdin_data) > 10000:

        return jsonify({
            "success": False,
            "error": "Input is too large."
        }), 413

    result = judge0_request(
        code,
        stdin_data
    )

    add_activity(
        session["user_id"],
        "code_compilation",
        "C program executed"
    )

    return jsonify(result)


# ============================================================
# USER ACTIVITY
# ============================================================

@app.route("/api/activity", methods=["POST"])
@login_required
def activity():

    data = request.get_json(silent=True) or {}

    event_type = str(
        data.get("event", "activity")
    )[:100]

    details = str(
        data.get("details", "")
    )[:500]

    add_activity(
        session["user_id"],
        event_type,
        details
    )

    return jsonify({
        "success": True
    })


# ============================================================
# HEALTH
# ============================================================

@app.route("/health")
def health():

    database_ok = False

    try:

        db = get_db()

        db.execute(
            "SELECT 1"
        ).fetchone()

        db.close()

        database_ok = True

    except Exception:
        database_ok = False

    return jsonify({

        "status": "ok",

        "application": "CodeQuest AI",

        "database": (
            "connected"
            if database_ok
            else "error"
        ),

        "courses": len(courses),

        "chapters": sum(
            len(course["chapters"])
            for course in courses
        ),

        "quiz_questions": len(quiz_questions),

        "compiler": (
            "configured"
            if JUDGE0_URL
            else "not_configured"
        )

    })


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):

    if request.path.startswith("/api/"):

        return jsonify({
            "success": False,
            "error": "API route not found."
        }), 404

    return render_template(
        "index.html"
    )


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({
        "success": False,
        "error": "Method not allowed."
    }), 405


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "success": False,
        "error": "Internal server error."
    }), 500


# ============================================================
# STARTUP
# ============================================================

init_db()


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
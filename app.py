from flask import Flask, jsonify, request, render_template
import os
import json
import sqlite3
import secrets
import time
import urllib.request
import urllib.error

# ============================================================
# CODEQUEST AI
# Learn • Practice • Play • Build
# Backend V1.0
# ============================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "codequest-ai-development-secret-change-me"
)

DATABASE_PATH = os.environ.get(
    "DATABASE_PATH",
    "codequest.db"
)

# ============================================================
# OPTIONAL FIREBASE ADMIN
# ============================================================

firebase_ready = False
firebase_auth = None

try:
    import firebase_admin
    from firebase_admin import credentials, auth as firebase_auth_module

    firebase_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")

    if firebase_json:
        try:
            service_account_info = json.loads(firebase_json)

            if not firebase_admin._apps:
                cred = credentials.Certificate(service_account_info)
                firebase_admin.initialize_app(cred)

            firebase_auth = firebase_auth_module
            firebase_ready = True

        except Exception as firebase_error:
            print("Firebase Admin initialization failed:", firebase_error)

except Exception as firebase_import_error:
    print("Firebase Admin not installed:", firebase_import_error)


# ============================================================
# DATABASE
# ============================================================

def get_db():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    db = get_db()

    db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        uid TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        photo_url TEXT,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        streak INTEGER DEFAULT 0,
        last_activity TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS progress (
        uid TEXT,
        lesson_id TEXT,
        course_id TEXT,
        completed INTEGER DEFAULT 0,
        completed_at TEXT,
        PRIMARY KEY(uid, lesson_id)
    );

    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT,
        score INTEGER,
        total INTEGER,
        xp_earned INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT,
        activity TEXT,
        xp INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    db.commit()
    db.close()


init_db()


# ============================================================
# COURSE HELPERS
# ============================================================

def lesson(
    lesson_id,
    title,
    explanation,
    example="",
    key_points=None
):
    return {
        "id": lesson_id,
        "title": title,
        "lesson": explanation,
        "sample": example,
        "key_points": key_points or []
    }


def course(
    course_id,
    title,
    icon,
    level,
    description,
    chapters
):
    return {
        "id": course_id,
        "title": title,
        "icon": icon,
        "level": level,
        "description": description,
        "chapters": chapters
    }


# ============================================================
# MASSIVE COURSE LIBRARY
# ============================================================

courses = [

# ============================================================
# 1. COMPUTER BASICS
# ============================================================

course(
    "computer-basics",
    "Computer Basics",
    "💻",
    "Beginner",
    "Understand computers from the ground up before learning programming.",
    [

        lesson(
            "cb-01",
            "What is a Computer?",
            """
A computer is an electronic device that accepts data as input, processes that data according to instructions, stores information when required, and produces useful output. The important point is that a computer is not simply a machine for doing calculations. Modern computers are used for communication, entertainment, education, banking, software development, scientific research, artificial intelligence and thousands of other activities.

A simple way to understand a computer is through the input-process-output model. When you type something using a keyboard, the keyboard provides input. The processor and software process that input. The computer may store the information in memory or storage, and finally the result appears on a screen or another output device.

For example, when you open CodeQuest AI and click a lesson, your phone or computer receives your touch as input, the browser processes the website code, the server may process an API request, and the final lesson appears on your screen as output.
            """,
            """
Input → Processing → Output

Example:
Keyboard → CPU/Software → Monitor
Mouse → CPU/Software → Screen
Microphone → CPU/Software → Speakers
            """,
            [
                "A computer accepts input.",
                "A computer processes data.",
                "A computer can store information.",
                "A computer produces output."
            ]
        ),

        lesson(
            "cb-02",
            "Hardware and Software",
            """
Computer hardware refers to the physical components that you can touch. Examples include the CPU, RAM, motherboard, keyboard, mouse, monitor and storage drive. Software is the collection of programs and instructions that tell hardware what to do.

Hardware without software cannot perform useful tasks by itself, while software requires hardware to execute its instructions. For example, a web browser is software, but it needs a processor, memory and storage to run.

When you write a Python program, the Python interpreter is software. The CPU, RAM and storage inside your computer are hardware that allow that software to execute.
            """,
            """
Hardware:
CPU
RAM
SSD
Keyboard
Monitor

Software:
Windows
Chrome
Python
VS Code
            """
        ),

        lesson(
            "cb-03",
            "CPU and Processing",
            """
The Central Processing Unit, commonly called the CPU or processor, executes instructions and performs calculations. It is often described as the brain of the computer, although technically it is better understood as the component responsible for executing machine instructions.

A CPU contains processing components such as the arithmetic logic unit, control unit and registers. Modern processors also contain multiple cores, allowing several instruction streams to be processed efficiently.

When a program calculates 25 + 75, the program's instructions eventually become machine-level operations that the processor executes.
            """,
            """
int a = 25;
int b = 75;
int result = a + b;

printf("%d", result);
            """
        ),

        lesson(
            "cb-04",
            "RAM and Memory",
            """
RAM stands for Random Access Memory. It is temporary working memory used by programs while they are running. When you open a browser, game or coding application, the operating system loads the necessary program data into RAM so that the CPU can access it quickly.

RAM is volatile, which means its contents normally disappear when the device loses power. This is different from SSD or hard-disk storage, which keeps data after the computer is turned off.

More RAM can allow a system to keep more active applications and data available at the same time, although performance also depends on the CPU, storage and software.
            """,
            """
Example:

Opening:
Chrome
VS Code
Music player

All three applications require RAM while they are running.
            """
        ),

        lesson(
            "cb-05",
            "Storage: HDD and SSD",
            """
Storage is used to keep data for longer periods. Hard disk drives use magnetic disks and mechanical components, while solid-state drives use flash memory and have no spinning disks.

SSDs are generally much faster for starting operating systems and applications because they provide low-latency access to stored data. Storage capacity is measured using units such as GB and TB.

Your source code, photographs, videos, documents and installed applications are normally stored on persistent storage rather than RAM.
            """,
            """
Example:

512 GB SSD
├── Windows
├── VS Code
├── Python
├── Projects
└── Personal files
            """
        ),

        lesson(
            "cb-06",
            "Operating Systems",
            """
An operating system is system software that manages computer hardware and provides services for applications. Windows, Linux, Android and macOS are examples of operating systems.

The operating system manages processes, memory, files, devices, permissions and networking. When you open an application, the operating system creates and manages the process and allocates resources to it.

For a programmer, understanding operating systems is important because software ultimately runs on top of operating-system services.
            """,
            """
Application
    ↓
Operating System
    ↓
Hardware

Example:
Chrome
↓
Windows
↓
CPU + RAM + SSD + Network
            """
        ),

        lesson(
            "cb-07",
            "Files and Folders",
            """
A file is a named collection of data stored by a computer. A folder is used to organize files and other folders. Operating systems use paths to identify where files are located.

For programmers, understanding paths is important because programs frequently read configuration files, source code, images and databases. A relative path starts from the current working directory, while an absolute path identifies a location from the root of the file system.
            """,
            """
project/
├── app.py
├── index.html
├── style.css
└── images/
    └── logo.png
            """
        ),

        lesson(
            "cb-08",
            "Binary and Data Representation",
            """
Computers ultimately represent information using binary values. Binary uses two symbols: 0 and 1. Individual binary digits are called bits, and groups of eight bits form a byte.

Numbers, text, images, audio and video are all represented using combinations of binary data. Programming languages hide most of this complexity from beginners, but understanding binary becomes useful when learning networking, memory, cybersecurity and computer architecture.
            """,
            """
Decimal 5 = Binary 101

Binary:
1×4 + 0×2 + 1×1 = 5
            """
        ),

        lesson(
            "cb-09",
            "Input and Output Devices",
            """
Input devices allow users or other systems to provide data to a computer. Examples include keyboards, mice, cameras, microphones and touchscreens.

Output devices communicate processed information back to the user. Examples include monitors, speakers and printers. Some devices perform both roles. A touchscreen, for example, displays output while also accepting touch input.
            """,
            """
Touchscreen:
Touch → Input
Display → Output
            """
        ),

        lesson(
            "cb-10",
            "Internet and the Web",
            """
The Internet is a global network of interconnected computer networks. The World Wide Web is one service that operates over the Internet. Websites communicate using protocols such as HTTP and HTTPS.

When you open a website, your device communicates with a server. DNS can translate a domain name into an IP address, a connection is established, and HTTP requests and responses transfer information between the browser and server.
            """,
            """
Browser
   ↓ HTTP request
Internet
   ↓
Web Server
   ↓ HTTP response
Browser
            """
        )
    ]
),

# ============================================================
# 2. PRODUCTIVITY
# ============================================================

course(
    "productivity",
    "Digital Productivity",
    "📊",
    "Beginner",
    "Learn practical computer productivity and professional digital skills.",
    [

        lesson(
            "prod-01",
            "Word Processing",
            """
Word processors are applications used to create and format documents. Microsoft Word and similar applications provide tools for headings, paragraphs, tables, images, page layout and document collaboration.

For an IT student, word processing is useful for lab records, project documentation, resumes, reports and assignments. Good formatting is not merely decoration; consistent headings and spacing make information easier to understand.
            """,
            """
Professional document structure:

Title
↓
Introduction
↓
Main Content
↓
Tables / Figures
↓
Conclusion
            """
        ),

        lesson(
            "prod-02",
            "Spreadsheets",
            """
Spreadsheets organize information in rows and columns and can perform calculations using formulas. They are useful for marks, budgets, attendance, experiments, project planning and data analysis.

A spreadsheet formula can reference other cells, meaning that changing an input automatically updates related calculations. This introduces an important programming concept: data and operations can be connected.
            """,
            """
A1 = 50
A2 = 70

A3:
=AVERAGE(A1:A2)
            """
        ),

        lesson(
            "prod-03",
            "Presentations",
            """
Presentation software is used to communicate ideas visually. A good technical presentation normally contains a clear problem, explanation, evidence or demonstration, and conclusion.

For engineering students, presentation skills are useful when explaining projects, research, technical concepts and software demonstrations.
            """,
            """
Presentation flow:

Problem
→ Idea
→ Technology
→ Demonstration
→ Result
→ Future scope
            """
        ),

        lesson(
            "prod-04",
            "Professional File Organization",
            """
Good file organization becomes increasingly important as projects grow. Instead of keeping every file in one directory, related files should be grouped logically.

A consistent naming convention makes projects easier to maintain and share with teammates. This habit becomes especially useful when working with Git and GitHub.
            """,
            """
CodeQuestAI/
├── backend/
├── frontend/
├── assets/
├── docs/
└── README.md
            """
        )
    ]
),

# ============================================================
# 3. GIT
# ============================================================

course(
    "git-github",
    "Git & GitHub",
    "🐙",
    "Beginner → Intermediate",
    "Learn version control and professional project collaboration.",
    [

        lesson(
            "git-01",
            "What is Git?",
            """
Git is a distributed version-control system used to track changes in files. Instead of manually creating folders such as project-final, project-final2 and project-final-real, Git records the history of changes.

This allows developers to experiment, compare versions and return to earlier states when necessary. Git is one of the most important tools in modern software development.
            """,
            """
git init
git add .
git commit -m "Initial project"
            """
        ),

        lesson(
            "git-02",
            "Repositories",
            """
A Git repository is a project whose files and change history are managed by Git. A repository can exist locally on your computer and can also be hosted on platforms such as GitHub.

Repositories make it possible to track who changed what, when changes were made and how the project evolved.
            """,
            """
Local project
     ↓
Git repository
     ↓
GitHub repository
            """
        ),

        lesson(
            "git-03",
            "Commit",
            """
A commit is a saved snapshot of project changes. Good commit messages explain what changed rather than simply saying 'update'.

Frequent meaningful commits make debugging and collaboration easier because developers can understand the history of the project.
            """,
            """
git add .
git commit -m "Fix quiz API"
            """
        ),

        lesson(
            "git-04",
            "Branches",
            """
A branch allows developers to work on a separate line of development without immediately changing the main version. This is useful for developing features, fixing bugs and testing ideas.

A feature can be developed in a branch and merged into the main branch after it has been reviewed.
            """,
            """
git checkout -b quiz-improvements
            """
        ),

        lesson(
            "git-05",
            "GitHub",
            """
GitHub is a platform for hosting Git repositories and collaborating on software projects. Developers use GitHub for source code, issues, pull requests, documentation and project discussions.

For a college student, a well-organized GitHub profile can also demonstrate practical project experience.
            """,
            """
git remote add origin YOUR_REPOSITORY
git push -u origin main
            """
        )
    ]
),

# ============================================================
# 4. C
# ============================================================

course(
    "c-programming",
    "C Programming",
    "🔵",
    "Beginner",
    "Build strong programming fundamentals using C.",
    [

        lesson(
            "c-01",
            "Your First C Program",
            """
C is a compiled programming language widely used for systems programming, embedded systems, operating systems and performance-sensitive software. Learning C gives students a strong understanding of variables, memory, control flow and program structure.

A C program normally contains a main function where execution begins. The printf function can display information on the console.
            """,
            """#include <stdio.h>

int main() {
    printf("Hello, CodeQuest AI!");
    return 0;
}"""
        ),

        lesson(
            "c-02",
            "Variables and Data Types",
            """
A variable is a named location used to store a value. C requires variables to have a data type such as int, float, double or char.

Choosing the correct data type tells the compiler what kind of value the variable will contain and how operations on that value should be interpreted.
            """,
            """int age = 18;
float mark = 92.5;
char grade = 'A';

printf("%d %.1f %c", age, mark, grade);"""
        ),

        lesson(
            "c-03",
            "Operators",
            """
Operators allow programs to perform calculations and comparisons. Arithmetic operators include +, -, *, / and %. Relational operators compare values, while logical operators combine conditions.

Understanding operators is essential because almost every useful program performs calculations or makes decisions based on comparisons.
            """,
            """int a = 10;
int b = 3;

printf("%d\n", a + b);
printf("%d\n", a % b);"""
        ),

        lesson(
            "c-04",
            "If Else",
            """
Conditional statements allow a program to choose between different actions. The if statement executes code when a condition is true, while else handles the alternative.

This is one of the foundations of programming logic because real applications constantly make decisions based on input and state.
            """,
            """int mark = 82;

if (mark >= 50) {
    printf("Pass");
} else {
    printf("Fail");
}"""
        ),

        lesson(
            "c-05",
            "Loops",
            """
Loops repeat a section of code. C provides for, while and do-while loops. Loops are useful when a task must be repeated without writing the same statements many times.

For example, printing numbers from 1 to 100 manually would be inefficient. A loop can perform the same task with a few lines.
            """,
            """for (int i = 1; i <= 10; i++) {
    printf("%d\n", i);
}"""
        ),

        lesson(
            "c-06",
            "Functions",
            """
Functions divide a program into reusable blocks. A function can accept inputs called parameters and may return a result.

Breaking large programs into functions makes code easier to read, test and maintain.
            """,
            """int add(int a, int b) {
    return a + b;
}

int main() {
    printf("%d", add(10, 20));
    return 0;
}"""
        ),

        lesson(
            "c-07",
            "Arrays",
            """
An array stores multiple values of the same data type in contiguous memory. Instead of creating separate variables for ten marks, an array allows the program to store them under one name and access each value using an index.
            """,
            """int marks[5] = {80, 75, 91, 68, 88};

for (int i = 0; i < 5; i++) {
    printf("%d\n", marks[i]);
}"""
        ),

        lesson(
            "c-08",
            "Pointers",
            """
A pointer is a variable that stores a memory address. Pointers are one of the concepts that makes C powerful because they allow programs to work directly with memory.

The address-of operator & obtains an address, while * can be used to access the value stored at that address.
            """,
            """int x = 25;
int *p = &x;

printf("%d\n", x);
printf("%d\n", *p);"""
        ),

        lesson(
            "c-09",
            "Structures",
            """
Structures allow programmers to combine different types of data into one custom data type. This is useful for representing real-world entities such as students, employees or products.

A student record could contain a name, roll number and mark in one structure.
            """,
            """struct Student {
    char name[30];
    int mark;
};

struct Student s = {"Joe", 92};

printf("%s %d", s.name, s.mark);"""
        ),

        lesson(
            "c-10",
            "File Handling",
            """
Programs often need to store information permanently. C provides file-handling functions for opening, reading, writing and closing files.

This introduces the important difference between temporary variables in memory and persistent information stored on a disk.
            """,
            """FILE *file = fopen("data.txt", "w");

if (file != NULL) {
    fprintf(file, "CodeQuest AI");
    fclose(file);
}"""
        )
    ]
),

# ============================================================
# 5. C++
# ============================================================

course(
    "cpp",
    "C++ Programming",
    "🟣",
    "Intermediate",
    "Learn object-oriented and modern C++ programming.",
    [

        lesson(
            "cpp-01",
            "C++ Basics",
            """
C++ extends the C programming language with features such as classes, objects, templates and a large standard library. It is widely used in systems software, game development, competitive programming and performance-sensitive applications.
            """,
            """#include <iostream>
using namespace std;

int main() {
    cout << "Hello C++";
    return 0;
}"""
        ),

        lesson(
            "cpp-02",
            "Classes and Objects",
            """
A class defines the structure and behavior of objects. Object-oriented programming allows related data and operations to be grouped together.

For example, a Student class can contain a student's name and methods that display information about that student.
            """,
            """class Student {
public:
    string name;

    void show() {
        cout << name;
    }
};"""
        ),

        lesson(
            "cpp-03",
            "Constructors",
            """
A constructor is a special member function that runs when an object is created. Constructors are commonly used to initialize an object's data.

This prevents objects from being created in an incomplete or invalid initial state.
            """,
            """class Student {
public:
    string name;

    Student(string n) {
        name = n;
    }
};"""
        ),

        lesson(
            "cpp-04",
            "STL",
            """
The C++ Standard Template Library provides reusable data structures and algorithms. Containers such as vector, map and set save programmers from implementing common structures from scratch.

Learning STL is particularly useful for problem solving and technical interviews.
            """,
            """#include <vector>
using namespace std;

vector<int> numbers = {10, 20, 30};

for (int x : numbers) {
    cout << x << endl;
}"""
        )
    ]
),

# ============================================================
# 6. PYTHON
# ============================================================

course(
    "python",
    "Python Programming",
    "🐍",
    "Beginner → Intermediate",
    "Learn Python for automation, development, data and AI.",
    [

        lesson(
            "py-01",
            "Python Introduction",
            """
Python is a high-level programming language known for readable syntax and a large ecosystem of libraries. It is used for web development, automation, data analysis, artificial intelligence, testing and many other tasks.

Python is popular among beginners because programs can often express an idea using relatively few lines of code.
            """,
            """name = "CodeQuest AI"
print("Welcome to", name)"""
        ),

        lesson(
            "py-02",
            "Variables",
            """
Python variables refer to objects and do not require the programmer to declare a traditional static type for every variable. Python determines the type of an object at runtime.

This makes Python convenient for rapid development, although programmers still need to understand the kinds of values they are working with.
            """,
            """name = "Joe"
age = 18
mark = 92.5

print(name)
print(age)
print(mark)"""
        ),

        lesson(
            "py-03",
            "Conditions",
            """
Conditional statements allow Python programs to make decisions. The if, elif and else keywords let a program choose different code paths based on conditions.

This same basic idea appears in web applications, games, automation scripts and data-processing programs.
            """,
            """mark = 85

if mark >= 90:
    print("Excellent")
elif mark >= 50:
    print("Pass")
else:
    print("Needs improvement")"""
        ),

        lesson(
            "py-04",
            "Loops",
            """
Loops allow Python programs to repeat operations. The for loop is commonly used to iterate through sequences, while the while loop repeats while a condition remains true.

Loops are particularly useful when processing collections of data.
            """,
            """for number in range(1, 6):
    print(number)"""
        ),

        lesson(
            "py-05",
            "Functions",
            """
Functions package reusable logic into named blocks. A function can receive parameters and return a value.

Using functions prevents duplicated code and makes larger Python applications easier to organize.
            """,
            """def add(a, b):
    return a + b

result = add(10, 20)
print(result)"""
        ),

        lesson(
            "py-06",
            "Lists and Dictionaries",
            """
Lists store ordered collections of values, while dictionaries store key-value pairs. These structures are fundamental to Python programming and are used heavily when processing API responses, configuration data and application state.
            """,
            """student = {
    "name": "Joe",
    "mark": 92
}

print(student["name"])
print(student["mark"])"""
        ),

        lesson(
            "py-07",
            "Exception Handling",
            """
Programs can encounter errors while running, such as invalid input or missing files. Python provides try and except blocks so programs can handle expected runtime problems without immediately terminating.
            """,
            """try:
    number = int(input("Enter number: "))
    print(100 / number)
except ValueError:
    print("Invalid number")
except ZeroDivisionError:
    print("Cannot divide by zero")"""
        ),

        lesson(
            "py-08",
            "Modules",
            """
A module is a Python file containing reusable code. Python also includes a large standard library, and thousands of third-party packages are available through the Python ecosystem.

Modules allow large applications to be divided into manageable components.
            """,
            """import math

print(math.sqrt(144))"""
        ),

        lesson(
            "py-09",
            "Object-Oriented Python",
            """
Python supports object-oriented programming through classes and objects. A class can combine data and behavior into a reusable structure.

Object-oriented design becomes useful as applications become larger and contain many related entities.
            """,
            """class Student:
    def __init__(self, name):
        self.name = name

    def show(self):
        print(self.name)

student = Student("Joe")
student.show()"""
        )
    ]
),

# ============================================================
# 7. WEB
# ============================================================

course(
    "web-development",
    "Web Development",
    "🌐",
    "Beginner → Intermediate",
    "Learn how modern websites and web applications are built.",
    [

        lesson(
            "web-01",
            "HTML",
            """
HTML provides the structure of a web page. Elements describe headings, paragraphs, links, images, forms and other content.

HTML does not primarily control visual appearance or application logic. CSS handles presentation while JavaScript provides behavior.
            """,
            """<!DOCTYPE html>
<html>
<body>
    <h1>CodeQuest AI</h1>
    <p>Learn. Practice. Play. Build.</p>
</body>
</html>"""
        ),

        lesson(
            "web-02",
            "CSS",
            """
CSS controls the visual presentation of HTML. It can change colors, spacing, typography, layouts, animations and responsive behavior.

Modern websites often use CSS Grid and Flexbox to create layouts that adapt to different screen sizes.
            """,
            """.card {
    padding: 20px;
    border-radius: 16px;
}

.card h2 {
    margin-bottom: 10px;
}"""
        ),

        lesson(
            "web-03",
            "JavaScript",
            """
JavaScript adds behavior to web pages. It can respond to user actions, modify the page, communicate with servers and manage application state.

For example, CodeQuest AI uses JavaScript to open lessons, start quizzes and communicate with Flask API endpoints.
            """,
            """document
    .getElementById("quizBtn")
    .addEventListener("click", function() {
        console.log("Quiz started");
    });"""
        ),

        lesson(
            "web-04",
            "DOM",
            """
The Document Object Model represents the HTML page as a structure that JavaScript can access and modify.

This allows JavaScript to change text, attributes, classes and elements after the page has loaded.
            """,
            """const title = document.getElementById("title");
title.textContent = "CodeQuest AI";"""
        ),

        lesson(
            "web-05",
            "Fetch API",
            """
Web applications frequently need data from a backend server. JavaScript's fetch API can send HTTP requests and process responses.

This is how a frontend can request courses or quiz questions without completely reloading the page.
            """,
            """fetch("/api/quiz")
    .then(response => response.json())
    .then(data => {
        console.log(data.questions);
    });"""
        ),

        lesson(
            "web-06",
            "REST APIs",
            """
An API provides a defined way for software components to communicate. REST-style web APIs commonly use HTTP methods such as GET and POST.

A frontend might use GET to retrieve courses and POST to submit progress or source code.
            """,
            """GET  /api/courses
GET  /api/quiz
POST /api/progress/lesson
POST /api/compile"""
        )
    ]
),

# ============================================================
# 8. DBMS
# ============================================================

course(
    "dbms-sql",
    "DBMS & SQL",
    "🗄️",
    "Beginner → Intermediate",
    "Learn databases, SQL and application data management.",
    [

        lesson(
            "db-01",
            "What is a Database?",
            """
A database is an organized collection of data that can be stored, searched and updated efficiently. Applications use databases to persist information such as users, products, orders, messages and learning progress.

For CodeQuest AI, a database can store a student's completed lessons, XP and quiz history.
            """,
            """
users
----------------
uid | name | xp

progress
----------------
uid | lesson | completed
            """
        ),

        lesson(
            "db-02",
            "Tables",
            """
A relational database stores information in tables. A table consists of rows and columns. Each row normally represents one record, while each column represents a property of that record.
            """,
            """CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    mark INTEGER
);"""
        ),

        lesson(
            "db-03",
            "SELECT",
            """
The SELECT statement retrieves information from a database. Conditions can be added using WHERE, and results can be sorted using ORDER BY.

Querying data is one of the most common operations performed by application backends.
            """,
            """SELECT name, mark
FROM students
WHERE mark >= 50
ORDER BY mark DESC;"""
        ),

        lesson(
            "db-04",
            "INSERT UPDATE DELETE",
            """
Databases must support changes as well as reading data. INSERT adds records, UPDATE changes existing records, and DELETE removes records.

Applications normally validate input before performing these operations.
            """,
            """INSERT INTO students(name, mark)
VALUES ('Joe', 92);

UPDATE students
SET mark = 95
WHERE name = 'Joe';"""
        ),

        lesson(
            "db-05",
            "Primary Keys",
            """
A primary key uniquely identifies a row. Using a unique identifier prevents ambiguity when several records have similar names or other properties.

In real applications, IDs are often used to connect related tables.
            """,
            """CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE
);"""
        ),

        lesson(
            "db-06",
            "SQL Injection",
            """
SQL injection occurs when untrusted user input is incorrectly inserted into SQL statements. Attackers may manipulate the query so that it performs unintended operations.

Parameterized queries are an important defense because they separate SQL structure from user-provided values.
            """,
            """cursor.execute(
    "SELECT * FROM users WHERE email = ?",
    (email,)
)"""
        )
    ]
),

# ============================================================
# 9. DSA
# ============================================================

course(
    "dsa",
    "Data Structures & Algorithms",
    "🧩",
    "Intermediate",
    "Develop problem-solving skills and understand efficient algorithms.",
    [

        lesson(
            "dsa-01",
            "What is an Algorithm?",
            """
An algorithm is a finite sequence of steps used to solve a problem. Good algorithms are clear, correct and efficient.

For example, finding the largest number in an array can be solved by scanning every element and remembering the largest value encountered so far.
            """,
            """int max = numbers[0];

for (int i = 1; i < n; i++) {
    if (numbers[i] > max)
        max = numbers[i];
}"""
        ),

        lesson(
            "dsa-02",
            "Arrays",
            """
Arrays store elements in an ordered structure. They provide fast access by index, making them useful when positions are important.

The trade-off is that inserting or removing elements in the middle may require shifting other elements.
            """,
            """int numbers[] = {10, 20, 30, 40};

printf("%d", numbers[2]);"""
        ),

        lesson(
            "dsa-03",
            "Linked Lists",
            """
A linked list consists of nodes connected using references or pointers. Unlike arrays, linked-list nodes do not have to occupy consecutive memory locations.

Linked lists are useful for learning dynamic data structures and pointer-based relationships.
            """,
            """struct Node {
    int data;
    struct Node *next;
};"""
        ),

        lesson(
            "dsa-04",
            "Stacks",
            """
A stack follows the Last In, First Out principle. The most recently added element is removed first.

Stacks are used in function calls, undo operations, expression evaluation and many algorithms.
            """,
            """
push(10)
push(20)
pop() → 20
            """
        ),

        lesson(
            "dsa-05",
            "Queues",
            """
A queue generally follows the First In, First Out principle. The first item added is normally the first item removed.

Queues are useful for task scheduling, printer jobs, buffering and breadth-first search.
            """,
            """
enqueue(A)
enqueue(B)
dequeue() → A
            """
        ),

        lesson(
            "dsa-06",
            "Searching",
            """
Searching means finding a desired value in a collection. Linear search checks elements one by one, while binary search repeatedly divides a sorted search range.

Choosing the right algorithm can make a major difference as data size grows.
            """,
            """int low = 0;
int high = n - 1;

while (low <= high) {
    int mid = (low + high) / 2;
    ...
}"""
        ),

        lesson(
            "dsa-07",
            "Sorting",
            """
Sorting arranges data according to an ordering rule. Common algorithms include bubble sort, insertion sort, merge sort and quicksort.

Learning sorting algorithms teaches important ideas about comparisons, loops, recursion and algorithm efficiency.
            """,
            """for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < n - i - 1; j++) {
        if (a[j] > a[j + 1]) {
            int t = a[j];
            a[j] = a[j + 1];
            a[j + 1] = t;
        }
    }
}"""
        ),

        lesson(
            "dsa-08",
            "Big O",
            """
Big O notation describes how an algorithm's resource requirements grow as the input size increases. It helps developers reason about scalability.

For example, a single loop over n elements is commonly O(n), while a nested loop over n elements can be O(n²).
            """,
            """
One loop:
O(n)

Nested loops:
O(n²)

Binary search:
O(log n)
            """
        )
    ]
),

# ============================================================
# 10. OPERATING SYSTEM
# ============================================================

course(
    "operating-systems",
    "Operating Systems",
    "⚙️",
    "Intermediate",
    "Understand processes, memory, files and operating-system fundamentals.",
    [

        lesson(
            "os-01",
            "Processes",
            """
A process is a running instance of a program. When you open an application, the operating system creates and manages a process containing the program's execution state and resources.

Multiple processes can run at the same time, with the operating system coordinating CPU access.
            """,
            """
Program:
CodeQuest.exe

Running instance:
Process #4210
            """
        ),

        lesson(
            "os-02",
            "Threads",
            """
A thread is an execution path within a process. A process can contain multiple threads that share certain resources.

Multithreading can allow applications to perform independent tasks concurrently, although shared data must be managed carefully.
            """,
            """
Application
├── UI thread
├── Network thread
└── Worker thread
            """
        ),

        lesson(
            "os-03",
            "Memory Management",
            """
Operating systems manage memory so that processes can run without incorrectly interfering with each other. Concepts such as virtual memory allow applications to work with an address space that is managed by the operating system.

Memory management is closely connected to performance, security and process isolation.
            """,
            """
Application
↓
Virtual memory
↓
Physical RAM
            """
        ),

        lesson(
            "os-04",
            "File Systems",
            """
A file system defines how files and directories are organized and stored. Different operating systems can use different file-system technologies.

File systems maintain metadata such as names, locations, sizes and permissions.
            """,
            """
/home/student/projects/codequest/
            """
        )
    ]
),

# ============================================================
# 11. NETWORKS
# ============================================================

course(
    "networks",
    "Computer Networks",
    "🌍",
    "Intermediate",
    "Understand how computers communicate across networks and the Internet.",
    [

        lesson(
            "net-01",
            "What is a Network?",
            """
A computer network connects devices so they can exchange information and share resources. Networks range from small local networks to the global Internet.

Applications depend heavily on networking. Web browsing, messaging, cloud storage and multiplayer games all require communication between devices.
            """,
            """
Phone
  ↓
Wi-Fi Router
  ↓
Internet
  ↓
Server
            """
        ),

        lesson(
            "net-02",
            "IP Addresses",
            """
An IP address identifies a network interface using the addressing system of a particular IP version. IPv4 uses 32-bit addresses, while IPv6 uses much larger 128-bit addresses.

Devices and services use IP addressing so network packets can be delivered toward their destinations.
            """,
            """
IPv4 example:
192.168.1.10
            """
        ),

        lesson(
            "net-03",
            "DNS",
            """
Domain Name System translates human-friendly domain names into information such as IP addresses. Without DNS, users would frequently need to remember numerical addresses instead of names.

When you type a website address, your device may first need to resolve the domain before communicating with the server.
            """,
            """
codequest-ai-2gsx.onrender.com
          ↓ DNS
IP address
          ↓
Web server
            """
        ),

        lesson(
            "net-04",
            "HTTP and HTTPS",
            """
HTTP is an application-layer protocol used for transferring web resources. HTTPS uses HTTP over an encrypted TLS connection, helping protect data while it travels between the client and server.

Modern web applications should use HTTPS for authentication and other sensitive communication.
            """,
            """GET /api/courses HTTP/1.1
Host: example.com"""
        ),

        lesson(
            "net-05",
            "TCP and UDP",
            """
TCP provides a connection-oriented transport mechanism with reliability and ordered delivery. UDP is connectionless and has lower protocol overhead, making it useful in scenarios where speed or application-controlled delivery is important.

The choice depends on the requirements of the application.
            """,
            """
TCP:
Web connections
File transfer

UDP:
Some real-time applications
Streaming scenarios
            """
        )
    ]
),

# ============================================================
# 12. CYBERSECURITY
# ============================================================

course(
    "cybersecurity",
    "Cybersecurity",
    "🛡️",
    "Intermediate",
    "Learn defensive security fundamentals and secure development.",
    [

        lesson(
            "sec-01",
            "What is Cybersecurity?",
            """
Cybersecurity is the practice of protecting systems, networks, applications and information from unauthorized access, disruption, modification or destruction.

Security is not a single feature. It involves authentication, authorization, secure coding, monitoring, backups, updates and careful handling of sensitive information.
            """,
            """
User
 ↓ authentication
Application
 ↓ authorization
Database
            """
        ),

        lesson(
            "sec-02",
            "Authentication",
            """
Authentication answers the question: who are you? Common mechanisms include passwords, authentication applications, security keys and federated identity providers.

CodeQuest AI uses Google/Firebase Authentication so that the application does not need to manage users' Google passwords itself.
            """,
            """
Google Account
      ↓
Firebase Authentication
      ↓
CodeQuest AI
            """
        ),

        lesson(
            "sec-03",
            "Authorization",
            """
Authorization determines what an authenticated user is allowed to do. Authentication and authorization are different concepts.

For example, a student may be authenticated but still not have permission to access an administrator-only dashboard.
            """,
            """
Authenticated? YES

Role:
student

Allowed:
learn
quiz
progress

Not allowed:
admin settings
            """
        ),

        lesson(
            "sec-04",
            "Hashing",
            """
Hashing transforms input data into a fixed-size representation. Secure password systems normally use specialized password-hashing algorithms rather than storing plaintext passwords.

Hashing is different from encryption because a secure hash is designed to be one-way.
            """,
            """
password
   ↓
password-hashing algorithm
   ↓
stored password verifier
            """
        ),

        lesson(
            "sec-05",
            "Secure Input",
            """
Applications should treat external input as untrusted. Users can submit unexpected values, malicious strings or oversized data.

Validation, parameterized database queries, output encoding and safe API design help reduce common security risks.
            """,
            """
User input
   ↓
Validate
   ↓
Sanitize / safely encode
   ↓
Application
            """
        )
    ]
),

# ============================================================
# 13. AI / ML
# ============================================================

course(
    "ai-ml",
    "AI & Machine Learning",
    "🤖",
    "Intermediate",
    "Understand artificial intelligence and practical machine learning concepts.",
    [

        lesson(
            "ai-01",
            "What is AI?",
            """
Artificial intelligence is a broad field concerned with creating systems that perform tasks commonly associated with intelligent behavior, such as perception, language processing, reasoning and decision support.

AI systems can use rules, search algorithms, machine learning and other techniques depending on the problem.
            """,
            """
Input
 ↓
AI system
 ↓
Prediction / decision / generated result
            """
        ),

        lesson(
            "ai-02",
            "Machine Learning",
            """
Machine learning is a family of methods where models learn patterns from data rather than being explicitly programmed with every individual rule.

A model is trained using examples and then evaluated on data to determine how well it generalizes.
            """,
            """
Training data
      ↓
ML algorithm
      ↓
Model
      ↓
New input
      ↓
Prediction
            """
        ),

        lesson(
            "ai-03",
            "Supervised Learning",
            """
Supervised learning uses training examples that include target labels or values. Classification predicts categories, while regression predicts numerical values.

For example, a model might learn from examples of houses and their prices and then estimate the price of another house.
            """,
            """
Features:
area
rooms
location

Target:
price
            """
        ),

        lesson(
            "ai-04",
            "Neural Networks",
            """
Neural networks are computational models composed of connected units arranged in layers. During training, the model adjusts parameters so that its outputs become closer to desired results.

Neural networks are widely used in computer vision, language processing, speech and other machine-learning applications.
            """,
            """
Input layer
     ↓
Hidden layers
     ↓
Output layer
            """
        ),

        lesson(
            "ai-05",
            "Generative AI",
            """
Generative AI refers to systems that generate new content such as text, images, audio or code based on learned patterns and user instructions.

Large language models are one example. They process sequences of tokens and generate responses based on their learned representations and the provided context.
            """,
            """
Prompt
 ↓
AI model
 ↓
Generated response
            """
        )
    ]
),

# ============================================================
# 14. CLOUD
# ============================================================

course(
    "cloud",
    "Cloud Computing",
    "☁️",
    "Intermediate",
    "Learn how applications use remote computing infrastructure.",
    [

        lesson(
            "cloud-01",
            "What is Cloud Computing?",
            """
Cloud computing provides computing resources such as servers, storage, databases and networking through remote infrastructure. Instead of purchasing and maintaining every physical server yourself, you can use cloud services according to your needs.

A deployed Flask application running on Render is an example of an application hosted on remote infrastructure.
            """,
            """
Your browser
     ↓
Internet
     ↓
Cloud platform
     ↓
Flask application
            """
        ),

        lesson(
            "cloud-02",
            "IaaS PaaS SaaS",
            """
Cloud services are often described using models such as Infrastructure as a Service, Platform as a Service and Software as a Service.

IaaS provides infrastructure resources, PaaS provides an environment for deploying applications, and SaaS delivers complete software to end users.
            """,
            """
IaaS → virtual machines
PaaS → application deployment platform
SaaS → ready-to-use application
            """
        ),

        lesson(
            "cloud-03",
            "Deployment",
            """
Deployment means making an application available in an environment where users can access it. A typical deployment includes source code, dependencies, configuration, a process manager and networking.

Continuous deployment can automatically rebuild an application after changes are pushed to a repository.
            """,
            """
GitHub
 ↓
Build
 ↓
Install dependencies
 ↓
Start Gunicorn
 ↓
Live application
            """
        ),

        lesson(
            "cloud-04",
            "Environment Variables",
            """
Environment variables allow configuration values to be supplied outside the source code. They are useful for database locations, API credentials, secret keys and deployment-specific settings.

Sensitive credentials should not be committed directly into a public repository.
            """,
            """DATABASE_PATH=/var/data/codequest.db
SECRET_KEY=...
FIREBASE_SERVICE_ACCOUNT_JSON=..."""
        )
    ]
),

# ============================================================
# 15. DEVOPS
# ============================================================

course(
    "devops",
    "DevOps & Software Engineering",
    "🚀",
    "Intermediate",
    "Learn professional software development and deployment practices.",
    [

        lesson(
            "dev-01",
            "Software Development Lifecycle",
            """
Software development normally involves multiple stages such as requirements, design, implementation, testing, deployment and maintenance.

Understanding the lifecycle helps developers think beyond simply writing code. A production application must also be tested, monitored, documented and maintained.
            """,
            """
Requirement
 ↓
Design
 ↓
Code
 ↓
Test
 ↓
Deploy
 ↓
Maintain
            """
        ),

        lesson(
            "dev-02",
            "Testing",
            """
Testing checks whether software behaves as expected. Unit tests focus on small pieces of code, integration tests check interactions between components, and broader system tests examine complete workflows.

Testing is especially valuable when applications become large enough that manual checking is no longer sufficient.
            """,
            """
Input
 ↓
Function
 ↓
Expected result
       =
Actual result
            """
        ),

        lesson(
            "dev-03",
            "Debugging",
            """
Debugging is the process of finding and correcting defects in software. A good debugging process reproduces the problem, gathers evidence, identifies the likely cause, changes the code carefully and verifies the fix.

Reading error messages rather than guessing is one of the most useful habits for new programmers.
            """,
            """
Error
 ↓
Read traceback
 ↓
Locate line
 ↓
Understand cause
 ↓
Fix
 ↓
Test again
            """
        ),

        lesson(
            "dev-04",
            "CI/CD",
            """
Continuous Integration and Continuous Delivery or Deployment automate parts of the software delivery process. Developers push changes, automated systems build and test the project, and successful changes can be deployed.

GitHub Actions is one example of a CI/CD platform.
            """,
            """
git push
   ↓
GitHub Actions
   ↓
Build + Test
   ↓
Deploy
            """
        ),

        lesson(
            "dev-05",
            "Logging",
            """
Logs provide information about what an application is doing. Useful logs help developers diagnose errors, performance problems and unexpected behavior.

Production applications should avoid logging passwords, private keys and other sensitive information.
            """,
            """print("Quiz API requested")

# Production applications
# should use structured logging.
            """
        )
    ]
),

# ============================================================
# 16. CAREER
# ============================================================

course(
    "career",
    "Career & Interview Preparation",
    "🎯",
    "All Levels",
    "Turn your technical knowledge into projects, portfolios and job readiness.",
    [

        lesson(
            "career-01",
            "Choosing a Development Path",
            """
There are many technology career paths. A student can explore frontend development, backend development, mobile development, data engineering, cybersecurity, cloud engineering, AI/ML and other areas.

You do not need to master every field simultaneously. A strong approach is to learn fundamentals first, then choose a direction and build increasingly realistic projects.
            """,
            """
Fundamentals
 ↓
Choose direction
 ↓
Learn tools
 ↓
Build projects
 ↓
Portfolio
 ↓
Internship / Job
            """
        ),

        lesson(
            "career-02",
            "Building Projects",
            """
Projects demonstrate that you can apply knowledge to solve problems. A good student project should have a clear problem, understandable users, useful features and evidence that the software actually works.

CodeQuest AI itself can become a portfolio project because it combines frontend development, backend APIs, authentication, databases, deployment and programming education.
            """,
            """
Problem
 ↓
Design
 ↓
Implementation
 ↓
Testing
 ↓
Deployment
 ↓
Documentation
            """
        ),

        lesson(
            "career-03",
            "GitHub Portfolio",
            """
A GitHub portfolio can show source code, project history, documentation and technical interests. A good README should explain the problem, features, technologies, setup process and screenshots or demonstrations where appropriate.

Quality matters more than simply having a large number of repositories.
            """,
            """
README
├── Project overview
├── Features
├── Technologies
├── Installation
├── Screenshots
└── Future improvements
            """
        ),

        lesson(
            "career-04",
            "Resume Projects",
            """
A technical resume should describe projects using concrete contributions rather than vague claims. Mention the technology used, what you built and what problem the project addresses.

For example, instead of simply writing 'Made a website', describe the application's major functionality and technology stack.
            """,
            """
Weak:
"Made a coding website."

Better:
"Developed a gamified CS learning platform using Flask,
JavaScript, Firebase Authentication and SQLite."
            """
        ),

        lesson(
            "career-05",
            "Technical Interviews",
            """
Technical interviews may evaluate programming fundamentals, data structures, algorithms, databases, operating systems, networking and problem-solving depending on the role.

Interview preparation should combine conceptual understanding with practice problems and the ability to explain your reasoning clearly.
            """,
            """
Question
 ↓
Understand requirements
 ↓
Explain approach
 ↓
Write solution
 ↓
Test edge cases
 ↓
Discuss complexity
            """
        )
    ]
)

]


# ============================================================
# QUIZ BANK
# ============================================================

quiz_questions = [

    # Computer basics
    {
        "id": "q001",
        "topic": "Computer Basics",
        "question": "Which component executes program instructions?",
        "options": ["CPU", "Monitor", "Keyboard", "Printer"],
        "answer": "CPU"
    },
    {
        "id": "q002",
        "topic": "Computer Basics",
        "question": "Which memory is normally volatile?",
        "options": ["RAM", "SSD", "HDD", "DVD"],
        "answer": "RAM"
    },
    {
        "id": "q003",
        "topic": "Computer Basics",
        "question": "Which device is primarily an input device?",
        "options": ["Keyboard", "Monitor", "Speaker", "Projector"],
        "answer": "Keyboard"
    },
    {
        "id": "q004",
        "topic": "Computer Basics",
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Computer Program Utility",
            "Central Program User",
            "Computer Processing Utility"
        ],
        "answer": "Central Processing Unit"
    },
    {
        "id": "q005",
        "topic": "Computer Basics",
        "question": "Which device provides persistent storage?",
        "options": ["SSD", "RAM", "CPU register", "Cache only"],
        "answer": "SSD"
    },

    # C
    {
        "id": "q006",
        "topic": "C Programming",
        "question": "Where does a normal C program begin execution?",
        "options": ["main()", "start()", "run()", "begin()"],
        "answer": "main()"
    },
    {
        "id": "q007",
        "topic": "C Programming",
        "question": "Which symbol ends a normal C statement?",
        "options": [";", ":", ".", ","],
        "answer": ";"
    },
    {
        "id": "q008",
        "topic": "C Programming",
        "question": "Which type stores an integer in C?",
        "options": ["int", "char", "float[]", "string"],
        "answer": "int"
    },
    {
        "id": "q009",
        "topic": "C Programming",
        "question": "Which keyword is used for a loop that commonly has initialization, condition and update?",
        "options": ["for", "if", "switch", "return"],
        "answer": "for"
    },
    {
        "id": "q010",
        "topic": "C Programming",
        "question": "Which operator obtains the address of a variable?",
        "options": ["&", "*", "#", "%"],
        "answer": "&"
    },

    # Python
    {
        "id": "q011",
        "topic": "Python",
        "question": "Which function displays output in Python?",
        "options": ["print()", "show()", "displayText()", "output()"],
        "answer": "print()"
    },
    {
        "id": "q012",
        "topic": "Python",
        "question": "Which keyword defines a function in Python?",
        "options": ["def", "function", "func", "define"],
        "answer": "def"
    },
    {
        "id": "q013",
        "topic": "Python",
        "question": "Which Python structure stores key-value pairs?",
        "options": ["Dictionary", "Tuple only", "Character", "Boolean"],
        "answer": "Dictionary"
    },
    {
        "id": "q014",
        "topic": "Python",
        "question": "Which block is used to handle exceptions?",
        "options": ["try/except", "if/else only", "loop/end", "catch/error"],
        "answer": "try/except"
    },

    # Web
    {
        "id": "q015",
        "topic": "Web Development",
        "question": "Which language provides the structure of a web page?",
        "options": ["HTML", "CSS", "SQL", "C"],
        "answer": "HTML"
    },
    {
        "id": "q016",
        "topic": "Web Development",
        "question": "Which language primarily controls web page styling?",
        "options": ["CSS", "HTML", "SQL", "Python"],
        "answer": "CSS"
    },
    {
        "id": "q017",
        "topic": "Web Development",
        "question": "Which language adds behavior to web pages?",
        "options": ["JavaScript", "HTML", "CSS", "SQL"],
        "answer": "JavaScript"
    },
    {
        "id": "q018",
        "topic": "Web Development",
        "question": "Which JavaScript API is commonly used to make HTTP requests?",
        "options": ["fetch()", "print()", "scan()", "requestSQL()"],
        "answer": "fetch()"
    },

    # DBMS
    {
        "id": "q019",
        "topic": "DBMS",
        "question": "Which SQL command retrieves data?",
        "options": ["SELECT", "GETDATA", "READ", "FETCHSQL"],
        "answer": "SELECT"
    },
    {
        "id": "q020",
        "topic": "DBMS",
        "question": "Which SQL command adds a row?",
        "options": ["INSERT", "ADDROW", "CREATE", "APPENDSQL"],
        "answer": "INSERT"
    },
    {
        "id": "q021",
        "topic": "DBMS",
        "question": "What uniquely identifies a row in a relational table?",
        "options": ["Primary key", "Folder", "CSS class", "Loop"],
        "answer": "Primary key"
    },

    # DSA
    {
        "id": "q022",
        "topic": "DSA",
        "question": "Which data structure follows LIFO?",
        "options": ["Stack", "Queue", "Tree only", "Graph"],
        "answer": "Stack"
    },
    {
        "id": "q023",
        "topic": "DSA",
        "question": "Which data structure normally follows FIFO?",
        "options": ["Queue", "Stack", "Heap only", "Array only"],
        "answer": "Queue"
    },
    {
        "id": "q024",
        "topic": "DSA",
        "question": "What is the typical complexity of binary search on sorted data?",
        "options": ["O(log n)", "O(n²)", "O(n³)", "O(2n)"],
        "answer": "O(log n)"
    },
    {
        "id": "q025",
        "topic": "DSA",
        "question": "What does Big O help describe?",
        "options": [
            "Growth of resource requirements",
            "Screen resolution",
            "Programming language age",
            "File extension"
        ],
        "answer": "Growth of resource requirements"
    },

    # OS
    {
        "id": "q026",
        "topic": "Operating Systems",
        "question": "What is a running instance of a program called?",
        "options": ["Process", "Folder", "Compiler", "Packet"],
        "answer": "Process"
    },
    {
        "id": "q027",
        "topic": "Operating Systems",
        "question": "What manages hardware resources and provides services to applications?",
        "options": ["Operating system", "Text editor", "Browser tab", "Image file"],
        "answer": "Operating system"
    },

    # Networks
    {
        "id": "q028",
        "topic": "Networks",
        "question": "What does DNS help translate?",
        "options": [
            "Domain names into network information",
            "Python into C",
            "Images into HTML",
            "RAM into storage"
        ],
        "answer": "Domain names into network information"
    },
    {
        "id": "q029",
        "topic": "Networks",
        "question": "Which protocol is used to secure HTTP communication?",
        "options": ["HTTPS", "FTP", "SMTP", "ARP only"],
        "answer": "HTTPS"
    },
    {
        "id": "q030",
        "topic": "Networks",
        "question": "Which transport protocol provides ordered reliable delivery?",
        "options": ["TCP", "UDP", "DNS", "HTTP"],
        "answer": "TCP"
    },

    # Security
    {
        "id": "q031",
        "topic": "Cybersecurity",
        "question": "Authentication primarily answers which question?",
        "options": [
            "Who are you?",
            "What color is the UI?",
            "How fast is the CPU?",
            "Where is the monitor?"
        ],
        "answer": "Who are you?"
    },
    {
        "id": "q032",
        "topic": "Cybersecurity",
        "question": "Authorization determines what an authenticated user can do.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": "q033",
        "topic": "Cybersecurity",
        "question": "What should applications generally treat external user input as?",
        "options": ["Untrusted", "Always safe", "Trusted code", "System configuration"],
        "answer": "Untrusted"
    },

    # AI
    {
        "id": "q034",
        "topic": "AI",
        "question": "What does ML commonly learn from?",
        "options": ["Data", "Only monitors", "Keyboard drivers", "CSS files"],
        "answer": "Data"
    },
    {
        "id": "q035",
        "topic": "AI",
        "question": "What does supervised learning use during training?",
        "options": ["Labeled examples", "No data", "Only passwords", "Only network packets"],
        "answer": "Labeled examples"
    },
    {
        "id": "q036",
        "topic": "AI",
        "question": "What can generative AI produce?",
        "options": [
            "New content",
            "Only electricity",
            "Only IP addresses",
            "Only database tables"
        ],
        "answer": "New content"
    },

    # Cloud
    {
        "id": "q037",
        "topic": "Cloud",
        "question": "What does cloud computing provide?",
        "options": [
            "Remote computing resources",
            "Only local storage",
            "Only keyboard input",
            "Only desktop wallpapers"
        ],
        "answer": "Remote computing resources"
    },
    {
        "id": "q038",
        "topic": "Cloud",
        "question": "Why are environment variables useful?",
        "options": [
            "They separate configuration from source code",
            "They replace CPUs",
            "They create monitors",
            "They compile C automatically"
        ],
        "answer": "They separate configuration from source code"
    },

    # Git
    {
        "id": "q039",
        "topic": "Git",
        "question": "What does Git primarily track?",
        "options": ["Changes to files", "Internet speed", "CPU temperature", "Screen brightness"],
        "answer": "Changes to files"
    },
    {
        "id": "q040",
        "topic": "Git",
        "question": "Which command creates a commit?",
        "options": [
            "git commit",
            "git save",
            "git snapshot-now",
            "git version"
        ],
        "answer": "git commit"
    },

    # Mixed
    {
        "id": "q041",
        "topic": "Programming",
        "question": "What is a function used for?",
        "options": [
            "Reusable logic",
            "Only storing images",
            "Changing hardware",
            "Creating an IP address"
        ],
        "answer": "Reusable logic"
    },
    {
        "id": "q042",
        "topic": "Programming",
        "question": "What is debugging?",
        "options": [
            "Finding and fixing software defects",
            "Installing a monitor",
            "Creating a database only",
            "Changing a keyboard"
        ],
        "answer": "Finding and fixing software defects"
    },
    {
        "id": "q043",
        "topic": "Programming",
        "question": "What is an algorithm?",
        "options": [
            "A sequence of steps for solving a problem",
            "A physical CPU",
            "A file extension",
            "A monitor setting"
        ],
        "answer": "A sequence of steps for solving a problem"
    },
    {
        "id": "q044",
        "topic": "Software Engineering",
        "question": "Why is testing important?",
        "options": [
            "It helps verify expected behavior",
            "It increases monitor size",
            "It replaces databases",
            "It removes all programming languages"
        ],
        "answer": "It helps verify expected behavior"
    },
    {
        "id": "q045",
        "topic": "Software Engineering",
        "question": "What does CI commonly stand for?",
        "options": [
            "Continuous Integration",
            "Computer Installation",
            "Code Internet",
            "Central Interface"
        ],
        "answer": "Continuous Integration"
    }
]


# ============================================================
# CAREER DATA
# ============================================================

careers = [
    {
        "id": "software-developer",
        "title": "Software Developer",
        "icon": "💻",
        "description": "Build applications, services and software products.",
        "skills": [
            "Programming",
            "Data Structures",
            "Git",
            "Databases",
            "APIs",
            "Testing"
        ],
        "roadmap": [
            "Programming fundamentals",
            "Git & GitHub",
            "Data structures",
            "Databases",
            "Web/backend development",
            "Projects",
            "Interview preparation"
        ]
    },
    {
        "id": "web-developer",
        "title": "Web Developer",
        "icon": "🌐",
        "description": "Build websites and full-stack web applications.",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "Frontend frameworks",
            "Backend",
            "Databases"
        ],
        "roadmap": [
            "HTML",
            "CSS",
            "JavaScript",
            "APIs",
            "Backend",
            "Database",
            "Deployment"
        ]
    },
    {
        "id": "python-developer",
        "title": "Python Developer",
        "icon": "🐍",
        "description": "Build automation, backend and data-driven applications.",
        "skills": [
            "Python",
            "OOP",
            "APIs",
            "SQL",
            "Git",
            "Testing"
        ],
        "roadmap": [
            "Python basics",
            "OOP",
            "Data structures",
            "SQL",
            "Web frameworks",
            "Projects",
            "Deployment"
        ]
    },
    {
        "id": "cybersecurity",
        "title": "Cybersecurity",
        "icon": "🛡️",
        "description": "Learn to identify and defend against security threats.",
        "skills": [
            "Networking",
            "Linux",
            "Security fundamentals",
            "Authentication",
            "Web security",
            "Monitoring"
        ],
        "roadmap": [
            "Computer fundamentals",
            "Networking",
            "Linux",
            "Security basics",
            "Web security",
            "Labs",
            "Certifications / projects"
        ]
    },
    {
        "id": "ai-ml",
        "title": "AI / ML Engineer",
        "icon": "🤖",
        "description": "Build data-driven and intelligent applications.",
        "skills": [
            "Python",
            "Math",
            "Statistics",
            "Machine Learning",
            "Data Processing",
            "Model Evaluation"
        ],
        "roadmap": [
            "Python",
            "Mathematics",
            "Statistics",
            "Data processing",
            "Machine learning",
            "Deep learning",
            "AI projects"
        ]
    },
    {
        "id": "cloud-devops",
        "title": "Cloud / DevOps",
        "icon": "☁️",
        "description": "Build, deploy and operate reliable applications.",
        "skills": [
            "Linux",
            "Networking",
            "Cloud",
            "Docker",
            "CI/CD",
            "Monitoring"
        ],
        "roadmap": [
            "Linux",
            "Networking",
            "Git",
            "Cloud basics",
            "Containers",
            "CI/CD",
            "Projects"
        ]
    }
]


# ============================================================
# ACHIEVEMENTS
# ============================================================

achievements = [
    {
        "id": "first-lesson",
        "title": "First Step",
        "description": "Complete your first lesson.",
        "icon": "🚀"
    },
    {
        "id": "five-lessons",
        "title": "Getting Started",
        "description": "Complete five lessons.",
        "icon": "🔥"
    },
    {
        "id": "ten-lessons",
        "title": "Knowledge Builder",
        "description": "Complete ten lessons.",
        "icon": "🧠"
    },
    {
        "id": "quiz-complete",
        "title": "Quiz Warrior",
        "description": "Complete a quiz.",
        "icon": "🏆"
    },
    {
        "id": "perfect-quiz",
        "title": "Perfect Score",
        "description": "Get every question correct.",
        "icon": "💎"
    },
    {
        "id": "hundred-xp",
        "title": "XP Hunter",
        "description": "Earn 100 XP.",
        "icon": "⚡"
    }
]


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def calculate_level(xp):
    if xp < 100:
        return 1
    if xp < 250:
        return 2
    if xp < 500:
        return 3
    if xp < 850:
        return 4
    if xp < 1300:
        return 5
    if xp < 2000:
        return 6
    return 7


def level_name(level):
    names = {
        1: "Code Explorer",
        2: "Bug Hunter",
        3: "Logic Builder",
        4: "Code Warrior",
        5: "System Architect",
        6: "Tech Master",
        7: "CodeQuest Legend"
    }

    return names.get(level, "Code Explorer")


def all_lessons():
    result = []

    for c in courses:
        for chapter in c["chapters"]:
            item = dict(chapter)
            item["course_id"] = c["id"]
            item["course_title"] = c["title"]
            result.append(item)

    return result


def find_lesson(lesson_id):
    for item in all_lessons():
        if item["id"] == lesson_id:
            return item

    return None


def find_course(course_id):
    for c in courses:
        if c["id"] == course_id:
            return c

    return None


def get_uid_from_request():
    """
    Gets a Firebase UID from:
    Authorization: Bearer <Firebase ID token>

    If Firebase Admin is configured, token is verified.
    """

    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1].strip()

    if not token:
        return None

    if not firebase_ready:
        return None

    try:
        decoded = firebase_auth.verify_id_token(token)
        return decoded.get("uid")

    except Exception as error:
        print("Firebase token verification failed:", error)
        return None


def get_optional_uid():
    return get_uid_from_request()


def ensure_user(uid, name="", email="", photo_url=""):
    if not uid:
        return

    db = get_db()

    existing = db.execute(
        "SELECT uid FROM users WHERE uid = ?",
        (uid,)
    ).fetchone()

    if existing:
        db.execute(
            """
            UPDATE users
            SET name = ?,
                email = ?,
                photo_url = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE uid = ?
            """,
            (name, email, photo_url, uid)
        )
    else:
        db.execute(
            """
            INSERT INTO users
            (uid, name, email, photo_url)
            VALUES (?, ?, ?, ?)
            """,
            (uid, name, email, photo_url)
        )

    db.commit()
    db.close()


def add_xp(uid, amount, activity="activity"):
    if not uid:
        return

    db = get_db()

    user = db.execute(
        "SELECT xp FROM users WHERE uid = ?",
        (uid,)
    ).fetchone()

    if not user:
        ensure_user(uid)
        current_xp = 0
    else:
        current_xp = user["xp"]

    new_xp = max(0, current_xp + int(amount))
    new_level = calculate_level(new_xp)

    db.execute(
        """
        UPDATE users
        SET xp = ?,
            level = ?,
            last_activity = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP
        WHERE uid = ?
        """,
        (new_xp, new_level, uid)
    )

    db.execute(
        """
        INSERT INTO activity_log(uid, activity, xp)
        VALUES (?, ?, ?)
        """,
        (uid, activity, amount)
    )

    db.commit()
    db.close()


# ============================================================
# FRONTEND
# ============================================================

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception:
        return """
        <h1>CodeQuest AI</h1>
        <p>Backend is running.</p>
        <p>Place index.html inside the templates folder.</p>
        """


# ============================================================
# HEALTH
# ============================================================

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "app": "CodeQuest AI",
        "version": "1.0",
        "courses": len(courses),
        "lessons": len(all_lessons()),
        "quiz_questions": len(quiz_questions),
        "firebase_admin": firebase_ready,
        "compiler": "wandbox",
        "compiler_endpoint": "https://wandbox.org/api/compile.json"
    })


# ============================================================
# COURSES
# ============================================================

@app.route("/api/courses")
def api_courses():
    output = []

    for c in courses:
        output.append({
            "id": c["id"],
            "title": c["title"],
            "icon": c["icon"],
            "level": c["level"],
            "description": c["description"],
            "chapters": [
                {
                    "id": chapter["id"],
                    "title": chapter["title"],
                    "lesson": chapter["lesson"],
                    "sample": chapter["sample"],
                    "key_points": chapter.get("key_points", [])
                }
                for chapter in c["chapters"]
            ]
        })

    return jsonify({
        "courses": output,
        "total_courses": len(output),
        "total_lessons": len(all_lessons())
    })


@app.route("/api/course/<course_id>")
def api_course(course_id):
    selected = find_course(course_id)

    if not selected:
        return jsonify({
            "error": "Course not found"
        }), 404

    return jsonify(selected)


@app.route("/api/lesson/<lesson_id>")
def api_lesson(lesson_id):
    selected = find_lesson(lesson_id)

    if not selected:
        return jsonify({
            "error": "Lesson not found"
        }), 404

    return jsonify(selected)


# ============================================================
# FIREBASE LOGIN
# ============================================================

@app.route("/api/firebase-login", methods=["POST"])
def firebase_login():

    if not firebase_ready:
        return jsonify({
            "success": False,
            "error": "Firebase Admin is not configured on the server.",
            "setup_required": True
        }), 503

    data = request.get_json(silent=True) or {}

    id_token = data.get("idToken")

    if not id_token:
        auth_header = request.headers.get("Authorization", "")

        if auth_header.startswith("Bearer "):
            id_token = auth_header.split(" ", 1)[1].strip()

    if not id_token:
        return jsonify({
            "success": False,
            "error": "Firebase ID token is missing."
        }), 401

    try:
        decoded = firebase_auth.verify_id_token(id_token)

        uid = decoded.get("uid")
        name = decoded.get("name", "")
        email = decoded.get("email", "")
        picture = decoded.get("picture", "")

        ensure_user(
            uid,
            name,
            email,
            picture
        )

        return jsonify({
            "success": True,
            "uid": uid,
            "name": name,
            "email": email,
            "photo_url": picture
        })

    except Exception as error:
        print("Firebase login error:", error)

        return jsonify({
            "success": False,
            "error": "Invalid or expired Firebase login token."
        }), 401


@app.route("/api/me")
def api_me():

    uid = get_optional_uid()

    if not uid:
        return jsonify({
            "authenticated": False
        })

    db = get_db()

    user = db.execute(
        "SELECT * FROM users WHERE uid = ?",
        (uid,)
    ).fetchone()

    db.close()

    if not user:
        return jsonify({
            "authenticated": True,
            "uid": uid
        })

    return jsonify({
        "authenticated": True,
        "user": dict(user),
        "level_name": level_name(user["level"])
    })


# ============================================================
# STATS
# ============================================================

@app.route("/api/stats")
def api_stats():

    uid = get_optional_uid()

    if not uid:
        return jsonify({
            "authenticated": False,
            "xp": 0,
            "level": 1,
            "level_name": "Code Explorer",
            "streak": 0,
            "completed": 0
        })

    db = get_db()

    user = db.execute(
        "SELECT * FROM users WHERE uid = ?",
        (uid,)
    ).fetchone()

    completed = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM progress
        WHERE uid = ? AND completed = 1
        """,
        (uid,)
    ).fetchone()["count"]

    db.close()

    if not user:
        return jsonify({
            "authenticated": True,
            "xp": 0,
            "level": 1,
            "level_name": "Code Explorer",
            "streak": 0,
            "completed": completed
        })

    return jsonify({
        "authenticated": True,
        "xp": user["xp"],
        "level": user["level"],
        "level_name": level_name(user["level"]),
        "streak": user["streak"],
        "completed": completed
    })


# ============================================================
# PROGRESS
# ============================================================

@app.route("/api/progress", methods=["GET"])
def get_progress():

    uid = get_optional_uid()

    if not uid:
        return jsonify({
            "authenticated": False,
            "completed": []
        })

    db = get_db()

    rows = db.execute(
        """
        SELECT lesson_id, course_id, completed, completed_at
        FROM progress
        WHERE uid = ?
        ORDER BY completed_at DESC
        """,
        (uid,)
    ).fetchall()

    db.close()

    return jsonify({
        "authenticated": True,
        "completed": [dict(row) for row in rows]
    })


@app.route("/api/progress/lesson", methods=["POST"])
def complete_lesson():

    uid = get_optional_uid()

    if not uid:
        return jsonify({
            "success": False,
            "error": "Login required."
        }), 401

    data = request.get_json(silent=True) or {}

    lesson_id = data.get("lesson_id")
    course_id = data.get("course_id")

    if not lesson_id:
        return jsonify({
            "success": False,
            "error": "lesson_id is required."
        }), 400

    selected = find_lesson(lesson_id)

    if not selected:
        return jsonify({
            "success": False,
            "error": "Lesson not found."
        }), 404

    if not course_id:
        course_id = selected["course_id"]

    db = get_db()

    existing = db.execute(
        """
        SELECT completed
        FROM progress
        WHERE uid = ? AND lesson_id = ?
        """,
        (uid, lesson_id)
    ).fetchone()

    already_completed = bool(
        existing and existing["completed"] == 1
    )

    if not already_completed:

        db.execute(
            """
            INSERT INTO progress
            (uid, lesson_id, course_id, completed, completed_at)
            VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)
            ON CONFLICT(uid, lesson_id)
            DO UPDATE SET
                completed = 1,
                completed_at = CURRENT_TIMESTAMP
            """,
            (uid, lesson_id, course_id)
        )

        db.commit()
        db.close()

        add_xp(
            uid,
            20,
            "lesson-completed"
        )

        return jsonify({
            "success": True,
            "already_completed": False,
            "xp_earned": 20
        })

    db.close()

    return jsonify({
        "success": True,
        "already_completed": True,
        "xp_earned": 0
    })


# ============================================================
# QUIZ
# ============================================================

@app.route("/api/quiz")
def api_quiz():

    # Return the complete bank.
    # Frontend can randomly choose questions.
    return jsonify({
        "success": True,
        "questions": quiz_questions,
        "total": len(quiz_questions)
    })


@app.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():

    uid = get_optional_uid()

    if not uid:
        return jsonify({
            "success": False,
            "error": "Login required."
        }), 401

    data = request.get_json(silent=True) or {}

    score = int(data.get("score", 0))
    total = int(data.get("total", 0))

    if total <= 0:
        return jsonify({
            "success": False,
            "error": "Invalid quiz total."
        }), 400

    score = max(0, min(score, total))

    # XP:
    # 10 per correct answer
    # +25 completion bonus
    # +50 perfect bonus
    xp_earned = (score * 10) + 25

    if score == total:
        xp_earned += 50

    db = get_db()

    db.execute(
        """
        INSERT INTO quiz_attempts
        (uid, score, total, xp_earned)
        VALUES (?, ?, ?, ?)
        """,
        (uid, score, total, xp_earned)
    )

    db.commit()
    db.close()

    add_xp(
        uid,
        xp_earned,
        "quiz-completed"
    )

    return jsonify({
        "success": True,
        "score": score,
        "total": total,
        "xp_earned": xp_earned,
        "perfect": score == total
    })


@app.route("/api/quiz/violation", methods=["POST"])
def quiz_violation():

    uid = get_optional_uid()

    if uid:
        db = get_db()

        db.execute(
            """
            INSERT INTO activity_log
            (uid, activity, xp)
            VALUES (?, ?, 0)
            """,
            (uid, "quiz-violation")
        )

        db.commit()
        db.close()

    return jsonify({
        "success": True
    })


# ============================================================
# ACHIEVEMENTS
# ============================================================

@app.route("/api/achievements")
def api_achievements():

    uid = get_optional_uid()

    completed_count = 0
    xp = 0

    if uid:
        db = get_db()

        completed_count = db.execute(
            """
            SELECT COUNT(*) AS count
            FROM progress
            WHERE uid = ? AND completed = 1
            """,
            (uid,)
        ).fetchone()["count"]

        user = db.execute(
            "SELECT xp FROM users WHERE uid = ?",
            (uid,)
        ).fetchone()

        if user:
            xp = user["xp"]

        db.close()

    result = []

    for achievement in achievements:

        unlocked = False

        if achievement["id"] == "first-lesson":
            unlocked = completed_count >= 1

        elif achievement["id"] == "five-lessons":
            unlocked = completed_count >= 5

        elif achievement["id"] == "ten-lessons":
            unlocked = completed_count >= 10

        elif achievement["id"] == "hundred-xp":
            unlocked = xp >= 100

        result.append({
            **achievement,
            "unlocked": unlocked
        })

    return jsonify({
        "achievements": result
    })


# ============================================================
# CAREER GUIDE
# ============================================================

@app.route("/api/careers")
def api_careers():
    return jsonify({
        "careers": careers
    })


@app.route("/api/career-roadmap/<career_id>")
def career_roadmap(career_id):

    for career in careers:
        if career["id"] == career_id:
            return jsonify(career)

    return jsonify({
        "error": "Career not found"
    }), 404


# ============================================================
# PROJECTS
# ============================================================

projects = [
    {
        "id": "calculator",
        "title": "Smart Calculator",
        "level": "Beginner",
        "description": "Build a calculator and practice conditions and functions.",
        "technologies": ["HTML", "CSS", "JavaScript"]
    },
    {
        "id": "student-manager",
        "title": "Student Management System",
        "level": "Beginner → Intermediate",
        "description": "Manage student records using a database.",
        "technologies": ["Python", "Flask", "SQLite"]
    },
    {
        "id": "quiz-app",
        "title": "Quiz Application",
        "level": "Intermediate",
        "description": "Build a question bank, scoring system and progress tracker.",
        "technologies": ["JavaScript", "Flask", "SQLite"]
    },
    {
        "id": "codequest",
        "title": "CodeQuest AI",
        "level": "Advanced Student Project",
        "description": "Gamified computer-science learning platform.",
        "technologies": [
            "HTML",
            "CSS",
            "JavaScript",
            "Flask",
            "Firebase",
            "SQLite",
            "Cloud Deployment"
        ]
    }
]


@app.route("/api/projects")
def api_projects():
    return jsonify({
        "projects": projects
    })


# ============================================================
# ACTIVITY
# ============================================================

@app.route("/api/activity")
def api_activity():

    uid = get_optional_uid()

    if not uid:
        return jsonify({
            "activities": []
        })

    db = get_db()

    rows = db.execute(
        """
        SELECT activity, xp, created_at
        FROM activity_log
        WHERE uid = ?
        ORDER BY id DESC
        LIMIT 30
        """,
        (uid,)
    ).fetchall()

    db.close()

    return jsonify({
        "activities": [dict(row) for row in rows]
    })


# ============================================================
# C COMPILER
# ============================================================

WANDBOX_URL = "https://wandbox.org/api/compile.json"


def compile_with_wandbox(code, stdin=""):

    payload = {
        "compiler": "gcc-head-c",
        "code": code,
        "stdin": stdin or "",
        "save": False
    }

    encoded = json.dumps(payload).encode("utf-8")

    http_request = urllib.request.Request(
        WANDBOX_URL,
        data=encoded,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "CodeQuest-AI/1.0"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            http_request,
            timeout=25
        ) as response:

            raw = response.read().decode("utf-8")
            return json.loads(raw)

    except urllib.error.HTTPError as error:

        try:
            body = error.read().decode("utf-8")
        except Exception:
            body = ""

        return {
            "error": f"Compiler service HTTP error {error.code}",
            "details": body
        }

    except urllib.error.URLError as error:

        return {
            "error": "Unable to reach the compiler service.",
            "details": str(error)
        }

    except Exception as error:

        return {
            "error": "Compiler service error.",
            "details": str(error)
        }


@app.route("/api/compile", methods=["POST"])
def api_compile():

    data = request.get_json(silent=True) or {}

    code = data.get("code", "")
    stdin = data.get("stdin", "")

    if not isinstance(code, str):
        return jsonify({
            "success": False,
            "error": "Invalid code."
        }), 400

    if len(code) > 50000:
        return jsonify({
            "success": False,
            "error": "Code is too large. Maximum size is 50 KB."
        }), 413

    if not code.strip():
        return jsonify({
            "success": False,
            "error": "Please enter some C code."
        }), 400

    result = compile_with_wandbox(
        code,
        stdin
    )

    if "error" in result and "status" not in result:
        return jsonify({
            "success": False,
            "output": "",
            "error": result.get("error"),
            "details": result.get("details", "")
        }), 502

    compiler_message = result.get(
        "compiler_message",
        ""
    )

    program_message = result.get(
        "program_message",
        ""
    )

    status = result.get(
        "status",
        ""
    )

    signal = result.get(
        "signal",
        ""
    )

    # Wandbox normally provides compiler_message for
    # compilation errors and program_message for program output.
    if compiler_message.strip():

        return jsonify({
            "success": False,
            "output": program_message,
            "error": compiler_message,
            "compiler_message": compiler_message,
            "program_message": program_message,
            "status": status,
            "signal": signal
        })

    return jsonify({
        "success": True,
        "output": program_message,
        "error": "",
        "compiler_message": "",
        "program_message": program_message,
        "status": status,
        "signal": signal
    })


# ============================================================
# ROADMAP
# ============================================================

@app.route("/api/roadmap")
def roadmap():

    stages = [
        {
            "stage": 1,
            "title": "Computer Foundations",
            "courses": [
                "Computer Basics",
                "Digital Productivity"
            ]
        },
        {
            "stage": 2,
            "title": "Programming Foundations",
            "courses": [
                "C Programming",
                "C++ Programming",
                "Python Programming"
            ]
        },
        {
            "stage": 3,
            "title": "Development",
            "courses": [
                "Web Development",
                "DBMS & SQL",
                "Git & GitHub"
            ]
        },
        {
            "stage": 4,
            "title": "Computer Science Core",
            "courses": [
                "Data Structures & Algorithms",
                "Operating Systems",
                "Computer Networks"
            ]
        },
        {
            "stage": 5,
            "title": "Modern Technology",
            "courses": [
                "Cybersecurity",
                "AI & Machine Learning",
                "Cloud Computing",
                "DevOps & Software Engineering"
            ]
        },
        {
            "stage": 6,
            "title": "Career Ready",
            "courses": [
                "Career & Interview Preparation"
            ]
        }
    ]

    return jsonify({
        "roadmap": stages
    })


# ============================================================
# 404
# ============================================================

@app.errorhandler(404)
def not_found(error):

    if request.path.startswith("/api/"):
        return jsonify({
            "error": "API endpoint not found.",
            "path": request.path
        }), 404

    return error


# ============================================================
# GLOBAL ERROR HANDLER
# ============================================================

@app.errorhandler(500)
def server_error(error):

    if request.path.startswith("/api/"):
        return jsonify({
            "success": False,
            "error": "Internal server error."
        }), 500

    return """
    <h1>CodeQuest AI server error</h1>
    <p>Please check the Render logs.</p>
    """, 500


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

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
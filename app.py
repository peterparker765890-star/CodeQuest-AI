"""
=============================================================
CODEQUEST AI
Learn • Practice • Play • Build
=============================================================

Flask backend for CodeQuest AI.

Features:
- Expanded CS curriculum
- Detailed paragraph lessons
- Real code examples
- Large quiz bank
- Reduced quiz repetition using SQLite
- Quiz malpractice termination
- XP / levels / streaks
- Lesson progress
- Achievements
- Career pathways
- Pro tricks and skills
- Firebase Google-login token verification
- C / C++ / Python / Java compiler through Wandbox
- Render compatible
- SQLite persistence

Recommended Render environment variables:

SECRET_KEY=your-long-random-secret
DATABASE_PATH=/var/data/codequest.db
FIREBASE_SERVICE_ACCOUNT_JSON={...}

Do NOT put Firebase service-account JSON in GitHub.
=============================================================
"""

from __future__ import annotations

import json
import os
import random
import sqlite3
import time
from datetime import datetime, timezone, timedelta
from functools import wraps
from threading import Lock

import requests
from flask import Flask, jsonify, request, session

# =============================================================
# OPTIONAL FIREBASE ADMIN SDK
# =============================================================

try:
    import firebase_admin
    from firebase_admin import auth as firebase_auth
    from firebase_admin import credentials
except Exception:
    firebase_admin = None
    firebase_auth = None
    credentials = None


# =============================================================
# APP CONFIGURATION
# =============================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "CHANGE_THIS_CODEQUEST_SECRET"
)

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "codequest.db"
)

WANDBOX_API = "https://wandbox.org/api/compile.json"
WANDBOX_LIST = "https://wandbox.org/api/list.json"

WANDBOX_TIMEOUT = int(
    os.getenv("WANDBOX_TIMEOUT", "25")
)

db_lock = Lock()

compiler_cache = {
    "items": [],
    "expires": 0
}

firebase_ready = False


# =============================================================
# DATABASE
# =============================================================

def get_db():
    conn = sqlite3.connect(
        DATABASE_PATH,
        timeout=30
    )
    conn.row_factory = sqlite3.Row
    return conn


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def init_db():

    directory = os.path.dirname(DATABASE_PATH)

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )

    with db_lock:

        conn = get_db()

        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT PRIMARY KEY,
                email TEXT DEFAULT '',
                name TEXT DEFAULT '',
                photo_url TEXT DEFAULT '',
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                streak INTEGER DEFAULT 0,
                last_active TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS lesson_progress (
                uid TEXT NOT NULL,
                lesson_id TEXT NOT NULL,
                course_id TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                completed_at TEXT,
                PRIMARY KEY(uid, lesson_id)
            );

            CREATE TABLE IF NOT EXISTS quiz_seen (
                uid TEXT NOT NULL,
                question_id TEXT NOT NULL,
                seen_at TEXT NOT NULL,
                PRIMARY KEY(uid, question_id)
            );

            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT NOT NULL,
                score INTEGER DEFAULT 0,
                total INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0,
                status TEXT DEFAULT 'completed',
                reason TEXT DEFAULT '',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS achievements (
                uid TEXT NOT NULL,
                achievement_id TEXT NOT NULL,
                unlocked_at TEXT NOT NULL,
                PRIMARY KEY(uid, achievement_id)
            );

            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT NOT NULL,
                event TEXT NOT NULL,
                details TEXT DEFAULT '',
                created_at TEXT NOT NULL
            );
            """
        )

        conn.commit()
        conn.close()


try:
    init_db()
except Exception as exc:
    print("Database initialization error:", exc)


# =============================================================
# FIREBASE ADMIN
# =============================================================

def init_firebase():

    global firebase_ready

    if firebase_admin is None:
        print("firebase-admin package is not installed.")
        return False

    try:

        if firebase_admin._apps:
            firebase_ready = True
            return True

        raw = os.getenv(
            "FIREBASE_SERVICE_ACCOUNT_JSON",
            ""
        ).strip()

        if not raw:
            print(
                "Firebase Admin disabled: "
                "FIREBASE_SERVICE_ACCOUNT_JSON is missing."
            )
            return False

        info = json.loads(raw)

        credential = credentials.Certificate(info)

        firebase_admin.initialize_app(
            credential,
            {
                "projectId": info.get(
                    "project_id",
                    "codequest-ai-69884"
                )
            }
        )

        firebase_ready = True

        print("Firebase Admin initialized successfully.")

        return True

    except Exception as exc:

        print(
            "Firebase Admin initialization failed:",
            exc
        )

        return False


init_firebase()


# =============================================================
# CURRICULUM HELPERS
# =============================================================

def make_lesson(
    course_id,
    number,
    title,
    explanation,
    code="",
    language="",
    takeaway=""
):

    return {
        "id": f"{course_id}-{number:02d}",
        "number": number,
        "title": title,
        "lesson": explanation,
        "sample": code,
        "language": language,
        "takeaway": takeaway
    }


def make_course(
    course_id,
    title,
    icon,
    level,
    description,
    lessons
):

    return {
        "id": course_id,
        "title": title,
        "icon": icon,
        "level": level,
        "description": description,
        "chapters": lessons
    }


# =============================================================
# COURSE DATA
# =============================================================

courses = [

    # =========================================================
    # 1 COMPUTER BASICS
    # =========================================================

    make_course(
        "computer-basics",
        "Computer Basics",
        "💻",
        "Beginner",
        "Understand computers from the ground up before entering programming and development.",
        [

            make_lesson(
                "computer-basics",
                1,
                "What is a Computer?",
                """
A computer is an electronic system that accepts input, processes
information according to instructions, stores information when
necessary, and produces output. The important point is that a
computer is not simply a machine for arithmetic. Modern computers
run browsers, games, development environments, databases, servers,
mobile applications and artificial-intelligence systems.

Think about what happens when you open CodeQuest AI. Your touch
is an input. The browser processes the interaction using HTML,
CSS and JavaScript. A request may travel to a Flask server, the
server performs processing, and the resulting information is sent
back to the browser. This is a real example of input, processing
and output working together.
                """,
                """
name = input("Enter your name: ")
print("Welcome to CodeQuest AI,", name)
                """,
                "Python",
                "A computer accepts input, processes it using instructions, and produces useful output."
            ),

            make_lesson(
                "computer-basics",
                2,
                "Hardware and Software",
                """
Hardware means the physical components of a computer. Examples
include the CPU, RAM, SSD, motherboard, keyboard, mouse, display
and network adapter. Software consists of instructions and data
that tell the hardware what work to perform.

Applications normally do not directly control electronic hardware.
The operating system provides services and interfaces between
applications and the physical machine. This separation allows
thousands of different programs to operate on the same computer.
                """,
                """
print("Application")
print("    ↓")
print("Operating System")
print("    ↓")
print("Hardware")
                """,
                "Python",
                "Hardware is physical; software contains instructions."
            ),

            make_lesson(
                "computer-basics",
                3,
                "CPU and Processing",
                """
The Central Processing Unit executes program instructions.
At a simplified level, the processor repeatedly fetches an
instruction, decodes it, and performs the required operation.
Modern CPUs improve performance using multiple cores, caches,
pipelines and sophisticated instruction execution techniques.

When your program performs an addition such as a + b, the
high-level expression eventually becomes machine-level operations
that the processor can execute. Understanding this connection
helps explain why programming languages ultimately depend on
computer architecture.
                """,
                """
#include <stdio.h>

int main(void) {
    int a = 10;
    int b = 20;
    int total = a + b;

    printf("%d\\n", total);

    return 0;
}
                """,
                "C",
                "The CPU executes the instructions produced from your program."
            ),

            make_lesson(
                "computer-basics",
                4,
                "RAM and Storage",
                """
RAM is temporary working memory used by running programs.
Storage devices such as SSDs provide persistent storage, meaning
data normally remains after the computer is turned off.

When you launch an application, the operating system loads
required data from storage into RAM. The CPU can then work with
that active data. This is why RAM and storage have different
purposes even though both are involved in keeping information.
                """,
                """
numbers = [10, 20, 30, 40]

print(numbers)
print("These values are currently being used by the program.")
                """,
                "Python",
                "RAM is active working memory; storage keeps data persistently."
            ),

            make_lesson(
                "computer-basics",
                5,
                "Operating Systems",
                """
An operating system manages important computer resources.
It handles processes, memory, files, devices, permissions and
networking. Windows, Linux, macOS and Android are examples of
operating systems.

Applications use operating-system services instead of having to
implement every hardware operation themselves. For example, a
Python program can open a file using a standard API while the
operating system handles the underlying filesystem operations.
                """,
                """
with open("notes.txt", "w") as file:
    file.write("CodeQuest AI")
                """,
                "Python",
                "The operating system provides common services between software and hardware."
            ),

            make_lesson(
                "computer-basics",
                6,
                "Binary and Data",
                """
Computers represent information using bits. A bit can represent
two logical states, commonly written as 0 and 1. Eight bits form
one byte. Numbers, characters, images, audio and video are all
stored using encoded patterns of bits.

Binary understanding becomes useful when learning memory,
networking, file sizes and low-level programming. Even though
modern developers normally work with high-level languages, the
underlying computer still works with encoded digital information.
                """,
                """
number = 13

print(bin(number))
print("13 in binary is:", bin(number))
                """,
                "Python",
                "Computers ultimately represent information as encoded binary data."
            ),

            make_lesson(
                "computer-basics",
                7,
                "Files, Folders and Paths",
                """
Files store information while folders organize files into a
hierarchy. A path tells a program where an item exists. Developers
work with paths constantly because projects contain source files,
images, databases, configuration files and documentation.

A relative path is interpreted from the current working directory.
An absolute path identifies a location from the filesystem root.
Understanding paths prevents many common programming and deployment
mistakes.
                """,
                """
from pathlib import Path

project_file = Path("src") / "app.py"

print(project_file)
                """,
                "Python",
                "Learn to distinguish file names, folders, relative paths and absolute paths."
            ),

            make_lesson(
                "computer-basics",
                8,
                "Compiler and Interpreter",
                """
A compiler transforms source code into another representation,
often native machine code or an intermediate form. An interpreter
or runtime executes source or intermediate instructions through
a runtime system. Real programming language implementations can
combine both ideas.

For example, Java source code is compiled into bytecode and then
executed by the Java Virtual Machine. Python implementations also
perform internal compilation before execution. The important lesson
is to understand how source instructions are transformed and run.
                """,
                """
x = 10
y = 20

print(x + y)
                """,
                "Python",
                "Compilation and interpretation describe how program instructions are transformed and executed."
            )
        ]
    ),


    # =========================================================
    # 2 DIGITAL PRODUCTIVITY
    # =========================================================

    make_course(
        "productivity",
        "Digital Literacy & Productivity",
        "🧰",
        "Beginner",
        "Build practical computer skills for college, projects and professional work.",
        [

            make_lesson(
                "productivity",
                1,
                "Professional Documents",
                """
A professional document is organized so another person can
quickly understand the information. Headings, spacing, lists,
tables, page numbers and consistent fonts create a clear visual
hierarchy.

For college projects, reports and lab records, good formatting
does not replace good content. Instead, it makes good content
easier to read and evaluate.
                """,
                """
REPORT STRUCTURE

1. Introduction
2. Objective
3. Method
4. Results
5. Discussion
6. Conclusion
                """,
                "",
                "Use formatting to make the structure of information obvious."
            ),

            make_lesson(
                "productivity",
                2,
                "Spreadsheet Formulas",
                """
Spreadsheets become powerful when formulas are used instead of
manual calculations. A formula can reference other cells and
automatically recalculate when the underlying data changes.

Students can use spreadsheets for marks, attendance, budgets,
survey results and simple data analysis. The same principle of
turning raw data into calculated information appears later in
programming and databases.
                """,
                """
=SUM(B2:B10)

=AVERAGE(B2:B10)

=MAX(B2:B10)

=MIN(B2:B10)
                """,
                "",
                "Use formulas so that calculations update automatically."
            ),

            make_lesson(
                "productivity",
                3,
                "Charts and Data",
                """
Charts convert numerical information into visual patterns.
A bar chart is useful for comparing categories, while a line
chart is useful for showing change over time. A chart should
answer a question rather than simply decorate a document.

Always label important axes, values and units. Poorly designed
charts can make correct data difficult to understand.
                """,
                """
Subject     Mark
C           82
Python      91
Maths       76

A bar chart can compare the marks directly.
                """,
                "",
                "Choose the chart type according to the relationship you want to show."
            ),

            make_lesson(
                "productivity",
                4,
                "Presentation Design",
                """
A presentation should guide the audience through an idea.
A strong technical presentation normally explains the problem,
the proposed solution, the technology, the implementation and
the result.

Slides should support the speaker instead of containing every
sentence that the speaker plans to say. Clear visuals and short
points usually make technical explanations easier to follow.
                """,
                """
PROBLEM
   ↓
SOLUTION
   ↓
ARCHITECTURE
   ↓
DEMO
   ↓
RESULT
   ↓
FUTURE SCOPE
                """,
                "",
                "Slides support your explanation; they should not become a wall of text."
            ),

            make_lesson(
                "productivity",
                5,
                "Searching Technical Information",
                """
Searching is a technical skill. Instead of searching for a huge
sentence, identify the exact concept you need. Then compare the
result with reliable documentation.

For programming, official documentation is especially valuable
because APIs and syntax can change between versions. Learning to
verify information is an important professional skill.
                """,
                """
Useful searches:

Python list sort official documentation
Flask JSON request documentation
SQLite CREATE TABLE documentation
                """,
                "",
                "Search precisely and verify important technical information."
            )
        ]
    ),


    # =========================================================
    # 3 GIT
    # =========================================================

    make_course(
        "git",
        "Git & GitHub",
        "🐙",
        "Beginner → Intermediate",
        "Learn version control and build a professional GitHub workflow.",
        [

            make_lesson(
                "git",
                1,
                "Why Git Exists",
                """
Git records how a project changes over time. Without version
control, developers often create confusing copies such as
final.py, final2.py and final-new.py. Git provides a structured
history of changes.

This history allows developers to inspect older versions, recover
mistakes and experiment with new ideas without losing the stable
version of a project.
                """,
                """
git init
git status
git add .
git commit -m "Initial project"
                """,
                "Git",
                "Git records project history instead of relying on manually renamed files."
            ),

            make_lesson(
                "git",
                2,
                "Commits",
                """
A commit represents a logical group of changes. A good commit
message explains what changed. Small meaningful commits make it
easier to understand project history and locate the change that
introduced a problem.

For example, adding a quiz API should be separate from completely
redesigning the website when possible.
                """,
                """
git add app.py
git commit -m "Add quiz API"
git log --oneline
                """,
                "Git",
                "Commit logical changes with clear messages."
            ),

            make_lesson(
                "git",
                3,
                "Branches",
                """
A branch provides an independent development path. You can build
a feature on a branch without putting unfinished code directly
into the main branch.

This is useful when several features are being developed at the
same time. Once a feature is tested, the branch can be reviewed
and merged.
                """,
                """
git switch -c feature/compiler
git add .
git commit -m "Add compiler UI"
git switch main
                """,
                "Git",
                "Branches provide safe spaces for feature development."
            ),

            make_lesson(
                "git",
                4,
                "GitHub",
                """
GitHub hosts Git repositories online and adds collaboration
features such as issues, pull requests and project discussions.
A public project can also become part of a developer portfolio.

A strong repository should explain what the project does,
how it works, how to install it and how someone can run it.
                """,
                """
git remote add origin https://github.com/USER/PROJECT.git
git push -u origin main
                """,
                "Git",
                "A GitHub repository can be both a development workspace and a project portfolio."
            ),

            make_lesson(
                "git",
                5,
                "Protecting Secrets",
                """
Source code repositories are often public or shared. Passwords,
private tokens, cloud credentials and service-account private keys
should never be committed to a repository.

Instead, applications commonly read sensitive configuration from
environment variables or secure secret-management systems.
                """,
                """
# .env example

SECRET_KEY=replace-me

# Never commit the real secret file.
                """,
                "",
                "Keep secrets outside source code and outside public repositories."
            )
        ]
    ),


    # =========================================================
    # 4 C
    # =========================================================

    make_course(
        "c",
        "C Programming",
        "⚙️",
        "Beginner → Intermediate",
        "Learn programming fundamentals through C and build strong problem-solving foundations.",
        [

            make_lesson(
                "c",
                1,
                "Your First C Program",
                """
C programs are built from functions, declarations, statements
and expressions. Execution begins in main. The stdio library
provides functions such as printf for displaying information.

Learning the structure of a simple C program gives you a base
for understanding variables, conditions, loops and functions.
                """,
                """
#include <stdio.h>

int main(void) {

    printf("Hello, CodeQuest AI!\\n");

    return 0;
}
                """,
                "C",
                "Most beginner C programs start execution inside main."
            ),

            make_lesson(
                "c",
                2,
                "Variables and Data Types",
                """
Variables allow programs to store values under meaningful names.
C requires you to declare a variable's type, such as int, float
or char. The type tells the compiler what kind of value the
variable represents and influences how it is stored and operated
on.

Choosing suitable variable types makes programs easier to read
and helps the compiler detect certain mistakes.
                """,
                """
#include <stdio.h>

int main(void) {

    int age = 18;
    float mark = 91.5f;
    char grade = 'A';

    printf("%d %.1f %c\\n",
           age, mark, grade);

    return 0;
}
                """,
                "C",
                "A variable stores a value and its type describes that value."
            ),

            make_lesson(
                "c",
                3,
                "Conditions",
                """
Programs frequently need to make decisions. The if statement
allows code to execute only when a condition is true. else and
else if allow multiple possible paths.

Conditional logic is the foundation of validation, games,
authentication, grading systems and many real-world applications.
                """,
                """
#include <stdio.h>

int main(void) {

    int mark = 82;

    if (mark >= 50)
        printf("Pass\\n");
    else
        printf("Fail\\n");

    return 0;
}
                """,
                "C",
                "Conditions allow a program to choose different actions."
            ),

            make_lesson(
                "c",
                4,
                "Loops",
                """
Loops repeat instructions. A for loop is convenient when the
number of repetitions is known, while while is useful when the
loop depends on a condition.

Loops are essential for processing arrays, generating patterns,
searching data and performing repeated calculations.
                """,
                """
#include <stdio.h>

int main(void) {

    for (int i = 1; i <= 5; i++) {
        printf("%d\\n", i);
    }

    return 0;
}
                """,
                "C",
                "Loops remove unnecessary repetition from programs."
            ),

            make_lesson(
                "c",
                5,
                "Functions",
                """
A function groups reusable logic under a name. Functions can
receive parameters and return values. Breaking a large program
into smaller functions makes the program easier to understand,
test and debug.

A useful function normally has one clear responsibility.
                """,
                """
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main(void) {

    printf("%d\\n", add(10, 20));

    return 0;
}
                """,
                "C",
                "Functions divide complex programs into reusable units."
            ),

            make_lesson(
                "c",
                6,
                "Arrays",
                """
An array stores multiple values of the same type in a contiguous
sequence. Each element is accessed using an index. Arrays are
important because they introduce the idea of collections and
memory layout.

Many data structures studied later in DSA build on concepts
introduced by arrays.
                """,
                """
#include <stdio.h>

int main(void) {

    int marks[] = {80, 90, 75, 88};

    for (int i = 0; i < 4; i++) {
        printf("%d\\n", marks[i]);
    }

    return 0;
}
                """,
                "C",
                "Arrays store multiple related values under one variable name."
            ),

            make_lesson(
                "c",
                7,
                "Pointers",
                """
A pointer stores a memory address. Pointers are one of the
features that make C powerful because they allow programs to work
directly with memory and pass addresses to functions.

Pointers can be confusing initially, so focus on the basic idea:
a normal variable stores a value, while a pointer can store the
address where a value is located.
                """,
                """
#include <stdio.h>

int main(void) {

    int value = 50;
    int *ptr = &value;

    printf("Value: %d\\n", value);
    printf("Value through pointer: %d\\n", *ptr);

    return 0;
}
                """,
                "C",
                "A pointer stores an address and * can be used to access the pointed value."
            ),

            make_lesson(
                "c",
                8,
                "Structures",
                """
Structures allow related values of different types to be grouped
into one custom data type. This is useful for representing real
entities such as students, products, employees and game players.

Structures are an important step toward modeling real-world
information in programs.
                """,
                """
#include <stdio.h>

struct Student {
    char name[30];
    int mark;
};

int main(void) {

    struct Student s = {"Joe", 90};

    printf("%s scored %d\\n",
           s.name, s.mark);

    return 0;
}
                """,
                "C",
                "Structures group related data into a meaningful record."
            )
        ]
    ),


    # =========================================================
    # 5 C++
    # =========================================================

    make_course(
        "cpp",
        "C++ Programming",
        "🚀",
        "Intermediate",
        "Learn object-oriented programming, STL and modern C++ concepts.",
        [

            make_lesson(
                "cpp",
                1,
                "C++ Basics",
                """
C++ is a general-purpose language that supports procedural,
object-oriented and generic programming. It extends many ideas
from C while providing abstractions such as classes, templates
and standard containers.

C++ is widely used in performance-sensitive software, games,
systems programming and competitive programming.
                """,
                """
#include <iostream>

int main() {

    std::cout << "Hello C++!";

    return 0;
}
                """,
                "C++",
                "C++ combines low-level control with higher-level abstractions."
            ),

            make_lesson(
                "cpp",
                2,
                "Classes and Objects",
                """
A class defines the data and behavior of a type. An object is an
instance of that class. Classes help developers model concepts
such as Student, Product, Player or BankAccount.

Encapsulation allows a class to control how its internal data is
used and changed.
                """,
                """
#include <iostream>
#include <string>

class Player {

public:

    std::string name;
    int xp = 0;

    void addXP(int value) {
        xp += value;
    }
};

int main() {

    Player p;

    p.name = "Joe";
    p.addXP(100);

    std::cout << p.name
              << " XP: "
              << p.xp;

    return 0;
}
                """,
                "C++",
                "Classes combine related data and behavior."
            ),

            make_lesson(
                "cpp",
                3,
                "Constructors",
                """
A constructor runs when an object is created. Constructors are
normally used to establish a valid initial state.

Using constructors becomes especially useful when an application
creates many objects that need different starting values.
                """,
                """
#include <iostream>
#include <string>

class Student {

public:

    std::string name;

    Student(std::string n) {
        name = n;
    }
};

int main() {

    Student s("Joe");

    std::cout << s.name;

    return 0;
}
                """,
                "C++",
                "Constructors initialize objects."
            ),

            make_lesson(
                "cpp",
                4,
                "Inheritance and Polymorphism",
                """
Inheritance allows a derived class to reuse or specialize
behavior from a base class. Polymorphism allows code to operate
through a common interface while the actual object determines
which implementation runs.

These concepts are useful when several related objects need a
shared design but different behavior.
                """,
                """
#include <iostream>

class Animal {

public:

    virtual void sound() {
        std::cout << "Sound";
    }
};

class Dog : public Animal {

public:

    void sound() override {
        std::cout << "Bark";
    }
};

int main() {

    Dog d;
    d.sound();

    return 0;
}
                """,
                "C++",
                "Polymorphism lets different objects respond to the same interface differently."
            ),

            make_lesson(
                "cpp",
                5,
                "STL Vector",
                """
The Standard Template Library provides reusable containers and
algorithms. vector is a dynamic array that can grow as elements
are added.

Using standard containers reduces the amount of manual memory
management required and makes code easier to maintain.
                """,
                """
#include <iostream>
#include <vector>

int main() {

    std::vector<int> marks =
        {80, 90, 75};

    for (int mark : marks) {
        std::cout << mark << " ";
    }

    return 0;
}
                """,
                "C++",
                "Use STL containers when they naturally match the problem."
            )
        ]
    ),


    # =========================================================
    # 6 PYTHON
    # =========================================================

    make_course(
        "python",
        "Python Programming",
        "🐍",
        "Beginner → Advanced",
        "Learn Python fundamentals, data structures, files, exceptions, modules and APIs.",
        [

            make_lesson(
                "python",
                1,
                "Variables and Data",
                """
Python variables are created by assignment. Python determines
the runtime type of the object referenced by the variable, which
makes simple programs concise.

Variables are fundamental because applications constantly need
to remember information such as names, scores, settings and
results.
                """,
                """
name = "Joe"
age = 18
score = 92.5

print(name)
print(age)
print(score)
                """,
                "Python",
                "Variables allow programs to work with named values."
            ),

            make_lesson(
                "python",
                2,
                "Conditions and Loops",
                """
Conditions choose between different paths while loops repeat
operations. Together they create most of the decision-making
behavior found in beginner programs.

For example, a student application can loop through marks and
decide whether each student has passed.
                """,
                """
marks = [72, 45, 91]

for mark in marks:

    if mark >= 50:
        print(mark, "Pass")
    else:
        print(mark, "Fail")
                """,
                "Python",
                "Control flow determines what code executes and when."
            ),

            make_lesson(
                "python",
                3,
                "Lists and Dictionaries",
                """
Lists store ordered collections of values. Dictionaries store
key-value relationships and are especially useful when data has
named properties.

A student record is naturally represented using a dictionary
because properties such as name, department and mark have
meaningful keys.
                """,
                """
student = {
    "name": "Joe",
    "department": "IT",
    "mark": 90
}

print(student["department"])
                """,
                "Python",
                "Choose a data structure based on how the program needs to access information."
            ),

            make_lesson(
                "python",
                4,
                "Functions",
                """
Functions package reusable logic into named blocks. Parameters
allow functions to receive data and return values allow them to
produce results.

Functions reduce duplication and make large programs easier to
test because individual pieces can be tested independently.
                """,
                """
def calculate_total(price, quantity):

    return price * quantity


total = calculate_total(250, 3)

print(total)
                """,
                "Python",
                "A good function normally has one clear responsibility."
            ),

            make_lesson(
                "python",
                5,
                "Exception Handling",
                """
Real programs encounter invalid input, missing files, network
failures and other runtime problems. Python exceptions provide a
structured mechanism for handling expected failures.

Good error handling should explain the problem and provide a
sensible recovery path. Avoid hiding every error with a broad
exception handler because that can make debugging harder.
                """,
                """
try:

    number = int(input("Number: "))

    print(100 / number)

except ValueError:

    print("Please enter an integer.")

except ZeroDivisionError:

    print("Zero is not allowed.")
                """,
                "Python",
                "Handle expected failures explicitly and keep unexpected bugs visible during development."
            ),

            make_lesson(
                "python",
                6,
                "Files and JSON",
                """
Files allow a Python application to preserve information beyond
one execution. JSON is a common format for structured data and is
widely used by APIs and configuration systems.

Learning JSON prepares you for web development because many APIs
send structured responses using JSON.
                """,
                """
import json

student = {
    "name": "Joe",
    "mark": 90
}

with open("student.json", "w") as file:

    json.dump(
        student,
        file,
        indent=2
    )
                """,
                "Python",
                "JSON connects application data with APIs and configuration files."
            ),

            make_lesson(
                "python",
                7,
                "Modules",
                """
A module is a Python file containing reusable code. Modules keep
large programs organized by separating responsibilities.

As projects grow, putting everything into one Python file becomes
difficult to maintain. Modules provide a natural way to split a
project into logical components.
                """,
                """
# math is part of Python's standard library

import math

print(math.sqrt(81))
                """,
                "Python",
                "Separate reusable functionality into modules as projects grow."
            ),

            make_lesson(
                "python",
                8,
                "APIs with Python",
                """
An API is a defined interface through which one program can
request information or actions from another system. Python
applications frequently use HTTP requests to communicate with
web services.

A good API client checks the HTTP status, handles errors and
validates the response before using the returned data.
                """,
                """
import requests

response = requests.get(
    "https://example.com"
)

print(response.status_code)
                """,
                "Python",
                "Treat APIs as contracts with defined inputs, outputs and errors."
            )
        ]
    ),


    # =========================================================
    # 7 WEB DEVELOPMENT
    # =========================================================

    make_course(
        "web",
        "Web Development",
        "🌐",
        "Beginner → Intermediate",
        "Learn HTML, CSS, JavaScript, browser behavior, forms and HTTP.",
        [

            make_lesson(
                "web",
                1,
                "HTML Structure",
                """
HTML describes the structure and meaning of a web page. Headings,
paragraphs, links, forms, buttons and lists provide semantic
information to the browser.

Good web development starts with meaningful structure before
visual styling is added.
                """,
                """
<!doctype html>

<html>

<body>

<h1>CodeQuest AI</h1>

<p>Learn. Practice. Play. Build.</p>

<button>Start Learning</button>

</body>

</html>
                """,
                "HTML",
                "HTML describes what the content is."
            ),

            make_lesson(
                "web",
                2,
                "CSS",
                """
CSS controls the visual presentation of HTML. It handles
typography, spacing, colors, borders, layout and responsive
design.

Separating CSS from HTML allows the same structure to be styled
in different ways without changing the underlying content.
                """,
                """
body {
    background: #120d22;
    color: white;
    font-family: Arial;
}

.card {
    padding: 20px;
    border-radius: 16px;
}
                """,
                "CSS",
                "CSS controls how structured content looks."
            ),

            make_lesson(
                "web",
                3,
                "JavaScript",
                """
JavaScript adds behavior to web pages. It can respond to button
clicks, modify page content, communicate with servers and use
browser APIs.

CodeQuest AI uses JavaScript for features such as opening lessons,
running quizzes, updating XP and communicating with Flask APIs.
                """,
                """
document
    .getElementById("startBtn")
    .addEventListener("click", function () {

        alert("Quest started!");

    });
                """,
                "JavaScript",
                "JavaScript makes a web page interactive."
            ),

            make_lesson(
                "web",
                4,
                "DOM Manipulation",
                """
The Document Object Model represents a web page as objects that
JavaScript can access and modify. This allows a program to change
text, classes, attributes and other elements after the page has
loaded.

Interactive websites depend heavily on DOM manipulation.
                """,
                """
const title =
    document.getElementById("title");

title.textContent =
    "Welcome to CodeQuest AI";
                """,
                "JavaScript",
                "The DOM lets JavaScript interact with page elements."
            ),

            make_lesson(
                "web",
                5,
                "Fetch and APIs",
                """
The fetch API allows browser JavaScript to communicate with a
server. CodeQuest AI uses this pattern to request courses,
quiz questions, career data and compiler results from Flask.

Understanding request and response flow is an important step from
static websites to full-stack applications.
                """,
                """
fetch("/api/courses")
    .then(response => response.json())
    .then(data => {

        console.log(data);

    });
                """,
                "JavaScript",
                "Fetch connects browser interfaces to backend APIs."
            ),

            make_lesson(
                "web",
                6,
                "Forms and Validation",
                """
Forms allow users to send information to an application. Client
validation can provide immediate feedback, while server-side
validation is still required because browser checks can be
bypassed.

Good validation improves both user experience and application
security.
                """,
                """
<form id="loginForm">

<input
    id="email"
    type="email"
    required
>

<button type="submit">
    Login
</button>

</form>
                """,
                "HTML",
                "Validate input on the client for usability and on the server for security."
            )
        ]
    ),


    # =========================================================
    # 8 DBMS
    # =========================================================

    make_course(
        "dbms",
        "DBMS & SQL",
        "🗄️",
        "Intermediate",
        "Learn databases, tables, SQL queries, relationships and practical data storage.",
        [

            make_lesson(
                "dbms",
                1,
                "What is a Database?",
                """
A database stores structured information so applications can
create, read, update and delete data efficiently. A student
application might store users, courses, marks and progress in
different tables.

Databases are essential because application data must survive
beyond the lifetime of a single program execution.
                """,
                """
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    mark INTEGER
);
                """,
                "SQL",
                "Databases provide persistent structured application data."
            ),

            make_lesson(
                "dbms",
                2,
                "SELECT",
                """
SELECT retrieves information from a database. Filtering with
WHERE allows an application to request only records matching a
condition.

This pattern appears everywhere: finding a user's account,
displaying completed lessons or retrieving products matching a
search.
                """,
                """
SELECT name, mark
FROM students
WHERE mark >= 50;
                """,
                "SQL",
                "SELECT reads data from tables."
            ),

            make_lesson(
                "dbms",
                3,
                "INSERT UPDATE DELETE",
                """
CRUD stands for Create, Read, Update and Delete. These four
operations represent the basic actions applications perform on
stored information.

A student portal may create a user record, read the user's
progress, update XP and delete an account.
                """,
                """
INSERT INTO students(name, mark)
VALUES ('Joe', 90);

UPDATE students
SET mark = 95
WHERE name = 'Joe';

DELETE FROM students
WHERE name = 'Joe';
                """,
                "SQL",
                "CRUD represents the fundamental operations on application data."
            ),

            make_lesson(
                "dbms",
                4,
                "Primary Keys",
                """
A primary key uniquely identifies a row. Without a reliable
identifier, applications can struggle to distinguish two records
with similar information.

For example, two students can have the same name, but each account
can have a unique numeric or UUID identifier.
                """,
                """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT
);
                """,
                "SQL",
                "Primary keys uniquely identify records."
            ),

            make_lesson(
                "dbms",
                5,
                "Relationships and JOIN",
                """
Real applications usually have multiple related tables. A
user table might contain account information while a progress
table stores completed lessons.

JOIN operations allow related information to be retrieved together.
This becomes especially important as applications grow.
                """,
                """
SELECT users.name, progress.lesson_id
FROM users
JOIN progress
ON users.id = progress.user_id;
                """,
                "SQL",
                "Relationships connect data stored across tables."
            ),

            make_lesson(
                "dbms",
                6,
                "Indexes",
                """
An index is an additional data structure that helps a database
find records efficiently. Indexes can greatly improve searches
on frequently queried columns.

However, indexes also consume storage and can make writes more
expensive, so they should be added based on actual query needs.
                """,
                """
CREATE INDEX idx_students_name
ON students(name);
                """,
                "SQL",
                "Indexes speed selected queries but are not free."
            )
        ]
    ),


    # =========================================================
    # 9 DSA
    # =========================================================

    make_course(
        "dsa",
        "Data Structures & Algorithms",
        "🧩",
        "Intermediate",
        "Learn problem solving, complexity, arrays, stacks, queues, searching, sorting and graphs.",
        [

            make_lesson(
                "dsa",
                1,
                "Why Data Structures Matter",
                """
A data structure determines how information is organized and
accessed. Different structures make different operations efficient.

For example, a list may be convenient for ordered data, while a
dictionary provides fast key-based lookup in many common cases.
Choosing the right structure can change the performance of an
entire application.
                """,
                """
students = {
    "101": "Joe",
    "102": "Alex"
}

print(students["101"])
                """,
                "Python",
                "Data structure choice affects how efficiently information can be used."
            ),

            make_lesson(
                "dsa",
                2,
                "Big O",
                """
Big O notation describes how an algorithm's resource requirements
grow as input size increases. It helps developers reason about
scalability.

For example, searching every item in a list may require examining
many elements, while a suitable indexed or hashed structure can
often locate information much faster.
                """,
                """
# Linear search

numbers = [10, 20, 30, 40]

target = 30

for number in numbers:

    if number == target:
        print("Found")
        break
                """,
                "Python",
                "Big O helps compare how algorithms scale with larger inputs."
            ),

            make_lesson(
                "dsa",
                3,
                "Stack",
                """
A stack follows the Last In, First Out principle. The most
recently added item is removed first.

Stacks appear in browser history, undo systems, expression
evaluation and function-call management.
                """,
                """
stack = []

stack.append("Page A")
stack.append("Page B")

print(stack.pop())
                """,
                "Python",
                "A stack follows LIFO: last in, first out."
            ),

            make_lesson(
                "dsa",
                4,
                "Queue",
                """
A queue follows the First In, First Out principle. The earliest
item added is processed first.

Queues are useful for print jobs, task processing, network
requests and scheduling systems.
                """,
                """
from collections import deque

queue = deque()

queue.append("Task A")
queue.append("Task B")

print(queue.popleft())
                """,
                "Python",
                "A queue follows FIFO: first in, first out."
            ),

            make_lesson(
                "dsa",
                5,
                "Binary Search",
                """
Binary search works on sorted data. Instead of checking every
element, it repeatedly eliminates half of the remaining search
space.

This makes binary search much more efficient than linear search
for large sorted collections.
                """,
                """
numbers = [10, 20, 30, 40, 50]

target = 40

left = 0
right = len(numbers) - 1

while left <= right:

    mid = (left + right) // 2

    if numbers[mid] == target:
        print("Found")
        break

    if numbers[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
                """,
                "Python",
                "Binary search repeatedly halves a sorted search space."
            ),

            make_lesson(
                "dsa",
                6,
                "Sorting",
                """
Sorting arranges data according to an ordering rule. Sorting is
useful because many later operations become easier when information
has a predictable order.

Python and C++ provide standard sorting tools, but understanding
basic algorithms such as bubble sort helps build algorithmic
thinking.
                """,
                """
numbers = [5, 2, 8, 1, 3]

numbers.sort()

print(numbers)
                """,
                "Python",
                "Understand sorting conceptually even when using standard library implementations."
            )
        ]
    ),


    # =========================================================
    # 10 OPERATING SYSTEMS
    # =========================================================

    make_course(
        "os",
        "Operating Systems",
        "🖥️",
        "Intermediate",
        "Understand processes, memory, files, scheduling and operating-system concepts.",
        [

            make_lesson(
                "os",
                1,
                "Processes",
                """
A process is a running instance of a program. The operating
system gives processes resources such as memory and CPU time.

Multiple processes can exist simultaneously, and the OS manages
their execution so applications can share the machine.
                """,
                """
print("This Python program is running as a process.")
                """,
                "Python",
                "A process represents a program that is currently executing."
            ),

            make_lesson(
                "os",
                2,
                "Threads",
                """
A thread is an execution path within a process. A process can
contain multiple threads that share much of the process's memory.

Threads can be useful for concurrent tasks, but shared data
creates synchronization challenges.
                """,
                """
import threading

def task():
    print("Running in a thread")

thread = threading.Thread(target=task)

thread.start()
thread.join()
                """,
                "Python",
                "Threads provide multiple execution paths within a process."
            ),

            make_lesson(
                "os",
                3,
                "Memory Management",
                """
Operating systems manage memory so multiple applications can
run safely. Each process normally receives its own virtual address
space, which helps isolate applications.

Virtual memory allows the OS to manage physical memory and
storage together while presenting programs with a useful address
space.
                """,
                """
numbers = [1, 2, 3, 4, 5]

print(numbers)
                """,
                "Python",
                "Memory management allows applications to run without directly controlling physical RAM."
            ),

            make_lesson(
                "os",
                4,
                "File Systems",
                """
A filesystem organizes persistent data into files and directories.
It tracks metadata such as names, locations and permissions.

Applications normally use operating-system APIs instead of
directly manipulating storage hardware.
                """,
                """
from pathlib import Path

Path("example.txt").write_text(
    "CodeQuest AI"
)

print(Path("example.txt").read_text())
                """,
                "Python",
                "Filesystems organize persistent data and metadata."
            ),

            make_lesson(
                "os",
                5,
                "CPU Scheduling",
                """
The CPU can execute only a limited amount of work at a time.
Operating systems use scheduling algorithms to decide which
process or thread should receive CPU time.

Scheduling involves trade-offs involving responsiveness,
throughput and fairness.
                """,
                """
tasks = [
    "Browser",
    "Music",
    "Code editor"
]

for task in tasks:
    print("Scheduling:", task)
                """,
                "Python",
                "Scheduling decides how CPU time is shared."
            )
        ]
    ),


    # =========================================================
    # 11 NETWORKS
    # =========================================================

    make_course(
        "networks",
        "Computer Networks",
        "🌐",
        "Intermediate",
        "Understand how computers communicate using IP, DNS, HTTP, ports and network protocols.",
        [

            make_lesson(
                "networks",
                1,
                "What is a Network?",
                """
A computer network allows devices to exchange information.
Networks can be small, such as a local network connecting
devices in a home, or enormous, such as the Internet.

Communication requires rules called protocols so that different
devices understand how messages should be structured and handled.
                """,
                """
print("Computer A")
print("    ↓")
print("Network")
print("    ↓")
print("Computer B")
                """,
                "",
                "Networks allow systems to communicate using agreed protocols."
            ),

            make_lesson(
                "networks",
                2,
                "IP Addresses",
                """
An IP address identifies a network interface in an IP network.
IPv4 uses 32-bit addresses while IPv6 uses much larger addresses.

Applications normally use names rather than memorizing IP
addresses, which is where DNS becomes important.
                """,
                """
import socket

print(socket.gethostbyname("example.com"))
                """,
                "Python",
                "IP addresses identify network endpoints."
            ),

            make_lesson(
                "networks",
                3,
                "DNS",
                """
DNS translates human-readable domain names into network
addresses. When you type a website name into a browser, the
browser or operating system may need to resolve that name before
connecting to the server.

DNS is one of the major services that makes the Internet convenient
for humans.
                """,
                """
import socket

ip = socket.gethostbyname(
    "example.com"
)

print(ip)
                """,
                "Python",
                "DNS connects domain names with network addresses."
            ),

            make_lesson(
                "networks",
                4,
                "HTTP",
                """
HTTP is an application-layer protocol used for web communication.
A client sends a request and a server returns a response.

Methods such as GET and POST communicate different intentions.
Status codes such as 200, 404 and 500 provide information about
the result.
                """,
                """
GET /api/courses

200 OK
{
    "courses": []
}
                """,
                "HTTP",
                "Web applications communicate using HTTP requests and responses."
            ),

            make_lesson(
                "networks",
                5,
                "Ports",
                """
A port identifies a network service on a host. An IP address
helps identify the host while the port helps identify the
service receiving the connection.

For example, a Flask development server commonly listens on
port 5000.
                """,
                """
http://localhost:5000
                """,
                "",
                "Ports help direct network traffic to the correct service."
            )
        ]
    ),


    # =========================================================
    # 12 CYBERSECURITY
    # =========================================================

    make_course(
        "cybersecurity",
        "Cybersecurity",
        "🛡️",
        "Intermediate",
        "Learn practical security fundamentals, authentication, passwords, input validation and safe development.",
        [

            make_lesson(
                "cybersecurity",
                1,
                "Security Fundamentals",
                """
Cybersecurity protects systems, applications and data against
unauthorized access, alteration and disruption. A useful
foundation is the confidentiality, integrity and availability
model.

Security is not a single feature added at the end of development.
It should be considered throughout design, implementation,
testing and deployment.
                """,
                """
Confidentiality
Integrity
Availability
                """,
                "",
                "Security should be considered throughout the software lifecycle."
            ),

            make_lesson(
                "cybersecurity",
                2,
                "Passwords",
                """
Passwords are authentication secrets and should never be stored
as plain text. Production systems normally store password hashes
using an appropriate password-hashing algorithm.

Strong authentication also considers rate limiting, account
recovery and, where appropriate, additional authentication factors.
                """,
                """
# Never do this in a real application:
password = "secret"

# Real applications should use a secure
# password hashing system.
                """,
                "Python",
                "Never store user passwords as plain text."
            ),

            make_lesson(
                "cybersecurity",
                3,
                "Input Validation",
                """
Applications receive input from users and other systems. That
input should be validated before it is trusted.

Validation can check type, length, allowed values and expected
format. Server-side validation remains necessary even when the
browser already validates the same field.
                """,
                """
age = input("Age: ")

if age.isdigit():
    age = int(age)

    if 0 <= age <= 120:
        print("Valid")
                """,
                "Python",
                "Treat external input as untrusted until it has been validated."
            ),

            make_lesson(
                "cybersecurity",
                4,
                "SQL Injection Concept",
                """
SQL injection occurs when untrusted input is incorrectly
combined with SQL commands. Parameterized queries are designed
to separate SQL structure from user-provided values.

This is one reason applications should never construct database
queries by directly concatenating arbitrary user input.
                """,
                """
# Safe pattern concept:

cursor.execute(
    "SELECT * FROM users WHERE email = ?",
    (email,)
)
                """,
                "Python",
                "Use parameterized database queries instead of string concatenation."
            ),

            make_lesson(
                "cybersecurity",
                5,
                "HTTPS",
                """
HTTPS uses TLS to protect HTTP communication against network
observation and tampering. Certificates help clients establish
the identity of the server they are connecting to.

Modern deployed web applications should use HTTPS for login,
session and other sensitive communication.
                """,
                """
Browser
   ↓
HTTPS / TLS
   ↓
Web Server
                """,
                "",
                "HTTPS protects communication between clients and servers."
            )
        ]
    ),


    # =========================================================
    # 13 AI / ML
    # =========================================================

    make_course(
        "ai",
        "Artificial Intelligence & Machine Learning",
        "🤖",
        "Intermediate → Advanced",
        "Understand AI, machine learning, data preparation, models and practical AI development.",
        [

            make_lesson(
                "ai",
                1,
                "What is AI?",
                """
Artificial intelligence is a broad field concerned with building
systems that perform tasks associated with capabilities such as
perception, reasoning, language processing and decision making.

AI includes many approaches. Machine learning is one major
approach where systems learn patterns from data instead of every
rule being manually specified.
                """,
                """
print("AI system receives input")
print("AI system processes information")
print("AI system produces output")
                """,
                "Python",
                "AI is a broad field; machine learning is one important approach within it."
            ),

            make_lesson(
                "ai",
                2,
                "Machine Learning",
                """
Machine learning algorithms learn patterns from examples.
A model is trained using data and then used to make predictions
or decisions on new data.

A useful mental model is:
data → training → model → prediction.
                """,
                """
training_data = [
    [1, 10],
    [2, 20],
    [3, 30]
]

print("Training data:", training_data)
                """,
                "Python",
                "Machine learning uses data to build models that can generalize to new inputs."
            ),

            make_lesson(
                "ai",
                3,
                "Features and Labels",
                """
In supervised learning, features are the input information
used to make a prediction and the label is the expected target.

For example, a house-price model may use area, location and
number of rooms as features while the selling price is the label.
                """,
                """
features = [
    [1200, 3],
    [1800, 4],
    [900, 2]
]

labels = [
    500000,
    750000,
    350000
]

print(features)
print(labels)
                """,
                "Python",
                "Features describe the input; labels represent the target in supervised learning."
            ),

            make_lesson(
                "ai",
                4,
                "Training and Testing",
                """
A model should not be evaluated only on the same data used for
training. A dataset is commonly divided into training and
evaluation portions.

The goal is to measure how well the learned model performs on
data it has not already seen.
                """,
                """
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = \
    train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )
                """,
                "Python",
                "Separate evaluation data helps measure generalization."
            ),

            make_lesson(
                "ai",
                5,
                "AI APIs",
                """
Modern applications can use hosted AI models through APIs
instead of implementing and training every model locally.

A developer still needs to understand prompts, input validation,
privacy, cost, response handling and failure cases when
integrating an AI service.
                """,
                """
response = {
    "model": "AI",
    "answer": "Generated response"
}

print(response["answer"])
                """,
                "Python",
                "AI integration is also software engineering: APIs, validation and error handling still matter."
            )
        ]
    ),


    # =========================================================
    # 14 CLOUD
    # =========================================================

    make_course(
        "cloud",
        "Cloud Computing",
        "☁️",
        "Intermediate",
        "Understand servers, hosting, storage, deployment and cloud concepts.",
        [

            make_lesson(
                "cloud",
                1,
                "What is Cloud Computing?",
                """
Cloud computing provides computing resources over a network.
Instead of purchasing and maintaining every physical server,
organizations can use hosted infrastructure and services.

Cloud platforms commonly provide compute, storage, databases,
networking and managed services.
                """,
                """
User
 ↓
Internet
 ↓
Cloud Server
 ↓
Application
                """,
                "",
                "Cloud computing provides computing resources as services."
            ),

            make_lesson(
                "cloud",
                2,
                "Web Hosting",
                """
Hosting means making an application available on a server that
users can reach through a network. A Flask application can be
hosted using a production WSGI server such as Gunicorn.

Deployment also requires configuration such as environment
variables, domain settings, logs and database persistence.
                """,
                """
gunicorn app:app
                """,
                "Shell",
                "Deployment turns your local application into a service users can access."
            ),

            make_lesson(
                "cloud",
                3,
                "Environment Variables",
                """
Environment variables allow configuration to be supplied
outside the source code. They are useful for database paths,
secret keys, API credentials and deployment-specific settings.

Keeping configuration outside the repository makes it easier to
deploy the same application in different environments.
                """,
                """
import os

secret = os.getenv(
    "SECRET_KEY"
)

print(bool(secret))
                """,
                "Python",
                "Environment variables separate deployment configuration from source code."
            ),

            make_lesson(
                "cloud",
                4,
                "Persistent Storage",
                """
Application instances can be replaced or restarted. If important
data is stored only in temporary local storage, it may disappear
when the instance changes.

Persistent storage keeps databases and other required data across
restarts according to the hosting provider's configuration.
                """,
                """
DATABASE_PATH=/var/data/codequest.db
                """,
                "",
                "Persistent data needs persistent storage."
            ),

            make_lesson(
                "cloud",
                5,
                "Scaling",
                """
Scaling means increasing a system's capacity as demand grows.
Vertical scaling increases resources for a machine, while
horizontal scaling adds more instances.

Real systems also use caching, queues, load balancing and database
optimization to handle growing traffic.
                """,
                """
Users
  ↓
Load Balancer
  ↓
Server 1
Server 2
Server 3
                """,
                "",
                "Scaling is about handling increasing workload reliably."
            )
        ]
    ),


    # =========================================================
    # 15 DEVOPS / SOFTWARE ENGINEERING
    # =========================================================

    make_course(
        "devops",
        "DevOps & Software Engineering",
        "⚡",
        "Intermediate → Advanced",
        "Learn software development practices, testing, deployment, debugging and maintainability.",
        [

            make_lesson(
                "devops",
                1,
                "Software Development Lifecycle",
                """
Software development is more than writing code. A typical
lifecycle includes understanding requirements, designing the
solution, implementing it, testing it, deploying it and maintaining
it.

Thinking about the entire lifecycle helps developers build
software that remains useful after the first working version.
                """,
                """
Idea
 ↓
Requirements
 ↓
Design
 ↓
Code
 ↓
Test
 ↓
Deploy
 ↓
Monitor
                """,
                "",
                "Software engineering includes planning, implementation, testing and maintenance."
            ),

            make_lesson(
                "devops",
                2,
                "Testing",
                """
Testing checks whether software behaves as expected. Unit tests
focus on small pieces of logic, while integration tests check how
components work together.

Testing does not prove that a program contains no bugs, but it
can catch regressions and make future changes safer.
                """,
                """
def add(a, b):
    return a + b


assert add(2, 3) == 5
                """,
                "Python",
                "Automated tests protect important behavior from regressions."
            ),

            make_lesson(
                "devops",
                3,
                "Debugging",
                """
Debugging is the process of locating and correcting the cause
of incorrect behavior. Good debugging starts with reproducing
the problem and collecting evidence instead of randomly changing
code.

Read error messages carefully. Identify where the failure occurs,
inspect relevant values and make one controlled change at a time.
                """,
                """
try:
    value = int("hello")
except ValueError as error:
    print("Actual error:", error)
                """,
                "Python",
                "Debug from evidence rather than guessing."
            ),

            make_lesson(
                "devops",
                4,
                "CI/CD",
                """
Continuous integration automates checks when code changes are
submitted. Continuous delivery or deployment automates the
process of preparing or releasing software.

A typical pipeline may install dependencies, run tests, build the
application and deploy it when the checks succeed.
                """,
                """
git push
   ↓
Build
   ↓
Tests
   ↓
Deploy
                """,
                "",
                "Automation makes software delivery repeatable."
            ),

            make_lesson(
                "devops",
                5,
                "Logs",
                """
Logs provide evidence about what an application is doing.
Useful logs include timestamps, severity and meaningful context.

Production debugging often depends on logs because developers
cannot directly observe every user's environment.
                """,
                """
import logging

logging.basicConfig(level=logging.INFO)

logging.info(
    "CodeQuest API started"
)
                """,
                "Python",
                "Good logs make deployed systems easier to understand."
            )
        ]
    ),


    # =========================================================
    # 16 CAREER / PROJECTS
    # =========================================================

    make_course(
        "career",
        "Career Preparation & Projects",
        "🚀",
        "Beginner → Job Ready",
        "Turn technical learning into projects, portfolio evidence, interviews and career preparation.",
        [

            make_lesson(
                "career",
                1,
                "Build Projects",
                """
Projects convert knowledge into evidence. Instead of only saying
that you know Python, a project can demonstrate that you can
design a feature, write code, handle data, debug problems and
deploy software.

Start with a small problem and improve it gradually. A finished
small project is more useful for learning than an enormous
unfinished idea.
                """,
                """
Project idea:

Student Task Manager

Features:
- Add task
- Complete task
- Save task
- Display progress
                """,
                "",
                "Projects demonstrate how you apply skills."
            ),

            make_lesson(
                "career",
                2,
                "GitHub Portfolio",
                """
A developer portfolio should make it easy for another person
to understand what you have built. Include a clear README,
screenshots, technology choices, setup instructions and a
description of what you personally implemented.

Do not simply upload a large project without explaining it.
                """,
                """
README

# Project Name

## Problem

## Features

## Tech Stack

## How to Run

## Screenshots

## Future Scope
                """,
                "",
                "Make your repository understandable to someone who has never seen it before."
            ),

            make_lesson(
                "career",
                3,
                "Resume Projects",
                """
A project description should focus on what you built and what
technical work you performed. Instead of writing only "Made a
website", explain the technologies and useful features.

Good project descriptions are specific and honest. Do not claim
tools or responsibilities that you did not actually use.
                """,
                """
Example:

CodeQuest AI
- Flask backend
- Firebase authentication
- SQLite persistence
- Gamified learning system
- Multi-language code execution
                """,
                "",
                "Describe your actual technical contribution clearly."
            ),

            make_lesson(
                "career",
                4,
                "Interview Preparation",
                """
Technical interviews commonly test programming fundamentals,
problem solving, data structures, databases, operating systems,
networks and project understanding depending on the role.

Prepare by explaining concepts in your own words and practicing
problems rather than memorizing answers.
                """,
                """
Practice:

Explain a variable.
Explain a loop.
Explain an array.
Explain a database.
Explain your project architecture.
Explain one difficult bug you fixed.
                """,
                "",
                "Be able to explain what you know and what you built."
            ),

            make_lesson(
                "career",
                5,
                "Communication Skills",
                """
Technical ability becomes more useful when you can communicate
your reasoning. When explaining a project, describe the problem,
your approach, important design decisions and the result.

If you do not know something during an interview or project
discussion, explain what you do know and describe how you would
investigate the missing information.
                """,
                """
Problem
→ Approach
→ Implementation
→ Challenge
→ Solution
→ Result
                """,
                "",
                "Clear communication helps others understand your technical work."
            ),

            make_lesson(
                "career",
                6,
                "Internship and Job Roadmap",
                """
A practical career journey can be divided into stages. First
build programming fundamentals. Then learn data structures,
databases, Git and a development stack. Next build several
projects and publish them. Finally practice interviews and apply
for opportunities that match your skills.

The exact path differs by role, so use the career pathway that
matches the type of work you want to explore.
                """,
                """
FOUNDATION
   ↓
PROGRAMMING
   ↓
DSA + SQL + GIT
   ↓
DEVELOPMENT
   ↓
PROJECTS
   ↓
PORTFOLIO
   ↓
INTERVIEW
   ↓
APPLICATIONS
                """,
                "",
                "Career preparation is a progression from fundamentals to demonstrated skills."
            )
        ]
    )
]


# =============================================================
# CAREER PATHWAYS
# =============================================================

career_paths = [

    {
        "id": "software-developer",
        "title": "Software Developer",
        "icon": "💻",
        "description": "Build applications, services and software systems.",
        "steps": [
            "Programming fundamentals",
            "C / C++ / Python",
            "Data Structures & Algorithms",
            "Git & GitHub",
            "SQL",
            "Web or backend development",
            "Projects",
            "Interview preparation"
        ],
        "skills": [
            "Programming",
            "Problem solving",
            "Git",
            "SQL",
            "APIs",
            "Debugging",
            "Testing"
        ],
        "projects": [
            "Student management system",
            "Task manager",
            "REST API",
            "Full-stack college project"
        ]
    },

    {
        "id": "full-stack",
        "title": "Full-Stack Developer",
        "icon": "🌐",
        "description": "Build complete web applications from interface to database.",
        "steps": [
            "HTML",
            "CSS",
            "JavaScript",
            "Frontend framework",
            "Backend",
            "REST APIs",
            "SQL / NoSQL",
            "Authentication",
            "Deployment"
        ],
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "Backend development",
            "Databases",
            "APIs",
            "Deployment"
        ],
        "projects": [
            "Student portal",
            "E-commerce application",
            "College event platform",
            "Learning management system"
        ]
    },

    {
        "id": "ai-ml",
        "title": "AI / ML Engineer",
        "icon": "🤖",
        "description": "Build software using machine learning and AI technologies.",
        "steps": [
            "Python",
            "Mathematics",
            "NumPy",
            "Pandas",
            "Data preparation",
            "Machine learning",
            "Model evaluation",
            "AI APIs",
            "Projects"
        ],
        "skills": [
            "Python",
            "Statistics",
            "Data handling",
            "Machine learning",
            "Model evaluation",
            "AI APIs"
        ],
        "projects": [
            "Student performance predictor",
            "Recommendation system",
            "Text classifier",
            "AI study assistant"
        ]
    },

    {
        "id": "cybersecurity",
        "title": "Cybersecurity",
        "icon": "🛡️",
        "description": "Learn defensive security, networks, authentication and secure development.",
        "steps": [
            "Computer fundamentals",
            "Networking",
            "Linux",
            "Authentication",
            "Web security",
            "Secure coding",
            "Security monitoring",
            "Practical labs"
        ],
        "skills": [
            "Networking",
            "Linux",
            "Security fundamentals",
            "Secure coding",
            "Authentication",
            "Monitoring"
        ],
        "projects": [
            "Password security demo",
            "Secure login system",
            "Network monitoring dashboard",
            "Security checklist tool"
        ]
    },

    {
        "id": "cloud-devops",
        "title": "Cloud & DevOps",
        "icon": "☁️",
        "description": "Learn deployment, automation, cloud infrastructure and reliable software delivery.",
        "steps": [
            "Linux",
            "Git",
            "Networking",
            "Python / scripting",
            "Docker",
            "CI/CD",
            "Cloud platform",
            "Monitoring"
        ],
        "skills": [
            "Linux",
            "Git",
            "Networking",
            "Docker",
            "CI/CD",
            "Cloud",
            "Monitoring"
        ],
        "projects": [
            "Deploy Flask application",
            "CI/CD pipeline",
            "Dockerized API",
            "Cloud-hosted database application"
        ]
    },

    {
        "id": "data-analyst",
        "title": "Data Analyst",
        "icon": "📊",
        "description": "Turn structured data into useful information and reports.",
        "steps": [
            "Excel",
            "SQL",
            "Statistics",
            "Python",
            "Pandas",
            "Data visualization",
            "Projects",
            "Portfolio"
        ],
        "skills": [
            "Excel",
            "SQL",
            "Python",
            "Statistics",
            "Data visualization",
            "Reporting"
        ],
        "projects": [
            "Student performance dashboard",
            "College attendance analysis",
            "Sales dashboard",
            "Survey analysis"
        ]
    }
]


# =============================================================
# PRO TRICKS / SKILLS
# =============================================================

pro_skills = [

    {
        "id": "debugging",
        "title": "Debugging Tricks",
        "icon": "🐛",
        "items": [
            "Read the first meaningful error instead of the last line only.",
            "Reproduce the bug consistently before changing code.",
            "Print or inspect important variable values.",
            "Change one thing at a time.",
            "Check assumptions about API responses.",
            "Use small test cases before testing the entire application."
        ]
    },

    {
        "id": "coding",
        "title": "Coding Skills",
        "icon": "⌨️",
        "items": [
            "Use meaningful variable names.",
            "Keep functions focused.",
            "Avoid unnecessary duplicated code.",
            "Validate external input.",
            "Write comments for decisions, not obvious syntax.",
            "Learn to read documentation."
        ]
    },

    {
        "id": "git",
        "title": "Git Skills",
        "icon": "🐙",
        "items": [
            "Commit logical changes.",
            "Write useful commit messages.",
            "Use branches for experiments.",
            "Never commit secrets.",
            "Read git diff before committing.",
            "Keep the README updated."
        ]
    },

    {
        "id": "college",
        "title": "College Project Skills",
        "icon": "🎓",
        "items": [
            "Start with a clear problem statement.",
            "Create a feature list before coding.",
            "Build a minimum working version first.",
            "Keep screenshots and documentation.",
            "Use GitHub from the beginning.",
            "Prepare a short demo and architecture explanation."
        ]
    },

    {
        "id": "interview",
        "title": "Interview Skills",
        "icon": "💼",
        "items": [
            "Explain your project in simple language.",
            "Understand the code you submit.",
            "Practice arrays, strings and basic DSA.",
            "Revise SQL.",
            "Know basic OS and networking concepts.",
            "Practice explaining how you debugged a real problem."
        ]
    },

    {
        "id": "terminal",
        "title": "Developer Terminal Skills",
        "icon": "🖥️",
        "items": [
            "pwd - show current directory",
            "ls - list files",
            "cd - change directory",
            "mkdir - create directory",
            "git status - inspect repository state",
            "python -m venv .venv - create Python environment"
        ]
    }
]


# =============================================================
# QUIZ BANK
# =============================================================

def q(
    qid,
    topic,
    question,
    options,
    answer,
    difficulty="Easy"
):
    return {
        "id": qid,
        "topic": topic,
        "question": question,
        "options": options,
        "answer": answer,
        "difficulty": difficulty
    }


quiz_bank = [

    q(
        "cb001",
        "Computer Basics",
        "Which component executes program instructions?",
        ["CPU", "Monitor", "Keyboard", "Speaker"],
        "CPU"
    ),

    q(
        "cb002",
        "Computer Basics",
        "Which memory is normally used as working memory?",
        ["RAM", "SSD", "DVD", "Keyboard"],
        "RAM"
    ),

    q(
        "cb003",
        "Computer Basics",
        "What does CPU stand for?",
        [
            "Central Processing Unit",
            "Computer Personal Unit",
            "Central Program Utility",
            "Computer Processing Utility"
        ],
        "Central Processing Unit"
    ),

    q(
        "cb004",
        "Computer Basics",
        "Which device provides persistent storage?",
        ["SSD", "RAM", "CPU", "Monitor"],
        "SSD"
    ),

    q(
        "cb005",
        "Computer Basics",
        "What is binary mainly based on?",
        ["0 and 1", "1 and 2", "A and B", "10 and 20"],
        "0 and 1"
    ),

    q(
        "cb006",
        "Computer Basics",
        "Which software manages computer resources?",
        [
            "Operating system",
            "Text document",
            "Image file",
            "Spreadsheet"
        ],
        "Operating system"
    ),

    q(
        "cb007",
        "Computer Basics",
        "What is hardware?",
        [
            "Physical computer components",
            "Only programming languages",
            "Internet websites",
            "User passwords"
        ],
        "Physical computer components"
    ),

    q(
        "cb008",
        "Computer Basics",
        "Which is an example of software?",
        [
            "Web browser",
            "Keyboard",
            "RAM",
            "SSD"
        ],
        "Web browser"
    ),

    q(
        "git001",
        "Git",
        "Which command creates a Git repository?",
        [
            "git init",
            "git start",
            "git create",
            "git repository"
        ],
        "git init"
    ),

    q(
        "git002",
        "Git",
        "Which command records staged changes?",
        [
            "git commit",
            "git save",
            "git record",
            "git store"
        ],
        "git commit"
    ),

    q(
        "git003",
        "Git",
        "Which command shows repository status?",
        [
            "git status",
            "git check",
            "git state",
            "git info"
        ],
        "git status"
    ),

    q(
        "git004",
        "Git",
        "What is a branch used for?",
        [
            "Independent development",
            "Deleting the repository",
            "Formatting a disk",
            "Installing Python"
        ],
        "Independent development"
    ),

    q(
        "c001",
        "C",
        "Which function is the usual entry point of a C program?",
        ["main", "start", "run", "begin"],
        "main"
    ),

    q(
        "c002",
        "C",
        "Which header provides printf?",
        ["stdio.h", "math.h", "string.h", "stdlib.hpp"],
        "stdio.h"
    ),

    q(
        "c003",
        "C",
        "Which type commonly stores an integer?",
        ["int", "char[]", "float[]", "void[]"],
        "int"
    ),

    q(
        "c004",
        "C",
        "Which symbol is used to take the address of a variable?",
        ["&", "*", "#", "%"],
        "&"
    ),

    q(
        "c005",
        "C",
        "Which structure repeats code while a condition is true?",
        ["while", "if", "switch", "struct"],
        "while"
    ),

    q(
        "c006",
        "C",
        "Which data structure stores multiple values of the same type?",
        ["Array", "Comment", "Function", "Header"],
        "Array"
    ),

    q(
        "c007",
        "C",
        "Which keyword defines a structure?",
        ["struct", "record", "object", "class"],
        "struct"
    ),

    q(
        "c008",
        "C",
        "Which function prints formatted output?",
        ["printf", "scanf", "malloc", "strlen"],
        "printf"
    ),

    q(
        "cpp001",
        "C++",
        "Which stream is commonly used for console output in C++?",
        ["cout", "cin", "printf", "output"],
        "cout"
    ),

    q(
        "cpp002",
        "C++",
        "What is an object?",
        [
            "An instance of a class",
            "A compiler",
            "A header file",
            "A loop"
        ],
        "An instance of a class"
    ),

    q(
        "cpp003",
        "C++",
        "Which STL container is a dynamic array?",
        ["vector", "stackfile", "arraylist", "dynamic"],
        "vector"
    ),

    q(
        "cpp004",
        "C++",
        "Which keyword enables runtime polymorphism in a base function?",
        ["virtual", "static", "const", "friend"],
        "virtual"
    ),

    q(
        "python001",
        "Python",
        "Which function displays output?",
        ["print()", "display()", "show()", "write()"],
        "print()"
    ),

    q(
        "python002",
        "Python",
        "Which collection stores key-value pairs?",
        ["Dictionary", "Tuple", "String", "Set only"],
        "Dictionary"
    ),

    q(
        "python003",
        "Python",
        "Which keyword defines a function?",
        ["def", "function", "fun", "define"],
        "def"
    ),

    q(
        "python004",
        "Python",
        "Which keyword handles exceptions?",
        ["try", "check", "error", "catching"],
        "try"
    ),

    q(
        "python005",
        "Python",
        "Which symbol begins a Python comment?",
        ["#", "//", "<!--", "/*"],
        "#"
    ),

    q(
        "python006",
        "Python",
        "Which method adds an item to a list?",
        ["append()", "addItem()", "pushValue()", "insertEnd()"],
        "append()"
    ),

    q(
        "web001",
        "Web",
        "Which language defines webpage structure?",
        ["HTML", "CSS", "SQL", "Python"],
        "HTML"
    ),

    q(
        "web002",
        "Web",
        "Which language controls webpage styling?",
        ["CSS", "HTML", "SQL", "C"],
        "CSS"
    ),

    q(
        "web003",
        "Web",
        "Which language commonly adds browser interactivity?",
        ["JavaScript", "SQL", "C", "Markdown"],
        "JavaScript"
    ),

    q(
        "web004",
        "Web",
        "What does DOM stand for?",
        [
            "Document Object Model",
            "Data Object Machine",
            "Document Output Method",
            "Digital Object Manager"
        ],
        "Document Object Model"
    ),

    q(
        "web005",
        "Web",
        "Which browser API is commonly used for HTTP requests?",
        ["fetch()", "requestPage()", "http()", "browserGet()"],
        "fetch()"
    ),

    q(
        "db001",
        "DBMS",
        "Which SQL command retrieves data?",
        ["SELECT", "GET", "READ", "FETCH"],
        "SELECT"
    ),

    q(
        "db002",
        "DBMS",
        "Which SQL command adds a row?",
        ["INSERT", "ADD", "PUT", "CREATE ROW"],
        "INSERT"
    ),

    q(
        "db003",
        "DBMS",
        "What uniquely identifies a table row?",
        ["Primary key", "Foreign screen", "Index page", "Column title"],
        "Primary key"
    ),

    q(
        "db004",
        "DBMS",
        "Which SQL command changes existing data?",
        ["UPDATE", "CHANGE", "MODIFY ROW", "ALTER DATA"],
        "UPDATE"
    ),

    q(
        "db005",
        "DBMS",
        "Which SQL command removes rows?",
        ["DELETE", "REMOVE", "DROP ROW", "ERASE"],
        "DELETE"
    ),

    q(
        "dsa001",
        "DSA",
        "Which principle does a stack follow?",
        ["LIFO", "FIFO", "Random", "Sorted"],
        "LIFO"
    ),

    q(
        "dsa002",
        "DSA",
        "Which principle does a queue follow?",
        ["FIFO", "LIFO", "Random", "Reverse"],
        "FIFO"
    ),

    q(
        "dsa003",
        "DSA",
        "Binary search requires what type of data?",
        ["Sorted data", "Encrypted data", "Random data", "Image data"],
        "Sorted data"
    ),

    q(
        "dsa004",
        "DSA",
        "What does Big O help describe?",
        [
            "Algorithm growth",
            "Screen size",
            "Programming language age",
            "File extension"
        ],
        "Algorithm growth"
    ),

    q(
        "dsa005",
        "DSA",
        "Which structure commonly provides key-value lookup?",
        ["Hash table", "Stack only", "Queue only", "Graph edge"],
        "Hash table"
    ),

    q(
        "os001",
        "Operating Systems",
        "What is a process?",
        [
            "A running instance of a program",
            "A file extension",
            "A database table",
            "A keyboard command"
        ],
        "A running instance of a program"
    ),

    q(
        "os002",
        "Operating Systems",
        "What does CPU scheduling decide?",
        [
            "Which task receives CPU time",
            "Which monitor is used",
            "Which file extension is valid",
            "Which password is correct"
        ],
        "Which task receives CPU time"
    ),

    q(
        "os003",
        "Operating Systems",
        "Which component manages files and memory?",
        [
            "Operating system",
            "HTML",
            "Database query",
            "Compiler only"
        ],
        "Operating system"
    ),

    q(
        "net001",
        "Networks",
        "What does DNS primarily translate?",
        [
            "Domain names to network addresses",
            "Passwords to usernames",
            "HTML to CSS",
            "C to Python"
        ],
        "Domain names to network addresses"
    ),

    q(
        "net002",
        "Networks",
        "Which protocol is commonly used for web communication?",
        ["HTTP", "FTP only", "RAM", "CPU"],
        "HTTP"
    ),

    q(
        "net003",
        "Networks",
        "What does an IP address identify?",
        [
            "A network interface/address",
            "A programming variable",
            "A database table",
            "A CPU instruction"
        ],
        "A network interface/address"
    ),

    q(
        "net004",
        "Networks",
        "What is a port used for?",
        [
            "Identifying a network service",
            "Storing RAM",
            "Formatting code",
            "Creating a variable"
        ],
        "Identifying a network service"
    ),

    q(
        "sec001",
        "Cybersecurity",
        "What should applications do with external input?",
        [
            "Validate it",
            "Always trust it",
            "Execute it",
            "Store it as a password"
        ],
        "Validate it"
    ),

    q(
        "sec002",
        "Cybersecurity",
        "How should production passwords normally be stored?",
        [
            "Using secure password hashes",
            "Plain text",
            "Inside HTML",
            "Inside a public README"
        ],
        "Using secure password hashes"
    ),

    q(
        "sec003",
        "Cybersecurity",
        "What does HTTPS protect?",
        [
            "Network communication",
            "CPU temperature",
            "Keyboard hardware",
            "Source-code indentation"
        ],
        "Network communication"
    ),

    q(
        "ai001",
        "AI",
        "What is machine learning?",
        [
            "A way for systems to learn patterns from data",
            "A type of monitor",
            "A database format",
            "A networking cable"
        ],
        "A way for systems to learn patterns from data"
    ),

    q(
        "ai002",
        "AI",
        "What are features in supervised learning?",
        [
            "Input variables",
            "Only output labels",
            "Passwords",
            "Compiler errors"
        ],
        "Input variables"
    ),

    q(
        "ai003",
        "AI",
        "Why separate training and test data?",
        [
            "To evaluate generalization",
            "To make files larger",
            "To remove Python",
            "To increase screen resolution"
        ],
        "To evaluate generalization"
    ),

    q(
        "cloud001",
        "Cloud",
        "What is cloud computing?",
        [
            "Using computing resources as services",
            "Only storing photos",
            "A type of keyboard",
            "A programming language"
        ],
        "Using computing resources as services"
    ),

    q(
        "cloud002",
        "Cloud",
        "Why use environment variables?",
        [
            "To separate configuration from source code",
            "To replace all databases",
            "To compile C",
            "To design HTML"
        ],
        "To separate configuration from source code"
    ),

    q(
        "dev001",
        "DevOps",
        "What is CI commonly used for?",
        [
            "Automated build and test checks",
            "Changing monitor brightness",
            "Writing HTML manually",
            "Deleting Git history"
        ],
        "Automated build and test checks"
    ),

    q(
        "dev002",
        "DevOps",
        "What is debugging?",
        [
            "Finding and correcting causes of incorrect behavior",
            "Installing a monitor",
            "Creating a password",
            "Compressing an image"
        ],
        "Finding and correcting causes of incorrect behavior"
    ),

    q(
        "career001",
        "Career",
        "What makes a technical project useful in a portfolio?",
        [
            "A clear explanation and evidence of your work",
            "Only a project name",
            "No documentation",
            "Copied code without explanation"
        ],
        "A clear explanation and evidence of your work"
    ),

    q(
        "career002",
        "Career",
        "Which skill is useful for almost every developer role?",
        [
            "Problem solving",
            "Avoiding documentation",
            "Never testing code",
            "Ignoring errors"
        ],
        "Problem solving"
    )
]


# =============================================================
# EXTRA QUESTION GENERATOR
# =============================================================

def build_extra_questions():

    extra = []

    for i in range(1, 21):

        extra.append(
            q(
                f"python_extra_{i}",
                "Python",
                f"Which language is this CodeQuest lesson practicing? Python example #{i}",
                [
                    "Python",
                    "C",
                    "Java",
                    "HTML"
                ],
                "Python"
            )
        )

    for i in range(1, 21):

        extra.append(
            q(
                f"c_extra_{i}",
                "C",
                f"Which language commonly uses printf? C practice #{i}",
                [
                    "C",
                    "Python",
                    "HTML",
                    "SQL"
                ],
                "C"
            )
        )

    for i in range(1, 21):

        extra.append(
            q(
                f"web_extra_{i}",
                "Web",
                f"Which language is responsible for webpage structure? Web practice #{i}",
                [
                    "HTML",
                    "CSS",
                    "Python",
                    "SQL"
                ],
                "HTML"
            )
        )

    for i in range(1, 21):

        extra.append(
            q(
                f"db_extra_{i}",
                "DBMS",
                f"Which command is used to retrieve rows? SQL practice #{i}",
                [
                    "SELECT",
                    "INSERT",
                    "DELETE",
                    "UPDATE"
                ],
                "SELECT"
            )
        )

    for i in range(1, 21):

        extra.append(
            q(
                f"dsa_extra_{i}",
                "DSA",
                f"What does FIFO mean? DSA practice #{i}",
                [
                    "First In First Out",
                    "First Input Final Output",
                    "Fast Input Fast Output",
                    "File In File Out"
                ],
                "First In First Out"
            )
        )

    return extra


quiz_bank.extend(build_extra_questions())


# =============================================================
# AUTH HELPERS
# =============================================================

def get_bearer_token():

    header = request.headers.get(
        "Authorization",
        ""
    )

    if header.startswith("Bearer "):
        return header[7:].strip()

    data = request.get_json(
        silent=True
    ) or {}

    token = data.get("idToken")

    if token:
        return str(token).strip()

    return ""


def verify_firebase_token():

    if not firebase_ready or firebase_auth is None:
        return None

    token = get_bearer_token()

    if not token:
        return None

    try:
        decoded = firebase_auth.verify_id_token(
            token
        )

        return decoded

    except Exception as exc:

        print(
            "Firebase token verification failed:",
            exc
        )

        return None


def current_uid(optional=True):

    uid = session.get("uid")

    if uid:
        return uid

    decoded = verify_firebase_token()

    if decoded:

        uid = decoded.get("uid")

        if uid:
            session["uid"] = uid

            return uid

    if optional:
        return None

    return None


def require_auth(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        uid = current_uid(
            optional=False
        )

        if not uid:

            return jsonify({
                "success": False,
                "error": "Authentication required."
            }), 401

        return function(
            uid,
            *args,
            **kwargs
        )

    return wrapper


# =============================================================
# USER HELPERS
# =============================================================

def upsert_user(
    uid,
    email="",
    name="",
    photo_url=""
):

    now = now_iso()

    conn = get_db()

    existing = conn.execute(
        "SELECT uid FROM users WHERE uid = ?",
        (uid,)
    ).fetchone()

    if existing:

        conn.execute(
            """
            UPDATE users
            SET email = ?,
                name = ?,
                photo_url = ?,
                updated_at = ?
            WHERE uid = ?
            """,
            (
                email,
                name,
                photo_url,
                now,
                uid
            )
        )

    else:

        conn.execute(
            """
            INSERT INTO users(
                uid,
                email,
                name,
                photo_url,
                xp,
                level,
                streak,
                created_at,
                updated_at
            )
            VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (
                uid,
                email,
                name,
                photo_url,
                0,
                1,
                0,
                now,
                now
            )
        )

    conn.commit()
    conn.close()


def level_from_xp(xp):

    if xp < 100:
        return 1

    return min(
        100,
        (xp // 100) + 1
    )


def award_xp(
    uid,
    amount
):

    amount = max(
        0,
        int(amount)
    )

    if amount == 0:
        return

    conn = get_db()

    row = conn.execute(
        "SELECT xp FROM users WHERE uid = ?",
        (uid,)
    ).fetchone()

    if not row:
        conn.close()
        return

    new_xp = int(row["xp"]) + amount

    conn.execute(
        """
        UPDATE users
        SET xp = ?,
            level = ?,
            updated_at = ?
        WHERE uid = ?
        """,
        (
            new_xp,
            level_from_xp(new_xp),
            now_iso(),
            uid
        )
    )

    conn.commit()
    conn.close()


def update_streak(uid):

    conn = get_db()

    row = conn.execute(
        """
        SELECT streak, last_active
        FROM users
        WHERE uid = ?
        """,
        (uid,)
    ).fetchone()

    if not row:
        conn.close()
        return

    today = datetime.now(
        timezone.utc
    ).date()

    old_streak = int(
        row["streak"] or 0
    )

    last = row["last_active"]

    if not last:

        streak = 1

    else:

        try:

            previous = datetime.fromisoformat(
                last
            ).date()

            difference = (
                today - previous
            ).days

            if difference == 0:

                streak = old_streak

            elif difference == 1:

                streak = old_streak + 1

            else:

                streak = 1

        except Exception:

            streak = 1

    conn.execute(
        """
        UPDATE users
        SET streak = ?,
            last_active = ?,
            updated_at = ?
        WHERE uid = ?
        """,
        (
            streak,
            now_iso(),
            now_iso(),
            uid
        )
    )

    conn.commit()
    conn.close()


# =============================================================
# ACHIEVEMENTS
# =============================================================

ACHIEVEMENTS = [

    {
        "id": "first-lesson",
        "title": "First Step",
        "description": "Complete your first lesson.",
        "icon": "🌟"
    },

    {
        "id": "first-quiz",
        "title": "Quiz Rookie",
        "description": "Complete your first quiz.",
        "icon": "🧠"
    },

    {
        "id": "perfect-quiz",
        "title": "Perfect Run",
        "description": "Answer every question correctly.",
        "icon": "💯"
    },

    {
        "id": "coder",
        "title": "Code Runner",
        "description": "Run code in Code Arena.",
        "icon": "💻"
    },

    {
        "id": "career-path",
        "title": "Path Finder",
        "description": "Explore a career pathway.",
        "icon": "🗺️"
    },

    {
        "id": "xp-500",
        "title": "XP Hunter",
        "description": "Earn 500 XP.",
        "icon": "⚡"
    },

    {
        "id": "xp-1000",
        "title": "Code Warrior",
        "description": "Earn 1000 XP.",
        "icon": "🏆"
    }
]


def unlock(
    uid,
    achievement_id
):

    conn = get_db()

    conn.execute(
        """
        INSERT OR IGNORE INTO achievements(
            uid,
            achievement_id,
            unlocked_at
        )
        VALUES(?,?,?)
        """,
        (
            uid,
            achievement_id,
            now_iso()
        )
    )

    conn.commit()
    conn.close()


def check_xp_achievements(uid):

    conn = get_db()

    row = conn.execute(
        "SELECT xp FROM users WHERE uid = ?",
        (uid,)
    ).fetchone()

    conn.close()

    if not row:
        return

    xp = int(row["xp"])

    if xp >= 500:
        unlock(
            uid,
            "xp-500"
        )

    if xp >= 1000:
        unlock(
            uid,
            "xp-1000"
        )


# =============================================================
# HOME
# =============================================================

@app.get("/")
def home():

    return jsonify({
        "success": True,
        "app": "CodeQuest AI",
        "tagline": "Learn • Practice • Play • Build",
        "version": "2.0",
        "message": "CodeQuest AI backend is running."
    })


# =============================================================
# HEALTH
# =============================================================

@app.get("/health")
def health():

    compiler = "Wandbox"

    return jsonify({
        "success": True,
        "status": "healthy",
        "app": "CodeQuest AI",
        "database": DATABASE_PATH,
        "firebase": firebase_ready,
        "compiler": compiler,
        "courses": len(courses),
        "lessons": sum(
            len(c["chapters"])
            for c in courses
        ),
        "questions": len(quiz_bank)
    })


# =============================================================
# FIREBASE LOGIN
# =============================================================

@app.post("/api/firebase-login")
def firebase_login():

    if not firebase_ready:

        return jsonify({
            "success": False,
            "error": (
                "Firebase Admin is not configured on the server. "
                "Add FIREBASE_SERVICE_ACCOUNT_JSON to Render."
            )
        }), 503

    token = get_bearer_token()

    if not token:

        return jsonify({
            "success": False,
            "error": "Firebase ID token is missing."
        }), 400

    try:

        decoded = firebase_auth.verify_id_token(
            token
        )

        uid = decoded.get("uid")

        email = decoded.get(
            "email",
            ""
        )

        name = decoded.get(
            "name",
            ""
        )

        picture = decoded.get(
            "picture",
            ""
        )

        if not uid:

            return jsonify({
                "success": False,
                "error": "Firebase token has no UID."
            }), 401

        upsert_user(
            uid,
            email,
            name,
            picture
        )

        session["uid"] = uid

        update_streak(uid)

        conn = get_db()

        row = conn.execute(
            "SELECT * FROM users WHERE uid = ?",
            (uid,)
        ).fetchone()

        conn.close()

        return jsonify({
            "success": True,
            "user": dict(row)
        })

    except Exception as exc:

        return jsonify({
            "success": False,
            "error": "Firebase authentication failed."
        }), 401


# =============================================================
# LOGOUT
# =============================================================

@app.post("/api/logout")
def logout():

    session.clear()

    return jsonify({
        "success": True
    })


# =============================================================
# CURRENT USER
# =============================================================

@app.get("/api/me")
def me():

    uid = current_uid()

    if not uid:

        return jsonify({
            "authenticated": False
        })

    conn = get_db()

    row = conn.execute(
        "SELECT * FROM users WHERE uid = ?",
        (uid,)
    ).fetchone()

    conn.close()

    if not row:

        return jsonify({
            "authenticated": False
        })

    return jsonify({
        "authenticated": True,
        "user": dict(row)
    })


# =============================================================
# COURSES
# =============================================================

@app.get("/api/courses")
def api_courses():

    result = []

    for c in courses:

        result.append({
            "id": c["id"],
            "title": c["title"],
            "icon": c["icon"],
            "level": c["level"],
            "description": c["description"],
            "chapters": [
                {
                    "id": chapter["id"],
                    "number": chapter["number"],
                    "title": chapter["title"],
                    "lesson": chapter["lesson"],
                    "sample": chapter["sample"],
                    "language": chapter["language"],
                    "takeaway": chapter["takeaway"]
                }
                for chapter in c["chapters"]
            ]
        })

    return jsonify({
        "success": True,
        "courses": result
    })


@app.get("/api/course/<course_id>")
def api_course(course_id):

    for c in courses:

        if c["id"] == course_id:

            return jsonify({
                "success": True,
                "course": c
            })

    return jsonify({
        "success": False,
        "error": "Course not found."
    }), 404


@app.get("/api/lesson/<lesson_id>")
def api_lesson(lesson_id):

    for c in courses:

        for chapter in c["chapters"]:

            if chapter["id"] == lesson_id:

                return jsonify({
                    "success": True,
                    "course": c["title"],
                    "lesson": chapter
                })

    return jsonify({
        "success": False,
        "error": "Lesson not found."
    }), 404


# =============================================================
# ROADMAP
# =============================================================

@app.get("/api/roadmap")
def roadmap():

    result = []

    for index, c in enumerate(courses, start=1):

        result.append({
            "order": index,
            "id": c["id"],
            "title": c["title"],
            "icon": c["icon"],
            "level": c["level"],
            "lessons": len(
                c["chapters"]
            )
        })

    return jsonify({
        "success": True,
        "roadmap": result
    })


# =============================================================
# CAREER
# =============================================================

@app.get("/api/careers")
def careers():

    return jsonify({
        "success": True,
        "careers": career_paths
    })


@app.get("/api/career-roadmap/<career_id>")
def career_roadmap(career_id):

    for career in career_paths:

        if career["id"] == career_id:

            return jsonify({
                "success": True,
                "career": career
            })

    return jsonify({
        "success": False,
        "error": "Career pathway not found."
    }), 404


# =============================================================
# PRO SKILLS
# =============================================================

@app.get("/api/pro-skills")
def get_pro_skills():

    return jsonify({
        "success": True,
        "skills": pro_skills
    })


# =============================================================
# ACHIEVEMENTS
# =============================================================

@app.get("/api/achievements")
def get_achievements():

    uid = current_uid()

    unlocked = set()

    if uid:

        conn = get_db()

        rows = conn.execute(
            """
            SELECT achievement_id
            FROM achievements
            WHERE uid = ?
            """,
            (uid,)
        ).fetchall()

        conn.close()

        unlocked = {
            row["achievement_id"]
            for row in rows
        }

    result = []

    for achievement in ACHIEVEMENTS:

        item = dict(achievement)

        item["unlocked"] = (
            achievement["id"]
            in unlocked
        )

        result.append(item)

    return jsonify({
        "success": True,
        "achievements": result
    })


# =============================================================
# COMPLETE LESSON
# =============================================================

@app.post("/api/progress/lesson")
@require_auth
def complete_lesson(uid):

    data = request.get_json(
        silent=True
    ) or {}

    lesson_id = str(
        data.get("lessonId", "")
    ).strip()

    course_id = str(
        data.get("courseId", "")
    ).strip()

    if not lesson_id:

        return jsonify({
            "success": False,
            "error": "lessonId is required."
        }), 400

    conn = get_db()

    already = conn.execute(
        """
        SELECT completed
        FROM lesson_progress
        WHERE uid = ?
        AND lesson_id = ?
        """,
        (
            uid,
            lesson_id
        )
    ).fetchone()

    if already and int(
        already["completed"]
    ) == 1:

        conn.close()

        return jsonify({
            "success": True,
            "alreadyCompleted": True,
            "xpEarned": 0
        })

    conn.execute(
        """
        INSERT INTO lesson_progress(
            uid,
            lesson_id,
            course_id,
            completed,
            completed_at
        )
        VALUES(?,?,?,?,?)
        ON CONFLICT(uid,lesson_id)
        DO UPDATE SET
            completed=1,
            completed_at=excluded.completed_at
        """,
        (
            uid,
            lesson_id,
            course_id,
            1,
            now_iso()
        )
    )

    conn.commit()
    conn.close()

    xp = 20

    award_xp(
        uid,
        xp
    )

    update_streak(uid)

    unlock(
        uid,
        "first-lesson"
    )

    check_xp_achievements(
        uid
    )

    return jsonify({
        "success": True,
        "alreadyCompleted": False,
        "xpEarned": xp
    })


# =============================================================
# STATS
# =============================================================

@app.get("/api/stats")
@require_auth
def stats(uid):

    conn = get_db()

    user = conn.execute(
        """
        SELECT xp, level, streak
        FROM users
        WHERE uid = ?
        """,
        (uid,)
    ).fetchone()

    completed = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM lesson_progress
        WHERE uid = ?
        AND completed = 1
        """,
        (uid,)
    ).fetchone()["count"]

    quizzes = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM quiz_attempts
        WHERE uid = ?
        AND status = 'completed'
        """,
        (uid,)
    ).fetchone()["count"]

    conn.close()

    return jsonify({
        "success": True,
        "xp": int(user["xp"]) if user else 0,
        "level": int(user["level"]) if user else 1,
        "streak": int(user["streak"]) if user else 0,
        "completed": int(completed),
        "quizzes": int(quizzes)
    })


@app.get("/api/progress")
@require_auth
def progress(uid):

    conn = get_db()

    lessons = conn.execute(
        """
        SELECT lesson_id, course_id, completed
        FROM lesson_progress
        WHERE uid = ?
        """,
        (uid,)
    ).fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "lessons": [
            dict(row)
            for row in lessons
        ]
    })


# =============================================================
# QUIZ HELPERS
# =============================================================

def get_seen_questions(uid):

    if not uid:
        return set()

    conn = get_db()

    rows = conn.execute(
        """
        SELECT question_id
        FROM quiz_seen
        WHERE uid = ?
        """,
        (uid,)
    ).fetchall()

    conn.close()

    return {
        row["question_id"]
        for row in rows
    }


def mark_questions_seen(
    uid,
    question_ids
):

    if not uid or not question_ids:
        return

    conn = get_db()

    for question_id in question_ids:

        conn.execute(
            """
            INSERT OR IGNORE INTO quiz_seen(
                uid,
                question_id,
                seen_at
            )
            VALUES(?,?,?)
            """,
            (
                uid,
                question_id,
                now_iso()
            )
        )

    conn.commit()
    conn.close()


# =============================================================
# QUIZ
# =============================================================

@app.get("/api/quiz")
def get_quiz():

    uid = current_uid()

    count = request.args.get(
        "count",
        default=10,
        type=int
    )

    count = max(
        5,
        min(count, 20)
    )

    topic = request.args.get(
        "topic",
        ""
    ).strip()

    pool = quiz_bank

    if topic:

        filtered = [
            item
            for item in quiz_bank
            if item["topic"].lower()
            == topic.lower()
        ]

        if filtered:
            pool = filtered

    seen = get_seen_questions(
        uid
    )

    unseen = [
        item
        for item in pool
        if item["id"] not in seen
    ]

    # Prefer unseen questions.
    random.shuffle(
        unseen
    )

    random.shuffle(
        pool
    )

    selected = (
        unseen[:count]
        if len(unseen) >= count
        else unseen
        + [
            item
            for item in pool
            if item["id"]
            not in {
                x["id"]
                for x in unseen
            }
        ][:count - len(unseen)]
    )

    random.shuffle(
        selected
    )

    selected = selected[:count]

    ids = [
        item["id"]
        for item in selected
    ]

    if uid:

        mark_questions_seen(
            uid,
            ids
        )

        session["quiz_ids"] = ids
        session["quiz_started_at"] = time.time()

    # Never expose correct answers to the browser.
    public_questions = []

    for item in selected:

        options = list(
            item["options"]
        )

        random.shuffle(
            options
        )

        public_questions.append({
            "id": item["id"],
            "topic": item["topic"],
            "question": item["question"],
            "options": options,
            "difficulty": item["difficulty"]
        })

    return jsonify({
        "success": True,
        "questions": public_questions,
        "count": len(public_questions)
    })


# =============================================================
# QUIZ SUBMISSION
# =============================================================

@app.post("/api/quiz/submit")
@require_auth
def submit_quiz(uid):

    data = request.get_json(
        silent=True
    ) or {}

    answers = data.get(
        "answers",
        {}
    )

    status = str(
        data.get(
            "status",
            "completed"
        )
    )

    reason = str(
        data.get(
            "reason",
            ""
        )
    )[:500]

    if not isinstance(
        answers,
        dict
    ):

        answers = {}

    ids = session.get(
        "quiz_ids",
        []
    )

    if not ids:

        return jsonify({
            "success": False,
            "error": "No active quiz."
        }), 400

    score = 0

    for question_id in ids:

        question = next(
            (
                x
                for x in quiz_bank
                if x["id"] == question_id
            ),
            None
        )

        if not question:
            continue

        supplied = answers.get(
            question_id
        )

        if supplied == question["answer"]:
            score += 1

    total = len(ids)

    terminated = (
        status == "terminated"
    )

    final_status = (
        "terminated"
        if terminated
        else "completed"
    )

    xp = 0

    if not terminated:

        xp = score * 10

        if (
            total > 0
            and score == total
        ):
            xp += 50

    conn = get_db()

    conn.execute(
        """
        INSERT INTO quiz_attempts(
            uid,
            score,
            total,
            xp,
            status,
            reason,
            created_at
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            uid,
            score,
            total,
            xp,
            final_status,
            reason,
            now_iso()
        )
    )

    conn.commit()
    conn.close()

    if xp:

        award_xp(
            uid,
            xp
        )

        update_streak(
            uid
        )

    if final_status == "completed":

        unlock(
            uid,
            "first-quiz"
        )

        if (
            total > 0
            and score == total
        ):

            unlock(
                uid,
                "perfect-quiz"
            )

    check_xp_achievements(
        uid
    )

    session.pop(
        "quiz_ids",
        None
    )

    session.pop(
        "quiz_started_at",
        None
    )

    return jsonify({
        "success": True,
        "score": score,
        "total": total,
        "xpEarned": xp,
        "status": final_status,
        "reason": reason
    })


# =============================================================
# QUIZ MALPRACTICE
# =============================================================

@app.post("/api/quiz/violation")
@require_auth
def quiz_violation(uid):

    data = request.get_json(
        silent=True
    ) or {}

    reason = str(
        data.get(
            "reason",
            "Quiz activity violation"
        )
    )[:500]

    ids = session.get(
        "quiz_ids",
        []
    )

    if not ids:

        return jsonify({
            "success": True,
            "status": "no-active-quiz"
        })

    conn = get_db()

    conn.execute(
        """
        INSERT INTO quiz_attempts(
            uid,
            score,
            total,
            xp,
            status,
            reason,
            created_at
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            uid,
            0,
            len(ids),
            0,
            "terminated",
            reason,
            now_iso()
        )
    )

    conn.commit()
    conn.close()

    session.pop(
        "quiz_ids",
        None
    )

    session.pop(
        "quiz_started_at",
        None
    )

    return jsonify({
        "success": True,
        "status": "terminated",
        "reason": reason,
        "xpEarned": 0
    })


# =============================================================
# WANDBOX COMPILER
# =============================================================

def get_wandbox_compilers():

    now = time.time()

    if (
        compiler_cache["items"]
        and compiler_cache["expires"] > now
    ):
        return compiler_cache["items"]

    response = requests.get(
        WANDBOX_LIST,
        timeout=WANDBOX_TIMEOUT
    )

    response.raise_for_status()

    data = response.json()

    if not isinstance(
        data,
        list
    ):
        raise RuntimeError(
            "Invalid compiler list received."
        )

    compiler_cache["items"] = data

    compiler_cache["expires"] = (
        now + 900
    )

    return data


def find_compiler(
    language
):

    language = language.lower().strip()

    try:

        compilers = get_wandbox_compilers()

    except Exception:

        compilers = []

    aliases = {

        "c": [
            "gcc-head-c",
            "gcc",
            "clang"
        ],

        "c++": [
            "gcc-head",
            "g++",
            "clang"
        ],

        "cpp": [
            "gcc-head",
            "g++",
            "clang"
        ],

        "python": [
            "cpython",
            "python"
        ],

        "java": [
            "openjdk",
            "java"
        ]
    }

    wanted = aliases.get(
        language,
        []
    )

    # First try exact-ish matches.
    for wanted_name in wanted:

        for compiler in compilers:

            name = str(
                compiler.get(
                    "name",
                    ""
                )
            ).lower()

            if wanted_name.lower() in name:

                return compiler.get(
                    "name"
                )

    # More flexible search.
    for compiler in compilers:

        name = str(
            compiler.get(
                "name",
                ""
            )
        )

        display = str(
            compiler.get(
                "display-name",
                ""
            )
        )

        blob = (
            name + " " + display
        ).lower()

        if language == "c":

            if (
                "gcc" in blob
                and "c++" not in blob
                and "g++" not in blob
            ):
                return name

        elif language in (
            "c++",
            "cpp"
        ):

            if (
                "gcc" in blob
                or "g++" in blob
                or "clang" in blob
            ):
                return name

        elif language == "python":

            if "python" in blob:

                return name

        elif language == "java":

            if "java" in blob:

                return name

    return None


# =============================================================
# COMPILER LIST
# =============================================================

@app.get("/api/compilers")
def compilers():

    results = []

    for language in [
        "C",
        "C++",
        "Python",
        "Java"
    ]:

        try:

            compiler = find_compiler(
                language
            )

            results.append({
                "language": language,
                "compiler": compiler,
                "available": bool(
                    compiler
                )
            })

        except Exception as exc:

            results.append({
                "language": language,
                "compiler": None,
                "available": False,
                "error": str(exc)
            })

    return jsonify({
        "success": True,
        "compilers": results
    })


# =============================================================
# CODE COMPILER
# =============================================================

@app.post("/api/compile")
def compile_code():

    data = request.get_json(
        silent=True
    ) or {}

    code = data.get(
        "code",
        ""
    )

    language = str(
        data.get(
            "language",
            "C"
        )
    ).strip()

    stdin = str(
        data.get(
            "stdin",
            ""
        )
    )

    if not isinstance(
        code,
        str
    ):

        return jsonify({
            "success": False,
            "error": "Code must be text."
        }), 400

    if not code.strip():

        return jsonify({
            "success": False,
            "error": "Code cannot be empty."
        }), 400

    allowed = {
        "c": "C",
        "c++": "C++",
        "cpp": "C++",
        "python": "Python",
        "java": "Java"
    }

    normalized = language.lower()

    if normalized not in allowed:

        return jsonify({
            "success": False,
            "error": (
                "Supported languages: "
                "C, C++, Python and Java."
            )
        }), 400

    if len(code) > 50000:

        return jsonify({
            "success": False,
            "error": "Code is too large."
        }), 413

    if len(stdin) > 10000:

        return jsonify({
            "success": False,
            "error": "Input is too large."
        }), 413

    try:

        compiler = find_compiler(
            normalized
        )

        if not compiler:

            return jsonify({
                "success": False,
                "error": (
                    "No compatible "
                    f"{allowed[normalized]} compiler "
                    "was found on the compiler service."
                )
            }), 503

        payload = {
            "compiler": compiler,
            "code": code,
            "stdin": stdin,
            "save": False
        }

        response = requests.post(
            WANDBOX_API,
            json=payload,
            headers={
                "Content-Type":
                    "application/json"
            },
            timeout=WANDBOX_TIMEOUT
        )

        response.raise_for_status()

        result = response.json()

        compiler_message = str(
            result.get(
                "compiler_message",
                ""
            ) or ""
        )

        program_message = str(
            result.get(
                "program_message",
                ""
            ) or ""
        )

        program_output = str(
            result.get(
                "program_output",
                ""
            ) or ""
        )

        status = result.get(
            "status"
        )

        signal = result.get(
            "signal"
        )

        output = (
            program_output
            or program_message
        )

        # Some compiler services use status
        # values as strings and some as integers.
        try:

            numeric_status = int(
                status
            ) if status is not None else 0

        except Exception:

            numeric_status = 0

        success = (
            numeric_status == 0
            and not signal
        )

        error = compiler_message

        if signal:

            if error:
                error += "\n"

            error += (
                "Process signal: "
                + str(signal)
            )

        return jsonify({
            "success": success,
            "language": allowed[normalized],
            "compiler": compiler,
            "output": output,
            "error": error,
            "compiler_message": compiler_message,
            "program_message": program_message,
            "status": status,
            "signal": signal
        })

    except requests.Timeout:

        return jsonify({
            "success": False,
            "error": (
                "Compiler service timed out. "
                "Please try again."
            )
        }), 504

    except requests.RequestException as exc:

        return jsonify({
            "success": False,
            "error": (
                "Compiler service connection failed: "
                + str(exc)
            )
        }), 503

    except Exception as exc:

        return jsonify({
            "success": False,
            "error": (
                "Compiler service error: "
                + str(exc)
            )
        }), 503


# =============================================================
# ACTIVITY
# =============================================================

@app.post("/api/activity")
@require_auth
def activity(uid):

    data = request.get_json(
        silent=True
    ) or {}

    event = str(
        data.get(
            "event",
            ""
        )
    ).strip()[:100]

    details = data.get(
        "details",
        ""
    )

    if not event:

        return jsonify({
            "success": False,
            "error": "event is required."
        }), 400

    if not isinstance(
        details,
        str
    ):

        details = json.dumps(
            details
        )

    conn = get_db()

    conn.execute(
        """
        INSERT INTO activity_log(
            uid,
            event,
            details,
            created_at
        )
        VALUES(?,?,?,?)
        """,
        (
            uid,
            event,
            details[:2000],
            now_iso()
        )
    )

    conn.commit()
    conn.close()

    if event == "career-path-explored":

        unlock(
            uid,
            "career-path"
        )

    if event == "compiler-run":

        unlock(
            uid,
            "coder"
        )

    return jsonify({
        "success": True
    })


# =============================================================
# 404
# =============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "error": "Endpoint not found."
    }), 404


# =============================================================
# 500
# =============================================================

@app.errorhandler(500)
def server_error(error):

    print(
        "Internal server error:",
        error
    )

    return jsonify({
        "success": False,
        "error": "Internal server error."
    }), 500


# =============================================================
# START
# =============================================================

if __name__ == "__main__":

    port = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
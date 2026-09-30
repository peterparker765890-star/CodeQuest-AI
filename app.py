import os
import json
import sqlite3
import hashlib
import urllib.request
import urllib.error
from datetime import date, timedelta
from functools import wraps

from flask import Flask, jsonify, request, render_template, session

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-codequest-secret-key"
)

DATABASE_PATH = os.environ.get(
    "DATABASE_PATH",
    "codequest.db"
)

WANDBOX_URL = "https://wandbox.org/api/compile.json"
WANDBOX_COMPILER = "gcc-head-c"

# =========================================================
# FIREBASE ADMIN
# =========================================================

firebase_admin = None
firebase_auth = None

try:
    import firebase_admin
    from firebase_admin import credentials, auth as firebase_auth

    service_account_json = os.environ.get(
        "FIREBASE_SERVICE_ACCOUNT_JSON"
    )

    if service_account_json:
        try:
            service_account_info = json.loads(
                service_account_json
            )

            if not firebase_admin._apps:
                cred = credentials.Certificate(
                    service_account_info
                )
                firebase_admin.initialize_app(cred)

        except Exception as error:
            print("Firebase Admin initialization error:", error)

except Exception as error:
    print("Firebase Admin package not installed:", error)


# =========================================================
# DATABASE
# =========================================================

def get_db():

    db = sqlite3.connect(
        DATABASE_PATH,
        timeout=30
    )

    db.row_factory = sqlite3.Row

    db.execute(
        "PRAGMA foreign_keys = ON"
    )

    return db


def init_db():

    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firebase_uid TEXT UNIQUE,
            email TEXT,
            name TEXT,
            photo_url TEXT,
            xp INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 1,
            last_active TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS progress(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firebase_uid TEXT NOT NULL,
            lesson_key TEXT NOT NULL,
            completed_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(firebase_uid, lesson_key)
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firebase_uid TEXT,
            score INTEGER,
            total INTEGER,
            percentage INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.commit()
    db.close()


init_db()


# =========================================================
# COURSE CONTENT
# =========================================================

def make_lesson(
    title,
    explanation,
    example,
    takeaway,
    practice
):

    return {
        "title": title,
        "lesson": explanation,
        "sample": example,
        "takeaway": takeaway,
        "practice": practice
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


courses = []


# =========================================================
# 1. COMPUTER BASICS
# =========================================================

courses.append(
    course(
        "computer-basics",
        "Computer Basics",
        "💻",
        "Beginner",
        "Build the foundation you need before learning programming.",
        [

            make_lesson(
                "What is a Computer?",
                """A computer is an electronic machine that accepts
input, processes information, stores data and produces output.

For example, when you type your name into a form, the keyboard
provides the input. The computer processes the characters and the
screen displays the result.

A simple way to remember the basic computer cycle is:

Input → Processing → Output → Storage

Understanding this cycle is important because almost every
computer system follows the same basic idea.""",

                """# Real-world computer cycle

Input:
You type 25 into a calculator.

Processing:
The processor calculates the required result.

Output:
The screen displays the answer.

Storage:
The result can be saved for later.""",

                "A computer receives data, processes it and produces useful information.",
                "Identify the input, processing and output in an ATM transaction."
            ),

            make_lesson(
                "Hardware and Software",
                """Hardware is the physical part of a computer that you
can touch.

Examples include the keyboard, mouse, monitor, CPU, RAM and SSD.

Software is a collection of instructions that tells hardware what
to do.

For example, a laptop is hardware. Windows, Chrome and VS Code are
software.

Hardware needs software to perform useful tasks, while software
needs hardware to execute its instructions.""",

                """Hardware examples:
CPU
RAM
SSD
Keyboard
Monitor

Software examples:
Windows
Chrome
VS Code
Python
""",

                "Hardware is physical; software is instructions and programs.",
                "List five hardware components and five software programs you use."
            ),

            make_lesson(
                "CPU - The Processor",
                """The CPU, or Central Processing Unit, executes
instructions.

When a program asks the computer to perform a calculation, the CPU
processes the instructions required to perform that operation.

Modern CPUs contain multiple cores, allowing several tasks to be
processed efficiently.

CPU performance is influenced by architecture, number of cores,
clock speed, cache and workload.""",

                """Example idea:

int a = 10;
int b = 20;
int result = a + b;

The CPU executes the instructions needed to calculate result.""",

                "The CPU executes program instructions.",
                "Explain what happens when a calculator app performs 20 + 30."
            ),

            make_lesson(
                "RAM",
                """RAM stands for Random Access Memory.

It is temporary working memory used by programs while they are
running.

For example, when you open a browser, operating system and browser
data are loaded into memory so the CPU can work with them quickly.

RAM is volatile, which means its working contents are normally lost
when the computer is powered off.""",

                """Example:

Open:
Chrome
VS Code
Spotify

All three applications need RAM while they are running.""",

                "RAM temporarily holds data and instructions needed by active programs.",
                "Why does opening many applications sometimes make a computer slower?"
            ),

            make_lesson(
                "Storage",
                """Storage keeps data even after the computer is powered
off.

Common storage devices include HDDs, SSDs, USB drives and memory
cards.

An SSD normally provides much faster access than a traditional HDD.

Storage capacity is measured using units such as GB and TB.""",

                """Example:

SSD:
Stores Windows
Stores applications
Stores photos
Stores projects

The files remain after shutdown.""",

                "Storage is persistent memory for files and programs.",
                "Compare RAM and SSD based on purpose and persistence."
            ),

            make_lesson(
                "Input Devices",
                """Input devices allow a user or another system to send
information to a computer.

A keyboard sends characters.
A mouse sends pointer actions.
A microphone sends audio.
A camera sends images or video.
A scanner sends scanned documents.""",

                """Keyboard → text input
Mouse → pointer input
Microphone → audio input
Camera → image/video input
Scanner → document input""",

                "Input devices send information into a computer.",
                "Give three examples of input devices used in a college environment."
            ),

            make_lesson(
                "Output Devices",
                """Output devices communicate processed information from
the computer to the user.

A monitor displays visual information.
Speakers produce sound.
A printer creates physical documents.
A projector displays information on a larger surface.""",

                """Computer
   ↓
Processed information
   ↓
Monitor / Speaker / Printer""",

                "Output devices present processed information.",
                "Identify the output device used for printing a college record."
            ),

            make_lesson(
                "Operating Systems",
                """An operating system manages the computer's hardware
and provides services for applications.

Windows, Linux, macOS, Android and iOS are examples of operating
systems.

The operating system manages processes, memory, files, devices,
security and user interaction.""",

                """Application
     ↓
Operating System
     ↓
Hardware

For example:
VS Code → Windows → CPU/RAM/Storage""",

                "The operating system acts as an important layer between applications and hardware.",
                "Name three operating systems and one device where each is commonly used."
            ),

            make_lesson(
                "Files and Folders",
                """Files contain information such as documents, programs,
images or videos.

Folders organize files.

A path identifies where a file exists in a storage system.

For example:

Projects/
    CodeQuest/
        app.py
        requirements.txt

This organization becomes extremely important when developing
software.""",

                """Example project structure:

CodeQuest/
├── app.py
├── requirements.txt
└── templates/
    └── index.html""",

                "Files store information and folders organize files.",
                "Create a folder structure for a small Python project."
            ),

            make_lesson(
                "Binary Numbers",
                """Computers use binary because digital electronic systems
can reliably represent two states.

Those states are commonly represented as 0 and 1.

Binary is base 2, while decimal is base 10.

For example:

Decimal 5 = Binary 101

because:

1×4 + 0×2 + 1×1 = 5.""",

                """Decimal:
5

Binary:
101

Calculation:
1×2² + 0×2¹ + 1×2⁰
= 4 + 0 + 1
= 5""",

                "Binary uses only 0 and 1.",
                "Convert decimal 10 into binary."
            ),

            make_lesson(
                "Number Systems",
                """Programmers frequently work with decimal, binary,
octal and hexadecimal number systems.

Decimal uses digits 0–9.
Binary uses 0–1.
Octal uses 0–7.
Hexadecimal uses 0–9 and A–F.

Hexadecimal is frequently used in computing because one hexadecimal
digit represents four binary bits.""",

                """Binary:
1111

Hexadecimal:
F

Therefore:

1111₂ = F₁₆""",

                "Different number systems provide different representations of the same value.",
                "Convert binary 1010 to hexadecimal."
            ),

            make_lesson(
                "How the Internet Works",
                """The internet is a global network of connected devices.

When you open a website, your device sends network requests to a
server.

DNS helps translate a domain name such as example.com into an IP
address.

Protocols such as TCP/IP, HTTP and HTTPS define how information is
communicated.""",

                """Browser
   ↓
DNS
   ↓
IP address
   ↓
Server
   ↓
HTTP/HTTPS response
   ↓
Browser""",

                "The web uses networks, addresses and protocols to exchange information.",
                "Explain what happens at a high level when you open a website."
            ),

            make_lesson(
                "Applications vs System Software",
                """System software helps operate and manage the computer.

Examples include operating systems and device drivers.

Application software helps users perform particular tasks.

Examples include browsers, word processors, media players and
development environments.""",

                """System software:
Windows
Linux
Device drivers

Application software:
Chrome
VS Code
MS Word""",

                "System software supports the computer; application software helps users perform tasks.",
                "Classify VS Code, Windows, Chrome and a printer driver."
            )

        ]
    )
)


# =========================================================
# 2. DIGITAL PRODUCTIVITY
# =========================================================

courses.append(
    course(
        "digital-productivity",
        "Digital Productivity",
        "📊",
        "Beginner",
        "Learn the everyday tools used by students and professionals.",
        [

            make_lesson(
                "Windows Fundamentals",
                """Windows provides a graphical environment for running
applications, managing files, connecting devices and configuring
the computer.

Important areas include the desktop, Start menu, taskbar,
File Explorer, Settings and Task Manager.""",

                """Example workflow:

Start Menu
   ↓
Open File Explorer
   ↓
Documents
   ↓
Create project folder
   ↓
Save files""",

                "Knowing the operating system makes development and troubleshooting easier.",
                "Create a folder called CollegeProjects and organize three files inside it."
            ),

            make_lesson(
                "MS Word",
                """Microsoft Word is a document-processing application.

It is commonly used for reports, assignments, resumes and
documentation.

Important skills include headings, formatting, tables, page
layout, references and exporting documents.""",

                """Example report structure:

Title
↓
Introduction
↓
Main Content
↓
Conclusion
↓
References""",

                "Good documents use structure, consistent formatting and readable content.",
                "Create a one-page technical report using headings and a table."
            ),

            make_lesson(
                "MS Excel",
                """Excel organizes information into rows and columns.

It can perform calculations using formulas and functions.

For example, if cells B2 through B6 contain marks, the average can
be calculated using the AVERAGE function.""",

                """=SUM(B2:B6)

=AVERAGE(B2:B6)

=MAX(B2:B6)

=MIN(B2:B6)""",

                "Spreadsheets can store, calculate and analyze structured data.",
                "Create a five-student marks table and calculate the average."
            ),

            make_lesson(
                "PowerPoint",
                """PowerPoint is used to communicate information through
slides.

A good technical presentation normally has a clear title,
problem statement, explanation, examples and conclusion.

Avoid putting entire paragraphs on slides. Use concise points and
explain the details verbally.""",

                """Example presentation:

Slide 1 → Project title
Slide 2 → Problem
Slide 3 → Solution
Slide 4 → Technology
Slide 5 → Demonstration
Slide 6 → Conclusion""",

                "Presentation software is a communication tool, not a document dump.",
                "Create six slides explaining a small software project."
            ),

            make_lesson(
                "Google Drive and Cloud Files",
                """Cloud storage allows files to be stored on remote
servers and accessed through the internet.

It can simplify collaboration, backup and sharing.

Always understand sharing permissions before publishing a
document publicly.""",

                """College project workflow:

Local file
   ↓
Cloud upload
   ↓
Share with team
   ↓
Collaborate
   ↓
Final submission""",

                "Cloud storage improves access and collaboration.",
                "Create a project folder and decide which files should be private and which can be shared."
            ),

            make_lesson(
                "Professional Email",
                """Professional communication should be clear,
specific and respectful.

A good email normally contains a useful subject, greeting,
purpose, necessary details and a professional closing.""",

                """Subject:
Request for Project Review

Hello Sir,

I am writing to request a review of our project...

Thank you.""",

                "Clear communication is an important technical skill.",
                "Write a short professional email requesting feedback on a project."
            )

        ]
    )
)


# =========================================================
# 3. PROGRAMMING FUNDAMENTALS
# =========================================================

courses.append(
    course(
        "programming-fundamentals",
        "Programming Fundamentals",
        "🧠",
        "Beginner",
        "Learn how programmers think before moving into advanced languages.",
        [

            make_lesson(
                "What is Programming?",
                """Programming is the process of creating instructions
that a computer can execute.

A program takes information, applies logic and produces a result.

Programming is not mainly about memorizing syntax. The important
skill is learning how to break a problem into smaller logical steps.""",

                """Problem:
Calculate the area of a rectangle.

Steps:
1. Read length.
2. Read width.
3. Multiply length × width.
4. Display result.""",

                "Programming means expressing a solution as executable instructions.",
                "Write the steps needed to calculate the average of three numbers."
            ),

            make_lesson(
                "Algorithms",
                """An algorithm is a finite sequence of clear steps used
to solve a problem.

Before writing code, programmers often design an algorithm.

A good algorithm should be clear, logically correct and eventually
produce the required result.""",

                """Algorithm: Find the larger of two numbers

1. Read A and B.
2. Compare A and B.
3. If A > B, output A.
4. Otherwise output B.""",

                "An algorithm describes the solution before implementation.",
                "Write an algorithm to determine whether a number is even or odd."
            ),

            make_lesson(
                "Flowcharts",
                """A flowchart visually represents an algorithm.

Common symbols include:
Oval → Start/End
Rectangle → Process
Diamond → Decision
Parallelogram → Input/Output""",

                """Start
  ↓
Read number
  ↓
number % 2 == 0?
 ↙          ↘
Yes          No
 ↓            ↓
Even         Odd
  ↘          ↙
     End""",

                "Flowcharts help visualize program logic.",
                "Draw a flowchart for finding the largest of two numbers."
            ),

            make_lesson(
                "Variables",
                """A variable is a named storage location used by a
program to hold a value.

The value may change during program execution.

For example, a student's score can be stored in a variable and
updated after another test.""",

                """int score = 75;

score = 82;

printf("%d", score);""",

                "Variables allow programs to work with changing data.",
                "Create variables representing a student's name, age and mark."
            ),

            make_lesson(
                "Data Types",
                """A data type tells the programming language what kind
of value is being stored.

Common types include integers, floating-point numbers, characters
and strings.

Choosing an appropriate type helps the program represent data
correctly.""",

                """int age = 18;
float mark = 87.5;
char grade = 'A';""",

                "Data types describe the kind of data a variable stores.",
                "Choose suitable C data types for age, percentage and grade."
            ),

            make_lesson(
                "Conditions",
                """Programs often need to make decisions.

An if statement executes code when a condition is true.

For example, a college application may check whether a student's
mark is at least 50 before displaying Pass.""",

                """int mark = 72;

if(mark >= 50) {
    printf("Pass");
} else {
    printf("Fail");
}""",

                "Conditions allow programs to choose between different paths.",
                "Write a condition that prints Eligible when age is at least 18."
            ),

            make_lesson(
                "Loops",
                """Loops repeat instructions.

A loop is useful when the same operation must be performed multiple
times.

For example, printing numbers from 1 to 10 does not require ten
separate print statements.""",

                """for(int i = 1; i <= 10; i++) {
    printf("%d\n", i);
}""",

                "Loops reduce repeated code.",
                "Write a loop that prints the numbers 1 to 20."
            ),

            make_lesson(
                "Functions",
                """A function is a reusable block of code designed to
perform a particular task.

Functions make programs easier to organize, test and maintain.""",

                """int add(int a, int b) {
    return a + b;
}

int result = add(10, 20);""",

                "Functions allow logic to be reused.",
                "Create a function that returns the square of a number."
            ),

            make_lesson(
                "Arrays",
                """An array stores multiple values of the same type
under one variable name.

Instead of creating separate variables for five marks, an array
can store all five marks together.""",

                """int marks[5] = {
    78, 85, 91, 66, 88
};

printf("%d", marks[2]);""",

                "Arrays are useful for collections of related values.",
                "Create an array containing the marks of five students."
            ),

            make_lesson(
                "Debugging",
                """Debugging is the process of finding and correcting
problems in a program.

Common errors include syntax errors, runtime errors and logical
errors.

Reading compiler messages carefully is an important debugging
skill.""",

                """Wrong:

int a = 10
printf("%d", a);

Correct:

int a = 10;
printf("%d", a);""",

                "Debugging means identifying the cause of incorrect program behavior and fixing it.",
                "Find the missing symbol in the incorrect C example."
            )

        ]
    )
)


# =========================================================
# 4. C PROGRAMMING
# =========================================================

courses.append(
    course(
        "c-programming",
        "C Programming",
        "⚙️",
        "Beginner → Intermediate",
        "Learn C from program structure through pointers and files.",
        [

            make_lesson(
                "Your First C Program",
                """A C program contains functions and statements.

The main function is the starting point of a normal C program.

The stdio.h header provides functions such as printf and scanf.""",

                """#include <stdio.h>

int main() {

    printf("Hello, CodeQuest AI!");

    return 0;
}""",

                "main() is the entry point of a normal C program.",
                "Change the program so it prints your name."
            ),

            make_lesson(
                "printf and scanf",
                """printf displays information.

scanf reads formatted input from the user.

When reading an integer into a variable, scanf normally receives
the address of that variable using &.""",

                """#include <stdio.h>

int main() {

    int age;

    printf("Enter age: ");
    scanf("%d", &age);

    printf("You are %d years old.", age);

    return 0;
}""",

                "printf produces output and scanf reads formatted input.",
                "Write a program that reads two integers and prints their sum."
            ),

            make_lesson(
                "Operators",
                """Operators perform calculations and comparisons.

Arithmetic operators include +, -, *, / and %.

Comparison operators include ==, !=, >, <, >= and <=.

Logical operators include &&, || and !.""",

                """int a = 10;
int b = 3;

printf("%d\n", a + b);
printf("%d\n", a % b);
printf("%d\n", a > b);""",

                "Operators allow programs to calculate and compare values.",
                "Write a program that checks whether one number is greater than another."
            ),

            make_lesson(
                "if else",
                """if and else allow a C program to choose between
different execution paths.

The condition is evaluated before deciding which block to execute.""",

                """int mark = 82;

if(mark >= 90) {
    printf("A+");
}
else if(mark >= 75) {
    printf("A");
}
else {
    printf("Needs improvement");
}""",

                "if/else implements decision-making logic.",
                "Create a grading program using three mark ranges."
            ),

            make_lesson(
                "switch",
                """switch is useful when one expression needs to be
compared against several fixed cases.

It is often useful for menu-based programs.""",

                """int choice = 2;

switch(choice) {

    case 1:
        printf("Add");
        break;

    case 2:
        printf("View");
        break;

    default:
        printf("Invalid choice");
}""",

                "switch is useful for multiple fixed choices.",
                "Create a menu with options 1, 2 and 3."
            ),

            make_lesson(
                "for Loop",
                """A for loop is useful when the number of repetitions is
known or can be expressed clearly.

It has initialization, condition and update parts.""",

                """for(int i = 1; i <= 5; i++) {
    printf("Iteration %d\n", i);
}""",

                "for loops are commonly used for counted repetition.",
                "Print the multiplication table of 7."
            ),

            make_lesson(
                "while Loop",
                """A while loop repeats as long as its condition remains
true.

It is useful when the number of iterations depends on a changing
condition.""",

                """int count = 1;

while(count <= 5) {

    printf("%d\n", count);

    count++;
}""",

                "while loops continue while a condition is true.",
                "Use while to print numbers from 10 down to 1."
            ),

            make_lesson(
                "Arrays in C",
                """A C array stores multiple values of the same type in
contiguous memory.

Array indexing starts at zero.

Therefore, the first element is array[0].""",

                """int marks[5] = {
    80, 72, 91, 65, 88
};

printf("%d", marks[0]);""",

                "C arrays use zero-based indexing.",
                "Calculate the total of five marks using a loop."
            ),

            make_lesson(
                "Strings in C",
                """C does not have a separate built-in string object like
some higher-level languages.

A string is commonly represented as an array of characters ending
with the null character '\\0'.""",

                """char name[] = "CodeQuest";

printf("%s", name);""",

                "A C string is a character sequence terminated by '\\0'.",
                "Store and print your first name using a character array."
            ),

            make_lesson(
                "Functions in C",
                """Functions divide a program into reusable logical
components.

A function can receive parameters and return a value.""",

                """int multiply(int a, int b) {
    return a * b;
}

int main() {

    int result = multiply(6, 7);

    printf("%d", result);

    return 0;
}""",

                "Functions improve reuse and organization.",
                "Create a function that returns the largest of two numbers."
            ),

            make_lesson(
                "Pointers",
                """A pointer stores the memory address of another
variable.

The & operator obtains an address.

The * operator can dereference a pointer to access the value stored
at that address.""",

                """int age = 18;

int *ptr = &age;

printf("Value = %d\n", *ptr);
printf("Address = %p\n", (void*)ptr);""",

                "Pointers provide direct access to memory addresses.",
                "Create a pointer to an integer and print both its value and address."
            ),

            make_lesson(
                "Structures",
                """A structure allows related values of different data
types to be grouped together.

This is useful when representing real-world entities such as a
student, employee or product.""",

                """struct Student {

    char name[50];
    int age;
    float mark;
};

struct Student s =
    {"Arun", 18, 87.5};""",

                "Structures group related data into one custom type.",
                "Create a Student structure containing name, roll number and mark."
            ),

            make_lesson(
                "File Handling",
                """C programs can work with files using functions such
as fopen, fprintf, fscanf and fclose.

File handling allows information to remain available after a
program ends.""",

                """FILE *file;

file = fopen("notes.txt", "w");

if(file != NULL) {

    fprintf(file, "CodeQuest AI");

    fclose(file);
}""",

                "Files allow programs to store persistent information.",
                "Write a program that creates a file and stores one sentence."
            ),

            make_lesson(
                "C Mini Project",
                """A mini project combines several concepts.

A student marks program can use variables, arrays, functions,
conditions and loops.

The goal is to solve a complete problem rather than memorize
individual syntax rules.""",

                """int marks[3] = {80, 90, 75};

int total = 0;

for(int i = 0; i < 3; i++) {
    total += marks[i];
}

printf("Total = %d", total);""",

                "Projects combine individual programming concepts into useful software.",
                "Extend the example to calculate average and display Pass/Fail."
            )

        ]
    )
)


# =========================================================
# 5. C++
# =========================================================

courses.append(
    course(
        "cpp",
        "C++ Programming",
        "🚀",
        "Intermediate",
        "Move from procedural programming into object-oriented programming.",
        [

            make_lesson(
                "C++ Basics",
                """C++ extends the C programming language with features
such as classes, objects, references, templates and the Standard
Library.

A basic C++ program uses iostream for input and output.""",

                """#include <iostream>
using namespace std;

int main() {

    cout << "Hello C++";

    return 0;
}""",

                "C++ supports both procedural and object-oriented programming.",
                "Modify the program to print your college name."
            ),

            make_lesson(
                "Classes and Objects",
                """A class defines a structure containing data and
functions.

An object is an instance of that class.

For example, a Student class can represent student information.""",

                """class Student {

public:
    string name;

    void introduce() {
        cout << "Student: " << name;
    }
};

Student s;
s.name = "Arun";
s.introduce();""",

                "A class is a blueprint; an object is an instance.",
                "Create a Car class with brand and speed."
            ),

            make_lesson(
                "Constructor",
                """A constructor is automatically called when an object
is created.

Constructors are commonly used to initialize object data.""",

                """class Student {

public:

    string name;

    Student(string n) {
        name = n;
    }
};

Student s("Arun");""",

                "Constructors initialize objects.",
                "Create a constructor that initializes a product name and price."
            ),

            make_lesson(
                "Inheritance",
                """Inheritance allows a class to derive characteristics
and behavior from another class.

It can represent an is-a relationship.""",

                """class Animal {

public:
    void eat() {
        cout << "Eating";
    }
};

class Dog : public Animal {

public:
    void bark() {
        cout << "Barking";
    }
};""",

                "Inheritance allows a derived class to reuse base-class functionality.",
                "Create a Vehicle base class and Car derived class."
            ),

            make_lesson(
                "Polymorphism",
                """Polymorphism means one interface can represent
different underlying behaviors.

Function overriding is a common object-oriented example.""",

                """class Animal {

public:
    virtual void sound() {
        cout << "Animal sound";
    }
};

class Dog : public Animal {

public:
    void sound() override {
        cout << "Bark";
    }
};""",

                "Polymorphism allows behavior to vary through a common interface.",
                "Create Animal and Cat classes with different sound methods."
            ),

            make_lesson(
                "STL",
                """The C++ Standard Template Library provides ready-made
containers and algorithms.

vector is one of the most commonly used containers.""",

                """#include <vector>

vector<int> marks = {
    80, 90, 75
};

for(int mark : marks) {
    cout << mark << endl;
}""",

                "STL reduces the need to implement common data structures manually.",
                "Create a vector containing five numbers and calculate their total."
            )

        ]
    )
)


# =========================================================
# 6. PYTHON
# =========================================================

courses.append(
    course(
        "python",
        "Python Programming",
        "🐍",
        "Beginner → Intermediate",
        "Learn Python for automation, development, data and AI.",
        [

            make_lesson(
                "Python Introduction",
                """Python is a high-level programming language known
for readable syntax.

It is widely used for automation, web development, data analysis,
AI and scripting.""",

                """print("Hello, CodeQuest AI")

name = "Arun"

print("Welcome", name)""",

                "Python emphasizes readable and productive programming.",
                "Write a Python program that prints your name and college."
            ),

            make_lesson(
                "Variables",
                """Python variables are created by assigning values.

Unlike C, you normally do not declare the variable type separately
before assignment.""",

                """name = "Arun"
age = 18
mark = 87.5

print(name)
print(age)
print(mark)""",

                "Python variables can hold different kinds of values.",
                "Create variables for your name, age and average mark."
            ),

            make_lesson(
                "Conditions",
                """Python uses indentation to define blocks.

if, elif and else are used to make decisions.""",

                """mark = 82

if mark >= 75:
    print("Distinction")
elif mark >= 50:
    print("Pass")
else:
    print("Fail")""",

                "Python uses indentation to structure conditional blocks.",
                "Write a program that checks whether a number is positive, negative or zero."
            ),

            make_lesson(
                "Loops",
                """for and while loops allow repeated operations.

Python's for loop can iterate directly over items in a sequence.""",

                """for number in range(1, 6):
    print(number)""",

                "Loops automate repeated work.",
                "Print the multiplication table of 5 using a loop."
            ),

            make_lesson(
                "Lists",
                """A list stores multiple values in an ordered,
changeable collection.

Lists are one of the most frequently used Python data structures.""",

                """marks = [80, 90, 75, 88]

print(marks[0])

marks.append(95)

print(marks)""",

                "Lists store ordered collections of values.",
                "Create a list of five programming languages."
            ),

            make_lesson(
                "Dictionaries",
                """A dictionary stores key-value pairs.

It is useful when data needs to be accessed using meaningful keys
rather than numeric positions.""",

                """student = {
    "name": "Arun",
    "age": 18,
    "mark": 87.5
}

print(student["name"])""",

                "Dictionaries represent structured key-value data.",
                "Create a dictionary representing a laptop."
            ),

            make_lesson(
                "Functions",
                """Functions group reusable logic.

Python functions are defined using the def keyword.""",

                """def add(a, b):
    return a + b

result = add(10, 20)

print(result)""",

                "Functions make Python programs reusable and organized.",
                "Write a function that returns the square of a number."
            ),

            make_lesson(
                "File Handling",
                """Python can read and write files using the open
function.

The with statement automatically handles closing the file.""",

                """with open("notes.txt", "w") as file:
    file.write("CodeQuest AI")""",

                "File handling lets Python programs store information persistently.",
                "Write a program that stores three lines in a text file."
            ),

            make_lesson(
                "Exception Handling",
                """Exceptions are runtime situations that interrupt
normal program execution.

try and except allow a program to handle expected errors
gracefully.""",

                """try:
    number = int(input("Enter number: "))
    print(10 / number)

except ValueError:
    print("Please enter a number.")

except ZeroDivisionError:
    print("Cannot divide by zero.")""",

                "Exception handling prevents expected runtime errors from crashing the user experience.",
                "Handle invalid numeric input in a calculator."
            ),

            make_lesson(
                "Python OOP",
                """Object-oriented programming organizes software using
classes and objects.

Classes can contain data and methods.""",

                """class Student:

    def __init__(self, name):
        self.name = name

    def introduce(self):
        print("Student:", self.name)

s = Student("Arun")

s.introduce()""",

                "Python supports object-oriented programming.",
                "Create a Book class containing title and author."
            )

        ]
    )
)


# =========================================================
# HELPER FOR LARGE ORDERED COURSES
# =========================================================

def simple_topic_lesson(
    title,
    explanation,
    example,
    takeaway,
    practice
):
    return make_lesson(
        title,
        explanation,
        example,
        takeaway,
        practice
    )


# =========================================================
# 7. WEB DEVELOPMENT
# =========================================================

courses.append(
    course(
        "web-development",
        "Web Development",
        "🌐",
        "Beginner → Advanced",
        "Build websites and understand how modern web applications work.",
        [

            simple_topic_lesson(
                "How Websites Work",
                """A website normally involves a client and a server.

The browser acts as the client. It sends HTTP requests to a server.
The server processes the request and sends a response.

HTML defines structure, CSS controls presentation and JavaScript
adds behavior.""",
                """Browser
   ↓ HTTP request
Server
   ↓ HTTP response
Browser""",
                "The browser and server communicate using web protocols.",
                "Explain what happens when a browser requests an HTML page."
            ),

            simple_topic_lesson(
                "HTML",
                """HTML stands for HyperText Markup Language.

It describes the structure of a web page using elements such as
headings, paragraphs, links, images and forms.""",
                """<!DOCTYPE html>

<html>
<body>

<h1>CodeQuest AI</h1>

<p>Learn computer science.</p>

</body>
</html>""",
                "HTML defines webpage structure.",
                "Create a page containing a heading, paragraph and button."
            ),

            simple_topic_lesson(
                "CSS",
                """CSS controls the appearance of HTML elements.

It can change colors, spacing, typography, layout, borders and
responsive behavior.""",
                """body {
    background: #090914;
    color: white;
}

h1 {
    color: #8b5cf6;
}""",
                "CSS controls presentation.",
                "Style an HTML heading with a background and custom font size."
            ),

            simple_topic_lesson(
                "JavaScript",
                """JavaScript adds behavior to web pages.

It can respond to clicks, modify HTML, communicate with APIs and
store client-side information.""",
                """document
    .getElementById("demo")
    .textContent = "Hello CodeQuest";""",
                "JavaScript makes webpages interactive.",
                "Create a button that changes a paragraph when clicked."
            ),

            simple_topic_lesson(
                "DOM",
                """The Document Object Model represents an HTML page as
objects that JavaScript can access and modify.""",
                """const heading =
    document.querySelector("h1");

heading.textContent =
    "New Heading";""",
                "The DOM lets JavaScript manipulate webpage elements.",
                "Change the text of a heading using JavaScript."
            ),

            simple_topic_lesson(
                "Events",
                """Events represent actions such as clicks, keyboard
input and mouse movement.

JavaScript can listen for events and execute functions when they
occur.""",
                """button.addEventListener(
    "click",
    function() {
        alert("Clicked!");
    }
);""",
                "Events connect user actions to program behavior.",
                "Create a click event for a button."
            ),

            simple_topic_lesson(
                "HTTP and HTTPS",
                """HTTP is a protocol used for communication on the web.

HTTPS uses encryption through TLS to protect data while it travels
between client and server.""",
                """GET /api/courses HTTP/1.1

Host: codequest-ai.example""",
                "HTTPS protects web communication from many network-level threats.",
                "Explain the difference between HTTP and HTTPS."
            ),

            simple_topic_lesson(
                "JSON",
                """JSON is a common text format for exchanging structured
data between applications.

It is frequently used by REST APIs.""",
                """{
    "name": "Arun",
    "xp": 250,
    "level": 3
}""",
                "JSON represents structured data in a widely supported format.",
                "Create JSON representing a student and three completed courses."
            ),

            simple_topic_lesson(
                "REST APIs",
                """An API allows one software system to communicate with
another.

A REST API commonly exposes resources through HTTP endpoints.""",
                """GET /api/courses

POST /api/quiz/submit

GET /api/stats""",
                "APIs allow different software components to communicate.",
                "Design three API endpoints for a student learning platform."
            ),

            simple_topic_lesson(
                "Git and GitHub",
                """Git tracks changes to source code.

GitHub hosts repositories and provides collaboration features such
as pull requests, issues and project documentation.""",
                """git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <repository-url>
git push -u origin main""",
                "Git tracks code history; GitHub provides hosted collaboration.",
                "Create a repository for a small college project."
            )

        ]
    )
)


# =========================================================
# 8. DBMS
# =========================================================

courses.append(
    course(
        "dbms",
        "DBMS & SQL",
        "🗄️",
        "Intermediate",
        "Learn how applications store, retrieve and organize data.",
        [

            simple_topic_lesson(
                "What is a Database?",
                """A database is an organized collection of information
that can be stored and retrieved efficiently.

Applications use databases to store users, products, orders,
messages, marks and other structured information.""",
                """Students

id | name | mark
---|------|-----
1  | Arun | 87
2  | Ravi | 91""",
                "Databases organize persistent application data.",
                "Design a table for storing college students."
            ),

            simple_topic_lesson(
                "Tables and Records",
                """A relational database organizes information into
tables.

Rows represent records and columns represent attributes.""",
                """Students

id | name | department
1  | Arun | IT
2  | Ravi | CSE""",
                "Rows represent records; columns represent attributes.",
                "Design a table for books."
            ),

            simple_topic_lesson(
                "Primary Keys",
                """A primary key uniquely identifies a row in a table.

Student ID is a common example because each student can have a
unique identifier.""",
                """CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT
);""",
                "A primary key uniquely identifies records.",
                "Create a table with a suitable primary key."
            ),

            simple_topic_lesson(
                "SELECT",
                """SELECT retrieves information from a table.""",
                """SELECT name, mark
FROM students;""",
                "SELECT retrieves database records.",
                "Write a query that retrieves all student names."
            ),

            simple_topic_lesson(
                "INSERT",
                """INSERT adds new records to a table.""",
                """INSERT INTO students
(id, name, mark)
VALUES
(1, 'Arun', 87);""",
                "INSERT creates new records.",
                "Insert two students into a table."
            ),

            simple_topic_lesson(
                "UPDATE",
                """UPDATE changes existing records.

A WHERE condition should normally be used carefully so that only
the intended rows are changed.""",
                """UPDATE students
SET mark = 92
WHERE id = 1;""",
                "UPDATE modifies existing records.",
                "Increase one student's mark using UPDATE."
            ),

            simple_topic_lesson(
                "DELETE",
                """DELETE removes records.

A missing WHERE clause can remove all rows, so destructive
operations should be handled carefully.""",
                """DELETE FROM students
WHERE id = 1;""",
                "DELETE removes selected records.",
                "Write a query that removes a student by ID."
            ),

            simple_topic_lesson(
                "JOIN",
                """JOIN combines related information from multiple
tables.

For example, a student table can be connected to a department
table using a department ID.""",
                """SELECT students.name,
       departments.name
FROM students
JOIN departments
ON students.department_id =
   departments.id;""",
                "JOIN connects related tables.",
                "Design two related tables and identify the JOIN column."
            )

        ]
    )
)


# =========================================================
# 9. DATA STRUCTURES
# =========================================================

courses.append(
    course(
        "dsa",
        "Data Structures & Algorithms",
        "🧩",
        "Intermediate → Advanced",
        "Learn how data is organized and how algorithms solve problems efficiently.",
        [

            simple_topic_lesson(
                "Time Complexity",
                """Time complexity describes how the amount of work
performed by an algorithm changes as input size increases.

Big-O notation is commonly used to express an upper-bound growth
rate.""",
                """Linear search:

for each item
    compare with target

Approximate complexity:
O(n)""",
                "Complexity helps compare algorithm scalability.",
                "Determine the basic complexity of a loop that processes every array element."
            ),

            simple_topic_lesson(
                "Stack",
                """A stack follows LIFO: Last In, First Out.

A stack is useful for undo operations, function calls and
expression processing.""",
                """push(10)
push(20)

top()
→ 20

pop()
→ 20""",
                "Stacks use LIFO ordering.",
                "Explain how browser back history can relate to a stack."
            ),

            simple_topic_lesson(
                "Queue",
                """A queue normally follows FIFO: First In, First Out.

Queues are useful for scheduling, print jobs and task processing.""",
                """enqueue(A)
enqueue(B)

dequeue()
→ A""",
                "Queues use FIFO ordering.",
                "Give a real-world example of a queue."
            ),

            simple_topic_lesson(
                "Linked List",
                """A linked list consists of nodes where each node stores
data and a link to another node.""",
                """[10 | next] → [20 | next] → [30 | NULL]""",
                "Linked lists connect nodes through references.",
                "Draw a three-node linked list."
            ),

            simple_topic_lesson(
                "Binary Tree",
                """A binary tree is a tree in which each node has at
most two children.

Trees are useful for hierarchical data and searching.""",
                """        50
       /  \
     30    70
    /  \  /  \
   20 40 60 80""",
                "Trees represent hierarchical relationships.",
                "Identify the root, leaves and children in a binary tree."
            ),

            simple_topic_lesson(
                "Graphs",
                """A graph contains vertices and edges.

Graphs can represent roads, social networks, computer networks and
many other relationships.""",
                """A ---- B
|      |
|      |
C ---- D""",
                "Graphs represent relationships between entities.",
                "Model four cities connected by roads as a graph."
            ),

            simple_topic_lesson(
                "Searching",
                """Searching algorithms locate a required value.

Linear search checks items sequentially. Binary search repeatedly
halves a sorted search range.""",
                """Binary search:

low = 0
high = n - 1

middle = (low + high) / 2""",
                "The appropriate search algorithm depends on the data structure and ordering.",
                "Explain why binary search requires sorted data."
            ),

            simple_topic_lesson(
                "Sorting",
                """Sorting arranges data into a chosen order.

Common algorithms include bubble sort, insertion sort, merge sort
and quicksort.""",
                """Input:
5 2 8 1

Sorted:
1 2 5 8""",
                "Sorting organizes data according to a comparison rule.",
                "Sort five numbers manually and describe your method."
            )

        ]
    )
)


# =========================================================
# 10. OPERATING SYSTEMS
# =========================================================

courses.append(
    course(
        "operating-systems",
        "Operating Systems",
        "🖥️",
        "Intermediate",
        "Understand processes, memory, files and system management.",
        [

            simple_topic_lesson(
                "What an OS Does",
                """An operating system manages hardware resources and
provides services to applications.

It handles processes, memory, files, devices and security.""",
                """Application
     ↓
Operating System
     ↓
CPU / RAM / Disk / Devices""",
                "The OS manages resources between applications and hardware.",
                "List five responsibilities of an operating system."
            ),

            simple_topic_lesson(
                "Processes",
                """A process is a program in execution.

A process has resources such as memory and execution state.""",
                """Program:
Chrome

Running instance:
Chrome process""",
                "A process represents an executing program.",
                "Explain the difference between a program and a process."
            ),

            simple_topic_lesson(
                "Threads",
                """A thread is an execution path within a process.

Multiple threads can allow parts of an application to work
concurrently.""",
                """Process
├── Thread 1
├── Thread 2
└── Thread 3""",
                "Threads allow concurrent execution within a process.",
                "Give an example of an application that could use multiple threads."
            ),

            simple_topic_lesson(
                "Memory Management",
                """The OS manages memory allocation so that programs can
use RAM safely and efficiently.""",
                """Application A → RAM region
Application B → RAM region
Operating System → manages both""",
                "Memory management prevents uncontrolled use of shared memory resources.",
                "Explain why two applications should not freely overwrite each other's memory."
            ),

            simple_topic_lesson(
                "File Systems",
                """A file system organizes data on storage devices.

It manages files, directories, metadata and access permissions.""",
                """/
├── home
├── projects
└── downloads""",
                "File systems provide structured persistent storage.",
                "Create a logical file structure for a web project."
            ),

            simple_topic_lesson(
                "Deadlocks",
                """A deadlock can occur when processes wait indefinitely
for resources held by each other.

Deadlock analysis is an important operating-system concept.""",
                """Process A holds Resource 1
and waits for Resource 2.

Process B holds Resource 2
and waits for Resource 1.""",
                "Deadlocks involve circular waiting for resources.",
                "Draw a simple two-process deadlock."
            )

        ]
    )
)


# =========================================================
# 11. NETWORKS
# =========================================================

courses.append(
    course(
        "networks",
        "Computer Networks",
        "🌐",
        "Intermediate",
        "Understand how computers communicate across networks and the internet.",
        [

            simple_topic_lesson(
                "Network Basics",
                """A computer network connects devices so they can
exchange information and share resources.""",
                """Laptop → Wi-Fi Router → Internet → Server""",
                "Networks allow connected devices to communicate.",
                "Draw the network used by your phone when accessing a website."
            ),

            simple_topic_lesson(
                "IP Address",
                """An IP address identifies a device or network interface
for communication at the IP layer.

IPv4 addresses contain four decimal octets.""",
                """Example IPv4:

192.168.1.10""",
                "IP addresses identify network endpoints.",
                "Explain why two devices on the same network need distinguishable addresses."
            ),

            simple_topic_lesson(
                "DNS",
                """DNS translates domain names into IP addresses so
users can use memorable names instead of numeric addresses.""",
                """codequest-ai.example
        ↓
       DNS
        ↓
203.0.113.10""",
                "DNS provides name-to-address resolution.",
                "Explain why humans prefer domain names to IP addresses."
            ),

            simple_topic_lesson(
                "TCP and UDP",
                """TCP provides reliable, ordered delivery.

UDP provides a lightweight datagram service without the same
connection-oriented guarantees.""",
                """TCP:
Reliable web/application communication

UDP:
Low-overhead real-time communication""",
                "TCP and UDP provide different transport characteristics.",
                "Give one use case where low latency may be more important than retransmission."
            ),

            simple_topic_lesson(
                "HTTP",
                """HTTP defines request and response communication used
by web applications.

Methods include GET, POST, PUT, PATCH and DELETE.""",
                """GET /api/courses

POST /api/login

DELETE /api/course/5""",
                "HTTP methods communicate the intended operation.",
                "Design GET and POST endpoints for a student application."
            ),

            simple_topic_lesson(
                "Ports",
                """Ports help identify network services associated with a
host.

A single computer can run multiple network services using
different ports.""",
                """Server IP:
203.0.113.10

HTTPS:
443

HTTP:
80""",
                "Ports distinguish services on a network endpoint.",
                "Explain why a server can provide multiple services simultaneously."
            )

        ]
    )
)


# =========================================================
# 12. CYBERSECURITY
# =========================================================

courses.append(
    course(
        "cybersecurity",
        "Cybersecurity",
        "🛡️",
        "Intermediate → Advanced",
        "Learn how systems and applications are protected from security threats.",
        [

            simple_topic_lesson(
                "Cybersecurity Fundamentals",
                """Cybersecurity protects systems, networks, applications
and information from unauthorized access, misuse, disruption or
destruction.

Security is not only about hacking. It also involves secure design,
authentication, access control, monitoring and recovery.""",
                """Security lifecycle:

Prevent
 ↓
Detect
 ↓
Respond
 ↓
Recover
 ↓
Improve""",
                "Cybersecurity covers prevention, detection, response and recovery.",
                "List three assets that need protection in a college system."
            ),

            simple_topic_lesson(
                "CIA Triad",
                """The CIA triad describes three important security
objectives:

Confidentiality
Integrity
Availability""",
                """Confidentiality:
Only authorized people access data.

Integrity:
Data is not improperly changed.

Availability:
Authorized users can access the service.""",
                "CIA stands for Confidentiality, Integrity and Availability.",
                "Give one real-world example for each CIA principle."
            ),

            simple_topic_lesson(
                "Authentication",
                """Authentication answers the question:

Who are you?

Examples include passwords, one-time codes, security keys and
biometric methods.""",
                """User
 ↓
Username + password
 ↓
Authentication service
 ↓
Access granted / denied""",
                "Authentication verifies identity.",
                "Explain the difference between authentication and authorization."
            ),

            simple_topic_lesson(
                "Authorization",
                """Authorization determines what an authenticated user
is allowed to do.

For example, a student may view marks while an administrator may
modify them.""",
                """Student:
READ marks

Teacher:
READ + UPDATE marks

Admin:
MANAGE users""",
                "Authorization controls permissions.",
                "Design three roles for a college learning platform."
            ),

            simple_topic_lesson(
                "Password Security",
                """Passwords should be long, unique and difficult to
guess.

Applications should not store plaintext passwords. They should
use appropriate password hashing mechanisms.""",
                """Good concept:

password
   ↓
password hashing
   ↓
stored password hash

Not:

password
   ↓
plaintext database""",
                "Passwords must be protected during both authentication and storage.",
                "Explain why storing plaintext passwords is dangerous."
            ),

            simple_topic_lesson(
                "Encryption",
                """Encryption transforms readable information into
protected ciphertext using an encryption method and key.

Decryption reverses the process for an authorized recipient.""",
                """Plaintext
   ↓ encryption + key
Ciphertext
   ↓ decryption + key
Plaintext""",
                "Encryption protects data from unauthorized reading.",
                "Explain where encryption is useful when using public Wi-Fi."
            ),

            simple_topic_lesson(
                "Hashing",
                """Hashing converts input into a fixed-size digest.

Cryptographic hashes are designed so that recovering the original
input is computationally difficult under appropriate assumptions.""",
                """Input:
hello

Hash function
   ↓

Digest:
[fixed-size value]""",
                "Hashing is different from reversible encryption.",
                "Explain one use of hashing in software security."
            ),

            simple_topic_lesson(
                "Phishing",
                """Phishing attempts to trick users into revealing
information or performing an unsafe action by pretending to be a
trusted source.

The strongest defense is careful verification rather than trusting
a message because it looks professional.""",
                """Suspicious message
        ↓
Unexpected link
        ↓
Fake login page
        ↓
Credentials stolen""",
                "Phishing targets people through deception.",
                "List three warning signs of a suspicious login message."
            ),

            simple_topic_lesson(
                "Malware",
                """Malware is malicious software designed to perform
unauthorized or harmful actions.

Examples include ransomware, spyware, worms and some forms of
trojans.""",
                """Malicious file
      ↓
Execution
      ↓
Unauthorized behavior""",
                "Malware is software designed for harmful or unauthorized purposes.",
                "Explain why downloading unknown executable files is risky."
            ),

            simple_topic_lesson(
                "Secure Coding",
                """Secure coding means considering security while
designing and implementing software.

Important practices include validating input, controlling access,
protecting secrets and handling errors safely.""",
                """User input
   ↓
Validate
   ↓
Process safely
   ↓
Database/API""",
                "Security should be considered during development, not only after deployment.",
                "Identify one security risk in a simple login form."
            ),

            simple_topic_lesson(
                "Web Security",
                """Web applications can face risks such as injection,
cross-site scripting, broken access control and insecure
authentication.

Developers should understand common application security
principles and test their own applications responsibly.""",
                """Browser
   ↓
Web application
   ↓
Validate input
   ↓
Database""",
                "Web security protects applications and their users.",
                "Explain why server-side validation is necessary even when JavaScript validates input."
            )

        ]
    )
)


# =========================================================
# 13. AI & MACHINE LEARNING
# =========================================================

courses.append(
    course(
        "ai-ml",
        "AI & Machine Learning",
        "🤖",
        "Intermediate",
        "Understand AI concepts before building machine-learning projects.",
        [

            simple_topic_lesson(
                "What is AI?",
                """Artificial intelligence is a broad field focused on
building systems that perform tasks associated with intelligent
behavior.

Examples include language processing, image recognition and
recommendation systems.""",
                """Input
 ↓
AI system
 ↓
Prediction / decision / generated result""",
                "AI is a broad field containing many techniques and applications.",
                "List three AI applications you use in everyday life."
            ),

            simple_topic_lesson(
                "Machine Learning",
                """Machine learning is a family of methods where systems
learn patterns from data rather than relying entirely on manually
written rules.""",
                """Training data
     ↓
Machine learning model
     ↓
Prediction""",
                "Machine learning learns patterns from examples.",
                "Explain the difference between a fixed rule and a learned pattern."
            ),

            simple_topic_lesson(
                "Training and Testing",
                """A dataset is often divided into training and testing
parts.

Training data helps build the model. Test data is used to estimate
how the model performs on unseen examples.""",
                """Dataset
  ↓
Training data → model
  ↓
Test data → evaluation""",
                "Testing should measure performance on data not used to train the model.",
                "Explain why testing only on training data can be misleading."
            ),

            simple_topic_lesson(
                "Features",
                """Features are measurable inputs used by a machine
learning model.

For example, a house-price model might use area, number of rooms
and location-related information.""",
                """Features:

area = 1200
rooms = 3
age = 5

→ model → predicted price""",
                "Features represent useful input information.",
                "Identify possible features for predicting student performance."
            ),

            simple_topic_lesson(
                "Classification",
                """Classification predicts a category.

Examples include spam/not-spam, pass/fail and healthy/not-healthy
depending on the application and data.""",
                """Email
 ↓
ML classifier
 ↓
Spam / Not Spam""",
                "Classification predicts discrete categories.",
                "Give three classification problems."
            ),

            simple_topic_lesson(
                "Regression",
                """Regression predicts a numerical value.

Examples include estimating house price or predicting demand.""",
                """Input:
area, rooms, location

Model
 ↓
Predicted price: ₹X""",
                "Regression predicts numerical quantities.",
                "Give one regression problem related to college life."
            ),

            simple_topic_lesson(
                "Neural Networks",
                """Neural networks are machine learning models composed
of connected computational units organized into layers.

They are useful for many complex pattern-recognition tasks.""",
                """Input Layer
     ↓
Hidden Layers
     ↓
Output Layer""",
                "Neural networks learn transformations through layers of parameters.",
                "Identify input, hidden and output layers in a simple network."
            ),

            simple_topic_lesson(
                "Generative AI",
                """Generative AI systems produce new content such as
text, images, audio or code based on learned patterns.

They should be used with verification because generated output can
contain mistakes.""",
                """Prompt
 ↓
Generative model
 ↓
Generated text/code/image""",
                "Generative AI creates new content based on learned patterns.",
                "Give three useful educational applications of generative AI."
            )

        ]
    )
)


# =========================================================
# 14. CLOUD & DEVOPS
# =========================================================

courses.append(
    course(
        "cloud-devops",
        "Cloud & DevOps",
        "☁️",
        "Intermediate → Advanced",
        "Understand deployment, cloud infrastructure and software delivery.",
        [

            simple_topic_lesson(
                "Cloud Computing",
                """Cloud computing provides computing resources through
network-accessible services.

Resources can include virtual machines, storage, databases,
networking and managed application services.""",
                """Developer
   ↓
Cloud platform
   ↓
Compute + Storage + Database""",
                "Cloud platforms provide remotely accessible computing resources.",
                "Give three resources that can be hosted in the cloud."
            ),

            simple_topic_lesson(
                "Virtual Machines",
                """A virtual machine provides an isolated computing
environment implemented using virtualization.

It can run an operating system and applications without requiring a
separate physical computer.""",
                """Physical server
 ├── VM 1
 ├── VM 2
 └── VM 3""",
                "Virtualization allows physical resources to host multiple isolated environments.",
                "Explain why virtual machines are useful in cloud platforms."
            ),

            simple_topic_lesson(
                "Docker",
                """Docker packages applications and their dependencies
into containers.

Containers help make software environments more consistent across
development and deployment.""",
                """Application
+ dependencies
+ runtime configuration
        ↓
     Container""",
                "Containers package software with its runtime environment.",
                "Explain why a developer might use Docker before deploying an application."
            ),

            simple_topic_lesson(
                "CI/CD",
                """Continuous Integration and Continuous Delivery or
Deployment automate parts of the software delivery process.

Typical stages include build, test and deployment.""",
                """git push
   ↓
Build
   ↓
Test
   ↓
Deploy""",
                "CI/CD reduces repetitive manual release work.",
                "Design a basic pipeline for a Flask application."
            ),

            simple_topic_lesson(
                "GitHub Actions",
                """GitHub Actions can run automated workflows in response
to repository events.

It can be used for testing, building and deployment tasks.""",
                """name: CI

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4""",
                "GitHub Actions automates repository workflows.",
                "Describe a workflow that tests code after every push."
            ),

            simple_topic_lesson(
                "Deployment",
                """Deployment makes an application available in an
environment where users can access it.

A deployment process should consider configuration, secrets,
logging and monitoring.""",
                """GitHub
   ↓
Build
   ↓
Render
   ↓
Live application""",
                "Deployment moves software from development into a usable environment.",
                "Describe the steps you use to deploy a Flask project."
            )

        ]
    )
)


# =========================================================
# 15. SOFTWARE DEVELOPMENT
# =========================================================

courses.append(
    course(
        "software-development",
        "Software Development",
        "🛠️",
        "Advanced",
        "Learn how real software projects are planned, built, tested and maintained.",
        [

            simple_topic_lesson(
                "Software Development Lifecycle",
                """The software development lifecycle describes the
activities involved in creating and maintaining software.

Common activities include requirements, design, implementation,
testing, deployment and maintenance.""",
                """Requirements
 ↓
Design
 ↓
Development
 ↓
Testing
 ↓
Deployment
 ↓
Maintenance""",
                "Software development is a process, not just writing code.",
                "Apply the lifecycle to a college attendance application."
            ),

            simple_topic_lesson(
                "Requirements",
                """Requirements describe what the system should do and
the constraints under which it should operate.

Clear requirements reduce confusion during development.""",
                """Functional:
Users can create accounts.

Non-functional:
Pages should load quickly.""",
                "Requirements describe expected system behavior and constraints.",
                "Write five requirements for a student learning platform."
            ),

            simple_topic_lesson(
                "Testing",
                """Testing evaluates whether software behaves as
expected.

Unit tests examine small pieces of code. Integration tests examine
how components work together.""",
                """Function:
calculate_total()

Test:
calculate_total(10,20)
Expected:
30""",
                "Testing helps detect defects before users encounter them.",
                "Write three test cases for a calculator."
            ),

            simple_topic_lesson(
                "Debugging",
                """Debugging investigates unexpected behavior and
identifies its cause.

A good debugging process reproduces the problem, isolates the
cause, changes the code and verifies the fix.""",
                """Bug
 ↓
Reproduce
 ↓
Inspect
 ↓
Fix
 ↓
Retest""",
                "Debugging is a systematic investigation rather than random code changes.",
                "Describe how you would debug a login button that does nothing."
            ),

            simple_topic_lesson(
                "APIs and Services",
                """Modern applications are commonly divided into
components that communicate through APIs.

A frontend may request data from a backend service, which may
communicate with a database.""",
                """Frontend
   ↓ API
Flask backend
   ↓
Database""",
                "APIs connect software components.",
                "Design an API for retrieving a student's XP."
            ),

            simple_topic_lesson(
                "Authentication",
                """Authentication systems verify user identity.

Modern applications should protect authentication flows, validate
tokens and avoid exposing secrets in client-side code.""",
                """User
 ↓
Identity provider
 ↓
ID token
 ↓
Backend verification
 ↓
Authorized request""",
                "Identity must be verified before protected operations are performed.",
                "Explain why a backend should verify an authentication token."
            ),

            simple_topic_lesson(
                "Project Architecture",
                """Architecture describes how the major parts of a
software system are organized.

A small web application might separate presentation, API logic,
data access and database storage.""",
                """Browser
  ↓
Frontend
  ↓
Flask API
  ↓
SQLite / Database""",
                "Architecture gives a system a clear structure.",
                "Draw the architecture of CodeQuest AI."
            )

        ]
    )
)


# =========================================================
# 16. CAREER PREPARATION
# =========================================================

courses.append(
    course(
        "career-preparation",
        "Career Preparation",
        "🎯",
        "Job Ready",
        "Turn your technical learning into projects, internships and interview preparation.",
        [

            simple_topic_lesson(
                "Build a GitHub Portfolio",
                """A GitHub profile can demonstrate what you have built
and how you work with source code.

Important projects should have clear repository names, README
files, screenshots and instructions for running the project.""",
                """README should explain:

Project
Features
Technology
Installation
Usage
Screenshots
Future improvements""",
                "A portfolio should make your actual skills easy to understand.",
                "Improve one existing project README."
            ),

            simple_topic_lesson(
                "Build Real Projects",
                """Projects demonstrate the ability to combine
multiple concepts.

A good student project should solve a recognizable problem and
include features you can explain yourself.""",
                """Problem
 ↓
Idea
 ↓
Design
 ↓
Code
 ↓
Testing
 ↓
Deployment""",
                "Projects convert isolated skills into practical experience.",
                "Write three real problems that software could solve for college students."
            ),

            simple_topic_lesson(
                "Resume",
                """A technical resume should clearly present education,
skills, projects, achievements and relevant experience.

Projects should describe what you built and what technologies you
used rather than simply saying 'made an app'.""",
                """Project:
CodeQuest AI

Technologies:
Python, Flask, JavaScript, Firebase

Contribution:
Built learning, quiz and progress features.""",
                "A resume should communicate evidence of skills clearly.",
                "Write three strong project bullet points for one project."
            ),

            simple_topic_lesson(
                "Internship Preparation",
                """Internships can help students gain practical
experience.

Preparation should include fundamentals, projects, communication,
GitHub and consistent applications.""",
                """Skills
+
Projects
+
Resume
+
Applications
+
Interview practice""",
                "Internship preparation combines technical and communication skills.",
                "Create a four-week internship preparation plan."
            ),

            simple_topic_lesson(
                "Coding Interviews",
                """Coding interviews often test problem solving,
data structures, algorithms and the ability to explain your
reasoning.

Understanding the solution is more valuable than memorizing a
single answer.""",
                """Problem
 ↓
Understand
 ↓
Example
 ↓
Approach
 ↓
Code
 ↓
Test
 ↓
Complexity""",
                "Interview coding requires both implementation and explanation.",
                "Solve one array problem and explain its complexity."
            ),

            simple_topic_lesson(
                "Technical Interviews",
                """Technical interviews may ask about programming,
OOP, DBMS, SQL, operating systems, networks and your projects.

You should be able to explain the decisions behind your own
projects.""",
                """Project question:

Why did you choose Flask?

Good answer:
Explain the project requirement,
technology choice and trade-offs.""",
                "Interviewers often evaluate understanding rather than memorized definitions.",
                "Prepare five questions someone could ask about your project."
            ),

            simple_topic_lesson(
                "HR Interview",
                """HR interviews commonly explore communication,
motivation, teamwork, goals and experiences.

Answers should be truthful, specific and supported with examples.""",
                """Situation
Task
Action
Result

This structure can help organize experience-based answers.""",
                "Clear examples make behavioral answers easier to understand.",
                "Prepare an example showing how you solved a difficult project problem."
            )

        ]
    )
)


# =========================================================
# ROADMAP ORDER
# =========================================================

roadmap = [
    c["title"]
    for c in courses
]


# =========================================================
# QUIZ QUESTIONS
# =========================================================

quiz_questions = [

    {
        "id": 1,
        "topic": "Computer Basics",
        "question": "Which component executes program instructions?",
        "options": [
            "CPU",
            "Keyboard",
            "Monitor",
            "Printer"
        ],
        "answer": "CPU"
    },

    {
        "id": 2,
        "topic": "Computer Basics",
        "question": "Which memory is normally temporary?",
        "options": [
            "RAM",
            "SSD",
            "USB drive",
            "DVD"
        ],
        "answer": "RAM"
    },

    {
        "id": 3,
        "topic": "Programming",
        "question": "What is an algorithm?",
        "options": [
            "A sequence of steps for solving a problem",
            "A computer monitor",
            "A storage device",
            "A network cable"
        ],
        "answer": "A sequence of steps for solving a problem"
    },

    {
        "id": 4,
        "topic": "C Programming",
        "question": "Which function is the usual starting point of a C program?",
        "options": [
            "main",
            "start",
            "run",
            "begin"
        ],
        "answer": "main"
    },

    {
        "id": 5,
        "topic": "C Programming",
        "question": "Which symbol is used to get the address of a variable in C?",
        "options": [
            "&",
            "*",
            "#",
            "@"
        ],
        "answer": "&"
    },

    {
        "id": 6,
        "topic": "Python",
        "question": "Which keyword defines a function in Python?",
        "options": [
            "def",
            "function",
            "func",
            "define"
        ],
        "answer": "def"
    },

    {
        "id": 7,
        "topic": "Web Development",
        "question": "Which language defines the structure of a webpage?",
        "options": [
            "HTML",
            "CSS",
            "SQL",
            "C"
        ],
        "answer": "HTML"
    },

    {
        "id": 8,
        "topic": "Web Development",
        "question": "Which technology primarily controls webpage styling?",
        "options": [
            "CSS",
            "HTML",
            "SQL",
            "C"
        ],
        "answer": "CSS"
    },

    {
        "id": 9,
        "topic": "DBMS",
        "question": "Which SQL command retrieves data?",
        "options": [
            "SELECT",
            "INSERT",
            "DELETE",
            "UPDATE"
        ],
        "answer": "SELECT"
    },

    {
        "id": 10,
        "topic": "DBMS",
        "question": "What uniquely identifies a record in a relational table?",
        "options": [
            "Primary key",
            "Folder",
            "Compiler",
            "Loop"
        ],
        "answer": "Primary key"
    },

    {
        "id": 11,
        "topic": "DSA",
        "question": "Which principle does a stack follow?",
        "options": [
            "LIFO",
            "FIFO",
            "Random only",
            "Sorted only"
        ],
        "answer": "LIFO"
    },

    {
        "id": 12,
        "topic": "DSA",
        "question": "Which principle does a normal queue follow?",
        "options": [
            "FIFO",
            "LIFO",
            "Random",
            "Binary"
        ],
        "answer": "FIFO"
    },

    {
        "id": 13,
        "topic": "Operating Systems",
        "question": "What is a process?",
        "options": [
            "A program in execution",
            "A keyboard",
            "A database table",
            "A CSS rule"
        ],
        "answer": "A program in execution"
    },

    {
        "id": 14,
        "topic": "Networks",
        "question": "What does DNS primarily help with?",
        "options": [
            "Resolving domain names to IP addresses",
            "Compiling C programs",
            "Editing images",
            "Formatting disks"
        ],
        "answer": "Resolving domain names to IP addresses"
    },

    {
        "id": 15,
        "topic": "Cybersecurity",
        "question": "What does the C in the CIA triad represent?",
        "options": [
            "Confidentiality",
            "Compilation",
            "Compression",
            "Connection"
        ],
        "answer": "Confidentiality"
    },

    {
        "id": 16,
        "topic": "Cybersecurity",
        "question": "What does authentication verify?",
        "options": [
            "Identity",
            "Screen size",
            "File extension",
            "CPU speed"
        ],
        "answer": "Identity"
    },

    {
        "id": 17,
        "topic": "AI",
        "question": "What does machine learning primarily learn from?",
        "options": [
            "Data",
            "Keyboard keys",
            "Monitor pixels only",
            "Power supply"
        ],
        "answer": "Data"
    },

    {
        "id": 18,
        "topic": "Cloud",
        "question": "What is Docker commonly used for?",
        "options": [
            "Containerizing applications",
            "Writing only HTML",
            "Replacing all databases",
            "Creating keyboards"
        ],
        "answer": "Containerizing applications"
    },

    {
        "id": 19,
        "topic": "Software Development",
        "question": "What is testing used for?",
        "options": [
            "Finding defects and verifying behavior",
            "Increasing monitor size",
            "Replacing RAM",
            "Changing Wi-Fi passwords only"
        ],
        "answer": "Finding defects and verifying behavior"
    },

    {
        "id": 20,
        "topic": "Career",
        "question": "What should a project README explain?",
        "options": [
            "The project, setup and usage",
            "Only the developer's name",
            "Only the project color",
            "Nothing"
        ],
        "answer": "The project, setup and usage"
    }

]


# =========================================================
# CAREER GUIDE
# =========================================================

careers = [

    {
        "title": "🎓 Internship Preparation",
        "content": """Start with strong programming fundamentals.
Build two or three projects that you can explain completely.
Keep your GitHub repositories organized.

Learn Git, practice problem solving and prepare a simple technical
resume.

Apply consistently rather than waiting until you feel perfect.

During interviews, be ready to explain what you personally built,
what problems you faced and how you solved them."""
    },

    {
        "title": "💼 Placement Preparation",
        "content": """Prepare programming, OOP, DSA, DBMS, SQL, operating
systems, computer networks and your project knowledge.

Practice writing code without depending entirely on autocomplete.

For every major project, prepare answers for:

What problem does it solve?
Why did you choose the technology?
What was difficult?
How does the architecture work?
What would you improve?"""
    },

    {
        "title": "🐙 GitHub Portfolio",
        "content": """Keep your important projects public when appropriate.

Use meaningful repository names.

Write useful README files.

Include:
Project description
Features
Technology
Installation
Usage
Screenshots
Future improvements

Do not upload passwords, API keys or private credentials."""
    },

    {
        "title": "🚀 Software Developer Roadmap",
        "content": """Start with programming fundamentals.

Then learn:
C or C++
Python
Git/GitHub
HTML/CSS/JavaScript
SQL
DSA
OOP
Operating Systems
Networks
APIs
Testing
Deployment

After the fundamentals, choose a development direction such as
web, mobile, backend, cloud, data or AI."""
    },

    {
        "title": "📄 Resume",
        "content": """Keep the resume readable and focused.

Highlight:
Education
Technical skills
Projects
Achievements
Internships
Certifications
GitHub
Portfolio

For projects, explain the technology and your actual contribution
instead of using vague statements."""
    },

    {
        "title": "🧠 Interview Preparation",
        "content": """Practice explaining concepts in simple language.

For coding problems:

Understand the problem.
Create examples.
Think of an approach.
Write the code.
Test edge cases.
Explain complexity.

For project interviews, understand every important part of your
own project."""
    }

]


# =========================================================
# USER HELPERS
# =========================================================

def get_user(firebase_uid):

    db = get_db()

    user = db.execute(
        """
        SELECT *
        FROM users
        WHERE firebase_uid = ?
        """,
        (firebase_uid,)
    ).fetchone()

    db.close()

    return user


def create_or_update_user(
    firebase_uid,
    email,
    name,
    photo_url
):

    today = date.today().isoformat()

    db = get_db()

    user = db.execute(
        """
        SELECT *
        FROM users
        WHERE firebase_uid = ?
        """,
        (firebase_uid,)
    ).fetchone()

    if user:

        last_active = user["last_active"]

        streak = user["streak"] or 1

        if last_active and last_active != today:

            try:

                previous = date.fromisoformat(
                    last_active
                )

                current = date.fromisoformat(
                    today
                )

                difference = (
                    current - previous
                ).days

                if difference == 1:
                    streak += 1

                elif difference > 1:
                    streak = 1

            except Exception:
                streak = 1

        db.execute(
            """
            UPDATE users

            SET
                email = ?,
                name = ?,
                photo_url = ?,
                streak = ?,
                last_active = ?

            WHERE firebase_uid = ?
            """,
            (
                email,
                name,
                photo_url,
                streak,
                today,
                firebase_uid
            )
        )

    else:

        db.execute(
            """
            INSERT INTO users(
                firebase_uid,
                email,
                name,
                photo_url,
                xp,
                streak,
                last_active
            )
            VALUES (?, ?, ?, ?, 0, 1, ?)
            """,
            (
                firebase_uid,
                email,
                name,
                photo_url,
                today
            )
        )

    db.commit()

    user = db.execute(
        """
        SELECT *
        FROM users
        WHERE firebase_uid = ?
        """,
        (firebase_uid,)
    ).fetchone()

    db.close()

    return user


def firebase_user_required():

    if not firebase_admin or not firebase_auth:
        return None

    auth_header = request.headers.get(
        "Authorization",
        ""
    )

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header[7:].strip()

    if not token:
        return None

    try:

        decoded = firebase_auth.verify_id_token(
            token
        )

        return decoded

    except Exception as error:

        print("Firebase token verification error:", error)

        return None


def require_firebase(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        user = firebase_user_required()

        if not user:
            return jsonify({
                "error": "Authentication required."
            }), 401

        return function(
            user,
            *args,
            **kwargs
        )

    return wrapper


# =========================================================
# LEVEL
# =========================================================

LEVELS = [
    (0, "Code Explorer"),
    (100, "Logic Builder"),
    (250, "Bug Hunter"),
    (500, "Code Warrior"),
    (900, "Algorithm Master"),
    (1400, "Software Crafter"),
    (2000, "Tech Adventurer"),
    (3000, "CodeQuest Legend")
]


def get_level(xp):

    current_index = 0

    for index, item in enumerate(LEVELS):

        if xp >= item[0]:
            current_index = index

    xp_start = LEVELS[current_index][0]

    if current_index + 1 < len(LEVELS):

        xp_next = LEVELS[current_index + 1][0]

    else:

        xp_next = xp_start + 1000

    return {
        "number": current_index + 1,
        "name": LEVELS[current_index][1],
        "xp": xp,
        "current_level_xp": xp_start,
        "next_level_xp": xp_next
    }


# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/health")
def health():

    compiler = "configured"

    try:

        request.urlopen(
            urllib.request.Request(
                "https://wandbox.org/api/list.json",
                method="GET"
            ),
            timeout=5
        )

    except Exception:

        compiler = "unreachable"

    return jsonify({
        "status": "ok",
        "database": os.path.abspath(
            DATABASE_PATH
        ),
        "courses": len(courses),
        "lessons": sum(
            len(c["chapters"])
            for c in courses
        ),
        "quiz_questions": len(
            quiz_questions
        ),
        "compiler": compiler,
        "firebase_admin": bool(
            firebase_admin
        )
    })


@app.route("/api/courses")
def api_courses():

    result = []

    for item in courses:

        result.append({
            "id": item["id"],
            "title": item["title"],
            "icon": item["icon"],
            "level": item["level"],
            "description": item["description"],
            "chapters": item["chapters"]
        })

    return jsonify(result)


@app.route("/api/course/<course_id>")
def api_course(course_id):

    for item in courses:

        if item["id"] == course_id:
            return jsonify(item)

    return jsonify({
        "error": "Course not found."
    }), 404


@app.route("/api/roadmap")
def api_roadmap():

    return jsonify({
        "courses": roadmap
    })


# =========================================================
# FIREBASE LOGIN
# =========================================================

@app.route(
    "/api/firebase-login",
    methods=["POST"]
)
def firebase_login():

    if not firebase_admin or not firebase_auth:

        return jsonify({
            "error":
                "Firebase Admin is not configured on the server."
        }), 503

    data = request.get_json(
        silent=True
    ) or {}

    id_token = data.get(
        "idToken",
        ""
    )

    if not id_token:

        return jsonify({
            "error": "Missing Firebase ID token."
        }), 400

    try:

        decoded = firebase_auth.verify_id_token(
            id_token
        )

        uid = decoded["uid"]

        user = create_or_update_user(
            uid,
            decoded.get("email", ""),
            decoded.get("name", "Student"),
            decoded.get("picture", "")
        )

        return jsonify({
            "success": True,
            "user": dict(user)
        })

    except Exception as error:

        print("Firebase login error:", error)

        return jsonify({
            "error": "Firebase authentication failed."
        }), 401


# =========================================================
# PROGRESS
# =========================================================

@app.route("/api/progress")
@require_firebase
def api_progress(firebase_user):

    uid = firebase_user["uid"]

    create_or_update_user(
        uid,
        firebase_user.get("email", ""),
        firebase_user.get("name", "Student"),
        firebase_user.get("picture", "")
    )

    db = get_db()

    user = db.execute(
        """
        SELECT *
        FROM users
        WHERE firebase_uid = ?
        """,
        (uid,)
    ).fetchone()

    completed_rows = db.execute(
        """
        SELECT lesson_key
        FROM progress
        WHERE firebase_uid = ?
        ORDER BY completed_at
        """,
        (uid,)
    ).fetchall()

    db.close()

    completed = [
        row["lesson_key"]
        for row in completed_rows
    ]

    level = get_level(
        user["xp"]
    )

    return jsonify({
        "xp": user["xp"],
        "streak": user["streak"],
        "completed": completed,
        "level": level
    })


@app.route(
    "/api/progress/lesson",
    methods=["POST"]
)
@require_firebase
def complete_lesson(firebase_user):

    data = request.get_json(
        silent=True
    ) or {}

    course_id = str(
        data.get("course_id", "")
    )

    lesson_title = str(
        data.get("lesson_title", "")
    )

    if not course_id or not lesson_title:

        return jsonify({
            "error": "Missing lesson information."
        }), 400

    lesson_key = (
        course_id +
        "::" +
        lesson_title
    )

    uid = firebase_user["uid"]

    db = get_db()

    existing = db.execute(
        """
        SELECT id
        FROM progress
        WHERE firebase_uid = ?
        AND lesson_key = ?
        """,
        (
            uid,
            lesson_key
        )
    ).fetchone()

    if existing:

        user = db.execute(
            """
            SELECT *
            FROM users
            WHERE firebase_uid = ?
            """,
            (uid,)
        ).fetchone()

        db.close()

        return jsonify({
            "success": True,
            "already_completed": True,
            "xp": user["xp"]
        })

    db.execute(
        """
        INSERT INTO progress(
            firebase_uid,
            lesson_key
        )
        VALUES (?, ?)
        """,
        (
            uid,
            lesson_key
        )
    )

    db.execute(
        """
        UPDATE users
        SET xp = xp + 20
        WHERE firebase_uid = ?
        """,
        (uid,)
    )

    db.commit()

    user = db.execute(
        """
        SELECT *
        FROM users
        WHERE firebase_uid = ?
        """,
        (uid,)
    ).fetchone()

    db.close()

    return jsonify({
        "success": True,
        "already_completed": False,
        "xp": user["xp"],
        "level": get_level(
            user["xp"]
        )
    })


# =========================================================
# STATS
# =========================================================

@app.route("/api/stats")
@require_firebase
def api_stats(firebase_user):

    uid = firebase_user["uid"]

    db = get_db()

    user = db.execute(
        """
        SELECT *
        FROM users
        WHERE firebase_uid = ?
        """,
        (uid,)
    ).fetchone()

    completed = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM progress
        WHERE firebase_uid = ?
        """,
        (uid,)
    ).fetchone()["count"]

    db.close()

    if not user:

        user = create_or_update_user(
            uid,
            firebase_user.get("email", ""),
            firebase_user.get("name", "Student"),
            firebase_user.get("picture", "")
        )

    return jsonify({
        "xp": user["xp"],
        "streak": user["streak"],
        "completed": completed,
        "level": get_level(
            user["xp"]
        )
    })


# =========================================================
# QUIZ
# =========================================================

@app.route("/api/quiz")
def api_quiz():

    safe_questions = []

    for question in quiz_questions:

        safe_questions.append({
            "id": question["id"],
            "topic": question["topic"],
            "question": question["question"],
            "options": question["options"]
        })

    return jsonify({
        "questions": safe_questions
    })


@app.route(
    "/api/quiz/submit",
    methods=["POST"]
)
def submit_quiz():

    data = request.get_json(
        silent=True
    ) or {}

    answers = data.get(
        "answers",
        []
    )

    if not isinstance(
        answers,
        list
    ):

        return jsonify({
            "error": "Invalid answers."
        }), 400

    question_map = {
        str(q["id"]): q
        for q in quiz_questions
    }

    score = 0

    for item in answers:

        question_id = str(
            item.get("id", "")
        )

        answer = str(
            item.get("answer", "")
        )

        question = question_map.get(
            question_id
        )

        if question and answer == str(
            question["answer"]
        ):

            score += 1

    total = len(answers)

    if total == 0:
        percentage = 0
    else:
        percentage = round(
            score / total * 100
        )

    return jsonify({
        "success": True,
        "score": score,
        "total": total,
        "percentage": percentage
    })


# =========================================================
# QUIZ VIOLATION
# =========================================================

@app.route(
    "/api/quiz/violation",
    methods=["POST"]
)
def quiz_violation():

    return jsonify({
        "success": True
    })


# =========================================================
# CAREER
# =========================================================

@app.route("/api/careers")
def api_careers():

    return jsonify(careers)


@app.route("/api/career-roadmap")
def career_roadmap():

    return jsonify({
        "steps": [
            "Programming fundamentals",
            "Git and GitHub",
            "Data Structures and Algorithms",
            "DBMS and SQL",
            "Operating Systems",
            "Computer Networks",
            "Projects",
            "Resume",
            "Internships",
            "Technical interviews",
            "HR preparation",
            "Job applications"
        ]
    })


# =========================================================
# PROJECT IDEAS
# =========================================================

@app.route("/api/projects")
def projects():

    return jsonify([
        {
            "title": "Student Study Planner",
            "level": "Beginner",
            "description":
                "Plan subjects, assignments and tests."
        },
        {
            "title": "College Attendance Tracker",
            "level": "Beginner",
            "description":
                "Track attendance and calculate required attendance."
        },
        {
            "title": "Expense Tracker",
            "level": "Intermediate",
            "description":
                "Record expenses and visualize spending."
        },
        {
            "title": "CodeQuest AI",
            "level": "Advanced",
            "description":
                "Gamified computer science learning platform."
        }
    ])


# =========================================================
# C COMPILER
# =========================================================

@app.route(
    "/api/compile",
    methods=["POST"]
)
def compile_c():

    data = request.get_json(
        silent=True
    ) or {}

    code = data.get(
        "code",
        ""
    )

    stdin = data.get(
        "stdin",
        ""
    )

    if not isinstance(
        code,
        str
    ):

        return jsonify({
            "success": False,
            "error": "Invalid code."
        }), 400

    if len(code) > 30000:

        return jsonify({
            "success": False,
            "error":
                "Code is too large. Keep it under 30,000 characters."
        }), 400

    if not code.strip():

        return jsonify({
            "success": False,
            "error": "Please enter C code."
        }), 400

    payload = {
        "compiler": WANDBOX_COMPILER,
        "code": code,
        "stdin": str(stdin),
        "options": "warning"
    }

    body = json.dumps(
        payload
    ).encode("utf-8")

    http_request = urllib.request.Request(
        WANDBOX_URL,
        data=body,
        headers={
            "Content-Type":
                "application/json",
            "Accept":
                "application/json"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            http_request,
            timeout=30
        ) as response:

            raw = response.read().decode(
                "utf-8",
                errors="replace"
            )

            result = json.loads(raw)

        compiler_message = (
            result.get(
                "compiler_message"
            )
            or ""
        )

        program_message = (
            result.get(
                "program_message"
            )
            or ""
        )

        status = result.get(
            "status"
        )

        if compiler_message:

            return jsonify({
                "success": False,
                "error":
                    compiler_message,
                "output":
                    program_message
            })

        if status:

            status_text = str(
                status
            )

            if (
                "Finish" not in
                status_text
                and "Success" not in
                status_text
                and program_message == ""
            ):

                return jsonify({
                    "success": False,
                    "error":
                        status_text
                })

        return jsonify({
            "success": True,
            "output":
                program_message
        })

    except urllib.error.HTTPError as error:

        details = ""

        try:
            details = error.read().decode(
                "utf-8",
                errors="replace"
            )
        except Exception:
            pass

        return jsonify({
            "success": False,
            "error":
                "Compiler service returned HTTP "
                + str(error.code)
                + ". "
                + details[:1000]
        }), 502

    except Exception as error:

        print(
            "Compiler error:",
            error
        )

        return jsonify({
            "success": False,
            "error":
                "Unable to reach the C compiler service."
        }), 502


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def not_found(error):

    if request.path.startswith("/api/"):

        return jsonify({
            "error": "API endpoint not found."
        }), 404

    return render_template(
        "index.html"
    )


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "error":
            "Internal server error."
    }), 500


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            "5000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
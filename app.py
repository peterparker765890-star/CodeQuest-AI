from flask import Flask, jsonify, request
import os
import json
import random
import sqlite3
import requests
from datetime import datetime

# ============================================================
# CODEQUEST AI
# Learn • Practice • Play • Build
# Backend v2.0
# ============================================================

app = Flask(__name__)

DATABASE_PATH = os.getenv("DATABASE_PATH", "codequest.db")
WANDBOX_URL = "https://wandbox.org/api/compile.json"


# ============================================================
# DATABASE
# ============================================================

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY,
            email TEXT,
            name TEXT,
            photo TEXT,
            created_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            uid TEXT,
            course_id TEXT,
            chapter_index INTEGER,
            completed INTEGER DEFAULT 0,
            PRIMARY KEY(uid, course_id, chapter_index)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT,
            score INTEGER,
            total INTEGER,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ============================================================
# HELPER
# ============================================================

def lesson(title, explanation, example=None, practice=None):
    return {
        "title": title,
        "lesson": explanation,
        "sample": example or "",
        "practice": practice or ""
    }


def course(cid, title, icon, level, description, chapters):
    return {
        "id": cid,
        "title": title,
        "icon": icon,
        "level": level,
        "description": description,
        "chapters": chapters
    }


# ============================================================
# COMPLETE COURSE SYLLABUS
# ============================================================

courses = [

# ============================================================
# 1 COMPUTER BASICS
# ============================================================

course(
    "computer-basics",
    "Computer Basics",
    "💻",
    "Beginner",
    "Build a strong foundation in computers before entering programming and software development.",
    [

        lesson(
            "What is a Computer?",
            """A computer is an electronic machine that accepts data, processes it according to instructions, stores information, and produces useful output.

Almost every digital system you use follows this basic idea. When you type a message, the keyboard provides input, the processor handles the instructions, memory temporarily holds the information, and the screen displays the result.

Understanding this input-process-output-storage cycle is important because programming is essentially the process of giving a computer precise instructions to perform useful tasks.

Real-world example:
When you calculate 25 + 75 using a calculator application, the numbers are input, the processor performs the calculation, and the answer 100 becomes the output.

Think of a computer as a very fast instruction-following machine. It does not independently understand what you mean. It executes instructions according to rules.""",

            """Input → Processing → Output

Keyboard → CPU → Monitor

Example:
10 + 20
        → Processing
        → 30""",

            "Identify five examples of computers you use in daily life."
        ),

        lesson(
            "Hardware and Software",
            """Hardware refers to the physical components of a computer that you can touch. Examples include the keyboard, monitor, motherboard, processor, RAM and storage drive.

Software is a collection of instructions that tells hardware what to do. Windows, web browsers, games, mobile applications and programming tools are examples of software.

Hardware and software depend on each other. A powerful processor without software has little practical use, while software cannot execute without suitable hardware.

For example, when you open a browser, the browser software requests resources from the operating system, which communicates with hardware such as RAM, CPU and storage.""",

            """Hardware:
CPU
RAM
Keyboard
SSD
Monitor

Software:
Windows
Chrome
VS Code
Python""",

            "List five hardware components and five software applications."
        ),

        lesson(
            "CPU and Processor",
            """The Central Processing Unit, commonly called the CPU, executes instructions and performs calculations.

A processor contains components such as the control unit and arithmetic and logic unit. Modern CPUs also contain multiple cores, allowing several tasks to be processed concurrently.

CPU performance is influenced by factors such as architecture, number of cores, clock frequency, cache and workload. A higher clock speed alone does not automatically mean one processor is faster in every task.

For a programmer, understanding the CPU helps explain why algorithms, loops and inefficient programs can affect performance.""",

            """Example:

Program:
Calculate 10 + 20

CPU receives instruction
        ↓
Performs calculation
        ↓
Produces 30""",

            "Explain why a CPU is called the brain of a computer."
        ),

        lesson(
            "RAM and Storage",
            """RAM and storage are both used to hold information, but they serve different purposes.

RAM is temporary working memory. Programs currently running use RAM because it provides fast access to data. When the computer is powered off, information stored only in RAM is lost.

Storage devices such as SSDs and hard drives retain files even after shutdown.

For example, when you open a Python project, the project files remain on storage, but the running Python editor and its active data are loaded into RAM.""",

            """Storage:
project.py
↓
RAM
↓
CPU
↓
Program execution""",

            "Explain the difference between RAM and SSD storage."
        ),

        lesson(
            "Operating Systems",
            """An operating system is system software that manages computer hardware and provides services to applications.

Windows, Linux, macOS, Android and iOS are examples of operating systems.

The operating system manages processes, memory, files, devices, permissions and networking.

When you open a program, you normally do not directly tell the CPU where every instruction should be placed. The operating system manages those resources for you.""",

            """Application
     ↓
Operating System
     ↓
Hardware

Example:
Chrome
↓
Windows
↓
CPU + RAM + Network""",

            "Name three operating systems and one device where each is commonly used."
        ),

        lesson(
            "Files, Folders and Extensions",
            """A file is a collection of stored information. A folder is used to organize files.

File extensions usually indicate the type of content or the application associated with it.

For example, .txt represents text, .jpg commonly represents an image, .py represents Python source code and .html represents an HTML document.

Understanding files and folders is essential for programming because projects usually contain many source files, configuration files, assets and documentation.""",

            """project/
├── app.py
├── index.html
├── style.css
└── README.md""",

            "Create a folder structure for a small Python project."
        ),

        lesson(
            "Binary and Digital Data",
            """Computers fundamentally process digital information using binary values.

Binary uses two symbols: 0 and 1. A single binary digit is called a bit. Eight bits form one byte.

Text, images, audio and video are ultimately represented using numerical data that computers can process.

You do not normally need to manually convert every piece of data into binary, because programming languages and operating systems handle those conversions for you. However, understanding binary becomes useful when learning memory, networking, encoding and cybersecurity.""",

            """Decimal 5

Binary:
101

Because:
4 + 0 + 1 = 5""",

            "Convert decimal 10 into binary."
        )
    ]
),

# ============================================================
# 2 WINDOWS
# ============================================================

course(
    "windows",
    "Windows & Digital Skills",
    "🪟",
    "Beginner",
    "Learn practical Windows skills required for college, programming and everyday computer use.",
    [

        lesson(
            "Windows Desktop",
            """The Windows desktop provides access to applications, files, system settings and common tools.

The Start menu, taskbar, notification area, desktop shortcuts and File Explorer form some of the most frequently used parts of the Windows interface.

Learning the desktop efficiently saves time when working on programming projects because developers repeatedly switch between editors, terminals, browsers and folders.""",

            """Useful shortcuts:

Win + E → File Explorer
Win + R → Run
Alt + Tab → Switch apps
Ctrl + Shift + Esc → Task Manager""",

            "Practice opening File Explorer and Task Manager using keyboard shortcuts."
        ),

        lesson(
            "File Explorer",
            """File Explorer allows you to browse, create, move, copy, rename and delete files and folders.

A programmer should become comfortable navigating directories because coding projects depend heavily on correct file locations.

For example, when running a Python application from a terminal, the terminal must usually be positioned in the correct project directory.""",

            """C:\\Users\\Student\\Documents\\CodeQuest\\

    app.py
    requirements.txt
    templates\\
    static\\""",

            "Create a folder named CodeProjects and create three subfolders."
        ),

        lesson(
            "Windows Terminal and Command Prompt",
            """A terminal allows you to interact with the operating system using commands rather than graphical controls.

Developers use terminals for installing packages, running programs, managing Git repositories, starting servers and automating tasks.

Learning basic commands early makes later programming and Git lessons much easier.""",

            """cd CodeProjects
dir

Python example:
python app.py""",

            "Open Command Prompt and navigate into a folder using cd."
        ),

        lesson(
            "Installing Software Safely",
            """Software should be downloaded from trusted sources whenever possible.

Before installing a development tool, check its official documentation, supported operating system and system requirements.

Developers commonly install editors, programming languages, Git, database tools and browsers.

Avoid downloading unknown executable files simply because a website claims they are required.""",

            """Typical development setup:

Browser
↓
VS Code
↓
Python / C / Java
↓
Git
↓
Project""",

            "List the development tools you expect to use during college."
        )
    ]
),

# ============================================================
# 3 WORD
# ============================================================

course(
    "ms-word",
    "Microsoft Word",
    "📝",
    "Beginner",
    "Learn professional document creation for assignments, reports, resumes and project documentation.",
    [

        lesson(
            "Creating a Professional Document",
            """Microsoft Word is commonly used to create assignments, reports, resumes and documentation.

A professional document is more than typing text. It should have consistent headings, readable spacing, appropriate fonts, page structure and clear organization.

For college work, styles and headings are particularly useful because they allow long documents to remain consistent.""",

            """Example structure:

PROJECT REPORT

1. Introduction
2. Objectives
3. Methodology
4. Results
5. Conclusion""",

            "Create a one-page project report using headings."
        ),

        lesson(
            "Formatting and Styles",
            """Formatting controls how information appears on a page. Styles provide a consistent way to apply headings, titles and body text.

Instead of manually changing every heading, a document can use Heading 1, Heading 2 and normal text styles.

This becomes especially useful for long technical documentation.""",

            """Title
↓
Heading 1
↓
Heading 2
↓
Body paragraph""",

            "Create three heading levels in a Word document."
        ),

        lesson(
            "Tables and Technical Documentation",
            """Tables allow structured information to be presented clearly.

Students commonly use tables for experiment readings, comparison charts, project requirements and schedules.

A good table should have meaningful column headings and consistent formatting rather than excessive decoration.""",

            """| Component | Purpose |
| CPU | Processing |
| RAM | Temporary memory |
| SSD | Storage |""",

            "Create a hardware comparison table."
        )
    ]
),

# ============================================================
# 4 EXCEL
# ============================================================

course(
    "ms-excel",
    "Microsoft Excel",
    "📊",
    "Beginner",
    "Learn spreadsheets, formulas, functions, charts and practical data analysis.",
    [

        lesson(
            "Spreadsheet Fundamentals",
            """Excel organizes information into rows and columns. The intersection of a row and column is called a cell.

Cells can contain text, numbers, dates and formulas.

Spreadsheets are useful for marks, budgets, attendance, inventory, calculations and simple data analysis.""",

            """A1 = 10
A2 = 20

A3:
=A1+A2

Result:
30""",

            "Create a marks sheet for five students."
        ),

        lesson(
            "Formulas and Functions",
            """Excel formulas allow calculations to be performed automatically.

Functions such as SUM, AVERAGE, MAX and MIN provide ready-made operations.

The important concept is that formulas can reference cells. When the underlying data changes, the result can update automatically.""",

            """=SUM(B2:B6)

=AVERAGE(B2:B6)

=MAX(B2:B6)

=MIN(B2:B6)""",

            "Calculate total and average marks for five subjects."
        ),

        lesson(
            "Charts and Data Visualization",
            """Charts convert numerical information into visual patterns.

Bar charts are useful for comparisons, line charts are useful for changes over time, and pie charts can represent proportions.

Choosing the appropriate chart is more important than simply making a colorful chart.""",

            """Monthly Sales

Jan █████
Feb ███████
Mar █████████
Apr ██████""",

            "Create a chart showing monthly sales."
        )
    ]
),

# ============================================================
# 5 POWERPOINT
# ============================================================

course(
    "powerpoint",
    "Microsoft PowerPoint",
    "🎨",
    "Beginner",
    "Create clean presentations for college seminars, projects and technical demonstrations.",
    [

        lesson(
            "Presentation Structure",
            """A presentation should guide the audience through a clear story.

A typical technical presentation can contain a title, problem statement, objectives, methodology, results and conclusion.

Slides should support the speaker rather than contain every sentence the speaker plans to say.""",

            """Slide 1 → Title
Slide 2 → Problem
Slide 3 → Solution
Slide 4 → Demo
Slide 5 → Conclusion""",

            "Design a five-slide presentation for a software project."
        ),

        lesson(
            "Visual Design",
            """Good presentation design uses consistent typography, spacing and visual hierarchy.

Avoid filling slides with large paragraphs. Use short points, diagrams, screenshots and meaningful visuals when they improve understanding.

Consistency makes a presentation easier for an audience to follow.""",

            """Bad:
One huge paragraph

Better:
• Problem
• Cause
• Solution
• Result""",

            "Convert one paragraph-heavy slide into a clean presentation slide."
        )
    ]
),

# ============================================================
# 6 INTERNET
# ============================================================

course(
    "internet",
    "Internet, Email & Online Tools",
    "🌐",
    "Beginner",
    "Understand how the web, browsers, email, URLs, search and online services work.",
    [

        lesson(
            "What is the Internet?",
            """The Internet is a global network of interconnected computer networks.

When you open a website, your device communicates with remote servers through networking infrastructure.

The Internet and the World Wide Web are related but not identical. The Web is one service that operates over the Internet.""",

            """Your phone
   ↓
Wi-Fi / Mobile Network
   ↓
Internet
   ↓
Web Server
   ↓
Website""",

            "Explain the difference between Internet and Web."
        ),

        lesson(
            "How a Website Opens",
            """When you enter a website address, several steps occur before the page appears.

The browser identifies the destination, DNS can translate a domain name into an IP address, a connection is established, and the server sends data back.

The browser then interprets HTML, CSS and JavaScript to display the page.""",

            """example.com
↓
DNS
↓
IP address
↓
Server
↓
HTML/CSS/JS
↓
Browser""",

            "Describe the basic journey from entering a URL to seeing a webpage."
        ),

        lesson(
            "Email and Digital Communication",
            """Email is an electronic messaging system used for personal, academic and professional communication.

Professional emails should have a clear subject, appropriate greeting, concise message and useful closing.

Students should also understand attachments, CC, BCC, spam and phishing.""",

            """Subject:
Project Submission - CodeQuest AI

Body:
Hello Sir,

I have attached the project report.

Thank you.""",

            "Write a professional email requesting project feedback."
        )
    ]
),

# ============================================================
# 7 GIT
# ============================================================

course(
    "git-github",
    "Git & GitHub",
    "🐙",
    "Beginner → Intermediate",
    "Learn version control and professional project collaboration.",
    [

        lesson(
            "Why Version Control Exists",
            """Imagine modifying a project for several weeks and accidentally deleting an important section. Version control allows developers to track changes and return to previous versions.

Git records changes to files and allows developers to create meaningful checkpoints called commits.

This is one reason Git has become an important part of modern software development.""",

            """Project
↓
git init
↓
git add .
↓
git commit
↓
History""",

            "Create a Git repository for a small project."
        ),

        lesson(
            "Git Basic Workflow",
            """A common Git workflow involves modifying files, reviewing changes, staging them and creating a commit.

The staging area allows you to choose what should be included in the next commit.

Understanding this workflow is more useful than memorizing commands without understanding what they do.""",

            """git status
git add .
git commit -m "Add login page"
git log""",

            "Make two commits in a practice repository."
        ),

        lesson(
            "GitHub Repositories",
            """GitHub provides remote hosting for Git repositories and adds collaboration features such as issues, pull requests and project discussions.

A GitHub repository can also act as a portfolio demonstrating your projects and development progress.

A good repository should normally contain a useful README and understandable project structure.""",

            """Local project
     ↓
     Git
     ↓
   GitHub
     ↓
Portfolio / Collaboration""",

            "Create a README for one of your projects."
        ),

        lesson(
            "Branches and Pull Requests",
            """Branches allow developers to work on changes without immediately modifying the main development line.

A pull request provides a place to review proposed changes before merging them.

This workflow becomes important when multiple developers work on the same project.""",

            """main
 │
 ├── feature-login
 │
 └── feature-dashboard""",

            "Create a feature branch and merge it into main."
        )
    ]
),

# ============================================================
# 8 C
# ============================================================

course(
    "c",
    "C Programming",
    "🔵",
    "Beginner → Intermediate",
    "Build programming fundamentals using C, from variables to pointers and data structures.",
    [

        lesson(
            "Your First C Program",
            """C is a compiled programming language that gives programmers relatively direct control over memory and system resources.

A C program begins execution from the main function.

The preprocessor directive #include <stdio.h> provides declarations for standard input/output functions such as printf.

Learning C gives a strong foundation for understanding programming fundamentals, memory and data structures.""",

            """#include <stdio.h>

int main() {
    printf("Hello, CodeQuest!");
    return 0;
}""",

            "Change the program so it prints your name."
        ),

        lesson(
            "Variables and Data Types",
            """A variable is a named storage location used by a program to hold a value.

The data type tells the compiler what kind of value the variable is expected to contain.

For example, int is commonly used for whole numbers, float for decimal values and char for a character.

Choosing appropriate data types helps a program represent information correctly.""",

            """int age = 18;
float height = 5.8;
char grade = 'A';

printf("%d", age);""",

            "Create variables representing your age, percentage and grade."
        ),

        lesson(
            "Input with scanf",
            """Programs become interactive when they accept information from the user.

The scanf function can read formatted input from standard input. When reading into a variable, scanf generally needs the variable's address, which is why the address-of operator & is commonly used.

This lesson is an important bridge between fixed-output programs and interactive applications.""",

            """#include <stdio.h>

int main() {
    int a, b;

    printf("Enter two numbers: ");
    scanf("%d %d", &a, &b);

    printf("Sum = %d", a + b);

    return 0;
}""",

            "Modify the program to calculate multiplication."
        ),

        lesson(
            "Conditional Statements",
            """Programs often need to make decisions.

An if statement executes code when a condition is true. else provides an alternative path.

This concept is fundamental to almost every programming language because real applications constantly make decisions based on data.""",

            """int age = 20;

if (age >= 18) {
    printf("Adult");
} else {
    printf("Minor");
}""",

            "Write a program that checks whether a number is positive, negative or zero."
        ),

        lesson(
            "Loops",
            """Loops allow a program to repeat instructions without writing the same code repeatedly.

The for loop is useful when the number of repetitions is known. while is useful when repetition depends on a condition.

Loops are used everywhere from processing arrays to handling repeated user input.""",

            """for (int i = 1; i <= 5; i++) {
    printf("%d\\n", i);
}""",

            "Print the multiplication table of 7."
        ),

        lesson(
            "Arrays",
            """An array stores multiple values of the same type in contiguous memory locations.

Instead of creating separate variables for ten marks, an array can store them under one variable name and use an index to access individual values.

Arrays are fundamental to later topics such as strings, sorting and data structures.""",

            """int marks[5] = {
    80, 75, 91, 68, 88
};

printf("%d", marks[2]);""",

            "Calculate the average of five numbers stored in an array."
        ),

        lesson(
            "Functions",
            """Functions divide a program into reusable blocks.

A function can receive input through parameters and return a result.

Using functions makes programs easier to understand, test and maintain because large problems can be divided into smaller responsibilities.""",

            """int add(int a, int b) {
    return a + b;
}

int result = add(10, 20);""",

            "Create a function that returns the square of a number."
        ),

        lesson(
            "Pointers",
            """A pointer is a variable capable of storing a memory address.

Pointers are one of C's most powerful concepts because they allow programs to work directly with memory and are heavily used with arrays, strings, dynamic memory and data structures.

The address-of operator & obtains an address, while * can be used to access the value at an address.""",

            """int x = 10;
int *p = &x;

printf("%d", *p);""",

            "Explain what p and *p represent in the example."
        ),

        lesson(
            "Structures",
            """A structure allows multiple related values of different data types to be grouped into one custom type.

For example, a student record might contain a name, roll number and percentage.

Structures are useful for representing real-world entities in C programs.""",

            """struct Student {
    char name[50];
    int roll;
    float mark;
};

struct Student s1;""",

            "Create a structure representing a book."
        )
    ]
),

# ============================================================
# 9 C++
# ============================================================

course(
    "cpp",
    "C++ Programming",
    "🔷",
    "Intermediate",
    "Move from procedural programming toward object-oriented and modern C++ programming.",
    [

        lesson(
            "C++ Fundamentals",
            """C++ extends the C programming tradition with features such as classes, objects, references, templates and the Standard Library.

It can support procedural, object-oriented and generic programming styles.

Understanding C++ becomes especially useful when learning object-oriented programming and performance-oriented software.""",

            """#include <iostream>
using namespace std;

int main() {
    cout << "Hello C++";
    return 0;
}""",

            "Write a C++ program that prints three lines."
        ),

        lesson(
            "Classes and Objects",
            """A class defines a structure containing data and behavior. An object is an instance created from that class.

This allows software to model real-world or conceptual entities.

For example, a Student class could contain a name and methods for displaying student information.""",

            """class Student {
public:
    string name;

    void show() {
        cout << name;
    }
};""",

            "Create a Book class with title and price."
        ),

        lesson(
            "Inheritance",
            """Inheritance allows one class to derive properties and behavior from another class.

It can be useful when multiple classes share common characteristics.

For example, Vehicle could provide common functionality while Car and Bike extend it with specialized behavior.""",

            """class Vehicle {
public:
    void start() {
        cout << "Starting";
    }
};

class Car : public Vehicle {
};""",

            "Create a simple parent and child class."
        ),

        lesson(
            "STL and Vectors",
            """The C++ Standard Template Library provides reusable containers and algorithms.

vector is a dynamic array that can grow as elements are added.

Using the Standard Library can reduce the amount of low-level code developers need to write themselves.""",

            """#include <vector>

vector<int> numbers = {
    10, 20, 30
};

numbers.push_back(40);""",

            "Create a vector containing five numbers."
        )
    ]
),

# ============================================================
# 10 PYTHON
# ============================================================

course(
    "python",
    "Python Programming",
    "🐍",
    "Beginner → Advanced",
    "Learn Python from fundamentals through practical programming concepts.",
    [

        lesson(
            "Python Fundamentals",
            """Python is a high-level programming language known for readable syntax and a large ecosystem of libraries.

It is widely used in automation, web development, data analysis, artificial intelligence and scripting.

Python's simple syntax makes it useful for beginners while its ecosystem allows developers to build complex systems.""",

            """name = "CodeQuest"

print("Welcome to", name)""",

            "Create a Python program that prints your name and college."
        ),

        lesson(
            "Variables and Types",
            """Python variables refer to objects rather than requiring you to explicitly declare a type in the same way as C.

Common built-in types include int, float, str, bool, list, tuple, set and dict.

Python determines the type associated with a value at runtime.""",

            """age = 18
name = "Joe"
percentage = 87.5
student = True""",

            "Create variables representing a student profile."
        ),

        lesson(
            "Conditions",
            """Conditional statements allow Python programs to choose different paths.

Comparison operators produce Boolean results, which can then be used by if, elif and else.

Decision-making is essential for everything from simple validation to application business logic.""",

            """marks = 85

if marks >= 90:
    print("Excellent")
elif marks >= 50:
    print("Pass")
else:
    print("Needs improvement")""",

            "Create a grade calculator."
        ),

        lesson(
            "Loops",
            """Loops repeat operations.

Python's for loop is commonly used to iterate over sequences, while while repeats code as long as a condition remains true.

Iteration is a core programming concept and appears in almost every practical program.""",

            """for number in range(1, 6):
    print(number)""",

            "Print numbers from 1 to 20 and identify even numbers."
        ),

        lesson(
            "Lists and Dictionaries",
            """Lists store ordered collections of values. Dictionaries store key-value pairs.

These structures are heavily used in practical Python programs because they can represent collections of records and configuration data.

For example, a dictionary can represent one student's profile.""",

            """student = {
    "name": "Arun",
    "age": 18,
    "mark": 91
}

print(student["name"])""",

            "Create a dictionary representing a product."
        ),

        lesson(
            "Functions",
            """Functions allow reusable pieces of logic to be separated from the rest of a program.

Parameters allow a function to receive data, while return sends a result back to the caller.

Good function design improves readability and reduces duplicated code.""",

            """def calculate_total(a, b):
    return a + b

result = calculate_total(10, 20)
print(result)""",

            "Create a function that calculates simple interest."
        ),

        lesson(
            "File Handling",
            """Programs often need to store information outside memory.

Python provides file-handling tools for reading and writing text files.

Using with open(...) is recommended because Python automatically handles closing the file when the block finishes.""",

            """with open("notes.txt", "w") as file:
    file.write("CodeQuest AI")""",

            "Create a text file and store three lines in it."
        ),

        lesson(
            "Object-Oriented Python",
            """Python supports object-oriented programming using classes and objects.

Classes can contain attributes and methods, allowing programs to model entities and their behavior.

Object-oriented design becomes increasingly useful as applications become larger.""",

            """class Student:
    def __init__(self, name):
        self.name = name

    def show(self):
        print(self.name)

s = Student("Arun")
s.show()""",

            "Create a class representing a bank account."
        )
    ]
),

# ============================================================
# 11 JAVA
# ============================================================

course(
    "java",
    "Java Programming",
    "☕",
    "Intermediate",
    "Learn Java fundamentals and object-oriented programming.",
    [

        lesson(
            "Java Fundamentals",
            """Java is a general-purpose programming language widely used for enterprise software, backend systems and many other applications.

Java programs are commonly compiled into bytecode that runs on the Java Virtual Machine.

This architecture contributes to Java's portability across supported platforms.""",

            """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello Java");
    }
}""",

            "Modify the program to print your name."
        ),

        lesson(
            "Classes and Objects",
            """Java is strongly associated with object-oriented programming.

Classes define data and behavior, while objects are instances of those classes.

Encapsulation allows implementation details to be controlled through methods and access modifiers.""",

            """class Student {
    String name;

    void show() {
        System.out.println(name);
    }
}""",

            "Create a Java Book class."
        ),

        lesson(
            "Arrays and Collections",
            """Java arrays have a fixed size, while collection classes such as ArrayList provide more flexible ways to manage groups of objects.

Understanding collections is important because practical applications constantly process groups of data.""",

            """ArrayList<String> names =
    new ArrayList<>();

names.add("Arun");
names.add("Kumar");""",

            "Create an ArrayList containing five student names."
        )
    ]
),

# ============================================================
# 12 HTML CSS
# ============================================================

course(
    "html-css",
    "HTML & CSS",
    "🌐",
    "Beginner → Intermediate",
    "Build the structure and visual appearance of modern web pages.",
    [

        lesson(
            "HTML Structure",
            """HTML describes the structure and meaning of content on a webpage.

Elements such as headings, paragraphs, links, images, forms and sections allow browsers to understand and display content.

HTML is not primarily a programming language. It is a markup language used to structure documents.""",

            """<!DOCTYPE html>
<html>
<head>
    <title>My Page</title>
</head>
<body>
    <h1>CodeQuest AI</h1>
    <p>Learn. Practice. Build.</p>
</body>
</html>""",

            "Create a webpage containing your name and three hobbies."
        ),

        lesson(
            "CSS Basics",
            """CSS controls the visual presentation of HTML.

It can change colors, spacing, typography, borders, layouts and responsive behavior.

Separating structure from presentation makes websites easier to maintain.""",

            """body {
    font-family: Arial;
}

h1 {
    font-size: 32px;
    margin-bottom: 20px;
}""",

            "Style your HTML page with a custom font and spacing."
        ),

        lesson(
            "Flexbox",
            """Flexbox provides a powerful method for arranging elements along one or two dimensions.

It is commonly used for navigation bars, cards, buttons and responsive layouts.

Properties such as justify-content and align-items control how elements are positioned.""",

            """.container {
    display: flex;
    justify-content: center;
    align-items: center;
}""",

            "Create a row of three cards using Flexbox."
        ),

        lesson(
            "Responsive Design",
            """Websites are viewed on many screen sizes. Responsive design allows layouts to adapt to phones, tablets and desktops.

Media queries can apply different CSS rules depending on screen characteristics.

A mobile-friendly interface is particularly important because many users access websites primarily from phones.""",

            """@media (max-width: 600px) {
    .cards {
        flex-direction: column;
    }
}""",

            "Make a three-column layout become one column on small screens."
        )
    ]
),

# ============================================================
# 13 JAVASCRIPT
# ============================================================

course(
    "javascript",
    "JavaScript",
    "⚡",
    "Intermediate",
    "Make websites interactive and learn browser-side programming.",
    [

        lesson(
            "JavaScript Basics",
            """JavaScript is a programming language widely used to add behavior and interactivity to web pages.

Unlike HTML and CSS, JavaScript can make decisions, process data and respond to user actions.

It can run in browsers and also in server-side environments such as Node.js.""",

            """let name = "CodeQuest";

console.log("Hello " + name);""",

            "Create a JavaScript variable containing your name."
        ),

        lesson(
            "DOM Manipulation",
            """The Document Object Model represents a webpage as objects that JavaScript can access and modify.

This allows JavaScript to change text, styles, attributes and page elements in response to user actions.""",

            """document
    .getElementById("title")
    .textContent = "Welcome!";""",

            "Create a button that changes a heading."
        ),

        lesson(
            "Events",
            """Events represent actions such as clicks, keyboard input and mouse movement.

JavaScript event listeners allow programs to respond to those actions.

Interactive web applications are largely built from combinations of events, state and UI updates.""",

            """button.addEventListener(
    "click",
    function() {
        alert("Button clicked!");
    }
);""",

            "Create a button that displays a message when clicked."
        ),

        lesson(
            "Fetch and APIs",
            """Modern websites frequently communicate with backend services using APIs.

The Fetch API allows JavaScript to request data from a server and process the response.

This is how frontend applications can obtain user information, products, quiz questions and many other types of data without manually embedding everything into the page.""",

            """fetch("/api/courses")
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });""",

            "Fetch JSON from a test API and display one value."
        )
    ]
),

# ============================================================
# 14 SQL
# ============================================================

course(
    "sql",
    "DBMS & SQL",
    "🗄️",
    "Intermediate",
    "Learn databases, tables, SQL queries and data relationships.",
    [

        lesson(
            "What is a Database?",
            """A database is an organized system for storing and retrieving information.

Applications use databases for users, products, orders, messages, scores and many other types of data.

A DBMS provides tools for creating, querying and managing databases.""",

            """Application
     ↓
Database API
     ↓
DBMS
     ↓
Tables""",

            "List three applications that require databases."
        ),

        lesson(
            "Tables and Records",
            """A relational database stores information in tables containing rows and columns.

A row usually represents one record, while a column represents an attribute.

For example, a students table could contain student_id, name, department and percentage.""",

            """students

id | name  | mark
1  | Arun  | 87
2  | Ravi  | 91""",

            "Design a table for storing books."
        ),

        lesson(
            "SQL SELECT",
            """SQL allows applications and developers to retrieve information from relational databases.

SELECT is used to retrieve data. WHERE can restrict the rows returned.

Understanding filtering is essential when working with large datasets.""",

            """SELECT name, mark
FROM students
WHERE mark >= 80;""",

            "Write a query that returns students with marks above 90."
        ),

        lesson(
            "INSERT UPDATE DELETE",
            """Databases must support more than reading data.

INSERT creates records, UPDATE modifies records and DELETE removes records.

These operations must be used carefully because an incorrect update or delete condition can affect many records.""",

            """INSERT INTO students
(name, mark)
VALUES ('Arun', 90);

UPDATE students
SET mark = 95
WHERE name = 'Arun';""",

            "Write an INSERT statement for a new product."
        )
    ]
),

# ============================================================
# 15 DSA
# ============================================================

course(
    "dsa",
    "Data Structures & Algorithms",
    "🧩",
    "Intermediate → Advanced",
    "Learn how to organize data and design efficient solutions.",
    [

        lesson(
            "What is an Algorithm?",
            """An algorithm is a finite sequence of steps designed to solve a problem.

A good algorithm should be understandable, correct and appropriate for the problem.

Programming languages implement algorithms, but the underlying problem-solving idea is separate from the language.""",

            """Problem:
Find the largest number.

1. Start with first number.
2. Compare next number.
3. Replace largest when necessary.
4. Continue until finished.""",

            "Write steps for finding the smallest value in a list."
        ),

        lesson(
            "Time Complexity",
            """Time complexity describes how the amount of work performed by an algorithm changes as input size increases.

Big O notation is commonly used to describe an upper-bound growth rate.

For example, scanning every element of an array is generally O(n), while repeatedly dividing the search space in half can lead to O(log n) behavior.""",

            """Linear search:

10 → 20 → 30 → 40 → 50
                  ↑
             search 40

Worst case: O(n)""",

            "Explain why checking every array element is O(n)."
        ),

        lesson(
            "Stacks and Queues",
            """A stack follows Last In, First Out. A queue generally follows First In, First Out.

Stacks appear in function calls, undo systems and expression processing.

Queues are useful for scheduling, task processing and many real-world waiting systems.""",

            """STACK

push 10
push 20
push 30

pop → 30""",

            "Give two real-world examples of stacks and queues."
        ),

        lesson(
            "Searching and Sorting",
            """Searching finds information in a collection, while sorting arranges information according to an ordering rule.

Linear search is simple but may inspect many values. Binary search can be much faster but requires sorted data.

Sorting algorithms differ in complexity and implementation characteristics.""",

            """Sorted:

10 20 30 40 50 60

Binary search
       ↓
      30""",

            "Explain why binary search requires sorted data."
        )
    ]
),

# ============================================================
# 16 OPERATING SYSTEMS
# ============================================================

course(
    "os",
    "Operating Systems",
    "⚙️",
    "Intermediate",
    "Understand processes, memory, files and operating system concepts.",
    [

        lesson(
            "Processes and Programs",
            """A program is a collection of instructions stored on a system. When it is executed, the operating system creates a process representing the running instance.

A process requires resources such as memory and CPU time.

Understanding processes helps explain multitasking and application behavior.""",

            """Program:
chrome.exe

Running instance:
Process

Multiple tabs may involve multiple processes or threads.""",

            "Explain the difference between a program and a process."
        ),

        lesson(
            "Memory Management",
            """Operating systems manage memory so multiple applications can operate without directly interfering with one another.

Modern systems use virtual memory and memory protection mechanisms.

Programmers still need to understand memory because inefficient allocation, leaks and invalid access can cause serious problems.""",

            """Application
↓
Virtual Memory
↓
Physical RAM""",

            "Explain why memory protection is important."
        ),

        lesson(
            "File Systems",
            """A file system determines how data is organized and accessed on storage devices.

Different operating systems can support different file systems.

File permissions, directories and metadata are important concepts for both normal users and developers.""",

            """Drive
├── Users
├── Programs
└── Projects""",

            "Explain why a file system is needed."
        )
    ]
),

# ============================================================
# 17 NETWORKING
# ============================================================

course(
    "networking",
    "Computer Networks",
    "🌐",
    "Intermediate",
    "Understand how computers communicate across local and global networks.",
    [

        lesson(
            "Network Fundamentals",
            """A computer network connects devices so they can exchange information and share resources.

Networks may be small, such as a home network, or extremely large, such as the Internet.

Networking knowledge is important for developers because modern applications communicate with servers and external services.""",

            """Phone
 ↓
Wi-Fi Router
 ↓
Internet
 ↓
Server""",

            "Describe your device's path to an online website."
        ),

        lesson(
            "IP Addresses",
            """An IP address identifies a network interface using an addressing system.

IPv4 commonly uses four decimal numbers separated by dots, while IPv6 provides a much larger address space.

Applications use network addressing to communicate with other devices and services.""",

            """IPv4 example:

192.168.1.10""",

            "Explain what an IP address is used for."
        ),

        lesson(
            "TCP and UDP",
            """TCP provides reliable, ordered communication and includes mechanisms for handling delivery.

UDP is connectionless and has lower protocol overhead, making it useful for applications where speed or timely delivery is important.

The appropriate protocol depends on the application's requirements.""",

            """TCP:
Reliable communication

UDP:
Low-overhead communication""",

            "Give one example where reliable delivery is important."
        ),

        lesson(
            "HTTP and HTTPS",
            """HTTP is a protocol used for communication between clients and web servers.

HTTPS uses TLS to protect HTTP traffic from being read or modified by unauthorized parties during transmission.

Modern web applications depend heavily on HTTP-based APIs.""",

            """Browser
   ↓ HTTPS
Web Server
   ↓
Response""",

            "Explain one difference between HTTP and HTTPS."
        )
    ]
),

# ============================================================
# 18 CYBERSECURITY
# ============================================================

course(
    "cybersecurity",
    "Cybersecurity",
    "🔐",
    "Intermediate",
    "Learn security fundamentals, threats, authentication and defensive practices.",
    [

        lesson(
            "CIA Triad",
            """The CIA triad describes three important security goals: confidentiality, integrity and availability.

Confidentiality means information should only be accessible to authorized parties.

Integrity means information should not be changed improperly.

Availability means authorized users should be able to access systems when needed.""",

            """Confidentiality → Who can see it?
Integrity → Was it changed?
Availability → Can I access it?""",

            "Give a real-world example of each CIA principle."
        ),

        lesson(
            "Passwords and Authentication",
            """Authentication determines whether a person or system is who they claim to be.

Strong authentication practices include long unique passwords and, where available, multi-factor authentication.

Applications should never store user passwords as plain text. Password storage normally uses secure password hashing mechanisms.""",

            """Password
   ↓
Secure hashing
   ↓
Stored representation""",

            "Explain why storing plain-text passwords is dangerous."
        ),

        lesson(
            "Phishing",
            """Phishing attempts to trick people into revealing information or performing an unsafe action.

Messages may imitate trusted organizations and create urgency.

A good defensive habit is to verify the destination, sender and context rather than trusting a message simply because it looks professional.""",

            """Fake message
     ↓
Urgency
     ↓
Fake link
     ↓
Credential theft""",

            "List three warning signs of a phishing message."
        ),

        lesson(
            "Secure Software Basics",
            """Developers are responsible for more than making software functional.

Applications should validate input, protect credentials, use secure communication, enforce authorization and avoid exposing sensitive information in logs or error messages.

Security should be considered during design rather than added only after an application is finished.""",

            """User Input
   ↓
Validation
   ↓
Application
   ↓
Database""",

            "List three security practices a web developer should follow."
        )
    ]
),

# ============================================================
# 19 AI
# ============================================================

course(
    "ai-ml",
    "AI & Machine Learning",
    "🤖",
    "Intermediate → Advanced",
    "Understand artificial intelligence, machine learning, data and model training.",
    [

        lesson(
            "What is Artificial Intelligence?",
            """Artificial intelligence refers broadly to systems designed to perform tasks that traditionally require aspects of human intelligence.

Examples include language processing, image recognition, recommendation systems and decision-support systems.

AI is a broad field containing multiple approaches rather than being one single technology.""",

            """Data
 ↓
AI System
 ↓
Prediction / Generation / Decision""",

            "List three AI systems you interact with in daily life."
        ),

        lesson(
            "Machine Learning",
            """Machine learning is a family of techniques where systems learn patterns from data rather than relying entirely on explicitly written rules.

A model is trained using data and then evaluated on examples.

The quality and representativeness of training data can strongly affect the resulting system.""",

            """Training Data
     ↓
Machine Learning
     ↓
Model
     ↓
Prediction""",

            "Explain the difference between traditional rules and machine learning."
        ),

        lesson(
            "Training and Testing",
            """A dataset is often divided so that a model can be trained on one portion and evaluated on data it did not directly train on.

This helps determine whether the model learned useful patterns rather than simply memorizing its training examples.

Evaluation metrics depend on the specific problem.""",

            """Dataset
  ↓
Training Set
  ↓
Model

Test Set
  ↓
Evaluation""",

            "Explain why testing a model on training data alone can be misleading."
        ),

        lesson(
            "AI Applications",
            """AI is used in many areas including search, recommendation systems, document processing, computer vision, robotics and software development.

When evaluating an AI system, developers should consider accuracy, reliability, security, privacy and the consequences of incorrect outputs.

AI systems are tools that require appropriate data, evaluation and human oversight.""",

            """AI examples:

Chatbots
Recommendation
Image recognition
Fraud detection
Code assistance""",

            "Choose one AI application and explain what data it might need."
        )
    ]
),

# ============================================================
# 20 CLOUD
# ============================================================

course(
    "cloud",
    "Cloud Computing",
    "☁️",
    "Intermediate",
    "Understand cloud services, deployment and scalable infrastructure.",
    [

        lesson(
            "What is Cloud Computing?",
            """Cloud computing provides computing resources through network-accessible services.

Instead of purchasing and maintaining every server yourself, a cloud provider can provide compute, storage, databases and networking resources.

Cloud services can be scaled according to application requirements.""",

            """User
 ↓
Internet
 ↓
Cloud Server
 ↓
Application""",

            "Give three examples of resources a cloud provider can provide."
        ),

        lesson(
            "Virtual Machines",
            """A virtual machine provides an isolated software environment that behaves like a computer.

Virtualization allows multiple virtual machines to run on physical infrastructure.

Developers can use virtual machines for development, testing and production workloads.""",

            """Physical Server
├── VM 1
├── VM 2
└── VM 3""",

            "Explain why virtualization can be useful."
        ),

        lesson(
            "Cloud Storage",
            """Cloud storage allows applications and users to store files on remote infrastructure.

Different storage systems are optimized for different use cases such as objects, blocks or files.

Cloud storage is commonly used for backups, media, documents and application assets.""",

            """Application
    ↓
Cloud Storage
    ↓
Files / Objects""",

            "Give two possible uses of cloud storage."
        )
    ]
),

# ============================================================
# 21 DEVOPS
# ============================================================

course(
    "devops",
    "DevOps & Software Development",
    "🚀",
    "Intermediate → Advanced",
    "Learn how modern software is built, tested, deployed and maintained.",
    [

        lesson(
            "Software Development Lifecycle",
            """Software development normally involves multiple stages such as planning, design, implementation, testing, deployment and maintenance.

The exact workflow differs between teams, but thinking about software as a lifecycle helps developers understand that writing code is only one part of delivering a product.""",

            """Idea
 ↓
Plan
 ↓
Code
 ↓
Test
 ↓
Deploy
 ↓
Maintain""",

            "Describe the lifecycle of a college software project."
        ),

        lesson(
            "Testing",
            """Testing helps developers detect incorrect behavior before software reaches users.

Unit tests focus on small pieces of functionality, while integration tests examine how components work together.

Good testing is not only about finding bugs; it also helps prevent previously fixed problems from returning.""",

            """Function
   ↓
Unit Test
   ↓
Integration Test
   ↓
Application""",

            "Write three test cases for a login form."
        ),

        lesson(
            "CI/CD",
            """Continuous Integration involves frequently integrating changes and automatically checking them.

Continuous Delivery or Deployment extends the process toward releasing software.

Automation can run tests, build applications and deploy changes consistently.""",

            """Git Push
   ↓
CI
   ↓
Tests
   ↓
Build
   ↓
Deploy""",

            "Explain what should happen after a developer pushes code."
        ),

        lesson(
            "Deployment",
            """Deployment means making software available in an environment where users or other systems can access it.

A simple web application might be deployed to a server that runs the backend and serves the frontend.

Production systems also require monitoring, logging, backups and security practices.""",

            """GitHub
   ↓
Build
   ↓
Server
   ↓
Live Application""",

            "Describe the steps required to deploy a small Flask application."
        )
    ]
),

# ============================================================
# 22 CAREER
# ============================================================

course(
    "career",
    "Projects, Resume & Interview Preparation",
    "💼",
    "Career",
    "Turn your technical knowledge into projects, a portfolio, resume and interview preparation.",
    [

        lesson(
            "Building Projects",
            """Projects are one of the most practical ways to demonstrate technical knowledge.

A useful student project should solve a clear problem and show how you applied programming, databases, APIs, user interfaces or other technical skills.

A project does not need to be enormous. A focused, working application with good documentation can demonstrate more than a large unfinished idea.""",

            """Problem
 ↓
Design
 ↓
Development
 ↓
Testing
 ↓
Deployment
 ↓
GitHub""",

            "Write a one-paragraph description of your own software project."
        ),

        lesson(
            "GitHub Portfolio",
            """A GitHub profile can act as a public record of software projects and learning progress.

Repositories should ideally contain meaningful names, README documentation, setup instructions and screenshots or demonstrations when appropriate.

Regularly improving repositories can make your technical growth easier to demonstrate.""",

            """Repository
├── README.md
├── source code
├── screenshots
└── documentation""",

            "Improve the README of one existing project."
        ),

        lesson(
            "Resume Fundamentals",
            """A technical resume should communicate relevant education, skills, projects, achievements and experience clearly.

Project descriptions are stronger when they explain what you built and what technologies you used rather than simply listing project names.

Keep information accurate and avoid claiming technologies or experience you cannot explain in an interview.""",

            """PROJECT

CodeQuest AI
• Built a gamified learning platform
• Flask backend
• Firebase authentication
• Quiz system
• Course management""",

            "Write three bullet points describing one project."
        ),

        lesson(
            "Technical Interviews",
            """Technical interviews can evaluate programming fundamentals, problem solving, data structures, databases, operating systems, networking and project knowledge depending on the role.

Preparation should involve both understanding concepts and solving practical problems.

For project questions, be prepared to explain your architecture, decisions, challenges and how you tested the application.""",

            """Interview preparation:

Concepts
+
Coding
+
Projects
+
Communication""",

            "Explain one project as if an interviewer asked you to describe it."
        )
    ]
)

]


# ============================================================
# QUIZ QUESTION BANK
# ============================================================
#
# IMPORTANT:
# Every question has a unique ID.
# The API randomly selects questions.
# Questions already used in a quiz are never repeated
# within that quiz.
#
# ============================================================

quiz_questions = [

    # ---------------- COMPUTER ----------------

    {
        "id": "cb001",
        "course": "computer-basics",
        "question": "Which component executes program instructions?",
        "options": ["Monitor", "CPU", "Keyboard", "Printer"],
        "answer": "CPU"
    },
    {
        "id": "cb002",
        "course": "computer-basics",
        "question": "Which memory is primarily used as temporary working memory?",
        "options": ["RAM", "SSD", "DVD", "ROM"],
        "answer": "RAM"
    },
    {
        "id": "cb003",
        "course": "computer-basics",
        "question": "Which of these is software?",
        "options": ["Keyboard", "SSD", "Windows", "RAM"],
        "answer": "Windows"
    },
    {
        "id": "cb004",
        "course": "computer-basics",
        "question": "How many bits are normally contained in one byte?",
        "options": ["4", "8", "16", "32"],
        "answer": "8"
    },
    {
        "id": "cb005",
        "course": "computer-basics",
        "question": "Which device is commonly used for permanent file storage?",
        "options": ["RAM", "CPU", "SSD", "Cache"],
        "answer": "SSD"
    },

    # ---------------- WINDOWS ----------------

    {
        "id": "win001",
        "course": "windows",
        "question": "Which shortcut normally opens File Explorer?",
        "options": ["Win + E", "Ctrl + E", "Alt + E", "Win + P"],
        "answer": "Win + E"
    },
    {
        "id": "win002",
        "course": "windows",
        "question": "Which tool shows running processes in Windows?",
        "options": ["Paint", "Task Manager", "Notepad", "Calculator"],
        "answer": "Task Manager"
    },
    {
        "id": "win003",
        "course": "windows",
        "question": "Which command is commonly used to change directories in a terminal?",
        "options": ["cd", "open", "move", "folder"],
        "answer": "cd"
    },

    # ---------------- WORD ----------------

    {
        "id": "word001",
        "course": "ms-word",
        "question": "Which feature helps maintain consistent heading formatting?",
        "options": ["Styles", "Calculator", "Paint", "Task Manager"],
        "answer": "Styles"
    },
    {
        "id": "word002",
        "course": "ms-word",
        "question": "Which Word feature is useful for presenting structured information?",
        "options": ["Table", "Recycle Bin", "Terminal", "Firewall"],
        "answer": "Table"
    },

    # ---------------- EXCEL ----------------

    {
        "id": "excel001",
        "course": "ms-excel",
        "question": "What is the intersection of a row and column called?",
        "options": ["Cell", "Slide", "Page", "Record"],
        "answer": "Cell"
    },
    {
        "id": "excel002",
        "course": "ms-excel",
        "question": "Which function calculates an average?",
        "options": ["SUM", "AVERAGE", "COUNTIF", "MAXIMUM"],
        "answer": "AVERAGE"
    },
    {
        "id": "excel003",
        "course": "ms-excel",
        "question": "Which formula adds values from B2 through B6?",
        "options": ["=SUM(B2:B6)", "=ADD(B2-B6)", "=TOTAL(B2:B6)", "=PLUS(B2:B6)"],
        "answer": "=SUM(B2:B6)"
    },

    # ---------------- INTERNET ----------------

    {
        "id": "net001",
        "course": "internet",
        "question": "What does DNS primarily help translate?",
        "options": ["Domain names to IP addresses", "Images to videos", "RAM to storage", "Passwords to usernames"],
        "answer": "Domain names to IP addresses"
    },
    {
        "id": "net002",
        "course": "internet",
        "question": "Which protocol is commonly used for secure web communication?",
        "options": ["HTTPS", "FTP only", "SMTP", "Bluetooth"],
        "answer": "HTTPS"
    },
    {
        "id": "net003",
        "course": "internet",
        "question": "Which email field can hide recipients from other recipients?",
        "options": ["CC", "BCC", "Subject", "Reply-To"],
        "answer": "BCC"
    },

    # ---------------- GIT ----------------

    {
        "id": "git001",
        "course": "git-github",
        "question": "What is Git primarily used for?",
        "options": ["Version control", "Image editing", "Video streaming", "Hardware repair"],
        "answer": "Version control"
    },
    {
        "id": "git002",
        "course": "git-github",
        "question": "Which command creates a Git commit?",
        "options": ["git commit", "git save", "git checkpoint", "git version"],
        "answer": "git commit"
    },
    {
        "id": "git003",
        "course": "git-github",
        "question": "What is GitHub commonly used for?",
        "options": ["Hosting and collaborating on repositories", "Replacing RAM", "Formatting disks", "Creating BIOS"],
        "answer": "Hosting and collaborating on repositories"
    },
    {
        "id": "git004",
        "course": "git-github",
        "question": "What does a Git branch allow developers to do?",
        "options": [
            "Work on a separate line of development",
            "Increase RAM",
            "Install Windows",
            "Encrypt the CPU"
        ],
        "answer": "Work on a separate line of development"
    },

    # ---------------- C ----------------

    {
        "id": "c001",
        "course": "c",
        "question": "Which function is the usual entry point of a C program?",
        "options": ["start()", "main()", "run()", "begin()"],
        "answer": "main()"
    },
    {
        "id": "c002",
        "course": "c",
        "question": "Which format specifier is commonly used for an int with printf?",
        "options": ["%d", "%f", "%c", "%s"],
        "answer": "%d"
    },
    {
        "id": "c003",
        "course": "c",
        "question": "Which symbol obtains the address of a variable?",
        "options": ["&", "#", "@", "$"],
        "answer": "&"
    },
    {
        "id": "c004",
        "course": "c",
        "question": "Which keyword is commonly used to define a structure?",
        "options": ["struct", "record", "object", "type"],
        "answer": "struct"
    },
    {
        "id": "c005",
        "course": "c",
        "question": "Which loop is convenient when the number of iterations is known?",
        "options": ["for", "switch", "if", "struct"],
        "answer": "for"
    },
    {
        "id": "c006",
        "course": "c",
        "question": "What does scanf commonly require when storing input into an int variable?",
        "options": ["The variable's address", "The variable's color", "A file name", "A class"],
        "answer": "The variable's address"
    },
    {
        "id": "c007",
        "course": "c",
        "question": "Which data type is commonly used for a single character?",
        "options": ["char", "string", "text", "character"],
        "answer": "char"
    },

    # ---------------- C++ ----------------

    {
        "id": "cpp001",
        "course": "cpp",
        "question": "Which stream is commonly used for output in C++?",
        "options": ["cout", "cin", "printfin", "output"],
        "answer": "cout"
    },
    {
        "id": "cpp002",
        "course": "cpp",
        "question": "What is an object?",
        "options": [
            "An instance of a class",
            "A compiler",
            "A loop",
            "A header file"
        ],
        "answer": "An instance of a class"
    },
    {
        "id": "cpp003",
        "course": "cpp",
        "question": "Which STL container behaves like a dynamic array?",
        "options": ["vector", "stackfile", "arraylist", "dynamic"],
        "answer": "vector"
    },

    # ---------------- PYTHON ----------------

    {
        "id": "py001",
        "course": "python",
        "question": "Which function displays output in Python?",
        "options": ["print()", "displayText()", "echo()", "writeScreen()"],
        "answer": "print()"
    },
    {
        "id": "py002",
        "course": "python",
        "question": "Which Python structure stores key-value pairs?",
        "options": ["Dictionary", "Tuple", "String", "Integer"],
        "answer": "Dictionary"
    },
    {
        "id": "py003",
        "course": "python",
        "question": "Which keyword defines a function?",
        "options": ["def", "function", "fun", "define"],
        "answer": "def"
    },
    {
        "id": "py004",
        "course": "python",
        "question": "Which Python structure is an ordered mutable collection?",
        "options": ["List", "Tuple", "Set", "Boolean"],
        "answer": "List"
    },
    {
        "id": "py005",
        "course": "python",
        "question": "Which statement is commonly used to read a text file safely?",
        "options": [
            "with open(...)",
            "read.file()",
            "file.start()",
            "open.readonly()"
        ],
        "answer": "with open(...)"
    },

    # ---------------- JAVA ----------------

    {
        "id": "java001",
        "course": "java",
        "question": "Which method is the usual Java program entry point?",
        "options": ["main()", "start()", "run()", "execute()"],
        "answer": "main()"
    },
    {
        "id": "java002",
        "course": "java",
        "question": "Which keyword creates a Java object?",
        "options": ["new", "create", "object", "make"],
        "answer": "new"
    },
    {
        "id": "java003",
        "course": "java",
        "question": "Which Java collection can dynamically grow?",
        "options": ["ArrayList", "FixedArray", "StaticList", "MemoryList"],
        "answer": "ArrayList"
    },

    # ---------------- HTML ----------------

    {
        "id": "html001",
        "course": "html-css",
        "question": "What does HTML primarily define?",
        "options": ["Webpage structure", "CPU speed", "Database indexes", "Network packets"],
        "answer": "Webpage structure"
    },
    {
        "id": "html002",
        "course": "html-css",
        "question": "Which HTML element represents a main heading?",
        "options": ["<h1>", "<heading>", "<head1>", "<title1>"],
        "answer": "<h1>"
    },
    {
        "id": "html003",
        "course": "html-css",
        "question": "What is CSS primarily used for?",
        "options": ["Presentation and styling", "Database storage", "CPU scheduling", "Compiling C"],
        "answer": "Presentation and styling"
    },

    # ---------------- JAVASCRIPT ----------------

    {
        "id": "js001",
        "course": "javascript",
        "question": "Which keyword can declare a block-scoped JavaScript variable?",
        "options": ["let", "define", "variable", "declare"],
        "answer": "let"
    },
    {
        "id": "js002",
        "course": "javascript",
        "question": "What does the DOM represent?",
        "options": [
            "The webpage as objects",
            "A database server",
            "A programming compiler",
            "A network router"
        ],
        "answer": "The webpage as objects"
    },
    {
        "id": "js003",
        "course": "javascript",
        "question": "Which API can JavaScript use to request data from a server?",
        "options": ["Fetch API", "Storage API only", "CPU API", "Compiler API"],
        "answer": "Fetch API"
    },

    # ---------------- SQL ----------------

    {
        "id": "sql001",
        "course": "sql",
        "question": "Which SQL command retrieves data?",
        "options": ["SELECT", "GET", "READ", "FETCHROW"],
        "answer": "SELECT"
    },
    {
        "id": "sql002",
        "course": "sql",
        "question": "Which SQL clause filters rows?",
        "options": ["WHERE", "FILTER", "ONLY", "LIMITER"],
        "answer": "WHERE"
    },
    {
        "id": "sql003",
        "course": "sql",
        "question": "Which SQL command adds a new record?",
        "options": ["INSERT", "ADDROW", "CREATEVALUE", "PUT"],
        "answer": "INSERT"
    },
    {
        "id": "sql004",
        "course": "sql",
        "question": "What does a database row normally represent?",
        "options": ["A record", "A database server", "A formula", "A password"],
        "answer": "A record"
    },

    # ---------------- DSA ----------------

    {
        "id": "dsa001",
        "course": "dsa",
        "question": "What does an algorithm provide?",
        "options": [
            "Steps for solving a problem",
            "Only source code",
            "A computer monitor",
            "A database password"
        ],
        "answer": "Steps for solving a problem"
    },
    {
        "id": "dsa002",
        "course": "dsa",
        "question": "What is the typical time complexity of scanning every element once?",
        "options": ["O(n)", "O(1)", "O(log n)", "O(n²)"],
        "answer": "O(n)"
    },
    {
        "id": "dsa003",
        "course": "dsa",
        "question": "Which data structure follows Last In, First Out?",
        "options": ["Stack", "Queue", "Graph", "Tree"],
        "answer": "Stack"
    },
    {
        "id": "dsa004",
        "course": "dsa",
        "question": "Which data structure normally follows First In, First Out?",
        "options": ["Queue", "Stack", "Tree", "Heap"],
        "answer": "Queue"
    },

    # ---------------- OS ----------------

    {
        "id": "os001",
        "course": "os",
        "question": "What is a running instance of a program called?",
        "options": ["Process", "Folder", "File type", "Driver letter"],
        "answer": "Process"
    },
    {
        "id": "os002",
        "course": "os",
        "question": "Which resource does an operating system manage?",
        "options": ["Memory", "Only keyboard colors", "Only documents", "Only browsers"],
        "answer": "Memory"
    },
    {
        "id": "os003",
        "course": "os",
        "question": "Why is memory protection important?",
        "options": [
            "It helps prevent processes from improperly accessing memory",
            "It increases screen brightness",
            "It creates Git commits",
            "It formats Word documents"
        ],
        "answer": "It helps prevent processes from improperly accessing memory"
    },

    # ---------------- NETWORKING ----------------

    {
        "id": "network001",
        "course": "networking",
        "question": "What does an IP address identify?",
        "options": ["A network interface/address", "A Word document", "A CPU core", "A programming variable"],
        "answer": "A network interface/address"
    },
    {
        "id": "network002",
        "course": "networking",
        "question": "Which protocol provides reliable ordered transport?",
        "options": ["TCP", "UDP", "HTML", "DNS"],
        "answer": "TCP"
    },
    {
        "id": "network003",
        "course": "networking",
        "question": "What protects HTTP traffic using TLS?",
        "options": ["HTTPS", "HTTP/0", "FTP", "SMTP"],
        "answer": "HTTPS"
    },

    # ---------------- CYBERSECURITY ----------------

    {
        "id": "sec001",
        "course": "cybersecurity",
        "question": "What does the C in the CIA triad represent?",
        "options": ["Confidentiality", "Compilation", "Connection", "Control"],
        "answer": "Confidentiality"
    },
    {
        "id": "sec002",
        "course": "cybersecurity",
        "question": "What is phishing?",
        "options": [
            "A deceptive attempt to obtain information",
            "A sorting algorithm",
            "A database query",
            "A programming language"
        ],
        "answer": "A deceptive attempt to obtain information"
    },
    {
        "id": "sec003",
        "course": "cybersecurity",
        "question": "What should applications avoid storing in plain text?",
        "options": ["Passwords", "Public documentation", "HTML headings", "CSS comments"],
        "answer": "Passwords"
    },

    # ---------------- AI ----------------

    {
        "id": "ai001",
        "course": "ai-ml",
        "question": "What does machine learning primarily learn from?",
        "options": ["Data", "Keyboard shortcuts", "Monitor pixels only", "Power cables"],
        "answer": "Data"
    },
    {
        "id": "ai002",
        "course": "ai-ml",
        "question": "Why is test data useful?",
        "options": [
            "To evaluate performance on data not directly used for training",
            "To increase monitor resolution",
            "To install Python",
            "To create folders"
        ],
        "answer": "To evaluate performance on data not directly used for training"
    },
    {
        "id": "ai003",
        "course": "ai-ml",
        "question": "Which is an example of an AI application?",
        "options": ["Recommendation system", "Keyboard cable", "USB connector", "Power switch"],
        "answer": "Recommendation system"
    },

    # ---------------- CLOUD ----------------

    {
        "id": "cloud001",
        "course": "cloud",
        "question": "What does cloud computing provide?",
        "options": [
            "Network-accessible computing resources",
            "Only local storage",
            "Only keyboard drivers",
            "Only desktop wallpaper"
        ],
        "answer": "Network-accessible computing resources"
    },
    {
        "id": "cloud002",
        "course": "cloud",
        "question": "What is a virtual machine?",
        "options": [
            "A software-based computer environment",
            "A physical keyboard",
            "A Git branch",
            "A database table"
        ],
        "answer": "A software-based computer environment"
    },

    # ---------------- DEVOPS ----------------

    {
        "id": "dev001",
        "course": "devops",
        "question": "What does CI commonly stand for?",
        "options": [
            "Continuous Integration",
            "Computer Installation",
            "Code Internet",
            "Cloud Input"
        ],
        "answer": "Continuous Integration"
    },
    {
        "id": "dev002",
        "course": "devops",
        "question": "Why is automated testing useful?",
        "options": [
            "It helps detect incorrect behavior consistently",
            "It replaces all programmers",
            "It increases RAM",
            "It creates monitors"
        ],
        "answer": "It helps detect incorrect behavior consistently"
    },

    # ---------------- CAREER ----------------

    {
        "id": "career001",
        "course": "career",
        "question": "What makes a project description stronger on a resume?",
        "options": [
            "Explaining what was built and technologies used",
            "Using only the project name",
            "Adding unrelated words",
            "Removing all technical details"
        ],
        "answer": "Explaining what was built and technologies used"
    },
    {
        "id": "career002",
        "course": "career",
        "question": "What is a GitHub repository useful for?",
        "options": [
            "Hosting and demonstrating software projects",
            "Increasing CPU clock speed",
            "Replacing an operating system",
            "Formatting a hard disk"
        ],
        "answer": "Hosting and demonstrating software projects"
    }
]


# ============================================================
# ADD MORE UNIQUE QUESTIONS AUTOMATICALLY
# ============================================================

extra_questions = [

    ("cb006", "computer-basics", "Which device is primarily used to display visual output?", ["Monitor", "Keyboard", "Mouse", "Microphone"], "Monitor"),
    ("cb007", "computer-basics", "Which component performs arithmetic and logical operations?", ["ALU", "Monitor", "SSD", "Keyboard"], "ALU"),
    ("cb008", "computer-basics", "Which device is commonly used to enter text?", ["Keyboard", "Monitor", "Speaker", "Projector"], "Keyboard"),

    ("win004", "windows", "Which shortcut switches between open applications?", ["Alt + Tab", "Ctrl + P", "Win + L", "Ctrl + D"], "Alt + Tab"),
    ("win005", "windows", "Which shortcut commonly opens the Run dialog?", ["Win + R", "Win + E", "Ctrl + R", "Alt + R"], "Win + R"),

    ("word003", "ms-word", "Which feature automatically creates a contents list from headings?", ["Table of Contents", "Task Manager", "Mail Merge", "Clipboard"], "Table of Contents"),
    ("word004", "ms-word", "Which feature can create personalized letters for many recipients?", ["Mail Merge", "WordArt", "Zoom", "Track Changes"], "Mail Merge"),

    ("excel004", "ms-excel", "Which Excel function returns the largest value?", ["MAX", "HIGH", "TOP", "LARGEONLY"], "MAX"),
    ("excel005", "ms-excel", "Which Excel function returns the smallest value?", ["MIN", "LOW", "BOTTOM", "SMALLESTONLY"], "MIN"),

    ("git005", "git-github", "Which command shows the current Git working state?", ["git status", "git check", "git state", "git inspect"], "git status"),
    ("git006", "git-github", "Which command downloads changes from a remote repository and integrates them?", ["git pull", "git take", "git download", "git receive"], "git pull"),

    ("c008", "c", "Which keyword exits a function and optionally returns a value?", ["return", "exitvalue", "back", "stop"], "return"),
    ("c009", "c", "Which symbol terminates most C statements?", [";", ":", ".", ","], ";"),
    ("c010", "c", "Which operator is used to dereference a pointer?", ["*", "&", "#", "@"], "*"),

    ("cpp004", "cpp", "Which C++ keyword defines a class?", ["class", "object", "defineclass", "typeclass"], "class"),
    ("cpp005", "cpp", "Which stream is commonly used for input?", ["cin", "cout", "inputstream", "read"], "cin"),

    ("py006", "python", "Which keyword begins a conditional statement?", ["if", "when", "check", "condition"], "if"),
    ("py007", "python", "Which symbol is used to create a comment on one line?", ["#", "//", "<!--", "--"], "#"),
    ("py008", "python", "Which function returns the number of items in a collection?", ["len()", "count()", "size()", "length()"], "len()"),

    ("java004", "java", "Which keyword is used to inherit from a class?", ["extends", "inherits", "using", "parent"], "extends"),
    ("java005", "java", "Which keyword prevents a variable from being reassigned?", ["final", "fixed", "constant", "lock"], "final"),

    ("html004", "html-css", "Which tag creates a hyperlink?", ["<a>", "<linkto>", "<url>", "<href>"], "<a>"),
    ("html005", "html-css", "Which CSS property changes text color?", ["color", "text-color", "font-color", "foreground"], "color"),

    ("js004", "javascript", "Which keyword declares a constant binding?", ["const", "constant", "fixed", "static"], "const"),
    ("js005", "javascript", "Which method is commonly used to select an element by ID?", ["getElementById()", "findById()", "selectId()", "elementById()"], "getElementById()"),

    ("sql005", "sql", "Which command modifies existing rows?", ["UPDATE", "CHANGE", "MODIFYROW", "ALTERROW"], "UPDATE"),
    ("sql006", "sql", "Which command removes rows?", ["DELETE", "REMOVE", "DROPROW", "CLEAR"], "DELETE"),

    ("dsa005", "dsa", "Which algorithm is commonly used to find an item in a sorted array efficiently?", ["Binary Search", "Linear Sort", "Random Search", "Depth Search"], "Binary Search"),
    ("dsa006", "dsa", "What does O(1) describe?", ["Constant-time growth", "Linear growth", "Quadratic growth", "Exponential growth"], "Constant-time growth"),

    ("os004", "os", "Which operating system component manages hardware resources?", ["Kernel", "Browser", "Text editor", "Compiler only"], "Kernel"),
    ("os005", "os", "What is multitasking?", ["Running multiple tasks/processes through system scheduling", "Installing multiple keyboards", "Using multiple monitors only", "Writing multiple programs"], "Running multiple tasks/processes through system scheduling"),

    ("network004", "networking", "Which device commonly connects devices within a local network?", ["Switch", "Compiler", "Monitor", "SSD"], "Switch"),
    ("network005", "networking", "What does DNS help applications discover?", ["Network addresses associated with domain names", "CPU temperature", "RAM size", "File permissions"], "Network addresses associated with domain names"),

    ("sec004", "cybersecurity", "Which security property ensures information is not improperly changed?", ["Integrity", "Availability", "Confidentiality", "Compression"], "Integrity"),
    ("sec005", "cybersecurity", "Which practice adds another verification factor beyond a password?", ["Multi-factor authentication", "Compression", "Caching", "Indexing"], "Multi-factor authentication"),

    ("ai004", "ai-ml", "What is a model in machine learning?", ["A learned computational representation used to make predictions or decisions", "A computer monitor", "A database password", "A network cable"], "A learned computational representation used to make predictions or decisions"),
    ("ai005", "ai-ml", "What is training data?", ["Data used to learn patterns for a model", "Data deleted after training", "Only test results", "A programming language"], "Data used to learn patterns for a model"),

    ("cloud003", "cloud", "Which cloud resource can provide computing capacity?", ["Virtual machine", "Word document", "Keyboard", "HTML heading"], "Virtual machine"),
    ("cloud004", "cloud", "Why might organizations use cloud services?", ["To obtain scalable computing resources", "To remove all software", "To eliminate networking", "To avoid data entirely"], "To obtain scalable computing resources"),

    ("dev003", "devops", "What does deployment mean?", ["Making software available in a target environment", "Deleting source code", "Creating a keyboard", "Formatting a document"], "Making software available in a target environment"),
    ("dev004", "devops", "Why are logs useful?", ["They provide information about application/system activity", "They increase RAM", "They compile C automatically", "They replace databases"], "They provide information about application/system activity"),

    ("career003", "career", "What should a technical project README usually contain?", ["Project description and setup/use information", "Only emojis", "A random password", "No information"], "Project description and setup/use information"),
    ("career004", "career", "Why should students be able to explain their projects in interviews?", ["Interviewers may ask about design and implementation decisions", "Projects never matter", "It replaces programming knowledge", "It is required by Git"], "Interviewers may ask about design and implementation decisions")
]

for qid, cid, question, options, answer in extra_questions:
    quiz_questions.append({
        "id": qid,
        "course": cid,
        "question": question,
        "options": options,
        "answer": answer
    })


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def home():
    return jsonify({
        "app": "CodeQuest AI",
        "version": "2.0",
        "message": "Learn • Practice • Play • Build",
        "status": "online"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "courses": len(courses),
        "quiz_questions": len(quiz_questions)
    })


# ============================================================
# COURSES
# ============================================================

@app.route("/api/courses")
def get_courses():
    return jsonify({
        "courses": courses
    })


@app.route("/api/course/<course_id>")
def get_course(course_id):

    for c in courses:
        if c["id"] == course_id:
            return jsonify(c)

    return jsonify({
        "error": "Course not found"
    }), 404


# ============================================================
# QUIZ ARENA
# ============================================================

@app.route("/api/quiz")
def get_quiz():

    course_id = request.args.get("course", "").strip()

    count = request.args.get("count", "10")

    try:
        count = int(count)
    except:
        count = 10

    count = max(1, min(count, 20))

    if course_id:
        pool = [
            q for q in quiz_questions
            if q["course"] == course_id
        ]
    else:
        pool = quiz_questions.copy()

    # Randomly select unique questions.
    selected = random.sample(
        pool,
        min(count, len(pool))
    )

    result = []

    for q in selected:

        # Copy question so original bank isn't modified.
        item = {
            "id": q["id"],
            "course": q["course"],
            "question": q["question"],
            "options": q["options"][:],
            "answer": q["answer"]
        }

        # Randomize answer options.
        random.shuffle(item["options"])

        result.append(item)

    return jsonify({
        "questions": result,
        "total": len(result)
    })


# ============================================================
# CAREER GUIDE
# ============================================================

careers = [

    {
        "id": "software-developer",
        "title": "Software Developer",
        "icon": "💻",
        "description": "Build applications, services and software systems.",
        "skills": [
            "Programming",
            "Data Structures",
            "Git",
            "Databases",
            "APIs",
            "Problem Solving"
        ],
        "roadmap": [
            "Programming fundamentals",
            "Data Structures",
            "Git & GitHub",
            "Databases",
            "Web/API development",
            "Projects",
            "Interview preparation"
        ]
    },

    {
        "id": "web-developer",
        "title": "Web Developer",
        "icon": "🌐",
        "description": "Build websites and web applications.",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "Git",
            "APIs",
            "Backend development"
        ],
        "roadmap": [
            "HTML & CSS",
            "JavaScript",
            "Git & GitHub",
            "Frontend framework",
            "Backend",
            "Database",
            "Deployment"
        ]
    },

    {
        "id": "python-developer",
        "title": "Python Developer",
        "icon": "🐍",
        "description": "Build applications and automation using Python.",
        "skills": [
            "Python",
            "OOP",
            "APIs",
            "Databases",
            "Git",
            "Testing"
        ],
        "roadmap": [
            "Python fundamentals",
            "OOP",
            "Data structures",
            "APIs",
            "Databases",
            "Projects",
            "Deployment"
        ]
    },

    {
        "id": "cybersecurity",
        "title": "Cybersecurity",
        "icon": "🔐",
        "description": "Understand and help protect systems, applications and networks.",
        "skills": [
            "Networking",
            "Linux",
            "Security fundamentals",
            "Authentication",
            "Web security",
            "Incident awareness"
        ],
        "roadmap": [
            "Computer basics",
            "Networking",
            "Operating systems",
            "Security fundamentals",
            "Web security",
            "Security labs",
            "Certifications/projects"
        ]
    },

    {
        "id": "data-ai",
        "title": "AI / Data",
        "icon": "🤖",
        "description": "Work with data, machine learning and AI systems.",
        "skills": [
            "Python",
            "Statistics",
            "Data analysis",
            "Machine learning",
            "SQL",
            "Model evaluation"
        ],
        "roadmap": [
            "Python",
            "Statistics",
            "SQL",
            "Data analysis",
            "Machine learning",
            "Projects",
            "Model deployment"
        ]
    }

]


@app.route("/api/careers")
def get_careers():
    return jsonify({
        "careers": careers
    })


# ============================================================
# FIREBASE LOGIN BACKEND
# ============================================================

firebase_admin_initialized = False
firebase_auth = None

try:

    import firebase_admin
    from firebase_admin import credentials, auth

    service_account_json = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_JSON"
    )

    if service_account_json:

        service_account_info = json.loads(
            service_account_json
        )

        credential = credentials.Certificate(
            service_account_info
        )

        firebase_admin.initialize_app(credential)

        firebase_admin_initialized = True
        firebase_auth = auth

except Exception as e:

    print("Firebase Admin initialization warning:", e)


@app.route("/api/firebase-login", methods=["POST"])
def firebase_login():

    data = request.get_json(silent=True) or {}

    id_token = data.get("idToken")

    if not id_token:
        return jsonify({
            "success": False,
            "error": "Firebase ID token missing"
        }), 400

    if not firebase_admin_initialized:

        return jsonify({
            "success": False,
            "error": "Firebase Admin is not configured on the server"
        }), 503

    try:

        decoded = firebase_auth.verify_id_token(id_token)

        uid = decoded.get("uid")
        email = decoded.get("email", "")
        name = decoded.get("name", "")
        photo = decoded.get("picture", "")

        conn = get_db()

        conn.execute("""
            INSERT INTO users
            (uid, email, name, photo, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(uid)
            DO UPDATE SET
                email=excluded.email,
                name=excluded.name,
                photo=excluded.photo
        """, (
            uid,
            email,
            name,
            photo,
            datetime.utcnow().isoformat()
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "uid": uid,
            "email": email,
            "name": name,
            "photo": photo
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 401


# ============================================================
# PROGRESS
# ============================================================

@app.route("/api/progress", methods=["POST"])
def save_progress():

    data = request.get_json(silent=True) or {}

    uid = data.get("uid")
    course_id = data.get("course_id")
    chapter_index = data.get("chapter_index")

    if not uid or not course_id:
        return jsonify({
            "success": False,
            "error": "Missing progress information"
        }), 400

    try:
        chapter_index = int(chapter_index)
    except:
        chapter_index = 0

    conn = get_db()

    conn.execute("""
        INSERT INTO progress
        (uid, course_id, chapter_index, completed)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(uid, course_id, chapter_index)
        DO UPDATE SET completed=1
    """, (
        uid,
        course_id,
        chapter_index
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True
    })


@app.route("/api/progress/<uid>")
def get_progress(uid):

    conn = get_db()

    rows = conn.execute("""
        SELECT course_id, chapter_index, completed
        FROM progress
        WHERE uid = ?
    """, (uid,)).fetchall()

    conn.close()

    return jsonify({
        "progress": [
            dict(row)
            for row in rows
        ]
    })


# ============================================================
# QUIZ RESULT
# ============================================================

@app.route("/api/quiz-result", methods=["POST"])
def save_quiz_result():

    data = request.get_json(silent=True) or {}

    uid = data.get("uid", "guest")
    score = int(data.get("score", 0))
    total = int(data.get("total", 0))

    conn = get_db()

    conn.execute("""
        INSERT INTO quiz_attempts
        (uid, score, total, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        uid,
        score,
        total,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "score": score,
        "total": total
    })


# ============================================================
# C COMPILER
# ============================================================

@app.route("/api/compile", methods=["POST"])
def compile_c():

    data = request.get_json(silent=True) or {}

    code = data.get("code", "")
    stdin = data.get("stdin", "")

    if not code.strip():

        return jsonify({
            "success": False,
            "output": "",
            "error": "Please enter C code.",
            "compile_output": ""
        }), 400

    # Limit request size.
    if len(code) > 30000:

        return jsonify({
            "success": False,
            "output": "",
            "error": "Code is too large.",
            "compile_output": ""
        }), 400

    if len(stdin) > 10000:

        return jsonify({
            "success": False,
            "output": "",
            "error": "Input is too large.",
            "compile_output": ""
        }), 400

    payload = {
        "compiler": "gcc-head-c",
        "code": code,
        "stdin": stdin,
        "save": False,
        "compiler_option_raw": "",
        "runtime_option_raw": ""
    }

    try:

        response = requests.post(
            WANDBOX_URL,
            json=payload,
            timeout=25
        )

        if response.status_code != 200:

            return jsonify({
                "success": False,
                "output": "",
                "error": "Compiler service returned an error.",
                "compile_output": ""
            }), 502

        result = response.json()

        compiler_message = (
            result.get("compiler_message") or ""
        )

        program_message = (
            result.get("program_message") or ""
        )

        status = result.get("status")

        signal = result.get("signal")

        success = (
            str(status) == "0"
            and not compiler_message
        )

        if success:

            return jsonify({
                "success": True,
                "output": program_message,
                "error": "",
                "compile_output": "",
                "signal": signal
            })

        error_text = program_message

        if not error_text:
            error_text = compiler_message

        if not error_text:
            error_text = "Program failed to execute."

        return jsonify({
            "success": False,
            "output": program_message,
            "error": error_text,
            "compile_output": compiler_message,
            "signal": signal
        })

    except requests.Timeout:

        return jsonify({
            "success": False,
            "output": "",
            "error": "Compiler request timed out.",
            "compile_output": ""
        }), 504

    except Exception as e:

        return jsonify({
            "success": False,
            "output": "",
            "error": "Compiler connection failed: " + str(e),
            "compile_output": ""
        }), 500


# ============================================================
# ACHIEVEMENTS
# ============================================================

@app.route("/api/achievements")
def achievements():

    return jsonify({
        "achievements": [
            {
                "id": "first-step",
                "title": "First Step",
                "description": "Complete your first lesson.",
                "icon": "🚀"
            },
            {
                "id": "quiz-starter",
                "title": "Quiz Starter",
                "description": "Complete your first quiz.",
                "icon": "🧠"
            },
            {
                "id": "code-runner",
                "title": "Code Runner",
                "description": "Successfully execute your first C program.",
                "icon": "💻"
            },
            {
                "id": "github-builder",
                "title": "GitHub Builder",
                "description": "Create your first GitHub project.",
                "icon": "🐙"
            },
            {
                "id": "quest-master",
                "title": "Quest Master",
                "description": "Make major progress across multiple courses.",
                "icon": "🏆"
            }
        ]
    })


# ============================================================
# ERROR HANDLER
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Route not found"
    }), 404


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "error": "Internal server error"
    }), 500


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    port = int(
        os.getenv("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
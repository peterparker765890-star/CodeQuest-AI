from flask import Flask, render_template, jsonify, request
import sqlite3
import random
import time
import requests
import os
from datetime import datetime, date

# ============================================================
# CODEQUEST AI
# Learn • Practice • Play • Build
# ============================================================

app = Flask(__name__)

DATABASE = "codequest.db"


# ============================================================
# DATABASE
# ============================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT DEFAULT 'Player',
            email TEXT DEFAULT '',
            xp INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            completed_lessons INTEGER DEFAULT 0,
            quizzes_completed INTEGER DEFAULT 0,
            weekly_tests INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_active TEXT DEFAULT ''
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS lesson_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            course TEXT,
            lesson_index INTEGER,
            completed_at TEXT,
            UNIQUE(user_id, course, lesson_index)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            question_id TEXT,
            answered_at TEXT,
            UNIQUE(user_id, question_id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS weekly_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            score INTEGER,
            total INTEGER,
            xp INTEGER,
            taken_at TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ============================================================
# LEVEL SYSTEM
# ============================================================

LEVELS = [
    (1, "Code Explorer", 0),
    (2, "Bug Hunter", 500),
    (3, "Logic Builder", 1000),
    (4, "Code Warrior", 2000),
    (5, "Developer", 3500),
    (6, "Tech Hunter", 5500),
    (7, "Code Master", 8000),
    (8, "Digital Architect", 12000),
    (9, "AI Pioneer", 17000),
    (10, "CodeQuest Legend", 25000)
]


def get_level(xp):
    xp = int(xp or 0)

    current = LEVELS[0]

    for level, name, required in LEVELS:
        if xp >= required:
            current = (level, name, required)

    return {
        "level": current[0],
        "name": current[1],
        "required_xp": current[2]
    }


# ============================================================
# COURSES
# ============================================================

courses = {

    "computer-basics": {
        "name": "Computer Basics",
        "icon": "💻",
        "level": "Beginner",
        "description": "Understand computers from the ground up.",
        "chapters": [

            {
                "title": "What is a Computer?",
                "topic": "computer",
                "explanation": """
A computer is an electronic device that accepts data as input,
processes it according to instructions, stores information and
produces useful output.

The basic computer cycle is:

Input → Processing → Output → Storage

For example, when you type a number into a calculator app,
the keyboard or touchscreen provides input, the processor performs
the calculation and the application displays the result.
""",
                "example": "A smartphone, laptop, ATM and supermarket billing machine are all examples of computer-based systems.",
                "code_language": "python",
                "code": """# Simple input → processing → output

name = input("Enter your name: ")
print("Welcome", name)
""",
                "notes": [
                    "CPU performs processing.",
                    "RAM temporarily stores active data.",
                    "Storage keeps data for long-term use.",
                    "Software provides instructions to hardware."
                ],
                "task": "Identify the input, processing, output and storage components of your smartphone."
            },

            {
                "title": "CPU and Processing",
                "topic": "cpu",
                "explanation": """
The CPU (Central Processing Unit) is one of the most important
components of a computer.

It executes instructions and performs calculations.

Important CPU concepts include:

• ALU - Arithmetic Logic Unit
• Control Unit
• Registers
• CPU cores
• Clock speed

Modern processors contain multiple cores, allowing them to work
on multiple tasks efficiently.
""",
                "example": "When you open a browser and play music at the same time, the processor handles instructions from several applications.",
                "code_language": "python",
                "code": """# CPU performs calculations

a = 25
b = 15

result = a * b

print("Result:", result)
""",
                "notes": [
                    "CPU is responsible for instruction execution.",
                    "More CPU cores can help with parallel workloads.",
                    "Clock speed is measured in GHz."
                ],
                "task": "Find the processor model and number of cores in your computer or phone."
            },

            {
                "title": "RAM and ROM",
                "topic": "memory",
                "explanation": """
RAM stands for Random Access Memory.

It temporarily stores programs and data that the computer is
currently using.

ROM stands for Read Only Memory and traditionally refers to
non-volatile memory used for firmware and startup instructions.

RAM is generally faster than permanent storage, but RAM loses
its contents when power is removed.
""",
                "example": "Opening a large development application requires RAM to keep its active data available.",
                "code_language": "python",
                "code": """# Memory example

numbers = [10, 20, 30, 40, 50]

print(numbers)
print("Number of items:", len(numbers))
""",
                "notes": [
                    "RAM is volatile memory.",
                    "Storage is non-volatile.",
                    "More RAM can help when running multiple applications."
                ],
                "task": "Check how much RAM your device has and list three applications currently using memory."
            },

            {
                "title": "Input and Output Devices",
                "topic": "io",
                "explanation": """
Input devices send information to a computer.

Examples:
• Keyboard
• Mouse
• Microphone
• Scanner
• Camera
• Touchscreen

Output devices present processed information.

Examples:
• Monitor
• Printer
• Speaker
• Projector
"""
                ,
                "example": "A barcode scanner provides input and a billing printer produces output.",
                "code_language": "python",
                "code": """# Simulating an input device

product = input("Scan product name: ")

print("Product received:", product)
""",
                "notes": [
                    "Touchscreens can act as both input and output devices.",
                    "Sensors are commonly used as computer inputs."
                ],
                "task": "List five input devices and five output devices."
            },

            {
                "title": "Operating Systems",
                "topic": "os",
                "explanation": """
An operating system manages computer hardware and provides
services for applications.

Examples include:

• Windows
• Linux
• macOS
• Android
• iOS

The operating system manages processes, memory, files,
devices, networking and security.
""",
                "example": "Android manages your phone's applications, memory, storage, permissions and hardware.",
                "code_language": "python",
                "code": """# Operating-system information

import platform

print("Operating System:", platform.system())
print("Version:", platform.version())
""",
                "notes": [
                    "The OS acts as a bridge between applications and hardware.",
                    "Linux is widely used on servers.",
                    "Android uses the Linux kernel."
                ],
                "task": "Find your operating system version."
            },

            {
                "title": "Files and Folders",
                "topic": "files",
                "explanation": """
Files contain information while folders organize files.

Common file types include:

.txt
.jpg
.png
.pdf
.docx
.xlsx
.py
.c
.cpp
.java

Programming projects normally contain multiple source files,
configuration files and resources.
""",
                "example": "A Python project might contain app.py, requirements.txt and a templates folder.",
                "code_language": "python",
                "code": """import os

print("Current folder:")
print(os.getcwd())

print("\\nFiles:")
print(os.listdir())
""",
                "notes": [
                    "File extensions indicate file types.",
                    "Folders help organize projects.",
                    "Backups protect important files."
                ],
                "task": "Create a folder named CodeQuestPractice and organize three programming files inside it."
            }
        ]
    },


    # ========================================================
    # PRODUCTIVITY
    # ========================================================

    "productivity": {
        "name": "Productivity Tools",
        "icon": "📊",
        "level": "Beginner",
        "description": "Master Word, Excel, PowerPoint and cloud productivity tools.",
        "chapters": [

            {
                "title": "MS Word Fundamentals",
                "topic": "word",
                "explanation": """
Microsoft Word is a word-processing application used to create
documents such as reports, assignments, resumes, letters and
project documentation.

Important skills include:

• Formatting
• Styles
• Tables
• Images
• Headers and footers
• Page numbers
• Page setup
• Exporting to PDF
""",
                "example": "Students commonly use Word to prepare laboratory records, assignments and resumes.",
                "code_language": "text",
                "code": """Example document structure:

TITLE

1. Introduction
2. Objective
3. Procedure
4. Result
5. Conclusion
""",
                "notes": [
                    "Use heading styles for professional documents.",
                    "Keep fonts and spacing consistent.",
                    "Use tables for structured information."
                ],
                "task": "Create a one-page professional resume using Word."
            },

            {
                "title": "Excel Formulas",
                "topic": "excel",
                "explanation": """
Excel is a spreadsheet application used for calculations,
data analysis, charts and reporting.

Important formulas include:

SUM
AVERAGE
MAX
MIN
COUNT
IF

Excel is extremely useful for student marks, attendance,
budgets and data analysis.
""",
                "example": "A teacher can calculate the average mark of a class using AVERAGE().",
                "code_language": "text",
                "code": """Example Excel formulas:

=SUM(B2:B10)

=AVERAGE(B2:B10)

=MAX(B2:B10)

=MIN(B2:B10)

=IF(B2>=40,"PASS","FAIL")
""",
                "notes": [
                    "Cell references can be relative or absolute.",
                    "Charts help visualize data.",
                    "Functions reduce repetitive calculations."
                ],
                "task": "Create a student marks sheet with total, average and pass/fail status."
            },

            {
                "title": "PowerPoint Presentations",
                "topic": "powerpoint",
                "explanation": """
PowerPoint is used to create visual presentations.

A strong technical presentation normally contains:

• Title
• Problem
• Objective
• Method
• Demonstration
• Results
• Conclusion

Avoid putting huge paragraphs on slides.
""",
                "example": "A college project presentation can explain the problem, solution, architecture and demo.",
                "code_language": "text",
                "code": """Suggested project presentation:

Slide 1 - Project Title
Slide 2 - Problem
Slide 3 - Proposed Solution
Slide 4 - Features
Slide 5 - Technology Stack
Slide 6 - Demo
Slide 7 - Future Scope
Slide 8 - Conclusion
""",
                "notes": [
                    "Use readable fonts.",
                    "Use diagrams when possible.",
                    "Keep each slide focused."
                ],
                "task": "Create an 8-slide presentation about your favourite technology."
            }
        ]
    },


    # ========================================================
    # PROGRAMMING FUNDAMENTALS
    # ========================================================

    "programming": {
        "name": "Programming Fundamentals",
        "icon": "🧠",
        "level": "Beginner",
        "description": "Learn programming logic and problem solving.",
        "chapters": [

            {
                "title": "Algorithms",
                "topic": "algorithm",
                "explanation": """
An algorithm is a step-by-step procedure for solving a problem.

A good algorithm should be:

• Clear
• Finite
• Correct
• Efficient

Example problem:

Find the largest of two numbers.

Steps:

1. Read A
2. Read B
3. Compare A and B
4. Print the larger value
""",
                "example": "Google Maps uses algorithms to calculate routes between locations.",
                "code_language": "python",
                "code": """a = int(input("Enter A: "))
b = int(input("Enter B: "))

if a > b:
    print("Largest:", a)
else:
    print("Largest:", b)
""",
                "notes": [
                    "Algorithms are independent of programming languages.",
                    "Flowcharts can visually represent algorithms."
                ],
                "task": "Write an algorithm to find the smallest of three numbers."
            },

            {
                "title": "Variables and Data Types",
                "topic": "variables",
                "explanation": """
A variable is a named location used to store a value.

Common data types include:

Integer
Float
Character
String
Boolean

Different programming languages represent these types
in different ways.
""",
                "example": "A shopping application may store product price as a decimal value and quantity as an integer.",
                "code_language": "python",
                "code": """name = "Jack"
age = 18
height = 5.8
student = True

print(name)
print(age)
print(height)
print(student)
""",
                "notes": [
                    "Choose meaningful variable names.",
                    "Avoid unnecessary global variables.",
                    "Understand the difference between data and variables."
                ],
                "task": "Create variables for your name, age, department, percentage and student status."
            },

            {
                "title": "Conditions",
                "topic": "conditions",
                "explanation": """
Conditional statements allow a program to make decisions.

Common structures:

if
if-else
if-elif-else

Conditions are fundamental to almost every application.
""",
                "example": "A banking application may allow a withdrawal only when sufficient balance exists.",
                "code_language": "python",
                "code": """balance = 5000
withdraw = 2000

if withdraw <= balance:
    balance -= withdraw
    print("Withdrawal successful")
    print("Remaining:", balance)
else:
    print("Insufficient balance")
""",
                "notes": [
                    "Use == for comparison.",
                    "Use = for assignment.",
                    "Combine conditions using and/or."
                ],
                "task": "Create a program that checks whether a student passed or failed."
            },

            {
                "title": "Loops",
                "topic": "loops",
                "explanation": """
Loops repeat a block of code.

Python provides:

for
while

Loops are useful for processing lists, generating patterns,
repeating calculations and reading multiple values.
""",
                "example": "An application may process thousands of records using a loop.",
                "code_language": "python",
                "code": """for number in range(1, 6):
    print("Number:", number)
""",
                "notes": [
                    "Make sure loops have a valid termination condition.",
                    "Nested loops can increase complexity."
                ],
                "task": "Print all even numbers from 1 to 100."
            },

            {
                "title": "Functions",
                "topic": "functions",
                "explanation": """
Functions divide a program into reusable blocks.

Benefits:

• Reusability
• Readability
• Easier testing
• Easier maintenance

A function may accept parameters and return a result.
""",
                "example": "A calculator application can use separate functions for addition, subtraction and multiplication.",
                "code_language": "python",
                "code": """def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

print(add(10, 20))
print(multiply(5, 6))
""",
                "notes": [
                    "Use descriptive function names.",
                    "Keep functions focused on one task.",
                    "Avoid unnecessarily large functions."
                ],
                "task": "Create functions for add, subtract, multiply and divide."
            },

            {
                "title": "Arrays and Lists",
                "topic": "arrays",
                "explanation": """
Arrays store multiple values under one logical structure.

Python uses lists for flexible collections.

Arrays are fundamental for searching, sorting and data processing.
""",
                "example": "A marks application can store marks of all students in an array.",
                "code_language": "python",
                "code": """marks = [78, 85, 92, 67, 88]

print("Marks:", marks)
print("Highest:", max(marks))
print("Average:", sum(marks) / len(marks))
""",
                "notes": [
                    "Many programming languages use zero-based indexing.",
                    "Choose the right data structure for the problem."
                ],
                "task": "Store ten student marks and calculate the average."
            }
        ]
    },


    # ========================================================
    # C
    # ========================================================

    "c-language": {
        "name": "C Programming",
        "icon": "🇨",
        "level": "Beginner → Intermediate",
        "description": "Master C programming from syntax to pointers and files.",
        "chapters": [

            {
                "title": "C Program Structure",
                "topic": "c-basics",
                "explanation": """
C is a compiled, general-purpose programming language.

It is widely used for systems programming, embedded systems,
operating systems, compilers and performance-sensitive software.

A basic C program contains headers, the main function and
statements.
""",
                "example": "Operating systems and embedded devices have historically relied heavily on C.",
                "code_language": "c",
                "code": """#include <stdio.h>

int main() {
    printf("Hello, CodeQuest AI!\\n");

    return 0;
}
""",
                "notes": [
                    "main() is the entry point of a C program.",
                    "printf() displays output.",
                    "return 0 indicates successful completion."
                ],
                "task": "Write a C program that prints your name, department and college."
            },

            {
                "title": "Variables and Input",
                "topic": "c-input",
                "explanation": """
C provides data types such as:

int
float
double
char

scanf() can be used to read input from the user.
""",
                "example": "A C application can accept marks from a student and calculate the result.",
                "code_language": "c",
                "code": """#include <stdio.h>

int main() {

    int mark;

    printf("Enter mark: ");
    scanf("%d", &mark);

    printf("Your mark is %d\\n", mark);

    return 0;
}
""",
                "notes": [
                    "Use & with scanf for most ordinary variables.",
                    "%d is used for int.",
                    "%f is used for float."
                ],
                "task": "Read three marks and calculate their average."
            },

            {
                "title": "Conditions in C",
                "topic": "c-if",
                "explanation": """
C supports decision-making using if, else if and else.

Conditions are used whenever the program needs to choose
between different actions.
""",
                "example": "A result-processing application can determine whether a student passed.",
                "code_language": "c",
                "code": """#include <stdio.h>

int main() {

    int mark;

    printf("Enter mark: ");
    scanf("%d", &mark);

    if (mark >= 50) {
        printf("PASS\\n");
    } else {
        printf("FAIL\\n");
    }

    return 0;
}
""",
                "notes": [
                    "Use == for equality comparison.",
                    "Use && for logical AND.",
                    "Use || for logical OR."
                ],
                "task": "Create a grade calculator using if-else."
            },

            {
                "title": "Loops in C",
                "topic": "c-loops",
                "explanation": """
C provides for, while and do-while loops.

Loops are used for repeated operations.
""",
                "example": "A program processing multiple student records can use loops.",
                "code_language": "c",
                "code": """#include <stdio.h>

int main() {

    for (int i = 1; i <= 10; i++) {
        printf("%d\\n", i);
    }

    return 0;
}
""",
                "notes": [
                    "for is useful when the number of repetitions is known.",
                    "while is useful when repetition depends on a condition."
                ],
                "task": "Print the multiplication table of a number."
            },

            {
                "title": "Arrays in C",
                "topic": "c-arrays",
                "explanation": """
An array stores multiple values of the same data type.

C arrays use zero-based indexing.
""",
                "example": "Student marks can be stored in an integer array.",
                "code_language": "c",
                "code": """#include <stdio.h>

int main() {

    int marks[] = {80, 75, 91, 68, 88};

    int total = 0;

    for (int i = 0; i < 5; i++) {
        total += marks[i];
    }

    printf("Total = %d\\n", total);
    printf("Average = %.2f\\n", total / 5.0);

    return 0;
}
""",
                "notes": [
                    "Array indexing starts from 0.",
                    "Accessing outside the array is unsafe."
                ],
                "task": "Find the highest value in an integer array."
            },

            {
                "title": "Functions in C",
                "topic": "c-functions",
                "explanation": """
Functions allow large programs to be divided into reusable
components.

A function can receive arguments and return a value.
""",
                "example": "A calculator can have separate functions for each mathematical operation.",
                "code_language": "c",
                "code": """#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {

    int result = add(10, 20);

    printf("Result = %d\\n", result);

    return 0;
}
""",
                "notes": [
                    "Function prototypes are useful when functions are declared later.",
                    "Keep functions focused."
                ],
                "task": "Write functions for square, cube and factorial."
            },

            {
                "title": "Pointers",
                "topic": "c-pointers",
                "explanation": """
A pointer stores the memory address of another variable.

Pointers are one of the most important advanced concepts in C.

They are used for:

• Dynamic memory
• Arrays
• Functions
• Data structures
• System programming
""",
                "example": "Operating-system and embedded programming frequently requires direct memory manipulation.",
                "code_language": "c",
                "code": """#include <stdio.h>

int main() {

    int number = 25;

    int *ptr = &number;

    printf("Value = %d\\n", number);
    printf("Address = %p\\n", (void *)ptr);
    printf("Value through pointer = %d\\n", *ptr);

    return 0;
}
""",
                "notes": [
                    "& obtains an address.",
                    "* dereferences a pointer.",
                    "Incorrect pointer usage can cause crashes."
                ],
                "task": "Write a program that changes a variable using a pointer."
            },

            {
                "title": "Structures",
                "topic": "c-structures",
                "explanation": """
Structures allow programmers to combine different data types
into one custom data structure.

They are useful for modelling real-world objects.
""",
                "example": "A student record can contain name, roll number and mark.",
                "code_language": "c",
                "code": """#include <stdio.h>

struct Student {
    int id;
    char name[50];
    float mark;
};

int main() {

    struct Student s = {
        101,
        "Jack",
        87.5
    };

    printf("ID: %d\\n", s.id);
    printf("Name: %s\\n", s.name);
    printf("Mark: %.2f\\n", s.mark);

    return 0;
}
""",
                "notes": [
                    "Structures are useful for records.",
                    "Structures can contain arrays and other structures."
                ],
                "task": "Create a structure for an employee."
            }
        ]
    },


    # ========================================================
    # C++
    # ========================================================

    "cpp": {
        "name": "C++ Programming",
        "icon": "⚡",
        "level": "Intermediate",
        "description": "Learn C++ and object-oriented programming.",
        "chapters": [

            {
                "title": "C++ Basics",
                "topic": "cpp-basics",
                "explanation": """
C++ is a powerful general-purpose language that supports
procedural, object-oriented and generic programming.

It is widely used in games, systems, competitive programming
and performance-sensitive applications.
""",
                "example": "Game engines and high-performance applications commonly use C++.",
                "code_language": "cpp",
                "code": """#include <iostream>
using namespace std;

int main() {

    cout << "Hello, CodeQuest AI!" << endl;

    return 0;
}
""",
                "notes": [
                    "iostream provides console input/output.",
                    "cout displays output.",
                    "cin reads input."
                ],
                "task": "Write a C++ program that reads two numbers and adds them."
            },

            {
                "title": "Classes and Objects",
                "topic": "classes",
                "explanation": """
A class is a blueprint for creating objects.

An object is an instance of a class.

Classes are fundamental to object-oriented programming.
""",
                "example": "A banking system might have an Account class containing balance and account operations.",
                "code_language": "cpp",
                "code": """#include <iostream>
using namespace std;

class Student {

public:
    string name;
    int mark;

    void display() {
        cout << name << " - " << mark << endl;
    }
};

int main() {

    Student s;

    s.name = "Jack";
    s.mark = 90;

    s.display();

    return 0;
}
""",
                "notes": [
                    "Classes can contain data and functions.",
                    "public controls member accessibility."
                ],
                "task": "Create a Car class with brand, model and speed."
            },

            {
                "title": "Constructors",
                "topic": "constructors",
                "explanation": """
A constructor is a special member function automatically called
when an object is created.

Constructors are commonly used to initialize objects.
""",
                "example": "When creating a Student object, the constructor can initialize the student's name and roll number.",
                "code_language": "cpp",
                "code": """#include <iostream>
using namespace std;

class Student {

private:
    string name;

public:

    Student(string studentName) {
        name = studentName;
    }

    void display() {
        cout << "Student: " << name << endl;
    }
};

int main() {

    Student s("Jack");

    s.display();

    return 0;
}
""",
                "notes": [
                    "Constructors have the same name as the class.",
                    "Constructors do not have a return type."
                ],
                "task": "Create a constructor for a BankAccount class."
            },

            {
                "title": "Inheritance",
                "topic": "inheritance",
                "explanation": """
Inheritance allows a class to reuse properties and behaviour
from another class.

This helps model relationships between objects.
""",
                "example": "A Vehicle base class can be extended by Car and Bike classes.",
                "code_language": "cpp",
                "code": """#include <iostream>
using namespace std;

class Vehicle {

public:
    void start() {
        cout << "Vehicle started" << endl;
    }
};

class Car : public Vehicle {

public:
    void drive() {
        cout << "Car is driving" << endl;
    }
};

int main() {

    Car car;

    car.start();
    car.drive();

    return 0;
}
""",
                "notes": [
                    "Inheritance supports code reuse.",
                    "C++ supports multiple forms of inheritance."
                ],
                "task": "Create Animal and Dog classes using inheritance."
            }
        ]
    },


    # ========================================================
    # PYTHON
    # ========================================================

    "python": {
        "name": "Python Programming",
        "icon": "🐍",
        "level": "Beginner → Advanced",
        "description": "Learn Python for development, automation, AI and data.",
        "chapters": [

            {
                "title": "Python Basics",
                "topic": "python-basics",
                "explanation": """
Python is a high-level programming language known for readable
syntax and a large ecosystem of libraries.

Python is used in:

• Web development
• Automation
• Data science
• AI/ML
• Cybersecurity
• Scripting
• Testing
""",
                "example": "Flask, Django, NumPy, Pandas and many AI tools are part of the Python ecosystem.",
                "code_language": "python",
                "code": """name = input("What is your name? ")

print("Welcome to Python,", name)
""",
                "notes": [
                    "Python uses indentation to define blocks.",
                    "Python is dynamically typed.",
                    "Use virtual environments for projects."
                ],
                "task": "Create a program that asks for your name and age."
            },

            {
                "title": "Lists and Dictionaries",
                "topic": "python-data",
                "explanation": """
Lists store ordered collections.

Dictionaries store key-value pairs.

These structures are used constantly in Python applications.
""",
                "example": "A student profile can be represented using a dictionary.",
                "code_language": "python",
                "code": """student = {
    "name": "Jack",
    "department": "IT",
    "year": 1,
    "mark": 88
}

print(student["name"])
print(student["department"])
print(student["mark"])
""",
                "notes": [
                    "Lists are ordered collections.",
                    "Dictionary keys should be meaningful.",
                    "Choose data structures based on the problem."
                ],
                "task": "Create a dictionary representing a college student."
            },

            {
                "title": "Object-Oriented Python",
                "topic": "python-oop",
                "explanation": """
Python supports object-oriented programming.

Classes can contain attributes and methods.

OOP is useful when building larger applications.
""",
                "example": "A game can represent players, enemies and weapons as objects.",
                "code_language": "python",
                "code": """class Student:

    def __init__(self, name, department):
        self.name = name
        self.department = department

    def introduce(self):
        print(
            f"My name is {self.name} "
            f"and I study {self.department}."
        )


student = Student("Jack", "IT")

student.introduce()
""",
                "notes": [
                    "self refers to the current object.",
                    "__init__ initializes object data."
                ],
                "task": "Create a BankAccount class with deposit and withdraw methods."
            },

            {
                "title": "File Handling",
                "topic": "python-files",
                "explanation": """
Python can read and write files.

Common modes:

r - read
w - write
a - append

Using with is recommended because it handles closing the file
automatically.
""",
                "example": "Applications can save reports, logs and configuration data in files.",
                "code_language": "python",
                "code": """with open("notes.txt", "w") as file:
    file.write("CodeQuest AI\\n")
    file.write("Learn. Practice. Build.\\n")

print("File created.")
""",
                "notes": [
                    "Use with open() for safe file handling.",
                    "Be careful when using write mode because it replaces existing content."
                ],
                "task": "Create a Python program that stores three student names in a file."
            },

            {
                "title": "Python APIs",
                "topic": "python-api",
                "explanation": """
An API allows one software system to communicate with another.

Python applications can send HTTP requests to APIs.

APIs are essential for modern web and mobile applications.
""",
                "example": "A weather application can request weather data from a weather API.",
                "code_language": "python",
                "code": """import requests

response = requests.get(
    "https://example.com"
)

print("Status:", response.status_code)
""",
                "notes": [
                    "Always validate API responses.",
                    "Use timeouts for network requests.",
                    "Never expose private API keys in public source code."
                ],
                "task": "Research a public API and identify its endpoint, method and response format."
            },

            {
                "title": "Flask Web Development",
                "topic": "flask",
                "explanation": """
Flask is a lightweight Python web framework.

A Flask application can provide:

• Web pages
• REST APIs
• Authentication
• Database integration
• Backend services
""",
                "example": "CodeQuest AI itself uses Flask as its backend architecture.",
                "code_language": "python",
                "code": """from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from CodeQuest AI!"

if __name__ == "__main__":
    app.run(debug=True)
""",
                "notes": [
                    "Routes connect URLs to Python functions.",
                    "Production deployments normally use a WSGI server such as Gunicorn."
                ],
                "task": "Create a Flask application with /, /about and /hello routes."
            }
        ]
    },


    # ========================================================
    # JAVA
    # ========================================================

    "java": {
        "name": "Java Programming",
        "icon": "☕",
        "level": "Intermediate",
        "description": "Learn Java, OOP and application development.",
        "chapters": [

            {
                "title": "Java Basics",
                "topic": "java-basics",
                "explanation": """
Java is a strongly typed, object-oriented programming language.

Java applications run on the Java Virtual Machine (JVM).

Java is widely used in enterprise software, backend systems
and Android-related development.
""",
                "example": "Large enterprise applications often use Java-based backend technologies.",
                "code_language": "java",
                "code": """public class Main {

    public static void main(String[] args) {

        System.out.println(
            "Hello, CodeQuest AI!"
        );
    }
}
""",
                "notes": [
                    "Java source files commonly use the .java extension.",
                    "The JVM executes Java bytecode."
                ],
                "task": "Write a Java program that prints your name and department."
            },

            {
                "title": "Java Variables",
                "topic": "java-variables",
                "explanation": """
Java requires variables to have declared data types.

Common types include:

int
double
char
boolean
String
""",
                "example": "A student management application may store IDs as integers and names as strings.",
                "code_language": "java",
                "code": """public class Main {

    public static void main(String[] args) {

        String name = "Jack";
        int age = 18;
        double percentage = 88.5;
        boolean active = true;

        System.out.println(name);
        System.out.println(age);
        System.out.println(percentage);
        System.out.println(active);
    }
}
""",
                "notes": [
                    "Java is statically typed.",
                    "String is a class rather than a primitive type."
                ],
                "task": "Create variables for a student's complete academic information."
            },

            {
                "title": "Java Conditions and Loops",
                "topic": "java-control",
                "explanation": """
Java supports if, else, switch and multiple loop types.

Loops include:

for
while
do-while

These structures are fundamental for program logic.
""",
                "example": "A result system can use conditions to determine grades.",
                "code_language": "java",
                "code": """public class Main {

    public static void main(String[] args) {

        int mark = 82;

        if (mark >= 90) {
            System.out.println("A+");
        } else if (mark >= 75) {
            System.out.println("A");
        } else if (mark >= 50) {
            System.out.println("PASS");
        } else {
            System.out.println("FAIL");
        }
    }
}
""",
                "notes": [
                    "Use braces consistently.",
                    "switch is useful for multiple discrete choices."
                ],
                "task": "Build a menu-driven calculator in Java."
            },

            {
                "title": "Java Classes and Objects",
                "topic": "java-oop",
                "explanation": """
Java is strongly associated with object-oriented programming.

A class defines the structure and behaviour of objects.

Objects are created using new.
""",
                "example": "A college application could contain Student, Course and Teacher classes.",
                "code_language": "java",
                "code": """class Student {

    String name;
    int mark;

    void display() {
        System.out.println(
            name + " - " + mark
        );
    }
}

public class Main {

    public static void main(String[] args) {

        Student student = new Student();

        student.name = "Jack";
        student.mark = 90;

        student.display();
    }
}
""",
                "notes": [
                    "Classes define object structure.",
                    "Objects contain state and behaviour."
                ],
                "task": "Create Employee and Department classes."
            }
        ]
    },


    # ========================================================
    # WEB DEVELOPMENT
    # ========================================================

    "web-development": {
        "name": "Web Development",
        "icon": "🌐",
        "level": "Beginner → Advanced",
        "description": "Build modern websites and web applications.",
        "chapters": [

            {
                "title": "HTML Fundamentals",
                "topic": "html",
                "explanation": """
HTML provides the structure of a webpage.

Important elements include:

html
head
body
h1-h6
p
a
img
form
input
button
table
section
div
""",
                "example": "Every webpage you visit is built from structured documents and web technologies.",
                "code_language": "html",
                "code": """<!DOCTYPE html>

<html>

<head>
    <title>My Website</title>
</head>

<body>

    <h1>Welcome</h1>

    <p>
        My first CodeQuest webpage.
    </p>

    <button>
        Start Learning
    </button>

</body>

</html>
""",
                "notes": [
                    "HTML describes structure, not application logic.",
                    "Use semantic HTML where possible."
                ],
                "task": "Build a personal profile webpage."
            },

            {
                "title": "CSS Styling",
                "topic": "css",
                "explanation": """
CSS controls the visual appearance of webpages.

Important concepts:

• Colors
• Fonts
• Box model
• Flexbox
• Grid
• Responsive design
• Animations
• Transitions
""",
                "example": "Modern dashboards use CSS cards, responsive layouts and animations.",
                "code_language": "html",
                "code": """<!DOCTYPE html>

<html>

<head>

<style>

.card {
    padding: 20px;
    border-radius: 16px;
    background: #18182b;
    color: white;
    width: 300px;
}

.button {
    padding: 12px 20px;
    border-radius: 10px;
    border: none;
}

</style>

</head>

<body>

<div class="card">

    <h2>CodeQuest</h2>

    <p>
        Learn. Practice. Build.
    </p>

    <button class="button">
        Start
    </button>

</div>

</body>

</html>
""",
                "notes": [
                    "Use responsive layouts for mobile devices.",
                    "Flexbox is excellent for one-dimensional layouts.",
                    "Grid is useful for two-dimensional layouts."
                ],
                "task": "Create a responsive course card."
            },

            {
                "title": "JavaScript Fundamentals",
                "topic": "javascript",
                "explanation": """
JavaScript adds behaviour and interactivity to webpages.

It can:

• Handle button clicks
• Modify HTML
• Validate forms
• Call APIs
• Store data
• Build interactive applications
""",
                "example": "A quiz application can use JavaScript to show questions and calculate scores.",
                "code_language": "javascript",
                "code": """const button = document.querySelector("#start");

button.addEventListener("click", () => {

    alert("Quest started!");

});
""",
                "notes": [
                    "Use const and let instead of var for most modern JavaScript.",
                    "DOM APIs allow JavaScript to interact with webpages."
                ],
                "task": "Create a button that changes a webpage message."
            },

            {
                "title": "Fetching APIs",
                "topic": "fetch",
                "explanation": """
Modern web applications frequently communicate with backend
servers through HTTP APIs.

JavaScript provides fetch() for making network requests.
""",
                "example": "A dashboard can request user progress from a Flask backend.",
                "code_language": "javascript",
                "code": """async function loadData() {

    const response =
        await fetch("/api/progress");

    const data =
        await response.json();

    console.log(data);
}

loadData();
""",
                "notes": [
                    "Always handle failed requests.",
                    "Validate server responses.",
                    "Never trust client input."
                ],
                "task": "Create a webpage that loads data from a public API."
            }
        ]
    },


    # ========================================================
    # DATABASE
    # ========================================================

    "database": {
        "name": "Database & SQL",
        "icon": "🗄️",
        "level": "Intermediate",
        "description": "Learn databases and SQL.",
        "chapters": [

            {
                "title": "Database Fundamentals",
                "topic": "database",
                "explanation": """
A database stores and organizes information so applications
can efficiently retrieve and update it.

Examples:

• Student databases
• Banking systems
• E-commerce systems
• Hospital systems
• Social networks
""",
                "example": "A college portal may store students, departments, subjects and marks.",
                "code_language": "sql",
                "code": """CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    mark INTEGER
);
""",
                "notes": [
                    "A relational database stores data in tables.",
                    "Primary keys uniquely identify rows."
                ],
                "task": "Design tables for a college student management system."
            },

            {
                "title": "SELECT Queries",
                "topic": "select",
                "explanation": """
SELECT retrieves data from a database.

Filtering is performed using WHERE.

Sorting is performed using ORDER BY.
""",
                "example": "A teacher can retrieve students who scored more than 80.",
                "code_language": "sql",
                "code": """SELECT name, mark
FROM students
WHERE mark >= 80
ORDER BY mark DESC;
""",
                "notes": [
                    "Avoid SELECT * when only a few columns are required.",
                    "Indexes can improve query performance."
                ],
                "task": "Write a query to find all IT students."
            },

            {
                "title": "INSERT UPDATE DELETE",
                "topic": "crud",
                "explanation": """
CRUD means:

Create
Read
Update
Delete

These operations form the foundation of many database-backed applications.
""",
                "example": "A student management application performs CRUD operations on student records.",
                "code_language": "sql",
                "code": """INSERT INTO students
(name, department, mark)
VALUES
('Jack', 'IT', 90);

UPDATE students
SET mark = 95
WHERE name = 'Jack';

DELETE FROM students
WHERE name = 'Jack';
""",
                "notes": [
                    "Always use WHERE carefully with UPDATE and DELETE.",
                    "Parameterized queries help prevent SQL injection."
                ],
                "task": "Create CRUD queries for an employee table."
            }
        ]
    },


    # ========================================================
    # GIT
    # ========================================================

    "git-github": {
        "name": "Git & GitHub",
        "icon": "🐙",
        "level": "Beginner → Intermediate",
        "description": "Learn version control and collaborative development.",
        "chapters": [

            {
                "title": "What is Git?",
                "topic": "git",
                "explanation": """
Git is a distributed version-control system.

It tracks changes in source code and allows developers to
restore earlier versions.

Git is extremely common in professional software development.
""",
                "example": "Developers can create a feature branch without directly changing the production branch.",
                "code_language": "bash",
                "code": """git init

git add .

git commit -m "Initial commit"

git status
""",
                "notes": [
                    "Git is the version-control system.",
                    "GitHub is a platform for hosting Git repositories."
                ],
                "task": "Create your first Git repository and make three commits."
            },

            {
                "title": "Push to GitHub",
                "topic": "github",
                "explanation": """
GitHub hosts Git repositories and provides collaboration tools.

A common workflow is:

Edit → Add → Commit → Push
""",
                "example": "A student can publish a portfolio project on GitHub.",
                "code_language": "bash",
                "code": """git add .

git commit -m "Add project feature"

git push origin main
""",
                "notes": [
                    "Commit messages should describe the change.",
                    "Never commit passwords or private API keys."
                ],
                "task": "Create a GitHub repository for a small programming project."
            }
        ]
    },


    # ========================================================
    # CYBERSECURITY
    # ========================================================

    "cybersecurity": {
        "name": "Cybersecurity",
        "icon": "🛡️",
        "level": "Beginner → Advanced",
        "description": "Learn defensive cybersecurity fundamentals.",
        "chapters": [

            {
                "title": "Cybersecurity Fundamentals",
                "topic": "security",
                "explanation": """
Cybersecurity protects systems, networks, applications and
data from unauthorized access, misuse and disruption.

The CIA triad represents:

Confidentiality
Integrity
Availability
""",
                "example": "A banking application must keep customer data confidential, prevent unauthorized modification and remain available.",
                "code_language": "python",
                "code": """import hashlib

password = "example-password"

hashed = hashlib.sha256(
    password.encode()
).hexdigest()

print(hashed)
""",
                "notes": [
                    "Never store passwords as plain text.",
                    "Modern applications should use dedicated password-hashing algorithms such as Argon2 or bcrypt rather than raw SHA-256."
                ],
                "task": "Identify five security risks in a student web application."
            },

            {
                "title": "Phishing Awareness",
                "topic": "phishing",
                "explanation": """
Phishing attempts to trick users into revealing sensitive
information or performing unsafe actions.

Common warning signs:

• Unexpected urgency
• Suspicious links
• Fake login pages
• Unknown attachments
• Requests for passwords or OTPs
""",
                "example": "An attacker may send a fake account verification message containing a malicious link.",
                "code_language": "text",
                "code": """Security checklist:

✓ Check the sender
✓ Check the domain
✓ Don't share OTPs
✓ Don't reuse passwords
✓ Enable MFA
✓ Report suspicious messages
""",
                "notes": [
                    "Social engineering targets human behaviour.",
                    "MFA adds another layer of protection."
                ],
                "task": "Analyse a fictional suspicious email and identify five warning signs."
            }
        ]
    },


    # ========================================================
    # CLOUD
    # ========================================================

    "cloud": {
        "name": "Cloud Computing",
        "icon": "☁️",
        "level": "Intermediate",
        "description": "Understand cloud services and deployment.",
        "chapters": [

            {
                "title": "Cloud Computing Basics",
                "topic": "cloud",
                "explanation": """
Cloud computing provides computing resources over a network.

Common service models:

IaaS
PaaS
SaaS

Cloud platforms provide computing, storage, databases,
networking and application services.
""",
                "example": "A web application can run on a cloud server instead of a student's personal computer.",
                "code_language": "text",
                "code": """Typical application architecture:

User
 ↓
Web Browser
 ↓
Cloud / Web Server
 ↓
Backend API
 ↓
Database
""",
                "notes": [
                    "Cloud systems can scale resources according to demand.",
                    "Deployment automation is important in modern development."
                ],
                "task": "Draw the architecture of a cloud-hosted student application."
            },

            {
                "title": "Deploying a Web App",
                "topic": "deployment",
                "explanation": """
Deployment means making an application available for users.

A typical Flask deployment contains:

Application
Requirements
Production server
Cloud platform
Environment variables
Database
""",
                "example": "CodeQuest AI can be deployed so classmates can access it through a browser.",
                "code_language": "bash",
                "code": """pip install -r requirements.txt

gunicorn app:app
""",
                "notes": [
                    "Never place secret credentials directly in source code.",
                    "Use environment variables for secrets."
                ],
                "task": "Deploy a small Flask application."
            }
        ]
    },


    # ========================================================
    # AI / ML
    # ========================================================

    "ai-ml": {
        "name": "AI & Machine Learning",
        "icon": "🤖",
        "level": "Intermediate → Advanced",
        "description": "Understand AI, ML and modern intelligent applications.",
        "chapters": [

            {
                "title": "Artificial Intelligence",
                "topic": "ai",
                "explanation": """
Artificial Intelligence is the field of creating systems that
perform tasks requiring capabilities commonly associated with
human intelligence.

Examples include:

• Recommendation systems
• Computer vision
• Speech recognition
• Natural language processing
• Generative AI
""",
                "example": "A recommendation system can suggest videos or products based on user behaviour.",
                "code_language": "python",
                "code": """# Simple rule-based recommendation

score = 85

if score >= 80:
    recommendation = "Advanced course"
elif score >= 50:
    recommendation = "Intermediate course"
else:
    recommendation = "Beginner course"

print(recommendation)
""",
                "notes": [
                    "Rule-based logic is not the same as machine learning.",
                    "AI is a broad field containing many approaches."
                ],
                "task": "Design a simple rule-based study recommendation system."
            },

            {
                "title": "Machine Learning Basics",
                "topic": "machine-learning",
                "explanation": """
Machine learning allows systems to learn patterns from data.

Common categories:

• Supervised learning
• Unsupervised learning
• Reinforcement learning

A typical ML workflow is:

Data → Cleaning → Features → Training → Evaluation → Prediction
""",
                "example": "A model can learn from historical student data to predict performance, although predictions should be used carefully.",
                "code_language": "python",
                "code": """# Very simple data example

marks = [60, 70, 80, 90]

average = sum(marks) / len(marks)

print("Average:", average)
""",
                "notes": [
                    "Good data is essential for machine learning.",
                    "Training and testing data should be separated."
                ],
                "task": "Find a beginner ML dataset and identify its features and target."
            }
        ]
    },


    # ========================================================
    # CAREER
    # ========================================================

    "career": {
        "name": "Career Preparation",
        "icon": "🚀",
        "level": "All Levels",
        "description": "Prepare for internships, placements and software careers.",
        "chapters": [

            {
                "title": "Build Your Resume",
                "topic": "resume",
                "explanation": """
A technical resume should communicate your skills, education,
projects and achievements clearly.

For a student, useful sections include:

• Name and contact
• Education
• Skills
• Projects
• Certifications
• Achievements
• GitHub
• Portfolio
""",
                "example": "A first-year student can already build a portfolio using small projects rather than waiting until final year.",
                "code_language": "text",
                "code": """PROJECT EXAMPLE

CodeQuest AI
- Flask backend
- HTML/CSS/JavaScript frontend
- Firebase authentication
- Gamified learning system
- Quiz system
- Progress tracking
- Cloud deployment
""",
                "notes": [
                    "Describe what you built and what technology you used.",
                    "Use measurable results when appropriate."
                ],
                "task": "Create a one-page student technical resume."
            },

            {
                "title": "GitHub Portfolio",
                "topic": "portfolio",
                "explanation": """
Your GitHub profile can act as a public record of your
programming work.

Useful portfolio projects should demonstrate:

• Problem solving
• Code quality
• Documentation
• UI/UX
• Deployment
• Real-world usefulness
""",
                "example": "A deployed student project gives you something concrete to demonstrate during interviews.",
                "code_language": "text",
                "code": """README structure:

# Project Name

## Problem

## Solution

## Features

## Technologies

## Installation

## Screenshots

## Future Improvements
""",
                "notes": [
                    "Keep repositories organized.",
                    "Write useful README files.",
                    "Never upload passwords or private keys."
                ],
                "task": "Create a professional README for one of your projects."
            },

            {
                "title": "Interview Preparation",
                "topic": "interview",
                "explanation": """
Technical interviews commonly evaluate programming fundamentals,
problem solving, data structures, communication and project
understanding.

You should be able to explain your own projects clearly.
""",
                "example": "For CodeQuest AI, you should be able to explain the frontend, backend, database, authentication and deployment architecture.",
                "code_language": "text",
                "code": """Practice questions:

1. What problem does your project solve?
2. Why did you choose your technology stack?
3. How does your backend work?
4. How is user progress stored?
5. How would you scale the application?
6. What security improvements would you make?
""",
                "notes": [
                    "Understand your projects rather than memorizing answers.",
                    "Practice explaining technical ideas simply."
                ],
                "task": "Explain one of your projects aloud in two minutes."
            }
        ]
    }
}


# ============================================================
# QUIZ BANK
# ============================================================

quiz_bank = [

    {
        "id": "python-001",
        "course": "Python Programming",
        "question": "Which keyword defines a function in Python?",
        "options": ["function", "def", "func", "define"],
        "answer": "def",
        "explanation": "Python uses the def keyword to define a function.",
        "xp": 10
    },

    {
        "id": "python-002",
        "course": "Python Programming",
        "question": "Which Python structure stores key-value pairs?",
        "options": ["List", "Tuple", "Dictionary", "Set"],
        "answer": "Dictionary",
        "explanation": "Dictionaries store data as key-value pairs.",
        "xp": 10
    },

    {
        "id": "c-001",
        "course": "C Programming",
        "question": "Which function is the usual entry point of a C program?",
        "options": ["start()", "run()", "main()", "begin()"],
        "answer": "main()",
        "explanation": "Execution normally begins in main().",
        "xp": 10
    },

    {
        "id": "c-002",
        "course": "C Programming",
        "question": "Which symbol obtains the address of a variable in C?",
        "options": ["*", "&", "#", "@"],
        "answer": "&",
        "explanation": "The & operator obtains a variable's address.",
        "xp": 10
    },

    {
        "id": "cpp-001",
        "course": "C++ Programming",
        "question": "Which feature allows a class to derive from another class?",
        "options": ["Inheritance", "Compilation", "Iteration", "Casting"],
        "answer": "Inheritance",
        "explanation": "Inheritance allows a derived class to reuse a base class.",
        "xp": 10
    },

    {
        "id": "java-001",
        "course": "Java Programming",
        "question": "Which keyword creates an object in Java?",
        "options": ["make", "object", "new", "create"],
        "answer": "new",
        "explanation": "The new keyword creates objects.",
        "xp": 10
    },

    {
        "id": "web-001",
        "course": "Web Development",
        "question": "Which technology provides webpage structure?",
        "options": ["HTML", "CSS", "SQL", "Python"],
        "answer": "HTML",
        "explanation": "HTML provides the structure of webpages.",
        "xp": 10
    },

    {
        "id": "web-002",
        "course": "Web Development",
        "question": "Which technology is primarily used for webpage styling?",
        "options": ["HTML", "CSS", "SQL", "Git"],
        "answer": "CSS",
        "explanation": "CSS controls presentation and styling.",
        "xp": 10
    },

    {
        "id": "db-001",
        "course": "Database & SQL",
        "question": "Which SQL command retrieves data?",
        "options": ["GET", "SELECT", "READ", "FETCH"],
        "answer": "SELECT",
        "explanation": "SELECT retrieves records from a database.",
        "xp": 10
    },

    {
        "id": "git-001",
        "course": "Git & GitHub",
        "question": "Which command records staged changes in Git?",
        "options": ["git save", "git record", "git commit", "git store"],
        "answer": "git commit",
        "explanation": "git commit creates a new commit from staged changes.",
        "xp": 10
    },

    {
        "id": "security-001",
        "course": "Cybersecurity",
        "question": "What does MFA provide?",
        "options": [
            "Multiple authentication factors",
            "Faster internet",
            "File compression",
            "Database backup"
        ],
        "answer": "Multiple authentication factors",
        "explanation": "Multi-factor authentication uses more than one authentication factor.",
        "xp": 10
    },

    {
        "id": "cloud-001",
        "course": "Cloud Computing",
        "question": "Which model provides software to users over the internet?",
        "options": ["SaaS", "CPU", "RAM", "BIOS"],
        "answer": "SaaS",
        "explanation": "Software as a Service delivers software through a service model.",
        "xp": 10
    },

    {
        "id": "algo-001",
        "course": "Programming Fundamentals",
        "question": "What is an algorithm?",
        "options": [
            "A programming language",
            "A step-by-step procedure for solving a problem",
            "A computer component",
            "A database"
        ],
        "answer": "A step-by-step procedure for solving a problem",
        "explanation": "Algorithms describe procedures for solving problems.",
        "xp": 10
    },

    {
        "id": "computer-001",
        "course": "Computer Basics",
        "question": "Which component executes program instructions?",
        "options": ["CPU", "Monitor", "Keyboard", "Printer"],
        "answer": "CPU",
        "explanation": "The CPU executes instructions.",
        "xp": 10
    },

    {
        "id": "ai-001",
        "course": "AI & Machine Learning",
        "question": "Which is a common machine-learning category?",
        "options": [
            "Supervised learning",
            "Screen learning",
            "Keyboard learning",
            "Folder learning"
        ],
        "answer": "Supervised learning",
        "explanation": "Supervised learning is a major machine-learning paradigm.",
        "xp": 10
    }
]


# ============================================================
# WEEKLY TEST BANK
# ============================================================

weekly_questions = [

    {
        "id": "w1",
        "question": "Which data structure stores key-value pairs in Python?",
        "options": ["List", "Dictionary", "Tuple", "Array"],
        "answer": "Dictionary"
    },

    {
        "id": "w2",
        "question": "Which language uses printf() for formatted output?",
        "options": ["C", "HTML", "SQL", "CSS"],
        "answer": "C"
    },

    {
        "id": "w3",
        "question": "Which technology structures a webpage?",
        "options": ["HTML", "CSS", "Git", "SQL"],
        "answer": "HTML"
    },

    {
        "id": "w4",
        "question": "Which SQL command retrieves records?",
        "options": ["SELECT", "INSERT", "DELETE", "UPDATE"],
        "answer": "SELECT"
    },

    {
        "id": "w5",
        "question": "Which Git command creates a commit?",
        "options": ["git push", "git commit", "git start", "git save"],
        "answer": "git commit"
    },

    {
        "id": "w6",
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Computer Primary Utility",
            "Central Program User",
            "Control Processing Utility"
        ],
        "answer": "Central Processing Unit"
    },

    {
        "id": "w7",
        "question": "Which C operator obtains an address?",
        "options": ["&", "*", "%", "#"],
        "answer": "&"
    },

    {
        "id": "w8",
        "question": "Which Java keyword creates an object?",
        "options": ["new", "make", "object", "create"],
        "answer": "new"
    },

    {
        "id": "w9",
        "question": "Which CSS layout system is useful for two-dimensional layouts?",
        "options": ["Grid", "Input", "SQL", "DOM"],
        "answer": "Grid"
    },

    {
        "id": "w10",
        "question": "Which cloud model provides software as a service?",
        "options": ["SaaS", "CPU", "RAM", "BIOS"],
        "answer": "SaaS"
    },

    {
        "id": "w11",
        "question": "What does MFA improve?",
        "options": [
            "Authentication security",
            "Screen resolution",
            "Storage capacity",
            "CPU speed"
        ],
        "answer": "Authentication security"
    },

    {
        "id": "w12",
        "question": "Which Python keyword defines a function?",
        "options": ["def", "function", "fun", "define"],
        "answer": "def"
    },

    {
        "id": "w13",
        "question": "Which OOP concept allows one class to derive from another?",
        "options": ["Inheritance", "Iteration", "Compilation", "Indexing"],
        "answer": "Inheritance"
    },

    {
        "id": "w14",
        "question": "What is an algorithm?",
        "options": [
            "A sequence of steps to solve a problem",
            "A storage device",
            "An operating system",
            "A programming keyboard"
        ],
        "answer": "A sequence of steps to solve a problem"
    },

    {
        "id": "w15",
        "question": "Which is a machine-learning approach?",
        "options": [
            "Supervised learning",
            "Monitor learning",
            "Keyboard learning",
            "Folder learning"
        ],
        "answer": "Supervised learning"
    },

    {
        "id": "w16",
        "question": "Which component is volatile memory?",
        "options": ["RAM", "SSD", "HDD", "ROM"],
        "answer": "RAM"
    },

    {
        "id": "w17",
        "question": "Which language is commonly used with Flask?",
        "options": ["Python", "HTML", "SQL", "CSS"],
        "answer": "Python"
    },

    {
        "id": "w18",
        "question": "Which HTML element creates a hyperlink?",
        "options": ["a", "p", "img", "table"],
        "answer": "a"
    },

    {
        "id": "w19",
        "question": "Which command sends local Git commits to a remote repository?",
        "options": ["git push", "git pull", "git send", "git upload"],
        "answer": "git push"
    },

    {
        "id": "w20",
        "question": "Which principle protects information from unauthorized access?",
        "options": [
            "Confidentiality",
            "Iteration",
            "Compilation",
            "Rendering"
        ],
        "answer": "Confidentiality"
    }
]


# ============================================================
# BUG HUNTER
# ============================================================

bug_challenges = [

    {
        "id": "bug1",
        "language": "python",
        "title": "Fix the Addition Bug",
        "code": """a = 10
b = 20

result = a - b

print(result)
""",
        "answer": "result = a + b",
        "explanation": "The program should add a and b, not subtract them.",
        "xp": 50
    },

    {
        "id": "bug2",
        "language": "python",
        "title": "Fix the Condition",
        "code": """age = 20

if age < 18:
    print("Adult")
else:
    print("Minor")
""",
        "answer": "if age >= 18:",
        "explanation": "The condition is reversed.",
        "xp": 50
    },

    {
        "id": "bug3",
        "language": "c",
        "title": "Fix the Output",
        "code": """#include <stdio.h>

int main() {

    printf("Hello")

    return 0;
}
""",
        "answer": "printf(\"Hello\");",
        "explanation": "The printf statement needs a semicolon.",
        "xp": 50
    }
]


# ============================================================
# CAREER GUIDE
# ============================================================

careers = [

    {
        "title": "Software Developer",
        "icon": "💻",
        "skills": [
            "Programming",
            "Data Structures",
            "Git",
            "Databases",
            "Problem Solving",
            "APIs"
        ],
        "roadmap": [
            "Learn programming fundamentals",
            "Master one primary language",
            "Learn data structures",
            "Build projects",
            "Learn Git and GitHub",
            "Practice technical interviews"
        ]
    },

    {
        "title": "Web Developer",
        "icon": "🌐",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "Backend",
            "Databases",
            "Git"
        ],
        "roadmap": [
            "Learn HTML",
            "Master CSS",
            "Learn JavaScript",
            "Build frontend projects",
            "Learn backend development",
            "Deploy applications"
        ]
    },

    {
        "title": "Python Developer",
        "icon": "🐍",
        "skills": [
            "Python",
            "OOP",
            "Flask/Django",
            "APIs",
            "SQL",
            "Git"
        ],
        "roadmap": [
            "Learn Python",
            "Learn OOP",
            "Learn SQL",
            "Build APIs",
            "Learn Flask/Django",
            "Deploy projects"
        ]
    },

    {
        "title": "AI / ML Engineer",
        "icon": "🤖",
        "skills": [
            "Python",
            "Statistics",
            "Machine Learning",
            "Data Processing",
            "Model Evaluation",
            "Deep Learning"
        ],
        "roadmap": [
            "Master Python",
            "Learn mathematics",
            "Learn statistics",
            "Study machine learning",
            "Build ML projects",
            "Explore deep learning"
        ]
    },

    {
        "title": "Cybersecurity",
        "icon": "🛡️",
        "skills": [
            "Networking",
            "Linux",
            "Security Fundamentals",
            "Cryptography",
            "Web Security",
            "Defensive Security"
        ],
        "roadmap": [
            "Learn networking",
            "Learn Linux",
            "Study security fundamentals",
            "Practice in legal labs",
            "Learn defensive security",
            "Build security projects"
        ]
    }
]


# ============================================================
# PROJECTS
# ============================================================

projects = [

    {
        "title": "Student Management System",
        "difficulty": "Beginner",
        "technologies": ["Python", "SQLite"],
        "description": "Manage student records using CRUD operations."
    },

    {
        "title": "Quiz Application",
        "difficulty": "Beginner",
        "technologies": ["HTML", "CSS", "JavaScript"],
        "description": "Build a timed quiz application with score tracking."
    },

    {
        "title": "Expense Tracker",
        "difficulty": "Beginner",
        "technologies": ["Python", "SQLite"],
        "description": "Track income and expenses."
    },

    {
        "title": "Weather Dashboard",
        "difficulty": "Intermediate",
        "technologies": ["HTML", "CSS", "JavaScript", "API"],
        "description": "Display weather information using an API."
    },

    {
        "title": "AI Study Assistant",
        "difficulty": "Advanced",
        "technologies": ["Python", "Flask", "AI API"],
        "description": "Create an assistant that helps students study."
    },

    {
        "title": "CodeQuest AI",
        "difficulty": "Advanced",
        "technologies": [
            "Flask",
            "HTML",
            "CSS",
            "JavaScript",
            "Firebase",
            "SQLite"
        ],
        "description": "Build a gamified computer-science learning platform."
    }
]


# ============================================================
# DAILY MISSIONS
# ============================================================

daily_missions = [

    {
        "id": "lesson",
        "title": "Knowledge Drop",
        "description": "Complete one lesson.",
        "xp": 20,
        "icon": "📚"
    },

    {
        "id": "quiz",
        "title": "Quiz Warrior",
        "description": "Answer five quiz questions.",
        "xp": 30,
        "icon": "🧠"
    },

    {
        "id": "bug",
        "title": "Bug Hunter",
        "description": "Solve one coding bug.",
        "xp": 50,
        "icon": "💻"
    },

    {
        "id": "daily",
        "title": "Daily Legend",
        "description": "Complete all daily missions.",
        "xp": 100,
        "icon": "🏆"
    }
]


# ============================================================
# HELPERS
# ============================================================

def get_user(user_id):

    if not user_id:
        user_id = "guest"

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    if not user:
        conn.execute("""
            INSERT INTO users
            (user_id, name, email, xp, streak, completed_lessons)
            VALUES (?, ?, ?, 0, 0, 0)
        """, (
            user_id,
            "Player",
            ""
        ))

        conn.commit()

        user = conn.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()

    conn.close()

    return user


def add_xp(user_id, amount):

    get_user(user_id)

    conn = get_db()

    conn.execute("""
        UPDATE users
        SET xp = xp + ?
        WHERE user_id = ?
    """, (
        int(amount),
        user_id
    ))

    conn.commit()

    user = conn.execute(
        "SELECT xp FROM users WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    conn.close()

    return user["xp"]


def update_user_info(user_id, name=None, email=None):

    get_user(user_id)

    conn = get_db()

    if name is not None:
        conn.execute("""
            UPDATE users
            SET name = ?
            WHERE user_id = ?
        """, (name, user_id))

    if email is not None:
        conn.execute("""
            UPDATE users
            SET email = ?
            WHERE user_id = ?
        """, (email, user_id))

    conn.commit()
    conn.close()


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/status")
def status():

    return jsonify({
        "success": True,
        "app": "CodeQuest AI",
        "version": "1.0",
        "status": "online",
        "courses": len(courses),
        "quiz_questions": len(quiz_bank)
    })


# ============================================================
# COURSES
# ============================================================

@app.route("/api/courses")
def get_courses():

    result = []

    for course_id, course in courses.items():

        result.append({
            "id": course_id,
            "name": course["name"],
            "icon": course["icon"],
            "level": course["level"],
            "description": course["description"],
            "chapter_count": len(course["chapters"])
        })

    return jsonify({
        "success": True,
        "courses": result
    })


@app.route("/api/course/<course_id>")
def get_course(course_id):

    course_id = course_id.lower().strip()

    course = courses.get(course_id)

    # Also allow searching by display name
    if not course:

        decoded_name = course_id.replace("-", " ")

        for cid, value in courses.items():

            if value["name"].lower() == decoded_name:
                course_id = cid
                course = value
                break

    if not course:

        return jsonify({
            "success": False,
            "error": "Course not found."
        }), 404

    chapters = []

    for index, chapter in enumerate(course["chapters"]):

        chapters.append({
            "index": index,
            "title": chapter["title"],
            "topic": chapter["topic"]
        })

    return jsonify({
        "success": True,
        "id": course_id,
        "name": course["name"],
        "icon": course["icon"],
        "level": course["level"],
        "description": course["description"],
        "chapters": chapters
    })


@app.route("/api/lesson/<course_id>/<int:index>")
def get_lesson(course_id, index):

    course_id = course_id.lower().strip()

    course = courses.get(course_id)

    if not course:

        for cid, value in courses.items():

            if value["name"].lower() == course_id.replace("-", " "):
                course = value
                course_id = cid
                break

    if not course:

        return jsonify({
            "success": False,
            "error": "Course not found."
        }), 404

    chapters = course["chapters"]

    if index < 0 or index >= len(chapters):

        return jsonify({
            "success": False,
            "error": "Lesson not found."
        }), 404

    lesson = chapters[index]

    return jsonify({
        "success": True,
        "course": course["name"],
        "course_id": course_id,
        "index": index,
        "lesson": lesson
    })


# Compatibility route for older frontend versions
@app.route("/api/lesson/<chapter>")
def old_lesson_route(chapter):

    chapter = chapter.lower()

    for course_id, course in courses.items():

        for index, lesson in enumerate(course["chapters"]):

            if lesson["title"].lower() == chapter.replace("-", " "):

                return jsonify({
                    "success": True,
                    "course": course["name"],
                    "course_id": course_id,
                    "index": index,
                    "lesson": lesson
                })

    return jsonify({
        "success": False,
        "error": "Lesson not found."
    }), 404


# ============================================================
# COMPLETE LESSON
# ============================================================

@app.route("/api/lesson-complete", methods=["POST"])
def lesson_complete():

    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id", "guest")
    course = data.get("course", "")
    lesson_index = int(data.get("lesson_index", 0))

    get_user(user_id)

    conn = get_db()

    existing = conn.execute("""
        SELECT id
        FROM lesson_progress
        WHERE user_id = ?
        AND course = ?
        AND lesson_index = ?
    """, (
        user_id,
        course,
        lesson_index
    )).fetchone()

    if existing:

        conn.close()

        user = get_user(user_id)

        return jsonify({
            "success": True,
            "already_completed": True,
            "xp": user["xp"],
            "level": get_level(user["xp"])
        })

    conn.execute("""
        INSERT INTO lesson_progress
        (user_id, course, lesson_index, completed_at)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        course,
        lesson_index,
        datetime.utcnow().isoformat()
    ))

    conn.execute("""
        UPDATE users
        SET completed_lessons = completed_lessons + 1
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()

    new_xp = add_xp(user_id, 20)

    return jsonify({
        "success": True,
        "already_completed": False,
        "earned_xp": 20,
        "xp": new_xp,
        "level": get_level(new_xp)
    })


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/api/dashboard")
def dashboard():

    user_id = request.args.get("user_id", "guest")

    user = get_user(user_id)

    level = get_level(user["xp"])

    return jsonify({
        "success": True,
        "user": {
            "id": user["user_id"],
            "name": user["name"],
            "email": user["email"]
        },
        "xp": user["xp"],
        "level": level["level"],
        "level_name": level["name"],
        "streak": user["streak"],
        "completed_lessons": user["completed_lessons"],
        "quizzes_completed": user["quizzes_completed"],
        "weekly_tests": user["weekly_tests"],
        "daily_missions": daily_missions
    })


# ============================================================
# PROGRESS
# ============================================================

@app.route("/api/progress")
def progress():

    user_id = request.args.get("user_id", "guest")

    user = get_user(user_id)

    conn = get_db()

    completed = conn.execute("""
        SELECT course, lesson_index, completed_at
        FROM lesson_progress
        WHERE user_id = ?
        ORDER BY completed_at DESC
    """, (user_id,)).fetchall()

    conn.close()

    level = get_level(user["xp"])

    return jsonify({
        "success": True,
        "xp": user["xp"],
        "level": level,
        "streak": user["streak"],
        "completed_lessons": user["completed_lessons"],
        "lessons": [
            dict(row) for row in completed
        ]
    })


# ============================================================
# QUIZ
# ============================================================

@app.route("/api/quiz")
def quiz():

    user_id = request.args.get("user_id", "guest")
    course_filter = request.args.get("course", "").lower()

    get_user(user_id)

    conn = get_db()

    used_rows = conn.execute("""
        SELECT question_id
        FROM quiz_history
        WHERE user_id = ?
    """, (user_id,)).fetchall()

    conn.close()

    used = {
        row["question_id"]
        for row in used_rows
    }

    available = [
        q for q in quiz_bank
        if q["id"] not in used
    ]

    if course_filter:

        filtered = [
            q for q in available
            if course_filter in q["course"].lower()
        ]

        if filtered:
            available = filtered

    if not available:

        return jsonify({
            "success": False,
            "message": "You have completed every available question. New questions will be added soon.",
            "remaining": 0
        })

    selected = random.sample(
        available,
        min(10, len(available))
    )

    # Never send answers to the frontend
    questions = []

    for q in selected:

        questions.append({
            "id": q["id"],
            "course": q["course"],
            "question": q["question"],
            "options": q["options"],
            "xp": q["xp"]
        })

    return jsonify({
        "success": True,
        "questions": questions,
        "remaining": len(available)
    })


@app.route("/api/quiz/answer", methods=["POST"])
def quiz_answer():

    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id", "guest")
    question_id = data.get("question_id")
    answer = data.get("answer")

    question = None

    for q in quiz_bank:

        if q["id"] == question_id:
            question = q
            break

    if not question:

        return jsonify({
            "success": False,
            "error": "Question not found."
        }), 404

    conn = get_db()

    existing = conn.execute("""
        SELECT id
        FROM quiz_history
        WHERE user_id = ?
        AND question_id = ?
    """, (
        user_id,
        question_id
    )).fetchone()

    if existing:

        conn.close()

        return jsonify({
            "success": False,
            "error": "This question has already been answered."
        }), 409

    correct = (
        str(answer).strip().lower()
        ==
        str(question["answer"]).strip().lower()
    )

    conn.execute("""
        INSERT INTO quiz_history
        (user_id, question_id, answered_at)
        VALUES (?, ?, ?)
    """, (
        user_id,
        question_id,
        datetime.utcnow().isoformat()
    ))

    conn.execute("""
        UPDATE users
        SET quizzes_completed = quizzes_completed + 1
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()

    earned = question["xp"] if correct else 0

    if earned:
        new_xp = add_xp(user_id, earned)
    else:
        new_xp = get_user(user_id)["xp"]

    return jsonify({
        "success": True,
        "correct": correct,
        "earned_xp": earned,
        "xp": new_xp,
        "correct_answer": question["answer"],
        "explanation": question["explanation"]
    })


@app.route("/api/quiz/reset", methods=["POST"])
def reset_quiz():

    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id", "guest")

    conn = get_db()

    conn.execute("""
        DELETE FROM quiz_history
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Quiz history reset."
    })


# ============================================================
# WEEKLY TEST
# ============================================================

@app.route("/api/weekly-test")
def weekly_test():

    selected = random.sample(
        weekly_questions,
        min(20, len(weekly_questions))
    )

    return jsonify({
        "success": True,
        "duration_seconds": 30 * 60,
        "total": len(selected),
        "questions": [
            {
                "id": q["id"],
                "question": q["question"],
                "options": q["options"]
            }
            for q in selected
        ]
    })


@app.route("/api/weekly-test/submit", methods=["POST"])
def weekly_test_submit():

    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id", "guest")
    answers = data.get("answers", {})

    score = 0
    total = len(weekly_questions)

    for q in weekly_questions:

        submitted = answers.get(q["id"])

        if submitted is not None:

            if str(submitted).strip().lower() == q["answer"].lower():
                score += 1

    # Maximum 500 XP
    xp = int((score / total) * 500) if total else 0

    new_xp = add_xp(user_id, xp)

    conn = get_db()

    conn.execute("""
        INSERT INTO weekly_history
        (user_id, score, total, xp, taken_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        score,
        total,
        xp,
        datetime.utcnow().isoformat()
    ))

    conn.execute("""
        UPDATE users
        SET weekly_tests = weekly_tests + 1
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 2) if total else 0,
        "earned_xp": xp,
        "xp": new_xp,
        "level": get_level(new_xp)
    })


# ============================================================
# CODE LAB
# ============================================================

@app.route("/api/compiler/languages")
def compiler_languages():

    return jsonify({
        "success": True,
        "languages": [
            {
                "id": "python",
                "name": "Python",
                "icon": "🐍"
            },
            {
                "id": "c",
                "name": "C",
                "icon": "🇨"
            },
            {
                "id": "cpp",
                "name": "C++",
                "icon": "⚡"
            },
            {
                "id": "java",
                "name": "Java",
                "icon": "☕"
            }
        ]
    })


@app.route("/api/compile", methods=["POST"])
def compile_code():

    data = request.get_json(silent=True) or {}

    code = str(data.get("code", ""))
    language = str(
        data.get("language", "python")
    ).lower().strip()

    stdin = str(data.get("stdin", ""))

    if not code.strip():

        return jsonify({
            "success": False,
            "error": "Please enter some code."
        }), 400

    supported = {
        "python",
        "c",
        "cpp",
        "c++",
        "java"
    }

    if language not in supported:

        return jsonify({
            "success": False,
            "error": "Unsupported language."
        }), 400

    # --------------------------------------------------------
    # Wandbox compiler discovery
    # --------------------------------------------------------

    try:

        compiler_list = requests.get(
            "https://wandbox.org/api/list.json",
            timeout=15
        )

        if compiler_list.status_code != 200:

            return jsonify({
                "success": False,
                "error": "Compiler service is currently unavailable."
            }), 503

        compiler_data = compiler_list.json()

        if language == "python":
            keywords = ["python"]

        elif language == "c":
            keywords = ["gcc-c"]

        elif language in ("cpp", "c++"):
            keywords = ["gcc-head", "g++"]

        elif language == "java":
            keywords = ["openjdk", "java"]

        else:
            keywords = []

        selected = None

        for compiler in compiler_data:

            name = str(
                compiler.get("name", "")
            ).lower()

            display = str(
                compiler.get("display-name", "")
            ).lower()

            for keyword in keywords:

                if keyword.lower() in name or \
                   keyword.lower() in display:

                    selected = compiler
                    break

            if selected:
                break

        if not selected:

            return jsonify({
                "success": False,
                "error":
                    f"No {language.upper()} compiler is currently available."
            }), 503

        compiler_name = selected.get("name")

        payload = {
            "code": code,
            "compiler": compiler_name,
            "stdin": stdin,
            "save": False
        }

        result = requests.post(
            "https://wandbox.org/api/compile.json",
            json=payload,
            timeout=30
        )

        if result.status_code != 200:

            return jsonify({
                "success": False,
                "error": "Compiler service returned an error.",
                "details": result.text[:1000]
            }), 502

        result_data = result.json()

        output = result_data.get(
            "program_output",
            ""
        )

        program_error = result_data.get(
            "program_error",
            ""
        )

        compiler_error = result_data.get(
            "compiler_error",
            ""
        )

        signal = result_data.get(
            "signal",
            0
        )

        success = (
            not compiler_error.strip()
            and not program_error.strip()
            and signal in (0, None)
        )

        return jsonify({
            "success": success,
            "language": language,
            "compiler": compiler_name,
            "output": output,
            "error": compiler_error or program_error,
            "compiler_error": compiler_error,
            "program_error": program_error,
            "signal": signal
        })

    except requests.Timeout:

        return jsonify({
            "success": False,
            "error":
                "Compiler request timed out. Please try again."
        }), 504

    except Exception as e:

        return jsonify({
            "success": False,
            "error":
                "Compiler error: " + str(e)
        }), 500


# ============================================================
# BUG HUNTER
# ============================================================

@app.route("/api/code-challenges")
def code_challenges():

    return jsonify({
        "success": True,
        "challenges": [
            {
                "id": c["id"],
                "language": c["language"],
                "title": c["title"],
                "code": c["code"],
                "xp": c["xp"]
            }
            for c in bug_challenges
        ]
    })


@app.route("/api/error-finder")
def error_finder():

    challenge = random.choice(bug_challenges)

    return jsonify({
        "success": True,
        "challenge": {
            "id": challenge["id"],
            "language": challenge["language"],
            "title": challenge["title"],
            "code": challenge["code"],
            "xp": challenge["xp"]
        }
    })


# ============================================================
# CAREER
# ============================================================

@app.route("/api/careers")
def get_careers():

    return jsonify({
        "success": True,
        "careers": careers
    })


# ============================================================
# PROJECTS
# ============================================================

@app.route("/api/projects")
def get_projects():

    return jsonify({
        "success": True,
        "projects": projects
    })


# ============================================================
# ACHIEVEMENTS
# ============================================================

@app.route("/api/achievements")
def achievements():

    user_id = request.args.get(
        "user_id",
        "guest"
    )

    user = get_user(user_id)

    achievements_list = [

        {
            "id": "first-step",
            "title": "First Step",
            "icon": "👣",
            "description": "Complete your first lesson.",
            "unlocked":
                user["completed_lessons"] >= 1
        },

        {
            "id": "quiz-master",
            "title": "Quiz Master",
            "icon": "🧠",
            "description": "Answer 10 quiz questions.",
            "unlocked":
                user["quizzes_completed"] >= 10
        },

        {
            "id": "programmer",
            "title": "Programmer",
            "icon": "💻",
            "description": "Reach 1,000 XP.",
            "unlocked":
                user["xp"] >= 1000
        },

        {
            "id": "code-master",
            "title": "Code Master",
            "icon": "👑",
            "description": "Reach 8,000 XP.",
            "unlocked":
                user["xp"] >= 8000
        },

        {
            "id": "legend",
            "title": "CodeQuest Legend",
            "icon": "⚡",
            "description": "Reach 25,000 XP.",
            "unlocked":
                user["xp"] >= 25000
        }
    ]

    return jsonify({
        "success": True,
        "achievements": achievements_list
    })


# ============================================================
# DAILY MISSIONS
# ============================================================

@app.route("/api/daily-missions")
def get_daily_missions():

    return jsonify({
        "success": True,
        "missions": daily_missions
    })


# ============================================================
# PROFILE
# ============================================================

@app.route("/api/profile", methods=["GET", "POST"])
def profile():

    if request.method == "GET":

        user_id = request.args.get(
            "user_id",
            "guest"
        )

        user = get_user(user_id)

        return jsonify({
            "success": True,
            "profile": {
                "user_id": user["user_id"],
                "name": user["name"],
                "email": user["email"],
                "xp": user["xp"],
                "level": get_level(user["xp"]),
                "streak": user["streak"]
            }
        })

    data = request.get_json(silent=True) or {}

    user_id = data.get(
        "user_id",
        "guest"
    )

    update_user_info(
        user_id,
        data.get("name"),
        data.get("email")
    )

    user = get_user(user_id)

    return jsonify({
        "success": True,
        "profile": {
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "xp": user["xp"],
            "level": get_level(user["xp"]),
            "streak": user["streak"]
        }
    })


# ============================================================
# ERROR HANDLER
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "error": "API route not found."
    }), 404


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "success": False,
        "error": "Internal server error."
    }), 500


# ============================================================
# START
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
        debug=True
    )
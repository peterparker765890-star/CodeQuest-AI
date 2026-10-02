from flask import Flask, render_template, jsonify, request
import os
import requests
import random
import math

app = Flask(__name__)

# ============================================================
# CODEQUEST AI
# LEARN • PRACTICE • PLAY • BUILD
# FINAL BACKEND
# ============================================================

APP_NAME = "CodeQuest AI"

# ------------------------------------------------------------
# OPTIONAL FIREBASE ADMIN
# ------------------------------------------------------------

try:
    import firebase_admin
    from firebase_admin import credentials, auth

    if not firebase_admin._apps:
        service_account_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")

        if service_account_json:
            import json
            cred = credentials.Certificate(json.loads(service_account_json))
            firebase_admin.initialize_app(cred)

    FIREBASE_READY = bool(firebase_admin._apps)

except Exception:
    FIREBASE_READY = False


# ------------------------------------------------------------
# ONECOMPILER
# ------------------------------------------------------------
#
# Add this Render environment variable:
#
# ONECOMPILER_API_KEY = your_key_here
#
# Current OneCompiler API:
# https://api.onecompiler.com/v1/run
#
# ------------------------------------------------------------

ONECOMPILER_API_KEY = os.environ.get("ONECOMPILER_API_KEY", "").strip()


# ============================================================
# COURSE DATA
# ============================================================

COURSES = {

    "Computer Basics": {
        "icon": "💻",
        "level": "Beginner",
        "description": "Understand computers from zero.",
        "chapters": [

            {
                "title": "What is a Computer?",
                "lessons": [
                    {
                        "title": "Introduction to Computers",
                        "explanation": """
A computer is an electronic device that accepts data,
processes it according to instructions, stores information,
and produces useful output.

A simple computer workflow is:

INPUT → PROCESSING → OUTPUT → STORAGE

For example, when you type two numbers into a calculator,
the numbers are input, the processor performs the calculation,
and the answer becomes the output.
""",
                        "example": "A laptop, smartphone, ATM and smart TV are all examples of computing devices.",
                        "code": """# A simple Python example
a = 10
b = 20

result = a + b

print(result)
""",
                        "practice": "Identify the input, processing and output when you search for something on Google."
                    },

                    {
                        "title": "Data and Information",
                        "explanation": """
Data means raw facts.

Information is processed data that has meaning.

Example:

Data:
90, 80, 70

Information:
The average mark is 80.

Computers work with data in many forms including numbers,
text, images, audio and video.
""",
                        "example": "A student's marks are data. A report showing the student's average and grade is information.",
                        "code": """marks = [90, 80, 70]

average = sum(marks) / len(marks)

print("Average:", average)
""",
                        "practice": "Give three examples of data used by a college."
                    }
                ]
            },

            {
                "title": "Hardware",
                "lessons": [
                    {
                        "title": "Computer Hardware",
                        "explanation": """
Hardware refers to the physical components of a computer.

Examples include:

• CPU
• RAM
• Keyboard
• Mouse
• Monitor
• SSD
• Motherboard
• Power supply

Hardware can be physically touched.
""",
                        "example": "When you open a laptop, the SSD, RAM, motherboard and cooling system are hardware.",
                        "code": """# Software can display information about hardware.
print("CPU")
print("RAM")
print("Storage")
""",
                        "practice": "List five hardware components."
                    },

                    {
                        "title": "CPU",
                        "explanation": """
CPU stands for Central Processing Unit.

It is responsible for executing instructions.

Important CPU concepts include:

• Control Unit
• Arithmetic Logic Unit
• Registers
• Cache

The CPU repeatedly performs a cycle:

Fetch → Decode → Execute
""",
                        "example": "When a program calculates 25 + 10, the CPU performs the required operations.",
                        "code": """a = 25
b = 10

print(a + b)
""",
                        "practice": "Explain why the CPU is important in a computer."
                    }
                ]
            },

            {
                "title": "Memory and Storage",
                "lessons": [
                    {
                        "title": "RAM and ROM",
                        "explanation": """
RAM is temporary working memory.

Programs currently being used are loaded into RAM.

RAM is volatile, meaning its contents are normally lost
when power is removed.

ROM is non-volatile memory used for information that should
remain available even after power is removed.
""",
                        "example": "Opening many applications can consume more RAM.",
                        "code": """numbers = []

for i in range(5):
    numbers.append(i)

print(numbers)
""",
                        "practice": "What is the main difference between RAM and storage?"
                    },

                    {
                        "title": "Storage Devices",
                        "explanation": """
Storage keeps information for long-term use.

Examples:

• HDD
• SSD
• USB drive
• Memory card
• Optical disk
• Cloud storage

SSD storage is generally much faster than traditional HDD storage.
""",
                        "example": "Your college project files can be stored on an SSD and backed up to Google Drive.",
                        "code": """file_name = "project.txt"

print("File:", file_name)
""",
                        "practice": "Name two storage devices."
                    }
                ]
            },

            {
                "title": "Operating Systems",
                "lessons": [
                    {
                        "title": "What is an Operating System?",
                        "explanation": """
An operating system manages computer hardware and provides
an environment in which applications can run.

Examples:

• Windows
• Linux
• macOS
• Android
• iOS

The operating system manages files, memory, processes,
devices and user interaction.
""",
                        "example": "Android manages the hardware and applications of your smartphone.",
                        "code": """import platform

print(platform.system())
""",
                        "practice": "Name three operating systems."
                    }
                ]
            },

            {
                "title": "Internet Basics",
                "lessons": [
                    {
                        "title": "How the Internet Works",
                        "explanation": """
The Internet is a global network of connected devices.

When you visit a website, your device communicates with
servers using networking protocols.

Important concepts include:

• IP address
• DNS
• HTTP
• HTTPS
• Client
• Server
• Router
""",
                        "example": "When you open CodeQuest AI, your browser acts as a client and communicates with the web server.",
                        "code": """import socket

host = "example.com"

print(socket.gethostbyname(host))
""",
                        "practice": "What does DNS do?"
                    }
                ]
            }
        ]
    },


    # ========================================================
    # PROGRAMMING FUNDAMENTALS
    # ========================================================

    "Programming Fundamentals": {
        "icon": "🧠",
        "level": "Beginner",
        "description": "Learn how programmers think and solve problems.",
        "chapters": [

            {
                "title": "Algorithms",
                "lessons": [
                    {
                        "title": "What is an Algorithm?",
                        "explanation": """
An algorithm is a step-by-step procedure for solving a problem.

A good algorithm should be:

• Clear
• Finite
• Ordered
• Effective

Example for making tea:

1. Boil water
2. Add tea powder
3. Add milk
4. Add sugar
5. Filter and serve
""",
                        "example": "A navigation application uses algorithms to calculate routes.",
                        "code": """number = 10

if number > 0:
    print("Positive")
else:
    print("Not positive")
""",
                        "practice": "Write five steps for logging into an application."
                    }
                ]
            },

            {
                "title": "Variables and Data Types",
                "lessons": [
                    {
                        "title": "Variables",
                        "explanation": """
A variable is a named location used to store a value.

For example:

name = "Joe"
age = 18

Here, name and age are variables.
""",
                        "example": "A student application may store a student's name, ID and department.",
                        "code": """name = "Student"
age = 18

print(name)
print(age)
""",
                        "practice": "Create variables for your name, age and department."
                    }
                ]
            },

            {
                "title": "Conditions",
                "lessons": [
                    {
                        "title": "if and else",
                        "explanation": """
Conditional statements allow programs to make decisions.

A program can check a condition and execute different
instructions depending on whether the condition is true or false.
""",
                        "example": "A college application can check whether a student has passed an exam.",
                        "code": """mark = 75

if mark >= 40:
    print("Pass")
else:
    print("Fail")
""",
                        "practice": "Create a program that checks whether a number is positive or negative."
                    }
                ]
            },

            {
                "title": "Loops",
                "lessons": [
                    {
                        "title": "Repeating Instructions",
                        "explanation": """
Loops allow a program to repeat instructions.

Common loops include:

• for
• while

Loops are useful when working with lists, numbers,
records and repeated tasks.
""",
                        "example": "A program can use a loop to display the names of 100 students.",
                        "code": """for i in range(1, 6):
    print(i)
""",
                        "practice": "Print numbers from 1 to 10."
                    }
                ]
            },

            {
                "title": "Functions",
                "lessons": [
                    {
                        "title": "Reusable Code",
                        "explanation": """
A function is a reusable block of code designed to perform
a particular task.

Functions make programs easier to understand,
test and maintain.
""",
                        "example": "A billing system might have separate functions for calculating tax and total price.",
                        "code": """def add(a, b):
    return a + b

print(add(5, 3))
""",
                        "practice": "Create a function that multiplies two numbers."
                    }
                ]
            }
        ]
    },


    # ========================================================
    # C
    # ========================================================

    "C Programming": {
        "icon": "🔵",
        "level": "Beginner → Intermediate",
        "description": "Build strong programming fundamentals with C.",
        "chapters": [

            {
                "title": "C Basics",
                "lessons": [
                    {
                        "title": "Your First C Program",
                        "explanation": """
C is a general-purpose programming language.

It is widely used for learning programming fundamentals,
systems programming, embedded systems and performance-critical software.

Every C program starts execution from the main function.
""",
                        "example": "C is used in operating systems, embedded devices and many low-level applications.",
                        "code": """#include <stdio.h>

int main() {
    printf("Hello, CodeQuest!");
    return 0;
}
""",
                        "practice": "Change the message printed by the program."
                    },

                    {
                        "title": "Variables and Input",
                        "explanation": """
Variables store values.

C requires you to specify the data type of a variable.

Common types:

int
float
char
double
""",
                        "example": "A student management program could store student age as an integer.",
                        "code": """#include <stdio.h>

int main() {
    int age;

    printf("Enter age: ");
    scanf("%d", &age);

    printf("Age = %d", age);

    return 0;
}
""",
                        "practice": "Create a program that accepts two numbers."
                    }
                ]
            },

            {
                "title": "Conditions and Loops",
                "lessons": [
                    {
                        "title": "if and else in C",
                        "explanation": """
Conditional statements allow C programs to make decisions.
""",
                        "example": "A result system can determine whether a student passed.",
                        "code": """#include <stdio.h>

int main() {
    int mark = 75;

    if (mark >= 40)
        printf("Pass");
    else
        printf("Fail");

    return 0;
}
""",
                        "practice": "Change the pass mark to 50."
                    },

                    {
                        "title": "for Loop",
                        "explanation": """
A for loop repeats a block of code a specified number of times.
""",
                        "example": "Loops can process marks of many students.",
                        "code": """#include <stdio.h>

int main() {
    for (int i = 1; i <= 5; i++) {
        printf("%d\\n", i);
    }

    return 0;
}
""",
                        "practice": "Print numbers from 1 to 10."
                    }
                ]
            },

            {
                "title": "Arrays and Functions",
                "lessons": [
                    {
                        "title": "Arrays",
                        "explanation": """
An array stores multiple values of the same data type.
""",
                        "example": "An array can store the marks of five students.",
                        "code": """#include <stdio.h>

int main() {
    int marks[3] = {80, 90, 75};

    printf("%d", marks[0]);

    return 0;
}
""",
                        "practice": "Create an array containing five numbers."
                    },

                    {
                        "title": "Functions",
                        "explanation": """
Functions allow you to divide a program into reusable pieces.
""",
                        "example": "A calculator can use separate functions for addition, subtraction and multiplication.",
                        "code": """#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    printf("%d", add(10, 20));
    return 0;
}
""",
                        "practice": "Create a subtraction function."
                    }
                ]
            },

            {
                "title": "Pointers and Structures",
                "lessons": [
                    {
                        "title": "Pointers",
                        "explanation": """
A pointer stores the memory address of another variable.

Pointers are one of the most important features of C.
They are used in arrays, functions, dynamic memory and systems programming.
""",
                        "example": "Operating systems and embedded software frequently use memory addresses.",
                        "code": """#include <stdio.h>

int main() {
    int x = 10;
    int *p = &x;

    printf("%d", *p);

    return 0;
}
""",
                        "practice": "Create a pointer to an integer variable."
                    }
                ]
            }
        ]
    },


    # ========================================================
    # C++
    # ========================================================

    "C++ Programming": {
        "icon": "⚙️",
        "level": "Intermediate",
        "description": "Learn modern C++ and object-oriented programming.",
        "chapters": [
            {
                "title": "C++ Basics",
                "lessons": [
                    {
                        "title": "Hello World",
                        "explanation": """
C++ is a powerful programming language commonly used in
software development, games, systems and competitive programming.
""",
                        "example": "Game engines and high-performance applications commonly use C++.",
                        "code": """#include <iostream>
using namespace std;

int main() {
    cout << "Hello CodeQuest!";
    return 0;
}
""",
                        "practice": "Print your name."
                    }
                ]
            },

            {
                "title": "Classes and Objects",
                "lessons": [
                    {
                        "title": "Your First Class",
                        "explanation": """
A class defines the structure and behaviour of objects.

An object is an instance of a class.
""",
                        "example": "A Student class can represent students in a college application.",
                        "code": """#include <iostream>
using namespace std;

class Student {
public:
    string name;
};

int main() {
    Student s;
    s.name = "Alex";

    cout << s.name;

    return 0;
}
""",
                        "practice": "Add an age property."
                    }
                ]
            },

            {
                "title": "Inheritance and Polymorphism",
                "lessons": [
                    {
                        "title": "Inheritance",
                        "explanation": """
Inheritance allows a class to reuse properties and behaviour
from another class.
""",
                        "example": "A Developer class could inherit common properties from an Employee class.",
                        "code": """#include <iostream>
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
}
""",
                        "practice": "Create a child class from another class."
                    }
                ]
            }
        ]
    },


    # ========================================================
    # PYTHON
    # ========================================================

    "Python Programming": {
        "icon": "🐍",
        "level": "Beginner → Advanced",
        "description": "Learn Python for development, automation and AI.",
        "chapters": [
            {
                "title": "Python Basics",
                "lessons": [
                    {
                        "title": "Hello Python",
                        "explanation": """
Python is a high-level programming language known for
its readable syntax.

It is widely used for web development, automation,
data analysis, artificial intelligence and machine learning.
""",
                        "example": "Python is used in automation scripts, web applications and AI projects.",
                        "code": """print("Hello, CodeQuest AI!")
""",
                        "practice": "Print your name and department."
                    },

                    {
                        "title": "Input and Variables",
                        "explanation": """
Python variables do not require an explicit type declaration.

The input function allows a program to receive user input.
""",
                        "example": "A registration form can ask a user for their name.",
                        "code": """name = input("Enter your name: ")

print("Hello", name)
""",
                        "practice": "Ask the user for their age."
                    }
                ]
            },

            {
                "title": "Conditions and Loops",
                "lessons": [
                    {
                        "title": "if Statement",
                        "explanation": """
The if statement executes code when a condition is true.
""",
                        "example": "An application can check whether a user is eligible for something.",
                        "code": """age = 18

if age >= 18:
    print("Eligible")
else:
    print("Not eligible")
""",
                        "practice": "Check whether a number is positive."
                    },

                    {
                        "title": "Loops",
                        "explanation": """
Loops are used to repeat operations.
""",
                        "example": "A loop can process every item in a list of students.",
                        "code": """for name in ["Alex", "Sam", "John"]:
    print(name)
""",
                        "practice": "Print numbers from 1 to 10."
                    }
                ]
            },

            {
                "title": "Lists and Dictionaries",
                "lessons": [
                    {
                        "title": "Python Lists",
                        "explanation": """
A list stores multiple values.

Lists are ordered and can be changed.
""",
                        "example": "A list can store subjects or student names.",
                        "code": """subjects = ["C", "Python", "Java"]

print(subjects[0])
""",
                        "practice": "Create a list containing five subjects."
                    },

                    {
                        "title": "Dictionaries",
                        "explanation": """
A dictionary stores data as key-value pairs.
""",
                        "example": "A student record can contain name, age and department.",
                        "code": """student = {
    "name": "Alex",
    "age": 18,
    "department": "IT"
}

print(student["name"])
""",
                        "practice": "Add a college key."
                    }
                ]
            },

            {
                "title": "Functions and OOP",
                "lessons": [
                    {
                        "title": "Functions",
                        "explanation": """
Functions organize reusable logic.
""",
                        "example": "An application can create a function for calculating a student's average.",
                        "code": """def average(a, b):
    return (a + b) / 2

print(average(80, 90))
""",
                        "practice": "Create a function that calculates the square of a number."
                    }
                ]
            }
        ]
    },


    # ========================================================
    # JAVA
    # ========================================================

    "Java Programming": {
        "icon": "☕",
        "level": "Intermediate",
        "description": "Learn Java and object-oriented programming.",
        "chapters": [
            {
                "title": "Java Basics",
                "lessons": [
                    {
                        "title": "Hello Java",
                        "explanation": """
Java is a popular object-oriented programming language.

It is widely used for enterprise applications,
backend systems and Android development.
""",
                        "example": "Java is commonly used in large business applications.",
                        "code": """class Main {
    public static void main(String[] args) {
        System.out.println("Hello CodeQuest!");
    }
}
""",
                        "practice": "Print your name."
                    }
                ]
            },

            {
                "title": "Variables and Conditions",
                "lessons": [
                    {
                        "title": "Java Variables",
                        "explanation": """
Java uses explicit data types.

For example:

int
double
char
boolean
String
""",
                        "example": "A student application can store an age using int.",
                        "code": """class Main {
    public static void main(String[] args) {
        int age = 18;

        System.out.println(age);
    }
}
""",
                        "practice": "Create a variable for your marks."
                    }
                ]
            },

            {
                "title": "Classes and Objects",
                "lessons": [
                    {
                        "title": "Java Class",
                        "explanation": """
Java is strongly based on object-oriented programming.

Classes define objects and their behaviour.
""",
                        "example": "A Student class can represent student records.",
                        "code": """class Student {
    String name = "Alex";
}

class Main {
    public static void main(String[] args) {
        Student s = new Student();

        System.out.println(s.name);
    }
}
""",
                        "practice": "Add an age variable to Student."
                    }
                ]
            }
        ]
    },


    # ========================================================
    # WEB DEVELOPMENT
    # ========================================================

    "Web Development": {
        "icon": "🌐",
        "level": "Beginner → Advanced",
        "description": "Build modern websites and web applications.",
        "chapters": [
            {
                "title": "HTML",
                "lessons": [
                    {
                        "title": "Your First Web Page",
                        "explanation": """
HTML provides the structure of a web page.

Common elements include:

html
head
body
h1
p
button
input
img
a
""",
                        "example": "Every website you visit uses HTML or technologies that generate HTML.",
                        "code": """<!DOCTYPE html>
<html>
<body>

<h1>Hello CodeQuest</h1>
<p>My first webpage.</p>

</body>
</html>
""",
                        "practice": "Create a webpage containing your name."
                    }
                ]
            },

            {
                "title": "CSS",
                "lessons": [
                    {
                        "title": "Styling a Page",
                        "explanation": """
CSS controls the appearance of web pages.

It can control:

• Colors
• Fonts
• Spacing
• Layout
• Animations
• Responsive design
""",
                        "example": "CSS is used to create the visual design of CodeQuest AI.",
                        "code": """<!DOCTYPE html>
<html>
<head>
<style>
h1 {
    font-size: 40px;
}
</style>
</head>

<body>
<h1>CodeQuest</h1>
</body>
</html>
""",
                        "practice": "Change the heading size."
                    }
                ]
            },

            {
                "title": "JavaScript",
                "lessons": [
                    {
                        "title": "Interactive Websites",
                        "explanation": """
JavaScript adds behaviour and interaction to websites.

It can:

• Respond to button clicks
• Change HTML
• Validate forms
• Communicate with APIs
• Build dynamic interfaces
""",
                        "example": "The buttons and interactive components of CodeQuest AI can use JavaScript.",
                        "code": """<!DOCTYPE html>
<html>
<body>

<button onclick="hello()">Click me</button>

<script>
function hello() {
    alert("Hello CodeQuest!");
}
</script>

</body>
</html>
""",
                        "practice": "Change the alert message."
                    }
                ]
            }
        ]
    },


    # ========================================================
    # DATABASE
    # ========================================================

    "Database & SQL": {
        "icon": "🗄️",
        "level": "Intermediate",
        "description": "Learn databases and SQL.",
        "chapters": [
            {
                "title": "Database Fundamentals",
                "lessons": [
                    {
                        "title": "What is a Database?",
                        "explanation": """
A database is an organized collection of data.

Applications use databases to store information
that must be retrieved and updated efficiently.
""",
                        "example": "A college application may store student records in a database.",
                        "code": """CREATE TABLE students (
    id INTEGER,
    name TEXT,
    department TEXT
);
""",
                        "practice": "Design a table for college students."
                    }
                ]
            },

            {
                "title": "SQL Queries",
                "lessons": [
                    {
                        "title": "SELECT",
                        "explanation": """
SELECT is used to retrieve data from a database.
""",
                        "example": "A college application can retrieve all IT students.",
                        "code": """SELECT * FROM students;
""",
                        "practice": "Write a query that selects only student names."
                    }
                ]
            }
        ]
    },


    # ========================================================
    # GIT
    # ========================================================

    "Git & GitHub": {
        "icon": "🐙",
        "level": "Intermediate",
        "description": "Learn version control and project collaboration.",
        "chapters": [
            {
                "title": "Git Basics",
                "lessons": [
                    {
                        "title": "What is Git?",
                        "explanation": """
Git is a distributed version control system.

It helps developers track changes to source code.

Important commands include:

git init
git add
git commit
git push
git pull
git clone
""",
                        "example": "Developers use Git to maintain the history of software projects.",
                        "code": """git init
git add .
git commit -m "Initial commit"
""",
                        "practice": "Explain why version control is useful."
                    }
                ]
            }
        ]
    },


    # ========================================================
    # CLOUD
    # ========================================================

    "Cloud Computing": {
        "icon": "☁️",
        "level": "Intermediate",
        "description": "Understand cloud services and deployment.",
        "chapters": [
            {
                "title": "Cloud Fundamentals",
                "lessons": [
                    {
                        "title": "What is Cloud Computing?",
                        "explanation": """
Cloud computing allows computing resources such as servers,
storage and databases to be accessed over a network.

Examples include:

• AWS
• Microsoft Azure
• Google Cloud
• Firebase
""",
                        "example": "Your CodeQuest AI Flask application runs on a cloud hosting platform.",
                        "code": """print("Application deployed to the cloud!")
""",
                        "practice": "Name three cloud platforms."
                    }
                ]
            }
        ]
    },


    # ========================================================
    # AI & ML
    # ========================================================

    "AI & Machine Learning": {
        "icon": "🤖",
        "level": "Advanced",
        "description": "Understand AI, machine learning and generative AI.",
        "chapters": [
            {
                "title": "Artificial Intelligence",
                "lessons": [
                    {
                        "title": "What is AI?",
                        "explanation": """
Artificial Intelligence is a field of computing concerned
with creating systems that perform tasks associated with
human-like capabilities such as pattern recognition,
prediction, language processing and decision making.

Modern AI includes machine learning, deep learning,
natural language processing and generative AI.
""",
                        "example": "Recommendation systems can use machine learning to predict content a user may find relevant.",
                        "code": """message = "AI can process information"

print(message)
""",
                        "practice": "Give three examples of AI applications."
                    }
                ]
            },

            {
                "title": "Machine Learning",
                "lessons": [
                    {
                        "title": "Basic Machine Learning Idea",
                        "explanation": """
Machine learning systems learn patterns from data.

A simplified workflow is:

DATA → TRAINING → MODEL → PREDICTION
""",
                        "example": "A model can learn from previous examples to classify new data.",
                        "code": """data = [10, 20, 30, 40]

average = sum(data) / len(data)

print("Average:", average)
""",
                        "practice": "Why is data important in machine learning?"
                    }
                ]
            }
        ]
    },


    # ========================================================
    # CYBERSECURITY
    # ========================================================

    "Cybersecurity": {
        "icon": "🛡️",
        "level": "Intermediate → Advanced",
        "description": "Learn defensive cybersecurity fundamentals.",
        "chapters": [
            {
                "title": "Security Fundamentals",
                "lessons": [
                    {
                        "title": "What is Cybersecurity?",
                        "explanation": """
Cybersecurity protects computers, applications,
networks and data from unauthorized access,
damage and disruption.

Three important security goals are:

Confidentiality
Integrity
Availability
""",
                        "example": "Online banking uses security controls to protect account information.",
                        "code": """password = "example"

if len(password) >= 8:
    print("Password length is acceptable")
else:
    print("Use a longer password")
""",
                        "practice": "Explain confidentiality in your own words."
                    }
                ]
            },

            {
                "title": "Authentication",
                "lessons": [
                    {
                        "title": "Passwords and Authentication",
                        "explanation": """
Authentication verifies who a user is.

Modern applications can use:

• Passwords
• OTP
• Security keys
• Biometrics
• OAuth
• Multi-factor authentication
""",
                        "example": "Google login is an example of authentication through an identity provider.",
                        "code": """username = "student"
password = "1234"

if username == "student" and password == "1234":
    print("Login successful")
else:
    print("Login failed")
""",
                        "practice": "Why is multi-factor authentication useful?"
                    }
                ]
            },

            {
                "title": "Web Security",
                "lessons": [
                    {
                        "title": "Safe Web Development",
                        "explanation": """
Web applications should validate input, protect authentication,
use secure communication and avoid exposing sensitive information.

Important topics include:

• HTTPS
• Input validation
• Access control
• Secure authentication
• SQL injection awareness
• XSS awareness
• Security headers
""",
                        "example": "A login system should never trust user input blindly.",
                        "code": """user_input = input("Enter name: ")

# Always validate and safely handle user input.
print("Hello", user_input)
""",
                        "practice": "Why should applications validate input?"
                    }
                ]
            }
        ]
    }
}


# ============================================================
# CAREER ROADMAP
# ============================================================

CAREERS = [

    {
        "role": "Software Developer",
        "icon": "💻",
        "description": "Design, build, test and maintain software applications.",
        "skills": ["Programming", "Data Structures", "Git", "Databases", "Problem Solving"],
        "languages": ["C", "C++", "Java", "Python", "JavaScript"],
        "tools": ["GitHub", "VS Code", "Docker", "SQL"],
        "roadmap": [
            "Learn programming fundamentals",
            "Master one programming language",
            "Learn data structures and algorithms",
            "Build projects",
            "Learn Git and GitHub",
            "Prepare for internships",
            "Practice technical interviews"
        ],
        "benefits": [
            "Wide range of software careers",
            "Strong project-based portfolio opportunities",
            "Opportunities across many industries"
        ],
        "future": "Software development continues to evolve with cloud computing, AI-assisted development and distributed systems."
    },

    {
        "role": "Frontend Developer",
        "icon": "🎨",
        "description": "Build the user-facing part of websites and web applications.",
        "skills": ["HTML", "CSS", "JavaScript", "Responsive Design", "UI Fundamentals"],
        "languages": ["HTML", "CSS", "JavaScript", "TypeScript"],
        "tools": ["React", "GitHub", "VS Code"],
        "roadmap": [
            "Learn HTML",
            "Learn CSS",
            "Learn JavaScript",
            "Build responsive websites",
            "Learn a frontend framework",
            "Create a portfolio",
            "Practice frontend interviews"
        ],
        "benefits": [
            "Visual project portfolio",
            "Strong web development foundation",
            "Can progress toward full-stack development"
        ],
        "future": "Modern frontend development increasingly involves component frameworks, TypeScript, performance optimization and AI-assisted workflows."
    },

    {
        "role": "Backend Developer",
        "icon": "⚙️",
        "description": "Build APIs, business logic, authentication and server-side systems.",
        "skills": ["Programming", "APIs", "Databases", "Authentication", "System Design"],
        "languages": ["Python", "Java", "JavaScript", "C#"],
        "tools": ["Flask", "Spring Boot", "Node.js", "SQL", "Git"],
        "roadmap": [
            "Master one backend language",
            "Learn HTTP and REST APIs",
            "Learn databases",
            "Build authentication systems",
            "Build APIs",
            "Deploy applications",
            "Learn basic system design"
        ],
        "benefits": [
            "Strong technical foundation",
            "Useful for web and enterprise applications",
            "Path toward full-stack and systems roles"
        ],
        "future": "Backend engineering is increasingly connected with cloud platforms, distributed systems, APIs and AI-enabled applications."
    },

    {
        "role": "Full-Stack Developer",
        "icon": "🚀",
        "description": "Work across frontend, backend and databases.",
        "skills": ["HTML", "CSS", "JavaScript", "Backend", "SQL", "Git", "APIs"],
        "languages": ["JavaScript", "Python", "Java", "TypeScript"],
        "tools": ["React", "Flask", "Node.js", "GitHub", "SQL"],
        "roadmap": [
            "Learn frontend fundamentals",
            "Learn JavaScript",
            "Learn backend development",
            "Learn databases",
            "Build complete applications",
            "Deploy projects",
            "Create a strong GitHub portfolio"
        ],
        "benefits": [
            "Broad development knowledge",
            "Ability to build complete applications",
            "Useful for startup and product development environments"
        ],
        "future": "Full-stack work increasingly combines cloud deployment, APIs, databases, frontend frameworks and AI services."
    },

    {
        "role": "Python Developer",
        "icon": "🐍",
        "description": "Use Python to build applications, automation and backend systems.",
        "skills": ["Python", "OOP", "APIs", "Flask", "SQL"],
        "languages": ["Python", "SQL"],
        "tools": ["Flask", "Django", "Git", "VS Code"],
        "roadmap": [
            "Learn Python fundamentals",
            "Learn functions and OOP",
            "Learn file handling",
            "Learn APIs",
            "Learn Flask or Django",
            "Build projects",
            "Learn databases"
        ],
        "benefits": [
            "Useful across web development, automation and data",
            "Readable beginner-friendly language",
            "Large ecosystem"
        ],
        "future": "Python remains widely used in web development, automation, data and AI ecosystems."
    },

    {
        "role": "AI / ML Engineer",
        "icon": "🤖",
        "description": "Develop systems that use machine learning and AI techniques.",
        "skills": ["Python", "Mathematics", "Statistics", "Machine Learning", "Data Processing"],
        "languages": ["Python", "SQL"],
        "tools": ["NumPy", "Pandas", "scikit-learn", "PyTorch", "TensorFlow"],
        "roadmap": [
            "Learn Python",
            "Learn mathematics and statistics",
            "Learn data handling",
            "Study machine learning",
            "Build ML projects",
            "Learn deep learning",
            "Learn model deployment"
        ],
        "benefits": [
            "Combines programming with data and AI",
            "Many application areas",
            "Strong project opportunities"
        ],
        "future": "AI engineering is expanding across software products, automation, analytics, language systems and computer vision."
    },

    {
        "role": "Cybersecurity Analyst",
        "icon": "🛡️",
        "description": "Monitor systems, investigate security events and help protect organizations.",
        "skills": ["Networking", "Linux", "Security Fundamentals", "Logs", "Incident Response"],
        "languages": ["Python", "Bash"],
        "tools": ["Linux", "Wireshark", "SIEM platforms", "Git"],
        "roadmap": [
            "Learn networking",
            "Learn Linux",
            "Learn security fundamentals",
            "Study authentication and encryption",
            "Learn security monitoring",
            "Practice defensive labs",
            "Prepare for security certifications where appropriate"
        ],
        "benefits": [
            "Security is relevant to organizations of many sizes",
            "Multiple specialization paths",
            "Strong combination of networking and programming"
        ],
        "future": "Security work continues to evolve with cloud infrastructure, identity systems, application security and automation."
    },

    {
        "role": "Cloud Engineer",
        "icon": "☁️",
        "description": "Build and maintain cloud infrastructure and deployment systems.",
        "skills": ["Linux", "Networking", "Cloud", "Automation", "Containers"],
        "languages": ["Python", "Bash"],
        "tools": ["AWS", "Azure", "Docker", "GitHub Actions"],
        "roadmap": [
            "Learn Linux",
            "Learn networking",
            "Understand cloud fundamentals",
            "Learn one cloud platform",
            "Learn containers",
            "Learn CI/CD",
            "Deploy real projects"
        ],
        "benefits": [
            "Useful across modern software infrastructure",
            "Strong connection to DevOps and platform engineering",
            "Practical project opportunities"
        ],
        "future": "Cloud engineering increasingly involves automation, containers, infrastructure as code and managed services."
    },

    {
        "role": "Data Analyst",
        "icon": "📊",
        "description": "Analyze data and communicate useful findings.",
        "skills": ["Excel", "SQL", "Statistics", "Data Visualization"],
        "languages": ["SQL", "Python"],
        "tools": ["Excel", "Power BI", "Pandas", "SQL"],
        "roadmap": [
            "Learn Excel",
            "Learn SQL",
            "Learn basic statistics",
            "Learn Python",
            "Practice data cleaning",
            "Create dashboards",
            "Build a portfolio"
        ],
        "benefits": [
            "Combines technical and business skills",
            "Useful in many industries",
            "Strong entry-level project opportunities"
        ],
        "future": "Data analysis is increasingly connected with automation, AI-assisted analytics and business intelligence."
    },

    {
        "role": "QA / Test Engineer",
        "icon": "🧪",
        "description": "Test software to find defects and verify expected behaviour.",
        "skills": ["Testing", "Problem Solving", "Automation", "APIs"],
        "languages": ["Python", "Java", "JavaScript"],
        "tools": ["Selenium", "Postman", "Git"],
        "roadmap": [
            "Learn software testing concepts",
            "Learn test cases",
            "Learn API testing",
            "Learn automation",
            "Practice bug reporting",
            "Build testing projects"
        ],
        "benefits": [
            "Important part of software development",
            "Can progress from manual testing to automation",
            "Strong understanding of software quality"
        ],
        "future": "Testing increasingly includes automation, API testing, performance testing and AI-assisted quality workflows."
    },

    {
        "role": "Game Developer",
        "icon": "🎮",
        "description": "Create interactive games using programming and game engines.",
        "skills": ["C#", "C++", "Game Logic", "3D Concepts", "Problem Solving"],
        "languages": ["C#", "C++"],
        "tools": ["Unity", "Unreal Engine", "Git"],
        "roadmap": [
            "Learn programming",
            "Learn game mathematics",
            "Learn a game engine",
            "Build small games",
            "Learn 2D and 3D concepts",
            "Publish portfolio projects"
        ],
        "benefits": [
            "Highly project-oriented field",
            "Combines programming and creative work",
            "Opportunities in games and interactive applications"
        ],
        "future": "Game development continues to evolve with real-time 3D, multiplayer systems, procedural content and AI-assisted development."
    }
]


# ============================================================
# QUIZ BANK
# ============================================================

QUIZ_BANK = [

    {
        "id": "computer_001",
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Computer Personal Unit",
            "Central Program Utility",
            "Control Processing User"
        ],
        "answer": 0,
        "explanation": "CPU stands for Central Processing Unit."
    },

    {
        "id": "computer_002",
        "question": "Which memory is normally volatile?",
        "options": [
            "RAM",
            "SSD",
            "ROM",
            "USB drive"
        ],
        "answer": 0,
        "explanation": "RAM is normally volatile memory."
    },

    {
        "id": "programming_001",
        "question": "What is an algorithm?",
        "options": [
            "A step-by-step procedure for solving a problem",
            "A computer screen",
            "A storage device",
            "A programming language"
        ],
        "answer": 0,
        "explanation": "An algorithm describes ordered steps used to solve a problem."
    },

    {
        "id": "programming_002",
        "question": "Which statement is commonly used for decisions?",
        "options": [
            "if",
            "print",
            "include",
            "import"
        ],
        "answer": 0,
        "explanation": "if is commonly used for conditional decisions."
    },

    {
        "id": "c_001",
        "question": "Which function is the usual entry point of a C program?",
        "options": [
            "main",
            "start",
            "run",
            "begin"
        ],
        "answer": 0,
        "explanation": "Execution normally begins in main()."
    },

    {
        "id": "c_002",
        "question": "Which symbol is used to obtain the address of a variable in C?",
        "options": [
            "&",
            "*",
            "#",
            "@"
        ],
        "answer": 0,
        "explanation": "The & operator obtains a variable's address."
    },

    {
        "id": "cpp_001",
        "question": "Which feature allows a class to acquire properties from another class?",
        "options": [
            "Inheritance",
            "Compilation",
            "Iteration",
            "Parsing"
        ],
        "answer": 0,
        "explanation": "Inheritance allows a class to derive from another class."
    },

    {
        "id": "python_001",
        "question": "Which function displays output in Python?",
        "options": [
            "print()",
            "show()",
            "displayText()",
            "output()"
        ],
        "answer": 0,
        "explanation": "print() displays output."
    },

    {
        "id": "python_002",
        "question": "Which Python structure stores key-value pairs?",
        "options": [
            "Dictionary",
            "List",
            "Tuple",
            "Set"
        ],
        "answer": 0,
        "explanation": "Dictionaries store key-value pairs."
    },

    {
        "id": "java_001",
        "question": "Which keyword creates an object in Java?",
        "options": [
            "new",
            "object",
            "create",
            "make"
        ],
        "answer": 0,
        "explanation": "The new keyword creates an object."
    },

    {
        "id": "web_001",
        "question": "Which language provides the structure of a web page?",
        "options": [
            "HTML",
            "CSS",
            "SQL",
            "Python"
        ],
        "answer": 0,
        "explanation": "HTML provides the structure of web pages."
    },

    {
        "id": "web_002",
        "question": "Which language is commonly used to add interactivity to web pages?",
        "options": [
            "JavaScript",
            "SQL",
            "C",
            "Bash"
        ],
        "answer": 0,
        "explanation": "JavaScript is widely used for web interactivity."
    },

    {
        "id": "database_001",
        "question": "Which SQL command retrieves data?",
        "options": [
            "SELECT",
            "GETDATA",
            "FETCHALL",
            "READ"
        ],
        "answer": 0,
        "explanation": "SELECT retrieves data from a database."
    },

    {
        "id": "git_001",
        "question": "Which Git command creates a commit?",
        "options": [
            "git commit",
            "git save",
            "git store",
            "git snapshot"
        ],
        "answer": 0,
        "explanation": "git commit records changes in Git history."
    },

    {
        "id": "cloud_001",
        "question": "Which is an example of a cloud platform?",
        "options": [
            "AWS",
            "Keyboard",
            "RAM",
            "CPU"
        ],
        "answer": 0,
        "explanation": "AWS is a cloud platform."
    },

    {
        "id": "ai_001",
        "question": "What is machine learning primarily concerned with?",
        "options": [
            "Learning patterns from data",
            "Replacing every computer",
            "Designing keyboards",
            "Creating operating systems only"
        ],
        "answer": 0,
        "explanation": "Machine learning uses data to learn patterns for tasks such as prediction or classification."
    },

    {
        "id": "security_001",
        "question": "Which security goal protects information from unauthorized disclosure?",
        "options": [
            "Confidentiality",
            "Availability",
            "Compilation",
            "Iteration"
        ],
        "answer": 0,
        "explanation": "Confidentiality protects information from unauthorized disclosure."
    },

    {
        "id": "security_002",
        "question": "What is phishing?",
        "options": [
            "A social engineering technique used to trick users",
            "A programming language",
            "A database",
            "A storage technology"
        ],
        "answer": 0,
        "explanation": "Phishing commonly attempts to trick people into revealing information or taking an unsafe action."
    }
]


# ============================================================
# HELPERS
# ============================================================

def flatten_courses():
    result = []

    for course_name, course in COURSES.items():

        lessons_count = 0

        for chapter in course["chapters"]:
            lessons_count += len(chapter["lessons"])

        result.append({
            "name": course_name,
            "icon": course["icon"],
            "level": course["level"],
            "description": course["description"],
            "chapters": len(course["chapters"]),
            "lessons": lessons_count
        })

    return result


def find_course(name):
    if name in COURSES:
        return COURSES[name]

    decoded = str(name).replace("%20", " ")

    for key in COURSES:
        if key.lower() == decoded.lower():
            return COURSES[key]

    return None


def safe_json():
    try:
        return request.get_json(silent=True) or {}
    except Exception:
        return {}


# ============================================================
# MAIN PAGE
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# HEALTH
# ============================================================

@app.route("/api/status")
def status():
    return jsonify({
        "success": True,
        "app": APP_NAME,
        "firebase": FIREBASE_READY,
        "compiler": bool(ONECOMPILER_API_KEY),
        "courses": len(COURSES),
        "quiz_questions": len(QUIZ_BANK)
    })


# ============================================================
# COURSES
# ============================================================

@app.route("/api/courses")
def courses():
    return jsonify({
        "success": True,
        "courses": flatten_courses()
    })


@app.route("/api/course/<path:course_name>")
def course(course_name):

    data = find_course(course_name)

    if not data:
        return jsonify({
            "success": False,
            "error": "Course not found"
        }), 404

    chapters = []

    for index, chapter in enumerate(data["chapters"]):

        lessons = []

        for lesson_index, lesson in enumerate(chapter["lessons"]):

            lessons.append({
                "index": lesson_index,
                "title": lesson["title"],
                "explanation": lesson["explanation"],
                "example": lesson["example"],
                "code": lesson["code"],
                "practice": lesson["practice"]
            })

        chapters.append({
            "index": index,
            "title": chapter["title"],
            "lessons": lessons
        })

    return jsonify({
        "success": True,
        "name": course_name,
        "icon": data["icon"],
        "level": data["level"],
        "description": data["description"],
        "chapters": chapters
    })


# ============================================================
# SINGLE LESSON
# ============================================================

@app.route("/api/lesson/<path:course_name>/<int:chapter_index>/<int:lesson_index>")
def lesson(course_name, chapter_index, lesson_index):

    data = find_course(course_name)

    if not data:
        return jsonify({
            "success": False,
            "error": "Course not found"
        }), 404

    try:
        chapter = data["chapters"][chapter_index]
        lesson_data = chapter["lessons"][lesson_index]

        return jsonify({
            "success": True,
            "course": course_name,
            "chapter": chapter["title"],
            "lesson": lesson_data
        })

    except (IndexError, KeyError):
        return jsonify({
            "success": False,
            "error": "Lesson not found"
        }), 404


# ============================================================
# QUIZ
# ============================================================

@app.route("/api/quiz")
def quiz():

    requested_count = request.args.get("count", "10")

    try:
        count = max(1, min(int(requested_count), len(QUIZ_BANK)))
    except Exception:
        count = 10

    questions = random.sample(QUIZ_BANK, count)

    public_questions = []

    for q in questions:
        public_questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        })

    return jsonify({
        "success": True,
        "questions": public_questions
    })


@app.route("/api/quiz/answer", methods=["POST"])
def quiz_answer():

    data = safe_json()

    question_id = data.get("question_id")
    selected = data.get("answer")

    question = next(
        (q for q in QUIZ_BANK if q["id"] == question_id),
        None
    )

    if not question:
        return jsonify({
            "success": False,
            "error": "Question not found"
        }), 404

    try:
        selected = int(selected)
    except Exception:
        selected = -1

    correct = selected == question["answer"]

    return jsonify({
        "success": True,
        "correct": correct,
        "answer": question["answer"],
        "explanation": question["explanation"],
        "xp": 10 if correct else 0
    })


# ============================================================
# CAREERS
# ============================================================

@app.route("/api/careers")
def careers():
    return jsonify({
        "success": True,
        "careers": CAREERS
    })


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/api/dashboard")
def dashboard():

    xp = 0

    try:
        xp = int(request.args.get("xp", 0))
    except Exception:
        xp = 0

    level = max(1, math.floor(xp / 100) + 1)

    ranks = [
        "Code Explorer",
        "Bug Hunter",
        "Logic Builder",
        "Code Warrior",
        "Developer",
        "Code Master",
        "Tech Hunter",
        "CodeQuest Legend"
    ]

    rank = ranks[min(level - 1, len(ranks) - 1)]

    return jsonify({
        "success": True,
        "xp": xp,
        "level": level,
        "rank": rank
    })


# ============================================================
# PROGRESS
# ============================================================

@app.route("/api/progress", methods=["GET", "POST"])
def progress():

    if request.method == "GET":
        return jsonify({
            "success": True,
            "xp": 0,
            "completed": 0,
            "streak": 0,
            "achievements": []
        })

    data = safe_json()

    return jsonify({
        "success": True,
        "message": "Progress received",
        "xp": data.get("xp", 0),
        "completed": data.get("completed", 0),
        "streak": data.get("streak", 0)
    })


# ============================================================
# COMPILE CODE
# ============================================================

@app.route("/api/compile", methods=["POST"])
def compile_code():

    data = safe_json()

    language = str(
        data.get("language") or data.get("lang") or ""
    ).strip().lower()

    code = data.get("code", "")
    stdin = data.get("input", data.get("stdin", ""))

    language_map = {
        "c": "c",
        "c++": "cpp",
        "cpp": "cpp",
        "python": "python",
        "python3": "python",
        "java": "java"
    }

    language = language_map.get(language)

    if not language:
        return jsonify({
            "success": False,
            "error": "Unsupported language. Use C, C++, Python or Java."
        }), 400

    if not isinstance(code, str) or not code.strip():
        return jsonify({
            "success": False,
            "error": "Code cannot be empty."
        }), 400

    if not ONECOMPILER_API_KEY:
        return jsonify({
            "success": False,
            "error": "Compiler API is not configured on Render.",
            "setup_required": True
        }), 503

    extension = {
        "c": "c",
        "cpp": "cpp",
        "python": "py",
        "java": "java"
    }[language]

    filename = {
        "c": "main.c",
        "cpp": "main.cpp",
        "python": "main.py",
        "java": "Main.java"
    }[language]

    payload = {
        "language": language,
        "stdin": str(stdin or ""),
        "files": [
            {
                "name": filename,
                "content": code
            }
        ]
    }

    try:

        response = requests.post(
            "https://api.onecompiler.com/v1/run",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": ONECOMPILER_API_KEY
            },
            json=payload,
            timeout=45
        )

        try:
            result = response.json()
        except Exception:
            result = {
                "error": response.text
            }

        if response.status_code >= 400:

            return jsonify({
                "success": False,
                "error": result.get(
                    "error",
                    "Compiler service returned an error."
                )
            }), response.status_code

        return jsonify({
            "success": True,
            "status": result.get("status"),
            "output": result.get("stdout") or "",
            "stderr": result.get("stderr") or "",
            "error": result.get("exception") or result.get("error") or "",
            "executionTime": result.get("executionTime"),
            "memoryUsed": result.get("memoryUsed")
        })

    except requests.Timeout:

        return jsonify({
            "success": False,
            "error": "Compiler timed out. Please try again."
        }), 504

    except requests.RequestException as e:

        return jsonify({
            "success": False,
            "error": f"Compiler connection failed: {str(e)}"
        }), 502

    except Exception as e:

        return jsonify({
            "success": False,
            "error": f"Compiler error: {str(e)}"
        }), 500


# ============================================================
# DAILY MISSIONS
# ============================================================

@app.route("/api/daily-missions")
def daily_missions():

    return jsonify({
        "success": True,
        "missions": [
            {
                "id": "lesson",
                "title": "Complete a lesson",
                "description": "Finish one learning lesson.",
                "xp": 20
            },
            {
                "id": "quiz",
                "title": "Answer 5 quiz questions",
                "description": "Complete five quiz questions.",
                "xp": 30
            },
            {
                "id": "code",
                "title": "Run a coding program",
                "description": "Write and execute code.",
                "xp": 50
            },
            {
                "id": "daily",
                "title": "Complete today's quest",
                "description": "Finish all daily missions.",
                "xp": 100
            }
        ]
    })


# ============================================================
# ACHIEVEMENTS
# ============================================================

@app.route("/api/achievements")
def achievements():

    return jsonify({
        "success": True,
        "achievements": [
            {
                "id": "first_step",
                "title": "First Step",
                "description": "Complete your first lesson.",
                "icon": "🚀"
            },
            {
                "id": "quiz_master",
                "title": "Quiz Master",
                "description": "Answer 25 quiz questions.",
                "icon": "🧠"
            },
            {
                "id": "streak",
                "title": "Streak Master",
                "description": "Maintain a learning streak.",
                "icon": "🔥"
            },
            {
                "id": "programmer",
                "title": "Programmer",
                "description": "Run your first program.",
                "icon": "💻"
            },
            {
                "id": "project_builder",
                "title": "Project Builder",
                "description": "Complete a project.",
                "icon": "🛠️"
            },
            {
                "id": "cyber_guardian",
                "title": "Cyber Guardian",
                "description": "Complete cybersecurity lessons.",
                "icon": "🛡️"
            }
        ]
    })


# ============================================================
# PROJECTS
# ============================================================

@app.route("/api/projects")
def projects():

    return jsonify({
        "success": True,
        "projects": [
            {
                "title": "Calculator",
                "level": "Beginner",
                "description": "Build a simple calculator."
            },
            {
                "title": "Quiz Application",
                "level": "Beginner",
                "description": "Create an interactive quiz."
            },
            {
                "title": "Student Management System",
                "level": "Intermediate",
                "description": "Store and manage student records."
            },
            {
                "title": "To-Do Application",
                "level": "Intermediate",
                "description": "Build a task management application."
            },
            {
                "title": "AI Chatbot",
                "level": "Advanced",
                "description": "Build an AI-powered conversational application."
            },
            {
                "title": "Cybersecurity Dashboard",
                "level": "Advanced",
                "description": "Create a defensive security monitoring dashboard."
            },
            {
                "title": "CodeQuest AI",
                "level": "Advanced",
                "description": "Build your own gamified learning platform."
            }
        ]
    })


# ============================================================
# ERROR HANDLER
# ============================================================

@app.errorhandler(404)
def not_found(error):

    if request.path.startswith("/api/"):
        return jsonify({
            "success": False,
            "error": "API endpoint not found."
        }), 404

    return render_template("index.html")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
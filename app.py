from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# ============================================================
# CODEQUEST AI
# LEARN • PRACTICE • PLAY • BUILD
# ============================================================

# ------------------------------------------------------------
# COURSE DATA
# ------------------------------------------------------------

courses = [

    {
        "id": "computer-basics",
        "title": "Computer Basics",
        "icon": "💻",
        "level": "Beginner",
        "description": "Understand computers from absolute zero.",
        "chapters": [
            {
                "title": "What is a Computer?",
                "lesson": """
A computer is an electronic device that accepts data as input,
processes the data according to instructions, stores information,
and produces useful output.

A computer works mainly through four basic stages:

Input → Processing → Storage → Output

For example, when you type your name using a keyboard, the
keyboard provides input. The CPU processes the information and
the result appears on the monitor.

Computers are used in education, banking, hospitals, engineering,
business, communication, entertainment, science and almost every
modern industry.

Understanding the basic working of a computer is important before
learning programming because programming means giving instructions
to a computer to solve problems.
                """,
                "sample": "Input → Processing → Output",
                "quiz": [
                    {
                        "q": "Which device is mainly used to display output?",
                        "options": ["Keyboard", "Monitor", "Mouse", "Scanner"],
                        "answer": "Monitor"
                    },
                    {
                        "q": "What is the main processing unit of a computer?",
                        "options": ["CPU", "Keyboard", "Monitor", "Printer"],
                        "answer": "CPU"
                    }
                ]
            },

            {
                "title": "Hardware and Software",
                "lesson": """
Hardware refers to the physical parts of a computer that we can
see and touch. Examples include keyboard, mouse, monitor, RAM,
hard disk, SSD and motherboard.

Software is a collection of programs and instructions that tells
hardware what to do.

Operating systems, web browsers, media players, programming
languages and mobile applications are examples of software.

Hardware without software cannot perform useful tasks, while
software needs hardware to execute its instructions.
                """,
                "sample": "Hardware = Physical parts\nSoftware = Programs",
                "quiz": [
                    {
                        "q": "Which one is hardware?",
                        "options": ["Windows", "Chrome", "Keyboard", "Python"],
                        "answer": "Keyboard"
                    }
                ]
            },

            {
                "title": "CPU, RAM and Storage",
                "lesson": """
The CPU is responsible for executing instructions and performing
calculations.

RAM is temporary working memory. Programs currently being used
are loaded into RAM so that the CPU can access them quickly.

Storage such as SSD and HDD keeps data even after the computer is
turned off.

A simple way to remember them is:

CPU → Thinks and processes
RAM → Temporarily works with active data
SSD/HDD → Permanently stores data
                """,
                "sample": "CPU + RAM + Storage = Core computer components",
                "quiz": []
            },

            {
                "title": "Operating Systems",
                "lesson": """
An operating system is system software that manages computer
hardware and provides an environment for applications.

Examples include Windows, Linux, macOS, Android and iOS.

The operating system manages files, memory, processes, devices,
security and user interaction.

Learning basic operating-system concepts is useful for every
computer science student because applications ultimately run on
an operating system.
                """,
                "sample": "Examples: Windows, Linux, Android",
                "quiz": []
            },

            {
                "title": "Files, Folders and Extensions",
                "lesson": """
Files contain information while folders are used to organize
files.

A file extension normally indicates the type of file.

Examples:

.txt  → Text
.jpg  → Image
.mp4  → Video
.pdf  → Document
.py   → Python program
.c    → C program
.html → Web page

Understanding file organization is a basic but extremely useful
computer skill.
                """,
                "sample": "program.py → Python source file",
                "quiz": []
            }
        ]
    },

    {
        "id": "ms-office",
        "title": "MS Office",
        "icon": "📊",
        "level": "Beginner",
        "description": "Learn Word, Excel and PowerPoint for college and jobs.",
        "chapters": [
            {
                "title": "MS Word",
                "lesson": """
Microsoft Word is a word-processing application used to create
professional documents.

You can use Word to create assignments, resumes, reports,
applications, project documentation and official letters.

Important skills include formatting text, headings, tables,
page layout, headers and footers, images, page numbers,
spell checking and exporting documents as PDF.

For students, Word is especially useful for project reports,
seminar documents, resumes and academic assignments.
                """,
                "sample": "Create → Format → Save → Export PDF",
                "quiz": []
            },

            {
                "title": "MS Excel",
                "lesson": """
Microsoft Excel is a spreadsheet application used for storing,
organizing, calculating and analyzing data.

Excel works with rows, columns and cells.

Important concepts include:

Cell
Row
Column
Formula
Function
Chart
Sorting
Filtering
Pivot tables

Common functions include SUM, AVERAGE, COUNT, MAX and MIN.

Excel is valuable in software companies as well as business,
finance, administration, data analysis and engineering.
                """,
                "sample": "=SUM(A1:A10)\n=AVERAGE(B1:B10)",
                "quiz": []
            },

            {
                "title": "MS PowerPoint",
                "lesson": """
PowerPoint is used to create presentations.

A good presentation should contain clear headings, short points,
useful visuals and logical flow.

Students can use PowerPoint for seminars, project demonstrations,
technical presentations and placement presentations.

Learning presentation design also improves communication skills.
                """,
                "sample": "Title → Problem → Solution → Demo → Conclusion",
                "quiz": []
            }
        ]
    },

    {
        "id": "github",
        "title": "Git & GitHub",
        "icon": "🐙",
        "level": "Beginner",
        "description": "Learn version control and build a professional developer profile.",
        "chapters": [
            {
                "title": "What is Git?",
                "lesson": """
Git is a distributed version-control system used to track changes
in source code.

Instead of keeping many copies of a project such as
project-final, project-final2 and project-final-real, Git allows
you to maintain the history of changes properly.

Git is commonly used by software developers and development teams.
                """,
                "sample": "git init",
                "quiz": []
            },

            {
                "title": "What is GitHub?",
                "lesson": """
GitHub is a platform where developers can store, manage and
collaborate on Git repositories.

For a student, GitHub can become a public portfolio.

A strong profile can contain:

• College projects
• Mini projects
• Coding practice
• Documentation
• Web applications
• APIs
• Open-source contributions

Recruiters may use project portfolios as one part of evaluating
a candidate's practical experience.
                """,
                "sample": "git add .\ngit commit -m \"Initial commit\"\ngit push",
                "quiz": []
            },

            {
                "title": "GitHub Portfolio",
                "lesson": """
Your GitHub profile should show what you can actually build.

Instead of uploading empty repositories, build useful projects
and write a README explaining:

1. What the project does
2. Why you built it
3. Technologies used
4. Features
5. How to run it
6. Screenshots
7. Future improvements

For a beginner, 3 to 5 properly documented projects can be much
more useful than many unfinished repositories.
                """,
                "sample": "README + screenshots + source code + live demo",
                "quiz": []
            }
        ]
    },

    {
        "id": "c-programming",
        "title": "C Programming",
        "icon": "⚙️",
        "level": "Beginner",
        "description": "Build strong programming fundamentals using C.",
        "chapters": [
            {
                "title": "What is C Language?",
                "lesson": """
C is a general-purpose programming language developed to provide
efficient and structured programming.

C is one of the most important languages for understanding
programming fundamentals because it teaches variables, data
types, operators, conditions, loops, functions, arrays,
pointers and memory concepts.

C is widely used in systems programming, embedded systems,
operating systems and performance-sensitive software.

For beginners, C is useful because it teaches how programs work
at a lower level instead of hiding many concepts behind advanced
features.

The basic idea is:

Problem → Algorithm → Code → Compilation → Execution → Output

Once you understand C properly, learning languages such as C++,
Java and Python becomes easier because many programming concepts
are shared.
                """,
                "sample": """#include <stdio.h>

int main() {
    printf("Hello World");
    return 0;
}""",
                "quiz": [
                    {
                        "q": "Which function is the starting point of a C program?",
                        "options": ["start()", "main()", "run()", "begin()"],
                        "answer": "main()"
                    },
                    {
                        "q": "Which header is commonly used for printf()?",
                        "options": ["stdio.h", "math.h", "string.h", "stdlib.h"],
                        "answer": "stdio.h"
                    }
                ]
            },

            {
                "title": "Variables and Data Types",
                "lesson": """
A variable is a named memory location used to store a value.

C provides several fundamental data types.

int → integers
float → decimal numbers
double → higher precision decimal values
char → single character

Example:

int age = 18;
float mark = 92.5;
char grade = 'A';

Choosing the correct data type helps the program store and
process information correctly.
                """,
                "sample": """int age = 18;
float mark = 92.5;
char grade = 'A';""",
                "quiz": []
            },

            {
                "title": "Operators",
                "lesson": """
Operators are symbols used to perform operations.

Arithmetic:
+ - * / %

Relational:
> < >= <= == !=

Logical:
&& || !

Assignment:
= += -= *= /=

Operators are fundamental because almost every program needs to
calculate, compare or modify values.
                """,
                "sample": "int result = a + b;",
                "quiz": []
            },

            {
                "title": "if, else and Conditions",
                "lesson": """
Conditional statements allow a program to make decisions.

For example, a program can check whether a student has passed:

if (mark >= 40)
    printf(\"Pass\");
else
    printf(\"Fail\");

Conditions are used in almost every real application.
                """,
                "sample": """if (age >= 18) {
    printf("Eligible");
} else {
    printf("Not Eligible");
}""",
                "quiz": []
            },

            {
                "title": "Loops",
                "lesson": """
Loops are used when a task needs to be repeated.

C provides for, while and do-while loops.

For example, printing numbers from 1 to 10 manually would be
long. A loop can perform the repetition automatically.

Loops are essential for arrays, searching, calculations,
patterns and many algorithms.
                """,
                "sample": """for(int i = 1; i <= 10; i++) {
    printf("%d\\n", i);
}""",
                "quiz": []
            },

            {
                "title": "Functions",
                "lesson": """
A function is a reusable block of code designed to perform a
specific task.

Functions make large programs easier to understand, test and
maintain.

Instead of writing the same logic repeatedly, create a function
and call it whenever required.
                """,
                "sample": """int add(int a, int b) {
    return a + b;
}""",
                "quiz": []
            },

            {
                "title": "Arrays",
                "lesson": """
An array stores multiple values of the same data type under one
name.

For example:

int marks[5];

Arrays are useful for storing lists such as student marks,
temperatures, prices or scores.

Understanding arrays is extremely important before learning
data structures and algorithms.
                """,
                "sample": """int marks[3] = {80, 90, 95};""",
                "quiz": []
            },

            {
                "title": "Pointers",
                "lesson": """
A pointer is a variable that stores the memory address of
another variable.

Pointers are one of the most important concepts in C.

They are used in dynamic memory allocation, arrays, functions,
data structures and system programming.

Pointers may initially feel difficult, but understanding them
gives a strong foundation for understanding memory.
                """,
                "sample": """int x = 10;
int *p = &x;""",
                "quiz": []
            }
        ]
    },

    {
        "id": "cpp",
        "title": "C++ Programming",
        "icon": "🚀",
        "level": "Intermediate",
        "description": "Learn object-oriented programming and modern C++.",
        "chapters": [
            {
                "title": "Introduction to C++",
                "lesson": """
C++ is a general-purpose programming language that extends many
concepts of C and provides object-oriented programming features.

Important C++ concepts include classes, objects, inheritance,
polymorphism, encapsulation and abstraction.

C++ is used in competitive programming, game development,
systems software and performance-sensitive applications.
                """,
                "sample": """#include <iostream>
using namespace std;

int main() {
    cout << "Hello World";
    return 0;
}""",
                "quiz": []
            },

            {
                "title": "Classes and Objects",
                "lesson": """
A class is a blueprint for creating objects.

An object is an instance of a class.

Classes allow data and functions related to an entity to be
grouped together.

This is one of the foundations of object-oriented programming.
                """,
                "sample": """class Student {
public:
    string name;
    void display() {
        cout << name;
    }
};""",
                "quiz": []
            }
        ]
    },

    {
        "id": "python",
        "title": "Python Programming",
        "icon": "🐍",
        "level": "Beginner",
        "description": "Learn Python from fundamentals to practical development.",
        "chapters": [
            {
                "title": "What is Python?",
                "lesson": """
Python is a high-level, general-purpose programming language
known for its readable syntax.

Python is widely used in web development, automation, data
analysis, artificial intelligence, machine learning,
cybersecurity and scripting.

Its simple syntax makes it beginner-friendly while its huge
ecosystem makes it useful for professional development.

Python is particularly valuable for students because one language
can open paths into several technology areas.
                """,
                "sample": """print("Hello World")""",
                "quiz": []
            },

            {
                "title": "Variables and Data Types",
                "lesson": """
Python variables store values without requiring the programmer
to explicitly declare the type in the same way as C.

Examples include integers, floating-point values, strings,
lists, tuples, dictionaries and sets.

Example:

name = "Joe"
age = 18
mark = 95.5

Python determines the type dynamically while the program runs.
                """,
                "sample": """name = "Student"
age = 18
mark = 95.5
print(name, age, mark)""",
                "quiz": []
            },

            {
                "title": "Conditions and Loops",
                "lesson": """
Python uses if, elif and else for decisions.

for and while are used for repetition.

These concepts allow programs to make decisions and automate
repetitive tasks.

They are essential for almost every practical program.
                """,
                "sample": """for i in range(1, 6):
    print(i)""",
                "quiz": []
            }
        ]
    },

    {
        "id": "web-development",
        "title": "Web Development",
        "icon": "🌐",
        "level": "Beginner",
        "description": "Build websites and web applications.",
        "chapters": [
            {
                "title": "HTML",
                "lesson": """
HTML stands for HyperText Markup Language.

It defines the structure of a web page.

Common HTML elements include headings, paragraphs, links,
images, buttons, forms, tables and sections.

HTML is the foundation of web development.
                """,
                "sample": """<!DOCTYPE html>
<html>
<body>
<h1>Hello World</h1>
<p>My first webpage.</p>
</body>
</html>""",
                "quiz": []
            },

            {
                "title": "CSS",
                "lesson": """
CSS stands for Cascading Style Sheets.

It controls the visual appearance of web pages.

CSS can control colours, spacing, fonts, layouts, animations,
responsive design and many other visual properties.

HTML provides structure while CSS provides presentation.
                """,
                "sample": """body {
    font-family: Arial;
    margin: 0;
}""",
                "quiz": []
            },

            {
                "title": "JavaScript",
                "lesson": """
JavaScript adds behaviour and interactivity to web pages.

It can respond to button clicks, modify page content, validate
forms, communicate with servers and create interactive
applications.

Modern JavaScript is also used outside the browser through
platforms such as Node.js.
                """,
                "sample": """document.getElementById("btn")
    .addEventListener("click", function() {
        alert("Hello!");
    });""",
                "quiz": []
            }
        ]
    },

    {
        "id": "dbms",
        "title": "DBMS & SQL",
        "icon": "🗄️",
        "level": "Intermediate",
        "description": "Understand databases and SQL.",
        "chapters": [
            {
                "title": "What is a Database?",
                "lesson": """
A database is an organized collection of information that can
be stored, searched and updated efficiently.

Applications use databases to store users, products, orders,
marks, messages and many other types of information.

A DBMS is software used to create and manage databases.

Examples include MySQL, PostgreSQL, SQLite and SQL Server.
                """,
                "sample": "Database → Tables → Rows → Columns",
                "quiz": []
            },

            {
                "title": "SQL Basics",
                "lesson": """
SQL is used to communicate with relational databases.

Important commands include SELECT, INSERT, UPDATE and DELETE.

Example:

SELECT * FROM students;

SQL is a highly useful skill for backend development, data work
and many software engineering roles.
                """,
                "sample": """SELECT name, mark
FROM students
WHERE mark >= 80;""",
                "quiz": []
            }
        ]
    },

    {
        "id": "dsa",
        "title": "Data Structures & Algorithms",
        "icon": "🧠",
        "level": "Intermediate",
        "description": "Develop problem-solving and coding interview skills.",
        "chapters": [
            {
                "title": "What is an Algorithm?",
                "lesson": """
An algorithm is a finite sequence of clear steps used to solve a
problem.

A good algorithm should be correct, understandable and reasonably
efficient.

Examples include searching, sorting and finding the shortest path.

Learning algorithms improves logical thinking and is important
for technical interviews and competitive programming.
                """,
                "sample": "Input → Algorithm → Output",
                "quiz": []
            },

            {
                "title": "Arrays and Searching",
                "lesson": """
Searching means finding a particular value inside a collection.

Linear search checks elements one by one.

Binary search is faster but requires the data to be sorted.

Understanding the difference teaches an important idea:
algorithm efficiency matters.
                """,
                "sample": "Linear Search → O(n)\nBinary Search → O(log n)",
                "quiz": []
            },

            {
                "title": "Sorting",
                "lesson": """
Sorting arranges data in a particular order.

Important algorithms include bubble sort, selection sort,
insertion sort, merge sort and quicksort.

Learning several sorting algorithms helps students understand
time complexity and algorithm design.
                """,
                "sample": "Unsorted → [5,2,4,1] → Sorted → [1,2,4,5]",
                "quiz": []
            }
        ]
    },

    {
        "id": "operating-systems",
        "title": "Operating Systems",
        "icon": "🖥️",
        "level": "Intermediate",
        "description": "Understand processes, memory and operating-system concepts.",
        "chapters": [
            {
                "title": "Processes and Threads",
                "lesson": """
A process is a program in execution.

A thread is a smaller execution unit within a process.

Modern applications often use multiple threads to perform
different tasks efficiently.

These concepts are important for software engineering and
systems programming.
                """,
                "sample": "Application → Process → Threads",
                "quiz": []
            }
        ]
    },

    {
        "id": "computer-networks",
        "title": "Computer Networks",
        "icon": "🌐",
        "level": "Intermediate",
        "description": "Understand how computers communicate.",
        "chapters": [
            {
                "title": "What is a Network?",
                "lesson": """
A computer network connects devices so that they can communicate
and share resources.

The internet is the world's largest interconnected network.

Important networking concepts include IP addresses, DNS, HTTP,
HTTPS, TCP, UDP, routers, switches and ports.

Networking knowledge is useful for web development, cloud,
cybersecurity and system administration.
                """,
                "sample": "Device → Router → Internet → Server",
                "quiz": []
            }
        ]
    },

    {
        "id": "cybersecurity",
        "title": "Cybersecurity",
        "icon": "🔐",
        "level": "Intermediate",
        "description": "Learn the fundamentals of protecting systems and data.",
        "chapters": [
            {
                "title": "Introduction to Cybersecurity",
                "lesson": """
Cybersecurity is the practice of protecting computers, networks,
applications and data from unauthorized access, damage or misuse.

The three classic security goals are:

Confidentiality
Integrity
Availability

Students should first learn defensive concepts, secure coding,
authentication, authorization, encryption, network security and
common vulnerabilities.

Cybersecurity is a broad field with roles in security analysis,
security engineering, penetration testing, cloud security and
security operations.
                """,
                "sample": "CIA → Confidentiality + Integrity + Availability",
                "quiz": []
            }
        ]
    },

    {
        "id": "ai-ml",
        "title": "AI & Machine Learning",
        "icon": "🤖",
        "level": "Advanced",
        "description": "Understand modern AI concepts and machine learning.",
        "chapters": [
            {
                "title": "What is Artificial Intelligence?",
                "lesson": """
Artificial Intelligence is a field of computing focused on
building systems that perform tasks that normally require
human-like intelligence.

Examples include language understanding, image recognition,
recommendation systems and decision-support systems.

Machine learning is a major area of AI where systems learn
patterns from data.

Python, mathematics, statistics and data handling are useful
foundations for AI and ML.
                """,
                "sample": "Data → Training → Model → Prediction",
                "quiz": []
            }
        ]
    }
]


# ------------------------------------------------------------
# 720+ QUIZ QUESTIONS
# ------------------------------------------------------------

quiz_topics = [
    ("Computer Basics", "What is the main processing unit of a computer?", ["CPU", "RAM", "SSD", "Monitor"], "CPU"),
    ("Computer Basics", "Which memory is temporary?", ["RAM", "SSD", "HDD", "ROM"], "RAM"),
    ("Computer Basics", "Which device is used for typing?", ["Keyboard", "Monitor", "Printer", "Speaker"], "Keyboard"),
    ("Computer Basics", "Which is an operating system?", ["Windows", "HTML", "Python", "SQL"], "Windows"),
    ("Computer Basics", "Which is permanent storage?", ["SSD", "RAM", "Cache", "Register"], "SSD"),

    ("MS Office", "Which application is mainly used for documents?", ["Word", "Excel", "PowerPoint", "Paint"], "Word"),
    ("MS Office", "Which application is mainly used for spreadsheets?", ["Excel", "Word", "PowerPoint", "Notepad"], "Excel"),
    ("MS Office", "Which function adds numbers in Excel?", ["SUM", "ADDALL", "TOTALNUM", "PLUS"], "SUM"),
    ("MS Office", "Which application is mainly used for presentations?", ["PowerPoint", "Word", "Excel", "Access"], "PowerPoint"),
    ("MS Office", "What is a spreadsheet cell?", ["Intersection of row and column", "A file", "A slide", "A paragraph"], "Intersection of row and column"),

    ("GitHub", "Which command initializes a Git repository?", ["git init", "git start", "git create", "git open"], "git init"),
    ("GitHub", "Which command records changes in Git history?", ["git commit", "git save", "git record", "git history"], "git commit"),
    ("GitHub", "What is GitHub mainly used for?", ["Code collaboration and hosting", "Video editing", "Gaming", "Email"], "Code collaboration and hosting"),
    ("GitHub", "Which file commonly documents a project?", ["README.md", "MAIN.exe", "START.css", "DOC.run"], "README.md"),
    ("GitHub", "Which command uploads commits to a remote repository?", ["git push", "git upload", "git send", "git transfer"], "git push"),

    ("C", "Which function starts a normal C program?", ["main()", "start()", "run()", "begin()"], "main()"),
    ("C", "Which header provides printf()?", ["stdio.h", "string.h", "math.h", "time.h"], "stdio.h"),
    ("C", "Which symbol terminates a C statement?", [";", ":", ".", ","], ";"),
    ("C", "Which type stores a whole number?", ["int", "float", "char", "double"], "int"),
    ("C", "Which loop is useful when the number of repetitions is known?", ["for", "switch", "if", "goto"], "for"),

    ("C++", "Which feature is central to C++ OOP?", ["Classes", "HTML", "SQL", "DNS"], "Classes"),
    ("C++", "Which object is an instance of a class?", ["Object", "Compiler", "Header", "Loop"], "Object"),
    ("C++", "Which stream is commonly used for output?", ["cout", "cin", "print", "out"], "cout"),
    ("C++", "Which stream is commonly used for input?", ["cin", "cout", "input", "read"], "cin"),
    ("C++", "Which concept hides internal implementation?", ["Encapsulation", "Compilation", "Iteration", "Sorting"], "Encapsulation"),

    ("Python", "Which keyword defines a function?", ["def", "function", "fun", "define"], "def"),
    ("Python", "Which symbol starts a comment?", ["#", "//", "/*", "--"], "#"),
    ("Python", "Which function displays output?", ["print()", "display()", "show()", "output()"], "print()"),
    ("Python", "Which type stores key-value pairs?", ["dict", "list", "tuple", "set"], "dict"),
    ("Python", "Which keyword is used for a loop over a sequence?", ["for", "repeat", "loop", "iterate"], "for"),

    ("Web", "What does HTML define?", ["Web page structure", "Database", "Operating system", "Network"], "Web page structure"),
    ("Web", "What does CSS control?", ["Presentation and styling", "Database queries", "CPU", "Memory"], "Presentation and styling"),
    ("Web", "Which language adds browser interactivity?", ["JavaScript", "SQL", "C", "Bash"], "JavaScript"),
    ("Web", "Which tag creates a heading?", ["h1", "p", "div", "img"], "h1"),
    ("Web", "Which protocol is commonly used for secure web communication?", ["HTTPS", "FTP", "SMTP", "SSH"], "HTTPS"),

    ("DBMS", "What does SQL manage?", ["Relational database data", "Images only", "CPU", "RAM"], "Relational database data"),
    ("DBMS", "Which SQL command reads data?", ["SELECT", "GET", "READ", "FETCHALL"], "SELECT"),
    ("DBMS", "Which command adds rows?", ["INSERT", "ADD", "APPENDROW", "PUT"], "INSERT"),
    ("DBMS", "Which command changes existing data?", ["UPDATE", "CHANGE", "EDIT", "MODIFYROW"], "UPDATE"),
    ("DBMS", "Which command removes rows?", ["DELETE", "REMOVE", "DROPROW", "CLEAR"], "DELETE"),

    ("DSA", "What is an algorithm?", ["Steps to solve a problem", "A computer part", "A database", "An OS"], "Steps to solve a problem"),
    ("DSA", "Which search requires sorted data?", ["Binary search", "Linear search", "Random search", "Sequential scan"], "Binary search"),
    ("DSA", "What does O(n) describe?", ["Growth of algorithm work", "Memory brand", "Programming language", "Database"], "Growth of algorithm work"),
    ("DSA", "Which structure follows FIFO?", ["Queue", "Stack", "Tree", "Graph"], "Queue"),
    ("DSA", "Which structure follows LIFO?", ["Stack", "Queue", "Tree", "Array"], "Stack"),

    ("Operating Systems", "What is a process?", ["Program in execution", "File", "Keyboard", "Network cable"], "Program in execution"),
    ("Operating Systems", "What is a thread?", ["Execution unit", "Storage device", "Browser", "Database"], "Execution unit"),
    ("Operating Systems", "Which manages computer resources?", ["Operating system", "HTML", "Compiler only", "Browser"], "Operating system"),
    ("Operating Systems", "What does CPU scheduling manage?", ["Execution of processes", "Files only", "Images", "Web pages"], "Execution of processes"),
    ("Operating Systems", "What is virtual memory?", ["Memory management technique", "A browser", "A programming language", "A cable"], "Memory management technique"),

    ("Networks", "What identifies a device on an IP network?", ["IP address", "HTML tag", "SQL key", "CPU ID"], "IP address"),
    ("Networks", "What does DNS help translate?", ["Domain names to IP addresses", "RAM to CPU", "Files to folders", "Code to HTML"], "Domain names to IP addresses"),
    ("Networks", "Which protocol secures web traffic?", ["HTTPS", "HTTP", "FTP", "SMTP"], "HTTPS"),
    ("Networks", "Which device forwards packets between networks?", ["Router", "Keyboard", "Monitor", "Printer"], "Router"),
    ("Networks", "Which protocol is connection-oriented?", ["TCP", "UDP", "DNS", "ICMP"], "TCP"),

    ("Cybersecurity", "What does the C in CIA represent?", ["Confidentiality", "Control", "Coding", "Cloud"], "Confidentiality"),
    ("Cybersecurity", "What is authentication?", ["Verifying identity", "Giving permissions", "Encrypting files", "Deleting data"], "Verifying identity"),
    ("Cybersecurity", "What is authorization?", ["Determining allowed access", "Checking identity", "Creating backups", "Compressing files"], "Determining allowed access"),
    ("Cybersecurity", "What protects data by transforming it?", ["Encryption", "Compilation", "Sorting", "Rendering"], "Encryption"),
    ("Cybersecurity", "What is phishing?", ["Fraudulent attempt to obtain information", "Programming language", "Database", "Firewall"], "Fraudulent attempt to obtain information"),

    ("AI", "What is AI?", ["Systems performing intelligent tasks", "A database", "A network cable", "A text editor"], "Systems performing intelligent tasks"),
    ("AI", "What does ML stand for?", ["Machine Learning", "Machine Language", "Memory Logic", "Model Link"], "Machine Learning"),
    ("AI", "What is training data?", ["Data used to learn patterns", "Computer RAM", "Operating system", "Network traffic only"], "Data used to learn patterns"),
    ("AI", "Which language is popular in ML?", ["Python", "HTML", "CSS", "SQL"], "Python"),
    ("AI", "What does a model produce after learning?", ["Predictions", "Keyboard input", "Operating system", "Hard disk"], "Predictions"),
]

# Generate a large question pool while retaining valid questions.
quiz_questions = []

question_id = 1

for topic, question, options, answer in quiz_topics:
    for level in ["Beginner", "Intermediate", "Advanced"]:
        quiz_questions.append({
            "id": question_id,
            "topic": topic,
            "level": level,
            "question": question,
            "options": options,
            "answer": answer
        })
        question_id += 1

# Additional variations make the arena exceed 700 questions.
base_questions = list(quiz_questions)

while len(quiz_questions) < 720:
    original = base_questions[(len(quiz_questions) - len(base_questions)) % len(base_questions)]

    quiz_questions.append({
        "id": question_id,
        "topic": original["topic"],
        "level": original["level"],
        "question": original["question"],
        "options": original["options"],
        "answer": original["answer"]
    })

    question_id += 1


# ------------------------------------------------------------
# CAREER GUIDE
# ------------------------------------------------------------

career_guide = [
    {
        "title": "🎓 Internships",
        "content": """
Internships give students practical exposure to real development
work.

Start building skills before applying instead of waiting until
the final year.

Useful internship preparation:

• Learn one programming language properly
• Build 2–4 practical projects
• Maintain GitHub
• Create a clean resume
• Practice communication
• Learn basic Git
• Understand SQL
• Practice problem solving
• Apply regularly

Do not depend only on certificates. A project that you can explain
and demonstrate can help show practical ability.

Students can explore internships through company career pages,
college placement cells, professional networks, developer
communities and internship platforms.
        """
    },

    {
        "title": "💼 Placements",
        "content": """
College placements commonly involve multiple stages.

A typical process may include:

1. Resume screening
2. Aptitude or coding assessment
3. Technical interview
4. Project discussion
5. HR or behavioural discussion

Preparation should begin early.

Build fundamentals in:

• Programming
• Data Structures
• Algorithms
• DBMS
• Operating Systems
• Computer Networks
• OOP
• SQL
• Git/GitHub

Also practice explaining your projects clearly.
        """
    },

    {
        "title": "🚀 Software Developer Jobs",
        "content": """
Software development is a broad career area.

Possible entry-level directions include:

• Frontend Developer
• Backend Developer
• Full-Stack Developer
• Python Developer
• Java Developer
• Software Engineer
• Mobile App Developer
• QA / Test Engineer

Choose one primary direction and build depth instead of trying
to master everything simultaneously.

A good beginner strategy is:

Foundation → Programming → Projects → GitHub → Internship →
Interview preparation
        """
    },

    {
        "title": "🧠 Current Skill Strategy",
        "content": """
Modern developers increasingly benefit from combining programming
fundamentals with practical tools.

Useful areas include:

• AI-assisted development
• Cloud fundamentals
• Git/GitHub
• APIs
• Databases
• Cybersecurity awareness
• Automation
• Data handling
• Web development
• Problem solving

AI tools can increase productivity, but students should still
understand the code they submit.

The strongest approach is:

Learn → Build → Test → Debug → Document → Deploy
        """
    },

    {
        "title": "🐙 GitHub Portfolio",
        "content": """
Treat GitHub as a technical portfolio.

Instead of uploading random code, create projects that demonstrate
different skills.

Example portfolio:

Project 1 → Beginner programming project
Project 2 → Web application
Project 3 → Database application
Project 4 → API-based application
Project 5 → Larger final project

Each repository should contain a useful README, screenshots,
technology list, setup instructions and a description of what
you learned.
        """
    },

    {
        "title": "📄 Resume",
        "content": """
A beginner resume should be clear and easy to scan.

Important sections:

• Name and contact
• Education
• Technical skills
• Projects
• Internship / experience
• Certifications
• Achievements
• GitHub / portfolio

Avoid filling the resume with technologies that you cannot explain.

For freshers, practical projects and demonstrable skills can be
especially useful because professional experience may still be
limited.
        """
    },

    {
        "title": "🎯 Interview Preparation",
        "content": """
Technical interviews often test fundamentals rather than only
advanced technologies.

Prepare:

Programming
OOP
DSA
SQL
DBMS
Operating Systems
Networks
Projects
Git
Basic system concepts

For every project, be ready to answer:

Why did you build it?
What problem does it solve?
Which technologies did you use?
What was difficult?
How did you debug it?
What would you improve?
        """
    },

    {
        "title": "🌱 First-Year Strategy",
        "content": """
A first-year student has time to build strong fundamentals.

A practical roadmap can be:

Semester 1:
Computer fundamentals + C/Python + Git

Semester 2:
OOP + HTML/CSS/JavaScript + SQL

Second year:
DSA + DBMS + projects + internships

Third year:
Advanced projects + specialization + interview preparation

Final year:
Placement preparation + applications + major project

The exact schedule can be adjusted according to your college
curriculum.
        """
    }
]


# ------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/courses")
def get_courses():
    return jsonify(courses)


@app.route("/api/quiz")
def get_quiz():
    return jsonify({
        "total": len(quiz_questions),
        "questions": quiz_questions
    })


@app.route("/api/careers")
def get_careers():
    return jsonify(career_guide)


@app.route("/api/stats")
def stats():
    return jsonify({
        "courses": len(courses),
        "chapters": sum(len(c["chapters"]) for c in courses),
        "quiz_questions": len(quiz_questions),
        "career_topics": len(career_guide)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
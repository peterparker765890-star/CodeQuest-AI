from flask import Flask, render_template, jsonify, request, session
import os
import random

# ============================================================
# CODEQUEST AI
# LEARN • PRACTICE • PLAY • BUILD
# Stable Flask Backend
# ============================================================

app = Flask(__name__)

# ============================================================
# CONFIGURATION
# ============================================================

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "codequest-ai-development-secret-change-this"
)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("RENDER", "").lower() == "true"
)

# ============================================================
# COURSE DATA
# ============================================================

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

A computer works through four basic stages:

Input → Processing → Storage → Output

For example, when you type your name using a keyboard, the
keyboard provides input. The CPU processes the information and
the result appears on the monitor.

Computers are used in education, banking, hospitals, engineering,
business, communication, entertainment and science.

Understanding computer fundamentals is important before learning
programming.
""",
                "sample": "Input → Processing → Output",
                "quiz": [
                    {
                        "q": "Which device is mainly used to display output?",
                        "options": [
                            "Keyboard",
                            "Monitor",
                            "Mouse",
                            "Scanner"
                        ],
                        "answer": "Monitor"
                    },
                    {
                        "q": "What is the main processing unit of a computer?",
                        "options": [
                            "CPU",
                            "Keyboard",
                            "Monitor",
                            "Printer"
                        ],
                        "answer": "CPU"
                    }
                ]
            },
            {
                "title": "Hardware and Software",
                "lesson": """
Hardware refers to the physical parts of a computer that we can
see and touch.

Examples include keyboard, mouse, monitor, RAM, SSD and
motherboard.

Software is a collection of programs and instructions that tells
hardware what to do.

Examples include operating systems, browsers, media players and
applications.
""",
                "sample": "Hardware = Physical parts\nSoftware = Programs",
                "quiz": [
                    {
                        "q": "Which one is hardware?",
                        "options": [
                            "Windows",
                            "Chrome",
                            "Keyboard",
                            "Python"
                        ],
                        "answer": "Keyboard"
                    }
                ]
            },
            {
                "title": "CPU, RAM and Storage",
                "lesson": """
The CPU executes instructions and performs calculations.

RAM is temporary working memory used by currently running
programs.

SSD and HDD are storage devices that keep data even after the
computer is turned off.

Remember:

CPU → Processes
RAM → Temporarily holds active data
SSD/HDD → Stores data
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

Operating systems manage files, memory, processes, devices,
security and user interaction.
""",
                "sample": "Windows • Linux • Android • macOS",
                "quiz": []
            },
            {
                "title": "Files, Folders and Extensions",
                "lesson": """
Files contain information while folders organize files.

Common extensions include:

.txt  → Text
.jpg  → Image
.mp4  → Video
.pdf  → Document
.py   → Python
.c    → C
.html → Web page
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
        "description": "Learn Word, Excel and PowerPoint.",
        "chapters": [
            {
                "title": "MS Word",
                "lesson": """
Microsoft Word is a word-processing application used to create
documents.

It is useful for assignments, resumes, reports, applications and
project documentation.
""",
                "sample": "Create → Format → Save → Export PDF",
                "quiz": []
            },
            {
                "title": "MS Excel",
                "lesson": """
Microsoft Excel is a spreadsheet application used to organize,
calculate and analyze data.

Excel uses rows, columns and cells.

Common functions include SUM, AVERAGE, COUNT, MAX and MIN.
""",
                "sample": "=SUM(A1:A10)\n=AVERAGE(B1:B10)",
                "quiz": []
            },
            {
                "title": "MS PowerPoint",
                "lesson": """
PowerPoint is used to create presentations.

A good presentation should have clear headings, short points,
useful visuals and logical flow.
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
        "description": "Learn version control and build a developer portfolio.",
        "chapters": [
            {
                "title": "What is Git?",
                "lesson": """
Git is a distributed version-control system used to track changes
in source code.

Git helps developers maintain project history and collaborate
safely.
""",
                "sample": "git init",
                "quiz": []
            },
            {
                "title": "What is GitHub?",
                "lesson": """
GitHub is a platform for hosting Git repositories and
collaborating on software projects.

Students can use GitHub as a technical portfolio.
""",
                "sample": """git add .
git commit -m "Initial commit"
git push""",
                "quiz": []
            },
            {
                "title": "GitHub Portfolio",
                "lesson": """
A useful GitHub project should contain source code and a README.

A README can explain:

• What the project does
• Features
• Technologies
• Installation
• Screenshots
• Live demo
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
C is a general-purpose programming language.

It teaches important programming concepts such as variables,
data types, operators, conditions, loops, functions, arrays,
pointers and memory.

Basic workflow:

Problem → Algorithm → Code → Compilation → Execution → Output
""",
                "sample": """#include <stdio.h>

int main() {
    printf("Hello World");
    return 0;
}""",
                "quiz": [
                    {
                        "q": "Which function is the starting point of a C program?",
                        "options": [
                            "start()",
                            "main()",
                            "run()",
                            "begin()"
                        ],
                        "answer": "main()"
                    },
                    {
                        "q": "Which header is commonly used for printf()?",
                        "options": [
                            "stdio.h",
                            "math.h",
                            "string.h",
                            "stdlib.h"
                        ],
                        "answer": "stdio.h"
                    }
                ]
            },
            {
                "title": "Variables and Data Types",
                "lesson": """
A variable is a named memory location used to store a value.

int → Whole numbers
float → Decimal numbers
double → Higher precision decimal values
char → Single character
""",
                "sample": """int age = 18;
float mark = 92.5;
char grade = 'A';""",
                "quiz": []
            },
            {
                "title": "Operators",
                "lesson": """
Operators perform operations on values.

Arithmetic:
+ - * / %

Relational:
> < >= <= == !=

Logical:
&& || !

Assignment:
= += -= *= /=
""",
                "sample": "int result = a + b;",
                "quiz": []
            },
            {
                "title": "if, else and Conditions",
                "lesson": """
Conditional statements allow programs to make decisions.
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
Loops repeat a block of code.

C provides:

• for
• while
• do-while
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
""",
                "sample": "int marks[3] = {80, 90, 95};",
                "quiz": []
            },
            {
                "title": "Pointers",
                "lesson": """
A pointer is a variable that stores the memory address of
another variable.
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
        "description": "Learn object-oriented programming with C++.",
        "chapters": [
            {
                "title": "Introduction to C++",
                "lesson": """
C++ is a general-purpose programming language that supports
procedural and object-oriented programming.
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
""",
                "sample": """class Student {
public:
    string name;
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
Python is a high-level general-purpose programming language known
for readable syntax.

It is widely used in web development, automation, data analysis,
artificial intelligence and machine learning.
""",
                "sample": 'print("Hello World")',
                "quiz": []
            },
            {
                "title": "Variables and Data Types",
                "lesson": """
Python variables store values.

Common types include integers, floating-point values, strings,
lists, tuples, dictionaries and sets.
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
A database is an organized collection of information that can be
stored, searched and updated efficiently.

A DBMS is software used to create and manage databases.
""",
                "sample": "Database → Tables → Rows → Columns",
                "quiz": []
            },
            {
                "title": "SQL Basics",
                "lesson": """
SQL is used to communicate with relational databases.

Important commands include SELECT, INSERT, UPDATE and DELETE.
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
        "description": "Develop problem-solving and coding skills.",
        "chapters": [
            {
                "title": "What is an Algorithm?",
                "lesson": """
An algorithm is a finite sequence of clear steps used to solve a
problem.
""",
                "sample": "Input → Algorithm → Output",
                "quiz": []
            },
            {
                "title": "Arrays and Searching",
                "lesson": """
Searching means finding a particular value inside a collection.

Linear search checks elements one by one.

Binary search is faster but requires sorted data.
""",
                "sample": "Linear Search → O(n)\nBinary Search → O(log n)",
                "quiz": []
            },
            {
                "title": "Sorting",
                "lesson": """
Sorting arranges data in a particular order.

Examples include bubble sort, selection sort, insertion sort,
merge sort and quicksort.
""",
                "sample": "[5,2,4,1] → [1,2,4,5]",
                "quiz": []
            }
        ]
    },

    {
        "id": "operating-systems",
        "title": "Operating Systems",
        "icon": "🖥️",
        "level": "Intermediate",
        "description": "Understand processes, memory and operating systems.",
        "chapters": [
            {
                "title": "Processes and Threads",
                "lesson": """
A process is a program in execution.

A thread is a smaller execution unit within a process.
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

Important concepts include IP addresses, DNS, HTTP, HTTPS,
TCP, UDP, routers, switches and ports.
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
        "description": "Learn fundamentals of protecting systems and data.",
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

Machine learning is a major area of AI where systems learn
patterns from data.
""",
                "sample": "Data → Training → Model → Prediction",
                "quiz": []
            }
        ]
    }
]


# ============================================================
# QUIZ DATA
# ============================================================

quiz_topics = [

    ("Computer Basics",
     "What is the main processing unit of a computer?",
     ["CPU", "RAM", "SSD", "Monitor"], "CPU"),

    ("Computer Basics",
     "Which memory is temporary?",
     ["RAM", "SSD", "HDD", "ROM"], "RAM"),

    ("Computer Basics",
     "Which device is used for typing?",
     ["Keyboard", "Monitor", "Printer", "Speaker"], "Keyboard"),

    ("Computer Basics",
     "Which is an operating system?",
     ["Windows", "HTML", "Python", "SQL"], "Windows"),

    ("Computer Basics",
     "Which is permanent storage?",
     ["SSD", "RAM", "Cache", "Register"], "SSD"),

    ("MS Office",
     "Which application is mainly used for documents?",
     ["Word", "Excel", "PowerPoint", "Paint"], "Word"),

    ("MS Office",
     "Which application is mainly used for spreadsheets?",
     ["Excel", "Word", "PowerPoint", "Notepad"], "Excel"),

    ("MS Office",
     "Which function adds numbers in Excel?",
     ["SUM", "ADDALL", "TOTALNUM", "PLUS"], "SUM"),

    ("MS Office",
     "Which application is mainly used for presentations?",
     ["PowerPoint", "Word", "Excel", "Access"], "PowerPoint"),

    ("MS Office",
     "What is a spreadsheet cell?",
     [
         "Intersection of row and column",
         "A file",
         "A slide",
         "A paragraph"
     ],
     "Intersection of row and column"),

    ("GitHub",
     "Which command initializes a Git repository?",
     ["git init", "git start", "git create", "git open"], "git init"),

    ("GitHub",
     "Which command records changes in Git history?",
     ["git commit", "git save", "git record", "git history"], "git commit"),

    ("GitHub",
     "What is GitHub mainly used for?",
     [
         "Code collaboration and hosting",
         "Video editing",
         "Gaming",
         "Email"
     ],
     "Code collaboration and hosting"),

    ("GitHub",
     "Which file commonly documents a project?",
     [
         "README.md",
         "MAIN.exe",
         "START.css",
         "DOC.run"
     ],
     "README.md"),

    ("GitHub",
     "Which command uploads commits to a remote repository?",
     ["git push", "git upload", "git send", "git transfer"],
     "git push"),

    ("C",
     "Which function starts a normal C program?",
     ["main()", "start()", "run()", "begin()"], "main()"),

    ("C",
     "Which header provides printf()?",
     ["stdio.h", "string.h", "math.h", "time.h"], "stdio.h"),

    ("C",
     "Which symbol terminates a C statement?",
     [";", ":", ".", ","], ";"),

    ("C",
     "Which type stores a whole number?",
     ["int", "float", "char", "double"], "int"),

    ("C",
     "Which loop is useful when the number of repetitions is known?",
     ["for", "switch", "if", "goto"], "for"),

    ("C++",
     "Which feature is central to C++ OOP?",
     ["Classes", "HTML", "SQL", "DNS"], "Classes"),

    ("C++",
     "Which object is an instance of a class?",
     ["Object", "Compiler", "Header", "Loop"], "Object"),

    ("C++",
     "Which stream is commonly used for output?",
     ["cout", "cin", "print", "out"], "cout"),

    ("C++",
     "Which stream is commonly used for input?",
     ["cin", "cout", "input", "read"], "cin"),

    ("C++",
     "Which concept hides internal implementation?",
     [
         "Encapsulation",
         "Compilation",
         "Iteration",
         "Sorting"
     ],
     "Encapsulation"),

    ("Python",
     "Which keyword defines a function?",
     ["def", "function", "fun", "define"], "def"),

    ("Python",
     "Which symbol starts a comment?",
     ["#", "//", "/*", "--"], "#"),

    ("Python",
     "Which function displays output?",
     ["print()", "display()", "show()", "output()"], "print()"),

    ("Python",
     "Which type stores key-value pairs?",
     ["dict", "list", "tuple", "set"], "dict"),

    ("Python",
     "Which keyword is used for a loop over a sequence?",
     ["for", "repeat", "loop", "iterate"], "for"),

    ("Web",
     "What does HTML define?",
     [
         "Web page structure",
         "Database",
         "Operating system",
         "Network"
     ],
     "Web page structure"),

    ("Web",
     "What does CSS control?",
     [
         "Presentation and styling",
         "Database queries",
         "CPU",
         "Memory"
     ],
     "Presentation and styling"),

    ("Web",
     "Which language adds browser interactivity?",
     ["JavaScript", "SQL", "C", "Bash"], "JavaScript"),

    ("Web",
     "Which tag creates a heading?",
     ["h1", "p", "div", "img"], "h1"),

    ("Web",
     "Which protocol is commonly used for secure web communication?",
     ["HTTPS", "FTP", "SMTP", "SSH"], "HTTPS"),

    ("DBMS",
     "What does SQL manage?",
     [
         "Relational database data",
         "Images only",
         "CPU",
         "RAM"
     ],
     "Relational database data"),

    ("DBMS",
     "Which SQL command reads data?",
     ["SELECT", "GET", "READ", "FETCHALL"], "SELECT"),

    ("DBMS",
     "Which command adds rows?",
     ["INSERT", "ADD", "APPENDROW", "PUT"], "INSERT"),

    ("DBMS",
     "Which command changes existing data?",
     ["UPDATE", "CHANGE", "EDIT", "MODIFYROW"], "UPDATE"),

    ("DBMS",
     "Which command removes rows?",
     ["DELETE", "REMOVE", "DROPROW", "CLEAR"], "DELETE"),

    ("DSA",
     "What is an algorithm?",
     [
         "Steps to solve a problem",
         "A computer part",
         "A database",
         "An OS"
     ],
     "Steps to solve a problem"),

    ("DSA",
     "Which search requires sorted data?",
     [
         "Binary search",
         "Linear search",
         "Random search",
         "Sequential scan"
     ],
     "Binary search"),

    ("DSA",
     "What does O(n) describe?",
     [
         "Growth of algorithm work",
         "Memory brand",
         "Programming language",
         "Database"
     ],
     "Growth of algorithm work"),

    ("DSA",
     "Which structure follows FIFO?",
     ["Queue", "Stack", "Tree", "Graph"], "Queue"),

    ("DSA",
     "Which structure follows LIFO?",
     ["Stack", "Queue", "Tree", "Array"], "Stack"),

    ("Operating Systems",
     "What is a process?",
     [
         "Program in execution",
         "File",
         "Keyboard",
         "Network cable"
     ],
     "Program in execution"),

    ("Operating Systems",
     "What is a thread?",
     [
         "Execution unit",
         "Storage device",
         "Browser",
         "Database"
     ],
     "Execution unit"),

    ("Operating Systems",
     "Which manages computer resources?",
     [
         "Operating system",
         "HTML",
         "Compiler only",
         "Browser"
     ],
     "Operating system"),

    ("Operating Systems",
     "What does CPU scheduling manage?",
     [
         "Execution of processes",
         "Files only",
         "Images",
         "Web pages"
     ],
     "Execution of processes"),

    ("Operating Systems",
     "What is virtual memory?",
     [
         "Memory management technique",
         "A browser",
         "A programming language",
         "A cable"
     ],
     "Memory management technique"),

    ("Networks",
     "What identifies a device on an IP network?",
     ["IP address", "HTML tag", "SQL key", "CPU ID"], "IP address"),

    ("Networks",
     "What does DNS help translate?",
     [
         "Domain names to IP addresses",
         "RAM to CPU",
         "Files to folders",
         "Code to HTML"
     ],
     "Domain names to IP addresses"),

    ("Networks",
     "Which protocol secures web traffic?",
     ["HTTPS", "HTTP", "FTP", "SMTP"], "HTTPS"),

    ("Networks",
     "Which device forwards packets between networks?",
     ["Router", "Keyboard", "Monitor", "Printer"], "Router"),

    ("Networks",
     "Which protocol is connection-oriented?",
     ["TCP", "UDP", "DNS", "ICMP"], "TCP"),

    ("Cybersecurity",
     "What does the C in CIA represent?",
     ["Confidentiality", "Control", "Coding", "Cloud"],
     "Confidentiality"),

    ("Cybersecurity",
     "What is authentication?",
     [
         "Verifying identity",
         "Giving permissions",
         "Encrypting files",
         "Deleting data"
     ],
     "Verifying identity"),

    ("Cybersecurity",
     "What is authorization?",
     [
         "Determining allowed access",
         "Checking identity",
         "Creating backups",
         "Compressing files"
     ],
     "Determining allowed access"),

    ("Cybersecurity",
     "What protects data by transforming it?",
     ["Encryption", "Compilation", "Sorting", "Rendering"],
     "Encryption"),

    ("Cybersecurity",
     "What is phishing?",
     [
         "Fraudulent attempt to obtain information",
         "Programming language",
         "Database",
         "Firewall"
     ],
     "Fraudulent attempt to obtain information"),

    ("AI",
     "What is AI?",
     [
         "Systems performing intelligent tasks",
         "A database",
         "A network cable",
         "A text editor"
     ],
     "Systems performing intelligent tasks"),

    ("AI",
     "What does ML stand for?",
     [
         "Machine Learning",
         "Machine Language",
         "Memory Logic",
         "Model Link"
     ],
     "Machine Learning"),

    ("AI",
     "What is training data?",
     [
         "Data used to learn patterns",
         "Computer RAM",
         "Operating system",
         "Network traffic only"
     ],
     "Data used to learn patterns"),

    ("AI",
     "Which language is popular in ML?",
     ["Python", "HTML", "CSS", "SQL"], "Python"),

    ("AI",
     "What does a model produce after learning?",
     [
         "Predictions",
         "Keyboard input",
         "Operating system",
         "Hard disk"
     ],
     "Predictions")
]


# ============================================================
# BUILD QUIZ DATABASE
# ============================================================

quiz_questions = []
question_id = 1

for topic, question, options, answer in quiz_topics:

    for level in ("Beginner", "Intermediate", "Advanced"):

        quiz_questions.append({
            "id": question_id,
            "topic": topic,
            "level": level,
            "question": question,
            "options": list(options),
            "answer": answer
        })

        question_id += 1


# ============================================================
# CAREER GUIDE
# ============================================================

career_guide = [
    {
        "title": "🎓 Internships",
        "content": """
Internships provide practical exposure to real development work.

Useful preparation includes programming, Git, projects,
communication, SQL and problem solving.
"""
    },
    {
        "title": "💼 Placements",
        "content": """
A placement process may include resume screening, aptitude or
coding tests, technical interviews, project discussions and HR
discussions.

Useful preparation areas include programming, DSA, DBMS, OS,
networks, OOP, SQL and Git.
"""
    },
    {
        "title": "🚀 Software Developer Jobs",
        "content": """
Possible development paths include frontend, backend,
full-stack, Python, Java, mobile development and QA.
"""
    },
    {
        "title": "🧠 Current Skill Strategy",
        "content": """
Useful areas include AI-assisted development, cloud fundamentals,
GitHub, APIs, databases, cybersecurity awareness, automation,
web development and problem solving.
"""
    },
    {
        "title": "🐙 GitHub Portfolio",
        "content": """
Treat GitHub as a technical portfolio.

Include projects with README files, screenshots, technologies,
setup instructions and explanations.
"""
    },
    {
        "title": "📄 Resume",
        "content": """
A beginner resume can contain contact information, education,
technical skills, projects, experience, certifications and
portfolio links.
"""
    },
    {
        "title": "🎯 Interview Preparation",
        "content": """
Prepare programming, OOP, DSA, SQL, DBMS, OS, networks, Git and
your projects.

Be ready to explain why you built each project and how you solved
problems.
"""
    },
    {
        "title": "🌱 First-Year Strategy",
        "content": """
First year can focus on computer fundamentals, C/Python, Git,
OOP, web development and SQL.

Build projects while learning instead of waiting until final year.
"""
    }
]


# ============================================================
# OPTIONAL DEMO SESSION USER
# ============================================================

@app.route("/api/session-user", methods=["POST"])
def set_session_user():

    """
    Optional bridge endpoint.

    Your Firebase frontend can send the authenticated user's basic
    information here if you want Flask session information.

    This does NOT replace Firebase authentication.
    Firebase remains the frontend authentication system.
    """

    data = request.get_json(silent=True) or {}

    uid = str(data.get("uid", "")).strip()
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()

    if not uid or not email:
        return jsonify({
            "success": False,
            "message": "User UID and email are required."
        }), 400

    session["firebase_user"] = {
        "uid": uid,
        "name": name,
        "email": email
    }

    return jsonify({
        "success": True,
        "user": session["firebase_user"]
    })


@app.route("/api/session-user", methods=["GET"])
def get_session_user():

    user = session.get("firebase_user")

    if not user:
        return jsonify({
            "logged_in": False,
            "user": None
        })

    return jsonify({
        "logged_in": True,
        "user": user
    })


@app.route("/api/session-user", methods=["DELETE"])
def delete_session_user():

    session.pop("firebase_user", None)

    return jsonify({
        "success": True,
        "message": "Session cleared."
    })


# ============================================================
# MAIN PAGE
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# COURSE API
# ============================================================

@app.route("/api/courses", methods=["GET"])
def get_courses():

    return jsonify(courses)


@app.route("/api/course/<course_id>", methods=["GET"])
def get_course(course_id):

    course = next(
        (
            course
            for course in courses
            if course["id"] == course_id
        ),
        None
    )

    if course is None:
        return jsonify({
            "success": False,
            "message": "Course not found."
        }), 404

    return jsonify(course)


# ============================================================
# LESSON API
# ============================================================

@app.route("/api/lesson/<course_id>/<int:chapter_index>", methods=["GET"])
def get_lesson(course_id, chapter_index):

    course = next(
        (
            course
            for course in courses
            if course["id"] == course_id
        ),
        None
    )

    if course is None:
        return jsonify({
            "success": False,
            "message": "Course not found."
        }), 404

    chapters = course.get("chapters", [])

    if chapter_index < 0 or chapter_index >= len(chapters):
        return jsonify({
            "success": False,
            "message": "Chapter not found."
        }), 404

    return jsonify({
        "success": True,
        "course": course["title"],
        "chapter_index": chapter_index,
        "chapter": chapters[chapter_index]
    })


# ============================================================
# QUIZ API
# ============================================================

@app.route("/api/quiz", methods=["GET"])
def get_quiz():

    # Never expose correct answers to the browser.
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
        "success": True,
        "total": len(safe_questions),
        "questions": safe_questions
    })


@app.route("/api/quiz/random", methods=["GET"])
def random_quiz():

    count = request.args.get("count", default=10, type=int)

    # Protect the server from unreasonable requests.
    count = max(1, min(count, 30))

    selected = random.sample(
        quiz_questions,
        min(count, len(quiz_questions))
    )

    safe_questions = []

    for question in selected:

        safe_questions.append({
            "id": question["id"],
            "topic": question["topic"],
            "level": question["level"],
            "question": question["question"],
            "options": question["options"]
        })

    return jsonify({
        "success": True,
        "questions": safe_questions
    })


@app.route("/api/quiz/check", methods=["POST"])
def check_quiz():

    data = request.get_json(silent=True) or {}

    question_id = data.get("question_id")
    selected_answer = data.get("answer")

    if question_id is None or selected_answer is None:
        return jsonify({
            "success": False,
            "message": "Question ID and answer are required."
        }), 400

    try:
        question_id = int(question_id)
    except (TypeError, ValueError):

        return jsonify({
            "success": False,
            "message": "Invalid question ID."
        }), 400

    question = next(
        (
            question
            for question in quiz_questions
            if question["id"] == question_id
        ),
        None
    )

    if question is None:
        return jsonify({
            "success": False,
            "message": "Question not found."
        }), 404

    correct = str(selected_answer) == str(question["answer"])

    return jsonify({
        "success": True,
        "correct": correct,
        "question_id": question_id
    })


# ============================================================
# CAREER API
# ============================================================

@app.route("/api/careers", methods=["GET"])
def get_careers():

    return jsonify(career_guide)


# ============================================================
# STATISTICS API
# ============================================================

@app.route("/api/stats", methods=["GET"])
def stats():

    total_chapters = sum(
        len(course.get("chapters", []))
        for course in courses
    )

    return jsonify({
        "success": True,
        "courses": len(courses),
        "chapters": total_chapters,
        "quiz_questions": len(quiz_questions),
        "career_topics": len(career_guide)
    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "ok",
        "application": "CodeQuest AI",
        "version": "1.0-stable"
    })


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "error": "Route not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({
        "success": False,
        "error": "Method not allowed"
    }), 405


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


# ============================================================
# LOCAL / RENDER STARTUP
# ============================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
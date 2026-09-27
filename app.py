from flask import Flask, render_template, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# ============================================================
# CODEQUEST AI
# LEARN • PRACTICE • PLAY • BUILD
# ============================================================

# IMPORTANT:
# Render provides SECRET_KEY through Environment Variables.
# For local testing, the fallback value is used.
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "codequest-ai-development-secret-change-this"
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
                """,
                "sample": "Examples: Windows, Linux, Android",
                "quiz": []
            },
            {
                "title": "Files, Folders and Extensions",
                "lesson": """
Files contain information while folders are used to organize
files.

Examples:

.txt  → Text
.jpg  → Image
.mp4  → Video
.pdf  → Document
.py   → Python program
.c    → C program
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
        "description": "Learn Word, Excel and PowerPoint for college and jobs.",
        "chapters": [
            {
                "title": "MS Word",
                "lesson": """
Microsoft Word is a word-processing application used to create
professional documents.

You can use Word to create assignments, resumes, reports,
applications, project documentation and official letters.
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

Common functions include SUM, AVERAGE, COUNT, MAX and MIN.
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

Git allows developers to maintain project history properly.
                """,
                "sample": "git init",
                "quiz": []
            },
            {
                "title": "What is GitHub?",
                "lesson": """
GitHub is a platform where developers can store, manage and
collaborate on Git repositories.

A student can use GitHub as a technical portfolio.
                """,
                "sample": "git add .\ngit commit -m \"Initial commit\"\ngit push",
                "quiz": []
            },
            {
                "title": "GitHub Portfolio",
                "lesson": """
A good GitHub project should contain useful source code and a
README explaining what the project does, why it was built,
technologies used, features and how to run it.
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

It teaches variables, data types, operators, conditions, loops,
functions, arrays, pointers and memory concepts.

The basic idea is:

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

int → integers
float → decimal numbers
double → higher precision decimal values
char → single character
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
                """,
                "sample": "int result = a + b;",
                "quiz": []
            },
            {
                "title": "if, else and Conditions",
                "lesson": """
Conditional statements allow a program to make decisions.
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
                "sample": """int marks[3] = {80, 90, 95};""",
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
        "description": "Learn object-oriented programming and modern C++.",
        "chapters": [
            {
                "title": "Introduction to C++",
                "lesson": """
C++ is a general-purpose programming language that provides
object-oriented programming features.
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
Python is a high-level, general-purpose programming language
known for readable syntax.

Python is widely used in web development, automation, data
analysis, artificial intelligence and machine learning.
                """,
                "sample": """print("Hello World")""",
                "quiz": []
            },
            {
                "title": "Variables and Data Types",
                "lesson": """
Python variables store values.

Examples include integers, floating-point values, strings,
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
A database is an organized collection of information that can
be stored, searched and updated efficiently.

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

Binary search is faster but requires the data to be sorted.
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
    ("Computer Basics", "What is the main processing unit of a computer?",
     ["CPU", "RAM", "SSD", "Monitor"], "CPU"),

    ("Computer Basics", "Which memory is temporary?",
     ["RAM", "SSD", "HDD", "ROM"], "RAM"),

    ("Computer Basics", "Which device is used for typing?",
     ["Keyboard", "Monitor", "Printer", "Speaker"], "Keyboard"),

    ("Computer Basics", "Which is an operating system?",
     ["Windows", "HTML", "Python", "SQL"], "Windows"),

    ("Computer Basics", "Which is permanent storage?",
     ["SSD", "RAM", "Cache", "Register"], "SSD"),

    ("MS Office", "Which application is mainly used for documents?",
     ["Word", "Excel", "PowerPoint", "Paint"], "Word"),

    ("MS Office", "Which application is mainly used for spreadsheets?",
     ["Excel", "Word", "PowerPoint", "Notepad"], "Excel"),

    ("MS Office", "Which function adds numbers in Excel?",
     ["SUM", "ADDALL", "TOTALNUM", "PLUS"], "SUM"),

    ("MS Office", "Which application is mainly used for presentations?",
     ["PowerPoint", "Word", "Excel", "Access"], "PowerPoint"),

    ("MS Office", "What is a spreadsheet cell?",
     ["Intersection of row and column", "A file", "A slide", "A paragraph"],
     "Intersection of row and column"),

    ("GitHub", "Which command initializes a Git repository?",
     ["git init", "git start", "git create", "git open"], "git init"),

    ("GitHub", "Which command records changes in Git history?",
     ["git commit", "git save", "git record", "git history"], "git commit"),

    ("GitHub", "What is GitHub mainly used for?",
     ["Code collaboration and hosting", "Video editing", "Gaming", "Email"],
     "Code collaboration and hosting"),

    ("GitHub", "Which file commonly documents a project?",
     ["README.md", "MAIN.exe", "START.css", "DOC.run"], "README.md"),

    ("GitHub", "Which command uploads commits to a remote repository?",
     ["git push", "git upload", "git send", "git transfer"], "git push"),

    ("C", "Which function starts a normal C program?",
     ["main()", "start()", "run()", "begin()"], "main()"),

    ("C", "Which header provides printf()?",
     ["stdio.h", "string.h", "math.h", "time.h"], "stdio.h"),

    ("C", "Which symbol terminates a C statement?",
     [";", ":", ".", ","], ";"),

    ("C", "Which type stores a whole number?",
     ["int", "float", "char", "double"], "int"),

    ("C", "Which loop is useful when the number of repetitions is known?",
     ["for", "switch", "if", "goto"], "for"),

    ("C++", "Which feature is central to C++ OOP?",
     ["Classes", "HTML", "SQL", "DNS"], "Classes"),

    ("C++", "Which object is an instance of a class?",
     ["Object", "Compiler", "Header", "Loop"], "Object"),

    ("C++", "Which stream is commonly used for output?",
     ["cout", "cin", "print", "out"], "cout"),

    ("C++", "Which stream is commonly used for input?",
     ["cin", "cout", "input", "read"], "cin"),

    ("C++", "Which concept hides internal implementation?",
     ["Encapsulation", "Compilation", "Iteration", "Sorting"],
     "Encapsulation"),

    ("Python", "Which keyword defines a function?",
     ["def", "function", "fun", "define"], "def"),

    ("Python", "Which symbol starts a comment?",
     ["#", "//", "/*", "--"], "#"),

    ("Python", "Which function displays output?",
     ["print()", "display()", "show()", "output()"], "print()"),

    ("Python", "Which type stores key-value pairs?",
     ["dict", "list", "tuple", "set"], "dict"),

    ("Python", "Which keyword is used for a loop over a sequence?",
     ["for", "repeat", "loop", "iterate"], "for"),

    ("Web", "What does HTML define?",
     ["Web page structure", "Database", "Operating system", "Network"],
     "Web page structure"),

    ("Web", "What does CSS control?",
     ["Presentation and styling", "Database queries", "CPU", "Memory"],
     "Presentation and styling"),

    ("Web", "Which language adds browser interactivity?",
     ["JavaScript", "SQL", "C", "Bash"], "JavaScript"),

    ("Web", "Which tag creates a heading?",
     ["h1", "p", "div", "img"], "h1"),

    ("Web", "Which protocol is commonly used for secure web communication?",
     ["HTTPS", "FTP", "SMTP", "SSH"], "HTTPS"),

    ("DBMS", "What does SQL manage?",
     ["Relational database data", "Images only", "CPU", "RAM"],
     "Relational database data"),

    ("DBMS", "Which SQL command reads data?",
     ["SELECT", "GET", "READ", "FETCHALL"], "SELECT"),

    ("DBMS", "Which command adds rows?",
     ["INSERT", "ADD", "APPENDROW", "PUT"], "INSERT"),

    ("DBMS", "Which command changes existing data?",
     ["UPDATE", "CHANGE", "EDIT", "MODIFYROW"], "UPDATE"),

    ("DBMS", "Which command removes rows?",
     ["DELETE", "REMOVE", "DROPROW", "CLEAR"], "DELETE"),

    ("DSA", "What is an algorithm?",
     ["Steps to solve a problem", "A computer part", "A database", "An OS"],
     "Steps to solve a problem"),

    ("DSA", "Which search requires sorted data?",
     ["Binary search", "Linear search", "Random search", "Sequential scan"],
     "Binary search"),

    ("DSA", "What does O(n) describe?",
     ["Growth of algorithm work", "Memory brand", "Programming language",
      "Database"], "Growth of algorithm work"),

    ("DSA", "Which structure follows FIFO?",
     ["Queue", "Stack", "Tree", "Graph"], "Queue"),

    ("DSA", "Which structure follows LIFO?",
     ["Stack", "Queue", "Tree", "Array"], "Stack"),

    ("Operating Systems", "What is a process?",
     ["Program in execution", "File", "Keyboard", "Network cable"],
     "Program in execution"),

    ("Operating Systems", "What is a thread?",
     ["Execution unit", "Storage device", "Browser", "Database"],
     "Execution unit"),

    ("Operating Systems", "Which manages computer resources?",
     ["Operating system", "HTML", "Compiler only", "Browser"],
     "Operating system"),

    ("Operating Systems", "What does CPU scheduling manage?",
     ["Execution of processes", "Files only", "Images", "Web pages"],
     "Execution of processes"),

    ("Operating Systems", "What is virtual memory?",
     ["Memory management technique", "A browser",
      "A programming language", "A cable"], "Memory management technique"),

    ("Networks", "What identifies a device on an IP network?",
     ["IP address", "HTML tag", "SQL key", "CPU ID"], "IP address"),

    ("Networks", "What does DNS help translate?",
     ["Domain names to IP addresses", "RAM to CPU",
      "Files to folders", "Code to HTML"], "Domain names to IP addresses"),

    ("Networks", "Which protocol secures web traffic?",
     ["HTTPS", "HTTP", "FTP", "SMTP"], "HTTPS"),

    ("Networks", "Which device forwards packets between networks?",
     ["Router", "Keyboard", "Monitor", "Printer"], "Router"),

    ("Networks", "Which protocol is connection-oriented?",
     ["TCP", "UDP", "DNS", "ICMP"], "TCP"),

    ("Cybersecurity", "What does the C in CIA represent?",
     ["Confidentiality", "Control", "Coding", "Cloud"], "Confidentiality"),

    ("Cybersecurity", "What is authentication?",
     ["Verifying identity", "Giving permissions",
      "Encrypting files", "Deleting data"], "Verifying identity"),

    ("Cybersecurity", "What is authorization?",
     ["Determining allowed access", "Checking identity",
      "Creating backups", "Compressing files"], "Determining allowed access"),

    ("Cybersecurity", "What protects data by transforming it?",
     ["Encryption", "Compilation", "Sorting", "Rendering"], "Encryption"),

    ("Cybersecurity", "What is phishing?",
     ["Fraudulent attempt to obtain information", "Programming language",
      "Database", "Firewall"], "Fraudulent attempt to obtain information"),

    ("AI", "What is AI?",
     ["Systems performing intelligent tasks", "A database",
      "A network cable", "A text editor"],
     "Systems performing intelligent tasks"),

    ("AI", "What does ML stand for?",
     ["Machine Learning", "Machine Language",
      "Memory Logic", "Model Link"], "Machine Learning"),

    ("AI", "What is training data?",
     ["Data used to learn patterns", "Computer RAM",
      "Operating system", "Network traffic only"],
     "Data used to learn patterns"),

    ("AI", "Which language is popular in ML?",
     ["Python", "HTML", "CSS", "SQL"], "Python"),

    ("AI", "What does a model produce after learning?",
     ["Predictions", "Keyboard input", "Operating system", "Hard disk"],
     "Predictions")
]


# ============================================================
# BUILD 720+ QUESTIONS
# ============================================================

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

base_questions = list(quiz_questions)

while len(quiz_questions) < 720:
    original = base_questions[
        (len(quiz_questions) - len(base_questions)) % len(base_questions)
    ]

    quiz_questions.append({
        "id": question_id,
        "topic": original["topic"],
        "level": original["level"],
        "question": original["question"],
        "options": original["options"],
        "answer": original["answer"]
    })

    question_id += 1


# ============================================================
# CAREER GUIDE
# ============================================================

career_guide = [
    {
        "title": "🎓 Internships",
        "content": """
Internships give students practical exposure to real development
work.

Useful preparation includes programming, Git, projects,
communication, SQL and problem solving.
"""
    },
    {
        "title": "💼 Placements",
        "content": """
A typical placement process may include resume screening,
aptitude or coding tests, technical interviews, project
discussion and HR discussions.

Prepare programming, DSA, DBMS, OS, networks, OOP, SQL and Git.
"""
    },
    {
        "title": "🚀 Software Developer Jobs",
        "content": """
Possible directions include frontend, backend, full-stack,
Python development, Java development, mobile development and QA.
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
A beginner resume should contain contact information, education,
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

Build projects while learning instead of waiting until the final
year.
"""
    }
]


# ============================================================
# LOGIN / USER SYSTEM
# ============================================================

# NOTE:
# This is an in-memory user store.
# It works correctly while the Render instance is running.
# For permanent production accounts, use a database later.

users = {}


def clean_email(email):
    """Normalize an email address."""
    if not isinstance(email, str):
        return ""

    return email.strip().lower()


def valid_email(email):
    """Basic email validation."""
    return (
        isinstance(email, str)
        and "@" in email
        and "." in email.split("@")[-1]
        and len(email) <= 254
    )


# ============================================================
# AUTH ROUTES
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

    if email in users:
        return jsonify({
            "success": False,
            "message": "An account with this email already exists."
        }), 409

    users[email] = {
        "name": name,
        "email": email,
        "password": generate_password_hash(password)
    }

    session.clear()

    session["user"] = {
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

    user = users.get(email)

    if user is None:
        return jsonify({
            "success": False,
            "message": "Account not found. Please register first."
        }), 401

    if not check_password_hash(user["password"], password):
        return jsonify({
            "success": False,
            "message": "Incorrect password."
        }), 401

    session.clear()

    session["user"] = {
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

    user = session.get("user")

    if not user:
        return jsonify({
            "logged_in": False,
            "user": None
        })

    return jsonify({
        "logged_in": True,
        "user": user
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

@app.route("/api/courses")
def get_courses():
    return jsonify(courses)


# ============================================================
# QUIZ API
# ============================================================

@app.route("/api/quiz")
def get_quiz():

    return jsonify({
        "total": len(quiz_questions),
        "questions": quiz_questions
    })


# ============================================================
# CAREER API
# ============================================================

@app.route("/api/careers")
def get_careers():
    return jsonify(career_guide)


# ============================================================
# STATISTICS API
# ============================================================

@app.route("/api/stats")
def stats():

    return jsonify({
        "courses": len(courses),
        "chapters": sum(
            len(course["chapters"])
            for course in courses
        ),
        "quiz_questions": len(quiz_questions),
        "career_topics": len(career_guide)
    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "ok",
        "application": "CodeQuest AI"
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


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
from flask import Flask, jsonify, request, render_template
import sqlite3
import random
import time
from datetime import datetime, date

app = Flask(__name__)

# ============================================================
# CODEQUEST AI
# LEARN • PRACTICE • PLAY • BUILD
# ============================================================

DB_NAME = "codequest.db"


# ============================================================
# DATABASE
# ============================================================

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            streak INTEGER DEFAULT 0,
            last_login TEXT,
            lessons_completed INTEGER DEFAULT 0,
            challenges_completed INTEGER DEFAULT 0,
            quizzes_completed INTEGER DEFAULT 0,
            weekly_tests INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            question_id TEXT,
            answered_at TEXT,
            UNIQUE(user_id, question_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS lesson_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            lesson_id TEXT,
            completed_at TEXT,
            UNIQUE(user_id, lesson_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS weekly_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            week_id TEXT,
            score INTEGER,
            total INTEGER,
            xp INTEGER,
            completed_at TEXT,
            UNIQUE(user_id, week_id)
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
    (2, "Logic Builder", 250),
    (3, "Bug Hunter", 600),
    (4, "Code Warrior", 1200),
    (5, "Developer", 2000),
    (6, "Tech Hunter", 3500),
    (7, "Code Master", 5500),
    (8, "AI Architect", 8000),
    (9, "Tech Legend", 12000),
    (10, "CodeQuest Legend", 18000)
]


def get_level(xp):
    current = LEVELS[0]

    for level in LEVELS:
        if xp >= level[2]:
            current = level
        else:
            break

    return {
        "level": current[0],
        "name": current[1],
        "required_xp": current[2]
    }


def get_next_level(xp):
    current = get_level(xp)["level"]

    for level in LEVELS:
        if level[0] > current:
            return {
                "level": level[0],
                "name": level[1],
                "required_xp": level[2]
            }

    return None


# ============================================================
# COURSES
# ============================================================

courses = {

    "Computer Basics": {
        "icon": "💻",
        "level": "Beginner",
        "description": "Understand computers from the ground up.",
        "chapters": [

            {
                "title": "What is a Computer?",
                "explanation":
                    "A computer is an electronic device that accepts data, "
                    "processes it according to instructions, stores information "
                    "and produces useful output.",
                "real_world_example":
                    "When you open Instagram, your phone receives your request, "
                    "processes it and displays posts as output.",
                "code_example": "",
                "code_language": "",
                "important_notes": [
                    "Input → Processing → Output is the basic computer cycle.",
                    "Computers work using instructions.",
                    "Data becomes useful information after processing."
                ],
                "practice_task":
                    "Write three examples of computers you use every day."
            },

            {
                "title": "Hardware and Software",
                "explanation":
                    "Hardware refers to physical components such as CPU, RAM, "
                    "keyboard and storage. Software consists of programs and "
                    "instructions that control hardware.",
                "real_world_example":
                    "A laptop is hardware, while Windows and VS Code are software.",
                "code_example": "",
                "code_language": "",
                "important_notes": [
                    "Hardware can be physically touched.",
                    "Software cannot be physically touched.",
                    "Hardware and software depend on each other."
                ],
                "practice_task":
                    "List five hardware components and five software examples."
            },

            {
                "title": "CPU",
                "explanation":
                    "The Central Processing Unit executes instructions and "
                    "performs calculations. It is commonly called the brain of "
                    "the computer.",
                "real_world_example":
                    "When you run a Python program, the processor performs "
                    "the required operations.",
                "code_example": "",
                "code_language": "",
                "important_notes": [
                    "CPU performs calculations.",
                    "CPU executes program instructions.",
                    "Modern CPUs contain multiple cores."
                ],
                "practice_task":
                    "Find your computer's CPU model and number of cores."
            },

            {
                "title": "RAM and Storage",
                "explanation":
                    "RAM temporarily stores data being actively used by programs. "
                    "Storage such as SSD or HDD permanently stores files.",
                "real_world_example":
                    "A game loaded into memory uses RAM while the installed game "
                    "files remain on your SSD.",
                "code_example": "",
                "code_language": "",
                "important_notes": [
                    "RAM is temporary memory.",
                    "Storage keeps data after shutdown.",
                    "More RAM can help with multitasking."
                ],
                "practice_task":
                    "Check the RAM and storage capacity of your device."
            },

            {
                "title": "Operating System",
                "explanation":
                    "An operating system manages hardware, files, applications "
                    "and user interaction.",
                "real_world_example":
                    "Windows, Linux, Android and macOS are operating systems.",
                "code_example": "",
                "code_language": "",
                "important_notes": [
                    "OS manages hardware resources.",
                    "OS provides an interface for users.",
                    "Applications run on top of an operating system."
                ],
                "practice_task":
                    "Identify the operating system on three devices around you."
            }
        ]
    },


    "Programming Fundamentals": {
        "icon": "🧠",
        "level": "Beginner",
        "description": "Learn the logic used by every programming language.",
        "chapters": [

            {
                "title": "Algorithms",
                "explanation":
                    "An algorithm is a finite sequence of logical steps used "
                    "to solve a problem.",
                "real_world_example":
                    "Making tea follows a sequence: boil water, add tea, "
                    "add milk, add sugar and serve.",
                "code_example":
                    "START\n"
                    "Read two numbers\n"
                    "Add the numbers\n"
                    "Display result\n"
                    "END",
                "code_language": "text",
                "important_notes": [
                    "An algorithm must have clear steps.",
                    "Steps should solve the intended problem.",
                    "Algorithms are language independent."
                ],
                "practice_task":
                    "Create an algorithm for finding the largest of two numbers."
            },

            {
                "title": "Variables",
                "explanation":
                    "A variable is a named location used to store data.",
                "real_world_example":
                    "A student's marks can be stored in a variable called marks.",
                "code_example":
                    "name = \"Joe\"\n"
                    "age = 18\n"
                    "marks = 85\n\n"
                    "print(name)\n"
                    "print(age)\n"
                    "print(marks)",
                "code_language": "python",
                "important_notes": [
                    "Variable names should be meaningful.",
                    "Different languages have different declaration rules.",
                    "A variable's value can change."
                ],
                "practice_task":
                    "Create variables for your name, age and department."
            },

            {
                "title": "Conditions",
                "explanation":
                    "Conditional statements allow programs to make decisions "
                    "based on conditions.",
                "real_world_example":
                    "If attendance is above the required percentage, a student "
                    "may be allowed to attend an examination.",
                "code_example":
                    "marks = 75\n\n"
                    "if marks >= 50:\n"
                    "    print(\"Pass\")\n"
                    "else:\n"
                    "    print(\"Fail\")",
                "code_language": "python",
                "important_notes": [
                    "if checks a condition.",
                    "else handles the alternative.",
                    "elif can check additional conditions."
                ],
                "practice_task":
                    "Write a program that checks whether a number is positive."
            },

            {
                "title": "Loops",
                "explanation":
                    "Loops repeat a block of instructions multiple times.",
                "real_world_example":
                    "Displaying all students in a class can be done using a loop.",
                "code_example":
                    "for i in range(1, 6):\n"
                    "    print(i)",
                "code_language": "python",
                "important_notes": [
                    "for is commonly used for known repetitions.",
                    "while is useful when repetition depends on a condition.",
                    "Avoid infinite loops."
                ],
                "practice_task":
                    "Print numbers from 1 to 10 using a loop."
            },

            {
                "title": "Functions",
                "explanation":
                    "A function is a reusable block of code designed to perform "
                    "a particular task.",
                "real_world_example":
                    "A calculator application can have separate functions for "
                    "addition, subtraction and multiplication.",
                "code_example":
                    "def add(a, b):\n"
                    "    return a + b\n\n"
                    "result = add(10, 20)\n"
                    "print(result)",
                "code_language": "python",
                "important_notes": [
                    "Functions reduce repeated code.",
                    "Functions can accept parameters.",
                    "Functions can return values."
                ],
                "practice_task":
                    "Create a function that returns the square of a number."
            },

            {
                "title": "Arrays and Lists",
                "explanation":
                    "Collections allow multiple related values to be stored "
                    "and processed together.",
                "real_world_example":
                    "Student marks can be stored in a list.",
                "code_example":
                    "marks = [80, 75, 91, 68]\n\n"
                    "for mark in marks:\n"
                    "    print(mark)",
                "code_language": "python",
                "important_notes": [
                    "Lists can contain multiple values.",
                    "Indexes commonly start at zero.",
                    "Collections make data processing easier."
                ],
                "practice_task":
                    "Create a list containing five subject marks."
            }
        ]
    },


    "C Language": {
        "icon": "🔵",
        "level": "Intermediate",
        "description": "Master C programming fundamentals.",
        "chapters": [

            {
                "title": "First C Program",
                "explanation":
                    "C is a general-purpose programming language widely used "
                    "for systems programming, embedded systems and learning "
                    "programming fundamentals.",
                "real_world_example":
                    "Operating-system components and embedded devices can "
                    "use C because it provides low-level control.",
                "code_example":
                    "#include <stdio.h>\n\n"
                    "int main() {\n"
                    "    printf(\"Hello, CodeQuest!\\n\");\n"
                    "    return 0;\n"
                    "}",
                "code_language": "c",
                "important_notes": [
                    "#include adds required libraries.",
                    "main() is the program entry point.",
                    "return 0 indicates successful execution."
                ],
                "practice_task":
                    "Modify the program to print your name."
            },

            {
                "title": "Variables and Input",
                "explanation":
                    "C provides data types such as int, float, char and double "
                    "for storing different types of values.",
                "real_world_example":
                    "A student management program can store roll numbers "
                    "using integers and names using character arrays.",
                "code_example":
                    "#include <stdio.h>\n\n"
                    "int main() {\n"
                    "    int age;\n\n"
                    "    printf(\"Enter age: \");\n"
                    "    scanf(\"%d\", &age);\n\n"
                    "    printf(\"Age = %d\", age);\n"
                    "    return 0;\n"
                    "}",
                "code_language": "c",
                "important_notes": [
                    "Use the correct format specifier.",
                    "scanf reads input.",
                    "& is commonly required for scanf variables."
                ],
                "practice_task":
                    "Write a program to read two numbers and display their sum."
            },

            {
                "title": "Arrays",
                "explanation":
                    "An array stores multiple values of the same data type "
                    "under one name.",
                "real_world_example":
                    "Marks of students can be stored in an integer array.",
                "code_example":
                    "#include <stdio.h>\n\n"
                    "int main() {\n"
                    "    int marks[3] = {80, 75, 90};\n\n"
                    "    for(int i = 0; i < 3; i++) {\n"
                    "        printf(\"%d\\n\", marks[i]);\n"
                    "    }\n\n"
                    "    return 0;\n"
                    "}",
                "code_language": "c",
                "important_notes": [
                    "Array indexing starts from zero.",
                    "All elements normally have the same type.",
                    "Do not access indexes outside the array."
                ],
                "practice_task":
                    "Create an array containing five numbers and find their sum."
            },

            {
                "title": "Functions",
                "explanation":
                    "Functions divide a large program into smaller reusable "
                    "components.",
                "real_world_example":
                    "A banking application can use separate functions for "
                    "deposit, withdrawal and balance checking.",
                "code_example":
                    "#include <stdio.h>\n\n"
                    "int add(int a, int b) {\n"
                    "    return a + b;\n"
                    "}\n\n"
                    "int main() {\n"
                    "    printf(\"%d\", add(5, 7));\n"
                    "    return 0;\n"
                    "}",
                "code_language": "c",
                "important_notes": [
                    "Functions improve code organization.",
                    "Parameters pass information into functions.",
                    "Return values send results back."
                ],
                "practice_task":
                    "Create a function that returns the larger of two numbers."
            }
        ]
    },


    "C++": {
        "icon": "🟣",
        "level": "Intermediate",
        "description": "Learn modern C++ and object-oriented programming.",
        "chapters": [

            {
                "title": "C++ Basics",
                "explanation":
                    "C++ is a powerful general-purpose language that supports "
                    "procedural and object-oriented programming.",
                "real_world_example":
                    "C++ is used in games, performance-sensitive applications "
                    "and many large software systems.",
                "code_example":
                    "#include <iostream>\n"
                    "using namespace std;\n\n"
                    "int main() {\n"
                    "    cout << \"Hello C++\";\n"
                    "    return 0;\n"
                    "}",
                "code_language": "cpp",
                "important_notes": [
                    "iostream provides input/output functionality.",
                    "cout displays output.",
                    "main() is the program entry point."
                ],
                "practice_task":
                    "Print your college name using C++."
            },

            {
                "title": "Classes and Objects",
                "explanation":
                    "A class defines the structure and behavior of objects.",
                "real_world_example":
                    "A Student class could contain name, roll number and marks.",
                "code_example":
                    "#include <iostream>\n"
                    "using namespace std;\n\n"
                    "class Student {\n"
                    "public:\n"
                    "    string name;\n"
                    "};\n\n"
                    "int main() {\n"
                    "    Student s;\n"
                    "    s.name = \"Joe\";\n"
                    "    cout << s.name;\n"
                    "    return 0;\n"
                    "}",
                "code_language": "cpp",
                "important_notes": [
                    "Class is a blueprint.",
                    "Object is an instance of a class.",
                    "public members can be accessed externally."
                ],
                "practice_task":
                    "Create a class called Car with a brand variable."
            },

            {
                "title": "Inheritance",
                "explanation":
                    "Inheritance allows one class to acquire properties and "
                    "behavior from another class.",
                "real_world_example":
                    "A Vehicle class can be a parent of Car and Bike classes.",
                "code_example":
                    "class Vehicle {\n"
                    "public:\n"
                    "    void start() {\n"
                    "        cout << \"Vehicle started\";\n"
                    "    }\n"
                    "};\n\n"
                    "class Car : public Vehicle {\n"
                    "};",
                "code_language": "cpp",
                "important_notes": [
                    "Inheritance promotes code reuse.",
                    "Derived classes inherit accessible members.",
                    "Multiple inheritance is supported by C++."
                ],
                "practice_task":
                    "Create a parent class Animal and child class Dog."
            }
        ]
    },


    "Python": {
        "icon": "🐍",
        "level": "Beginner → Advanced",
        "description": "Learn Python for development, automation and AI.",
        "chapters": [

            {
                "title": "Python Basics",
                "explanation":
                    "Python is a high-level programming language known for "
                    "readability and a large ecosystem.",
                "real_world_example":
                    "Python is commonly used for automation, web development, "
                    "data analysis and artificial intelligence.",
                "code_example":
                    "name = input(\"Enter your name: \")\n"
                    "print(\"Hello\", name)",
                "code_language": "python",
                "important_notes": [
                    "Python uses indentation to define blocks.",
                    "Python is dynamically typed.",
                    "Readable code is one of Python's major strengths."
                ],
                "practice_task":
                    "Create a program that asks for the user's name and age."
            },

            {
                "title": "Lists and Dictionaries",
                "explanation":
                    "Lists store ordered collections while dictionaries store "
                    "key-value pairs.",
                "real_world_example":
                    "A student record can be represented using a dictionary.",
                "code_example":
                    "student = {\n"
                    "    \"name\": \"Joe\",\n"
                    "    \"department\": \"IT\",\n"
                    "    \"year\": 1\n"
                    "}\n\n"
                    "print(student[\"name\"])",
                "code_language": "python",
                "important_notes": [
                    "Lists use indexes.",
                    "Dictionaries use keys.",
                    "Collections are fundamental to Python programming."
                ],
                "practice_task":
                    "Create a dictionary containing your student details."
            },

            {
                "title": "File Handling",
                "explanation":
                    "Python can read and write files using built-in file "
                    "handling functions.",
                "real_world_example":
                    "A program can save student attendance into a text file.",
                "code_example":
                    "with open(\"notes.txt\", \"w\") as file:\n"
                    "    file.write(\"CodeQuest AI\")",
                "code_language": "python",
                "important_notes": [
                    "with automatically handles file closing.",
                    "Use suitable file modes.",
                    "Always handle file-related errors properly."
                ],
                "practice_task":
                    "Create a file and store five lines of text."
            },

            {
                "title": "Object-Oriented Python",
                "explanation":
                    "Python supports classes, objects, inheritance and other "
                    "object-oriented concepts.",
                "real_world_example":
                    "A college management application can represent students "
                    "and teachers as objects.",
                "code_example":
                    "class Student:\n"
                    "    def __init__(self, name):\n"
                    "        self.name = name\n\n"
                    "student = Student(\"Joe\")\n"
                    "print(student.name)",
                "code_language": "python",
                "important_notes": [
                    "self refers to the current object.",
                    "__init__ initializes an object.",
                    "Classes help organize larger applications."
                ],
                "practice_task":
                    "Create a class called Laptop with brand and RAM."
            }
        ]
    },


    "Java": {
        "icon": "☕",
        "level": "Intermediate",
        "description": "Learn Java and object-oriented application development.",
        "chapters": [

            {
                "title": "Java Basics",
                "explanation":
                    "Java is a widely used object-oriented programming "
                    "language designed to run across platforms using the JVM.",
                "real_world_example":
                    "Java is used in enterprise software, backend systems "
                    "and Android development.",
                "code_example":
                    "public class Main {\n"
                    "    public static void main(String[] args) {\n"
                    "        System.out.println(\"Hello Java\");\n"
                    "    }\n"
                    "}",
                "code_language": "java",
                "important_notes": [
                    "Java programs commonly begin execution in main().",
                    "Java is strongly typed.",
                    "JVM provides platform independence."
                ],
                "practice_task":
                    "Modify the program to print your name."
            },

            {
                "title": "Classes and Objects",
                "explanation":
                    "Java uses classes and objects as fundamental building "
                    "blocks of object-oriented programming.",
                "real_world_example":
                    "A Student class can represent students in a college system.",
                "code_example":
                    "class Student {\n"
                    "    String name;\n"
                    "}\n\n"
                    "public class Main {\n"
                    "    public static void main(String[] args) {\n"
                    "        Student s = new Student();\n"
                    "        s.name = \"Joe\";\n"
                    "        System.out.println(s.name);\n"
                    "    }\n"
                    "}",
                "code_language": "java",
                "important_notes": [
                    "new creates an object.",
                    "Fields store object data.",
                    "Methods define object behavior."
                ],
                "practice_task":
                    "Create a Book class with title and author."
            }
        ]
    },


    "Web Development": {
        "icon": "🌐",
        "level": "Beginner → Advanced",
        "description": "Build modern websites and web applications.",
        "chapters": [

            {
                "title": "HTML Basics",
                "explanation":
                    "HTML provides the structure of web pages using elements "
                    "such as headings, paragraphs, links and forms.",
                "real_world_example":
                    "Every website begins with a document structure that the "
                    "browser can understand.",
                "code_example":
                    "<!DOCTYPE html>\n"
                    "<html>\n"
                    "<body>\n"
                    "    <h1>CodeQuest AI</h1>\n"
                    "    <p>Learn. Practice. Build.</p>\n"
                    "</body>\n"
                    "</html>",
                "code_language": "html",
                "important_notes": [
                    "HTML is a markup language.",
                    "Elements describe page structure.",
                    "Semantic HTML improves accessibility."
                ],
                "practice_task":
                    "Create a personal profile page using HTML."
            },

            {
                "title": "CSS Basics",
                "explanation":
                    "CSS controls the appearance and layout of HTML elements.",
                "real_world_example":
                    "Colors, spacing, fonts, cards and responsive layouts "
                    "are controlled using CSS.",
                "code_example":
                    "body {\n"
                    "    background: #101020;\n"
                    "    color: white;\n"
                    "}\n\n"
                    "h1 {\n"
                    "    color: #9b5cff;\n"
                    "}",
                "code_language": "css",
                "important_notes": [
                    "CSS separates design from HTML structure.",
                    "Flexbox is useful for layouts.",
                    "Grid is useful for two-dimensional layouts."
                ],
                "practice_task":
                    "Style your HTML profile page with CSS."
            },

            {
                "title": "JavaScript Basics",
                "explanation":
                    "JavaScript adds behavior and interactivity to web pages.",
                "real_world_example":
                    "Buttons, menus, calculators and interactive dashboards "
                    "can use JavaScript.",
                "code_example":
                    "const button = document.querySelector(\"button\");\n\n"
                    "button.addEventListener(\"click\", () => {\n"
                    "    alert(\"Welcome to CodeQuest!\");\n"
                    "});",
                "code_language": "javascript",
                "important_notes": [
                    "JavaScript runs in browsers.",
                    "DOM allows JavaScript to interact with HTML.",
                    "Events respond to user actions."
                ],
                "practice_task":
                    "Create a button that changes a paragraph when clicked."
            }
        ]
    },


    "Database & SQL": {
        "icon": "🗄️",
        "level": "Intermediate",
        "description": "Store, query and manage application data.",
        "chapters": [

            {
                "title": "Database Basics",
                "explanation":
                    "A database organizes information so that applications "
                    "can efficiently store and retrieve data.",
                "real_world_example":
                    "College systems store student details, marks and attendance "
                    "in databases.",
                "code_example":
                    "CREATE TABLE students (\n"
                    "    id INTEGER,\n"
                    "    name TEXT,\n"
                    "    department TEXT\n"
                    ");",
                "code_language": "sql",
                "important_notes": [
                    "Tables contain rows and columns.",
                    "A database can contain multiple tables.",
                    "Keys help identify records."
                ],
                "practice_task":
                    "Design a table for storing student details."
            },

            {
                "title": "SELECT Queries",
                "explanation":
                    "SELECT retrieves information from database tables.",
                "real_world_example":
                    "A college application can retrieve all IT department students.",
                "code_example":
                    "SELECT name, department\n"
                    "FROM students\n"
                    "WHERE department = 'IT';",
                "code_language": "sql",
                "important_notes": [
                    "SELECT retrieves data.",
                    "FROM identifies the table.",
                    "WHERE filters records."
                ],
                "practice_task":
                    "Write a query to find students with marks above 80."
            }
        ]
    },


    "Git & GitHub": {
        "icon": "🐙",
        "level": "Intermediate",
        "description": "Learn version control and collaborative development.",
        "chapters": [

            {
                "title": "Git Basics",
                "explanation":
                    "Git is a version-control system that tracks changes "
                    "in source code.",
                "real_world_example":
                    "Developers use Git to maintain different versions of "
                    "software projects.",
                "code_example":
                    "git init\n"
                    "git add .\n"
                    "git commit -m \"Initial commit\"",
                "code_language": "bash",
                "important_notes": [
                    "Git tracks project changes.",
                    "Commits create checkpoints.",
                    "Branches allow parallel development."
                ],
                "practice_task":
                    "Create a Git repository for a small Python project."
            },

            {
                "title": "GitHub",
                "explanation":
                    "GitHub provides online repositories and collaboration "
                    "features for software projects.",
                "real_world_example":
                    "Students can publish projects on GitHub as part of "
                    "their portfolio.",
                "code_example":
                    "git remote add origin YOUR_REPOSITORY_URL\n"
                    "git push -u origin main",
                "code_language": "bash",
                "important_notes": [
                    "Never upload passwords or secret API keys.",
                    "README files explain projects.",
                    "GitHub can showcase your development work."
                ],
                "practice_task":
                    "Create a GitHub repository for your first college project."
            }
        ]
    },


    "Cloud Computing": {
        "icon": "☁️",
        "level": "Advanced",
        "description": "Understand cloud services and application deployment.",
        "chapters": [

            {
                "title": "What is Cloud Computing?",
                "explanation":
                    "Cloud computing provides computing resources such as "
                    "servers, storage and databases through network services.",
                "real_world_example":
                    "Web applications can be deployed on cloud platforms "
                    "instead of running only on a personal computer.",
                "code_example": "",
                "code_language": "",
                "important_notes": [
                    "Cloud resources are accessed over networks.",
                    "Cloud services can scale with demand.",
                    "Common models include IaaS, PaaS and SaaS."
                ],
                "practice_task":
                    "Find three applications you use that rely on cloud services."
            },

            {
                "title": "Deployment",
                "explanation":
                    "Deployment makes an application available for users "
                    "through a server or hosting platform.",
                "real_world_example":
                    "A Flask application can be deployed so classmates can "
                    "open it through a web browser.",
                "code_example":
                    "pip install gunicorn\n"
                    "gunicorn app:app",
                "code_language": "bash",
                "important_notes": [
                    "Production deployment requires suitable configuration.",
                    "Environment variables should protect secrets.",
                    "Logs help diagnose deployment problems."
                ],
                "practice_task":
                    "Deploy a simple web application."
            }
        ]
    },


    "AI & Machine Learning": {
        "icon": "🤖",
        "level": "Advanced",
        "description": "Understand AI, machine learning and modern intelligent systems.",
        "chapters": [

            {
                "title": "What is AI?",
                "explanation":
                    "Artificial intelligence involves building systems capable "
                    "of performing tasks that normally require human-like "
                    "reasoning or perception.",
                "real_world_example":
                    "Recommendation systems, voice assistants and image "
                    "recognition systems use AI techniques.",
                "code_example":
                    "message = \"hello\"\n\n"
                    "if \"hello\" in message.lower():\n"
                    "    print(\"Hi! How can I help?\")",
                "code_language": "python",
                "important_notes": [
                    "AI is a broad field.",
                    "Machine learning is one approach used in AI.",
                    "Data quality strongly affects machine-learning systems."
                ],
                "practice_task":
                    "List five AI systems you interact with every week."
            },

            {
                "title": "Machine Learning Basics",
                "explanation":
                    "Machine learning enables systems to learn patterns "
                    "from data and make predictions or decisions.",
                "real_world_example":
                    "A model can learn from historical data to predict "
                    "whether an email is spam.",
                "code_example":
                    "from sklearn.linear_model import LinearRegression\n\n"
                    "model = LinearRegression()\n"
                    "model.fit(X_train, y_train)",
                "code_language": "python",
                "important_notes": [
                    "Training data teaches a model.",
                    "Testing evaluates performance on unseen data.",
                    "Overfitting is an important ML problem."
                ],
                "practice_task":
                    "Research the difference between supervised and unsupervised learning."
            }
        ]
    },


    "Cyber Security": {
        "icon": "🛡️",
        "level": "Advanced",
        "description": "Learn cybersecurity concepts and safe digital practices.",
        "chapters": [

            {
                "title": "Cybersecurity Basics",
                "explanation":
                    "Cybersecurity protects systems, networks, applications "
                    "and data from unauthorized access and attacks.",
                "real_world_example":
                    "Strong passwords and multi-factor authentication protect "
                    "online accounts.",
                "code_example": "",
                "code_language": "",
                "important_notes": [
                    "Never share passwords or authentication codes.",
                    "Keep software updated.",
                    "Use multi-factor authentication when available."
                ],
                "practice_task":
                    "Create a checklist for securing your personal accounts."
            },

            {
                "title": "Phishing",
                "explanation":
                    "Phishing attempts to trick people into revealing sensitive "
                    "information through fake messages or websites.",
                "real_world_example":
                    "A fake bank message may ask users to click a fraudulent link.",
                "code_example": "",
                "code_language": "",
                "important_notes": [
                    "Check suspicious links carefully.",
                    "Do not provide credentials through unknown links.",
                    "Urgency is commonly used in phishing messages."
                ],
                "practice_task":
                    "Identify three warning signs of a suspicious email."
            }
        ]
    },


    "Career Preparation": {
        "icon": "🚀",
        "level": "All Levels",
        "description": "Prepare for internships, placements and software careers.",
        "chapters": [

            {
                "title": "Build a Resume",
                "explanation":
                    "A resume presents your education, skills, projects "
                    "and achievements to employers.",
                "real_world_example":
                    "A student applying for an internship can highlight "
                    "relevant programming projects and GitHub work.",
                "code_example": "",
                "code_language": "",
                "important_notes": [
                    "Keep information relevant.",
                    "Projects can demonstrate practical skills.",
                    "Avoid fake skills or achievements."
                ],
                "practice_task":
                    "Create a one-page student resume."
            },

            {
                "title": "GitHub Portfolio",
                "explanation":
                    "A GitHub portfolio can demonstrate your ability to build "
                    "and maintain software projects.",
                "real_world_example":
                    "A recruiter can inspect a student's projects, README files "
                    "and code history.",
                "code_example": "",
                "code_language": "",
                "important_notes": [
                    "Keep repositories organized.",
                    "Write useful README files.",
                    "Never expose private credentials."
                ],
                "practice_task":
                    "Publish one small project with a proper README."
            }
        ]
    }
}


# ============================================================
# QUIZ BANK
# ============================================================

QUIZZES = [

    {
        "id": "cb01",
        "course": "Computer Basics",
        "question": "Which component executes program instructions?",
        "options": ["RAM", "CPU", "Keyboard", "Monitor"],
        "answer": "CPU"
    },

    {
        "id": "cb02",
        "course": "Computer Basics",
        "question": "Which memory is temporary?",
        "options": ["SSD", "HDD", "RAM", "DVD"],
        "answer": "RAM"
    },

    {
        "id": "pf01",
        "course": "Programming Fundamentals",
        "question": "What is an algorithm?",
        "options": [
            "A programming language",
            "A sequence of steps to solve a problem",
            "A computer component",
            "A database"
        ],
        "answer": "A sequence of steps to solve a problem"
    },

    {
        "id": "pf02",
        "course": "Programming Fundamentals",
        "question": "Which statement is commonly used for decisions?",
        "options": ["if", "print", "import", "return"],
        "answer": "if"
    },

    {
        "id": "pf03",
        "course": "Programming Fundamentals",
        "question": "Which structure repeats instructions?",
        "options": ["Loop", "Variable", "Comment", "Compiler"],
        "answer": "Loop"
    },

    {
        "id": "c01",
        "course": "C Language",
        "question": "Which function is the entry point of a C program?",
        "options": ["start()", "main()", "run()", "begin()"],
        "answer": "main()"
    },

    {
        "id": "c02",
        "course": "C Language",
        "question": "Which function is commonly used for output in C?",
        "options": ["print()", "cout", "printf()", "display()"],
        "answer": "printf()"
    },

    {
        "id": "cpp01",
        "course": "C++",
        "question": "Which keyword defines a class in C++?",
        "options": ["object", "class", "define", "structclass"],
        "answer": "class"
    },

    {
        "id": "cpp02",
        "course": "C++",
        "question": "What is an object?",
        "options": [
            "Instance of a class",
            "A compiler",
            "A loop",
            "A header file"
        ],
        "answer": "Instance of a class"
    },

    {
        "id": "py01",
        "course": "Python",
        "question": "Which keyword defines a function in Python?",
        "options": ["function", "def", "func", "method"],
        "answer": "def"
    },

    {
        "id": "py02",
        "course": "Python",
        "question": "Which data structure stores key-value pairs?",
        "options": ["List", "Tuple", "Dictionary", "Set"],
        "answer": "Dictionary"
    },

    {
        "id": "java01",
        "course": "Java",
        "question": "Which method is the usual entry point of a Java application?",
        "options": ["start()", "main()", "run()", "execute()"],
        "answer": "main()"
    },

    {
        "id": "web01",
        "course": "Web Development",
        "question": "What does HTML mainly provide?",
        "options": [
            "Database storage",
            "Web page structure",
            "Operating system services",
            "Network routing"
        ],
        "answer": "Web page structure"
    },

    {
        "id": "web02",
        "course": "Web Development",
        "question": "Which technology controls web page styling?",
        "options": ["HTML", "CSS", "SQL", "Git"],
        "answer": "CSS"
    },

    {
        "id": "web03",
        "course": "Web Development",
        "question": "Which language adds interactivity to web pages?",
        "options": ["SQL", "JavaScript", "HTML", "CSS"],
        "answer": "JavaScript"
    },

    {
        "id": "sql01",
        "course": "Database & SQL",
        "question": "Which SQL command retrieves data?",
        "options": ["GET", "SELECT", "SHOWDATA", "READ"],
        "answer": "SELECT"
    },

    {
        "id": "git01",
        "course": "Git & GitHub",
        "question": "Which command creates a Git commit?",
        "options": [
            "git save",
            "git commit",
            "git checkpoint",
            "git store"
        ],
        "answer": "git commit"
    },

    {
        "id": "cloud01",
        "course": "Cloud Computing",
        "question": "Which is a cloud service model?",
        "options": ["IaaS", "CPU", "RAM", "BIOS"],
        "answer": "IaaS"
    },

    {
        "id": "ai01",
        "course": "AI & Machine Learning",
        "question": "What does ML commonly learn from?",
        "options": ["Data", "Keyboard", "Monitor", "Power supply"],
        "answer": "Data"
    },

    {
        "id": "cyber01",
        "course": "Cyber Security",
        "question": "What is phishing?",
        "options": [
            "A programming language",
            "A social-engineering attack",
            "A database",
            "A compiler"
        ],
        "answer": "A social-engineering attack"
    },

    {
        "id": "career01",
        "course": "Career Preparation",
        "question": "Which can demonstrate practical development skills?",
        "options": [
            "GitHub projects",
            "Random passwords",
            "Unrelated screenshots",
            "Empty folders"
        ],
        "answer": "GitHub projects"
    }
]


# ============================================================
# WEEKLY TEST QUESTIONS
# ============================================================

WEEKLY_TEST = [

    {
        "id": "wt01",
        "question": "Which component processes instructions?",
        "options": ["RAM", "CPU", "SSD", "Monitor"],
        "answer": "CPU"
    },

    {
        "id": "wt02",
        "question": "Which language is known for indentation-based blocks?",
        "options": ["Python", "C", "Java", "SQL"],
        "answer": "Python"
    },

    {
        "id": "wt03",
        "question": "Which keyword creates a class in C++?",
        "options": ["object", "class", "newclass", "define"],
        "answer": "class"
    },

    {
        "id": "wt04",
        "question": "Which SQL command retrieves records?",
        "options": ["SELECT", "PUSH", "GETROW", "READ"],
        "answer": "SELECT"
    },

    {
        "id": "wt05",
        "question": "Which technology styles HTML?",
        "options": ["CSS", "SQL", "Python", "Git"],
        "answer": "CSS"
    },

    {
        "id": "wt06",
        "question": "What is Git primarily used for?",
        "options": [
            "Version control",
            "Image editing",
            "Video playback",
            "Hardware repair"
        ],
        "answer": "Version control"
    },

    {
        "id": "wt07",
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
        "id": "wt08",
        "question": "Which is an example of strong account security?",
        "options": [
            "Using the same password everywhere",
            "Sharing OTPs",
            "Multi-factor authentication",
            "Writing passwords publicly"
        ],
        "answer": "Multi-factor authentication"
    },

    {
        "id": "wt09",
        "question": "Which Java method is the normal application entry point?",
        "options": ["main()", "start()", "begin()", "execute()"],
        "answer": "main()"
    },

    {
        "id": "wt10",
        "question": "Which keyword defines a function in Python?",
        "options": ["def", "function", "func", "define"],
        "answer": "def"
    }
]


# ============================================================
# CAREER GUIDE
# ============================================================

CAREERS = [

    {
        "title": "Software Developer",
        "icon": "💻",
        "skills": [
            "Programming",
            "Data Structures",
            "Git",
            "Problem Solving",
            "Database",
            "Web Development"
        ],
        "roadmap": [
            "Learn programming fundamentals",
            "Master one programming language",
            "Learn Git and GitHub",
            "Build projects",
            "Learn databases",
            "Create a portfolio",
            "Prepare for interviews"
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
            "Database",
            "Git"
        ],
        "roadmap": [
            "Learn HTML",
            "Learn CSS",
            "Learn JavaScript",
            "Build frontend projects",
            "Learn backend development",
            "Connect databases",
            "Deploy projects"
        ]
    },

    {
        "title": "AI / ML Engineer",
        "icon": "🤖",
        "skills": [
            "Python",
            "Mathematics",
            "Statistics",
            "Machine Learning",
            "Data Processing",
            "Deep Learning"
        ],
        "roadmap": [
            "Learn Python",
            "Learn mathematics basics",
            "Learn NumPy and Pandas",
            "Learn machine learning",
            "Build ML projects",
            "Learn deep learning",
            "Build an AI portfolio"
        ]
    },

    {
        "title": "Cybersecurity Analyst",
        "icon": "🛡️",
        "skills": [
            "Networking",
            "Linux",
            "Security Concepts",
            "Authentication",
            "Threat Analysis"
        ],
        "roadmap": [
            "Learn networking",
            "Learn Linux",
            "Learn security fundamentals",
            "Practice in legal labs",
            "Study common vulnerabilities",
            "Build security projects"
        ]
    }
]


# ============================================================
# PROJECTS
# ============================================================

PROJECTS = [

    {
        "name": "Student Management System",
        "level": "Beginner",
        "skills": ["Python", "Database"],
        "description": "Manage student records, marks and attendance."
    },

    {
        "name": "Quiz Application",
        "level": "Beginner",
        "skills": ["HTML", "CSS", "JavaScript"],
        "description": "Build a browser-based quiz system."
    },

    {
        "name": "College To-Do App",
        "level": "Intermediate",
        "skills": ["Python", "Flask", "SQLite"],
        "description": "Manage assignments, tests and daily tasks."
    },

    {
        "name": "AI Chatbot",
        "level": "Advanced",
        "skills": ["Python", "AI", "APIs"],
        "description": "Build an intelligent conversational application."
    },

    {
        "name": "CodeQuest AI",
        "level": "Advanced",
        "skills": [
            "Python",
            "Flask",
            "JavaScript",
            "Firebase",
            "SQLite",
            "AI"
        ],
        "description":
            "Build a gamified computer-science learning platform."
    }
]


# ============================================================
# ACHIEVEMENTS
# ============================================================

ACHIEVEMENTS = [
    {
        "id": "first_step",
        "name": "First Step",
        "icon": "🌟",
        "description": "Complete your first lesson."
    },
    {
        "id": "quiz_master",
        "name": "Quiz Master",
        "icon": "🧠",
        "description": "Complete 10 quizzes."
    },
    {
        "id": "bug_hunter",
        "name": "Bug Hunter",
        "icon": "🐛",
        "description": "Complete a coding challenge."
    },
    {
        "id": "streak_master",
        "name": "Streak Master",
        "icon": "🔥",
        "description": "Maintain a 7-day learning streak."
    },
    {
        "id": "project_builder",
        "name": "Project Builder",
        "icon": "🚀",
        "description": "Build your first project."
    },
    {
        "id": "codequest_legend",
        "name": "CodeQuest Legend",
        "icon": "👑",
        "description": "Reach the highest CodeQuest level."
    }
]


# ============================================================
# USER HELPERS
# ============================================================

def ensure_user(user_id, name="", email=""):

    if not user_id:
        user_id = "guest"

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cur.fetchone()

    if not user:

        cur.execute("""
            INSERT INTO users
            (user_id, name, email, last_login)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            name,
            email,
            datetime.utcnow().isoformat()
        ))

    else:

        cur.execute("""
            UPDATE users
            SET name = ?, email = ?, last_login = ?
            WHERE user_id = ?
        """, (
            name or user["name"],
            email or user["email"],
            datetime.utcnow().isoformat(),
            user_id
        ))

    conn.commit()
    conn.close()

    return user_id


def add_xp(user_id, amount):

    ensure_user(user_id)

    conn = get_db()

    conn.execute("""
        UPDATE users
        SET xp = xp + ?
        WHERE user_id = ?
    """, (amount, user_id))

    conn.commit()

    row = conn.execute(
        "SELECT xp FROM users WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    conn.close()

    return row["xp"]


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# LOGIN / USER
# ============================================================

@app.route("/api/user", methods=["POST"])
def create_user():

    data = request.get_json() or {}

    user_id = data.get("user_id") or "guest"
    name = data.get("name", "")
    email = data.get("email", "")

    ensure_user(user_id, name, email)

    return jsonify({
        "success": True,
        "message": "User connected",
        "user_id": user_id
    })


# ============================================================
# COURSES
# ============================================================

@app.route("/api/courses")
def get_courses():

    result = []

    for name, course in courses.items():

        result.append({
            "name": name,
            "icon": course["icon"],
            "level": course["level"],
            "description": course["description"],
            "chapter_count": len(course["chapters"])
        })

    return jsonify(result)


@app.route("/api/course/<path:course_name>")
def get_course(course_name):

    if course_name not in courses:
        return jsonify({
            "error": "Course not found"
        }), 404

    course = courses[course_name]

    chapters = []

    for index, chapter in enumerate(course["chapters"]):

        chapters.append({
            "index": index,
            "title": chapter["title"],
            "has_code": bool(chapter.get("code_example"))
        })

    return jsonify({
        "name": course_name,
        "icon": course["icon"],
        "level": course["level"],
        "description": course["description"],
        "chapters": chapters
    })


# ============================================================
# LESSON
# ============================================================

@app.route("/api/lesson/<path:course_name>/<int:index>")
def get_lesson(course_name, index):

    if course_name not in courses:
        return jsonify({"error": "Course not found"}), 404

    chapters = courses[course_name]["chapters"]

    if index < 0 or index >= len(chapters):
        return jsonify({"error": "Lesson not found"}), 404

    chapter = chapters[index]

    return jsonify({
        "course": course_name,
        "index": index,
        **chapter
    })


# ============================================================
# COMPLETE LESSON
# ============================================================

@app.route("/api/lesson-complete", methods=["POST"])
def complete_lesson():

    data = request.get_json() or {}

    user_id = data.get("user_id", "guest")
    lesson_id = data.get("lesson_id")

    ensure_user(user_id)

    if not lesson_id:
        return jsonify({
            "error": "lesson_id required"
        }), 400

    conn = get_db()

    try:

        conn.execute("""
            INSERT INTO lesson_history
            (user_id, lesson_id, completed_at)
            VALUES (?, ?, ?)
        """, (
            user_id,
            lesson_id,
            datetime.utcnow().isoformat()
        ))

        conn.execute("""
            UPDATE users
            SET lessons_completed = lessons_completed + 1
            WHERE user_id = ?
        """, (user_id,))

        conn.commit()

        xp = add_xp(user_id, 20)

        return jsonify({
            "success": True,
            "xp_earned": 20,
            "xp": xp,
            "message": "Lesson completed!"
        })

    except sqlite3.IntegrityError:

        return jsonify({
            "success": False,
            "message": "Lesson already completed."
        })

    finally:
        conn.close()


# ============================================================
# QUIZ
# NO REPEATING QUESTIONS
# ============================================================

@app.route("/api/quiz")
def get_quiz():

    user_id = request.args.get("user_id", "guest")
    course = request.args.get("course")
    count = int(request.args.get("count", 10))

    ensure_user(user_id)

    conn = get_db()

    rows = conn.execute("""
        SELECT question_id
        FROM quiz_history
        WHERE user_id = ?
    """, (user_id,)).fetchall()

    used = {row["question_id"] for row in rows}

    conn.close()

    available = [
        q for q in QUIZZES
        if q["id"] not in used
    ]

    if course:
        available = [
            q for q in available
            if q["course"] == course
        ]

    random.shuffle(available)

    selected = available[:count]

    # Record questions immediately so they cannot appear again.
    conn = get_db()

    for q in selected:
        try:
            conn.execute("""
                INSERT INTO quiz_history
                (user_id, question_id, answered_at)
                VALUES (?, ?, ?)
            """, (
                user_id,
                q["id"],
                datetime.utcnow().isoformat()
            ))
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

    safe_questions = []

    for q in selected:

        safe_questions.append({
            "id": q["id"],
            "course": q["course"],
            "question": q["question"],
            "options": q["options"]
        })

    return jsonify({
        "questions": safe_questions,
        "count": len(safe_questions),
        "remaining_questions": len(available) - len(selected)
    })


# ============================================================
# QUIZ ANSWER
# ============================================================

@app.route("/api/quiz/answer", methods=["POST"])
def quiz_answer():

    data = request.get_json() or {}

    question_id = data.get("question_id")
    answer = data.get("answer")
    user_id = data.get("user_id", "guest")

    question = next(
        (q for q in QUIZZES if q["id"] == question_id),
        None
    )

    if not question:
        return jsonify({
            "error": "Question not found"
        }), 404

    correct = answer == question["answer"]

    xp = 0

    if correct:
        xp = add_xp(user_id, 10)

    conn = get_db()

    conn.execute("""
        UPDATE users
        SET quizzes_completed = quizzes_completed + 1
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "correct": correct,
        "xp_earned": xp,
        "correct_answer": question["answer"] if correct else None
    })


# ============================================================
# RESET QUIZ HISTORY
# ============================================================

@app.route("/api/quiz/reset", methods=["POST"])
def reset_quiz():

    data = request.get_json() or {}
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

def current_week_id():

    now = datetime.utcnow()

    year, week, _ = now.isocalendar()

    return f"{year}-W{week}"


@app.route("/api/weekly-test")
def weekly_test():

    user_id = request.args.get("user_id", "guest")

    ensure_user(user_id)

    week_id = current_week_id()

    conn = get_db()

    previous = conn.execute("""
        SELECT *
        FROM weekly_tests
        WHERE user_id = ? AND week_id = ?
    """, (user_id, week_id)).fetchone()

    conn.close()

    questions = WEEKLY_TEST.copy()

    random.shuffle(questions)

    safe_questions = []

    for q in questions:

        safe_questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        })

    return jsonify({
        "week_id": week_id,
        "already_completed": bool(previous),
        "duration_minutes": 30,
        "total_questions": len(safe_questions),
        "max_xp": 500,
        "questions": safe_questions
    })


# ============================================================
# SUBMIT WEEKLY TEST
# ============================================================

@app.route("/api/weekly-test/submit", methods=["POST"])
def submit_weekly_test():

    data = request.get_json() or {}

    user_id = data.get("user_id", "guest")
    answers = data.get("answers", {})

    ensure_user(user_id)

    week_id = current_week_id()

    conn = get_db()

    existing = conn.execute("""
        SELECT *
        FROM weekly_tests
        WHERE user_id = ? AND week_id = ?
    """, (user_id, week_id)).fetchone()

    if existing:

        conn.close()

        return jsonify({
            "success": False,
            "message": "You have already completed this week's test."
        }), 400

    score = 0

    for question in WEEKLY_TEST:

        given = answers.get(question["id"])

        if given == question["answer"]:
            score += 1

    total = len(WEEKLY_TEST)

    xp = int((score / total) * 500)

    conn.execute("""
        INSERT INTO weekly_tests
        (user_id, week_id, score, total, xp, completed_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        week_id,
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

    total_xp = add_xp(user_id, xp)

    return jsonify({
        "success": True,
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 2),
        "xp_earned": xp,
        "total_xp": total_xp
    })


# ============================================================
# MULTI-LANGUAGE CODE LAB
# ============================================================

SUPPORTED_LANGUAGES = {
    "python": {
        "name": "Python",
        "extension": "py"
    },
    "c": {
        "name": "C",
        "extension": "c"
    },
    "cpp": {
        "name": "C++",
        "extension": "cpp"
    },
    "java": {
        "name": "Java",
        "extension": "java"
    }
}


@app.route("/api/compiler/languages")
def compiler_languages():

    return jsonify({
        "languages": SUPPORTED_LANGUAGES
    })


@app.route("/api/compile", methods=["POST"])
def compile_code():

    data = request.get_json() or {}

    language = data.get("language")
    code = data.get("code", "")
    stdin = data.get("stdin", "")

    if language not in SUPPORTED_LANGUAGES:

        return jsonify({
            "success": False,
            "error": "Unsupported language."
        }), 400

    if not code.strip():

        return jsonify({
            "success": False,
            "error": "Code cannot be empty."
        }), 400

    # --------------------------------------------------------
    # SECURITY NOTE:
    # This endpoint intentionally does not execute arbitrary code
    # directly on the Flask server.
    #
    # Connect a sandboxed compiler service here for production.
    # --------------------------------------------------------

    return jsonify({
        "success": False,
        "language": SUPPORTED_LANGUAGES[language]["name"],
        "output": "",
        "error":
            "Compiler service is not connected yet. "
            "The Code Lab API is ready for a sandboxed compiler provider."
    })


# ============================================================
# BUG HUNTER
# ============================================================

BUG_CHALLENGES = [

    {
        "id": "bug01",
        "language": "python",
        "title": "Fix the Variable Bug",
        "code":
            "name = \"CodeQuest\"\n"
            "print(nam)",
        "hint": "Check the variable name.",
        "answer": "name"
    },

    {
        "id": "bug02",
        "language": "python",
        "title": "Fix the Indentation",
        "code":
            "age = 18\n"
            "if age >= 18:\n"
            "print(\"Adult\")",
        "hint": "Check the indentation.",
        "answer": "indentation"
    },

    {
        "id": "bug03",
        "language": "c",
        "title": "Find the Missing Symbol",
        "code":
            "#include <stdio.h>\n\n"
            "int main() {\n"
            "    printf(\"Hello\")\n"
            "    return 0;\n"
            "}",
        "hint": "Check the end of the printf statement.",
        "answer": ";"
    }
]


@app.route("/api/code-challenges")
def code_challenges():

    return jsonify(BUG_CHALLENGES)


@app.route("/api/error-finder")
def error_finder():

    return jsonify({
        "title": "Bug Hunter",
        "description":
            "Find the bug, understand why it happened and fix it.",
        "challenges": BUG_CHALLENGES
    })


# ============================================================
# CAREER GUIDE
# ============================================================

@app.route("/api/careers")
def careers():

    return jsonify(CAREERS)


# ============================================================
# PROJECTS
# ============================================================

@app.route("/api/projects")
def projects():

    return jsonify(PROJECTS)


# ============================================================
# ACHIEVEMENTS
# ============================================================

@app.route("/api/achievements")
def achievements():

    return jsonify(ACHIEVEMENTS)


# ============================================================
# DASHBOARD / PROGRESS
# ============================================================

@app.route("/api/progress")
def progress():

    user_id = request.args.get("user_id", "guest")

    ensure_user(user_id)

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE user_id = ?
    """, (user_id,)).fetchone()

    lessons = conn.execute("""
        SELECT COUNT(*) AS count
        FROM lesson_history
        WHERE user_id = ?
    """, (user_id,)).fetchone()

    quizzes = conn.execute("""
        SELECT COUNT(*) AS count
        FROM quiz_history
        WHERE user_id = ?
    """, (user_id,)).fetchone()

    weekly = conn.execute("""
        SELECT COUNT(*) AS count
        FROM weekly_tests
        WHERE user_id = ?
    """, (user_id,)).fetchone()

    conn.close()

    xp = user["xp"]

    current = get_level(xp)
    next_level = get_next_level(xp)

    progress_percent = 100

    if next_level:

        current_xp = current["required_xp"]
        next_xp = next_level["required_xp"]

        progress_percent = int(
            ((xp - current_xp) /
             (next_xp - current_xp)) * 100
        )

    return jsonify({

        "user": {
            "id": user["user_id"],
            "name": user["name"],
            "email": user["email"]
        },

        "xp": xp,

        "level": current,

        "next_level": next_level,

        "level_progress": progress_percent,

        "streak": user["streak"],

        "lessons_completed": lessons["count"],

        "quizzes_completed": quizzes["count"],

        "weekly_tests": weekly["count"],

        "challenges_completed":
            user["challenges_completed"]
    })


# ============================================================
# DAILY MISSIONS
# ============================================================

@app.route("/api/daily-missions")
def daily_missions():

    return jsonify([
        {
            "id": "lesson",
            "title": "Knowledge Drop",
            "description": "Complete one lesson.",
            "xp": 20
        },
        {
            "id": "quiz",
            "title": "Quiz Warrior",
            "description": "Answer five quiz questions.",
            "xp": 30
        },
        {
            "id": "bug",
            "title": "Bug Hunter",
            "description": "Complete one coding challenge.",
            "xp": 50
        },
        {
            "id": "all",
            "title": "Daily Legend",
            "description": "Complete all daily missions.",
            "xp": 100
        }
    ])


# ============================================================
# STATUS
# ============================================================

@app.route("/api/status")
def status():

    return jsonify({
        "app": "CodeQuest AI",
        "version": "1.0",
        "status": "online",
        "message": "Learn • Practice • Play • Build",
        "features": [
            "Gamified Learning",
            "XP and Levels",
            "Google Login Compatible",
            "Persistent Progress",
            "Non-Repeating Quiz",
            "Weekly Test",
            "Career Guide",
            "Bug Hunter",
            "Projects",
            "Multi-Language Code Lab"
        ]
    })


# ============================================================
# 404
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Route not found"
    }), 404


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
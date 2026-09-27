from flask import Flask, render_template, jsonify, request, session
from functools import wraps
from datetime import datetime, timezone
import os
import random
import secrets
import time

app = Flask(__name__)

# =========================================================
# CODEQUEST AI V0.5
# SMART LEARNING + PRACTICE + SECURE TEST ENGINE
# =========================================================

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    secrets.token_hex(32)
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Render uses HTTPS in production.
app.config["SESSION_COOKIE_SECURE"] = (
    os.environ.get("FLASK_ENV") == "production"
)


# =========================================================
# COURSE DATABASE
# =========================================================

courses = {

    "Computer Basics": {
        "icon": "💻",
        "level": "Beginner → Intermediate",
        "description": "Understand computers from the absolute basics to practical computer skills.",
        "chapters": [
            "What is a Computer?",
            "History of Computers",
            "Types of Computers",
            "Computer Generations",
            "Hardware and Software",
            "CPU",
            "RAM and ROM",
            "Storage Devices",
            "Motherboard",
            "Input Devices",
            "Output Devices",
            "Ports and Connectors",
            "Operating Systems",
            "Files and Folders",
            "File Extensions",
            "Installing Software",
            "Uninstalling Software",
            "Computer Networks",
            "Internet Basics",
            "Web Browsers",
            "Search Engines",
            "Email Basics",
            "Cloud Storage",
            "Computer Security",
            "Passwords and Authentication",
            "Malware",
            "Phishing",
            "Safe Browsing",
            "Backup and Recovery",
            "Practical Computer Skills",
            "Computer Basics Final Challenge"
        ]
    },

    "MS Word": {
        "icon": "📝",
        "level": "Beginner → Advanced",
        "description": "Learn document creation, formatting, tables, images and professional document design.",
        "chapters": [
            "Introduction to MS Word",
            "Word Interface",
            "Creating a Document",
            "Saving and Opening Documents",
            "Typing and Editing",
            "Selecting Text",
            "Copy Cut and Paste",
            "Font Formatting",
            "Paragraph Formatting",
            "Alignment",
            "Line Spacing",
            "Bullets and Numbering",
            "Styles",
            "Page Setup",
            "Margins",
            "Headers and Footers",
            "Page Numbers",
            "Tables",
            "Table Formatting",
            "Images",
            "Shapes",
            "Text Boxes",
            "WordArt",
            "Hyperlinks",
            "Find and Replace",
            "Spelling and Grammar",
            "References",
            "Footnotes",
            "Table of Contents",
            "Mail Merge",
            "Printing Documents",
            "Professional Resume Project"
        ]
    },

    "MS Excel": {
        "icon": "📊",
        "level": "Beginner → Advanced",
        "description": "Master spreadsheets, formulas, functions, charts, filtering and data analysis.",
        "chapters": [
            "Introduction to Excel",
            "Excel Interface",
            "Workbooks and Worksheets",
            "Cells Rows and Columns",
            "Data Entry",
            "Editing Data",
            "Cell Formatting",
            "Number Formats",
            "Basic Formulas",
            "Arithmetic Operators",
            "Relative References",
            "Absolute References",
            "SUM Function",
            "AVERAGE Function",
            "MIN and MAX",
            "COUNT and COUNTA",
            "IF Function",
            "AND and OR",
            "Nested IF",
            "Text Functions",
            "Date Functions",
            "Sorting Data",
            "Filtering Data",
            "Conditional Formatting",
            "Tables",
            "Charts",
            "Pivot Tables",
            "Data Validation",
            "Removing Duplicates",
            "Basic Data Analysis",
            "Excel Productivity",
            "Practical Excel Project"
        ]
    },

    "MS PowerPoint": {
        "icon": "📽️",
        "level": "Beginner → Advanced",
        "description": "Create professional presentations with slides, graphics, animations and presentations.",
        "chapters": [
            "Introduction to PowerPoint",
            "PowerPoint Interface",
            "Creating Presentations",
            "Slides and Layouts",
            "Themes",
            "Text Formatting",
            "Images",
            "Shapes",
            "Icons",
            "SmartArt",
            "Tables",
            "Charts",
            "Transitions",
            "Animations",
            "Audio and Video",
            "Hyperlinks",
            "Speaker Notes",
            "Slide Master",
            "Presentation Design",
            "Presentation Delivery",
            "Professional Presentation Project"
        ]
    },

    "MS Office": {
        "icon": "📑",
        "level": "Beginner → Advanced",
        "description": "Understand the complete Microsoft Office productivity environment.",
        "chapters": [
            "What is MS Office?",
            "Word Fundamentals",
            "Excel Fundamentals",
            "PowerPoint Fundamentals",
            "Office File Formats",
            "Document Management",
            "Data Management",
            "Presentation Skills",
            "Office Productivity",
            "Professional Office Workflow",
            "Mini Office Project"
        ]
    },

    "Programming Fundamentals": {
        "icon": "🧠",
        "level": "Beginner → Intermediate",
        "description": "Build strong programming logic before moving into advanced programming languages.",
        "chapters": [
            "What is Programming?",
            "Programming Languages",
            "Source Code",
            "Compiler and Interpreter",
            "Algorithms",
            "Flowcharts",
            "Pseudocode",
            "Variables",
            "Constants",
            "Data Types",
            "Operators",
            "Arithmetic Operators",
            "Comparison Operators",
            "Logical Operators",
            "Conditions",
            "if Statement",
            "if else",
            "Nested Conditions",
            "Loops",
            "for Loop",
            "while Loop",
            "Nested Loops",
            "break and continue",
            "Functions",
            "Parameters",
            "Return Values",
            "Arrays",
            "Strings",
            "Problem Solving",
            "Debugging",
            "Testing",
            "Programming Final Challenge"
        ]
    },

    "C Language": {
        "icon": "🔵",
        "level": "Beginner → Advanced",
        "description": "Learn C step-by-step from your first program to pointers, structures and file handling.",
        "chapters": [
            "Introduction to C",
            "History of C",
            "Structure of a C Program",
            "Header Files",
            "main Function",
            "Comments",
            "Variables",
            "Constants",
            "Data Types",
            "Format Specifiers",
            "Input and Output",
            "printf",
            "scanf",
            "Operators",
            "Arithmetic Operators",
            "Relational Operators",
            "Logical Operators",
            "Assignment Operators",
            "if Statement",
            "if else",
            "Nested if",
            "else if Ladder",
            "switch Statement",
            "for Loop",
            "while Loop",
            "do while Loop",
            "Nested Loops",
            "break and continue",
            "Arrays",
            "One Dimensional Arrays",
            "Two Dimensional Arrays",
            "Strings",
            "String Functions",
            "Functions",
            "Function Arguments",
            "Return Values",
            "Recursion",
            "Pointers",
            "Pointer Arithmetic",
            "Arrays and Pointers",
            "Strings and Pointers",
            "Structures",
            "Unions",
            "Enumerations",
            "Dynamic Memory",
            "malloc and calloc",
            "realloc and free",
            "File Handling",
            "Preprocessor",
            "Command Line Arguments",
            "Debugging C Programs",
            "C Mini Project",
            "Final C Challenge"
        ]
    },

    "C++": {
        "icon": "🟣",
        "level": "Beginner → Advanced",
        "description": "Learn modern C++ programming and object-oriented programming concepts.",
        "chapters": [
            "Introduction to C++",
            "C++ and C",
            "Basic Syntax",
            "Comments",
            "Variables",
            "Data Types",
            "Input and Output",
            "Operators",
            "Conditions",
            "Loops",
            "Arrays",
            "Strings",
            "Functions",
            "Function Overloading",
            "References",
            "Pointers",
            "Classes",
            "Objects",
            "Access Specifiers",
            "Constructors",
            "Destructors",
            "this Pointer",
            "Inheritance",
            "Types of Inheritance",
            "Polymorphism",
            "Function Overriding",
            "Virtual Functions",
            "Encapsulation",
            "Abstraction",
            "Friend Functions",
            "Operator Overloading",
            "Templates",
            "Exception Handling",
            "STL",
            "Vectors",
            "Maps",
            "Sets",
            "Iterators",
            "File Handling",
            "C++ Mini Projects",
            "Final C++ Challenge"
        ]
    },

    "OOP Concepts": {
        "icon": "🧩",
        "level": "Intermediate",
        "description": "Master object-oriented thinking used in modern software development.",
        "chapters": [
            "What is OOP?",
            "Why OOP?",
            "Classes",
            "Objects",
            "Attributes",
            "Methods",
            "Constructors",
            "Destructors",
            "Encapsulation",
            "Access Modifiers",
            "Inheritance",
            "Single Inheritance",
            "Multilevel Inheritance",
            "Multiple Inheritance",
            "Hierarchical Inheritance",
            "Polymorphism",
            "Compile Time Polymorphism",
            "Runtime Polymorphism",
            "Method Overloading",
            "Method Overriding",
            "Abstraction",
            "Interfaces",
            "Association",
            "Aggregation",
            "Composition",
            "Real World OOP",
            "OOP Design Thinking",
            "OOP Mini Project"
        ]
    },

    "Python": {
        "icon": "🐍",
        "level": "Beginner → Advanced",
        "description": "Learn Python from zero to real-world programming and projects.",
        "chapters": [
            "Introduction to Python",
            "Installing Python",
            "Python Syntax",
            "Comments",
            "Variables",
            "Naming Rules",
            "Numbers",
            "Strings",
            "Boolean Values",
            "Input",
            "Output",
            "Type Conversion",
            "Arithmetic Operators",
            "Comparison Operators",
            "Logical Operators",
            "Assignment Operators",
            "if Statement",
            "if else",
            "elif",
            "Nested Conditions",
            "for Loop",
            "while Loop",
            "break",
            "continue",
            "Lists",
            "List Methods",
            "Tuples",
            "Sets",
            "Dictionaries",
            "Dictionary Methods",
            "String Methods",
            "Functions",
            "Parameters",
            "Return Values",
            "Scope",
            "Lambda Functions",
            "Modules",
            "Packages",
            "File Handling",
            "Reading Files",
            "Writing Files",
            "Exception Handling",
            "Debugging",
            "Object Oriented Python",
            "Classes",
            "Objects",
            "Inheritance",
            "Polymorphism",
            "Libraries",
            "APIs",
            "Python Mini Projects",
            "Final Python Challenge"
        ]
    },

    "Java": {
        "icon": "☕",
        "level": "Beginner → Advanced",
        "description": "Learn Java programming, OOP, collections, exceptions and practical development.",
        "chapters": [
            "Introduction to Java",
            "Java Features",
            "JDK JRE and JVM",
            "Java Program Structure",
            "Variables",
            "Data Types",
            "Input and Output",
            "Operators",
            "Conditions",
            "Loops",
            "Arrays",
            "Strings",
            "Methods",
            "Method Overloading",
            "Classes",
            "Objects",
            "Constructors",
            "this Keyword",
            "Inheritance",
            "Polymorphism",
            "Method Overriding",
            "Interfaces",
            "Abstract Classes",
            "Encapsulation",
            "Packages",
            "Exception Handling",
            "Collections",
            "ArrayList",
            "HashMap",
            "HashSet",
            "File Handling",
            "Multithreading Basics",
            "Java Mini Projects",
            "Final Java Challenge"
        ]
    },

    "HTML": {
        "icon": "🌐",
        "level": "Beginner → Advanced",
        "description": "Build the structure of modern websites using HTML.",
        "chapters": [
            "What is HTML?",
            "HTML Document Structure",
            "HTML Tags",
            "HTML Elements",
            "Headings",
            "Paragraphs",
            "Links",
            "Images",
            "Lists",
            "Tables",
            "Forms",
            "Input Elements",
            "Buttons",
            "Labels",
            "Semantic HTML",
            "Audio",
            "Video",
            "Iframes",
            "HTML Attributes",
            "Classes and IDs",
            "Meta Tags",
            "Accessibility Basics",
            "SEO Basics",
            "HTML Best Practices",
            "HTML Mini Project"
        ]
    },

    "CSS": {
        "icon": "🎨",
        "level": "Beginner → Advanced",
        "description": "Learn how to design modern responsive websites with CSS.",
        "chapters": [
            "What is CSS?",
            "CSS Syntax",
            "Selectors",
            "Colors",
            "Backgrounds",
            "Fonts",
            "Text Styling",
            "Borders",
            "Margins",
            "Padding",
            "Box Model",
            "Width and Height",
            "Display",
            "Position",
            "Flexbox",
            "Grid",
            "Responsive Design",
            "Media Queries",
            "Transitions",
            "Animations",
            "Pseudo Classes",
            "Pseudo Elements",
            "CSS Variables",
            "Modern UI Design",
            "CSS Mini Project"
        ]
    },

    "JavaScript": {
        "icon": "🟨",
        "level": "Beginner → Advanced",
        "description": "Learn JavaScript for interactive websites and modern web applications.",
        "chapters": [
            "Introduction to JavaScript",
            "JavaScript Syntax",
            "Variables",
            "let const and var",
            "Data Types",
            "Operators",
            "Conditions",
            "Loops",
            "Functions",
            "Arrow Functions",
            "Arrays",
            "Array Methods",
            "Objects",
            "Object Methods",
            "Strings",
            "DOM Introduction",
            "Selecting Elements",
            "Changing HTML",
            "Changing CSS",
            "Events",
            "Forms",
            "Validation",
            "Local Storage",
            "JSON",
            "Fetch API",
            "Async and Await",
            "Error Handling",
            "JavaScript Modules",
            "Web APIs",
            "JavaScript Mini Project"
        ]
    },

    "SQL": {
        "icon": "🗄️",
        "level": "Beginner → Advanced",
        "description": "Learn databases and SQL from basic queries to practical data management.",
        "chapters": [
            "What is a Database?",
            "DBMS and RDBMS",
            "Tables",
            "Rows and Columns",
            "Primary Keys",
            "Foreign Keys",
            "SQL Introduction",
            "CREATE DATABASE",
            "CREATE TABLE",
            "INSERT",
            "SELECT",
            "WHERE",
            "ORDER BY",
            "LIMIT",
            "UPDATE",
            "DELETE",
            "AND OR NOT",
            "LIKE",
            "IN",
            "BETWEEN",
            "Aggregate Functions",
            "GROUP BY",
            "HAVING",
            "JOINS",
            "INNER JOIN",
            "LEFT JOIN",
            "RIGHT JOIN",
            "Subqueries",
            "Constraints",
            "Indexes",
            "Normalization",
            "SQL Security",
            "Database Project"
        ]
    },

    "Data Structures": {
        "icon": "🌳",
        "level": "Intermediate → Advanced",
        "description": "Understand how data is organized and efficiently processed by programs.",
        "chapters": [
            "Introduction to Data Structures",
            "Time Complexity",
            "Space Complexity",
            "Arrays",
            "Strings",
            "Linked Lists",
            "Singly Linked List",
            "Doubly Linked List",
            "Circular Linked List",
            "Stacks",
            "Queues",
            "Circular Queue",
            "Priority Queue",
            "Hash Tables",
            "Trees",
            "Binary Trees",
            "Binary Search Trees",
            "Heaps",
            "Graphs",
            "Graph Representation",
            "BFS",
            "DFS",
            "Searching",
            "Linear Search",
            "Binary Search",
            "Sorting",
            "Bubble Sort",
            "Selection Sort",
            "Insertion Sort",
            "Merge Sort",
            "Quick Sort",
            "Data Structures Final Challenge"
        ]
    },

    "Git and GitHub": {
        "icon": "🐙",
        "level": "Beginner → Intermediate",
        "description": "Learn version control and professional software collaboration.",
        "chapters": [
            "What is Git?",
            "What is GitHub?",
            "Git vs GitHub",
            "Installing Git",
            "Git Configuration",
            "Repositories",
            "git init",
            "git status",
            "git add",
            "git commit",
            "git log",
            "git diff",
            "Branches",
            "Merging",
            "Merge Conflicts",
            "Remote Repositories",
            "git push",
            "git pull",
            "git clone",
            "GitHub Projects",
            "README Files",
            "Issues",
            "Pull Requests",
            "Open Source Basics",
            "GitHub Portfolio Project"
        ]
    },

    "Computer Networks": {
        "icon": "🌐",
        "level": "Beginner → Advanced",
        "description": "Understand how computers communicate across networks and the internet.",
        "chapters": [
            "What is a Network?",
            "Types of Networks",
            "LAN",
            "MAN",
            "WAN",
            "Network Topologies",
            "Network Devices",
            "Hub",
            "Switch",
            "Router",
            "Modem",
            "IP Address",
            "IPv4",
            "IPv6",
            "MAC Address",
            "DNS",
            "DHCP",
            "HTTP",
            "HTTPS",
            "TCP",
            "UDP",
            "Ports",
            "OSI Model",
            "TCP IP Model",
            "Firewalls",
            "WiFi",
            "Ethernet",
            "Network Troubleshooting",
            "Network Security Basics",
            "Networking Final Challenge"
        ]
    },

    "Cybersecurity Fundamentals": {
        "icon": "🛡️",
        "level": "Beginner → Intermediate",
        "description": "Learn the foundations of cybersecurity, threats, protection and safe computing.",
        "chapters": [
            "What is Cybersecurity?",
            "CIA Triad",
            "Threats and Vulnerabilities",
            "Risk",
            "Authentication",
            "Authorization",
            "Passwords",
            "Multi Factor Authentication",
            "Social Engineering",
            "Phishing",
            "Malware",
            "Viruses",
            "Worms",
            "Trojans",
            "Ransomware",
            "Spyware",
            "Password Attacks",
            "Brute Force Concepts",
            "Encryption",
            "Hashing",
            "Digital Signatures",
            "Public Key Cryptography",
            "Network Security",
            "Firewalls",
            "Secure Browsing",
            "Web Security Basics",
            "SQL Injection Concepts",
            "XSS Concepts",
            "Security Awareness",
            "Incident Response Basics",
            "Cybersecurity Ethics",
            "Cybersecurity Final Challenge"
        ]
    }
}


# =========================================================
# LESSON CONTENT ENGINE
# =========================================================

def create_lesson(chapter, course_name):

    lower = chapter.lower()

    special = {

        "What is a Computer?": {
            "explanation": (
                "A computer is an electronic device that accepts data "
                "as input, processes that data according to instructions, "
                "stores information when needed, and produces useful output. "
                "Computers are used for communication, education, business, "
                "entertainment, scientific work and many other activities. "
                "Even a smartphone is essentially a specialized computer."
            ),
            "example": (
                'number1 = 10\n'
                'number2 = 20\n'
                'result = number1 + number2\n'
                'print(result)'
            ),
            "tip": "Remember the basic cycle: Input → Processing → Output → Storage.",
            "mistake": "Do not think that a computer only means a desktop PC. Phones, tablets and many embedded devices are computers too.",
            "question": "Which component mainly processes instructions?",
            "options": ["Keyboard", "CPU", "Monitor", "Mouse"],
            "answer": 1
        },

        "What is Programming?": {
            "explanation": (
                "Programming is the process of creating instructions that "
                "a computer can follow to perform a task. A programmer first "
                "understands a problem, designs a solution, writes code, "
                "tests it and fixes mistakes. Programming is mainly about "
                "logical problem solving."
            ),
            "example": (
                'name = "Joe"\n'
                'print("Hello", name)'
            ),
            "tip": "Good programming starts with understanding the problem before writing code.",
            "mistake": "Do not memorize code without understanding what each instruction does.",
            "question": "What is programming mainly used for?",
            "options": [
                "Writing instructions for computers",
                "Cleaning a keyboard",
                "Changing a monitor",
                "Connecting a printer"
            ],
            "answer": 0
        },

        "Algorithms": {
            "explanation": (
                "An algorithm is a clear, ordered set of steps used to solve "
                "a problem or complete a task. Algorithms are important because "
                "they allow us to plan a solution before converting it into "
                "programming code."
            ),
            "example": (
                'a = 10\n'
                'b = 20\n'
                'if a > b:\n'
                '    print(a)\n'
                'else:\n'
                '    print(b)'
            ),
            "tip": "Algorithm = step-by-step method for solving a problem.",
            "mistake": "An algorithm is not a programming language. It is a method for solving a problem.",
            "question": "What does an algorithm provide?",
            "options": [
                "A step-by-step solution",
                "A computer monitor",
                "An internet connection",
                "A hardware cable"
            ],
            "answer": 0
        },

        "Variables": {
            "explanation": (
                "A variable is a named location used by a program to store "
                "a value. The value can represent information such as a name, "
                "age, mark or calculation result."
            ),
            "example": (
                'age = 18\n'
                'print(age)'
            ),
            "tip": "Think of a variable as a labelled box containing a value.",
            "mistake": "The variable name and the value stored inside it are not the same thing.",
            "question": "What is a variable mainly used for?",
            "options": [
                "Storing data",
                "Displaying a monitor",
                "Connecting Wi-Fi",
                "Printing paper"
            ],
            "answer": 0
        },

        "Introduction to C": {
            "explanation": (
                "C is a general-purpose programming language created by "
                "Dennis Ritchie at Bell Labs. It became extremely important "
                "for system programming and influenced many later languages."
            ),
            "example": (
                '#include <stdio.h>\n\n'
                'int main() {\n'
                '    printf("Hello World");\n'
                '    return 0;\n'
                '}'
            ),
            "tip": "Most basic C programs begin execution from main().",
            "mistake": "Remember that C is case-sensitive. main and Main are different names.",
            "question": "Who developed the C programming language?",
            "options": [
                "James Gosling",
                "Dennis Ritchie",
                "Guido van Rossum",
                "Bjarne Stroustrup"
            ],
            "answer": 1
        },

        "Introduction to Python": {
            "explanation": (
                "Python is a high-level, general-purpose programming language "
                "designed with an emphasis on readability. It is used in web "
                "development, automation, data analysis, artificial intelligence "
                "and many other areas."
            ),
            "example": (
                'name = "Joe"\n'
                'print(name)'
            ),
            "tip": "Python focuses on readable code and uses indentation to organize blocks.",
            "mistake": "Do not ignore indentation in Python.",
            "question": "Which language is known for readable and beginner-friendly syntax?",
            "options": [
                "Machine Code",
                "Python",
                "Assembly",
                "Binary"
            ],
            "answer": 1
        },

        "Introduction to C++": {
            "explanation": (
                "C++ is a general-purpose programming language developed by "
                "Bjarne Stroustrup. It builds upon many concepts from C and "
                "adds classes, objects, inheritance and polymorphism."
            ),
            "example": (
                '#include <iostream>\n'
                'using namespace std;\n\n'
                'int main() {\n'
                '    cout << "Hello";\n'
                '    return 0;\n'
                '}'
            ),
            "tip": "C++ supports both procedural and object-oriented programming.",
            "mistake": "C++ is not simply C with a different name.",
            "question": "Which language is C++ closely related to?",
            "options": ["C", "HTML", "SQL", "CSS"],
            "answer": 0
        },

        "What is OOP?": {
            "explanation": (
                "Object-oriented programming, commonly called OOP, is a way "
                "of designing software around objects that contain data and "
                "behaviour. Important OOP concepts include encapsulation, "
                "inheritance, polymorphism and abstraction."
            ),
            "example": (
                'class Student:\n'
                '    def __init__(self, name):\n'
                '        self.name = name\n\n'
                'student = Student("Joe")\n'
                'print(student.name)'
            ),
            "tip": "OOP helps organize large programs into reusable components.",
            "mistake": "An object is an instance of a class; the two terms are related but not identical.",
            "question": "What does OOP stand for?",
            "options": [
                "Object Oriented Programming",
                "Operating Output Program",
                "Open Online Programming",
                "Object Output Process"
            ],
            "answer": 0
        },

        "What is HTML?": {
            "explanation": (
                "HTML stands for HyperText Markup Language. It is used to "
                "define the structure and meaning of content on a web page."
            ),
            "example": (
                '<h1>Welcome to CodeQuest</h1>\n'
                '<p>Learn programming step by step.</p>'
            ),
            "tip": "HTML describes structure; CSS handles presentation; JavaScript handles behaviour.",
            "mistake": "HTML is a markup language, not a general-purpose programming language.",
            "question": "What does HTML mainly define?",
            "options": [
                "Web page structure",
                "Database passwords",
                "CPU instructions",
                "Network cables"
            ],
            "answer": 0
        },

        "What is CSS?": {
            "explanation": (
                "CSS stands for Cascading Style Sheets. It controls how HTML "
                "content looks on a web page. CSS controls colors, fonts, "
                "spacing, borders, layouts, animations and responsive designs."
            ),
            "example": (
                'h1 {\n'
                '    font-size: 40px;\n'
                '}'
            ),
            "tip": "HTML builds the structure; CSS makes that structure look good.",
            "mistake": "CSS changes presentation. It does not replace HTML structure.",
            "question": "What is CSS mainly used for?",
            "options": [
                "Styling web pages",
                "Creating CPU hardware",
                "Managing databases",
                "Sending emails"
            ],
            "answer": 0
        },

        "What is Cybersecurity?": {
            "explanation": (
                "Cybersecurity is the practice of protecting computers, networks, "
                "applications, systems and information from unauthorized access, "
                "damage, disruption or misuse."
            ),
            "example": (
                'password = "StrongPassword123!"\n'
                'print("Use multi-factor authentication")'
            ),
            "tip": "Security is a process, not a single application or tool.",
            "mistake": "Never assume that antivirus software alone can protect an entire system.",
            "question": "What is a major goal of cybersecurity?",
            "options": [
                "Protecting systems and information",
                "Making computers heavier",
                "Increasing screen brightness",
                "Replacing keyboards"
            ],
            "answer": 0
        },

        "What is a Database?": {
            "explanation": (
                "A database is an organized collection of information that can "
                "be stored, searched, updated and managed efficiently."
            ),
            "example": (
                'CREATE TABLE Students (\n'
                '    id INT,\n'
                '    name VARCHAR(50)\n'
                ');'
            ),
            "tip": "Database = organized information that software can manage.",
            "mistake": "A database is more than just a plain text file.",
            "question": "What is a database?",
            "options": [
                "An organized collection of information",
                "A computer monitor",
                "A programming keyboard",
                "A network cable"
            ],
            "answer": 0
        }
    }

    if chapter in special:

        data = special[chapter].copy()

    else:

        topic = chapter

        if "Loop" in chapter:

            concept = (
                f"{topic} is related to repetition in programming. "
                "Loops allow a program to execute a block of instructions "
                "multiple times instead of writing the same instructions repeatedly."
            )

            example = (
                'for i in range(1, 6):\n'
                '    print(i)'
            )

        elif "Function" in chapter or "Method" in chapter:

            concept = (
                f"{topic} helps organize reusable behaviour in a program. "
                "Developers can separate related operations into reusable units."
            )

            example = (
                'def calculate_total(a, b):\n'
                '    return a + b\n\n'
                'print(calculate_total(10, 20))'
            )

        elif "Array" in chapter or "List" in chapter:

            concept = (
                f"{topic} deals with storing multiple related values. "
                "Collections are useful when a program needs to work with "
                "many values."
            )

            example = (
                'marks = [80, 75, 90]\n'
                'print(marks[0])'
            )

        elif "Class" in chapter or "Object" in chapter:

            concept = (
                f"{topic} is an important object-oriented programming concept. "
                "OOP allows software to represent data and behaviour in organized units."
            )

            example = (
                'class Student:\n'
                '    pass\n\n'
                'student = Student()'
            )

        elif (
            "Security" in lower
            or "Cyber" in lower
            or "Phishing" in lower
        ):

            concept = (
                f"{topic} is an important cybersecurity concept. "
                "Understanding this topic helps users and developers recognize "
                "risks and design safer systems."
            )

            example = (
                'message = "You won a prize! Click here!"\n'
                'print("Check the message before clicking")'
            )

        elif (
            "Network" in chapter
            or "Internet" in chapter
            or "HTTP" in chapter
        ):

            concept = (
                f"{topic} is part of computer networking. "
                "Networking concepts explain how devices communicate, "
                "how information travels and how services work together."
            )

            example = (
                'url = "https://example.com"\n'
                'print(url)'
            )

        elif (
            "Database" in chapter
            or "SQL" in chapter
            or "Table" in chapter
        ):

            concept = (
                f"{topic} is related to data management. "
                "Applications need organized data so information can be "
                "stored, searched, changed and protected efficiently."
            )

            example = (
                'SELECT name\n'
                'FROM Students;'
            )

        elif "Git" in chapter or "GitHub" in chapter:

            concept = (
                f"{topic} is part of version control and software collaboration. "
                "Developers use version-control tools to track changes and "
                "collaborate on projects."
            )

            example = (
                'git add .\n'
                'git commit -m "Initial commit"'
            )

        else:

            concept = (
                f"{topic} is an important part of {course_name}. "
                "Learning this topic gives you another building block for "
                "understanding how computers, software and technology work. "
                "The goal is not just to memorize the definition, but to "
                "understand what the concept does, why it is useful and "
                "where you may encounter it in real applications."
            )

            # Real executable-looking example instead of paragraph text.
            example = (
                'topic = "' + topic + '"\n'
                'print(topic)'
            )

        data = {
            "explanation": concept,
            "example": example,
            "tip": (
                f"Understand the purpose of {topic} "
                "before trying to memorize its definition."
            ),
            "mistake": (
                "Do not memorize the topic without understanding "
                "what problem it solves."
            ),
            "question": f"Which statement best describes {topic}?",
            "options": [
                f"It is an important concept related to {course_name}",
                "It is only a type of computer game",
                "It is a physical power cable",
                "It has no practical use"
            ],
            "answer": 0
        }

    return {
        "title": chapter,
        "course": course_name,
        "chapter": chapter,
        "explanation": data["explanation"],
        "example": data["example"],
        "tip": data["tip"],
        "mistake": data.get(
            "mistake",
            "Read the concept carefully and try it yourself."
        ),
        "question": data["question"],
        "options": data["options"],
        "answer": data["answer"]
    }


# =========================================================
# QUIZ DATABASE
# =========================================================

quiz_questions = [

    {
        "id": "q001",
        "question": "Which component processes instructions in a computer?",
        "options": ["Keyboard", "CPU", "Monitor", "Mouse"],
        "answer": 1,
        "explanation": "The CPU executes instructions and performs processing."
    },

    {
        "id": "q002",
        "question": "Which language is known for readable syntax?",
        "options": ["Python", "Machine Code", "Binary", "Assembly"],
        "answer": 0,
        "explanation": "Python is designed with relatively simple and readable syntax."
    },

    {
        "id": "q003",
        "question": "What does HTML mainly define?",
        "options": [
            "Web page structure",
            "Database encryption",
            "CPU instructions",
            "Wi-Fi signals"
        ],
        "answer": 0,
        "explanation": "HTML describes the structure and meaning of web page content."
    },

    {
        "id": "q004",
        "question": "Which symbol normally ends a C statement?",
        "options": [".", ",", ";", ":"],
        "answer": 2,
        "explanation": "Most C statements end with a semicolon."
    },

    {
        "id": "q005",
        "question": "Which Excel function calculates a total?",
        "options": [
            "TOTAL()",
            "SUM()",
            "ADD()",
            "PLUS()"
        ],
        "answer": 1,
        "explanation": "SUM() is used to add values in Excel."
    },

    {
        "id": "q006",
        "question": "Which OOP concept allows a class to acquire features from another class?",
        "options": [
            "Encapsulation",
            "Inheritance",
            "Compilation",
            "Formatting"
        ],
        "answer": 1,
        "explanation": "Inheritance allows one class to derive from another."
    },

    {
        "id": "q007",
        "question": "What is an algorithm?",
        "options": [
            "A step-by-step method for solving a problem",
            "A monitor",
            "A programming keyboard",
            "A network cable"
        ],
        "answer": 0,
        "explanation": "An algorithm describes ordered steps for solving a problem."
    },

    {
        "id": "q008",
        "question": "What is a variable used for?",
        "options": [
            "Storing data",
            "Displaying a monitor",
            "Connecting Wi-Fi",
            "Printing paper"
        ],
        "answer": 0,
        "explanation": "Variables provide named storage for values used by programs."
    },

    {
        "id": "q009",
        "question": "What is CSS mainly used for?",
        "options": [
            "Styling web pages",
            "Creating CPUs",
            "Managing electricity",
            "Replacing databases"
        ],
        "answer": 0,
        "explanation": "CSS controls the presentation and appearance of web content."
    },

    {
        "id": "q010",
        "question": "What is cybersecurity mainly concerned with?",
        "options": [
            "Protecting systems and information",
            "Increasing monitor size",
            "Changing keyboard keys",
            "Printing documents"
        ],
        "answer": 0,
        "explanation": "Cybersecurity protects systems, networks, applications and information."
    },

    {
        "id": "q011",
        "question": "Which SQL command retrieves data?",
        "options": [
            "SELECT",
            "REMOVE",
            "DISPLAY",
            "FETCHDATAONLY"
        ],
        "answer": 0,
        "explanation": "SELECT is used to retrieve data from database tables."
    },

    {
        "id": "q012",
        "question": "Which Git command records changes in the local repository?",
        "options": [
            "git commit",
            "git screen",
            "git savepage",
            "git record"
        ],
        "answer": 0,
        "explanation": "git commit creates a recorded snapshot of staged changes."
    },

    {
        "id": "q013",
        "question": "Which network device normally connects different networks?",
        "options": [
            "Router",
            "Keyboard",
            "Monitor",
            "Printer"
        ],
        "answer": 0,
        "explanation": "Routers forward traffic between networks."
    },

    {
        "id": "q014",
        "question": "What does OOP stand for?",
        "options": [
            "Object Oriented Programming",
            "Open Online Process",
            "Operating Object Program",
            "Output Oriented Protocol"
        ],
        "answer": 0,
        "explanation": "OOP means Object-Oriented Programming."
    },

    {
        "id": "q015",
        "question": "Which Python collection stores key-value pairs?",
        "options": [
            "Dictionary",
            "Tuple",
            "String",
            "Integer"
        ],
        "answer": 0,
        "explanation": "Python dictionaries store data using key-value pairs."
    }
]


# =========================================================
# CODE CHALLENGES
# =========================================================

code_challenges = [

    {
        "id": "c001",
        "language": "C",
        "question": "What will this program print?",
        "code": """#include <stdio.h>

int main() {
    int a = 5;
    int b = 3;

    printf("%d", a + b);

    return 0;
}""",
        "options": ["2", "8", "15", "53"],
        "answer": 1,
        "explanation": "5 + 3 = 8."
    },

    {
        "id": "c002",
        "language": "Python",
        "question": "What will this program print?",
        "code": """a = 10
b = 2

print(a * b)""",
        "options": ["12", "20", "102", "5"],
        "answer": 1,
        "explanation": "10 × 2 = 20."
    },

    {
        "id": "c003",
        "language": "C++",
        "question": "What will this program print?",
        "code": """#include <iostream>
using namespace std;

int main() {
    cout << 10 - 4;
    return 0;
}""",
        "options": ["6", "14", "104", "Error"],
        "answer": 0,
        "explanation": "10 - 4 = 6."
    },

    {
        "id": "c004",
        "language": "Python",
        "question": "What will this program print?",
        "code": """x = 5

if x > 3:
    print("Yes")
else:
    print("No")""",
        "options": ["Yes", "No", "5", "Error"],
        "answer": 0,
        "explanation": "5 is greater than 3, so the if block executes."
    }
]


# =========================================================
# ERROR FINDER
# =========================================================

error_challenges = [

    {
        "id": "e001",
        "language": "C",
        "question": "Find the error:",
        "code": """#include <stdio.h>

int main() {
    int age = 18
    printf("%d", age);
    return 0;
}""",
        "options": [
            "Missing semicolon after 18",
            "printf is wrong",
            "main cannot return 0",
            "No error"
        ],
        "answer": 0,
        "explanation": "The declaration int age = 18 needs a semicolon."
    },

    {
        "id": "e002",
        "language": "Python",
        "question": "Find the error:",
        "code": """age = 20

if age >= 18
    print("Adult")""",
        "options": [
            "Missing colon after the condition",
            "age cannot be 20",
            "print is invalid",
            "No error"
        ],
        "answer": 0,
        "explanation": "Python requires a colon after the if condition."
    },

    {
        "id": "e003",
        "language": "C++",
        "question": "Find the error:",
        "code": """#include <iostream>

int main() {
    std::cout << "Hello"
    return 0;
}""",
        "options": [
            "Missing semicolon",
            "cout cannot print text",
            "main cannot return",
            "No error"
        ],
        "answer": 0,
        "explanation": "The cout statement requires a semicolon."
    }
]


# =========================================================
# SECURITY HEADERS
# =========================================================

@app.after_request
def add_security_headers(response):

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["X-Frame-Options"] = "DENY"

    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )

    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' "
        "https://www.gstatic.com "
        "https://apis.google.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self' "
        "https://*.googleapis.com "
        "https://*.firebaseio.com "
        "https://*.firebaseapp.com "
        "https://identitytoolkit.googleapis.com "
        "https://securetoken.googleapis.com; "
        "frame-src "
        "https://*.firebaseapp.com "
        "https://accounts.google.com; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none';"
    )

    return response


# =========================================================
# BASIC ROUTES
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        courses=courses
    )


@app.route("/api/status")
def status():

    return jsonify({
        "app": "CodeQuest AI",
        "version": "0.5",
        "status": "online",
        "architecture": "Smart Learning Engine",
        "features": [
            "Expanded Learning Paths",
            "Beginner Friendly Lessons",
            "Chapter Quick Checks",
            "Quiz Arena",
            "Code Challenges",
            "Error Finder",
            "Career Guide",
            "Protected Test Engine",
            "Server Side Test Validation",
            "Progress Tracking",
            "Google Authentication Ready",
            "Firestore Progress Ready",
            "Security Headers"
        ]
    })


# =========================================================
# COURSE API
# =========================================================

@app.route("/api/courses")
def get_courses():

    return jsonify(courses)


@app.route("/api/course/<path:course_name>")
def get_course(course_name):

    if course_name not in courses:

        return jsonify({
            "error": "Course not found"
        }), 404

    return jsonify(courses[course_name])


# =========================================================
# LESSON API
# =========================================================

@app.route("/api/lesson/<path:chapter>")
def get_lesson(chapter):

    course_name = request.args.get(
        "course",
        "Programming Fundamentals"
    )

    lesson = create_lesson(
        chapter,
        course_name
    )

    return jsonify(lesson)


# =========================================================
# COURSE LESSON LIST
# =========================================================

@app.route("/api/course/<path:course_name>/lessons")
def get_course_lessons(course_name):

    if course_name not in courses:

        return jsonify({
            "error": "Course not found"
        }), 404

    result = []

    for index, chapter in enumerate(
        courses[course_name]["chapters"],
        start=1
    ):

        result.append({
            "number": index,
            "title": chapter,
            "course": course_name
        })

    return jsonify({
        "course": course_name,
        "total": len(result),
        "lessons": result
    })


# =========================================================
# NORMAL PRACTICE QUIZ
# =========================================================

@app.route("/api/quiz")
def get_quiz():

    amount = request.args.get(
        "amount",
        default=10,
        type=int
    )

    amount = max(
        1,
        min(amount, len(quiz_questions))
    )

    questions = random.sample(
        quiz_questions,
        amount
    )

    return jsonify(questions)


# =========================================================
# CODE CHALLENGES
# =========================================================

@app.route("/api/code-challenges")
def get_code_challenges():

    return jsonify(code_challenges)


# =========================================================
# ERROR FINDER
# =========================================================

@app.route("/api/error-finder")
def get_error_challenges():

    return jsonify(error_challenges)


# =========================================================
# CAREER GUIDE
# =========================================================

@app.route("/api/career", methods=["POST"])
def career_guide():

    data = request.get_json(
        silent=True
    ) or {}

    question = str(
        data.get(
            "question",
            ""
        )
    ).strip()

    if not question:

        return jsonify({
            "answer": "Please ask me a career-related question."
        }), 400

    q = question.lower()

    if "internship" in q:

        answer = (
            "To prepare for internships, build strong programming basics, "
            "complete 2–3 practical projects, learn Git and GitHub, create "
            "a clean resume and practice coding questions. Start applying "
            "while you continue learning."
        )

    elif "placement" in q or "campus" in q:

        answer = (
            "For campus placements, focus on programming fundamentals, "
            "data structures, SQL, communication skills, aptitude and "
            "interview preparation. Keep your projects and GitHub profile ready."
        )

    elif "resume" in q or "cv" in q:

        answer = (
            "Keep your resume simple and preferably one page as a student. "
            "Include education, technical skills, projects, certifications "
            "and relevant achievements. For projects, explain what you built "
            "and what technologies you used."
        )

    elif (
        "hardware" in q
        or "laptop" in q
        or "computer" in q
    ):

        answer = (
            "For computer hardware and systems, learn CPU, RAM, storage, "
            "motherboard, operating systems, networking and basic troubleshooting. "
            "For software development, also learn a programming language and Git."
        )

    elif (
        "software" in q
        or "developer" in q
        or "coding" in q
        or "programming" in q
    ):

        answer = (
            "A software developer should build strong programming logic, "
            "learn data structures, databases, Git/GitHub, APIs and software "
            "development practices. Then choose a specialization such as "
            "web, mobile, backend, AI or cybersecurity."
        )

    elif (
        "project" in q
        or "portfolio" in q
    ):

        answer = (
            "Build projects that solve real problems instead of only making "
            "tutorial projects. Start with small applications and gradually "
            "add databases, authentication, APIs and deployment. Put your "
            "best projects on GitHub."
        )

    elif (
        "roadmap" in q
        or "job" in q
    ):

        answer = (
            "A simple IT roadmap is: Programming Fundamentals → C/Python → "
            "Data Structures → SQL → Git/GitHub → Web or another specialization "
            "→ Projects → Resume → Internship and Placement preparation."
        )

    else:

        answer = (
            "Start by strengthening programming fundamentals, problem solving, "
            "Git/GitHub and SQL. Then build practical projects and choose a "
            "specialization that interests you. Consistent practice is more "
            "useful than trying to learn everything at once."
        )

    return jsonify({
        "answer": answer
    })


# =========================================================
# PROTECTED TEST SYSTEM
# =========================================================

TEST_DURATION = 10 * 60

TEST_SIZE = 10


def test_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        test = session.get(
            "secure_test"
        )

        if not test:

            return jsonify({
                "error": "No active test session."
            }), 403

        if time.time() > test["expires_at"]:

            session.pop(
                "secure_test",
                None
            )

            return jsonify({
                "error": "Test time has expired."
            }), 403

        return function(
            *args,
            **kwargs
        )

    return wrapper


# =========================================================
# START SECURE TEST
# =========================================================

@app.route(
    "/api/test/start",
    methods=["POST"]
)
def start_secure_test():

    if session.get("secure_test"):

        existing = session["secure_test"]

        if time.time() < existing["expires_at"]:

            return jsonify({
                "error": "A test is already active."
            }), 409

    questions = random.sample(
        quiz_questions,
        min(
            TEST_SIZE,
            len(quiz_questions)
        )
    )

    public_questions = []

    for question in questions:

        public_questions.append({
            "id": question["id"],
            "question": question["question"],
            "options": question["options"]
        })

    now = time.time()

    test_id = secrets.token_urlsafe(24)

    session["secure_test"] = {
        "id": test_id,
        "started_at": now,
        "expires_at": now + TEST_DURATION,
        "questions": [
            question["id"]
            for question in questions
        ],
        "answers": {},
        "violations": 0
    }

    session.modified = True

    return jsonify({
        "success": True,
        "test_id": test_id,
        "duration_seconds": TEST_DURATION,
        "question_count": len(public_questions),
        "questions": public_questions
    })


# =========================================================
# SUBMIT SECURE TEST ANSWER
# =========================================================

@app.route(
    "/api/test/answer",
    methods=["POST"]
)
@test_required
def submit_test_answer():

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "error": "Invalid request."
        }), 400

    question_id = data.get(
        "question_id"
    )

    selected = data.get(
        "selected"
    )

    if not isinstance(
        question_id,
        str
    ):

        return jsonify({
            "error": "Invalid question ID."
        }), 400

    if not isinstance(
        selected,
        int
    ):

        return jsonify({
            "error": "Invalid answer."
        }), 400

    test = session["secure_test"]

    if question_id not in test["questions"]:

        return jsonify({
            "error": "Question does not belong to this test."
        }), 400

    # Prevent invalid option indexes.
    question = next(
        (
            q for q in quiz_questions
            if q["id"] == question_id
        ),
        None
    )

    if question is None:

        return jsonify({
            "error": "Question not found."
        }), 400

    if selected < 0 or selected >= len(
        question["options"]
    ):

        return jsonify({
            "error": "Invalid option."
        }), 400

    test["answers"][question_id] = selected

    session.modified = True

    return jsonify({
        "success": True,
        "saved": True
    })


# =========================================================
# SECURITY VIOLATION REPORT
# =========================================================

@app.route(
    "/api/test/violation",
    methods=["POST"]
)
@test_required
def test_violation():

    data = request.get_json(
        silent=True
    ) or {}

    reason = str(
        data.get(
            "reason",
            "unknown"
        )
    )[:100]

    test = session["secure_test"]

    test["violations"] += 1

    session.modified = True

    violations = test["violations"]

    if violations >= 3:

        session.pop(
            "secure_test",
            None
        )

        return jsonify({
            "success": True,
            "terminated": True,
            "reason": reason,
            "message": (
                "Test terminated because "
                "the security violation limit was reached."
            )
        })

    return jsonify({
        "success": True,
        "terminated": False,
        "violations": violations,
        "remaining_warnings": 3 - violations,
        "reason": reason
    })


# =========================================================
# FINISH SECURE TEST
# =========================================================

@app.route(
    "/api/test/finish",
    methods=["POST"]
)
@test_required
def finish_secure_test():

    test = session["secure_test"]

    score = 0

    total = len(
        test["questions"]
    )

    submitted_answers = test[
        "answers"
    ]

    question_lookup = {
        question["id"]: question
        for question in quiz_questions
    }

    for question_id in test["questions"]:

        question = question_lookup.get(
            question_id
        )

        if not question:
            continue

        selected = submitted_answers.get(
            question_id
        )

        if selected == question["answer"]:

            score += 1

    percentage = (
        (score / total) * 100
        if total
        else 0
    )

    violations = test[
        "violations"
    ]

    result = {
        "test_id": test["id"],
        "score": score,
        "total": total,
        "percentage": round(
            percentage,
            2
        ),
        "violations": violations,
        "completed_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    session.pop(
        "secure_test",
        None
    )

    return jsonify(result)


# =========================================================
# TEST STATUS
# =========================================================

@app.route("/api/test/status")
def test_status():

    test = session.get(
        "secure_test"
    )

    if not test:

        return jsonify({
            "active": False
        })

    remaining = max(
        0,
        int(
            test["expires_at"]
            - time.time()
        )
    )

    if remaining <= 0:

        session.pop(
            "secure_test",
            None
        )

        return jsonify({
            "active": False,
            "expired": True
        })

    return jsonify({
        "active": True,
        "test_id": test["id"],
        "remaining_seconds": remaining,
        "violations": test["violations"],
        "answered": len(
            test["answers"]
        ),
        "total": len(
            test["questions"]
        )
    })


# =========================================================
# PROGRESS
# =========================================================

@app.route("/api/progress")
def progress():

    return jsonify({
        "server_tracking": False,
        "storage": "Firebase Firestore",
        "message": (
            "Account progress is designed to be stored "
            "in the user's Google account through Firebase."
        )
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "service": "CodeQuest AI",
        "version": "0.5"
    })


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Resource not found"
    }), 404


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "error": "Internal server error"
    }), 500


# =========================================================
# LOCAL DEVELOPMENT / RENDER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=False
    )
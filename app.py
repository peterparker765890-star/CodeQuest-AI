from flask import Flask, render_template, jsonify

app = Flask(__name__)

# =========================================================
# CODEQUEST AI V0.3
# Learn • Practice • Play • Build
# =========================================================

courses = {
    "Computer Basics": {
        "icon": "💻",
        "level": "Beginner",
        "description": "Start from zero and understand computers.",
        "chapters": [
            "What is a Computer?",
            "Hardware and Software",
            "Input and Output Devices",
            "Operating Systems",
            "Files and Folders",
            "Internet Basics",
            "Computer Safety",
            "Practical Computer Skills"
        ]
    },

    "MS Word": {
        "icon": "📝",
        "level": "Beginner",
        "description": "Create professional documents from scratch.",
        "chapters": [
            "Introduction to MS Word",
            "Creating and Saving Documents",
            "Text Formatting",
            "Paragraph Formatting",
            "Tables",
            "Images and Shapes",
            "Headers and Footers",
            "Page Layout",
            "References",
            "Mail Merge",
            "Practical Document Project"
        ]
    },

    "MS Excel": {
        "icon": "📊",
        "level": "Beginner → Advanced",
        "description": "Learn spreadsheets, formulas, data and charts.",
        "chapters": [
            "Introduction to Excel",
            "Cells, Rows and Columns",
            "Data Entry",
            "Basic Formulas",
            "Functions",
            "IF and Logical Functions",
            "Sorting and Filtering",
            "Charts",
            "Conditional Formatting",
            "Data Analysis",
            "Practical Excel Project"
        ]
    },

    "MS Office": {
        "icon": "📑",
        "level": "Beginner → Advanced",
        "description": "Master essential Microsoft Office skills.",
        "chapters": [
            "Introduction to MS Office",
            "Word Basics",
            "Excel Basics",
            "PowerPoint Basics",
            "Creating Presentations",
            "Office Productivity",
            "File Management",
            "Professional Office Skills",
            "Mini Office Project"
        ]
    },

    "Programming Fundamentals": {
        "icon": "🧠",
        "level": "Beginner",
        "description": "Build programming logic before learning languages.",
        "chapters": [
            "What is Programming?",
            "Algorithms",
            "Flowcharts",
            "Variables",
            "Data Types",
            "Operators",
            "Conditions",
            "Loops",
            "Functions",
            "Problem Solving",
            "Introduction to Debugging"
        ]
    },

    "C Language": {
        "icon": "🔵",
        "level": "Beginner → Master",
        "description": "Learn C from your first program to advanced concepts.",
        "chapters": [
            "Introduction to C",
            "Structure of a C Program",
            "Variables and Data Types",
            "Input and Output",
            "Operators",
            "if and else",
            "switch",
            "for Loop",
            "while Loop",
            "do while Loop",
            "Arrays",
            "Strings",
            "Functions",
            "Recursion",
            "Pointers",
            "Structures",
            "Unions",
            "File Handling",
            "Dynamic Memory",
            "Advanced C",
            "C Mini Projects",
            "Final C Challenge"
        ]
    },

    "C++": {
        "icon": "🟣",
        "level": "Beginner → Master",
        "description": "Learn C++ and object-oriented programming.",
        "chapters": [
            "Introduction to C++",
            "Basic Syntax",
            "Variables and Data Types",
            "Input and Output",
            "Operators",
            "Conditions",
            "Loops",
            "Arrays and Strings",
            "Functions",
            "Classes and Objects",
            "Constructors",
            "Inheritance",
            "Polymorphism",
            "Encapsulation",
            "Abstraction",
            "Templates",
            "STL Basics",
            "File Handling",
            "C++ Projects",
            "Final C++ Challenge"
        ]
    },

    "OOP Concepts": {
        "icon": "🧩",
        "level": "Intermediate",
        "description": "Understand the core ideas behind object-oriented programming.",
        "chapters": [
            "What is OOP?",
            "Classes",
            "Objects",
            "Constructors",
            "Encapsulation",
            "Inheritance",
            "Polymorphism",
            "Abstraction",
            "Method Overloading",
            "Method Overriding",
            "Real World OOP",
            "OOP Mini Project"
        ]
    },

    "Python": {
        "icon": "🐍",
        "level": "Beginner → Master",
        "description": "Learn Python from your first program to real projects.",
        "chapters": [
            "Introduction to Python",
            "Python Syntax",
            "Variables",
            "Data Types",
            "Input and Output",
            "Operators",
            "if and else",
            "Loops",
            "Lists",
            "Tuples",
            "Sets",
            "Dictionaries",
            "Functions",
            "Lambda Functions",
            "Modules",
            "File Handling",
            "Exception Handling",
            "Object-Oriented Python",
            "Libraries",
            "Python Projects",
            "Final Python Challenge"
        ]
    },

    "Java": {
        "icon": "☕",
        "level": "Beginner → Master",
        "description": "Learn Java and object-oriented programming.",
        "chapters": [
            "Introduction to Java",
            "Java Syntax",
            "Variables and Data Types",
            "Input and Output",
            "Operators",
            "Conditions",
            "Loops",
            "Arrays",
            "Strings",
            "Methods",
            "Classes and Objects",
            "Constructors",
            "Inheritance",
            "Polymorphism",
            "Interfaces",
            "Exception Handling",
            "Collections",
            "File Handling",
            "Java Projects",
            "Final Java Challenge"
        ]
    }
}


# =========================================================
# LESSON DATABASE
# =========================================================

lessons = {

    "What is a Computer?": {
        "title": "What is a Computer?",
        "explanation": "A computer is an electronic device that accepts data, processes it, stores it and produces useful information.",
        "example": "Example: When you type 10 + 20 into a calculator, the computer processes the values and produces 30.",
        "tip": "Remember: Input → Processing → Output → Storage",
        "question": "Which part of a computer processes instructions?",
        "options": ["Keyboard", "CPU", "Monitor", "Mouse"],
        "answer": 1
    },

    "Hardware and Software": {
        "title": "Hardware and Software",
        "explanation": "Hardware refers to the physical parts of a computer. Software refers to the programs and instructions that run on the computer.",
        "example": "Hardware: keyboard, monitor, CPU. Software: Windows, Chrome, Python.",
        "tip": "Hardware can be touched. Software cannot be physically touched.",
        "question": "Which of these is software?",
        "options": ["Keyboard", "RAM", "Windows", "Monitor"],
        "answer": 2
    },

    "What is Programming?": {
        "title": "What is Programming?",
        "explanation": "Programming is the process of writing instructions that tell a computer how to perform a task.",
        "example": "Python, C, C++ and Java are programming languages used to create programs.",
        "tip": "Think of a program as instructions given to a computer.",
        "question": "What is programming?",
        "options": [
            "Repairing a monitor",
            "Writing instructions for a computer",
            "Typing documents",
            "Browsing websites"
        ],
        "answer": 1
    },

    "Algorithms": {
        "title": "Algorithms",
        "explanation": "An algorithm is a step-by-step procedure used to solve a problem or complete a task.",
        "example": "To make tea: boil water → add tea → add milk → add sugar → serve.",
        "tip": "Algorithm = Step-by-step solution.",
        "question": "What does an algorithm provide?",
        "options": [
            "A step-by-step solution",
            "Computer hardware",
            "Internet connection",
            "A programming language"
        ],
        "answer": 0
    },

    "Variables": {
        "title": "Variables",
        "explanation": "A variable is a named storage location used by a program to store a value.",
        "example": "In Python: age = 18. Here, age is a variable containing 18.",
        "tip": "Variable = name + stored value.",
        "question": "What is a variable used for?",
        "options": [
            "Storing data",
            "Displaying a monitor",
            "Connecting Wi-Fi",
            "Printing paper"
        ],
        "answer": 0
    },

    "Introduction to C": {
        "title": "Introduction to C",
        "explanation": "C is a general-purpose programming language developed by Dennis Ritchie. It is widely used for system programming and learning programming fundamentals.",
        "example": """#include <stdio.h>

int main() {
    printf("Hello World");
    return 0;
}""",
        "tip": "C programs commonly use main() as the starting point.",
        "question": "Who developed the C programming language?",
        "options": [
            "James Gosling",
            "Dennis Ritchie",
            "Guido van Rossum",
            "Bjarne Stroustrup"
        ],
        "answer": 1
    },

    "Structure of a C Program": {
        "title": "Structure of a C Program",
        "explanation": "A basic C program normally contains header files, the main() function, statements and a return statement.",
        "example": """#include <stdio.h>

int main() {
    printf("Hello");
    return 0;
}""",
        "tip": "Execution normally begins from main().",
        "question": "Where does execution normally begin in a C program?",
        "options": ["printf()", "main()", "include()", "return()"],
        "answer": 1
    },

    "Variables and Data Types": {
        "title": "Variables and Data Types",
        "explanation": "C provides different data types such as int, float, char and double to store different kinds of values.",
        "example": """int age = 18;
float mark = 85.5;
char grade = 'A';""",
        "tip": "Choose a data type according to the kind of value you want to store.",
        "question": "Which data type stores an integer in C?",
        "options": ["float", "char", "int", "string"],
        "answer": 2
    },

    "Introduction to Python": {
        "title": "Introduction to Python",
        "explanation": "Python is a high-level programming language known for its readable syntax and wide range of applications.",
        "example": """name = "Joe"
print(name)""",
        "tip": "Python programs can often be written with fewer lines of code.",
        "question": "Which language is known for readable and simple syntax?",
        "options": ["Machine Code", "Python", "Assembly", "Binary"],
        "answer": 1
    },

    "Python Syntax": {
        "title": "Python Syntax",
        "explanation": "Python syntax defines how Python code must be written. Indentation is important because it defines blocks of code.",
        "example": """age = 18

if age >= 18:
    print("Adult")""",
        "tip": "Python uses indentation to organize blocks of code.",
        "question": "What is especially important for Python code blocks?",
        "options": ["Indentation", "Semicolon", "Brackets only", "Colon only"],
        "answer": 0
    },

    "Introduction to C++": {
        "title": "Introduction to C++",
        "explanation": "C++ is a general-purpose programming language that supports procedural and object-oriented programming.",
        "example": """#include <iostream>
using namespace std;

int main() {
    cout << "Hello";
    return 0;
}""",
        "tip": "C++ extends many concepts of the C language.",
        "question": "Which language is C++ closely related to?",
        "options": ["C", "HTML", "SQL", "CSS"],
        "answer": 0
    }
}


# =========================================================
# QUIZ
# =========================================================

quiz_questions = [

    {
        "question": "Which language is known for its simplicity and readability?",
        "options": ["C", "Python", "Assembly", "Machine Code"],
        "answer": 1,
        "explanation": "Python is designed with simple and readable syntax."
    },

    {
        "question": "Which symbol is commonly used to end a statement in C?",
        "options": [".", ",", ";", ":"],
        "answer": 2,
        "explanation": "C statements normally end with a semicolon (;)."
    },

    {
        "question": "Which component is known as the brain of a computer?",
        "options": ["RAM", "CPU", "Keyboard", "Monitor"],
        "answer": 1,
        "explanation": "The CPU processes instructions and performs calculations."
    },

    {
        "question": "Which Excel function is commonly used to calculate a total?",
        "options": ["TOTAL()", "SUM()", "ADD()", "PLUS()"],
        "answer": 1,
        "explanation": "SUM() adds numbers together in Excel."
    },

    {
        "question": "Which OOP concept allows one class to acquire properties of another?",
        "options": [
            "Encapsulation",
            "Inheritance",
            "Abstraction",
            "Compilation"
        ],
        "answer": 1,
        "explanation": "Inheritance allows a class to derive properties and behaviour from another class."
    },

    {
        "question": "What does HTML mainly describe?",
        "options": [
            "Database queries",
            "Web page structure",
            "Computer hardware",
            "Operating systems"
        ],
        "answer": 1,
        "explanation": "HTML defines the structure of web pages."
    }
]


# =========================================================
# CODE CHALLENGES
# =========================================================

code_challenges = [

    {
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
    }
]


# =========================================================
# ERROR FINDER
# =========================================================

error_challenges = [

    {
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
        "explanation": "The statement int age = 18 needs a semicolon."
    },

    {
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
        "explanation": "Python requires a colon (:) after an if condition."
    }
]


# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def home():
    return render_template("index.html", courses=courses)


@app.route("/api/courses")
def get_courses():
    return jsonify(courses)


@app.route("/api/course/<course_name>")
def get_course(course_name):

    if course_name not in courses:
        return jsonify({"error": "Course not found"}), 404

    return jsonify(courses[course_name])


@app.route("/api/lesson/<chapter>")
def get_lesson(chapter):

    lesson = lessons.get(chapter)

    if lesson:
        return jsonify(lesson)

    # Generic lesson for chapters that don't yet have
    # specialized content.
    return jsonify({
        "title": chapter,
        "explanation": f"This lesson introduces the important concepts of {chapter}. Study the topic carefully and practice the examples.",
        "example": "Practice this concept by writing a small program or creating your own example.",
        "tip": "Take notes, practice the example and test yourself before moving to the next chapter.",
        "question": f"Which statement best describes {chapter}?",
        "options": [
            "It is an important programming/computer concept",
            "It is only a computer game",
            "It is a type of hardware cable",
            "None of these"
        ],
        "answer": 0
    })


@app.route("/api/quiz")
def get_quiz():
    return jsonify(quiz_questions)


@app.route("/api/code-challenges")
def get_code_challenges():
    return jsonify(code_challenges)


@app.route("/api/error-finder")
def get_error_challenges():
    return jsonify(error_challenges)


@app.route("/api/status")
def status():
    return jsonify({
        "app": "CodeQuest AI",
        "version": "0.3",
        "status": "online",
        "features": [
            "Learning",
            "Interactive Lessons",
            "Quiz Arena",
            "Code Challenges",
            "Error Finder",
            "AI Career Assistant",
            "Progress Tracking"
        ]
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
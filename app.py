from flask import Flask, jsonify, render_template
import os
import random

app = Flask(__name__)

# =========================================================
# CODEQUEST AI
# Learn • Practice • Play • Build
# =========================================================

courses = [

    # =====================================================
    # 1. COMPUTER BASICS
    # =====================================================
    {
        "id": "computer-basics",
        "title": "Computer Basics",
        "icon": "💻",
        "level": "Beginner",
        "description": "Build your foundation from zero.",
        "chapters": [
            {
                "title": "What is a Computer?",
                "lesson": """
A computer is an electronic device that accepts data as input,
processes it according to instructions, stores information and
produces useful output.

A computer works mainly through four basic operations:
Input → Processing → Storage → Output.

For example, when you type your name using a keyboard, the keyboard
provides input. The processor handles the data, memory temporarily
stores it, and the monitor displays the result.

Modern computers are used in almost every field including education,
banking, healthcare, engineering, business, communication,
entertainment, artificial intelligence and cybersecurity.

Understanding these fundamentals is important because almost every
advanced computer science topic is built on these concepts.
                """,
                "key_points": [
                    "Input gives data to the computer.",
                    "CPU processes instructions.",
                    "Memory and storage keep information.",
                    "Output presents the result."
                ]
            },
            {
                "title": "Hardware and Software",
                "lesson": """
Computer hardware means the physical parts of a computer that we can
touch. Examples include the CPU, RAM, keyboard, mouse, monitor,
motherboard and storage devices.

Software is a collection of programs and instructions that tells
hardware what to do.

Operating systems such as Windows, Linux and Android are system
software. Applications such as Microsoft Word, Excel, browsers and
media players are application software.

Hardware without software cannot perform useful tasks, while software
needs hardware to execute its instructions.

Learning the difference between hardware and software is one of the
most important foundations for beginners.
                """,
                "key_points": [
                    "Hardware is physical.",
                    "Software is a collection of instructions.",
                    "Operating systems manage computer resources.",
                    "Applications help users perform tasks."
                ]
            },
            {
                "title": "CPU, RAM and Storage",
                "lesson": """
The CPU, or Central Processing Unit, is responsible for executing
instructions and performing calculations. It is often called the
brain of the computer.

RAM, or Random Access Memory, is temporary working memory. Programs
currently being used are loaded into RAM so the CPU can access them
quickly.

Storage devices such as SSDs and HDDs keep data even after the
computer is switched off.

A simple way to remember them is:

CPU = Processing
RAM = Temporary working space
SSD/HDD = Long-term storage

Understanding these components helps you later understand operating
systems, programming, performance and computer architecture.
                """,
                "key_points": [
                    "CPU executes instructions.",
                    "RAM is temporary memory.",
                    "SSD/HDD provide permanent storage.",
                    "More RAM can help with multitasking."
                ]
            }
        ]
    },

    # =====================================================
    # 2. MS OFFICE
    # =====================================================
    {
        "id": "ms-office",
        "title": "MS Office",
        "icon": "📊",
        "level": "Beginner",
        "description": "Learn Word, Excel and PowerPoint for college and jobs.",
        "chapters": [
            {
                "title": "Microsoft Word",
                "lesson": """
Microsoft Word is a word-processing application used to create,
edit, format and print documents.

Students commonly use Word for assignments, lab records, reports,
resumes, project documentation and applications.

Important skills include text formatting, headings, page layout,
tables, images, headers and footers, page numbers and document
sharing.

For career preparation, learn professional document formatting,
resume creation and report writing rather than only basic typing.
                """,
                "key_points": [
                    "Used for documents and reports.",
                    "Learn professional formatting.",
                    "Tables and page layout are important.",
                    "Useful for resumes and project reports."
                ]
            },
            {
                "title": "Microsoft Excel",
                "lesson": """
Microsoft Excel is a spreadsheet application used to store,
organize, calculate and analyse data.

An Excel worksheet contains rows and columns. Their intersection is
called a cell.

Important beginner functions include SUM, AVERAGE, COUNT, MAX and
MIN.

As you improve, learn IF, VLOOKUP/XLOOKUP, conditional formatting,
charts, sorting, filtering and PivotTables.

Excel is useful not only for office work but also for data analysis,
finance, business and many internship roles.
                """,
                "key_points": [
                    "Excel organizes data in spreadsheets.",
                    "Functions automate calculations.",
                    "Charts help visualize information.",
                    "PivotTables help analyse large datasets."
                ]
            },
            {
                "title": "Microsoft PowerPoint",
                "lesson": """
PowerPoint is used to create presentations.

A good presentation should communicate an idea clearly rather than
fill every slide with text.

Learn slide layouts, themes, images, diagrams, charts, animations
and presenter tools.

For college students, presentation skills are useful during seminars,
project reviews, hackathons and placement interviews.
                """,
                "key_points": [
                    "Used for presentations.",
                    "Keep slides clear and readable.",
                    "Use diagrams and visuals when useful.",
                    "Presentation skill helps in interviews."
                ]
            }
        ]
    },

    # =====================================================
    # 3. C PROGRAMMING
    # =====================================================
    {
        "id": "c-programming",
        "title": "C Programming",
        "icon": "🔵",
        "level": "Beginner",
        "description": "Learn programming fundamentals using C.",
        "chapters": [
            {
                "title": "What is C Language?",
                "lesson": """
C is a general-purpose programming language developed by Dennis
Ritchie at Bell Labs.

C is one of the most important languages for understanding programming
because it teaches variables, data types, operators, conditions,
loops, functions, arrays, pointers and memory concepts.

C is widely associated with system programming, embedded systems,
operating systems and performance-oriented software.

For a beginner, the main goal is not simply memorising syntax.
You should learn how a program thinks: input → processing → output.

Once you understand these fundamentals, learning languages such as
C++, Java and Python becomes easier.
                """,
                "key_points": [
                    "C is a general-purpose programming language.",
                    "It teaches strong programming fundamentals.",
                    "C is important for understanding memory and systems.",
                    "Programming logic is more important than memorising syntax."
                ],
                "program": """#include <stdio.h>

int main() {
    printf("Hello, World!");
    return 0;
}"""
            },
            {
                "title": "Variables and Data Types",
                "lesson": """
A variable is a named memory location used to store a value.

C provides several basic data types. int is commonly used for whole
numbers, float for decimal values, char for a character and double
for higher-precision decimal values.

Choosing an appropriate data type is important because computers
store different kinds of information differently.

For example, if you want to store a student's age, int is suitable.
If you want to store a percentage such as 87.5, float can be used.

Variables make programs dynamic because their values can change while
the program is running.
                """,
                "key_points": [
                    "Variables store values.",
                    "int stores integers.",
                    "float stores decimal values.",
                    "char stores a character."
                ],
                "program": """#include <stdio.h>

int main() {
    int age = 18;
    float mark = 87.5;

    printf("Age = %d\\n", age);
    printf("Mark = %.2f", mark);

    return 0;
}"""
            },
            {
                "title": "Input and Output",
                "lesson": """
Input allows a program to receive information from the user.

In C, printf() is commonly used for output while scanf() is commonly
used for input.

For example, a calculator program can ask the user for two numbers,
receive them using scanf(), perform a calculation and display the
result using printf().

Understanding input and output is essential because most practical
programs interact with data in some way.
                """,
                "key_points": [
                    "printf() displays output.",
                    "scanf() receives input.",
                    "Format specifiers describe data types.",
                    "Input allows interactive programs."
                ],
                "program": """#include <stdio.h>

int main() {
    int a, b;

    printf("Enter two numbers: ");
    scanf("%d %d", &a, &b);

    printf("Sum = %d", a + b);

    return 0;
}"""
            },
            {
                "title": "Conditional Statements",
                "lesson": """
Conditional statements allow a program to make decisions.

The if statement executes code when a condition is true.
The else statement provides an alternative when the condition is
false.

Multiple conditions can be handled using else-if.

Decision making is used everywhere in programming. Login systems,
grading systems, shopping discounts and game logic all use conditions.

Learning conditions properly is an important step toward solving
real programming problems.
                """,
                "key_points": [
                    "if checks a condition.",
                    "else handles the alternative.",
                    "else-if handles multiple conditions.",
                    "Conditions are used in real applications."
                ],
                "program": """#include <stdio.h>

int main() {
    int mark;

    printf("Enter mark: ");
    scanf("%d", &mark);

    if(mark >= 50)
        printf("Pass");
    else
        printf("Fail");

    return 0;
}"""
            },
            {
                "title": "Loops",
                "lesson": """
Loops repeat a block of code.

The three commonly studied loops in C are for, while and do-while.

A for loop is useful when the number of repetitions is known.
A while loop is useful when repetition depends on a condition.
A do-while loop executes its body at least once.

Loops are extremely important because they allow programmers to
process many values without writing the same code repeatedly.

They are heavily used with arrays, searching, sorting and data
processing.
                """,
                "key_points": [
                    "Loops reduce repeated code.",
                    "for is useful for counted repetition.",
                    "while is condition-based.",
                    "do-while executes at least once."
                ],
                "program": """#include <stdio.h>

int main() {
    int i;

    for(i = 1; i <= 5; i++) {
        printf("%d\\n", i);
    }

    return 0;
}"""
            }
        ]
    },

    # =====================================================
    # 4. C++
    # =====================================================
    {
        "id": "cpp",
        "title": "C++ Programming",
        "icon": "⚙️",
        "level": "Intermediate",
        "description": "Learn object-oriented programming with C++.",
        "chapters": [
            {
                "title": "Introduction to C++",
                "lesson": """
C++ is a general-purpose programming language developed by Bjarne
Stroustrup.

It extends many ideas from C and adds powerful features such as
classes, objects, inheritance, polymorphism and templates.

C++ is commonly used for competitive programming, game development,
high-performance applications and systems software.

Learning C++ after C helps you understand object-oriented programming
and larger software structures.
                """,
                "key_points": [
                    "C++ supports procedural and object-oriented programming.",
                    "Classes and objects are important concepts.",
                    "C++ is widely used in performance-oriented software."
                ],
                "program": """#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!";
    return 0;
}"""
            },
            {
                "title": "Classes and Objects",
                "lesson": """
A class is a blueprint that defines data and functions.

An object is an instance of a class.

For example, a Student class can contain a student's name, roll
number and functions such as displayDetails().

Classes help programmers organise related data and behaviour together.

This concept is one of the foundations of object-oriented programming.
                """,
                "key_points": [
                    "Class = blueprint.",
                    "Object = instance of a class.",
                    "Classes combine data and functions."
                ],
                "program": """#include <iostream>
using namespace std;

class Student {
public:
    string name;

    void display() {
        cout << "Student: " << name;
    }
};

int main() {
    Student s;
    s.name = "Joe";
    s.display();

    return 0;
}"""
            }
        ]
    },

    # =====================================================
    # 5. PYTHON
    # =====================================================
    {
        "id": "python",
        "title": "Python Programming",
        "icon": "🐍",
        "level": "Beginner",
        "description": "Learn Python for automation, data and AI.",
        "chapters": [
            {
                "title": "What is Python?",
                "lesson": """
Python is a high-level, general-purpose programming language known
for its readable syntax.

Python is widely used in automation, web development, data analysis,
machine learning, artificial intelligence, scripting and education.

One reason beginners like Python is that programs can often be written
with less syntax compared with lower-level languages.

However, becoming good at Python requires understanding programming
logic, data structures, functions, modules, errors and real projects.
                """,
                "key_points": [
                    "Python has readable syntax.",
                    "It is widely used in AI and data science.",
                    "Python is useful for automation and web development."
                ],
                "program": """print("Hello, World!")"""
            },
            {
                "title": "Variables and Data Types",
                "lesson": """
Python variables are names that refer to values.

Common data types include int, float, str, bool, list, tuple, set
and dictionary.

Python automatically determines the type of many variables when
values are assigned.

Understanding data types is important because different operations
work with different kinds of data.
                """,
                "key_points": [
                    "Variables store references to values.",
                    "Python supports many built-in data types.",
                    "Strings represent text.",
                    "Lists store collections of values."
                ],
                "program": """name = "Joe"
age = 18
mark = 87.5

print(name)
print(age)
print(mark)"""
            }
        ]
    },

    # =====================================================
    # 6. DATA STRUCTURES
    # =====================================================
    {
        "id": "dsa",
        "title": "Data Structures & Algorithms",
        "icon": "🧩",
        "level": "Intermediate",
        "description": "Learn how programmers solve problems efficiently.",
        "chapters": [
            {
                "title": "Introduction to Data Structures",
                "lesson": """
A data structure is a way of organising and storing data so that it
can be accessed and modified efficiently.

Common data structures include arrays, linked lists, stacks, queues,
trees, graphs, hash tables and heaps.

Choosing the correct data structure can significantly affect the
performance of a program.

For example, a queue is useful when data should be processed in
first-in-first-out order.

Data structures are extremely important for coding interviews,
competitive programming and software development.
                """,
                "key_points": [
                    "Data structures organise information.",
                    "Different structures suit different problems.",
                    "DSA is important for technical interviews."
                ]
            },
            {
                "title": "Algorithms",
                "lesson": """
An algorithm is a step-by-step procedure used to solve a problem.

A good algorithm should be clear, correct and efficient.

Examples include searching algorithms, sorting algorithms and graph
algorithms.

Programmers often compare algorithms using time complexity and space
complexity.

Learning algorithms develops problem-solving ability, which is useful
far beyond one programming language.
                """,
                "key_points": [
                    "Algorithms solve problems step by step.",
                    "Efficiency matters.",
                    "Time and space complexity help measure efficiency."
                ]
            }
        ]
    },

    # =====================================================
    # 7. DBMS
    # =====================================================
    {
        "id": "dbms",
        "title": "DBMS & SQL",
        "icon": "🗄️",
        "level": "Intermediate",
        "description": "Learn databases and SQL.",
        "chapters": [
            {
                "title": "What is DBMS?",
                "lesson": """
A Database Management System is software used to create, store,
organise, retrieve and manage data.

Examples include MySQL, PostgreSQL, Oracle Database and Microsoft SQL
Server.

Instead of storing important application information randomly in
files, databases provide structured methods to manage large amounts
of data.

Databases are used in banking, e-commerce, education, healthcare,
social media and almost every modern application.
                """,
                "key_points": [
                    "DBMS manages data.",
                    "Databases support structured storage.",
                    "SQL is commonly used to communicate with relational databases."
                ],
                "program": """CREATE TABLE students (
    id INT,
    name VARCHAR(100),
    mark INT
);"""
            },
            {
                "title": "SQL Basics",
                "lesson": """
SQL stands for Structured Query Language.

SQL is used to create tables, insert data, update records, delete
records and retrieve information.

Important commands include SELECT, INSERT, UPDATE, DELETE and CREATE.

Learning SQL is highly useful for backend development, data analysis
and many software engineering roles.
                """,
                "key_points": [
                    "SELECT retrieves data.",
                    "INSERT adds records.",
                    "UPDATE changes records.",
                    "DELETE removes records."
                ],
                "program": """SELECT * FROM students;

SELECT name, mark
FROM students
WHERE mark >= 50;"""
            }
        ]
    },

    # =====================================================
    # 8. WEB DEVELOPMENT
    # =====================================================
    {
        "id": "web",
        "title": "Web Development",
        "icon": "🌐",
        "level": "Beginner",
        "description": "Build websites and web applications.",
        "chapters": [
            {
                "title": "HTML",
                "lesson": """
HTML stands for HyperText Markup Language.

HTML provides the structure of a web page.

Headings, paragraphs, links, images, forms, tables and buttons can
all be represented using HTML elements.

HTML is the starting point for frontend development. After learning
HTML, combine it with CSS for design and JavaScript for behaviour.
                """,
                "key_points": [
                    "HTML provides webpage structure.",
                    "HTML uses elements and tags.",
                    "HTML works together with CSS and JavaScript."
                ],
                "program": """<!DOCTYPE html>
<html>
<body>
    <h1>Hello CodeQuest!</h1>
    <p>My first webpage.</p>
</body>
</html>"""
            },
            {
                "title": "CSS",
                "lesson": """
CSS stands for Cascading Style Sheets.

CSS controls the appearance of websites including colours, spacing,
fonts, layouts, animations and responsive design.

Modern CSS skills include Flexbox, Grid, responsive design and
component-based styling.

Good CSS makes an application easier to use and more professional.
                """,
                "key_points": [
                    "CSS controls presentation.",
                    "Flexbox and Grid are important.",
                    "Responsive design supports different screen sizes."
                ]
            },
            {
                "title": "JavaScript",
                "lesson": """
JavaScript is a programming language commonly used to make websites
interactive.

It can respond to button clicks, validate forms, update page content,
communicate with APIs and create dynamic web applications.

JavaScript is also used outside the browser through environments such
as Node.js.

Learning JavaScript is valuable for modern frontend and full-stack
development.
                """,
                "key_points": [
                    "JavaScript adds behaviour.",
                    "It can interact with HTML and CSS.",
                    "JavaScript is widely used in web development."
                ],
                "program": """const button = document.querySelector("button");

button.addEventListener("click", function() {
    alert("Hello CodeQuest!");
});"""
            }
        ]
    },

    # =====================================================
    # 9. GIT & GITHUB
    # =====================================================
    {
        "id": "github",
        "title": "Git & GitHub",
        "icon": "🐙",
        "level": "Beginner",
        "description": "Learn version control and professional project workflow.",
        "chapters": [
            {
                "title": "What is Git?",
                "lesson": """
Git is a distributed version control system.

It records changes made to files so developers can track the history
of a project, restore earlier versions and work safely on different
features.

Important commands include git init, git add, git commit, git status,
git branch, git merge and git log.

Git is one of the most important tools for modern software developers.
                """,
                "key_points": [
                    "Git tracks changes.",
                    "Commits create project history.",
                    "Branches allow separate development."
                ],
                "program": """git init
git add .
git commit -m "Initial commit" """
            },
            {
                "title": "What is GitHub?",
                "lesson": """
GitHub is a platform for hosting Git repositories and collaborating
on software projects.

Developers use GitHub to showcase projects, collaborate with teams,
review code and contribute to open-source projects.

A strong GitHub profile can help students demonstrate practical work
during internship and job applications.

Learn to create clean repositories, useful README files and meaningful
commit history.
                """,
                "key_points": [
                    "GitHub hosts Git repositories.",
                    "Repositories can showcase projects.",
                    "README files explain projects.",
                    "GitHub can support a student's portfolio."
                ]
            }
        ]
    },

    # =====================================================
    # 10. OPERATING SYSTEM
    # =====================================================
    {
        "id": "os",
        "title": "Operating Systems",
        "icon": "🖥️",
        "level": "Intermediate",
        "description": "Understand how operating systems manage computers.",
        "chapters": [
            {
                "title": "Introduction to Operating Systems",
                "lesson": """
An operating system is system software that manages computer hardware
and provides services for application programs.

Examples include Windows, Linux, macOS, Android and iOS.

The operating system manages processes, memory, files, devices and
security.

Understanding operating systems is important for software development,
system administration, cloud computing and cybersecurity.
                """,
                "key_points": [
                    "OS manages hardware and software resources.",
                    "It manages processes and memory.",
                    "It provides an interface for users and applications."
                ]
            },
            {
                "title": "Processes and Threads",
                "lesson": """
A process is a program in execution.

A thread is a smaller unit of execution within a process.

Modern applications often use multiple processes or threads to
perform tasks concurrently.

Understanding processes and threads helps explain multitasking,
performance and server applications.
                """,
                "key_points": [
                    "Process = program in execution.",
                    "Thread = execution unit within a process.",
                    "Concurrency can improve application responsiveness."
                ]
            }
        ]
    },

    # =====================================================
    # 11. COMPUTER NETWORKS
    # =====================================================
    {
        "id": "networks",
        "title": "Computer Networks",
        "icon": "📡",
        "level": "Intermediate",
        "description": "Understand how computers communicate.",
        "chapters": [
            {
                "title": "Introduction to Networks",
                "lesson": """
A computer network is a group of connected devices that communicate
and share resources.

Networks can be classified by size, such as LAN, MAN and WAN.

The Internet is a massive interconnected network.

Important concepts include IP addresses, routers, switches,
protocols, DNS, HTTP and HTTPS.

Networking knowledge is useful in software development, cloud
computing, system administration and cybersecurity.
                """,
                "key_points": [
                    "Networks allow devices to communicate.",
                    "IP addresses identify network interfaces.",
                    "Routers connect networks.",
                    "Protocols define communication rules."
                ]
            },
            {
                "title": "Internet and DNS",
                "lesson": """
When you type a website name into a browser, the Domain Name System
helps translate the human-readable domain name into an IP address.

This allows the browser to locate the correct server.

Understanding DNS, HTTP, HTTPS and IP addresses helps beginners
understand what actually happens when a website loads.
                """,
                "key_points": [
                    "DNS translates domain names to IP addresses.",
                    "HTTP/HTTPS are web communication protocols.",
                    "Browsers communicate with servers."
                ]
            }
        ]
    },

    # =====================================================
    # 12. CYBERSECURITY
    # =====================================================
    {
        "id": "cybersecurity",
        "title": "Cybersecurity",
        "icon": "🛡️",
        "level": "Intermediate",
        "description": "Learn the foundations of digital security.",
        "chapters": [
            {
                "title": "What is Cybersecurity?",
                "lesson": """
Cybersecurity is the practice of protecting computers, networks,
applications and data from unauthorised access, misuse, damage or
disruption.

Important areas include network security, application security,
identity management, cryptography, security monitoring and incident
response.

Students should first learn networking, operating systems and basic
programming before moving deeply into cybersecurity.

Cybersecurity is a continuously changing field because new threats
and technologies appear regularly.
                """,
                "key_points": [
                    "Cybersecurity protects digital systems.",
                    "Security includes people, processes and technology.",
                    "Networking and OS knowledge are important foundations."
                ]
            },
            {
                "title": "Passwords and Authentication",
                "lesson": """
Authentication is the process of verifying who a user is.

Strong authentication reduces the chance of unauthorised access.

Good security practices include using unique passwords, password
managers where appropriate and multi-factor authentication.

Students should also understand phishing because attackers often
target people rather than technical systems directly.
                """,
                "key_points": [
                    "Authentication verifies identity.",
                    "Use unique strong passwords.",
                    "Multi-factor authentication adds protection.",
                    "Phishing attempts to trick users."
                ]
            }
        ]
    },

    # =====================================================
    # 13. CLOUD COMPUTING
    # =====================================================
    {
        "id": "cloud",
        "title": "Cloud Computing",
        "icon": "☁️",
        "level": "Intermediate",
        "description": "Understand modern cloud services and deployment.",
        "chapters": [
            {
                "title": "What is Cloud Computing?",
                "lesson": """
Cloud computing provides computing resources such as servers,
storage, databases and software through the Internet.

Instead of maintaining every physical server yourself, cloud
providers can provide infrastructure on demand.

Important cloud concepts include virtual machines, containers,
storage, databases, serverless computing and scalability.

Cloud knowledge is increasingly useful for software development and
DevOps-related careers.
                """,
                "key_points": [
                    "Cloud provides computing resources through networks.",
                    "Cloud supports scalability.",
                    "Containers and serverless are modern concepts."
                ]
            }
        ]
    },

    # =====================================================
    # 14. AI & MACHINE LEARNING
    # =====================================================
    {
        "id": "ai",
        "title": "AI & Machine Learning",
        "icon": "🤖",
        "level": "Intermediate",
        "description": "Understand the fundamentals of AI and ML.",
        "chapters": [
            {
                "title": "Introduction to AI",
                "lesson": """
Artificial Intelligence is a field of computing focused on creating
systems that can perform tasks that normally require aspects of human
intelligence.

Modern AI includes machine learning, computer vision, natural
language processing, recommendation systems and generative AI.

Students should understand that AI is not simply about using a
chatbot. Building AI systems requires programming, mathematics,
data and evaluation.

Python is widely used for learning and building AI applications.
                """,
                "key_points": [
                    "AI is a broad field.",
                    "Machine learning is a major AI approach.",
                    "Data and algorithms are important.",
                    "Python is widely used in AI."
                ]
            },
            {
                "title": "Machine Learning Basics",
                "lesson": """
Machine learning allows computers to learn patterns from data rather
than relying entirely on manually written rules.

Common learning types include supervised learning, unsupervised
learning and reinforcement learning.

A basic ML workflow includes collecting data, preparing data,
training a model, evaluating it and improving the system.

Understanding the limitations of data and model predictions is just
as important as understanding the algorithm.
                """,
                "key_points": [
                    "ML learns patterns from data.",
                    "Training and evaluation are important.",
                    "Data quality strongly affects results."
                ]
            }
        ]
    }
]


# =========================================================
# CAREER GUIDE
# =========================================================

career_guide = {

    "intro": """
Computer Science careers are built through a combination of
fundamentals, practical skills, projects, communication and
professional experience.

Do not try to learn every technology at once. Build a strong
foundation first and then specialise.

Your CodeQuest journey can be viewed as:

Learn → Practice → Build → Publish → Apply → Interview → Grow
""",

    "internships": {
        "title": "🎓 Internships",
        "content": """
Internships give students practical exposure to real development
work.

For beginners, the important goal is not simply getting a certificate.
Try to find opportunities where you can actually build, test,
document or maintain something.

Useful preparation:

• Learn one programming language properly.
• Build 2–4 practical projects.
• Maintain a clean GitHub profile.
• Create a simple one-page resume.
• Learn basic Git and GitHub.
• Practise communication.
• Apply regularly instead of waiting for one perfect opportunity.

Possible internship areas include:

• Web Development
• Python Development
• Software Development
• Data Analytics
• Testing
• Cybersecurity
• Cloud/DevOps
• AI/ML
• Technical Support

Eligibility varies by company. Some internships accept beginners,
while others require specific skills, projects or academic criteria.
Always check the actual requirements of each opportunity.
"""
    },

    "placements": {
        "title": "🏫 Campus Placements",
        "content": """
Campus placements commonly evaluate several areas:

1. Aptitude
2. Logical reasoning
3. Programming
4. Data structures
5. Computer science fundamentals
6. Communication
7. Technical interviews
8. HR or behavioural discussions

Start preparation early.

A useful progression is:

First year:
Programming + GitHub + communication + small projects

Second year:
DSA + DBMS + OS + Networks + web development

Third year:
Advanced DSA + projects + internships + resume

Final year:
Placement-specific preparation + mock interviews +
company-specific practice

The exact recruitment process differs between companies, so learn
the common fundamentals while checking each company's current process.
"""
    },

    "jobs": {
        "title": "💼 Jobs & Career Paths",
        "content": """
Computer Science can lead to many career paths.

Software Developer:
Builds and maintains applications.

Frontend Developer:
Creates the user interface of web applications.

Backend Developer:
Builds APIs, databases and server-side systems.

Full Stack Developer:
Works across frontend and backend.

Data Analyst:
Works with data to discover useful information.

Data Scientist:
Uses statistics, programming and machine learning to analyse data.

AI/ML Engineer:
Builds and integrates machine-learning or AI systems.

Cybersecurity Analyst:
Helps identify, investigate and reduce security risks.

Cloud/DevOps Engineer:
Works with deployment, infrastructure, automation and cloud systems.

QA/Test Engineer:
Tests software and helps improve product quality.

The best path depends on your interests, skills and the type of work
you want to perform.
"""
    },

    "smart": {
        "title": "🧠 Smart Ways to Become Job Ready",
        "content": """
Instead of collecting dozens of certificates, build evidence that
you can actually do the work.

SMART STRATEGY

1. Pick one main programming language.
2. Build projects instead of only watching tutorials.
3. Upload projects to GitHub.
4. Write useful README files.
5. Deploy suitable projects online.
6. Practise DSA regularly.
7. Learn SQL.
8. Understand OS and Networks.
9. Create a clean resume.
10. Practise explaining your own projects.
11. Participate in hackathons or coding events when possible.
12. Apply for internships early.
13. Build communication skills.
14. Follow current technologies without abandoning fundamentals.

A project becomes more valuable when you can explain:

• What problem does it solve?
• Why did you build it?
• What technologies did you use?
• How does it work?
• What difficulties did you face?
• How did you solve them?
• What would you improve next?
"""
    },

    "current_trends": {
        "title": "🔥 Current Technology Trends",
        "content": """
Technology changes quickly, so students should learn fundamentals
while keeping an eye on current industry directions.

Areas worth exploring include:

• Generative AI
• AI-assisted software development
• Cloud computing
• Cybersecurity
• Data engineering
• Full-stack development
• APIs and automation
• DevOps and CI/CD
• Containers
• Open-source development
• Mobile application development

Important:

Do not chase every trend.

A student who understands programming, databases, networking,
software development and problem solving can adapt to new tools much
more easily.

Use AI tools as learning and productivity assistants, but understand
the code you submit and build.
"""
    },

    "resume": {
        "title": "📄 Resume & GitHub",
        "content": """
Your resume should quickly communicate:

• Education
• Technical skills
• Projects
• Internship experience
• Achievements
• Relevant certifications

For a beginner, projects can be extremely useful.

Instead of writing:

'Made a website.'

Write what you actually built, the technology used and what the
application does.

Your GitHub profile should contain organised repositories, meaningful
README files and projects that you can explain confidently.

Avoid copying projects without understanding them.
"""
    },

    "interview": {
        "title": "🎯 Interview Preparation",
        "content": """
Technical interviews can test both knowledge and problem solving.

Prepare:

Programming:
Variables, conditions, loops, functions, arrays and strings.

DSA:
Searching, sorting, stacks, queues, linked lists, trees and basic
complexity.

DBMS:
SQL, keys, normalisation, joins and transactions.

OS:
Processes, threads, memory and file systems.

Networks:
IP, DNS, HTTP/HTTPS and basic networking.

Projects:
Be ready to explain every important part of your own project.

Communication:
Practise explaining technical ideas in simple language.
"""
    }
}


# =========================================================
# 700+ QUIZ ENGINE
# =========================================================

quiz_topics = [
    ("Computer Basics", [
        ("What does CPU stand for?", "Central Processing Unit"),
        ("What does RAM stand for?", "Random Access Memory"),
        ("Which device is used to display output?", "Monitor"),
        ("Which device is commonly used to enter text?", "Keyboard"),
        ("What is software?", "A collection of instructions/programs"),
        ("What is hardware?", "Physical computer components"),
        ("Which memory is temporary?", "RAM"),
        ("Which storage device commonly uses flash memory?", "SSD"),
        ("What does OS stand for?", "Operating System"),
        ("Which component executes instructions?", "CPU")
    ]),

    ("Programming", [
        ("Which symbol is commonly used to end a C statement?", ";"),
        ("Which function is used for output in C?", "printf()"),
        ("Which function is commonly used for input in C?", "scanf()"),
        ("Which language was created by Dennis Ritchie?", "C"),
        ("Which language is known for readable syntax and AI usage?", "Python"),
        ("What is a variable?", "A named storage/reference for a value"),
        ("What does a loop do?", "Repeats instructions"),
        ("What does an if statement provide?", "Decision making"),
        ("What is a function?", "A reusable block of code"),
        ("What is an algorithm?", "A step-by-step method for solving a problem")
    ]),

    ("C++", [
        ("Who developed C++?", "Bjarne Stroustrup"),
        ("What is a class?", "A blueprint for objects"),
        ("What is an object?", "An instance of a class"),
        ("What does OOP stand for?", "Object-Oriented Programming"),
        ("Which C++ feature supports inheritance?", "Classes"),
        ("Which stream is commonly used for output?", "cout"),
        ("Which stream is commonly used for input?", "cin"),
        ("What is a constructor?", "A special member function used during object creation"),
        ("What is inheritance?", "Deriving a class from another class"),
        ("What is polymorphism?", "Ability to use one interface in different forms")
    ]),

    ("Python", [
        ("Which language uses indentation as part of its syntax?", "Python"),
        ("Which keyword defines a function in Python?", "def"),
        ("Which symbol starts a Python comment?", "#"),
        ("Which type stores True or False?", "bool"),
        ("Which Python collection is ordered and mutable?", "list"),
        ("Which Python collection stores key-value pairs?", "dictionary"),
        ("What is a module?", "A reusable Python file/code unit"),
        ("Which function displays output?", "print()"),
        ("Which keyword is used to create a class?", "class"),
        ("Which language is widely used in machine learning?", "Python")
    ]),

    ("Web Development", [
        ("What does HTML stand for?", "HyperText Markup Language"),
        ("What does CSS stand for?", "Cascading Style Sheets"),
        ("What language adds interactivity to web pages?", "JavaScript"),
        ("Which HTML tag creates a heading?", "<h1>"),
        ("Which HTML tag creates a paragraph?", "<p>"),
        ("Which HTML tag creates a link?", "<a>"),
        ("What is CSS mainly used for?", "Styling web pages"),
        ("What is JavaScript mainly used for?", "Web interactivity and application logic"),
        ("What does API stand for?", "Application Programming Interface"),
        ("What protocol is commonly used for websites?", "HTTP/HTTPS")
    ]),

    ("DBMS", [
        ("What does DBMS stand for?", "Database Management System"),
        ("What does SQL stand for?", "Structured Query Language"),
        ("Which SQL command retrieves data?", "SELECT"),
        ("Which SQL command adds records?", "INSERT"),
        ("Which SQL command changes records?", "UPDATE"),
        ("Which SQL command removes records?", "DELETE"),
        ("What is a primary key?", "A field that uniquely identifies a record"),
        ("What is a database?", "An organised collection of data"),
        ("What is a table?", "A structured collection of rows and columns"),
        ("What does JOIN do?", "Combines related data from tables")
    ]),

    ("Git & GitHub", [
        ("What is Git?", "A version control system"),
        ("What is GitHub?", "A platform for hosting and collaborating on repositories"),
        ("Which command creates a Git repository?", "git init"),
        ("Which command stages files?", "git add"),
        ("Which command creates a commit?", "git commit"),
        ("Which command shows repository status?", "git status"),
        ("What is a repository?", "A project managed by version control"),
        ("What is a branch?", "A separate line of development"),
        ("What is a README?", "A document explaining a project"),
        ("What is version control?", "Tracking and managing changes to files")
    ]),

    ("Operating Systems", [
        ("What does OS stand for?", "Operating System"),
        ("Name one operating system.", "Windows"),
        ("What is a process?", "A program in execution"),
        ("What is a thread?", "A unit of execution within a process"),
        ("What does multitasking mean?", "Running/managing multiple tasks"),
        ("What does an OS manage?", "Hardware and software resources"),
        ("What is virtual memory?", "Memory management using disk as an extension of RAM"),
        ("What is a file system?", "A method of organising files and directories"),
        ("Name an open-source OS.", "Linux"),
        ("Which OS is widely used on Android phones?", "Android")
    ]),

    ("Networks", [
        ("What does IP stand for?", "Internet Protocol"),
        ("What does DNS stand for?", "Domain Name System"),
        ("What does LAN stand for?", "Local Area Network"),
        ("What does WAN stand for?", "Wide Area Network"),
        ("What device connects different networks?", "Router"),
        ("What does HTTP stand for?", "HyperText Transfer Protocol"),
        ("What does HTTPS add to HTTP?", "Encryption/security"),
        ("What does an IP address identify?", "A network interface/device address"),
        ("What is a protocol?", "A set of communication rules"),
        ("What does Wi-Fi provide?", "Wireless network connectivity")
    ]),

    ("Cybersecurity", [
        ("What is cybersecurity?", "Protection of digital systems and data"),
        ("What is authentication?", "Verifying identity"),
        ("What is authorisation?", "Determining permitted access"),
        ("What is phishing?", "A deceptive attempt to obtain information"),
        ("What is malware?", "Malicious software"),
        ("What does MFA stand for?", "Multi-Factor Authentication"),
        ("What is encryption?", "Converting data into protected form"),
        ("What is a firewall?", "A system that controls network traffic"),
        ("What is a vulnerability?", "A weakness that can be exploited"),
        ("Why are strong passwords important?", "To reduce unauthorised access")
    ]),

    ("Cloud", [
        ("What is cloud computing?", "Internet-based computing resources"),
        ("What does IaaS stand for?", "Infrastructure as a Service"),
        ("What does SaaS stand for?", "Software as a Service"),
        ("What does PaaS stand for?", "Platform as a Service"),
        ("What is scalability?", "Ability to handle changing workload"),
        ("What is a virtual machine?", "A software-based computer environment"),
        ("What is a container?", "An isolated application environment"),
        ("What is serverless computing?", "Running code without managing servers directly"),
        ("Why is cloud useful?", "Flexible and scalable computing resources"),
        ("Name a cloud provider.", "AWS")
    ]),

    ("AI & ML", [
        ("What does AI stand for?", "Artificial Intelligence"),
        ("What does ML stand for?", "Machine Learning"),
        ("What is machine learning?", "Learning patterns from data"),
        ("What is training data?", "Data used to train a model"),
        ("What is supervised learning?", "Learning using labelled examples"),
        ("What is unsupervised learning?", "Learning patterns without labelled outputs"),
        ("What is a model?", "A learned computational representation"),
        ("Which language is widely used in AI?", "Python"),
        ("What is generative AI?", "AI that generates new content"),
        ("Why is data important in ML?", "Models learn patterns from data")
    ])
]


def build_quiz_bank():
    """
    Creates 720+ questions from the core question pool.
    The base questions remain educational while variations
    provide a much larger practice bank.
    """
    bank = []

    question_id = 1

    for topic, questions in quiz_topics:
        for question, answer in questions:

            # Original question
            bank.append({
                "id": question_id,
                "topic": topic,
                "question": question,
                "answer": answer,
                "difficulty": "Beginner"
            })
            question_id += 1

            # Explanation-based variation
            bank.append({
                "id": question_id,
                "topic": topic,
                "question": "Which answer correctly describes: " + question,
                "answer": answer,
                "difficulty": "Beginner"
            })
            question_id += 1

            # Recall variation
            bank.append({
                "id": question_id,
                "topic": topic,
                "question": "Quick recall: " + question,
                "answer": answer,
                "difficulty": "Beginner"
            })
            question_id += 1

            # Concept variation
            bank.append({
                "id": question_id,
                "topic": topic,
                "question": "For a beginner studying " + topic +
                            ", what is the correct answer to: " + question,
                "answer": answer,
                "difficulty": "Intermediate"
            })
            question_id += 1

            # Challenge variation
            bank.append({
                "id": question_id,
                "topic": topic,
                "question": "Challenge: identify the correct concept for: "
                            + question,
                "answer": answer,
                "difficulty": "Advanced"
            })
            question_id += 1

            # Practical variation
            bank.append({
                "id": question_id,
                "topic": topic,
                "question": "Practical check: " + question,
                "answer": answer,
                "difficulty": "Intermediate"
            })
            question_id += 1

    # This gives 720 questions from 120 base questions.
    return bank


quiz_bank = build_quiz_bank()


# =========================================================
# API ROUTES
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/courses")
def get_courses():
    return jsonify(courses)


@app.route("/api/lesson/<course_id>/<int:index>")
def get_lesson(course_id, index):

    for course in courses:
        if course["id"] == course_id:

            if 0 <= index < len(course["chapters"]):
                return jsonify({
                    "course": course["title"],
                    "chapter": index + 1,
                    "total": len(course["chapters"]),
                    "lesson": course["chapters"][index]
                })

            return jsonify({
                "error": "Chapter not found"
            }), 404

    return jsonify({
        "error": "Course not found"
    }), 404


@app.route("/api/quizzes")
def get_quizzes():

    # Send the full 720+ question bank.
    return jsonify({
        "total": len(quiz_bank),
        "questions": quiz_bank
    })


@app.route("/api/quiz/<int:count>")
def get_random_quiz(count):

    count = max(1, min(count, len(quiz_bank)))

    questions = random.sample(quiz_bank, count)

    return jsonify({
        "total": len(quiz_bank),
        "questions": questions
    })


@app.route("/api/career")
def get_career():
    return jsonify(career_guide)


@app.route("/api/stats")
def get_stats():
    return jsonify({
        "courses": len(courses),
        "total_chapters": sum(
            len(course["chapters"]) for course in courses
        ),
        "quiz_questions": len(quiz_bank)
    })


@app.route("/api/test")
def test():
    return jsonify({
        "status": "CodeQuest AI is running",
        "courses": len(courses),
        "quiz_questions": len(quiz_bank)
    })


# =========================================================
# FIREBASE CONFIG
# =========================================================

@app.route("/api/firebase-config")
def firebase_config():

    config = {
        "apiKey": os.environ.get("FIREBASE_API_KEY", ""),
        "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN", ""),
        "projectId": os.environ.get("FIREBASE_PROJECT_ID", ""),
        "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.environ.get(
            "FIREBASE_MESSAGING_SENDER_ID", ""
        ),
        "appId": os.environ.get("FIREBASE_APP_ID", ""),
        "measurementId": os.environ.get(
            "FIREBASE_MEASUREMENT_ID", ""
        )
    }

    required = [
        "apiKey",
        "authDomain",
        "projectId",
        "storageBucket",
        "messagingSenderId",
        "appId"
    ]

    configured = all(config.get(key) for key in required)

    return jsonify({
        "configured": configured,
        "config": config if configured else {}
    })


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
<script>

/* =====================================================
   CODEQUEST AI - FIXED JAVASCRIPT
===================================================== */

let quizData = [];
let codeData = [];
let errorData = [];

let xp = Number(localStorage.getItem("codequest_xp") || 0);

let completedChapters = [];

try {
    completedChapters = JSON.parse(
        localStorage.getItem("codequest_chapters") || "[]"
    );
} catch (e) {
    completedChapters = [];
}

let solvedChallenges = Number(
    localStorage.getItem("codequest_challenges") || 0
);


/* =====================================================
   SAFE HTML
===================================================== */

function escapeHtml(text) {

    if (text === null || text === undefined) {
        return "";
    }

    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/* =====================================================
   XP
===================================================== */

function addXP(amount) {

    xp += Number(amount);

    localStorage.setItem(
        "codequest_xp",
        String(xp)
    );

    updateProgress();
}


function getLevelName(level) {

    const names = [
        "Code Explorer",
        "Bug Hunter",
        "Logic Builder",
        "Code Warrior",
        "Programmer",
        "Code Master",
        "Tech Creator"
    ];

    return names[
        Math.min(level - 1, names.length - 1)
    ];
}


function updateProgress() {

    const level =
        Math.floor(xp / 100) + 1;

    const currentXP =
        xp % 100;

    const xpText =
        document.getElementById("xpText");

    const levelText =
        document.getElementById("levelText");

    const progressText =
        document.getElementById("progressText");

    const progressBar =
        document.getElementById("progressBar");

    if (xpText) {
        xpText.textContent =
            `⭐ ${xp} XP`;
    }

    if (levelText) {
        levelText.textContent =
            `Level ${level} — ${getLevelName(level)} 🚀`;
    }

    if (progressText) {
        progressText.textContent =
            `${currentXP} / 100 XP`;
    }

    if (progressBar) {
        progressBar.style.width =
            `${currentXP}%`;
    }
}


/* =====================================================
   MODAL
===================================================== */

function showModal(content) {

    const modal =
        document.getElementById("modal");

    const modalContent =
        document.getElementById("modalContent");

    if (!modal || !modalContent) {
        alert("CodeQuest interface error.");
        return;
    }

    modalContent.innerHTML = content;

    modal.style.display = "block";
}


function closeModal() {

    const modal =
        document.getElementById("modal");

    if (modal) {
        modal.style.display = "none";
    }
}


/* =====================================================
   COURSE
===================================================== */

async function openCourse(name) {

    console.log("START COURSE:", name);

    showModal(`
        <h2>⏳ Loading Course...</h2>
        <p style="color:#aaa;margin-top:15px;">
            Loading ${escapeHtml(name)}...
        </p>
    `);

    try {

        const response = await fetch(
            "/api/course/" +
            encodeURIComponent(name),
            {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                }
            }
        );

        console.log(
            "Course response:",
            response.status
        );

        if (!response.ok) {
            throw new Error(
                "Course API returned " +
                response.status
            );
        }

        const course =
            await response.json();

        if (
            !course ||
            !Array.isArray(course.chapters)
        ) {
            throw new Error(
                "Invalid course data"
            );
        }

        let completedCount =
            course.chapters.filter(
                chapter =>
                    completedChapters.includes(
                        name + "::" + chapter
                    )
            ).length;

        let html = `

            <h2>
                ${escapeHtml(course.icon || "📚")}
                ${escapeHtml(name)}
            </h2>

            <p style="
                color:#aaa;
                margin-top:10px;
                line-height:1.6;
            ">
                ${escapeHtml(
                    course.description || ""
                )}
            </p>

            <div class="result">

                📚 Chapters:
                ${course.chapters.length}

                <br>

                ✅ Completed:
                ${completedCount}

            </div>

            <h3 style="margin-top:25px;">
                📖 Learning Path
            </h3>

        `;

        course.chapters.forEach(
            (chapter, index) => {

                const completed =
                    completedChapters.includes(
                        name + "::" + chapter
                    );

                html += `

                    <button
                        type="button"
                        class="chapter"
                        data-course="${escapeHtml(name)}"
                        data-chapter="${escapeHtml(chapter)}"
                        style="
                            width:100%;
                            text-align:left;
                            color:white;
                            font-family:inherit;
                            font-size:15px;
                        "
                    >

                        ${completed ? "✅" : `${index + 1}.`}

                        ${escapeHtml(chapter)}

                        <span style="
                            float:right;
                            color:#a855f7;
                        ">
                            →
                        </span>

                    </button>

                `;
            }
        );

        showModal(html);

        /*
         * Attach chapter clicks AFTER
         * the HTML has been inserted.
         */

        document
            .querySelectorAll(".chapter")
            .forEach(button => {

                button.addEventListener(
                    "click",
                    function () {

                        const courseName =
                            this.dataset.course;

                        const chapter =
                            this.dataset.chapter;

                        startChapter(
                            courseName,
                            chapter
                        );
                    }
                );
            });

    } catch (error) {

        console.error(
            "COURSE ERROR:",
            error
        );

        showModal(`

            <h2>
                ⚠️ Course Error
            </h2>

            <p style="
                color:#aaa;
                margin-top:15px;
                line-height:1.6;
            ">
                We couldn't load this course.
            </p>

            <div class="result">
                ${escapeHtml(error.message)}
            </div>

            <button
                type="button"
                class="primary"
                onclick="closeModal()"
            >
                CLOSE
            </button>

        `);
    }
}


/* =====================================================
   LESSON
===================================================== */

async function startChapter(
    courseName,
    chapter
) {

    console.log(
        "START CHAPTER:",
        courseName,
        chapter
    );

    showModal(`
        <h2>⏳ Loading Lesson...</h2>
        <p style="color:#aaa;margin-top:15px;">
            Loading ${escapeHtml(chapter)}...
        </p>
    `);

    try {

        const response = await fetch(
            "/api/lesson/" +
            encodeURIComponent(chapter),
            {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                }
            }
        );

        if (!response.ok) {
            throw new Error(
                "Lesson API returned " +
                response.status
            );
        }

        const lesson =
            await response.json();

        const key =
            courseName + "::" + chapter;

        const alreadyCompleted =
            completedChapters.includes(key);

        let html = `

            <h2>
                📖 ${escapeHtml(
                    lesson.title || chapter
                )}
            </h2>

            <div class="lesson-box">

                <h3>💡 Explanation</h3>

                <p>
                    ${escapeHtml(
                        lesson.explanation
                    )}
                </p>

                <h3 style="margin-top:20px;">
                    💻 Example
                </h3>

                <div class="example">
                    ${escapeHtml(
                        lesson.example
                    )}
                </div>

                <div class="tip">

                    💡 Tip:
                    ${escapeHtml(
                        lesson.tip
                    )}

                </div>

            </div>

            <div class="lesson-question">

                🧠 Quick Check

                <p style="
                    color:#aaa;
                    font-size:15px;
                    margin-top:10px;
                    font-weight:normal;
                ">
                    ${escapeHtml(
                        lesson.question
                    )}
                </p>

            </div>

            <div id="lessonOptions"></div>

            <div id="lessonResult"></div>

        `;

        showModal(html);

        const optionsBox =
            document.getElementById(
                "lessonOptions"
            );

        if (
            optionsBox &&
            Array.isArray(lesson.options)
        ) {

            lesson.options.forEach(
                (option, index) => {

                    const button =
                        document.createElement(
                            "button"
                        );

                    button.type = "button";

                    button.className =
                        "option";

                    button.textContent =
                        `${String.fromCharCode(
                            65 + index
                        )}. ${option}`;

                    button.addEventListener(
                        "click",
                        function () {

                            checkLesson(
                                index,
                                Number(
                                    lesson.answer
                                ),
                                key
                            );
                        }
                    );

                    optionsBox.appendChild(
                        button
                    );
                }
            );
        }

        if (alreadyCompleted) {

            const result =
                document.getElementById(
                    "lessonResult"
                );

            if (result) {

                result.innerHTML = `

                    <div
                        class="result"
                        style="color:#4ade80"
                    >

                        ✅ Chapter already completed.

                    </div>

                `;
            }
        }

    } catch (error) {

        console.error(
            "LESSON ERROR:",
            error
        );

        showModal(`

            <h2>
                ⚠️ Lesson Error
            </h2>

            <p style="
                color:#aaa;
                margin-top:15px;
            ">
                This lesson could not be loaded.
            </p>

            <div class="result">
                ${escapeHtml(error.message)}
            </div>

        `);
    }
}


/* =====================================================
   LESSON ANSWER
===================================================== */

function checkLesson(
    selected,
    correct,
    key
) {

    console.log(
        "LESSON ANSWER:",
        selected,
        correct
    );

    const result =
        document.getElementById(
            "lessonResult"
        );

    if (!result) {
        return;
    }

    if (Number(selected) === Number(correct)) {

        if (
            !completedChapters.includes(key)
        ) {

            completedChapters.push(key);

            localStorage.setItem(
                "codequest_chapters",
                JSON.stringify(
                    completedChapters
                )
            );

            addXP(25);

            result.innerHTML = `

                <div
                    class="result"
                    style="color:#4ade80"
                >

                    🎉 Correct!

                    <br><br>

                    Chapter completed! ✅

                    <br>

                    +25 XP ⭐

                </div>

            `;

        } else {

            result.innerHTML = `

                <div
                    class="result"
                    style="color:#4ade80"
                >

                    ✅ Correct!

                    <br><br>

                    This chapter was already completed.

                </div>

            `;
        }

    } else {

        result.innerHTML = `

            <div
                class="result"
                style="color:#fb7185"
            >

                ❌ Not quite.

                <br><br>

                Try reviewing the lesson
                and answer again.

            </div>

        `;
    }
}


/* =====================================================
   QUIZ
===================================================== */

async function openQuiz() {

    console.log("QUIZ OPEN");

    try {

        if (!quizData.length) {

            const response =
                await fetch("/api/quiz");

            if (!response.ok) {
                throw new Error(
                    "Quiz API returned " +
                    response.status
                );
            }

            quizData =
                await response.json();
        }

        if (!quizData.length) {
            throw new Error(
                "No quiz questions found."
            );
        }

        showQuizQuestion();

    } catch (error) {

        console.error(
            "QUIZ ERROR:",
            error
        );

        showModal(`

            <h2>
                ⚠️ Quiz unavailable
            </h2>

            <div class="result">
                ${escapeHtml(error.message)}
            </div>

        `);
    }
}


function showQuizQuestion() {

    const question =
        quizData[
            Math.floor(
                Math.random() *
                quizData.length
            )
        ];

    let html = `

        <h2>
            🧠 Quiz Arena
        </h2>

        <div class="quiz-question">
            ${escapeHtml(
                question.question
            )}
        </div>

        <div id="quizOptions"></div>

        <div id="quizResult"></div>

    `;

    showModal(html);

    const optionsBox =
        document.getElementById(
            "quizOptions"
        );

    question.options.forEach(
        (option, index) => {

            const button =
                document.createElement(
                    "button"
                );

            button.type = "button";

            button.className =
                "option";

            button.textContent =
                `${String.fromCharCode(
                    65 + index
                )}. ${option}`;

            button.addEventListener(
                "click",
                function () {

                    checkQuiz(
                        index,
                        Number(question.answer),
                        question.explanation
                    );
                }
            );

            optionsBox.appendChild(
                button
            );
        }
    );
}


function checkQuiz(
    selected,
    correct,
    explanation
) {

    const result =
        document.getElementById(
            "quizResult"
        );

    if (!result) {
        return;
    }

    if (
        Number(selected) === Number(correct)
    ) {

        addXP(10);

        result.innerHTML = `

            <div
                class="result"
                style="color:#4ade80"
            >

                🎉 CORRECT!

                <br><br>

                +10 XP ⭐

                <br><br>

                ${escapeHtml(
                    explanation
                )}

                <br><br>

                <button
                    type="button"
                    class="primary"
                    id="nextQuiz"
                >
                    NEXT QUESTION →
                </button>

            </div>

        `;

        document
            .getElementById("nextQuiz")
            .addEventListener(
                "click",
                showQuizQuestion
            );

    } else {

        result.innerHTML = `

            <div
                class="result"
                style="color:#fb7185"
            >

                ❌ Not quite!

                <br><br>

                ${escapeHtml(
                    explanation
                )}

                <br><br>

                <button
                    type="button"
                    class="primary"
                    id="tryQuiz"
                >
                    TRY ANOTHER →
                </button>

            </div>

        `;

        document
            .getElementById("tryQuiz")
            .addEventListener(
                "click",
                showQuizQuestion
            );
    }
}


/* =====================================================
   CODE CHALLENGE
===================================================== */

async function openCodeChallenge() {

    try {

        if (!codeData.length) {

            const response =
                await fetch(
                    "/api/code-challenges"
                );

            if (!response.ok) {
                throw new Error(
                    "Challenge API returned " +
                    response.status
                );
            }

            codeData =
                await response.json();
        }

        if (!codeData.length) {
            throw new Error(
                "No challenges found."
            );
        }

        const challenge =
            codeData[
                Math.floor(
                    Math.random() *
                    codeData.length
                )
            ];

        let html = `

            <h2>
                💻 Code Challenge
            </h2>

            <p style="
                color:#aaa;
                margin:15px 0;
            ">
                ${escapeHtml(
                    challenge.question
                )}
            </p>

            <pre class="example">${escapeHtml(
                challenge.code
            )}</pre>

            <div id="codeOptions"></div>

            <div id="codeResult"></div>

        `;

        showModal(html);

        const optionsBox =
            document.getElementById(
                "codeOptions"
            );

        challenge.options.forEach(
            (option, index) => {

                const button =
                    document.createElement(
                        "button"
                    );

                button.type = "button";

                button.className =
                    "option";

                button.textContent =
                    `${String.fromCharCode(
                        65 + index
                    )}. ${option}`;

                button.addEventListener(
                    "click",
                    function () {

                        checkCodeAnswer(
                            index,
                            Number(
                                challenge.answer
                            ),
                            challenge.explanation
                        );
                    }
                );

                optionsBox.appendChild(
                    button
                );
            }
        );

    } catch (error) {

        console.error(
            "CODE CHALLENGE ERROR:",
            error
        );

        showModal(`

            <h2>
                ⚠️ Challenge unavailable
            </h2>

            <div class="result">
                ${escapeHtml(error.message)}
            </div>

        `);
    }
}


function checkCodeAnswer(
    selected,
    correct,
    explanation
) {

    const result =
        document.getElementById(
            "codeResult"
        );

    if (!result) {
        return;
    }

    if (
        Number(selected) === Number(correct)
    ) {

        addXP(15);

        solvedChallenges++;

        localStorage.setItem(
            "codequest_challenges",
            String(solvedChallenges)
        );

        result.innerHTML = `

            <div
                class="result"
                style="color:#4ade80"
            >

                🧠 Correct!

                <br><br>

                +15 XP ⭐

                <br><br>

                ${escapeHtml(
                    explanation
                )}

                <br><br>

                <button
                    type="button"
                    class="primary"
                    id="nextCode"
                >
                    NEXT CHALLENGE →
                </button>

            </div>

        `;

        document
            .getElementById("nextCode")
            .addEventListener(
                "click",
                openCodeChallenge
            );

    } else {

        result.innerHTML = `

            <div
                class="result"
                style="color:#fb7185"
            >

                ❌ Incorrect

                <br><br>

                ${escapeHtml(
                    explanation
                )}

            </div>

        `;
    }
}


/* =====================================================
   ERROR FINDER
===================================================== */

async function openErrorFinder() {

    try {

        if (!errorData.length) {

            const response =
                await fetch(
                    "/api/error-finder"
                );

            if (!response.ok) {
                throw new Error(
                    "Error Finder API returned " +
                    response.status
                );
            }

            errorData =
                await response.json();
        }

        if (!errorData.length) {
            throw new Error(
                "No error challenges found."
            );
        }

        const challenge =
            errorData[
                Math.floor(
                    Math.random() *
                    errorData.length
                )
            ];

        let html = `

            <h2>
                🔍 Error Finder
            </h2>

            <p style="
                color:#aaa;
                margin:15px 0;
            ">
                ${escapeHtml(
                    challenge.question
                )}
            </p>

            <pre class="example">${escapeHtml(
                challenge.code
            )}</pre>

            <div id="errorOptions"></div>

            <div id="errorResult"></div>

        `;

        showModal(html);

        const optionsBox =
            document.getElementById(
                "errorOptions"
            );

        challenge.options.forEach(
            (option, index) => {

                const button =
                    document.createElement(
                        "button"
                    );

                button.type = "button";

                button.className =
                    "option";

                button.textContent =
                    `${String.fromCharCode(
                        65 + index
                    )}. ${option}`;

                button.addEventListener(
                    "click",
                    function () {

                        checkError(
                            index,
                            Number(
                                challenge.answer
                            ),
                            challenge.explanation
                        );
                    }
                );

                optionsBox.appendChild(
                    button
                );
            }
        );

    } catch (error) {

        console.error(
            "ERROR FINDER ERROR:",
            error
        );

        showModal(`

            <h2>
                ⚠️ Error Finder unavailable
            </h2>

            <div class="result">
                ${escapeHtml(error.message)}
            </div>

        `);
    }
}


function checkError(
    selected,
    correct,
    explanation
) {

    const result =
        document.getElementById(
            "errorResult"
        );

    if (!result) {
        return;
    }

    if (
        Number(selected) === Number(correct)
    ) {

        addXP(20);

        solvedChallenges++;

        localStorage.setItem(
            "codequest_challenges",
            String(solvedChallenges)
        );

        result.innerHTML = `

            <div
                class="result"
                style="color:#4ade80"
            >

                🔥 ERROR FOUND!

                <br><br>

                +20 XP ⭐

                <br><br>

                ${escapeHtml(
                    explanation
                )}

            </div>

        `;

    } else {

        result.innerHTML = `

            <div
                class="result"
                style="color:#fb7185"
            >

                ❌ Keep looking!

                <br><br>

                ${escapeHtml(
                    explanation
                )}

            </div>

        `;
    }
}


/* =====================================================
   CAREER
===================================================== */

function careerAssistant() {

    showModal(`

        <h2>
            🤖 CodeQuest AI Career Assistant
        </h2>

        <p style="
            color:#aaa;
            line-height:1.7;
            margin-top:18px;
        ">
            Choose a career path:
        </p>

        <button
            type="button"
            class="option"
            onclick="careerResult('developer')"
        >
            💻 Software Developer
        </button>

        <button
            type="button"
            class="option"
            onclick="careerResult('data')"
        >
            📊 Data / AI Career
        </button>

        <button
            type="button"
            class="option"
            onclick="careerResult('web')"
        >
            🌐 Web Developer
        </button>

        <button
            type="button"
            class="option"
            onclick="careerResult('app')"
        >
            📱 App Developer
        </button>

    `);
}


function careerResult(type) {

    const ideas = {

        developer:
            "C/C++ → OOP → DSA → Java/Python → Git → Projects → Internship",

        data:
            "Python → Excel → SQL → Statistics → Pandas → Data Projects",

        web:
            "HTML → CSS → JavaScript → Flask → APIs → Full Stack Projects",

        app:
            "Java/Kotlin → Android → APIs → Databases → App Projects"
    };

    showModal(`

        <h2>
            🧠 Suggested Learning Path
        </h2>

        <div class="lesson-box">

            <p style="
                color:#c084fc;
                font-size:18px;
            ">
                ${escapeHtml(
                    ideas[type]
                )}
            </p>

        </div>

        <button
            type="button"
            class="primary"
            onclick="closeModal()"
        >
            START MY JOURNEY 🚀
        </button>

    `);
}


/* =====================================================
   COMPILER
===================================================== */

function compiler() {

    showModal(`

        <h2>
            ▶️ Online Compiler
        </h2>

        <p style="
            color:#aaa;
            margin:15px 0;
        ">
            Write code here.
        </p>

        <textarea
            id="codeEditor"
            style="
                width:100%;
                min-height:250px;
                background:#050507;
                color:#d8b4fe;
                border:1px solid #33333d;
                border-radius:12px;
                padding:15px;
                font-family:monospace;
                resize:vertical;
            "
            placeholder="Write your code here..."
        ></textarea>

        <button
            type="button"
            class="primary"
            onclick="runCompiler()"
        >
            ▶ RUN CODE
        </button>

        <div id="compilerResult"></div>

    `);
}


function runCompiler() {

    const result =
        document.getElementById(
            "compilerResult"
        );

    if (result) {

        result.innerHTML = `

            <div class="result">

                🚧 Compiler engine is the next upgrade.

                <br><br>

                The editor is ready.

            </div>

        `;
    }
}


/* =====================================================
   PROGRESS
===================================================== */

function showProgress() {

    const level =
        Math.floor(xp / 100) + 1;

    showModal(`

        <h2>
            🏆 My Progress
        </h2>

        <div class="stats-grid">

            <div class="stat">
                ⭐ XP
                <strong>${xp}</strong>
            </div>

            <div class="stat">
                🎯 Level
                <strong>${level}</strong>
            </div>

            <div class="stat">
                📚 Chapters
                <strong>
                    ${completedChapters.length}
                </strong>
            </div>

            <div class="stat">
                🧠 Challenges
                <strong>
                    ${solvedChallenges}
                </strong>
            </div>

        </div>

        <div class="result">

            Keep learning and completing
            challenges to increase your XP! 🚀

        </div>

    `);
}


/* =====================================================
   MODAL BACKGROUND CLICK
===================================================== */

const modal =
    document.getElementById("modal");

if (modal) {

    modal.addEventListener(
        "click",
        function(event) {

            if (event.target === modal) {
                closeModal();
            }

        }
    );
}


/* =====================================================
   START
===================================================== */

updateProgress();

console.log(
    "✅ CodeQuest AI JavaScript loaded successfully."
);

</script>
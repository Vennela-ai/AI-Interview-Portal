// =========================
// Interview Navigation
// =========================

const cards = document.querySelectorAll(".question-card");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const submitBtn = document.getElementById("submitBtn");

const progressFill = document.querySelector(".progress-fill");
const progressText = document.getElementById("progressText");
const questionCounter = document.getElementById("questionCounter");

let currentQuestion = 0;
const totalQuestions = cards.length;

// =========================
// Show Current Question
// =========================

function updateQuestion() {

    cards.forEach(card => card.classList.add("hidden"));

    cards[currentQuestion].classList.remove("hidden");

    questionCounter.innerHTML =
        `Question ${currentQuestion + 1} / ${totalQuestions}`;

    let percent = Math.round(((currentQuestion + 1) / totalQuestions) * 100);

    progressText.innerHTML = percent + "%";

    progressFill.style.width = percent + "%";

    prevBtn.disabled = currentQuestion === 0;

    if (currentQuestion === totalQuestions - 1) {

        nextBtn.style.display = "none";
        submitBtn.classList.remove("hidden");

    } else {

        nextBtn.style.display = "inline-block";
        submitBtn.classList.add("hidden");

    }

}

// =========================
// Next
// =========================

nextBtn.addEventListener("click", () => {

    if (currentQuestion < totalQuestions - 1) {

        currentQuestion++;

        updateQuestion();

    }

});

// =========================
// Previous
// =========================

prevBtn.addEventListener("click", () => {

    if (currentQuestion > 0) {

        currentQuestion--;

        updateQuestion();

    }

});

// =========================
// Character Counter
// =========================

document.querySelectorAll("textarea").forEach((textarea) => {

    const counter = textarea.parentElement.querySelector(".char-count");

    textarea.addEventListener("input", () => {

        counter.textContent =
            textarea.value.length + " Characters";

    });

});

// =========================
// Auto Save
// =========================

document.querySelectorAll("textarea").forEach((textarea, index) => {

    textarea.value =
        localStorage.getItem("answer_" + index) || "";

    textarea.dispatchEvent(new Event("input"));

    textarea.addEventListener("input", () => {

        localStorage.setItem(
            "answer_" + index,
            textarea.value
        );

    });

});

// =========================
// Clear Storage
// =========================

document.getElementById("interviewForm")
.addEventListener("submit", () => {

    document.querySelectorAll("textarea")
    .forEach((textarea, index) => {

        localStorage.removeItem("answer_" + index);

    });

});

// =========================
// Submit Confirmation
// =========================

document.getElementById("interviewForm")
.addEventListener("submit", function(e){

    if(!confirm("Submit Interview?")){

        e.preventDefault();

    }

});

// =========================
// Timer
// =========================

let timeLeft = 20 * 60;

const timer = document.getElementById("timer");

setInterval(() => {

    let min = Math.floor(timeLeft / 60);

    let sec = timeLeft % 60;

    timer.innerHTML =
        `${min}:${String(sec).padStart(2,"0")}`;

    if(timeLeft <= 0){

        document.getElementById("interviewForm").submit();

    }

    timeLeft--;

},1000);

// =========================
// Initialize
// =========================

updateQuestion();
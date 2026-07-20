

const cards = document.querySelectorAll(".question-card");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const submitBtn = document.getElementById("submitBtn");
const counter = document.getElementById("questionCounter");
const progressFill = document.querySelector(".progress-fill");
const progressText = document.getElementById("progressText");
const form = document.getElementById("interviewForm");

let currentQuestion = 0;
const totalQuestions = cards.length;
function updateQuestion() {

    cards.forEach(card => card.classList.add("hidden"));

    cards[currentQuestion].classList.remove("hidden");

    counter.textContent =
        `Question ${currentQuestion + 1} / ${totalQuestions}`;

    prevBtn.disabled = currentQuestion === 0;

    if (currentQuestion === totalQuestions - 1) {

        nextBtn.style.display = "none";
        submitBtn.style.display = "inline-block";

    } else {

        nextBtn.style.display = "inline-block";
        submitBtn.style.display = "none";

    }

    let percent =
        ((currentQuestion + 1) / totalQuestions) * 100;

    progressFill.style.width = percent + "%";
    progressText.textContent = Math.round(percent) + "%";
}

nextBtn.addEventListener("click", () => {

    if (currentQuestion < totalQuestions - 1) {

        currentQuestion++;
        updateQuestion();

    }

});

prevBtn.addEventListener("click", () => {

    if (currentQuestion > 0) {

        currentQuestion--;
        updateQuestion();

    }

});

document.querySelectorAll("textarea").forEach((area) => {

    const counter = area.parentElement.querySelector(".char-count");

    area.addEventListener("input", () => {

        counter.textContent =
            area.value.length + " characters";

    });

});

document.querySelectorAll("textarea").forEach((area, index) => {

    const saved = localStorage.getItem("answer_" + index);

    if (saved) {

        area.value = saved;

    }

    area.dispatchEvent(new Event("input"));

    area.addEventListener("input", () => {

        localStorage.setItem(
            "answer_" + index,
            area.value
        );

    });

});

const timer = document.getElementById("timer");

let timeLeft = 20 * 60;

const countdown = setInterval(() => {

    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;

    timer.textContent =
        `${minutes}:${String(seconds).padStart(2, "0")}`;

    if (timeLeft <= 0) {

        clearInterval(countdown);

        alert("Time is up!");

        form.submit();

    }

    timeLeft--;

}, 1000);

// ============================
// SUBMIT
// ============================

form.addEventListener("submit", function(e){

    if(!confirm("Submit your interview?")){

        e.preventDefault();
        return;

    }

    document.querySelectorAll("textarea").forEach((area,index)=>{

        localStorage.removeItem("answer_"+index);

    });

});



updateQuestion();
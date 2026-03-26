let currentQuestion = "";
let recognition;

// TEXT TO SPEECH
function speakText(text) {

    if (!("speechSynthesis" in window)) return;

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";
    speech.rate = 0.95;  // slower = more natural
    speech.pitch = 1.1;  // slightly expressive

    window.speechSynthesis.cancel();

    setTimeout(() => {
        window.speechSynthesis.speak(speech);
    }, 150);
}

//  START INTERVIEW
async function startInterview() {

    const role = document.getElementById("role").value;
    const level = document.getElementById("level").value;

    try {

        const response = await fetch("/start_interview", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ role, level })
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("interviewArea").style.display = "block";
        document.getElementById("resultArea").style.display = "none";

        document.getElementById("questionText").innerText = data.question;

        document.getElementById("questionCounter").innerText =
            `Question ${data.question_number} of ${data.total_questions}`;

        currentQuestion = data.question;

        speakText(data.question);

    } catch (error) {

        console.error(error);
        alert("Error starting interview. Check backend.");

    }
}


//  SPEAK AGAIN
function speakQuestion() {
    if (currentQuestion) {
        speakText(currentQuestion);
    }
}


//  VOICE INPUT
function startListening() {

    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Speech recognition not supported. Use Google Chrome.");
        return;
    }

    recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("answerBox").value = transcript;
    };

    recognition.onerror = function (event) {
        console.error(event);
        alert("Speech recognition error: " + event.error);
    };
}


//  SUBMIT ANSWER (FIXED VERSION)
async function submitAnswer() {

    const answer = document.getElementById("answerBox").value.trim();

    if (!answer) {
        alert("Please type or speak your answer first.");
        return;
    }

    try {

        const response = await fetch("/submit_interview_answer", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ answer })
        });

        const data = await response.json();

        //  INTERVIEW FINISHED
        if (data.finished) {

            document.getElementById("interviewArea").style.display = "none";
            document.getElementById("resultArea").style.display = "block";

            //  SCORE
            document.getElementById("finalResult").innerText =
                `Final Score: ${data.final_score}% | Correct Answers: ${data.correct_answers}/${data.total_questions}`;

            //  EXPECTED ANSWERS / FEEDBACK
            let answersHTML = "<h3>Interview Feedback:</h3>";

            if (data.details && data.details.length > 0) {

                data.details.forEach((item, index) => {

                    answersHTML += `
                        <div class="answer-card">
                            <p><strong>Q${index + 1}: ${item.question}</strong></p>
                            <p><b>Your Answer:</b> ${item.user_answer}</p>
                            <p><b>Score:</b> ${item.score}%</p>
                            <p style="color: lightgreen;"><b>✔ Strengths:</b> ${item.matched.join(", ") || "None"}</p>
                            <p style="color: orange;"><b>⚠ Missing:</b> ${item.missing.join(", ") || "None"}</p>
                            <p style="color: cyan;"><b>💡 Feedback:</b> ${item.feedback}</p>
                            <p><b>Expected Answer:</b> ${item.expected_answer}</p>
                        </div>
                        <hr>
                    `;
                });

            } else {

                answersHTML += "<p>No answers available.</p>";
            }

            document.getElementById("expectedAnswers").innerHTML = answersHTML;

            //  SPEAK RESULT
            let finalVoice = "";

            if (data.final_score >= 75) {
                finalVoice = `Excellent performance. You are interview ready. Your score is ${data.final_score} percent.`;
            } 
            else if (data.final_score >= 50) {
                finalVoice = `Good effort. You can improve further. Your score is ${data.final_score} percent.`;
            } 
            else {
                finalVoice = `You need more practice. Don't worry, keep learning. Your score is ${data.final_score} percent.`;
            }

            speakText(finalVoice);

            //  SCROLL
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: "smooth"
            });

        } 
        
        //  NEXT QUESTION
        else {

            document.getElementById("answerBox").value = "";

            document.getElementById("questionText").innerText = data.next_question;

            document.getElementById("questionCounter").innerText =
                `Question ${data.question_number} of ${data.total_questions}`;

            currentQuestion = data.next_question;

            let feedbackVoice = "";

// AI-like feedback
            if (data.last_score >= 70) {
                feedbackVoice = "Good answer. Let's move to the next question.";
            } 
            else if (data.last_score >= 40) {
                feedbackVoice = "Not bad, but you missed some important points.";
            } 
            else {
                feedbackVoice = "You should improve this concept. Let's continue.";
            }

//  Speak feedback + next question
            speakText(feedbackVoice + " " + data.next_question);
        }

    } catch (error) {

        console.error(error);
        alert("Error submitting answer. Check backend.");

    }
}
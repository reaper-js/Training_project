const container = document.getElementById('question-container');
const feedbackMessageEl = document.getElementById('feedback-message');
let currentQuestionIndex = 0;
let questions = [];

// Function to preload all questions
function preloadQuestions() {
    fetch('http://localhost:5000/ask-question')  // Replace with the appropriate endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(allQuestions => {
            questions = allQuestions;
            if (questions.length > 0) {
                displayQuestion();
            } else {
                container.innerHTML = '<p>No questions available.</p>';
            }
        })
        .catch(error => {
            feedbackMessageEl.textContent = 'Error fetching questions: ' + error;
        });
}

// Function to display the current question
function displayQuestion() {
    const currentQuestion = questions[currentQuestionIndex];

    if (currentQuestion) {
        console.log('Current question:', currentQuestion);

        const questionDiv = document.createElement('div');

        const questionTextEl = document.createElement('div');
        questionTextEl.textContent = currentQuestion.text;

        const responseForm = document.createElement('form');
        responseForm.addEventListener('submit', function (event) {
            event.preventDefault();
            handleResponseSubmit(currentQuestion.id, responseForm);
        });

        let responseInput;
        if (currentQuestion.type === 'descriptive') {
            responseInput = createDescriptiveInput();
        } else if (currentQuestion.type === 'yes_no') {
            responseInput = createTrueFalseOptions();
        } else if (currentQuestion.type === 'mcq') {
            responseInput = createMcqOptions(currentQuestion.options);
        }

        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.textContent = 'Submit';

        responseForm.appendChild(responseInput);
        responseForm.appendChild(submitButton);

        questionDiv.appendChild(questionTextEl);
        questionDiv.appendChild(responseForm);

        // Ensure that questionDiv is a valid DOM element
        if (questionDiv instanceof Node) {
            // Append the new questionDiv directly without clearing the container
            container.innerHTML = ''; // Clear the container before appending the new question
            container.appendChild(questionDiv);
        } else {
            console.error('Error creating questionDiv:', questionDiv);
        }
    } else {
        container.innerHTML = '<p>No more questions available.</p>';
    }
}



// Function to create a descriptive input
function createDescriptiveInput() {
    const input = document.createElement('textarea');
    input.name = 'answer';
    input.placeholder = 'Your answer...';
    return input;
}

// Function to create true/false options
function createTrueFalseOptions() {
    const trueOption = document.createElement('input');
    trueOption.type = 'radio';
    trueOption.name = 'answer';
    trueOption.value = 'true';
    trueOption.id = 'true-option';

    const falseOption = document.createElement('input');
    falseOption.type = 'radio';
    falseOption.name = 'answer';
    falseOption.value = 'false';
    falseOption.id = 'false-option';

    const trueLabel = document.createElement('label');
    trueLabel.htmlFor = 'true-option';
    trueLabel.textContent = 'True';

    const falseLabel = document.createElement('label');
    falseLabel.htmlFor = 'false-option';
    falseLabel.textContent = 'False';

    const optionsContainer = document.createElement('div');
    optionsContainer.appendChild(trueOption);
    optionsContainer.appendChild(trueLabel);
    optionsContainer.appendChild(falseOption);
    optionsContainer.appendChild(falseLabel);

    return optionsContainer;
}

// Function to create multiple-choice options
function createMcqOptions(options) {
    const ul = document.createElement('ul');
    options.forEach((option, index) => {
        const li = document.createElement('li');
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'answer';
        radio.value = index; // Assuming the index is the correct answer
        li.textContent = option;
        li.appendChild(radio);
        ul.appendChild(li);
    });
    return ul;
}



let startTime = null; // Initialize startTime to null

function startTimer() {
    startTime = new Date().getTime(); // Capture the start time
}

function handleResponseSubmit(questionId, form) {
    const formData = new FormData(form);
    const userResponse = formData.get('answer');

    // If startTime is null, initialize the timer
    if (startTime === null) {
        startTimer();
    } else {
        // Capture the time before submitting the form in milliseconds
        const currentTime = new Date().getTime();

        // Calculate elapsed time in seconds
        const elapsedTime = (currentTime - startTime) / 1000;

        // You can send the user response and time taken to the backend if needed
        fetch('http://localhost:5000/submit-answers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ questionId, userResponse, elapsedTime }),
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server if needed
            console.log(data);

            // Move to the next question
            currentQuestionIndex += 1;

            // Reset the timer
            startTimer();

            // Display the next question
            displayQuestion();
        })
        .catch(error => {
            console.error('Error submitting response:', error);
        });
    }
}

// Example: Start the timer when fetching questions
startTimer();


// Load all questions initially
preloadQuestions();

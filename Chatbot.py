from flask import Flask, render_template_string, request, jsonify
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

app = Flask(__name__)

# LangChain setup
template = """Question: {question}
              You are a friendly and helpful chatbot that gently responds to the user query.
              Keep your response concise.
"""

prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.2:1b")
chain = prompt | model

# HTML content with bright mode and updated font
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matrix Chatbot - Bright Mode</title>
    <!-- Google Font (Roboto) -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif; /* Changed font to Roboto */
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #ffffff; /* White background */
            color: #000000; /* Black text */
        }
        h1, h2, h3 {
            color: #0073e6; /* Bright blue color for headings */
            margin: 0;
            padding: 0;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        h2 {
            font-size: 1.3rem;
            margin-bottom: 20px;
        }
        #chat-box {
            width: 80%;
            max-width: 700px;
            height: 60%;
            max-height: 70vh;
            background-color: #f0f0f0; /* Light gray for chat box */
            border-radius: 10px;
            padding: 20px;
            overflow-y: auto;
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
            border: 1px solid #ccc; /* Light border for chat box */
        }
        .message {
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 20px;
            max-width: 80%;
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
        }
        .message.user {
            background-color: #cce7ff; /* Light blue for user messages */
            color: #000000; /* Black text for user messages */
            align-self: flex-end;
            text-align: right;
            margin-left: auto;
        }
        .message.bot {
            background-color: #e0e0e0; /* Light gray for bot messages */
            color: #000000; /* Black text for bot messages */
            align-self: flex-start;
        }
        .message.appear {
            opacity: 1;
        }
        #loading-indicator {
            display: none;
            align-self: flex-start;
            margin-bottom: 10px;
        }
        #loading-indicator .dot {
            height: 10px;
            width: 10px;
            margin: 0 2px;
            background-color: #0073e6; /* Bright blue for loading dots */
            border-radius: 50%;
            display: inline-block;
            animation: bounce 1s infinite ease-in-out;
        }
        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-10px);
            }
        }
        #user-input {
            width: 80%;
            max-width: 600px;
            padding: 15px;
            font-size: 16px;
            border: none;
            border-radius: 30px;
            background-color: #e8e8e8; /* Light gray for input */
            color: #000000; /* Black text for input */
        }
        #user-input::placeholder {
            color: #666666; /* Darker gray for placeholder */
            font-size: 14px;
        }
        #send-button {
            padding: 15px 30px;
            font-size: 16px;
            color: white;
            background-color: #0073e6; /* Bright blue for button */
            border: none;
            border-radius: 30px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        #send-button:hover {
            background-color: #005bb5; /* Darker blue on hover */
            transform: scale(1.05); /* Slightly larger on hover */
        }
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
</head>
<body>

    <h1>Welcome to the Matrix Chatbot</h1>
    <h2>Ask me anything, and I'll guide you through the matrix!</h2>

    <div id="chat-box">
        <div id="loading-indicator">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </div>
    </div>

    <h3>Enter your prompt below:</h3>
    
    <div class="container">
        <input type="text" id="user-input" placeholder="Type your question here...">
        <button id="send-button">Send</button>
    </div>

    <script>
        document.getElementById('send-button').addEventListener('click', sendMessage);

        document.getElementById('user-input').addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });

        async function sendMessage() {
            const question = document.getElementById('user-input').value;
            if (question) {
                addMessage('user', question);
                document.getElementById('user-input').value = '';
                showLoadingIndicator();
                
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: question }),
                });

                const data = await response.json();
                hideLoadingIndicator();
                if (data.response) {
                    addMessage('bot', data.response);
                } else {
                    addMessage('bot', 'Error: ' + data.error);
                }
            }
        }

        function addMessage(sender, message) {
            const chatBox = document.getElementById('chat-box');
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            messageDiv.classList.add(sender);
            messageDiv.innerText = message;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;

            // Add appear animation
            setTimeout(() => messageDiv.classList.add('appear'), 50);
        }

        function showLoadingIndicator() {
            const loadingIndicator = document.getElementById('loading-indicator');
            loadingIndicator.style.display = 'flex';
        }

        function hideLoadingIndicator() {
            const loadingIndicator = document.getElementById('loading-indicator');
            loadingIndicator.style.display = 'none';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_content)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '')
    if question:
        response = chain.invoke({"question": question})
        return jsonify({"response": response})
    return jsonify({"error": "No question provided"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

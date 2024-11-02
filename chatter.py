from flask import Flask, render_template_string, request, jsonify
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from pyngrok import ngrok

app = Flask(__name__)

# Chatbot prompt template
template = """Question: {question}
              You are a friendly and helpful chatbot that gently responds to the user query.
              Keep your response concise.
"""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.2:1b")

# HTML template with blue Send button and dark background
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #000000;  /* Black background */
            padding: 0;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #ffffff;  /* White text */
        }
        #chat {
            background-color: #1c1c1e;  /* Dark gray background for chat window */
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
            max-width: 450px;
            width: 100%;
            display: flex;
            flex-direction: column;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #ffffff;
            font-size: 1.5rem;
            margin-bottom: 20px;
        }
        #messages {
            border: 1px solid #444;
            padding: 15px;
            height: 300px;
            overflow-y: auto;
            background-color: #2c2c2e;
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.05);
        }
        #messages div {
            margin-bottom: 10px;
        }
        #messages div strong {
            color: #4da6ff;  /* Light blue text for usernames */
        }
        #userInput {
            width: 100%;
            padding: 12px;
            border-radius: 5px;
            border: 1px solid #555;
            background-color: #2c2c2e;
            color: white;
            margin-top: 10px;
        }
        #sendButton {
            padding: 10px 20px;
            margin-top: 10px;
            width: 100%;
            background-color: #4da6ff;  /* Blue button */
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            transition: background-color 0.3s;
        }
        #sendButton:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        #sendButton:hover:not(:disabled) {
            background-color: #1e90ff;
        }
        #chatContainer {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
    </style>
</head>
<body>
    <div id="chat">
        <h1>AI Chatbot</h1>
        <div id="messages" aria-live="polite" aria-relevant="additions"></div>
        <div id="chatContainer">
            <input type="text" id="userInput" placeholder="Ask a question..." aria-label="Your question" />
            <button id="sendButton" disabled>Send</button>
        </div>
    </div>

    <script>
        const inputField = document.getElementById('userInput');
        const sendButton = document.getElementById('sendButton');
        const messagesDiv = document.getElementById('messages');

        inputField.addEventListener('input', () => {
            sendButton.disabled = !inputField.value.trim();
        });

        sendButton.onclick = function() {
            const question = inputField.value.trim();
            if (!question) return;

            sendButton.disabled = true;
            messagesDiv.innerHTML += `<div><strong>You:</strong> ${question}</div>`;
            fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            })
            .then(response => response.json())
            .then(data => {
                messagesDiv.innerHTML += `<div><strong>Bot:</strong> ${data.response}</div>`;
                inputField.value = '';
                sendButton.disabled = false;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            })
            .catch(err => {
                messagesDiv.innerHTML += `<div><strong>Error:</strong> Failed to get a response.</div>`;
                sendButton.disabled = false;
            });
        };

        inputField.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendButton.click();
            }
        });
    </script>
</body>
</html>
"""

# Home route to serve HTML template
@app.route('/')
def home():
    return render_template_string(html_template)

# Chatbot response route
@app.route('/ask', methods=['POST'])
def ask():
    question = request.json['question']
    response = (prompt | model).invoke({"question": question})
    return jsonify({'response': response})

# Start Flask app with ngrok tunneling for public access
if __name__ == '__main__':
    # Open a ngrok tunnel on port 5000
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")
    
    # Run Flask app
    app.run(host="0.0.0.0", port=5000)

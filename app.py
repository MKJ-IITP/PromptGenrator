from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "need to put API Key here"
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_prompt', methods=['POST'])
def generate_prompt():
    try:
        context = request.form['context']
        transcript_file = request.files['transcript_file']

        # Read the file content
        transcript_text = transcript_file.read().decode("utf-8")

        # Create prompt for ChatGPT
        prompt = f"{context}\n\nCall Transcript:\n{transcript_text}\n\nGenerate meaningful prompt keys and messages."

        # Use the Chat Completion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150  # Adjust the max tokens as needed
        )

        # Extract the generated response
        message = response['choices'][0]['message']['content']
        # Assume the response format as "Prompt Key: <key>, Prompt Message: <message>"
        lines = message.split('\n')
        prompt_key = lines[0].split(': ')[1] if len(lines) > 0 else "No Key Generated"
        prompt_message = lines[1].split(': ')[1] if len(lines) > 1 else "No Message Generated"

        return jsonify({"prompt_key": prompt_key, "prompt_message": prompt_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

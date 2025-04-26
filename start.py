from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from werkzeug.utils import secure_filename
import os
import utils
import tiktoken

UPLOAD_FOLDER = './uploads'
FILE_CONTENT = None
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set you api key in config file named API_KEY
# or set the OPENAI_API_KEY Environment Variable
# Unix/Linux/MacOS: export OPENAI_API_KEY=your_api_key
# Windows: set OPENAI_API_KEY=your_api_key
client = OpenAI(api_key=open('API_KEY').read().strip())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config', methods=['POST'])
def config():
    global OpenAI
    OpenAI.api_key = request.form['openai_key']
    # other config here
    return jsonify({'success': True})


@app.route('/upload', methods=['POST'])
def success():
    if request.method == 'POST':
        file = request.files['file']
        if file and utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'success': True})
            #return render_template("Acknowledgement.html", name=f.filename)

@app.route('/message', methods=['POST'])
def send_message():
    # Get the JSON data from the request
    data = request.get_json()
    # Extract the content from the JSON data
    content = data.get('content')

    # Here you can process the received message, for now, let's just print it
    print("Received message:", content)

    # response = "Message received successfully!"
    response = send_request(content)
    return jsonify({'response': response})

# Modify your send_request function
def send_request(user_input):
    file_content = utils.getFileContent(UPLOAD_FOLDER)

    # Combine user input and file content
    analysis_input = f"With the following user input: {user_input}, please analyze these log messages:\n{file_content}"

    # Function to estimate token count
    def num_tokens_from_string(text, model_name="gpt-3.5-turbo"):
        encoding = tiktoken.encoding_for_model(model_name)
        return len(encoding.encode(text))

    # Define limits
    MAX_TOKENS = 14000  # Leave some buffer under 16,385 tokens for response tokens

    # If the total analysis input is too large, split it
    if num_tokens_from_string(analysis_input) > MAX_TOKENS:
        print("Large input detected. Splitting into chunks...")
        chunks = split_text_into_chunks(file_content, max_tokens=MAX_TOKENS - 2000)
        responses = []

        for idx, chunk in enumerate(chunks):
            chunk_input = f"With the following user input: {user_input}, please analyze these log messages (chunk {idx+1}):\n{chunk}"
            analysis = [
                {"role": "system", "content": "You are a Site Reliability Engineer, please review logs messages and suggest the root cause and how to fix it."},
                {"role": "user", "content": chunk_input}
            ]
            analysis_response = client.responses.create(
                model="ft:gpt-3.5-turbo-1106:personal::BQXPzaI8",
                input=analysis,
            )
            partial_response = analysis_response.output_text
            responses.append(partial_response)

        # Combine all partial responses
        response = "\n\n".join(responses)
    else:
        # If small enough, send as single request
        analysis = [
            {"role": "system", "content": "You are a Site Reliability Engineer, please review logs messages and suggest the root cause and how to fix it."},
            {"role": "user", "content": analysis_input}
        ]
        analysis_response = client.responses.create(
            model="ft:gpt-3.5-turbo-1106:personal::BQXPzaI8",
            input=analysis,
        )
        response = analysis_response.output_text

    print(response)
    # Minor cleanups
    response = response.replace('\n', '\\n')
    response = response.replace('####', '')
    response = response.replace('###', '')
    return response

# Helper function to split large text
def split_text_into_chunks(text, max_tokens=14000, model_name="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model_name)
    words = text.split()
    current_chunk = []
    current_tokens = 0

    for word in words:
        token_len = len(encoding.encode(word + " "))
        if current_tokens + token_len > max_tokens:
            yield ' '.join(current_chunk)
            current_chunk = []
            current_tokens = 0
        current_chunk.append(word)
        current_tokens += token_len

    if current_chunk:
        yield ' '.join(current_chunk)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
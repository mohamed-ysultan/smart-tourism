import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from thread_manager import ThreadManager
from assistant_manager import AssistantManager
import openai

# Load environment variables
load_dotenv()

client = openai.OpenAI()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # تحميل المفتاح السري من البيئة

# Flask route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to assist the user
@app.route('/assist', methods=['POST'])
def assist():
    data = request.get_json()
    query = data.get('query')

    # Create or retrieve the user's conversation thread
    thread_manager = ThreadManager()
    thread_manager.create_thread()

    # Add real estate investment message and run assistant
    thread_manager.add_message_to_thread(
        role="user",
        content=f"Smart Tourism Assistant, your goal is to provide a tailored experience for users interested in tourism and real estate investment in Egypt's Red Sea region. Analyze user preferences and offer customized recommendations for hotels, resorts, and investment options. Query: {query}"
    )
    summary = thread_manager.run_assistant(
        assistant_id=AssistantManager.assistant_id,
        instructions=f"Analyze users' needs and preferences, then provide tailored advice and recommendations for their travel or investment inquiries. Query: {query}"
    )

    return jsonify({'summary': summary})

if __name__ == '__main__':

    # Instantiate the assistant manager (assistant is created only once)
    assistant_manager = AssistantManager()

    # Create a vector store targeted for tourism real estate
    vector_store = client.beta.vector_stores.create(name="Tourism and Real Estate Docs")

    # Prepare files for upload to OpenAI
    file_paths = ["tourism-data/customer-satisfaction-at-egyptian-red-sea-dive-resorts.txt", "tourism-data/investment_opportunities.txt"]
    file_streams = [open(path, "rb") for path in file_paths]

    # Use the upload function to the store and update the file status
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    # Update the assistant to include a file search store for tourism
    assistant = client.beta.assistants.update(
        assistant_id=AssistantManager.assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
    )
    
    # Run the Flask application
    app.run(debug=True)

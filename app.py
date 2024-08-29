from flask import Flask, jsonify, request
import scrape_url
import scrape_pdf
import chat

app = Flask(__name__)


@app.route("/preguntar_chatbot", methods=["POST"]) # pyright: ignore
def askChatbot():
    """Endpoint to ask a question to the chatbot."""
    json_content = request.json
    question = json_content.get("question") # pyright: ignore

    response = chat.answer_question_with_context(question)

    return response


@app.route("/obtener_info_from_url", methods=["POST"])
def scrapeUrl():
    """Endpoint to scrape an article from a URL."""
    json_content = request.json
    url = json_content.get("url") # pyright: ignore

    messages = scrape_url.fetch_and_persist_article(url)

    return jsonify({"url": url, "messages": messages}), 200


@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    """Endpoint to upload and save PDF files."""
    if 'file' not in request.files:
        return jsonify({"error": "No se ha seleccionado un archivo"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No se ha seleccionado un archivo"}), 400

    if not scrape_pdf.allowed_file(file.filename):
        return jsonify({"error": "Tipo de archivo no permitido, solo PDFs son permitidos"}), 400

    file_path, error = scrape_pdf.save_file(file)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": f"Arhivo {file.filename} subido correctamente", "file_path": file_path}), 200


@app.route("/load_documents", methods=["POST"])
def load_documents_endpoint():
    """Endpoint to load documents from the PDF files."""
    documents = scrape_pdf.load_documents()
    chunks = scrape_pdf.split_documents(documents)
    scrape_pdf.add_to_chroma(chunks)
    return jsonify({"message": "Documents loaded and added to Chroma"}), 200


@app.route("/reset_database", methods=["POST"])
def reset_database():
    """Endpoint to reset the Chroma database."""
    scrape_pdf.clear_database()
    return jsonify({"message": "Database cleared successfully"}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

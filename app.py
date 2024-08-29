from flask import Flask, jsonify, request
import scrape_url
import scrape_pdf
import chat

app = Flask(__name__)


@app.route("/obtener_info_from_url", methods=["POST"])
def scrapeUrl():
    json_content = request.json
    url = json_content.get("url") # pyright: ignore

    messages = scrape_url.fetch_and_persist_article(url)

    return {"url": url, "messages": messages}


@app.route("/preguntar_chatbot", methods=["POST"]) # pyright: ignore
def askChatbot():
    json_content = request.json
    question = json_content.get("question") # pyright: ignore

    response = chat.answer_question_with_context(question)

    return response

@app.route("/reset_database", methods=["POST"])
def reset_database():
    scrape_pdf.clear_database()
    return jsonify({"message": "Database cleared successfully"}), 200


@app.route("/load_documents", methods=["POST"])
def load_documents_endpoint():
    documents = scrape_pdf.load_documents()
    chunks = scrape_pdf.split_documents(documents)
    scrape_pdf.add_to_chroma(chunks)
    return jsonify({"message": "Documents loaded and added to Chroma"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

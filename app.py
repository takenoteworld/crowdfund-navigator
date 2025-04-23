from flask import Flask, send_file
import requests
import io

app = Flask(__name__)

# 🔐 Your real Pdfless API Key
import os
API_KEY = os.environ.get("PDFLESS_API_KEY")


# 📄 Your Pdfless template ID
TEMPLATE_ID = 'cdf49ddf-47b6-46c0-b600-26e054107683'

@app.route('/generate-pdf', methods=['GET'])
def generate_pdf():
    payload = {
        "template_id": TEMPLATE_ID,
        "payload": {
            "Company": "Visionary Tech Co.",
            "Founder": "Kimberly Tomczyk",
            "RaiseTarget": "$40 Million",
            "BusinessModel": "Crowdfunding AI-as-a-Service Platform"
        }
    }

    response = requests.post(
        "https://api.pdfless.com/v1/pdfs",
        headers={
            "apikey": API_KEY,
            "Content-Type": "application/json"
        },
        json=payload
    )

    if response.status_code == 200:
        download_url = response.json()["data"]["download_url"]
        pdf_response = requests.get(download_url)

        return send_file(
            io.BytesIO(pdf_response.content),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="crowdfund_navigator_output.pdf"
        )

    return f"Error: {response.status_code} - {response.text}", 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)




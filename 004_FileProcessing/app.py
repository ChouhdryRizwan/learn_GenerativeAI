import os
import pathlib
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = "gemini-2.5-flash" 

def summarize_file(file_path: str, custom_prompt: str = None) -> str:
    """
    Summarize any supported file: image, pdf, docx, xlsx, txt
    """
    file_path = pathlib.Path(file_path)
    if not file_path.exists():
        return "Error: File not found!"

    # Auto-detect MIME type
    mime_type = {
        '.pdf' : 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.txt' : 'text/plain',
        '.jpg' : 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png' : 'image/png',
        '.webp': 'image/webp',
        '.bmp' : 'image/bmp',
    }.get(file_path.suffix.lower())

    if not mime_type:
        return f"Unsupported file type: {file_path.suffix}"

    # Upload file (Gemini handles it automatically)
    print(f"Uploading {file_path.name}...")
    uploaded_file = genai.upload_file(path=file_path, mime_type=mime_type)

    # Default smart prompt
    if custom_prompt is None:
        prompt = {
            'image': "Describe this image in detail and summarize its key content, charts, text, or diagrams.",
            'application/pdf': "Summarize this entire PDF document concisely. Include main topics, conclusions, and key data points.",
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 
                "Summarize this Word document. Extract headings, key paragraphs, and main conclusions.",
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                "Analyze this Excel file. Summarize each sheet, key metrics, trends, totals, and important insights.",
            'text/plain': "Summarize this text file in 3-5 bullet points."
        }.get(mime_type, "Summarize this file.")

    else:
        prompt = custom_prompt

    # Generate summary
    model = genai.GenerativeModel(MODEL_NAME)
    print("Generating summary...")
    response = model.generate_content(
        [uploaded_file, prompt],
        generation_config={
            "temperature": 0.4,
            "top_p": 0.95,
            "max_output_tokens": 2048,
        }
    )

    # Clean up uploaded file (optional, auto-expires in 48h)
    # genai.delete_file(uploaded_file.name)

    return response.text

# ================ USAGE EXAMPLE ================
if __name__ == "__main__":
    # Put your files in the same folder or give full path
    files_to_summarize = ["sample_pdf.pdf"]

    for file in files_to_summarize:
        if os.path.exists(file):
            print(f"\n{'='*60}")
            print(f"SUMMARIZING: {file}")
            print(f"{'='*60}")
            summary = summarize_file(file)
            print(summary)
        else:
            print(f"File not found: {file}")
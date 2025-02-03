# pdf.py
import os
from flask import Blueprint, jsonify, send_from_directory

pdf_blueprint = Blueprint("pdf", __name__)

PDF_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs')

def ensure_pdf_folder():
    if not os.path.exists(PDF_FOLDER):
        os.makedirs(PDF_FOLDER)
        print(f"Folder '{PDF_FOLDER}' created.")

def list_pdfs_recursive(root):
    items = []
    try:
        for entry in os.listdir(root):
            path = os.path.join(root, entry)
            if os.path.isdir(path):
                children = list_pdfs_recursive(path)
                items.append({
                    "name": entry,
                    "type": "folder",
                    "path": os.path.relpath(path, PDF_FOLDER).replace('\\', '/'),
                    "children": children
                })
            elif entry.lower().endswith('.pdf'):
                items.append({
                    "name": entry,
                    "type": "file",
                    "path": os.path.relpath(path, PDF_FOLDER).replace('\\', '/')
                })
    except Exception as e:
        print(f"Error listing PDFs in {root}: {e}")
    return items

@pdf_blueprint.route("/api/pdfs_list")
def api_pdfs_list():
    ensure_pdf_folder()
    tree = list_pdfs_recursive(PDF_FOLDER)
    return jsonify(tree)

@pdf_blueprint.route("/pdf_file/<path:filename>")
def serve_pdf_file(filename):
    ensure_pdf_folder()
    filename = filename.replace('\\', '/').strip('/')
    print(f"Requested PDF: {filename}")
    print(f"Full path: {os.path.join(PDF_FOLDER, filename)}")
    try:
        return send_from_directory(PDF_FOLDER, filename)
    except Exception as e:
        print(f"Error serving PDF: {str(e)}")
        return str(e), 404
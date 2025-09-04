import tempfile
import os
from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf_from_buffer(file_buffer: bytes):
    """
    Save a PDF bytes buffer to a temporary file and load it.
    This works with all loaders expecting file paths.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file_buffer)
        tmp_file.flush()
        tmp_path = tmp_file.name

    loader = PyMuPDFLoader(tmp_path)
    docs = loader.load()

    # Clean up the temp file
    os.remove(tmp_path)

    return docs

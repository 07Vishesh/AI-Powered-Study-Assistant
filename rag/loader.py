import os
import tempfile
import fitz
import docx2txt
from llama_index.core import Document
class MultiDocumentLoader:
    """Loads multiple PDF, DOCX and TXT filesand converts them into LlamaIndex Documents."""
    SUPPORTED_EXTENSIONS = {"pdf", "docx", "txt"}
    def __init__(self):
        self.documents = []
    def load_documents(self, uploaded_files):
        """
        Parameters
        ----------
        uploaded_files : list
            Streamlit UploadedFile objects
        Returns
        -------
        list[Document]
        """
        self.documents = []
        if not uploaded_files:
            return self.documents
        for uploaded_file in uploaded_files:
            filename = uploaded_file.name
            extension = filename.split(".")[-1].lower()
            if extension not in self.SUPPORTED_EXTENSIONS:
                print(f"Skipping unsupported file: {filename}")
                continue
            file_bytes = uploaded_file.read()
            if extension == "pdf":
                self._load_pdf(filename, file_bytes)
            elif extension == "docx":
                self._load_docx(filename, file_bytes)
            elif extension == "txt":
                self._load_txt(filename, file_bytes)
        return self.documents
    # PDF
    def _load_pdf(self, filename, file_bytes):
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        for page_number in range(len(pdf)):
            page = pdf.load_page(page_number)
            text = page.get_text().strip()
            if text:
                self.documents.append(
                    Document(
                        text=text,
                        metadata={
                            "file_name": filename,
                            "page": page_number + 1,
                            "file_type": "pdf",
                        },
                    )
                )
        pdf.close()
    # DOCX
    def _load_docx(self, filename, file_bytes):
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".docx"
        ) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name
        try:
            text = docx2txt.process(temp_path)
            if text.strip():
                self.documents.append(
                    Document(
                        text=text,
                        metadata={
                            "file_name": filename,
                            "page": None,
                            "file_type": "docx",
                        },
                    )
                )
        finally:
            os.remove(temp_path)
    # TXT
    def _load_txt(self, filename, file_bytes):
        text = file_bytes.decode(
            "utf-8",
            errors="ignore",
        )
        if text.strip():
            self.documents.append(
                Document(
                    text=text,
                    metadata={
                        "file_name": filename,
                        "page": None,
                        "file_type": "txt",
                    },
                )
            )
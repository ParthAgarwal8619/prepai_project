import os
import io
import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF.
    - Text-based PDFs: direct extraction via PyMuPDF
    - Scanned PDFs: attempts OCR if tesseract is available, else skips gracefully
    """
    full_text = []

    try:
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc):
            text = page.get_text("text").strip()

            if text and len(text) > 50:
                # Normal text-based page
                full_text.append(text)
            else:
                # Scanned page - try OCR
                print(f"[PDF] Page {page_num + 1} is scanned → attempting OCR")
                ocr_text = try_ocr(page)
                if ocr_text:
                    full_text.append(ocr_text)
                else:
                    print(f"[PDF] Page {page_num + 1} skipped (OCR unavailable)")

        doc.close()
    except Exception as e:
        print(f"[PDF] Error reading {file_path}: {e}")

    return "\n\n".join(full_text)


def try_ocr(page) -> str:
    """Try OCR on a page. Returns empty string if tesseract not available."""
    try:
        import pytesseract
        from PIL import Image

        # Check tesseract path from env
        tesseract_path = os.getenv("TESSERACT_PATH", "")
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

        # Render page to image
        mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better OCR
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))

        text = pytesseract.image_to_string(img, lang="eng")
        return text.strip()

    except ImportError:
        return ""
    except Exception as e:
        # tesseract not installed or PATH issue - silently skip
        return ""

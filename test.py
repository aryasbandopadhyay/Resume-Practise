from pdfminer.high_level import extract_text

k=(repr(extract_text('./uploads/MyCV.pdf')))

print(k.split('\\n'))
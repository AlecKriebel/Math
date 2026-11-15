#!/usr/bin/env python3
"""Read acquired PDF bodies with the existing official PDF dependency only.

Creates local text derivatives, not scientific computations or source changes.
Text extraction is not a claim of personally reading every extracted page.
"""
from pathlib import Path
import hashlib
import json
from pypdf import PdfReader

OWN = Path(__file__).resolve().parent
OUTPUT = OWN / 'primary-derived'
PDFS = {
    'gaboriau-2002': 'primary/gaboriau-2002.pdf',
    'openai-pinned': 'primary/openai-pinned.pdf',
    'gaboriau-2000': 'primary/extra-v3/gaboriau-2000-author.hop0.body',
    'faq': 'primary/extra-v2/gaboriau-faq.hop0.body',
    'notes': 'primary/extra-v2/gaboriau-notes.hop0.body',
    'psv-v1': 'primary/extra-v3/psv-v1-pdf.hop0.body',
    'lueck-v1': 'primary/extra-v3/lueck-v1-pdf.hop0.body',
    'hatcher': 'primary/extra-v2/hatcher-author.hop0.body',
}

def main():
    OUTPUT.mkdir()
    receipt = []
    for role, relative in PDFS.items():
        path = OWN / relative
        reader = PdfReader(path)
        pages = []
        for index, page in enumerate(reader.pages):
            # Hatcher's required interface pages are known from the actual web body.
            if role == 'hatcher' and index not in list(range(98, 105)) + [354, 355, 374, 375, 376]:
                continue
            pages.append({'PDF_page_one_based': index + 1, 'text': page.extract_text()})
        out = OUTPUT / (role + '.json')
        with out.open('x') as f:
            json.dump(pages, f, ensure_ascii=False, indent=2)
            f.write('\n')
        body = out.read_bytes()
        receipt.append({'role': role, 'raw_body': relative, 'total_PDF_pages': len(reader.pages), 'extracted_page_numbers': [p['PDF_page_one_based'] for p in pages], 'text_derivative': str(out), 'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(), 'all_extracted_pages_personally_read_claimed': False})
    with (OUTPUT / 'DERIVATION_RECEIPT.json').open('x') as f:
        json.dump(receipt, f, indent=2)
        f.write('\n')
    print(json.dumps([{'role': r['role'], 'PDF_pages': r['total_PDF_pages'], 'extracted': len(r['extracted_page_numbers'])} for r in receipt], indent=2))

if __name__ == '__main__':
    main()

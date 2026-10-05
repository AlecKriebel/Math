import html, pathlib, re
root=pathlib.Path(__file__).resolve().parent
data=(root/'process_evidence'/'metadata_das2014_author'/'stdout.bin').read_text()
for m in re.finditer(r'.{0,150}(?:022319|arxiv\.org/abs/|arxiv\.org/pdf/).{0,180}', data):
    print(html.unescape(m.group()))

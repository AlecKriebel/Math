import pathlib, json, re, html
root=pathlib.Path(__file__).resolve().parent
for label in ['download_yuan2011_springer','metadata_measurements2026']:
    data=(root/'process_evidence'/label/'stdout.bin').read_bytes()
    print(label, 'bytes',len(data),'magic',repr(data[:16]))
    if data[:5]!=b'%PDF-':
        t=data.decode(errors='replace')
        for key in ['citation_title','citation_pdf_url','citation_publication_date','citation_doi']:
            for m in re.finditer(r'<meta[^>]*name="'+key+r'"[^>]*content="([^"]*)"',t):
                print(key,html.unescape(m.group(1)))
        if label=='metadata_measurements2026':
            m=re.search(r'<div class="submission-history">(.*?)</div>',t,re.S)
            if m: print(html.unescape(re.sub(r'<[^>]+>',' ',m.group(1))))
print('successful downloadable PDF inputs', len([p for p in (root/'process_evidence').glob('download_*/stdout.bin') if p.read_bytes()[:5]==b'%PDF-']))
print('copied authenticated PDF inputs',len(list((root/'private'/'primary').glob('*.pdf'))))
for p in sorted((root/'process_evidence').glob('*/result.json')):
    d=json.loads(p.read_text())
    if d['exit_code']:
        print('NONZERO', p.parent.name, d['exit_code'],d['stdout']['bytes'])

import html, pathlib, re
root=pathlib.Path(__file__).resolve().parent
labels=['metadata_original2004','metadata_companion2005','metadata_piani','metadata_preprocess','metadata_deterministic','metadata_routing','metadata_das2014','metadata_situ2011','metadata_winter1998']
for label in labels:
    data=(root/'process_evidence'/label/'stdout.bin').read_text()
    print(label)
    match=re.search(r'<div class="submission-history">(.*?)</div>',data,re.S)
    if match:
        print(html.unescape(re.sub(r'<[^>]+>',' ',match.group(1))))
    for key in ['citation_title','citation_arxiv_id','citation_date','citation_doi']:
        for m in re.finditer(r'<meta name="'+key+r'" content="([^"]*)"',data):
            print(key,html.unescape(m.group(1)))

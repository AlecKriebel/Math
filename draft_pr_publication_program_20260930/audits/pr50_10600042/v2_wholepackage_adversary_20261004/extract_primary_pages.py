import json, pathlib
root=pathlib.Path(__file__).resolve().parent
cases={'kamada': (4,5,6,7), 'gks': (4,5), 'kl': (30,), 'survey_publisher_correct': (29,)}
for name,pages in cases.items():
    text=(root/'private/primary'/f'{name}.txt').read_text()
    split=text.split('\f')
    for page in pages:
        body=split[page-1]
        (root/'private/primary'/f'{name}_page_{page}.txt').write_text(body)
        print(f'=== {name}, PDF page {page} ===\n{body}')
manifest={'page_selection':cases,'note':'PDF pages are one-based; source printed folios checked visually where relevant.'}
(root/'PRIMARY_PAGE_SELECTION.json').write_text(json.dumps(manifest,indent=2)+'\n')

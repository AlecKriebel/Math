#!/usr/bin/env python3
"""Measure the four material journal overflow witnesses in shipped PDFs."""
import json,re,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'source_snapshot'

def word_pages(pdf):
    raw=subprocess.check_output(['pdftotext','-bbox',str(pdf),'-']).decode()
    raw=re.sub('[\x00-\x08\x0b\x0c\x0e-\x1f]','',raw)
    tree=ET.fromstring(raw)
    pages=[]
    for page in tree.iter():
        if not page.tag.endswith('}page'):continue
        words=[dict(text=w.text or '',**{k:float(v) for k,v in w.attrib.items()}) for w in page.iter() if w.tag.endswith('}word')]
        pages.append(words)
    return pages

main=word_pages(SOURCE/'submission/journal/manuscript.pdf')
supp=word_pages(SOURCE/'submission/journal/supplement.pdf')
results=[]
def record(name,pdf,page,words):
    assert words,name
    xmin=min(w['xMin'] for w in words);xmax=max(w['xMax'] for w in words)
    assert xmin>=90 and xmax<=522,(name,xmin,xmax)
    results.append(dict(name=name,pdf=pdf,page=page,left_text_bound=90,right_text_bound=522,xMin=xmin,xMax=xmax,words=words,inside_text_area=True))
for name,pages,pdf in [('main command',main,'submission/journal/manuscript.pdf'),('supplement command',supp,'submission/journal/supplement.pdf')]:
    matches=[]
    for i,page in enumerate(pages,1):
        words=[w for w in page if 'independent_verifier/' in w['text'] or 'verify_symbolic_certificates.py' in w['text']]
        if words:matches.append((i,words))
    assert len(matches)==1,(name,matches)
    record(name,pdf,*matches[0])
values={'2.80855','2.70635','2.67689','2.66288','2.65469','2.64932','2.64553','2.6427'}
for i,page in enumerate(main,1):
    words=[w for w in page if w['text'] in values]
    if len(words)==8:
        record('contrast table final-column values','submission/journal/manuscript.pdf',i,words);break
else:raise AssertionError('missing contrast table values')
for i,page in enumerate(supp,1):
    section_starts=[w['yMin'] for w in page if w['text']=='Reference']
    if not section_starts:continue
    anchors=[w for w in page if '286118780220' in w['text'] and w['yMin']>min(section_starts)]
    if anchors and i>=14:
        y=min(w['yMin'] for w in anchors)
        words=[w for w in page if abs(w['yMin']-y)<12 and w['xMin']>=90]
        record('reference coefficient rational display','submission/journal/supplement.pdf',i,words);break
else:raise AssertionError('missing rational identity')
(HERE/'JOURNAL_REPAIR_COORDINATES.json').write_text(json.dumps(results,indent=2)+'\n')
for r in results:print(r['name'],r['page'],r['xMin'],r['xMax'])
print('FOUR_MATERIAL_JOURNAL_OVERFLOWS_REPAIRED')

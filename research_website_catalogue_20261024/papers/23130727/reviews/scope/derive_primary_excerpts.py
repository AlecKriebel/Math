#!/usr/bin/env python3
"""Explicit scoped document derivatives of pinned existing PDFs; default inert.
No network, native programme, project import or scientific checker execution.
"""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

A = Path(__file__).resolve().parent

def pin(p):
    b = p.read_bytes()
    return {'path':str(p),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def main():
    if sys.argv[1:] != ['--derive']:
        print('Inert default; explicit --derive creates bounded document excerpts.')
        return
    handoff = json.loads((A/'RAW_PRIMARY_HANDOFF_01.json').read_bytes())
    bodies = {}
    for row in handoff['records']:
        original = row['whole_original_raw_body']
        p = Path(original['path'])
        if pin(p) != original:
            raise ValueError('raw body changed')
        bodies[row['label']] = p
    D = A/'primary-excerpts'
    D.mkdir(exist_ok=False)
    receipts = []
    def run(label, argv, outputs):
        start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        r = subprocess.run(argv,capture_output=True)
        so,se=D/(label+'.stdout'),D/(label+'.stderr')
        so.write_bytes(r.stdout);se.write_bytes(r.stderr)
        receipts.append({'started_UTC':start,'completed_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'argv':argv,'exit':r.returncode,'stdout':pin(so),'stderr':pin(se),'outputs':[pin(p) for p in outputs if p.exists()]})
        (D/'RECEIPTS.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
        if r.returncode:
            raise RuntimeError('document derivative failed; exact first streams retained')
    ranges = {'Fine-Wilf1965':[(1,2)],'Bischoff-DIP3095':[(1,1),(21,28)],
              'CKS-journal2010':[(1,2),(6,8),(11,11),(13,13)],
              'Kari-Seki-author':[(1,1)],'Simpson-published2025':[(1,1),(9,11)],
              'OWR37-2010-publisher-report':[(25,28)]}
    for label, source in bodies.items():
        run(label+'-pdfinfo',['pdfinfo',str(source)],[])
        for first,last in ranges[label]:
            name=label+'-'+str(first)+'-'+str(last)
            out=D/(name+'.txt')
            run(name,['pdftotext','-layout','-f',str(first),'-l',str(last),str(source),str(out)],[out])
    images = [('Fine-Wilf1965',1),('OWR37-2010-publisher-report',26),('Bischoff-DIP3095',27),
              ('CKS-journal2010',8),('Simpson-published2025',10),
              ('Kari-Seki-author',3),('Kari-Seki-author',9),('Kari-Seki-author',18),('Kari-Seki-author',19)]
    for label,page in images:
        name=label+'-page'+str(page)
        out=D/name
        run(name,['pdftoppm','-f',str(page),'-l',str(page),'-r','120','-png','-singlefile',str(bodies[label]),str(out)],[out.with_suffix('.png')])
    print(json.dumps({'scoped_document_derivatives':True,'raw_bodies_reused_byreference':6,'fresh_GETs':0,
                      'fresh_own_critical_rasters':len(images),'scientific_programmes_executed':[]}))

if __name__ == '__main__':
    main()

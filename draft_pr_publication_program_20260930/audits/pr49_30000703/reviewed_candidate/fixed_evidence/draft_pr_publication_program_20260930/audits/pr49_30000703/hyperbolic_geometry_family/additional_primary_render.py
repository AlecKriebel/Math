#!/usr/bin/python3
import hashlib,json,pathlib,subprocess
out=pathlib.Path(__file__).parent
meta=json.loads((out/'PRIMARY_IDENTITIES.json').read_text())
row=next(r for r in meta['documents'] if r['name']=='hyperbolic_v1')
p=pathlib.Path(row['temporary_pdf']);rows=[]
for page in [4,5,6,40]:
    prefix=p.parent/('hyperbolic_v1_page_%02d'%page)
    c=subprocess.run(['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1800','-png','-singlefile',str(p),str(prefix)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if c.returncode:raise RuntimeError('render exit '+str(c.returncode))
    q=prefix.with_suffix('.png');b=q.read_bytes()
    rows.append({'one_based_pdf_page':page,'temporary_png':str(q),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(out/'ADDITIONAL_PRIMARY_IDENTITIES.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows))

#!/usr/bin/python3
"""Fetch primary documents transiently; retain identities, not foreign bodies."""
import datetime,hashlib,json,pathlib,subprocess,tempfile,urllib.request

specs=[('owr','https://ems.press/content/serial-article-files/46093',[42,43,44]),('hyperbolic_v1','https://arxiv.org/pdf/2410.13965v1',[1,2,3,31,32])]
out=pathlib.Path(__file__).parent
temp=pathlib.Path(tempfile.mkdtemp(prefix='pr49_hyperbolic_primary_'))
rows=[]
for name,url,pages in specs:
    with urllib.request.urlopen(url,timeout=40) as r:
        b=r.read();resolved=r.geturl();ctype=r.headers.get('Content-Type')
    p=temp/(name+'.pdf');p.write_bytes(b)
    row={'name':name,'url':url,'resolved_url':resolved,'content_type':ctype,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'temporary_pdf':str(p),'rendered_pages':[]}
    for page in pages:
        prefix=temp/('%s_page_%02d'%(name,page))
        c=subprocess.run(['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1800','-png','-singlefile',str(p),str(prefix)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if c.returncode: raise RuntimeError('Render failed: '+str(c.returncode))
        q=prefix.with_suffix('.png');bb=q.read_bytes()
        row['rendered_pages'].append({'one_based_pdf_page':page,'temporary_png':str(q),'bytes':len(bb),'sha256':hashlib.sha256(bb).hexdigest()})
    rows.append(row)
meta={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'temporary_directory':str(temp),'documents':rows,'retention_policy':'All foreign PDF and rendered image files deleted after personal reading; only identities and first-party derivations remain','personally_inspected_yet':False}
(out/'PRIMARY_IDENTITIES.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta))

#!/usr/bin/env python3
"""Reproduce byte-level public provenance without printing source contents."""
import argparse
import hashlib
import json
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--problems',type=Path,required=True)
parser.add_argument('--research',type=Path,required=True)
parser.add_argument('--catalog',type=Path,required=True)
parser.add_argument('--pdf-directory',type=Path,required=True)
args=parser.parse_args()
digest=lambda b:hashlib.sha256(b).hexdigest()
datasets={
    'problems.json':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
    'research_results.json':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')}
out={'status':'PASS','scope':'Complete supplied local public-source bytes checked; no fresh corpus download claimed.','datasets':{}}
for label,path in [('problems.json',args.problems),('research_results.json',args.research)]:
    b=path.read_bytes(); expected=datasets[label]
    assert (len(b),digest(b))==expected,label
    out['datasets'][label]={'bytes':len(b),'sha256':digest(b),'match':True}
records=json.loads(args.problems.read_bytes()); reports=json.loads(args.research.read_bytes())
numeric=[i for i,p in enumerate(records) if p.get('id')==20000276]
named=[i for i,p in enumerate(records) if p.get('problem_number')=='AIM-ALGEBRAIC_GEOMETRY-0276']
assert numeric==named==[5701]
p=records[numeric[0]];r=reports['AIM-ALGEBRAIC_GEOMETRY-0276']
statement=digest(p['statement'].encode())
review=digest(json.dumps([p,r],sort_keys=True).encode())
assert statement=='bcb76be9e84178d52dfac4ba10d1cf997dd588abc92e3cc124567fe8f863cd8d'
assert review=='6151a5cbb38fe289d9efc5d7da329ece470d84357c0de64e45654019ed2fd155'
cat=args.catalog.read_bytes(); target=[p for p in json.loads(cat) if str(p.get('id'))=='20000276']
assert len(target)==1
assert target[0]['rank']==757
assert target[0]['statement_hash']==statement and target[0]['review_hash']==review
out['target']={'id':20000276,'problem_code':'AIM-ALGEBRAIC_GEOMETRY-0276','unique_problem_index':5701,
               'separate_report_present':True,'statement_sha256':statement,'review_sha256':review,
               'review_hash_recipe':'UTF-8 of Python json.dumps([problem_record, research_record], sort_keys=True); other options default.',
               'catalog_unique_match':True,'rank':757}
out['catalog']={'bytes':len(cat),'sha256':digest(cat),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(cat)).encode()+b'\0'+cat).hexdigest()}
pdfs=[
 ('bms.pdf','Discreteness and rationality of F-thresholds','https://arxiv.org/abs/math/0607660v2',286972,'728151b3fcbc88f872cbd960b1338a524faa0a1c59b19f2549c5e57d18d0acbe'),
 ('koley_kumar.pdf','F-thresholds of filtrations of ideals','https://arxiv.org/abs/2312.07761v1',375113,'293f67b998509e7ff128ad3729986902ac87bf9d213b521819601bac71cfe900'),
 ('dsn.pdf','F-thresholds of graded rings','https://doi.org/10.1017/nmj.2016.65',583779,'334c196fd52d861fb99c5cfd94c2f7894c74523f2840b585441c802f93a18a71'),
 ('badilla_cespedes.pdf','On F-thresholds of differential power filtrations','https://arxiv.org/abs/2607.09028v1',408236,'bea01ab9e8fcfec93903b1c5f1cc2cdf99d0c4716b86db35ee8865a287b3d572')]
out['pdfs']=[]
for filename,title,url,size,sha in pdfs:
    b=(args.pdf_directory/filename).read_bytes()
    assert b.startswith(b'%PDF-')
    assert (len(b),digest(b))==(size,sha),filename
    out['pdfs'].append({'title':title,'url':url,'bytes':len(b),'sha256':digest(b),'match':True})
print(json.dumps(out,indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Read separately held sources; print only identity verification metadata."""
import argparse,hashlib,json
from pathlib import Path

def check(ok,what):
    if not ok: raise RuntimeError(what)

def main():
    p=argparse.ArgumentParser()
    for name in ['problems','research-results','primary-pdf','extension-pdf']:
        p.add_argument('--'+name,required=True,type=Path)
    a=p.parse_args()
    specs=[('problems',a.problems,68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
    ('research_results',a.research_results,80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
    ('primary_pdf',a.primary_pdf,1151433,'e0dbfa6ad56d14971d4f901dc8568731e22359feeb1efb429b240f156b88d29e'),
    ('extension_pdf',a.extension_pdf,858073,'a3005e8a47eb33697d6c3e59dc46630e98f2ad1b6013f64c0495e7b525d7bc4a')]
    out={}; parsed={}
    for name,path,size,sha in specs:
        b=path.read_bytes();check(len(b)==size and hashlib.sha256(b).hexdigest()==sha,name+' identity mismatch')
        if name.endswith('_pdf'):check(b.startswith(b'%PDF-'),name+' is not PDF')
        else:parsed[name]=json.loads(b)
        out[name]={'bytes':size,'sha256':sha,'match':True}
    target=[r for r in parsed['problems'] if str(r.get('id'))=='5300014']
    check(len(target)==1,'unique numeric identity');r=target[0]
    check(r['problem_number']=='AMR-052-0014','target code')
    review=parsed['research_results'][r['problem_number']]
    statement=hashlib.sha256(r['statement'].encode()).hexdigest()
    joined=hashlib.sha256(json.dumps([r,review],sort_keys=True).encode()).hexdigest()
    check(statement=='605796659aee2713aa353da0765ccfa7d55ab8e33ede87910ea9e4a9812a2d52','statement hash')
    check(joined=='af0145f5497fd2fb898e1bf4adcb814e2d197dec6cfa425569248011eccc7aee','joined review hash')
    out['target']={'numeric_id':5300014,'code':'AMR-052-0014','statement_hash':statement,'review_hash':joined,'all_matches':True}
    out['identity_does_not_certify_math']=True
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()

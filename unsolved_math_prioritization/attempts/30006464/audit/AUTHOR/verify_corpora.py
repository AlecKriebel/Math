#!/usr/bin/env python3
"""Optional full-corpus identity replay. Paths are supplied by the operator."""
import hashlib,json,pathlib,stat,sys
ROOT=pathlib.Path(__file__).resolve().parent
EXPECTED=[(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')]
def need(v,m):
    if not v:raise ValueError(m)
def main():
    need(len(sys.argv)==4,'supply catalog, problems, research-results corpus paths')
    data=[]
    for x,(size,h) in zip(sys.argv[1:],EXPECTED):
        p=pathlib.Path(x);need(stat.S_ISREG(p.lstat().st_mode),'nonregular input');b=p.read_bytes();need(len(b)==size and hashlib.sha256(b).hexdigest()==h,'corpus identity');data.append(json.loads(b))
    cat,problems,reports=data;cs=[r for r in cat if str(r['id'])=='30006464'];ps=[r for r in problems if r['id']==30006464];need(len(cs)==len(ps)==1,'unique target');c,p=cs[0],ps[0]
    need(c['rank']==831 and p['problem_number']==c['problem_number']=='OWR-14299577-017','target/rank')
    need(p['problem_number'] not in reports,'missing report representation')
    s=hashlib.sha256(p['statement'].encode()).hexdigest();b=json.dumps([p,reports.get(p['problem_number'],{})],sort_keys=True).encode();r=hashlib.sha256(b).hexdigest()
    need(s==c['statement_hash']=='3fd58aab3ddd149d21db6223b60f498cdc98c006ae67bf89495dc0e180f9605e','statement match');need(len(b)==4313 and r==c['review_hash']=='73ff2584746c1f75184a94669e67aea3ff3000e90e8c2b54cb6bac17cb33a395','review match')
    print(json.dumps({'status':'pass','problem_id':30006464,'corpora_matched':3,'complete_review_match':True,'statement_match':True,'review_bytes':4313},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:raise SystemExit('FAIL: '+str(e))

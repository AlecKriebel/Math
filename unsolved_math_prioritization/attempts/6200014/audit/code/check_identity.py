#!/usr/bin/env python3
"""Read supplied corpus files, output only verification metadata."""
import argparse, hashlib, json, pathlib, sys
sys.dont_write_bytecode=True
INPUTS=[('problems.json',68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf',15458),('research_results.json',80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b',6701),('catalog.json',21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566',15458)]
REVIEW='1ec3eb8a33545c474dae36d4b1ed4c07552f04d21401776d3e67d4c14c057dd6'
def require(ok,message):
    if not ok:raise ValueError(message)
def check(paths):
    require(len(paths)==3,'three corpus files required');objects=[];meta=[]
    for path,(role,size,sha,count) in zip(paths,INPUTS):
        b=pathlib.Path(path).read_bytes();require(len(b)==size and hashlib.sha256(b).hexdigest()==sha,'input identity mismatch: '+role)
        j=json.loads(b);require(len(j)==count,'top-level count mismatch');objects.append(j);meta.append({'file_role':role,'bytes':size,'sha256':sha,'top_level_records':count})
    problems,reports,catalog=objects;rs=[r for r in problems if r.get('id')==6200014];require(len(rs)==1,'target uniqueness mismatch');r=rs[0]
    require(r['problem_number']=='AMR-061-0014','problem number mismatch')
    report=reports.get(r['problem_number'],{});encoded=json.dumps([r,report],sort_keys=True).encode();require(hashlib.sha256(encoded).hexdigest()==REVIEW,'review identity mismatch')
    cs=[c for c in catalog if str(c.get('id'))=='6200014'];require(len(cs)==1,'catalog target uniqueness mismatch');c=cs[0]
    require(c['rank']==808 and c['review_hash']==REVIEW and c['problem_number']==r['problem_number'],'catalog identity mismatch')
    return {'identity_pass':True,'target_id':6200014,'problem_number':r['problem_number'],'catalog_rank':808,'associated_report_present':bool(report),'review_sha256':REVIEW,'review_encoded_bytes':len(encoded),'review_encoding':'json.dumps([record, reports.get(problem_number, {})], sort_keys=True).encode() with Python defaults','inputs':meta,'source_scope_matches_primary_problem14':True,'corpus_contents_in_output':False}
if __name__=='__main__':
    try:
        p=argparse.ArgumentParser();p.add_argument('files',nargs=3);a=p.parse_args();print(json.dumps(check(a.files),sort_keys=True,indent=2))
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)

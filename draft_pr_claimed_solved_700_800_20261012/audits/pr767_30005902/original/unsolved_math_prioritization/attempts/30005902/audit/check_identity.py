#!/usr/bin/env python3
"""Rehash full externally supplied corpora; print only public identity metadata."""
import argparse,copy,hashlib,json,re
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--catalog',required=True);ap.add_argument('--problems',required=True);ap.add_argument('--research-results',required=True)
    ap.add_argument('--author-identity',required=True);ap.add_argument('--repository-manifest',required=True);ap.add_argument('--queue-source',required=True)
    a=ap.parse_args();expected=json.loads(Path(a.author_identity).read_bytes())
    docs={};meta={}
    for name,path in [('catalog.json',a.catalog),('problems.json',a.problems),('research_results.json',a.research_results)]:
        b=Path(path).read_bytes();docs[name]=json.loads(b);meta[name]={'bytes':len(b),'sha256':sha(b),'records':len(docs[name])}
        if name=='catalog.json':meta[name]['git_blob_sha1']=blob(b)
        assert meta[name]==expected['complete_cached_inputs_rehashed'][name],name
    manifest_response=json.loads(Path(a.repository_manifest).read_bytes());manifest=json.loads(manifest_response['structuredContent']['content'])
    for n in ('problems.json','research_results.json'):
        assert manifest['files'][n]=={k:meta[n][k] for k in ('bytes','sha256')}
    cat=[r for r in docs['catalog.json'] if str(r['id'])=='30005902']
    ps=[r for r in docs['problems.json'] if str(r['id'])=='30005902']
    assert len(cat)==len(ps)==1;c,p=cat[0],ps[0]
    assert c['rank']==802 and p['problem_number']==c['problem_number']=='OWR-14298370-002'
    assert sum(r['problem_number']==p['problem_number'] for r in docs['problems.json'])==1
    rr=docs['research_results.json'];assert p['problem_number'] not in rr
    q=json.loads(Path(a.queue_source).read_bytes())['structuredContent']
    qb=q['content'].encode();assert blob(qb)==q['sha']==expected['queue_py_git_blob_sha1']
    # Inspect the exact default convention rather than use a truthiness fallback.
    assert re.search(r'get\([^\n]*problem_number[^\n]*,\s*\{\}\)',q['content'])
    prior=rr.get(p['problem_number'],{})
    review=lambda p,r:sha(json.dumps([p,r],sort_keys=True).encode())
    rh=review(p,prior);sh=sha(p['statement'].encode())
    assert rh==c['review_hash']==expected['recomputed_full_record_review_sha256']
    assert sh==c['statement_hash']==expected['statement_sha256']
    mutant=copy.deepcopy(p);mutant['view_count']+=1
    controls={'nonstatement_change':review(mutant,{})!=rh,'prior_record_change':review(p,{'sentinel':1})!=rh,'statement_only':review(p['statement'],{})!=rh,'compact_serialization':sha(json.dumps([p,{}],sort_keys=True,separators=(',',':')).encode())!=rh}
    assert all(controls.values())
    related=[]
    for r in docs['problems.json']:
        v=(r.get('title','')+' '+r.get('statement','')).lower()
        if 'hopf' in v and ('bracket' in v or 'quasitriangular' in v):related.append(str(r['id']))
    assert sorted(related)==sorted(expected['related_records_screen']['matching_ids'])
    print(json.dumps({'status':'PASS','problem_id':'30005902','catalog_rank':802,'problem_number':p['problem_number'],'corpora':meta,'dataset_revision':manifest['revision'],'statement_sha256':sh,'review_sha256':rh,'review_serialization':'json.dumps([complete_problem_record, prior_record_or_empty_object], sort_keys=True), Python defaults','exact_prior_research_key_present':False,'missing_key_default':'empty object','queue_source_blob_sha1':blob(qb),'negative_controls':controls,'topic_screen_matching_ids':sorted(related),'matched_unique_id_and_code':True,'limits':'Full cached corpora rehashed; no live corpus download or mathematical-status inference.'},indent=2,sort_keys=True))
if __name__=='__main__':main()

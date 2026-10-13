"""UNEXECUTED separate own evidence reader; no candidate execution."""
import argparse,json,hashlib
from closure_common import F,need,raw,load,row,topology,fixed_inputs,own_ready
def main():
    p=argparse.ArgumentParser();p.add_argument('--self-manifest-sha256',required=True);a=p.parse_args();b=raw(F/'SELF_MANIFEST.json');need(hashlib.sha256(b).hexdigest()==a.self_manifest_sha256,'Genuine own closed self pin');s=load(F/'SELF_MANIFEST.json')
    need(type(s) is dict and set(s)=={'schema','source_only','self_excluded','files_count','files','file_modes','directory_modes','verdict_status','candidate_ready_sha256'} and s['schema']=='pr48-corrective-v5-review-evidence-closure/v1' and s['source_only'] is True and s['self_excluded']==['SELF_MANIFEST.json'] and type(s['files_count']) is int and s['files_count']==len(s['files']) and s['verdict_status']=='PASS_SOURCE_ONLY','Exact typed review self')
    ready_sha=hashlib.sha256(raw(F/'READY.json')).hexdigest();v=own_ready(ready_sha,0o444);names=v['closure_payload_files'];dirs=v['closure_directory_names'];need(s['candidate_ready_sha256']==v['candidate_source_ready_sha256'],'Bound rejected SOURCE');need([z['path'] for z in s['files']]==names,'Complete own domain');topology(F,sorted(names+['SELF_MANIFEST.json']),dirs,0o444)
    need(s['file_modes']==[dict(path=n,full_mode=0o444) for n in sorted(names+['SELF_MANIFEST.json'])] and s['directory_modes']==[dict(path=d,full_mode=0o755) for d in dirs],'Entire explicit mode domains')
    for z in s['files']:row(F,z,0o444)
    fixed_inputs();print(json.dumps(dict(status='PASS_READONLY_REVIEW_EVIDENCE_ONLY',files_count=s['files_count'],self_manifest_sha256=a.self_manifest_sha256,candidate_approved=False,production_executed=False)))
if __name__=='__main__':main()

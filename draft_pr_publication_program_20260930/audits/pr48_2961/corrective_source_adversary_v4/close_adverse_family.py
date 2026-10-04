"""UNEXECUTED ROOT-only own adverse freeze; no candidate/ROOT approval."""
import argparse,json,os,hashlib
from closure_common import F,need,raw,triple,topology,fixed_inputs,own_ready
def main():
    p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--personally-read-complete-source',action='store_true');p.add_argument('--ready-sha256',required=True);a=p.parse_args();need(a.execute and a.personally_read_complete_source,'ROOT explicit full source read');need(not (F/'SELF_MANIFEST.json').exists(),'Absent own self')
    v=own_ready(a.ready_sha256,0o644);names=v['closure_payload_files'];dirs=v['closure_directory_names'];topology(F,names,dirs,0o644);fixed_inputs();rows=[triple(F/n,n) for n in names]
    self=dict(schema='pr48-corrective-v4-adverse-evidence-closure/v1',source_only=True,self_excluded=['SELF_MANIFEST.json'],files_count=len(rows),files=rows,file_modes=[dict(path=n,full_mode=0o444) for n in sorted(names+['SELF_MANIFEST.json'])],directory_modes=[dict(path=d,full_mode=0o755) for d in dirs],verdict_status='REPAIR_REQUIRED_SOURCE',candidate_ready_sha256=v['candidate_source_ready_sha256'])
    with (F/'SELF_MANIFEST.json').open('xb') as f:f.write((json.dumps(self,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
    for n in names+['SELF_MANIFEST.json']:(F/n).chmod(0o444)
    topology(F,sorted(names+['SELF_MANIFEST.json']),dirs,0o444)
    for z in rows:need(triple(F/z['path'],z['path'])==z,'Entire adverse body unchanged by own freeze')
    print(json.dumps(dict(status='PASS_ADVERSE_EVIDENCE_CLOSURE_ONLY',files_count=len(rows),self_manifest_sha256=hashlib.sha256(raw(F/'SELF_MANIFEST.json')).hexdigest(),candidate_approved=False,production_executed=False)))
if __name__=='__main__':main()

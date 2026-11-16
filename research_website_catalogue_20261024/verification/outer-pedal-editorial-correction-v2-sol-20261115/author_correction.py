"""Exact seven-paragraph private overlay author and finite sealer; no old code execution."""
import sys
sys.dont_write_bytecode=True
from datetime import datetime,timezone
import json
import verify_correction as V

N=V.N

def new(p,b):
    V.need(p.is_relative_to(N),'owned new write only')
    with p.open('xb') as f:V.need(f.write(b)==len(b),'complete exclusive write')

def author(mode):
    V.need((mode=='normal')==__debug__,'actual requested optimization mode')
    rows,inputs,witness=V.references();fraction=V.fraction_guard(inputs);folder=N/('overlay-'+mode);folder.mkdir()
    out=[]
    for name in V.PATHS:
        old=V.pin(V.OLD/name,rows[name]);before,after=V.paragraphs(witness,name)
        V.need(old.count(before)==1,'one exact native-witnessed paragraph; no global replacement')
        body=old.replace(before,after,1);V.check_replacement(old,body,before,after)
        p=folder/name;p.parent.mkdir(parents=True,exist_ok=True);new(p,body)
        out.append({'path':name,'bytes':len(body),'SHA256':V.sha(body)})
    print(json.dumps({'status':'PRIVATE_SEVEN_BUFFER_OVERLAY_AUTHORED','mode':mode,'optimization_level':sys.flags.optimize,'files':out,'fraction_guard':fraction,'all_other_paths_resolve_to_original_pinned_namespace':True,'source_native_Bib_head_config_transformations':[],'publication_authority':False,'AA':None,'canonical_url':None},sort_keys=True))

def seal():
    V.need(not (N/'OWNED_MANIFEST.json').exists(),'new exact root terminals only')
    for mode in ('normal','optimized'):
        r=json.loads(V.read(N/('PRESEAL-'+mode+'.stdout')));V.need(r['status']=='PRIVATE_SEVEN_BUFFER_COPY_CORRECTION_CUSTODY_PASSED' and V.read(N/('PRESEAL-'+mode+'.stderr'))==b'','actual new normal/O closures')
    fs,dirs=V.extent(N);payload={}
    for n in fs:
        b=V.read(N/n);payload[n]={'bytes':len(b),'SHA256':V.sha(b)}
    for n in ['REPORT.md','VERDICT.json','CURRENT_CODE_MANIFEST.json','MINIMAL_DIFF.patch','EXECUTIONS.json']:V.need(n in payload,'complete bounded review packet')
    mb=(json.dumps({'payloads':payload,'directories':dirs,'exact_root_terminal_exclusions':['OWNED_MANIFEST.json','FINAL_SEAL.json'],'future_subtree_exclusions':[]},indent=2)+'\n').encode();new(N/'OWNED_MANIFEST.json',mb)
    s={'UTC':datetime.now(timezone.utc).isoformat(),'status':'FINAL_PRIVATE_COPY_CORRECTION_PENDING_INDEPENDENT_FACT_AUDIT_AND_ROOT_ADOPTION','manifest_SHA256':V.sha(mb),'payload_files':len(fs),'total_files_including2rootterminals':len(fs)+2,'directories':dirs,'authorization_SHA256':V.AUTH,'original_editorial_SHA256':'a6199b1d554dcfaae1201c2440ec0b92d97caf5c6d71fc6e24919bf781e898a5','original_fact_SHA256':'fea1ae8be0c778bb6b0a2cb6ed60cb4d4c492c5ae7a306fc098ef7d67f3a9e7b','original_NO_GO_retained':True,'exact_overlay_paths':V.PATHS,'only_semantic_change':'exact-star caustic semiaxis5/12->25/144','zero_other_byte_changes':True,'paired_normal_optimized_buffers':7,'publication_authority':False,'root_copy_adopted':False,'production_installation_authorized':False,'installed':False,'deployed':False,'live_verified':False,'browser_verified':False,'native_tracker_mutation_authority':False,'AA':None,'canonical_url':None,'follow_up':None,'completion_percent':100,'postseal_owned_writes_allowed':False}
    new(N/'FINAL_SEAL.json',(json.dumps(s,indent=2)+'\n').encode());V.close(N,fs,dirs,['OWNED_MANIFEST.json','FINAL_SEAL.json'])
    print(json.dumps({'status':s['status'],'FINAL_SEAL_SHA256':V.sha(V.read(N/'FINAL_SEAL.json')),'manifest_SHA256':V.sha(mb),'files':len(fs)+2,'directories':len(dirs),'publication_authority':False},sort_keys=True))

def main():
    V.need(not (N/'FINAL_SEAL.json').exists(),'immutable FINAL no reauthoring')
    V.need(sys.argv[1:] in [['normal'],['optimized'],['seal']],'finite private operations')
    if sys.argv[1]=='seal':seal()
    else:author(sys.argv[1])

if __name__=='__main__':main()

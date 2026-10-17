#!/usr/bin/env python3
"""Offline guard regressions: no Git/network/application mutations permitted."""
from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,subprocess,sys
ROOT=Path(__file__).resolve().parent

def load(name):
    spec=importlib.util.spec_from_file_location('offline_'+name,ROOT/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def need(c,m):
    if not c:raise RuntimeError(m)

def worker():
    m=load('update_pr_publication');metadata=load('check_public_downloads')
    # The identity validator is exercised directly; its Git reads are synthetic,
    # and any call outside these read-only commands fails the test immediately.
    files={m.BASE+'/fixture-'+str(n):('reviewed-bytes-'+str(n)).encode() for n in range(13)}
    commit='a'*40;mode={'tree':'valid'};calls=[]
    def fake_git(*args,data=None):
        calls.append(args)
        if args[0]=='rev-list':return (commit+' '+('b'*40 if mode['tree']=='parent' else m.ORIGINAL)+'\n').encode()
        if args[0]=='diff-tree':return ('\n'.join(sorted(files)+( ['foreign/path'] if mode['tree']=='paths' else []))+'\n').encode()
        if args[0]=='show':
            ref,path=args[1].split(':',1);need(ref==commit,'unexpected test commit')
            return b'wrong' if mode['tree']=='bytes' else files[path]
        raise RuntimeError('Unexpected Git operation; offline test permits only mocked tree reads: '+repr(args))
    m.git=fake_git;m.digest=lambda p:hashlib.sha256(('current:'+p.name).encode()).hexdigest()
    wanted=m.expected_identity({'doi':'10.5281/zenodo.current','id':123},{'updatedRange':"'Math Puzzles'!A999:D999"},files)
    saved={**copy.deepcopy(wanted),'commit':commit}
    need(m.validate_saved(saved,wanted,files)==commit,'valid saved identity rejected')
    rejected=[]
    for key in ['pr','base','branch','paths','files','review_gate_sha256','metadata_sha256','doi','deposit_id','tracker_range','tracker_receipt_sha256','public_verification_receipt_sha256','shared_index_modified']:
        bad=copy.deepcopy(saved)
        if key=='paths':bad[key].append('foreign/path')
        elif key=='files':bad[key][sorted(files)[0]]['sha256']='0'*64
        elif isinstance(bad[key],bool):bad[key]=not bad[key]
        elif isinstance(bad[key],int):bad[key]+=1
        else:bad[key]='stale:'+str(bad[key])
        try:m.validate_saved(bad,wanted,files)
        except RuntimeError:rejected.append(key)
        else:raise RuntimeError('Stale saved identity accepted at '+key)
    for kind in ['parent','paths','bytes']:
        mode['tree']=kind
        try:m.validate_saved(saved,wanted,files)
        except RuntimeError:rejected.append('actual_tree_'+kind)
        else:raise RuntimeError('Changed actual commit accepted: '+kind)
    mode['tree']='valid'
    bad={**saved,'commit':'not-a-commit'}
    try:m.validate_saved(bad,wanted,files)
    except RuntimeError:rejected.append('invalid_commit')
    else:raise RuntimeError('Invalid commit syntax accepted')
    wanted_meta=json.loads((ROOT/'zenodo-deposit.json').read_text())['metadata']
    public=copy.deepcopy(wanted_meta)
    public['resource_type']={'type':public.pop('upload_type'),'subtype':public.pop('publication_type'),'title':'Preprint'}
    public['license']={'id':public['license']};public['doi']='10.5281/zenodo.generated';public['relations']={'generated':True}
    fields=metadata.verify_public_metadata(public,wanted_meta);need(fields==sorted(wanted_meta),'not all supplied fields checked')
    rejected_meta=[]
    for key in wanted_meta:
        bad=copy.deepcopy(public)
        if key=='upload_type':bad['resource_type']['type']='wrong'
        elif key=='publication_type':bad['resource_type']['subtype']='wrong'
        elif key=='license':bad['license']['id']='wrong'
        else:bad[key]=None
        try:metadata.verify_public_metadata(bad,wanted_meta)
        except RuntimeError:rejected_meta.append(key)
        else:raise RuntimeError('Changed supplied public metadata accepted: '+key)
    return {'status':'PASS','valid_saved_identity_and_tree':True,'stale_saved_or_tree_controls_rejected':rejected,'all_public_metadata_fields_exact_fixture':fields,'each_supplied_public_metadata_field_corruption_rejected':sorted(rejected_meta),'scope':'Tests saved-identity validator and full metadata projection with offline fixtures, not a live GitHub/Zenodo/GWS integration test. Publication main guards receive an additional independent whole-package review. No actual Git, network or application call is allowed.'}

def main():
    if '--worker' in sys.argv:print(json.dumps(worker(),sort_keys=True));return
    runs=[]
    for flags in [[],['-O'],['-OO']]:
        r=subprocess.run([sys.executable,'-B',*flags,str(Path(__file__).resolve()),'--worker'],capture_output=True,text=True)
        need(r.returncode==0,r.stderr);runs.append({'flags':flags,'result':json.loads(r.stdout)})
    need(all(x['result']==runs[0]['result'] for x in runs),'mode-dependent regressions')
    receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':runs,'all_modes_identical':True,'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'repaired_workflow_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['update_pr_publication.py','check_public_downloads.py']}}
    (ROOT/'WORKFLOW_REGRESSION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Export only a concretely reviewed offer; no staging, commit, merge or services."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,stat,subprocess,sys
A=Path(__file__).resolve().parents[1];C=A.parents[2]
def need(v,m):
    if not v:raise RuntimeError(m)
def now():return datetime.now(timezone.utc).isoformat()
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_text())
def canonical(v):return (json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def regular(path):
    if os.path.lexists(path):
        s=path.lstat();need(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'Unsafe existing regular file')
def mkdirs(path):
    need(path.is_relative_to(C),'Outside own checkout')
    cur=C
    for part in path.relative_to(C).parts:
        cur=cur/part
        if os.path.lexists(cur):need(stat.S_ISDIR(cur.lstat().st_mode) and not cur.is_symlink(),'Unsafe directory component')
        else:cur.mkdir()
def atomic(path,body):
    mkdirs(path.parent);regular(path);tmp=path.with_name(path.name+'.pr110-export-tmp')
    fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    try:
        with os.fdopen(fd,'wb') as f:f.write(body);f.flush();os.fsync(f.fileno())
        regular(path);os.replace(tmp,path)
    finally:
        if tmp.exists():tmp.unlink()
def main():
    gatefile=Path(sys.argv[1]);need(gatefile.is_relative_to(A),'Root export gate must belong to effort');gate=read(gatefile)
    need(gate['schema']=='pr110-root-candidate-export-review/v1' and gate['actual_review'] is True and gate['clearance'] is True and gate['required_findings']==[],'Fresh actual candidate export gate')
    W=Path(gate['candidate']);need(W.parent==A/'native_execution_programs_v1/workspaces','Exact candidate scope');receiptfile=W/'CANDIDATE_RECEIPT.json';r=read(receiptfile)
    need(hp(receiptfile.read_bytes())==gate['candidate_receipt_pin'] and r['packet_sha256']==gate['packet_sha256'] and r['main_parent']==gate['main_parent'] and r['native_export_executed'] is False,'Exact actual private candidate binding')
    need(hp((W/'DIFF.txt').read_bytes())==r['DIFF_pin'] and r['native_status']=='claimed_solved' and r['turns_used']==2 and r['new_central_proof_search_turns']==0,'Reviewed diff/effort')
    actualpub=read(A/'ROOT_ACTUAL_PUBLICATION_TRACKER_AUTHENTICATION_20261006.json');need(actualpub['DOI']=='10.5281/zenodo.23191247' and actualpub['range']=="'Math Puzzles'!A32:D32",'Published/tracked actual bindings')
    operations=[];D=A/'actual_native_export_20261006';D.mkdir(exist_ok=False)
    def git(*args):
        start=now();p=subprocess.Popen(['git',*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);termination=None
        try:out,err=p.communicate(timeout=30)
        except subprocess.TimeoutExpired:p.kill();out,err=p.communicate();termination='deadline_KILL_and_reap'
        operations.append({'argv':['git',*args],'actual_PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'reaped':True,'termination_reason':termination,'stdout':hp(out),'stderr':hp(err)})
        (D/'PRECHECK_PROCESS_JOURNAL.json').write_bytes(canonical({'actual_operator_PID':os.getpid(),'operations':operations}))
        need(p.returncode==0 and termination is None,'Readonly export precheck failed; real failure retained');return out
    parent=gate['main_parent'];need(git('symbolic-ref','--short','HEAD').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==parent,'Own main changed')
    need(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==parent and not git('diff','--cached','--name-only','-z'),'Remote main or index changed')
    rows=r['affected_paths'];need(len({row['path'] for row in rows})==len(rows),'Duplicate export destinations')
    prefix='unsolved_math_prioritization/attempts/5100032/';derived={'assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','QUEUE.md'}
    need(not os.path.lexists(C/prefix),'Target attempt appeared before export')
    for row in rows:
        name=row['path'];rel=Path(name);need(not rel.is_absolute() and '..' not in rel.parts and str(rel)==name and (name.startswith(prefix) or name in {'unsolved_math_prioritization/'+n for n in derived}),'Exact allowed export path')
        source=W/'offer'/name;regular(source);need(source.is_file() and hp(source.read_bytes())==row['after'],'Reviewed offer drift')
        if row['before'] is not None:
            need(hp(git('show',parent+':'+name))==row['before'],'Native Git preimage drift');dest=C/name;regular(dest)
            if dest.exists():need(hp(dest.read_bytes())==row['before'],'Materialized native preimage drift')
    need(shutil.disk_usage(C).free>=sum(row['after']['bytes'] for row in rows)+64*1024*1024,'Export allocation/reserve')
    started=now();copied=[]
    for row in rows:
        dest=C/row['path'];body=(W/'offer'/row['path']).read_bytes();atomic(dest,body);need(hp(dest.read_bytes())==row['after'],'Full live native export readback')
        copied.append(row);(D/'PROGRESS.json').write_bytes(canonical({'UTC':now(),'actual_operator_PID':os.getpid(),'main_parent':parent,'copied':copied,'export_incomplete':len(copied)<len(rows)}))
    result={'schema':'pr110-actual-reviewed-native-export/v1','actual_operator_PID':os.getpid(),'UTC_start':started,'UTC_end':now(),'main_parent':parent,'candidate':str(W),'packet_sha256':r['packet_sha256'],'candidate_receipt_pin':hp(receiptfile.read_bytes()),'exported_paths':rows,'native_export_executed':True,'all_exported_full_bytes_checked':True,'original_status':'claimed_solved','original_budget':'2/5','new_central_proof_search_turns':0,'nonempty_prior_preserved':True,'DOI':actualpub['DOI'],'tracker_range':actualpub['range'],'Git_staging_executed':False,'merge_executed':False,'actual_precheck_processes':operations}
    result['native_acceptance_receipt_path']=prefix+'NATIVE_ACCEPTANCE_RECEIPT.json'
    body=canonical(result);(D/'RECEIPT.json').write_bytes(body);atomic(C/result['native_acceptance_receipt_path'],body)
    need((C/result['native_acceptance_receipt_path']).read_bytes()==body,'Actual target acceptance receipt readback')
    print(json.dumps({'exported_paths':len(rows),'additional_actual_target_receipt':result['native_acceptance_receipt_path'],'DOI':actualpub['DOI'],'main_parent':parent,'merge_pending':True}))
if __name__=='__main__':main()

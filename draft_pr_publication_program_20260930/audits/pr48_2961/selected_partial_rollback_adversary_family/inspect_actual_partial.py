"""Independent read-only footprint check; no rollback/helper import or native write."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Optimized Python refused')
R = Path('/Users/alec/Documents/Math')
A = R/'draft_pr_publication_program_20260930/audits/pr48_2961'
K = R/'unsolved_math_prioritization/attempts/2961'
ADMIN = {'status.json','readiness.json','review/verdict.json','review/review_summary.json'}
NEW_K = {'acceptance.json','ACCEPTANCE.md','MANIFEST.json'}
NEW_A = {'acceptance.json','remote_merge_receipt.json','integration_finalization.json'}
MERGE = '209581a4627b01745974837fe7adab62ab8c0af7'
HISTORICAL_HEAD = '11590683569346ea67151a497e798094347c8d29'
COMMANDS = []

def need(ok, message):
    if not ok: raise RuntimeError(message)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def pairs(items):
    out = {}
    for key, value in items:
        need(key not in out, 'Duplicate JSON key')
        out[key] = value
    return out
def parse(raw): return json.loads(raw, object_pairs_hook=pairs)
def safe(p):
    p=Path(p)
    need(p.is_absolute() and p.is_relative_to(R), 'Outside repo')
    need(all(not d.is_symlink() for d in [p,*p.parents]), 'Symlink path')
    st=p.lstat(); need(stat.S_ISREG(st.st_mode), 'Not regular')
    return st
def row(p):
    st=safe(p); raw=p.read_bytes(); after=p.lstat()
    identity=lambda z:(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns,stat.S_IMODE(z.st_mode))
    need(identity(st)==identity(after), 'Concurrent file mutation')
    return {'path':p.relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw),'worktree_mode':stat.S_IMODE(st.st_mode),'uid':st.st_uid,'gid':st.st_gid,'mtime_ns':st.st_mtime_ns,'ctime_ns':st.st_ctime_ns,'inode':st.st_ino,'device':st.st_dev,'nlink':st.st_nlink}
def relative(n):
    need(type(n) is str and n and '\\' not in n and '\0' not in n, 'Bad path')
    p=PurePosixPath(n)
    need(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git'}.intersection(p.parts),'Noncanonical path')
    return n
def git(*args):
    env=os.environ.copy()
    for n in ['GIT_INDEX_FILE','GIT_WORK_TREE','GIT_DIR','GIT_COMMON_DIR','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES']: env.pop(n,None)
    env.update(GIT_OPTIONAL_LOCKS='0',GIT_LITERAL_PATHSPECS='1')
    start=utc(); p=subprocess.Popen(['git',*args],cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate(timeout=30)
    COMMANDS.append({'argv':['git',*args],'pid':p.pid,'started_utc':start,'finished_utc':utc(),'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr_utf8':err.decode('utf8',errors='replace')})
    need(p.returncode==0,'Read-only Git query failed')
    return out
def compare_pin(z):
    got=row(R/relative(z['path']))
    return {'expected':z,'actual':got,'body_and_full_mode_match':all(got[k]==z[k] for k in ['path','bytes','sha256','worktree_mode'])}
def diff(old,new,path=''):
    if type(old) is not type(new): return [{'path':path,'before':old,'after':new}]
    if isinstance(old,dict):
        result=[]
        for key in sorted(old.keys()|new.keys()):
            if key not in old: result.append({'path':path+'/'+key,'before_absent':True,'after':new[key]})
            elif key not in new: result.append({'path':path+'/'+key,'before':old[key],'after_absent':True})
            else: result.extend(diff(old[key],new[key],path+'/'+key))
        return result
    if isinstance(old,list):
        need(len(old)==len(new),'List length changed')
        return [z for i,(o,n) in enumerate(zip(old,new)) for z in diff(o,n,path+'/'+str(i))]
    return [] if old==new else [{'path':path,'before':old,'after':new}]

def main():
    started=utc()
    capraw=(A/'root_finalize_actual_capture/CAPTURE.json').read_bytes(); cap=parse(capraw)
    need(cap['pid']==80480 and cap['exit_code']==1 and cap['phase']=='finalize','Wrong failed actual adapter')
    need(sha(capraw)=='7da4a46f2fbedb2e4e56f7a4f2b5968369fc2841acca622b4a76e72456583983','Wrong failed capture')
    need(cap['HEAD_before']==HISTORICAL_HEAD,'Wrong historical failed HEAD')
    current_head=git('rev-parse','HEAD').decode().strip()
    index_path=Path(git('rev-parse','--git-path','index').decode().strip())
    if not index_path.is_absolute(): index_path=R/index_path
    index_before=row(index_path)
    cached=git('diff','--cached','--raw','-z')
    manifest=parse((K/'MANIFEST.json').read_bytes())
    rows=manifest['files']; names={relative(z['path']) for z in rows}
    need(len(rows)==1957 and len(names)==1957 and manifest['files_count']==1957 and manifest['self_excluded']==['MANIFEST.json'],'Wrong strict canonical manifest domain')
    all_names=names|{'MANIFEST.json'}
    actual_files=set(); actual_dirs=set()
    for p in K.rglob('*'):
        need(not p.is_symlink(),'Canonical symlink')
        n=p.relative_to(K).as_posix()
        if p.is_file(): actual_files.add(n)
        elif p.is_dir(): actual_dirs.add(n)
        else: need(False,'Canonical special file')
    expected_dirs={d.as_posix() for n in all_names for d in PurePosixPath(n).parents if d.as_posix()!='.'}
    need(actual_files==all_names and actual_dirs==expected_dirs,'Canonical exact topology differs')
    observed={n:row(K/n) for n in all_names}
    need(all(z['worktree_mode']==0o444 for z in observed.values()),'Canonical partial freeze differs')
    need(all(observed[z['path']]['bytes']==z['bytes'] and observed[z['path']]['sha256']==z['sha256'] for z in rows),'Canonical manifest body closure fails')
    overlay=parse((A/'integration_check.json').read_bytes())['canonical_overlay_files']
    old={relative(z['path']):z for z in overlay}
    need(len(overlay)==1955 and len(old)==1955 and all_names==set(old)|NEW_K,'Original overlay/current1958 domain differs')
    changed={n for n,z in old.items() if observed[n]['bytes']!=z['bytes'] or observed[n]['sha256']!=z['sha256']}
    need(changed==ADMIN,'Body changes outside exact ADMIN4')
    restore=[]
    for n in sorted(ADMIN):
        body=git('show',MERGE+':'+(K/n).relative_to(R).as_posix())
        need(len(body)==old[n]['bytes'] and sha(body)==old[n]['sha256'],'Original merge admin blob not overlay exact')
        restore.append({'path':(K/n).relative_to(R).as_posix(),'merge':MERGE,'original_overlay':old[n],'current':observed[n],'restoration_full_mode_proposed':0o644,'current_full_mode':0o444})
    canonical_new=[observed[n] for n in sorted(NEW_K)]
    audit_new=[row(A/n) for n in sorted(NEW_A)]
    inventory_current=row(R/'draft_pr_publication_program_20260930/inventory.json')
    preimage=row(A/'integration_inventory_before.json')
    need(preimage['sha256']=='171061fc88b5ca06e200cc2cead9d11fe1e7435f8f98435907937bdc0f9df0d8','Inventory preimage changed')
    invdiff=diff(parse((A/'integration_inventory_before.json').read_bytes()),parse((R/'draft_pr_publication_program_20260930/inventory.json').read_bytes()))
    native=[compare_pin(z) for z in cap['native13_before'] if z['path']!='draft_pr_publication_program_20260930/inventory.json']
    foreign=[compare_pin(z) for z in cap['protected_foreign_before']]
    logs=[compare_pin(z) for z in cap['owned_mutable_logs_before']]
    need(len(native)==12 and len(foreign)==7 and len(logs)==2,'Protection cardinality wrong')
    need(all(z['body_and_full_mode_match'] for z in native+logs),'Protected native/log full body/mode differs')
    for z in native+foreign+logs:
        need(row(R/z['actual']['path'])==z['actual'],'Current protection changed during scan')
    index_after=row(index_path)
    need(index_before==index_after,'Current raw real index changed during check')
    need(git('rev-parse','HEAD').decode().strip()==current_head,'HEAD drift during check')
    footprint=[z['current'] for z in restore]+canonical_new+audit_new+[inventory_current]
    need(len(footprint)==11 and len({z['path'] for z in footprint})==11,'Exact selected footprint count differs')
    result={'schema':'pr48-independent-selected-partial-footprint/v1','operator_pid':os.getpid(),'started_utc':started,'finished_utc':utc(),'read_only':True,'rollback_source_read':False,'production_or_git_mutation_executed':False,'ROOT_approval_claimed':False,'math_review_credit':0,'failed_capture':row(A/'root_finalize_actual_capture/CAPTURE.json'),'failed_streams':[row(A/'root_finalize_actual_capture/stdout.bin'),row(A/'root_finalize_actual_capture/stderr.bin')],'canonical_manifest':row(K/'MANIFEST.json'),'canonical_manifest_payload_count':1957,'canonical_total_files':1958,'canonical_directories':len(actual_dirs),'canonical_all_current_modes':0o444,'original_overlay_count':1955,'unchanged_science_bodies_count':1951,'unchanged_science_full_mode':0o444,'changed_existing_admin_count':4,'restore_admin':restore,'canonical_new':canonical_new,'audit_new':audit_new,'inventory_preimage':preimage,'inventory_current':inventory_current,'inventory_exact_structural_changes':invdiff,'selected_current_footprint':footprint,'selected_current_footprint_count':11,'protected_native12':native,'protected_foreign7':foreign,'protected_owned_logs2':logs,'current_protection_reread_stable':True,'historical_foreign_differences_count':sum(not z['body_and_full_mode_match'] for z in foreign),'foreign_concurrent_change_causation_established':False,'current_HEAD':current_head,'historical_failed_HEAD':HISTORICAL_HEAD,'current_real_index_before':index_before,'current_real_index_after':index_after,'historical_failed_capture_index_before':cap['whole_index_before'],'current_index_equals_historical_preimage_sha':index_before['sha256']==cap['whole_index_before']['sha256'],'cached_raw_diff_bytes':len(cached),'cached_raw_diff_sha256':sha(cached),'index_drift_causation_established':False,'read_only_git_commands':COMMANDS}
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
    try: main()
    except BaseException:
        print(json.dumps({'partial_read_only_git_commands':COMMANDS,'checks_completed':False},sort_keys=True,indent=2))
        raise

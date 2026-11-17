"""Administrative finite audit seal only; no producer/helper modes or imports."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import time

HERE=Path(__file__).resolve().parent
TERMINALS=('OWNED_MANIFEST.json','FINAL.json')
def enc(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'SHA256':sha(b),'mode':format(stat.S_IMODE(p.lstat().st_mode),'04o')}
def snap(root):
    files={};dirs={}
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat();name='.' if p==root else p.relative_to(root).as_posix()
        if stat.S_ISDIR(st.st_mode):dirs[name]={'mode':format(stat.S_IMODE(st.st_mode),'04o'),'empty':not any(p.iterdir())}
        else:
            assert stat.S_ISREG(st.st_mode),(root,name)
            files[name]=pin(p)
    return {'root':str(root),'files':files,'directories':dirs,'regular_files':len(files),'child_directories':len(dirs)-1}

before=json.loads((HERE/'BEFORE.json').read_text());after=json.loads((HERE/'AFTER.json').read_text())
final_guards={}
for key in ('PREPARATION','STAGE'):
    assert before[key]==after[key]
    current=snap(Path(before[key]['root']));assert current==before[key],key
    final_guards[key]=current
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (HERE/'FINAL_INPUT_CUSTODY.json').open('xb') as f:
    f.write(enc({'UTC':stamp,'full_preparation_stage_final_exact':True,'roots':final_guards}))
with (HERE/'SEAL_READ_RECEIPT.json').open('xb') as f:
    f.write(enc({'UTC':stamp,'administrative_sealer_complete_read_before_execution':True,
                'sealer':pin(Path(__file__)),'producer_helper_executions':0,'static_data_reader_attempts':1}))
with (HERE/'RESEARCH_LOG.md').open('a') as f:
    f.write('- '+stamp+': Static source audit PASS, no blocking source flaw or requested source correction. Full preparation11/0 and stage1598/760 closure guards match byte/mode/hidden/empty/topology snapshots. Own finite actual audit namespace sealed; producer/helper modes remain unexecuted. Completion100%; no action authority; follow_up:null. STOP for root adoption.\n')
finding=json.loads((HERE/'FINDINGS.json').read_text())
assert finding['status']=='PASS_STATIC_SOURCE_NO_ACTION_AUTHORITY' and finding['blocking_static_findings']==[]
handles={name:(HERE/name).open('xb') for name in TERMINALS}
paths=[HERE,*sorted(HERE.rglob('*'))]
for p in paths:assert stat.S_ISREG(p.lstat().st_mode) or stat.S_ISDIR(p.lstat().st_mode)
for p in paths:
    if p.is_file():p.chmod(0o444)
for p in sorted(paths,key=lambda x:len(x.parts),reverse=True):
    if p.is_dir():p.chmod(0o555)
frozen_ns=time.time_ns();rows=[]
for p in [HERE,*sorted(HERE.rglob('*'))]:
    st=p.lstat();name='.' if p==HERE else p.relative_to(HERE).as_posix();kind='directory' if p.is_dir() else 'file'
    r={'path':name,'kind':kind,'mode':format(stat.S_IMODE(st.st_mode),'04o'),
       'hidden':any(t.startswith('.') and t not in ('.','..') for t in Path(name).parts),'mtime_ns':st.st_mtime_ns}
    if kind=='directory':r['empty']=not any(p.iterdir())
    elif name in TERMINALS:r.update(bytes=0,SHA256=None,empty=False,mtime_ns=frozen_ns,recursive_terminal_hash_excluded=True)
    else:
        raw=p.read_bytes();r.update(bytes=len(raw),SHA256=sha(raw),empty=not raw)
    rows.append(r)
counts={'regular_files':sum(r['kind']=='file' for r in rows),
        'child_directories':sum(r['kind']=='directory' for r in rows)-1,
        'hidden_files':sum(r['kind']=='file' and r['hidden'] for r in rows),
        'empty_files':sum(r['kind']=='file' and r['empty'] for r in rows),
        'empty_directories':sum(r['kind']=='directory' and r['empty'] for r in rows)}
manifest={'schema':'finite-independent-production-static-audit-manifest-v1','UTC':stamp,'root':str(HERE),
    'counts':counts,'all_actual_hidden_ignored_empty_modes_topology_included':True,
    'only_recursive_terminal_content_hash_exclusions':list(TERMINALS),'entries':rows}
sizes={name:0 for name in TERMINALS}
for step in range(20):
    for row in rows:
        if row['path'] in TERMINALS:row['bytes']=sizes[row['path']]
    mb=enc(manifest)
    final={'schema':'independent-hafnian-retract-production-static-audit-FINAL-v1','UTC':stamp,
        'status':'PASS_STATIC_SOURCE_NO_ACTION_AUTHORITY','completion_percent':100,'root':str(HERE),'counts':counts,
        'manifest_SHA256':sha(mb),'terminal_sizes':sizes,'REPORT':pin(HERE/'REPORT.md'),'FINDINGS':pin(HERE/'FINDINGS.json'),
        'helper':{'path':str(Path(before['PREPARATION']['root'])/'release_two.py'),'bytes':90609,'lines':1260,
                  'SHA256':'6a831b55fbd1d49196619e047e6461d36c9171da94f5ede8d45cdd8148d5b734','mode':'0644'},
        'PLAN':{'path':str(Path(before['PREPARATION']['root'])/'PLAN.json'),'bytes':11588,
                'SHA256':'682ae4747c3004aef1b74fb8bce7f43b76984c427353419a7e8c770e941fa2a1','mode':'0644'},
        'blocking_static_findings':[],'required_source_corrections':[],
        'preparation_counts':[11,0],'stage_counts':[1598,760],'complete_final_input_guard':pin(HERE/'FINAL_INPUT_CUSTODY.json'),
        'all_producer_helper_modes_unexecuted_by_audit':True,'producer_import_AST_compile_test':0,
        'passive_data_reader_attempts':1,'Git_commands':0,'network':0,'W_source_otherpacket_mutations':0,
        'administrative_custody_seal_only':True,'root_mode':'0555','all_file_modes':'0444',
        'future_root_audit_adoptions_ignore_prerequisite_fresh_action_authorities_required':True,
        'runtime_install_publish_or_live_success_certificate':False,'action_authority':False,
        'deployment_Sheet_AA_redirect_authority':False,'AA':None,'follow_up':None,
        'only_recursive_terminal_content_hash_exclusions':list(TERMINALS),'quiescent_stop':True}
    fb=enc(final);new_sizes={TERMINALS[0]:len(mb),TERMINALS[1]:len(fb)}
    if new_sizes==sizes:break
    sizes=new_sizes
else:raise AssertionError('finite terminal sizes did not stabilize')
handles[TERMINALS[0]].write(mb);handles[TERMINALS[1]].write(fb)
for f in handles.values():f.flush();os.fsync(f.fileno());f.close()
for name in TERMINALS:os.utime(HERE/name,ns=(frozen_ns,frozen_ns))
actual=[HERE,*sorted(HERE.rglob('*'))];assert len(actual)==len(rows)
for r,p in zip(rows,actual):
    st=p.lstat();assert format(stat.S_IMODE(st.st_mode),'04o')==r['mode'] and st.st_mtime_ns==r['mtime_ns']
    if r['kind']=='file':
        raw=p.read_bytes();assert len(raw)==r['bytes'] and (not raw)==r['empty']
        if r['SHA256'] is not None:assert sha(raw)==r['SHA256']
    else:assert (not any(p.iterdir()))==r['empty']
assert pin(HERE/'OWNED_MANIFEST.json')['SHA256']==final['manifest_SHA256']
print(json.dumps({'status':final['status'],'UTC':stamp,'counts':counts,
    'FINAL_SHA256':pin(HERE/'FINAL.json')['SHA256'],'OWNED_MANIFEST_SHA256':pin(HERE/'OWNED_MANIFEST.json')['SHA256'],
    'REPORT_SHA256':pin(HERE/'REPORT.md')['SHA256'],'inputs_final_exact':True,'stop':True}))

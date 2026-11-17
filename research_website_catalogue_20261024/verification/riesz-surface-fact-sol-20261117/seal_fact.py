"""Administrative custody closure only; does not repeat the fact audit."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import time

HERE=Path(__file__).resolve().parent
TERMINALS=('MANIFEST.json','FINAL.json')
def enc(x): return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def sha(x): return hashlib.sha256(x).hexdigest()
def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':sha(b),'md5':hashlib.md5(b).hexdigest(),
            'mode':oct(stat.S_IMODE(p.lstat().st_mode))}
def snap(root):
    rows=[]
    for p in [root,*sorted(root.rglob('*'))]:
        m=p.lstat().st_mode
        name='.' if p==root else p.relative_to(root).as_posix()
        kind='directory' if stat.S_ISDIR(m) else 'file' if stat.S_ISREG(m) else 'other'
        assert kind!='other'
        r={'path':name,'kind':kind,'mode':oct(stat.S_IMODE(m)),
           'hidden':any(t.startswith('.') and t not in ('.','..') for t in Path(name).parts)}
        if kind=='file':r.update(pin(p));r['empty']=r['bytes']==0
        else:r['empty']=not any(p.iterdir())
        rows.append(r)
    return {'root':str(root),'files':sum(r['kind']=='file' for r in rows),
            'child_directories':sum(r['kind']=='directory' for r in rows)-1,'entries':rows}

before=json.loads((HERE/'BEFORE.json').read_text())
after=json.loads((HERE/'AFTER.json').read_text())
guards={}
for label in ('SOURCE','WRITER'):
    assert before[label]==after[label]
    current=snap(Path(before[label]['root']))
    assert current==before[label],label
    guards[label]=current
for row in json.loads((HERE/'PROTECTED_PINS.json').read_text()):
    assert pin(Path(row['path']))=={k:v for k,v in row.items() if k!='path'}
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (HERE/'FINAL_PROTECTED_GUARDS.json').open('xb') as f:
    f.write(enc({'UTC':stamp,'source_and_writer_complete_exact':True,
                'protected_pins_final_exact':True,'roots':guards}))
with (HERE/'RESEARCH_LOG.md').open('a') as f:
    f.write('- '+stamp+': Independent private fact audit PASS, no issues or producer changes. Final source39/15 and writer28/1 custody rechecks remain exact. Finite actual audit packet sealed with no excluded payloads, source/writer modes untouched. Completion100%; follow_up:null. STOP for root adoption.\n')
issues=json.loads((HERE/'ISSUES.json').read_text())
assert issues['status']=='PASS' and not issues['issues']
with (HERE/'SEAL_READ_RECEIPT.json').open('xb') as f:
    f.write(enc({'UTC':stamp,'complete_custody_sealer_read_before_execution':True,
                'sealer':pin(Path(__file__)),'fact_reader_executions':1,
                'producer_executions':0,'scientific_executions':0}))

handles={name:(HERE/name).open('xb') for name in TERMINALS}
paths=[HERE,*sorted(HERE.rglob('*'))]
for p in paths:
    assert stat.S_ISREG(p.lstat().st_mode) or stat.S_ISDIR(p.lstat().st_mode)
for p in paths:
    if p.is_file():p.chmod(0o444)
for p in sorted(paths,key=lambda q:len(q.parts),reverse=True):
    if p.is_dir():p.chmod(0o555)
frozen_ns=time.time_ns()
rows=[]
for p in [HERE,*sorted(HERE.rglob('*'))]:
    st=p.lstat();name='.' if p==HERE else p.relative_to(HERE).as_posix()
    kind='directory' if p.is_dir() else 'file'
    r={'path':name,'kind':kind,'mode':oct(stat.S_IMODE(st.st_mode)),
       'hidden':any(t.startswith('.') and t not in ('.','..') for t in Path(name).parts),
       'mtime_ns':st.st_mtime_ns}
    if kind=='directory':r['empty']=not any(p.iterdir())
    elif name in TERMINALS:
        r.update(bytes=0,sha256=None,empty=False,mtime_ns=frozen_ns,
                 recursive_terminal_hash_excluded=True)
    else:
        data=p.read_bytes();r.update(bytes=len(data),sha256=sha(data),empty=not data)
    rows.append(r)
counts={'files':sum(r['kind']=='file' for r in rows),
        'child_directories':sum(r['kind']=='directory' for r in rows)-1,
        'hidden_files':sum(r['kind']=='file' and r['hidden'] for r in rows),
        'empty_files':sum(r['kind']=='file' and r['empty'] for r in rows),
        'empty_directories':sum(r['kind']=='directory' and r['empty'] for r in rows)}
manifest={'schema':'finite-private-fact-audit-manifest-v1','root':str(HERE),'UTC':stamp,
          'counts':counts,'all_actual_hidden_ignored_empty_and_modes':True,
          'only_recursive_content_hash_exclusions':list(TERMINALS),'entries':rows}
sizes={name:0 for name in TERMINALS}
for step in range(20):
    for row in rows:
        if row['path'] in TERMINALS:row['bytes']=sizes[row['path']]
    mb=enc(manifest)
    final={'schema':'finite-private-fact-audit-final-v1','UTC':stamp,'record_id':'23202994','row':190,
           'status':'PASS','issues':[],'completion_percent':100,'root':str(HERE),'counts':counts,
           'MANIFEST_sha256':sha(mb),'terminal_sizes':sizes,
           'REPORT_sha256':pin(HERE/'REPORT.md')['sha256'],
           'protected_guards_sha256':pin(HERE/'FINAL_PROTECTED_GUARDS.json')['sha256'],
           'writer_FINAL_sha256':'4d48b3304f6e1de25e53092ef489f9bb5f02259e26ad4c751df4146e16b5ef4d',
           'writer_MANIFEST_sha256':'13164254fa6596772435ad817efacf99ab035bf418a07d601687f44846b50db6',
           'article_sha256':'3685e7c43c42d45743a22ed8d05c3cb2277bca1922162549cb348d67c610380e',
           'source_counts':[39,15],'writer_counts':[28,1],'source_writer_full_final_exact':True,
           'root_mode':'0o555','file_modes':'0o444','fact_reader_attempts':1,
           'new_scientific_runs':0,'producer_runs':0,'repair_or_retry':False,
           'canonical_url':None,'base_url':None,'production_url':None,'actual_publication_date':None,
           'AA':None,'publication_authority':False,'W_access':False,'Sheet_access':False,'network':0,
           'follow_up':None,'only_recursive_content_hash_exclusions':list(TERMINALS),
           'scope':'Private static fact verdict; root adoption only; no staging, deployment, rendering or live certificate',
           'quiescent_stop':True}
    fb=enc(final)
    next_sizes={TERMINALS[0]:len(mb),TERMINALS[1]:len(fb)}
    if next_sizes==sizes:break
    sizes=next_sizes
else:raise AssertionError('finite terminal sizing failed')
handles[TERMINALS[0]].write(mb);handles[TERMINALS[1]].write(fb)
for f in handles.values():f.flush();os.fsync(f.fileno());f.close()
for name in TERMINALS:os.utime(HERE/name,ns=(frozen_ns,frozen_ns))
actual=[HERE,*sorted(HERE.rglob('*'))]
assert len(actual)==len(rows)
for row,p in zip(rows,actual):
    st=p.lstat()
    assert oct(stat.S_IMODE(st.st_mode))==row['mode'] and st.st_mtime_ns==row['mtime_ns']
    if row['kind']=='file':
        data=p.read_bytes()
        assert len(data)==row['bytes'] and (not data)==row['empty']
        if row['sha256'] is not None:assert sha(data)==row['sha256']
    else:assert (not any(p.iterdir()))==row['empty']
assert pin(HERE/'MANIFEST.json')['sha256']==final['MANIFEST_sha256']
print(json.dumps({'status':'PASS','UTC':stamp,'counts':counts,
    'FINAL_sha256':pin(HERE/'FINAL.json')['sha256'],
    'MANIFEST_sha256':pin(HERE/'MANIFEST.json')['sha256'],
    'REPORT_sha256':pin(HERE/'REPORT.md')['sha256'],
    'source_writer_final_exact':True,'stop':True}))

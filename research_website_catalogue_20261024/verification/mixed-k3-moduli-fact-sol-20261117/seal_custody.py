"""Administrative finite fact-audit custody seal; no repeat fact/science route."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import time

HERE=Path(__file__).resolve().parent;TERMINALS=('MANIFEST.json','FINAL.json')
def enc(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'SHA256':sha(b),'MD5':hashlib.md5(b).hexdigest(),'mode':oct(stat.S_IMODE(p.lstat().st_mode))}
def snap(root):
    rows=[]
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat();name='.' if p==root else p.relative_to(root).as_posix();directory=stat.S_ISDIR(st.st_mode)
        assert directory or stat.S_ISREG(st.st_mode)
        r={'path':name,'kind':'directory' if directory else 'file','mode':oct(stat.S_IMODE(st.st_mode)),
           'hidden':any(t.startswith('.') and t not in ('.','..') for t in Path(name).parts)}
        if directory:r['empty']=not any(p.iterdir())
        else:r.update(pin(p));r['empty']=r['bytes']==0
        rows.append(r)
    return {'root':str(root),'files':sum(r['kind']=='file' for r in rows),'childdirs':sum(r['kind']=='directory' for r in rows)-1,'entries':rows}
before=json.loads((HERE/'BEFORE.json').read_text());after=json.loads((HERE/'AFTER.json').read_text())
guards={}
for label in ('SOURCE','WRITER'):
    assert before[label]==after[label]
    current=snap(Path(before[label]['root']));assert current==before[label],label
    guards[label]=current
for row in json.loads((HERE/'INPUT_PINS.json').read_text()):
    assert pin(Path(row['path']))=={k:v for k,v in row.items() if k!='path'}
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (HERE/'FINAL_INPUT_GUARDS.json').open('xb') as f:f.write(enc({'UTC':stamp,'source_writer_full_exact':True,'roots':guards,'W_access_or_guard':False}))
with (HERE/'SEAL_READ_RECEIPT.json').open('xb') as f:f.write(enc({'UTC':stamp,'complete_custody_sealer_read_before_execution':True,'sealer':pin(Path(__file__)),'fact_data_reader_attempts':1,'new_scientific_or_producer_runs':0}))
with (HERE/'RESEARCH_LOG.md').open('a') as f:f.write('- '+stamp+': Private fact audit PASS/no issues. Final source43/7 and writer28/1 full custody remains exact; bounded scientific disposition and reservation preserved. Own complete actual packet frozen at files0444/root0555. Completion100%; no future action authority; follow_up:null. STOP for root adoption.\n')
assert json.loads((HERE/'ISSUES.json').read_text())['issues']==[]
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
    r={'path':name,'kind':kind,'mode':oct(stat.S_IMODE(st.st_mode)),'mtime_ns':st.st_mtime_ns,
       'hidden':any(t.startswith('.') and t not in ('.','..') for t in Path(name).parts)}
    if kind=='directory':r['empty']=not any(p.iterdir())
    elif name in TERMINALS:r.update(bytes=0,SHA256=None,empty=False,mtime_ns=frozen_ns,recursive_terminal_hash_excluded=True)
    else:
        data=p.read_bytes();r.update(bytes=len(data),SHA256=sha(data),empty=not data)
    rows.append(r)
counts={'files':sum(r['kind']=='file' for r in rows),'child_directories':sum(r['kind']=='directory' for r in rows)-1,
        'hidden_files':sum(r['kind']=='file' and r['hidden'] for r in rows),'empty_files':sum(r['kind']=='file' and r['empty'] for r in rows),
        'empty_directories':sum(r['kind']=='directory' and r['empty'] for r in rows)}
manifest={'schema':'finite-private-k3-fact-manifest-v1','root':str(HERE),'UTC':stamp,'counts':counts,
          'all_actual_hidden_ignored_empty_modes_topology_included':True,'only_recursive_content_hash_exclusions':list(TERMINALS),'entries':rows}
sizes={name:0 for name in TERMINALS}
for step in range(20):
    for row in rows:
        if row['path'] in TERMINALS:row['bytes']=sizes[row['path']]
    mb=enc(manifest)
    final={'schema':'independent-private-k3-fact-FINAL-v1','status':'PASS','record_id':'23204176','sheet_row':191,
        'UTC':stamp,'completion_percent':100,'root':str(HERE),'counts':counts,'MANIFEST_SHA256':sha(mb),'terminal_sizes':sizes,
        'REPORT':pin(HERE/'REPORT.md'),'ISSUES':pin(HERE/'ISSUES.json'),'final_input_guard':pin(HERE/'FINAL_INPUT_GUARDS.json'),
        'writer_FINAL_SHA256':'245fcc03a3105d4a3a093821bd79e995d13225246a5e0f96b7a6c3e322a814b8',
        'writer_MANIFEST_SHA256':'1aa3d7271c59f80db746b41005b605d2e68ec448cdf3125b3b282ae7e6acb171',
        'article_SHA256':'fa80a828093717d9648e8a806aed891f0e52e9c517c17f7200624e67915c37e5',
        'issues':[],'source_counts':[43,7],'writer_counts':[28,1],'source_writer_full_exact':True,
        'scientific_clearance_inherited':'PASS_BOUNDED_SUBSTANTIVE_REVIEW','SCOPE_reservation_preserved':True,
        'fact_reader_attempts':1,'new_scientific_or_producer_runs':0,'source_import_AST_compile_test':0,
        'network_Git_W_Sheet':0,'W_access_or_whole_W_guard':False,'administrative_custody_seal_only':True,
        'root_mode':'0o555','all_file_modes':'0o444','native_API_version':None,
        'canonical_url':None,'base_url':None,'production_url':None,'actual_publication_date':None,'AA':None,
        'publication_or_future_action_authority':False,'rendered_or_live_certificate':False,'follow_up':None,
        'only_recursive_content_hash_exclusions':list(TERMINALS),'quiescent_stop':True}
    fb=enc(final);new_sizes={TERMINALS[0]:len(mb),TERMINALS[1]:len(fb)}
    if new_sizes==sizes:break
    sizes=new_sizes
else:raise AssertionError('finite terminal sizes')
handles[TERMINALS[0]].write(mb);handles[TERMINALS[1]].write(fb)
for f in handles.values():f.flush();os.fsync(f.fileno());f.close()
for name in TERMINALS:os.utime(HERE/name,ns=(frozen_ns,frozen_ns))
actual=[HERE,*sorted(HERE.rglob('*'))];assert len(actual)==len(rows)
for r,p in zip(rows,actual):
    st=p.lstat();assert oct(stat.S_IMODE(st.st_mode))==r['mode'] and st.st_mtime_ns==r['mtime_ns']
    if r['kind']=='file':
        b=p.read_bytes();assert len(b)==r['bytes'] and (not b)==r['empty']
        if r['SHA256'] is not None:assert sha(b)==r['SHA256']
    else:assert (not any(p.iterdir()))==r['empty']
assert pin(HERE/'MANIFEST.json')['SHA256']==final['MANIFEST_SHA256']
print(json.dumps({'status':'PASS','UTC':stamp,'counts':counts,'FINAL_SHA256':pin(HERE/'FINAL.json')['SHA256'],
    'MANIFEST_SHA256':pin(HERE/'MANIFEST.json')['SHA256'],'REPORT_SHA256':pin(HERE/'REPORT.md')['SHA256'],
    'source_writer_full_final_exact':True,'W_access':False,'stop':True}))

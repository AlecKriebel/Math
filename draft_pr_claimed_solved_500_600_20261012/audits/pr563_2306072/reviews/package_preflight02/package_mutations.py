#!/usr/bin/env python3
"""Fresh adversarial runner mutations on expendable copies, never canonical files."""
from pathlib import Path, PurePosixPath
import hashlib, json, os, shutil, subprocess, sys

HERE=Path(__file__).resolve().parent
BASE=HERE/'.cache/extract1/support_slit_verification'
CACHE=HERE/'.cache/mutations'
CACHE.mkdir(exist_ok=True)
records=[]
def write(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
def reseal_outer(p):
    m=json.loads((p/'MANIFEST.json').read_text())
    for n,x in m['files'].items():
        b=(p/n).read_bytes();x['sha256']=hashlib.sha256(b).hexdigest();x['bytes']=len(b)
    write(p/'MANIFEST.json',m)
def reseal_inner_file(p,seal,name):
    q=p/seal;m=json.loads(q.read_text());b=(q.parent/name).read_bytes()
    m['files'][name]=hashlib.sha256(b).hexdigest();write(q,m)
def case(name,mutate,expected,env=None,accept=False):
    p=CACHE/name
    if p.exists():shutil.rmtree(p)
    shutil.copytree(BASE,p);mutate(p)
    run=subprocess.run([sys.executable,str(p/'run_all.py')],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',**(env or {})),capture_output=True,text=True)
    ok=(run.returncode==0) if accept else (run.returncode!=0 and expected in run.stderr)
    records.append({'name':name,'pass':ok,'code':run.returncode,'expected':expected,'stderr':run.stderr,'stdout':run.stdout})
    if not ok:raise RuntimeError(records[-1])
def changed(p): (p/'support_slit.tex').write_text((p/'support_slit.tex').read_text()+'\n% mutation\n')
case('outer_payload_changed',changed,'Payload mismatch: support_slit.tex')
case('extra_jsonl',lambda p:(p/'unexpected.jsonl').write_text('{}\n'),'Inventory mismatch')
case('missing_gitignore',lambda p:(p/'reviews/source01/.gitignore').unlink(),'Inventory mismatch')
case('source_pdf_added',lambda p:(p/'third_party.pdf').write_bytes(b'%PDF fake'),'Inventory mismatch')
case('symlink',lambda p:(p/'linked.md').symlink_to(p/'README.md'),'Unexpected symlink')
def innerbad(p):
    n='reviews/priority05_friedland1977/MANIFEST.json';x=json.loads((p/n).read_text());x['files']['CHECKS.json']='0'*64;write(p/n,x);reseal_outer(p)
case('nested_seal_after_outer_reseal',innerbad,'Nested hash mismatch')
def registrybad(p):
    x=json.loads((p/'SEALS.json').read_text());x.pop();write(p/'SEALS.json',x);reseal_outer(p)
case('registry_disagreement',registrybad,'Nested seal registry disagrees')
def replayfalse(p):
    q=p/'root_reproduction/angle_distinction_results.json';x=json.loads(q.read_text());x['mutation_falsehood']=True;write(q,x);reseal_outer(p)
case('replayed_record_falsehood',replayfalse,'Replay mismatch')
def hfullfalse(p):
    q=p/'reviews/priority04_hib1996/CHECKS.json';x=json.loads(q.read_text());x['checks'][5]['evidence']['real']='64/65';write(q,x)
    reseal_inner_file(p,'reviews/priority04_hib1996/MANIFEST.json','CHECKS.json');reseal_outer(p)
case('H_full_record_same_count_falsehood',hfullfalse,'Replay mismatch: reviews/priority04_hib1996/checks.py')
def hsummaryfalse(p):
    q=p/'root_reproduction/priority04_checks_rerun.json';x=json.loads(q.read_text());x['all_pass']=False;write(q,x);reseal_outer(p)
case('H_stdout_summary_falsehood',hsummaryfalse,'Replay summary mismatch')
# source01 manifest format is distinct; use its actual record representation.
def stamp(p):
    q=p/'reviews/source01/SOURCE_BRIDGE_CHECKS.json';x=json.loads(q.read_text());x['checked_at_utc']='2000-01-01T00:00:00Z';write(q,x)
    seal=p/'reviews/source01/AUTHORED_MANIFEST.json';m=json.loads(seal.read_text());h=hashlib.sha256(q.read_bytes()).hexdigest()
    data=m.get('files',m.get('authored_files'))
    if isinstance(data,dict):
        rec=data['SOURCE_BRIDGE_CHECKS.json']
        if isinstance(rec,str):data['SOURCE_BRIDGE_CHECKS.json']=h
        else:rec['sha256']=h;rec['bytes']=len(q.read_bytes())
    else:
        for rec in data:
            if rec['path']=='SOURCE_BRIDGE_CHECKS.json':
                rec['sha256']=h
                for k in ['bytes','size_bytes','size']:
                    if k in rec:rec[k]=len(q.read_bytes())
    write(seal,m);reseal_outer(p)
case('sole_source_timestamp_normalization',stamp,'PASS',accept=True)
def mathfield(p):
    stamp(p);q=p/'reviews/source01/SOURCE_BRIDGE_CHECKS.json';x=json.loads(q.read_text());x['q_at_1']='-3/5';write(q,x)
    seal=p/'reviews/source01/AUTHORED_MANIFEST.json';m=json.loads(seal.read_text());data=m.get('files',m.get('authored_files'))
    # Restore only the relevant inner digest without changing the false field.
    if isinstance(data,dict):
        rec=data['SOURCE_BRIDGE_CHECKS.json'];h=hashlib.sha256(q.read_bytes()).hexdigest()
        if isinstance(rec,str):data['SOURCE_BRIDGE_CHECKS.json']=h
        else:
            rec['sha256']=h
            for k in ['bytes','size_bytes','size']:
                if k in rec:rec[k]=len(q.read_bytes())
    else:
        for rec in data:
            if rec['path']=='SOURCE_BRIDGE_CHECKS.json':
                rec['sha256']=hashlib.sha256(q.read_bytes()).hexdigest()
                for k in ['bytes','size_bytes','size']:
                    if k in rec:rec[k]=len(q.read_bytes())
    write(seal,m);reseal_outer(p)
case('source_math_field_not_normalized',mathfield,'Replay mismatch: reviews/source01/check_source_bridge.py')
def broaden_ignore(p):
    q=p/'JOBS.json';x=json.loads(q.read_text());x[0]['ignored_dynamic_fields']=['checks'];write(q,x);reseal_outer(p)
case('normalization_cannot_hide_math',broaden_ignore,'Unsupported replay normalization')
case('optimization_guard',lambda p:None,'Run without Python optimization',env={'PYTHONOPTIMIZE':'1'})

# Independent safety-parser controls; import only from an expendable extraction.
sys.path.insert(0,str(BASE));from integrity import safe_path
for n in ['../escape','/abs','a/../b','a\\b','a:b','a//b','./a','']:
    rejected=False
    try:safe_path(n)
    except RuntimeError:rejected=True
    if not rejected:raise RuntimeError('unsafe accepted '+repr(n))
    records.append({'name':'unsafe_path_'+repr(n),'pass':True})

result={'status':'PASS','mutation_controls':len(records),'records':records,'limits':'Controls test consistency and replay rejection on local copies; coherent replacement of scripts, expected outputs and all seals is not authenticated by these hashes.'}
write(HERE/'MUTATION_RESULTS.json',result)
print(json.dumps({'status':'PASS','mutation_controls':len(records)}))

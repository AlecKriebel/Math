"""Freeze only source/root/core byte references and already read expectations.
No editorial namespace access, project import, network, subprocess or science.
Writes exclusively new three initial JSON files in this owned audit namespace.
"""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import stat

N=Path(__file__).absolute().parent
P=N.parent.parent

def need(x,why):
    if not x:raise ValueError(why)

def descriptor(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def read(p):
    need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real source input');return p.read_bytes()

def namespace(root):
    need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary frozen namespace')
    fs,ds=[],[]
    def walk(d):
        with os.scandir(d) as entries:
            for e in entries:
                q=Path(e.path);r=q.relative_to(root).as_posix();m=q.lstat().st_mode
                if stat.S_ISDIR(m):ds.append(r);walk(q)
                else:need(stat.S_ISREG(m),'reject links/specials');fs.append(r)
    walk(root);return sorted(fs),sorted(ds)

def new(name,x):
    with (N/name).open('xb') as f:f.write((json.dumps(x,indent=2,sort_keys=True)+'\n').encode())

def main():
    clearance=P/'verification/root-clearance-23203732-20261115.json';rb=read(clearance)
    need(descriptor(rb)['SHA256']=='1bfac7edfb5ae34ba7c5c4d4078c025ee25bfc299d91c547702b15eca462eb09','actual root clearance')
    specs=[('source','papers/23203732/sources',101,18,'SOURCE_READY_SEAL.json','cf9ffb0b5f509af974aa3e7a368c2672e000f2665aecf772a0df57f658145287'),('scope','papers/23203732/reviews/scope',233,29,'FINAL_SEAL.json','c9ae1ef347f619ab7a45fa8374999c5e80129dd4900f1488a4e058df97fe8553'),('adversarial','papers/23203732/reviews/adversarial',159,20,'FINAL_SEAL.json','ac56647773baa8e66de655af3ce092457719d16d12012020c1f0f07d45520182'),('correction','verification/23203732-adversarial-custody-correction-sol-20261115',14,0,'FINAL_SEAL.json','fe806f3f32f50f344a66dfca9ae8ca4aa935fc0a2acec77e17af9da8890cc53e'),('root','papers/23203732/reviews/root',29,2,'FINAL_SEAL.json','fe0ff4985a2ece4f2af8890e5e62303d0abddab09921075823ef0fd4bcc65490')]
    files=[];extents=[]
    for kind,relative,count,dircount,seal,expected in specs:
        root=P/relative;fs,ds=namespace(root)
        need(len(fs)==count and len(ds)==dircount and descriptor(read(root/seal))['SHA256']==expected,'exact frozen '+kind)
        extents.append({'kind':kind,'path':str(root),'files':fs,'directories':ds})
        files.extend({'path':str(root/name),**descriptor(read(root/name))} for name in fs)
    oldoracle=P/'verification/supported-cycle-focal-production-preparation-sol-20261115/INPUT_ORACLE.json';ob=read(oldoracle)
    need(descriptor(ob)['SHA256']=='47bc490586bad56ea17ba6864b28a1fef0e34bd4d7a9a3e562f384146e9598ec','previously authenticated reference oracle')
    contract=P/'papers/23578142/reviews/editorial/PROTECTED_INPUTS.json'
    binding=next(r for r in json.loads(ob)['frozen_original_files'] if r['path']==str(contract))
    cb=read(contract);need(descriptor(cb)=={k:binding[k] for k in ('bytes','SHA256')},'same previously authenticated protected-input contract')
    old=json.loads(cb);core=old['core_files'];need(len(core)==18,'qualified core names')
    oldrows={r['path']:r for r in old['files']};cores=[]
    for path in core:
        b=read(Path(path));d=descriptor(b);helper=path==str(P/'scripts/checkpoint_subtree.py')
        expected='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0' if helper else oldrows[path]['SHA256']
        need(d['SHA256']==expected,'original17 or sole authorized405b helper')
        cores.append({'path':path,**d,'classification':'sole separately authorized405b helper' if helper else 'one of17 original core files'})
    files.extend(cores);files.append({'path':str(clearance),**descriptor(rb)})
    new('SOURCE_INPUTS.json',{'UTC':datetime.now(timezone.utc).isoformat(),'files':files,'namespaces':extents,'core_files':cores,'core_contract_reference':{'path':str(contract),**descriptor(cb)},'prior_authenticated_oracle_reference':{'path':str(oldoracle),**descriptor(ob)},'all_originals_read_by_reference_not_copied':True,'current_editorial_namespace_accessed':False,'prior_root_scientific_judgment_exposure':'informed audit, not scientifically blind'})
    own={}
    for q in [N/'INITIAL_EXPECTATIONS.md',N/'freeze_initial.py',*sorted((N/'private').rglob('*'))]:
        if q.is_file():own[q.relative_to(N).as_posix()]=descriptor(read(q))
    new('INITIAL_READ_RECEIPT.json',{'UTC':datetime.now(timezone.utc).isoformat(),'entire_actual_PDF_pages_read':6,'all_controlling_TeX_lines_read':198,'fresh_own_individual_rasters_viewed':6,'native_record_SOURCE_READY_README_DEPENDENCIES_root_clearance_full_root_proof_read':True,'root_proof_bytes':15654,'fresh_PDF_utility_exits':[0,0,0],'native_or_scientific_programmes_executed':0,'current_editorial_copy_config_code_results_read':False,'owned_read_inputs':own,'completion_percent_for_entire_fact_audit':45})
    new('INITIAL_SEAL.json',{'UTC':datetime.now(timezone.utc).isoformat(),'status':'FROZEN_INFORMED_SOURCE_EXPECTATIONS_BEFORE_WRITER_COPY_CODE_EXPOSURE','SOURCE_INPUTS':descriptor(read(N/'SOURCE_INPUTS.json')),'INITIAL_EXPECTATIONS':descriptor(read(N/'INITIAL_EXPECTATIONS.md')),'INITIAL_READ_RECEIPT':descriptor(read(N/'INITIAL_READ_RECEIPT.json')),'source_root_core_files':len(files),'frozen_namespaces':len(extents),'current_editorial_copy_or_results_exposed':False,'production_authority':False,'AA':None,'canonical_url':None})
    print(json.dumps({'status':'INITIAL_FROZEN_BEFORE_EDITORIAL_EXPOSURE','source_root_core_files':len(files),'namespaces':len(extents),'core':'17original+sole405b','root_science_exposure':'informed','current_editorial_exposure':False,'completion_percent_fact_audit':45},sort_keys=True))

if __name__=='__main__':main()

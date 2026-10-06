from pathlib import Path
import datetime, hashlib, json, os, zipfile
A=Path(__file__).resolve().parent;Q=A/'qualified_publication_package_v2';V1=A/'qualified_publication_package_v1'
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def entries(base,rows):
    seen=set()
    for e in rows:
        rel=Path(e['file']);p=base/rel
        require(not rel.is_absolute() and '..' not in rel.parts and e['file'] not in seen,'entry scope');seen.add(e['file'])
        require(p.is_file() and not p.is_symlink() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'entry pin '+str(rel))
    return len(seen)
f=Q/'private_notes/FROZEN_CANDIDATE_MANIFEST.json';m=Q/'PREPARATION_MANIFEST.json'
require(sha(f)=='673af544d918a9db7533e36135f7faf2192b2a4e22ba9cc292e093725abdc4dd','frozen pin')
require(sha(m)=='fcc73333912877ffa482ed482feafb52ef3a1046b1dcf1da3d428e32282b6c09','preparation pin')
fd=load(f);md=load(m);counts={'prepared':entries(Q,md['files']),'public':entries(Q,fd['public_files'])}
for e in md['intentional_control_symlinks']:
    p=Q/e['file'];require(p.is_symlink() and os.readlink(p)==e['target'] and e['intentional_negative_control'],'hostile fixture link')
require(md['frozen_candidate_manifest_sha256']==sha(f),'manifest binding')
counts['immutable_v1']=entries(V1,load(V1/'PREPARATION_MANIFEST.json')['files'])
same=['pr95_note.tex','pr95_note.pdf','verification/verify.py','verification/independent_checks.py','verification/root_lattice_check.py','PR95_PRIORITY_QUALIFICATION.md','LICENSE.txt']
for rel in same:require((Q/'publicfiles'/rel).read_bytes()==(V1/'publicfiles'/rel).read_bytes(),'math/disclosure unchanged '+rel)
require((Q/'zenodo-deposit.json').read_bytes()==(V1/'zenodo-deposit.json').read_bytes(),'metadata unchanged')
payload=load(Q/'publicfiles/PAYLOAD_MANIFEST.json');counts['payload']=entries(Q/'publicfiles',payload['files'])
with zipfile.ZipFile(Q/'publicfiles/pr95_support.zip') as z:
    expected={e['file']:e for e in payload['files']};expected['PAYLOAD_MANIFEST.json']={'bytes':(Q/'publicfiles/PAYLOAD_MANIFEST.json').stat().st_size,'sha256':sha(Q/'publicfiles/PAYLOAD_MANIFEST.json')}
    require(len(z.namelist())==len(expected) and set(z.namelist())==set(expected),'safe exact archive')
    for n,e in expected.items():
        require(not Path(n).is_absolute() and '..' not in Path(n).parts,'archive scope')
        b=z.read(n);require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'archive byte pin')
    counts['archive']=len(expected)
for label in ('assembled_run','clean_archive_run'):
    result=load(Q/'private_notes'/label/'results.json')
    require(result['status']=='PASS_EXACT_SPECIALIZATION' and len(result['runs'])==12,'fresh complete suite')
    for r in result['runs']:
        p=Q/'private_notes'/label/r['label']/'process.json';require(sha(p)==r['process_sha256'],'actual receipt pin')
        data=load(p);require(data['pid']>0 and data['exit_code']==r['exit_code']==(1 if r['negative'] else 0),'actual PID exit')
        for stream in ('stdout.bin','stderr.bin'):require(sha(p.parent/stream)==r[stream[:-4]+'_sha256'],'actual stream pin')
guards=load(Q/'private_notes/PAYLOAD_GUARD_CONTROLS.json')
negative=[r for r in guards['cases'] if r['case']!='positive']
positive=[r for r in guards['cases'] if r['case']=='positive']
require(guards['ancestor_rejects_both_modes_before_output'] is True and len(negative)==guards['hostile_cases']==14
        and len(positive)==guards['positive_guard_cases']==2,'hostile scope')
require({(r['case'],r['optimized']) for r in negative}=={(n,b) for n in ['missing','changed','leaf_symlink','ancestor_symlink','unsafe','duplicate','ast_assertion'] for b in [False,True]},'both modes complete')
for r in negative:
    p=Q/r['process_file'];require(sha(p)==r['process_sha256'] and r['exit_code']==1 and r['output_created'] is False,'hostile receipt')
    process=load(p);require(process['pid']>0 and process['exit_code']==1,'hostile actual exit')
    require(r['explicit_error'] in (p.parent/'stderr.bin').read_text(),'hostile explicit cause')
processes={sha(p):p for p in (Q/'private_notes/processes').rglob('process.json')}
for r in positive:
    require(r['process_sha256'] in processes,'positive guard receipt')
    data=load(processes[r['process_sha256']]);require(data['pid']>0 and data['exit_code']==r['exit_code']==0,'positive guard actual exit')
dm=load(Q/'zenodo-deposit.json');pins=[]
for e in dm['files']:
    p=Q/e['path'];pins.append({'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
result={'schema':'pr95-root-corrected-candidate-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'actual_operator_PID':os.getpid(),'verified':True,'counts':counts,'R1_repair_authenticated':True,
 'hostile_guard_rejections':14,'frozen_manifest_sha256':sha(f),'preparation_manifest_sha256':sha(m),
 'upload_pins':pins,'priority_clearance':False,'publication_clearance':False,
 'root_authentication_harness_correction':'Initial strict check counted16 cases as14; the declared set contains14 hostile and2 positive probes. Captured failed audit retained; corrected partition authenticates actual evidence without rerunning science.',
 'new_second_whole_package_review_active':True}
(A/'ROOT_REPAIRED_CANDIDATE_AUTHENTICATION_20261005.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='upload_pins'}))

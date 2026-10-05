from pathlib import Path
import datetime, hashlib, json, os, zipfile

A=Path(__file__).resolve().parent
Q=A/'qualified_publication_package_v1'
D=A/'root_qualified_candidate_authentication_20261005'
D.mkdir(exist_ok=False)
checks=[]
def require(ok, message):
    if not ok: raise RuntimeError(message)
    checks.append(message)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def verify_entries(base, entries):
    seen=set()
    for e in entries:
        rel=Path(e['file']);p=base/rel
        require(not rel.is_absolute() and '..' not in rel.parts, 'safe '+str(rel))
        require(e['file'] not in seen, 'unique '+str(rel));seen.add(e['file'])
        require(p.is_file() and not p.is_symlink(), 'file '+str(rel))
        require(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'], 'pin '+str(rel))
    return len(seen)
frozen=Q/'private_notes/FROZEN_CANDIDATE_MANIFEST.json'
prep=Q/'PREPARATION_MANIFEST.json'
require(sha(frozen)=='7391bd4c70a8c51518aa8d28cf9d9320273e9bcdd462726680338f8fb083e963','frozen manifest')
require(sha(prep)=='de851339009ddf3914cadc823d3499f011148244a310cb3a7c9124ac033d24b7','preparation manifest')
fd=load(frozen);pd=load(prep)
counts={'prepared':verify_entries(Q,pd['files']), 'public':verify_entries(Q,fd['public_files']),
        'author_inputs':verify_entries(A,load(Q/'private_notes/INPUTS.json')['inputs'])}
require(pd['frozen_candidate_manifest_sha256']==sha(frozen),'frozen-preparation binding')
require(fd['priority_clearance'] is False and fd['publication_clearance'] is False,'candidate no clearance')
dm=Q/'zenodo-deposit.json';de=fd['deposit_manifest']
require(dm.stat().st_size==de['bytes'] and sha(dm)==de['sha256'],'deposit manifest pin')
meta=load(dm);uploads=[]
for e in meta['files']:
    p=Q/e['path'];require(p.is_file() and p.is_relative_to(Q/'publicfiles'),'owned upload')
    uploads.append({'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
require(len(uploads)==7 and len({e['file'] for e in uploads})==7,'seven unique uploads')
payload=load(Q/'publicfiles/PAYLOAD_MANIFEST.json')
counts['payload']=verify_entries(Q/'publicfiles',payload['files'])
with zipfile.ZipFile(Q/'publicfiles/pr95_support.zip') as z:
    expected={e['file']:e for e in payload['files']}
    expected['PAYLOAD_MANIFEST.json']={'sha256':sha(Q/'publicfiles/PAYLOAD_MANIFEST.json'),
        'bytes':(Q/'publicfiles/PAYLOAD_MANIFEST.json').stat().st_size}
    require(set(z.namelist())==set(expected) and len(z.namelist())==len(expected),'exact ZIP inventory')
    for name,e in expected.items():
        b=z.read(name);require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'ZIP '+name)
    counts['archive']=len(expected)
for name in ('assembled_final_run','clean_archive_run'):
    result=load(Q/'private_notes'/name/'results.json')
    require(result['status']=='PASS_EXACT_SPECIALIZATION','assembly PASS '+name)
    runs=result['runs'];require(len(runs)==12,'assembly twelve processes '+name)
    for r in runs:
        process=Q/'private_notes'/name/r['label']/'process.json'
        require(sha(process)==r['process_sha256'],'actual process pin '+name+'/'+r['label'])
        data=load(process)
        require(data['pid']>0 and data['exit_code']==r['exit_code'],'actual PID exit '+name+'/'+r['label'])
        require(r['exit_code']==(1 if r['negative'] else 0),'actual expected result '+name+'/'+r['label'])
        for stream in ('stdout.bin','stderr.bin'):
            require(sha(process.parent/stream)==r[stream[:-4]+'_sha256'],'actual stream '+name+'/'+r['label']+'/'+stream)
out={'schema':'pr95-root-candidate-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'operator_PID':os.getpid(),'status':'PASS_BYTE_AND_RECEIPT_AUTHENTICATION','counts':counts,
     'checks':len(checks),'frozen_manifest_sha256':sha(frozen),'preparation_manifest_sha256':sha(prep),
     'upload_pins':uploads,'worldwide_priority_established':False,'publication_clearance':False,
     'incidental_root_read_errors':'Two earlier reads used an incorrect manifest location; no scientific execution or candidate mutation occurred. Correct paths are private_notes/INPUTS.json and PREPARATION_MANIFEST.json at package root.'}
(D/'RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['upload_pins','incidental_root_read_errors']}))

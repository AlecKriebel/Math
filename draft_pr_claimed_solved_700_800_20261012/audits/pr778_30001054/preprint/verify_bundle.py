"""Offline exact finite replication and custody; no formal topology or priority proof."""
from pathlib import Path
import argparse, hashlib, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
from build_package import (METADATA, PREFIX, PIN, REVIEW_PINS, identity, safe_name,
                           require, regular, inventory, review_entries, priority_scope)
ROOT = Path(__file__).resolve().parent

def unique(pairs):
    out = {}
    for key,value in pairs:
        require(key not in out, 'Duplicate JSON key')
        out[key] = value
    return out

def read_json(raw):
    def reject(value):
        raise ValueError('Nonfinite JSON constant: '+value)
    return json.loads(raw.decode('utf-8'), object_pairs_hook=unique, parse_constant=reject)

def validate_closed_map(actual):
    require(type(actual) is dict and all(type(k) is str and type(v) is bytes for k,v in actual.items()),
            'Invalid byte mapping')
    manifest = read_json(actual['MANIFEST.json'])
    require(type(manifest) is dict and set(manifest)=={'schema','scope','files'}
            and manifest['schema']=='sha256-exact-file-inventory-v1'
            and type(manifest['scope']) is str and type(manifest['files']) is list,
            'Invalid manifest shape')
    listed = {}
    for row in manifest['files']:
        require(type(row) is dict and set(row)=={'path','bytes','sha256'}, 'Invalid file record')
        name = safe_name(row['path'])
        require(name not in listed and name != 'MANIFEST.json', 'Duplicate/self manifest path')
        require(type(row['bytes']) is int and row['bytes']>=0, 'Invalid byte count')
        require(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,
                'Invalid SHA256 grammar')
        listed[name] = {k:row[k] for k in ('bytes','sha256')}
    require(set(actual)==set(listed)|{'MANIFEST.json'}, 'Missing/extra source file')
    for name,record in listed.items():
        require(identity(actual[name])==record, 'Source content mismatch: '+name)
    return actual

def read_closed(root):
    return validate_closed_map(inventory(root))

def check_structure(before, pdf):
    require(read_json(before['zenodo-metadata.json'])=={'metadata':METADATA}, 'Metadata differs')
    priority_scope(read_json(before['audit/PRIORITY_GATE.json']))
    bindings = read_json(before['PREPRINT_BINDINGS.json'])
    require(identity(before['paper.tex'])==bindings['paper.tex'], 'TeX binding differs')
    if pdf is not None:
        require(identity(regular(pdf))==bindings['paper.pdf'], 'PDF binding differs')
    prefix='audit/original/'+PREFIX
    require(identity(before[prefix+'PUBLICATION_MANIFEST.json'])['sha256']==PIN, 'Original manifest pin')
    snapshot=read_json(before['audit/SNAPSHOT.json'])
    require(len(snapshot['files'])==32, 'Original count')
    expected={}
    for row in snapshot['files']:
        require(row['path'].startswith(PREFIX), 'Wrong original problem')
        name=safe_name(row['path'][len(PREFIX):])
        require(name not in expected, 'Duplicate original path')
        expected[name]={k:row[k] for k in ('bytes','sha256')}
        require(identity(before[prefix+name])==expected[name], 'Frozen original changed')
    require({n[len(prefix):] for n in before if n.startswith(prefix)}==set(expected), 'Original closure')
    require(identity(before[prefix+'audit/SCOPE_CORRECTION.md'])['sha256']==bindings['scope_correction_sha256'],
            'Scope-correction binding')
    require(identity(before[prefix+'audit/WITNESS.json'])['sha256']==bindings['witness_sha256'], 'Witness binding')
    for family,pin in REVIEW_PINS.items():
        prefix='audit/'+family+'/'
        raw=before[prefix+'MANIFEST.json']
        require(identity(raw)['sha256']==pin, 'Closed review manifest pin: '+family)
        names=set()
        for row in review_entries(read_json(raw)):
            name=safe_name(row['path'])
            require(name not in names and name!='MANIFEST.json','Duplicate/self review path')
            names.add(name)
            require(identity(before[prefix+name])=={k:row[k] for k in ('bytes','sha256')},'Closed review bytes')
        require({n[len(prefix):] for n in before if n.startswith(prefix)}==names|{'MANIFEST.json'},
                'Closed review inventory')
    source=before['audit/private_sources/selected_record.json']
    require(identity(source)['sha256']=='7a1d26575554344c3033d03813d55f3b249a09775c667fa38bc06be93d2b85d1',
            'Selected source bytes')
    selected=read_json(source)
    canonical=hashlib.sha256(json.dumps([selected['problem'],selected['prior_research']],sort_keys=True).encode()).hexdigest()
    require(canonical=='51710cccfe6bcd44ff5a8bd2b663db2387edbf19169806cfc0c1855f24822377',
            'Canonical full source/research identity')

# Expected exact stdout from independently executed closed scripts; no floats or timestamps.
# Original/combinatorial scripts internally cover both normal and optimized operation.
RUNS = [
 ('audit/original/'+PREFIX+'verify_publication.py',['--manifest-sha256',PIN],
  '2803b91e553ab7817f6dea2db249fade1b49e6fb1bce25694a3e8b2a38ad25f0',None),
 ('audit/review_combinatorial_family/replicate.py',[],
  '1bcaf24d8d8e188db0d2b919450fbbfae05020c708ee2de1aaef884e41f85c6a',None),
 ('audit/review_combinatorial_family/check_adjacent_inputs.py',[],
  'e48043015568d4520b61bbfa528f54c8610abb57f95f81dd62b00c586ff6dc0e',None),
 ('audit/review_geometric_family/verify_packet.py',['--current-inputs'],
  'add91079d71e5f3fc0c40ff6ed471a28f64ddecd25b43c323dff986ac0f1a238',None),
 ('audit/review_geometric_family/check_geometric.py',[],
  'f40c3775cb8d8eee019b4ebb17f186c4ce0575a5b455260772a1c530c717a9d7',None),
 ('audit/priority_audit/verify_custody.py',['--manifest-sha256',REVIEW_PINS['priority_audit'],'--inputs'],
  'b5b04aadee0438fa3bc88d1aaca48486038a1868c96dd358be45ec7ea7b12650',
  '044ee70c5d96dbee182b131314987988a37aef3d339d0834c8784b09135835c1'),
 ('audit/priority_adversary01/verify_custody.py',['--manifest-sha256',REVIEW_PINS['priority_adversary01']],
  '5e9607115453f47ad96d5ee06bb105c524ea6a822f87c423ac15e736c5b55e22',None),
 ('audit/priority_adversary01/check_current_inputs.py',[],
  '8921195ae28e7588497484462fd19988983450f3050c8097df4c061a94ef5c6c',None),
 ('audit/priority_adversary01/check_event_mapping.py',[],
  'bc155fbf05822591dbeb6c71094f22da4c14862e805a4845102ec23cff05098a',None),
 ('audit/priority_adversary01/test_custody.py',[],
  '89c5ec31c5af60b9c3c84add32aefdd7297f3bbd9534de6e43e640d4d49bda76',None),
]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--integrity-only',action='store_true')
    ap.add_argument('--pdf',type=Path,help='Optional exact published PDF; read only')
    args=ap.parse_args()
    before=read_closed(ROOT)
    check_structure(before,args.pdf)
    result={'status':'PASS','inventory_files':len(before),'original_files':32,
            'outer_optimization':sys.flags.optimize,'pdf_binding_checked':bool(args.pdf),
            'scope':'Exact finite checks/custody; no formal general proof, topology or exhaustive priority certificate.'}
    if not args.integrity_only:
        env=os.environ.copy()
        for key in ('PYTHONOPTIMIZE','PYTHONPATH','PYTHONHOME'):
            env.pop(key,None)
        rows=[]
        for opt in (False,True):
            for script,arguments,normal,optimized in RUNS:
                command=[sys.executable,'-E','-s','-B']+(['-O'] if opt else [])+[str(ROOT/script)]+arguments
                proc=subprocess.run(command,env=env,cwd='/',capture_output=True,timeout=300)
                require(proc.returncode==0,'Replay failed: '+script+': '+proc.stderr.decode(errors='replace'))
                actual=hashlib.sha256(proc.stdout).hexdigest()
                require(actual==((optimized or normal) if opt else normal),'Exact replay output differs: '+script)
                read_json(proc.stdout)
                rows.append({'script':script,'mode':'optimized' if opt else 'normal','stdout_sha256':actual})
            proc=subprocess.run([sys.executable,'-E','-s','-B']+(['-O'] if opt else [])+[str(ROOT/'guard_controls.py')],
                                env=env,cwd='/',capture_output=True,timeout=60)
            require(proc.returncode==0,'Own guard controls failed: '+proc.stderr.decode(errors='replace'))
            controls=read_json(proc.stdout)
            require(controls['status']=='PASS' and controls['negative_controls']==14,'Own guard count')
        require(read_closed(ROOT)==before,'Replay altered closed authored files')
        result['replays']=rows
        result['guard_controls']={'positive':1,'negative':14,'modes':['normal','optimized']}
        result['temporary_fixture_note']='Declared tiny owned test fixtures are created and removed; authored input bytes/inventory unchanged before and after.'
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()

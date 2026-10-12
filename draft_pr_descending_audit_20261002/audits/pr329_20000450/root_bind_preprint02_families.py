"""External current binding of held independent geometry/kernel certificates."""
from root_submission_gate import A,Capture,inventory,load,pin,sha,utc
from pathlib import Path
import json,sys

assert __debug__ and sys.flags.optimize==0
F=A/'preprint_review_02/families';G=F/'geometry';K=F/'kernel'
snapshots={n:inventory(F/n) for n in ['geometry','kernel']}
gm=load(G/'EVIDENCE_MANIFEST.json');gs=load(G/'HOLD_SEAL.json')
assert pin(G/'EVIDENCE_MANIFEST.json')['sha256']==gs['manifest_sha256']
assert pin(G/'GEOMETRY_FAMILY_REPORT.md')['sha256']==gs['report_sha256']
assert pin(G/'SOURCE_ONLY_BASELINE.md')['sha256']==gs['baseline_sha256']
assert gm['excluded_self_referential_files']==['EVIDENCE_MANIFEST.json','HOLD_SEAL.json']
assert {x['path']:{k:x[k] for k in ['bytes','sha256']} for x in gm['files']}=={n:{k:e[k] for k in ['bytes','sha256']} for n,e in snapshots['geometry']['payloads'].items() if n not in gm['excluded_self_referential_files']}
km=load(K/'HOLD_INVENTORY.json');assert not km['publication_seal']
assert {n:e for n,e in snapshots['kernel']['payloads'].items() if n!='HOLD_INVENTORY.json'}==km['files']
assert {n:e for n,e in snapshots['kernel']['directory_modes'].items() if n!='.'}==km['directory_modes']
bf=load(K/'baseline-freeze.json');assert not bf['candidate_read_before_freeze']
for n,h in bf['sha256'].items():assert pin(K/n)['sha256']==h
gb=load(G/'BASELINE_FREEZE.json');assert not gb['candidate_read_before_freeze']
assert gb['baseline_sha256']==pin(G/'SOURCE_ONLY_BASELINE.md')['sha256']

def frames(b):
    text=b.decode();decoder=json.JSONDecoder();out=[]
    while text.strip():
        value,i=decoder.raw_decode(text.lstrip());out.append(value);text=text.lstrip()[i:]
    return out
def scientific(b,kind):
    if kind=='UTC_LINES':return b'\n'.join(x for x in b.splitlines() if not x.startswith((b'UTC_START ',b'UTC_END ')))+b'\n'
    if kind=='JSON_UTC':
        objects=frames(b)
        assert 'utc' in objects[0];del objects[0]['utc']
        return (json.dumps(objects,sort_keys=True,separators=(',',':'))+'\n').encode()
    return b

specs=[('geometry','geometry_v01','preprint02_geometry_root001','UTC_LINES'),
    ('geometry','boundary_v01','preprint02_boundary_root001','UTC_LINES'),
    ('geometry','tate_discriminant_v01','preprint02_tate_discriminant_root001','UTC_LINES'),
    ('kernel','kernel_exact_v01','preprint02_kernel_root001','JSON_UTC'),
    ('kernel','map_boundaries_v03','preprint02_kernel_map_root001','BYTES'),
    ('kernel','finite_direct_v01','preprint02_kernel_finite_root001','BYTES'),
    ('kernel','extra_exact_v02','preprint02_kernel_extra_root001','BYTES'),
    ('kernel','public_consistency_v01','preprint02_kernel_export_root001','JSON_UTC')]
comparisons=[]
for family,label,rootname,kind in specs:
    d=F/family
    if family=='geometry':
        old=load(d/(label+'.receipt.json'));oldout=(d/(label+'.stdout.txt')).read_bytes();olderr=(d/(label+'.stderr.txt')).read_bytes()
        assert old['stdout_utf8'].encode()==oldout and old['stderr_utf8'].encode()==olderr
        assert old['exit_code']==0 and old['utc_start']<=old['utc_end']
    else:
        d=d/'native'/label;old=load(d/'execution.json');oldout=(d/'stdout.bin').read_bytes();olderr=(d/'stderr.bin').read_bytes()
        assert sha(oldout)==old['stdout_sha256'] and sha(olderr)==old['stderr_sha256']
        assert old['exit_code']==0 and old['started_utc']<=old['ended_utc']
    r=A/'root_runs_private'/rootname;new=load(r/'execution.json');newout=(r/'stdout.bin').read_bytes();newerr=(r/'stderr.bin').read_bytes()
    assert olderr==newerr==b'' and new['exit_code']==0
    program=Path(new['programs'][0]['path']);assert new['programs'][0]['sha256']==pin(program)['sha256']
    if family=='geometry':assert old['input_file_sha256'][str(program)]==pin(program)['sha256']
    else:assert old['body_sha256']==pin(program)['sha256']
    assert scientific(oldout,kind)==scientific(newout,kind),(family,label)
    comparisons.append(dict(family=family,label=label,normalization=kind,only_omitted_metadata='UTC_START/UTC_END lines' if kind=='UTC_LINES' else 'first JSON object utc key' if kind=='JSON_UTC' else 'none',complete_scientific_bytes_equal=True,scientific_sha256=sha(scientific(newout,kind)),original_actual_execution=old,root_actual_execution=new))

failures={'map_boundaries_v01':('map_boundary_exact.failed_v01.py','AssertionError: x=0 positive-v infinity slope is r/delta'),
    'map_boundaries_v02':('map_boundary_exact.failed_v02.py','AssertionError: x=0 positive-v infinity slope is -r/delta'),
    'extra_exact_v01':('extra_exact_checks.failed_v01.py',"AttributeError: 'int' object has no attribute 'subs'")}
actual=[]
for p in sorted((K/'native').glob('*/execution.json')):
    rec=load(p);out=(p.parent/'stdout.bin').read_bytes();err=(p.parent/'stderr.bin').read_bytes()
    assert rec['started_utc']<=rec['ended_utc'] and rec['cwd']==str(K)
    assert sha(out)==rec['stdout_sha256'] and sha(err)==rec['stderr_sha256']
    name=p.parent.name
    if name in failures:
        file,error=failures[name];assert rec['exit_code']==1 and error in err.decode()
        assert rec['body_sha256']==pin(K/file)['sha256']
    else:assert rec['exit_code']==0
    if rec.get('body_sha256'):
        candidates=[f for f in K.glob('*.py') if pin(f)['sha256']==rec['body_sha256']]
        assert candidates,(name,'missing exact executed body')
    actual.append(dict(label=name,record=rec))
assert len(actual)==19

# Compare the geometry export records to the current actual original/public bytes.
import difflib
export=load(G/'export_binding.json')
for e in export.values():
    old=Path(e['original_path']);new=Path(e['exported_path']);ob=old.read_bytes();nb=new.read_bytes()
    assert sha(ob)==e['original_sha256'] and len(ob)==e['original_bytes']
    assert sha(nb)==e['exported_sha256'] and len(nb)==e['exported_bytes']
    assert e['full_diff']==''.join(difflib.unified_diff(ob.decode().splitlines(True),nb.decode().splitlines(True),fromfile=str(old),tofile=str(new)))

cap=Capture('preprint02_family_external')
for name,snapshot in snapshots.items():
    d=F/name
    run=cap.run(name+'_hashes',['/usr/bin/shasum','-a','256',*snapshot['payloads']],cwd=d)
    assert run.stdout.decode()==''.join(e['sha256']+'  '+n+'\n' for n,e in snapshot['payloads'].items())
    names=sorted(list(snapshot['payloads'])+list(snapshot['directory_modes']))
    run=cap.run(name+'_modes',['/usr/bin/stat','-f','%N|%HT|%OLp|%z',*names],cwd=d)
    lines=run.stdout.decode().splitlines();assert len(lines)==len(names)
    for n,line in zip(names,lines):
        rel,kind,mode,size=line.split('|');assert rel==n
        if n in snapshot['payloads']:
            e=snapshot['payloads'][n];assert kind=='Regular File' and int(size)==e['bytes'] and int(mode,8)==int(e['mode'],8)
        else:assert kind=='Directory' and int(mode,8)==int(snapshot['directory_modes'][n],8)
    assert inventory(d)==snapshot
record=dict(utc=utc(),status='PASS_ROOT_CURRENT_HELD_GEOMETRY_AND_KERNEL_FAMILIES_AND_EIGHT_COMPLETE_SCIENTIFIC_REPLAYS',
    namespaces=snapshots,root_actual_native_hash_mode_captures=cap.entries,scientific_comparisons=comparisons,actual_kernel_receipts=actual,
    root_read_scope='Entire geometry24544/kernel22100 reports, both source-only baselines and bindings/hold/logs, eight scientific/consistency bodies plus receipt drivers and full failed-to-corrected diffs; complete root scientific outputs; nineteen actual kernel native records and all three full failures; geometry process/body metadata, full export diffs and HTTP trace fields. Original source/current candidate PDFs match previously root-visually-read bytes.',
    boundary_counterexample='Allowed lambda=-(13+5sqrt(5))/2 has lambda+c=-1. Two distinct residual fifth-torsion normalization points map to each plane vertex; exact rational/branch/kernel factors and independent p101/lambda83 five collisions reproduce. No25-distinct-plane-image claim is made.',
    evidence_boundaries=['Fresh family source-first baselines were hash-recorded before their candidate reading; they were not independently root-sealed entire namespaces at that earlier time. The parent whole-preprint reviewer has separately root-native frozen source-only and first-assessment namespaces before respective releases.',
      'Geometry family historical inventory omits modes and directories; these are independently root-native bound now, without asserting historical mode attestation. Kernel held inventory includes file/directory modes but omits the root directory mode, now bound.',
      '14571-character public TLS certificate trace text in geometry retrieval stdout was body/equality/hash bound, not semantically certificate-inspected. All HTTP metadata and mathematical outputs were read.'],
    assigned_combined_geometry_and_kernel_scope_complete=True,full_preprint_review_complete=False,publication_clearance=False)
out=A/'ROOT_PREPRINT02_FAMILIES_GATE.json';assert not out.exists();out.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(dict(utc=record['utc'],status=record['status'],namespaces={n:dict(files=len(e['payloads']),directories=len(e['directory_modes'])) for n,e in snapshots.items()},complete_scientific_replays=len(comparisons),actual_kernel_receipts=len(actual),gate_sha256=sha(out.read_bytes()),publication_clearance=False),indent=2))

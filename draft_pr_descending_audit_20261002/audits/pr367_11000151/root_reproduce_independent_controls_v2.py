"""Root replay of immutable, independent PR367 controls, in fresh private copies.

All replayed program sources were read in full before this program was created.
Only each control's expressly generated UTC is normalized; every other value
and every complete finite action record is compared without truncation.
"""
from pathlib import Path
from datetime import datetime, timezone
import fnmatch, gzip, hashlib, json, shutil, subprocess, sys

A=Path(__file__).resolve().parent
PRIVATE=A/'root_family_replay_private_02'
STREAMS=A/'root_family_control_streams_02'
assert not PRIVATE.exists() and not STREAMS.exists(), 'fresh run namespace required'
PRIVATE.mkdir(); STREAMS.mkdir()
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
checks=[]; commands=[]
def check(condition,label):
    assert condition,label
    checks.append({'check':label,'pass':True})
def load(p): return json.loads(p.read_bytes())
def binding(p,n,s,label):
    b=p.read_bytes();check(len(b)==n and sha(b)==s,label);return b
def manifest(family,name,digest,exclusions):
    d=A/family;p=d/name
    check(sha(p.read_bytes())==digest, family+' literal sealed manifest')
    m=load(p);rows=m['files'];expected={r['path'] for r in rows}
    check(len(expected)==len(rows),family+' unique binding paths')
    actual={str(p.relative_to(d)) for p in d.rglob('*') if p.is_file()
            and not any(fnmatch.fnmatch(str(p.relative_to(d)),pattern) for pattern in exclusions)}
    check(actual==expected,family+' complete closed public inventory')
    for r in rows:binding(d/r['path'],r['bytes'],r['sha256'],family+' entire bound file '+r['path'])
    return m
configs=[
 ('group_presentations_review','PUBLIC_MANIFEST.json','e3685edb5ddcddca42d8590fcda5d1b8673f92dcb36b8e97a67456aff9d88638',
  ['PUBLIC_MANIFEST.json','primary_sources/*','private_streams/*','private_tmp/*','receipts/API_*.json']),
 ('mapping_class_geometry_review','PUBLIC_MANIFEST.json','f60145d44f73e872274c46df6017603a2aebe767f349d48b291a80973db77193',
  ['PUBLIC_MANIFEST.json','FINAL_SEAL.json','private/*']),
 ('clean_final_adversary','PUBLIC_MANIFEST.json','94c21d0e9c753b69d3acab6967ce1330e26462fa496305852799499f60f17129',
  ['PUBLIC_MANIFEST.json','private_sources/*','private_runtime/*','__pycache__/*','final_live/*','post_merge/*']),
 ('priority_audit','IMMUTABLE_MANIFEST.json','645622f50f871637c89f683a88771c24f049f9c98f91d8c97afc7a1c4237ef88',
  ['IMMUTABLE_MANIFEST.json','private/*'])]
started=utc()
manifests={f:manifest(f,n,h,e) for f,n,h,e in configs}
for family in ('clean_final_adversary',):
    for row in load(A/family/'FINAL_SEAL.json')['sealed_artifacts']:
        binding(A/family/row['path'],row['bytes'],row['sha256'],family+' final seal '+row['path'])
geo=load(A/'mapping_class_geometry_review/FINAL_SEAL.json')['public_manifest']
binding(A/'mapping_class_geometry_review'/geo['path'],geo['bytes'],geo['sha256'],'geometry separately self-excluded final seal')
def copy_program(family,name):
    d=PRIVATE/family;d.mkdir(exist_ok=True)
    for sub in ('receipts','fullstreams','private_tmp'): (d/sub).mkdir(exist_ok=True)
    source=A/family/name;destination=d/name;shutil.copyfile(source,destination)
    check(destination.read_bytes()==source.read_bytes(),'exact pre-read private copy '+family+'/'+name)
    return destination
def execute(label,program):
    start=utc();p=subprocess.run([sys.executable,str(program)],capture_output=True);end=utc()
    row={'label':label,'program':str(program.relative_to(PRIVATE)) if program.is_relative_to(PRIVATE) else str(program.relative_to(A)),
         'program_sha256':sha(program.read_bytes()),'started_utc':start,'finished_utc':end,'exit':p.returncode}
    for channel,b in (('stdout',p.stdout),('stderr',p.stderr)):
        stored=STREAMS/(label+'.'+channel+'.gz');stored.write_bytes(gzip.compress(b,mtime=0))
        check(gzip.decompress(stored.read_bytes())==b,label+' complete '+channel+' lossless retention')
        row[channel]={'path':str(stored.relative_to(A)),'raw_bytes':len(b),'raw_sha256':sha(b),
                      'stored_bytes':stored.stat().st_size,'stored_sha256':sha(stored.read_bytes())}
    commands.append(row);check(p.returncode==0 and p.stderr==b'',label+' successful empty-error replay')
    return p.stdout,row
def compare_json(actual,expected,row,label):
    left=json.loads(json.dumps(actual));right=json.loads(json.dumps(expected))
    if 'utc' in left or 'utc' in right:
        check('utc' in left and 'utc' in right,label+' both literal UTC fields')
        t=datetime.fromisoformat(left.pop('utc'))
        check(datetime.fromisoformat(row['started_utc'])<=t<=datetime.fromisoformat(row['finished_utc']),label+' generated UTC lies inside replay')
        datetime.fromisoformat(right.pop('utc'))
    check(left==right,label+' complete structured output equality')
# The control alone needs the unchanged candidate C++ source at its documented relative path.
cpp=PRIVATE/'snapshot/problems/11000151_artin_a5_quotient/check_turn_4.cpp';cpp.parent.mkdir(parents=True)
source=A/'snapshot/problems/11000151_artin_a5_quotient/check_turn_4.cpp'
shutil.copyfile(source,cpp);check(cpp.read_bytes()==source.read_bytes(),'exact original candidate C++ copy for independent comparison')
program=copy_program('group_presentations_review','independent_finite_controls.py')
out,row=execute('group_finite',program)
actual=load(program.parent/'receipts/INDEPENDENT_FINITE_CONTROLS.json')
compare_json(actual,load(A/'group_presentations_review/receipts/INDEPENDENT_FINITE_CONTROLS.json'),row,'independent ranks1..6 and810 F4 actions')
# Six compact rank lines precede the complete final JSON; check all, in order.
lines=out.decode().splitlines();rank_lines=[json.loads(line) for line in lines[:6]]
check(rank_lines==actual['ranks'],'all six rank stdout records match complete receipt')
check(json.loads('\n'.join(lines[6:]))==actual,'complete final stdout JSON matches file')
for rank in range(1,7):
    name=f'rank{rank}_all_coaccessible_actions.txt'
    check((program.parent/'private_streams'/name).read_bytes()==gzip.decompress((A/'group_presentations_review/private_streams'/(name+'.gz')).read_bytes()),'every complete independent rank'+str(rank)+' action byte')
check((program.parent/'private_streams/all_810_F4_actions.jsonl').read_bytes()==gzip.decompress((A/'group_presentations_review/private_streams/all_810_F4_actions.jsonl.gz').read_bytes()),'all810 full F4 action records exact bytes')
out,row=execute('group_negative',copy_program('group_presentations_review','negative_merging_control.py'))
compare_json(json.loads(out),load(A/'group_presentations_review/receipts/NEGATIVE_MERGING_CONTROL.json'),row,'negative equal-count noncoaccessible collision')
for name in ('geometry_controls','postseal_geometry_controls','independent_f4_reduction'):
    out,row=execute(name,copy_program('mapping_class_geometry_review',name+'.py'))
    expected=(A/'mapping_class_geometry_review'/(name+'.json')).read_bytes()
    check(out==expected,name+' entire stdout byte equality')
    check((PRIVATE/'mapping_class_geometry_review'/(name+'.json')).read_bytes()==expected,name+' entire generated artifact byte equality')
program=copy_program('clean_final_adversary','independent_controls.py')
out,row=execute('whole_independent',program)
actual=json.loads(out);compare_json(actual,load(A/'clean_final_adversary/receipts/independent_controls.json'),row,'independent labeled-strand and reverse-DAG full receipt')
check(load(program.parent/'receipts/independent_controls.json')==actual,'whole exact stdout matches own generated receipt')
root_cpp=gzip.decompress((A/'root_original_streams_02/direct_CPP_full_state_stream.stdout.gz').read_bytes())
records=b''.join(line for line in root_cpp.splitlines(keepends=True) if line.startswith(b'S|'))
check(len(records)==15258431 and sha(records)=='af2b8ec569d613e4f3d8ba3b72d18e85e8c612f4265057b7f4c485d544d159bf','full root original CPP record bytes and independent known digest')
check(records==(PRIVATE/'group_presentations_review/private_streams/rank6_all_coaccessible_actions.txt').read_bytes(),'every90921 independently constructed group-family record equals root candidate record')
for p in [program.parent/'fullstreams/independent_backward_records.txt.gz',A/'clean_final_adversary/fullstreams/independent_backward_records.txt.gz']:
    check(gzip.decompress(p.read_bytes())==records,'every90921 full reverse-DAG record '+str(p.relative_to(A)))
for p in [A/'mapping_class_geometry_review/private/full_cpp_stream.stdout.gz']:
    check(gzip.decompress(p.read_bytes())==root_cpp,'every byte of geometry full candidate replay')
# Preserve complete independent outputs without holding uncompressed record files.
for p in sorted((PRIVATE/'group_presentations_review/private_streams').glob('*')):
    b=p.read_bytes();dest=STREAMS/('group_'+p.name+'.gz');dest.write_bytes(gzip.compress(b,mtime=0))
    check(gzip.decompress(dest.read_bytes())==b,'lossless full new group record storage '+p.name)
    p.unlink()
dest=STREAMS/'whole_independent_backward_records.txt.gz'
shutil.copyfile(program.parent/'fullstreams/independent_backward_records.txt.gz',dest)
check(gzip.decompress(dest.read_bytes())==records,'complete root independent backward record retention')
# Read-only whole auditor verifies all44 original execution output streams.
out,row=execute('whole_manifest_readonly',A/'clean_final_adversary/verify_audit.py')
check(out==b'PASS: complete self-excluded public audit, earlier/final seals and44 raw execution-output streams\n','whole auditor exact full output')
for r in load(A/'clean_final_adversary/receipts/replay_storage.json'):
    b=binding(A/'clean_final_adversary'/r['stored_path'],r['stored_bytes'],r['stored_sha256'],'whole full stored replay '+r['stored_path'])
    raw=gzip.decompress(b) if r['compression']=='gzip' else b
    check(len(raw)==r['complete_raw_output_bytes'] and sha(raw)==r['complete_raw_output_sha256'],'whole entire raw replay '+r['stored_path'])
out,row=execute('priority_quotient',copy_program('priority_audit','check_quotient_mapping.py'))
check(out==(A/'priority_audit/QUOTIENT_MAPPING_CHECK.json').read_bytes(),'priority identity complete exact replay')
for f,n,h,e in configs:manifest(f,n,h,e)
report={'status':'PASS','started_utc':started,'finished_utc':utc(),'checks':checks,'check_count':len(checks),
        'commands':commands,'manifest_binding_counts':{f:len(m['files']) for f,m in manifests.items()},
        'workflow_completion_percent':60,'original_discovery_completion_percent':0,
        'scope':'Exact frozen fixed-generator result. Root source/math baseline predates program reading/replay. Every full independent finite action record compared; no novelty certification.'}
(A/'root_family_reproduction_receipt.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','check_count':len(checks),'commands':len(commands),'binding_counts':report['manifest_binding_counts'],'workflow_completion_percent':60},indent=2))

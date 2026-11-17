"""Bind released current mutable pins first, then preserve immutable custody keys."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat
if not __debug__:
    raise RuntimeError('Checkpoint assertions must be enabled')
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'verification/checkpoint-native144-pentagonINITIAL-20261117'
CURRENT={'PROGRESS.json':(149353,'efe6261f60c64ad155ed566326671066515d557404052e3c0323a2339b2f4f75'),'RESEARCH_LOG.md':(285583,'3539bc34b0ab05ba993af73f6b28392841d64fff69ebd090e4ac71d5d2bb7901'),'.gitignore':(5640,'41e7201f34f6002c23d56834540e4e4c9b51fefa91c85ebecaad380d72af59ef')}
current_pins={}
for rel,(size,sha) in CURRENT.items():
    path=P/rel
    assert path.is_file() and not path.is_symlink(),rel
    raw=path.read_bytes()
    assert len(raw)==size and hashlib.sha256(raw).hexdigest()==sha,rel
    current_pins[rel]=dict(bytes=size,SHA256=sha)
old=json.loads((P/'verification/checkpoint-d4-pass144-20261117/ROOT_RELEASE.json').read_bytes())
roots={x['path']:dict(x) for x in old['durable_tree_roots']}
important=list(old['important_paths'])
pins=dict(old['expected_key_file_SHA256'])
for rel,pin in current_pins.items():
    pins[rel]=pin['SHA256']

def add(rel,files,dirs):
    root=P/rel
    assert root.is_dir() and not root.is_symlink(),rel
    count_f=count_d=0
    for here,ds,fs in os.walk(root):
        count_f+=len(fs);count_d+=len(ds)
        assert not any((Path(here)/n).is_symlink() for n in ds+fs),rel
    assert (count_f,count_d)==(files,dirs),(rel,count_f,count_d,files,dirs)
    roots[rel]=dict(path=rel,files=files,directories=dirs)

for spec in [('verification/checkpoint-d4-pass144-20261117',57,0),('verification/sheet-d4-pass144-20261117',9,0),('verification/mink-riesz-k3-postpublication-sol-20261117',22,0),('verification/thompson-cstar-corrected-fact-sol-20261117',19,0),('verification/d4-canonical-potential-editorial-sol-20261117',22,0),('papers/23137834/sources',97,7),('papers/23137834/reviews/root-initial-20261117',17,1)]:
    add(*spec)
initial=P/'papers/23137834/reviews/root-initial-20261117'
assert stat.S_IMODE(initial.stat().st_mode)==0o555
for item in initial.rglob('*'):
    assert stat.S_IMODE(item.stat().st_mode)==(0o555 if item.is_dir() else 0o444),str(item)
extra={'verification/checkpoint-d4-pass144-20261117/FINAL.json':'612433d7605755190ea276d9c56efae6555321af4e407a326d641b897dd58376','verification/checkpoint-d4-pass144-20261117/MANIFEST.json':'6292f30c19753691e4fed0628da9541e30994d504b38a2f82445d6a8868a710d','papers/23137834/reviews/root-initial-20261117/INITIAL_SEAL.json':'a47cd3a2b923f87c6479f17277aa3cd35e4ef3792e20a2a69a8be1623575632b','papers/23137834/reviews/root-initial-20261117/INITIAL_MANIFEST.json':'223215551a335131ef19947432afd1d9c614353882c1ae7bdbe2a772a5efee15','verification/mink-riesz-k3-postpublication-sol-20261117/FINAL.json':'94bb9973b6776b5c11b04ccba88315423905ff141b47959850de7e88100dd13d','verification/mink-riesz-k3-postpublication-sol-20261117/MANIFEST.json':'49eeee3592f6a89bf0d73625e9ff10af0c6e8d14f9c19a9643d29e25bfcc74d0'}
for rel,sha in extra.items():
    important.append(rel);pins[rel]=sha
for rel in ['verification/sheet-d4-pass144-20261117/FINAL_READBACK.json','verification/sheet-d4-pass144-20261117/SNAPSHOT_ENCODING.md','verification/sheet-d4-pass144-20261117/BEFORE_CELLS.packed.json','verification/sheet-d4-pass144-20261117/AFTER_CELLS.packed.json','verification/sheet-d4-pass144-20261117/BEFORE_METADATA.packed.json','verification/sheet-d4-pass144-20261117/AFTER_METADATA.packed.json','verification/sheet-d4-pass144-20261117/REQUESTS.json','verification/sheet-d4-pass144-20261117/MUTATION.json','verification/root-checkpoint-14013-adoption-20261117.json','verification/root-checkpoint-14013-adoption-first-failure-20261117.json','verification/root-mink-riesz-k3-postpublication-adoption-20261117.json','verification/root-thompson-cstar-editorial-adoption-20261117.json','reconciliation/current-native-queue-20261117-pass144-d4.json']:
    assert (P/rel).is_file(),rel
    important.append(rel)
controls=['SOURCE_FINAL.json','SOURCE_MANIFEST.json','INITIAL_SEAL.json','INITIAL_MANIFEST.json','FINAL.json','MANIFEST.json','OWNED_MANIFEST.json','FINAL_MANIFEST.json','FINAL_SEAL.json','SEAL.json']
for rel in roots:
    if rel not in old['immutable_packet_paths'] or rel=='verification/d4-canonical-potential-editorial-sol-20261117':
        for name in controls:
            if (P/rel/name).is_file():important.append(rel+'/'+name)
important=list(dict.fromkeys(important))
for rel in important:
    path=P/rel
    assert path.is_file() and not path.is_symlink(),rel
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    if rel in pins:assert pins[rel]==sha,rel
    else:pins[rel]=sha
active=['verification/d4-canonical-potential-editorial-v2-sol-20261117']
for rel in active:assert (P/rel).is_dir() and not (P/rel).is_symlink(),rel
release=dict(schema='explicit-root-native144-pentagonINITIAL-checkpoint-release-v1',UTC=datetime.now(timezone.utc).isoformat(),authorization='ROOT_RELEASE_TO_CHECKPOINT',expected_parent='14013a3a64b3beb7689a53d5551e9a9ca9a8d990',authorizing_agent='/root',root_P_W_writes_quiescent=True,current_mutable_pins_bound_before_inherited_metadata=current_pins,authorized_active_verification_paths=active,durable_tree_roots=list(roots.values()),immutable_packet_paths=list(roots),important_paths=important,expected_key_file_SHA256=pins,private_cache_paths=old['private_cache_paths'],scientific_reviewed=144,scientific_passes=136,scientific_deferred=8,scientific_remaining=59,total=203,native_Sheet_reviewed=144,programme_counts=dict(verified=123,deployed=10,preparing=3,under_review=7,queued=50,holds=2,deferred=8),programme_goal_active_incomplete=True,scientific_percent=144/203*100,pentagon_INITIAL=dict(files=17,directories=1,root_and_directories_mode='0555',files_mode='0444',original_only=True,no_verdict=True,root_completion_percent=35,scientific_program_runs=0),inclusion_updates=dict(frozen_postaudit22_included=True,frozen_corrected_fact19_included=True,failed_D4_editorial22_included=True,previous_checkpoint57_included=True,native_transition144_encoded_snapshots_included=True),expected_W_HEAD=old['expected_W_HEAD'],expected_W_tree=old['expected_W_tree'],expected_W_index_SHA256=old['expected_W_index_SHA256'],expected_W_index_bytes=old['expected_W_index_bytes'],expected_public_files=803,expected_public_child_directories=387,on_actual_failure='STOP retain literal streams/exits/timestamps; no automatic repair/retry',no_global_PROGRESS_or_programme_log_mutation=True)
with (OWN/'ROOT_RELEASE.json').open('x') as f:json.dump(release,f,indent=2);f.write('\n')
rows=[]
for name in ['construct_release.py','capture_guards.py','run_helper_once.py','git','inspect_checkpoint.py','seal_evidence.py','run_step.py']:
    raw=(OWN/name).read_bytes()
    rows.append(dict(path=name,bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),full_saved_source_personally_read_before_first_attempt=True))
h=(P/'scripts/checkpoint_subtree.py').read_bytes()
assert len(h)==6213 and hashlib.sha256(h).hexdigest()=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0'
with (OWN/'READ_ATTESTATION.json').open('x') as f:json.dump(dict(UTC=release['UTC'],fresh_sources=rows,authorized_helper=dict(bytes=len(h),SHA256=hashlib.sha256(h).hexdigest(),entire94line_source_personally_read_and_unchanged=True),no_old_publication_helper_execution_or_help=True,no_future_or_paper_exclusions=True),f,indent=2);f.write('\n')
with (OWN/'CHECKPOINT_LOG.md').open('a') as f:f.write('\n'+release['UTC']+' — Current mutable3 verified before inherited immutable pins; released metadata bound. Included original-only pentagonINITIAL17/1, native144 lossless packed snapshots, frozen postaudit22, correctedfact19, failedD4editorial22 and priorcheckpoint57. Only existing active D4V2 and own excluded. Sources fully saved/read. Checkpoint30%; scientific/native144/203=70.935961%; programme active/incomplete.\n')
print(json.dumps(dict(closed_roots=len(roots),key_files=len(important),active=active,private_cache_paths=len(old['private_cache_paths']),mutable3_exact=True,no_helper_Git_network_yet=True)))

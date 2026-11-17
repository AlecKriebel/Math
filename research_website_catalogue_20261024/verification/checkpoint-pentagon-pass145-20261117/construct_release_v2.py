"""Bind fresh released mutable pins, then preserve prior immutable evidence pins."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
if not __debug__:raise RuntimeError('Assertions must remain enabled')
M=Path('/Users/alec/Documents/Math');P=M/'research_website_catalogue_20261024'
OWN=P/'verification/checkpoint-pentagon-pass145-20261117'
current={'PROGRESS.json':(150305,'b494638fe5212cb5ff891ba84a350736dbb3c4d1b2d8934f6c30cf6b94360b63'),'RESEARCH_LOG.md':(286506,'4d374f193f01b930233c80e2de4e4703a96359c2f21875dac47ca2480bd3bf7f'),'.gitignore':(5785,'2681b39afa0f77c24233d87f5cac4555c61ff42bafbe7642c01d3c619a916cb4')}
current_pins={}
for rel,(size,digest) in current.items():
    p=P/rel;assert p.is_file() and not p.is_symlink();raw=p.read_bytes()
    assert len(raw)==size and hashlib.sha256(raw).hexdigest()==digest,rel
    current_pins[rel]=dict(bytes=size,SHA256=digest)
native_ignore=(M/'.gitignore').read_bytes()
assert len(native_ignore)==2540 and hashlib.sha256(native_ignore).hexdigest()=='6fdc9c60941d83bd2b81a1d082288f85f95ebd727fa7eff79bf66efeab1bdaa5'
old=json.loads((P/'verification/checkpoint-native144-pentagonINITIAL-20261117/ROOT_RELEASE.json').read_bytes())
roots={x['path']:dict(x) for x in old['durable_tree_roots']}
important=list(old['important_paths']);pins=dict(old['expected_key_file_SHA256'])
for rel,pin in current_pins.items():pins[rel]=pin['SHA256']
def add(rel,files,dirs):
    p=P/rel;assert p.is_dir() and not p.is_symlink(),rel
    nf=nd=0
    for here,ds,fs in os.walk(p):
        nf+=len(fs);nd+=len(ds)
        assert not any((Path(here)/x).is_symlink() for x in ds+fs),rel
    assert (nf,nd)==(files,dirs),(rel,nf,nd,files,dirs)
    roots[rel]=dict(path=rel,files=files,directories=dirs)
for spec in [('verification/checkpoint-native144-pentagonINITIAL-20261117',54,0),('papers/23137834/reviews/adversarial-sol',47,4),('papers/23137834/reviews/scope-sol',81,3),('papers/23137834/reviews/root-continuation-20261117',12,1),('papers/23137834/reviews/verdure-convention-challenge-sol-20261117',23,0),('verification/pentagon-root-custody-sol-20261117',10,0),('verification/d4-canonical-potential-editorial-v2-sol-20261117',30,1),('verification/d4-canonical-potential-editorial-fact-sol-20261117',16,0),('verification/d4-canonical-potential-legacy-sol-20261117',21,0),('verification/gram-thompson-d4-overlay-sol-20261117',41,6),('verification/pentagon-full-fifth-torsion-editorial-sol-20261117',19,1)]:add(*spec)
extra={'papers/23137834/reviews/root-continuation-20261117/ROOT_REVIEW.md':(15716,'acd210977221457737949db0684d2c60c289fef197b6b4dcaa26d87c8aa99599'),'verification/root-clearance-23137834-20261117.json':(2546,'55ea79efc35b209694e5afd51edd42ffa6994cb6ca755e83c981494b7e291951'),'verification/root-pentagon-final-evidence-adoption-20261117.json':(1965,'0de161432109b2f92b39edead5ec49b2c0a038f4b07232110ecf616e643362a1'),'verification/root-d4-canonical-potential-editorial-adoption-20261117.json':(2359,'4eb74780ca57774a77f0c8c0bbd116806bdb4ad36c1696714aa1c8e03a83c5b9'),'verification/root-checkpoint-b510-adoption-20261117.json':(1192,'5687006d05ac49e3684ed0599390a221e6e127cb1db2d554491c86af6f9cdb6c'),'verification/checkpoint-native144-pentagonINITIAL-20261117/FINAL.json':(720,'d426b0e904fb255c3c17ba06b9f6c14e4f8aeb8ac6dc7ca74ee625f109bdaeb5'),'verification/checkpoint-native144-pentagonINITIAL-20261117/MANIFEST.json':(12515,'8525bbd1850a9368bab192ec08fb3c68fb165abed434b326a1fdbdb5dca5b242'),'verification/pentagon-root-custody-sol-20261117/FINAL.json':(734,'956ecbede9184ad062e7ed5c0d1344e0f4ae8ddc3f8e5865fa76411f8872f43f'),'verification/pentagon-root-custody-sol-20261117/MANIFEST.json':(2347,'398874e6650d7d04c1062904be1791729be5ecfa17dc4210ed664b014417e89f'),'verification/pentagon-root-custody-sol-20261117/DATA_AUTHENTICATION.json':(176758,'d2b0802f2eedbc784c761a23e64243c864daab729b03998647249ea157d0a20e'),'verification/gram-thompson-d4-overlay-sol-20261117/FINAL.json':(1529,'a8a21cbbd909f13d44dfa1ba35a10758acad996a831eaa756d8f053f1bbd4762')}
extra.update({'verification/pentagon-full-fifth-torsion-editorial-sol-20261117/FINAL.json': (1972, '0c6838af4b2acf9065b89587f8701b692be78caf974b67e6e5dbb06899a713aa'), 'verification/pentagon-full-fifth-torsion-editorial-sol-20261117/FINAL_MANIFEST.json': (4483, 'e31cdbc3460f63e135e075fbb21bff87e72ae5cbbedb71ce222b822f29645584')})
for rel,(size,digest) in extra.items():
    p=P/rel;raw=p.read_bytes();assert len(raw)==size and hashlib.sha256(raw).hexdigest()==digest,rel
    important.append(rel);pins[rel]=digest
controls=['SOURCE_FINAL.json','SOURCE_MANIFEST.json','INITIAL_SEAL.json','INITIAL_MANIFEST.json','FINAL.json','FINAL.md','MANIFEST.json','MANIFEST.sha256','OWNED_MANIFEST.json','FINAL_MANIFEST.json','FINAL_SEAL.json','SEAL.json']
for rel in roots:
    if rel not in old['immutable_packet_paths']:
        for name in controls:
            if (P/rel/name).is_file():important.append(rel+'/'+name)
important=list(dict.fromkeys(important))
for rel in important:
    p=P/rel;assert p.is_file() and not p.is_symlink(),rel;digest=hashlib.sha256(p.read_bytes()).hexdigest()
    if rel in pins:assert pins[rel]==digest,rel
    else:pins[rel]=digest
active=['verification/gram-thompson-d4-overlay-audit-sol-20261117','verification/gram-thompson-d4-production-prepare-sol-20261117']
for rel in active:assert (P/rel).is_dir() and not (P/rel).is_symlink(),rel
caches=list(old['private_cache_paths'])+['papers/23137834/reviews/root-continuation-20261117/primary']
assert (P/caches[-1]).is_dir()
release=dict(schema='explicit-root-pentagon-pass145-native144-checkpoint-release-v1',UTC=datetime.now(timezone.utc).isoformat(),authorization='ROOT_RELEASE_TO_CHECKPOINT',expected_parent='b510aecb1a5ad89bc0efa0e2798aefa9f7a928c6',authorizing_agent='/root',root_P_W_writes_quiescent=True,current_mutable_pins_bound_before_inherited_metadata=current_pins,native_root_gitignore=dict(bytes=2540,SHA256=hashlib.sha256(native_ignore).hexdigest(),outside_programme_scope_preserve_only=True),authorized_active_verification_paths=active,durable_tree_roots=list(roots.values()),immutable_packet_paths=list(roots),important_paths=important,expected_key_file_SHA256=pins,private_cache_paths=caches,scientific_reviewed=145,scientific_passes=137,scientific_deferred=8,scientific_remaining=58,total=203,native_Sheet_reviewed=144,programme_counts=dict(verified=123,deployed=10,preparing=3,under_review=7,queued=50,holds=2,deferred=8),programme_goal_active_incomplete=True,scientific_percent=145/203*100,pentagon_INITIAL=old['pentagon_INITIAL'],inclusion_updates=dict(pentagon_current_root_PASS145_and_clearance_included=True,all_current_pentagon_frozen_families_challenge_custody_included=True,frozen_D4_writer30_fact16_legacy21_included=True,frozen_overlay41files6dirs_included=True,previous_checkpoint54_and_correct_root_adoption_included=True,frozen_pentagon_editorial19files1dir_included=True,administrative_preexecution_scope_V2=True),expected_W_HEAD=old['expected_W_HEAD'],expected_W_tree=old['expected_W_tree'],expected_W_index_SHA256=old['expected_W_index_SHA256'],expected_W_index_bytes=old['expected_W_index_bytes'],expected_public_files=803,expected_public_child_directories=387,on_actual_failure='STOP retain literal streams/exits/timestamps; no automatic repair/retry',no_global_PROGRESS_or_programme_log_mutation=True)
with (OWN/'ROOT_RELEASE.json').open('x') as f:json.dump(release,f,indent=2);f.write('\n')
rows=[]
for name in ['construct_release_v2.py','capture_guards.py','run_helper_once.py','git','inspect_checkpoint.py','seal_evidence.py','run_step.py']:
    raw=(OWN/name).read_bytes();rows.append(dict(path=name,bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),full_saved_source_personally_read_before_first_attempt=True))
h=(P/'scripts/checkpoint_subtree.py').read_bytes();assert len(h)==6213 and hashlib.sha256(h).hexdigest()=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0'
with (OWN/'READ_ATTESTATION.json').open('x') as f:json.dump(dict(UTC=release['UTC'],fresh_sources=rows,authorized_helper=dict(bytes=6213,SHA256=hashlib.sha256(h).hexdigest(),entire94line_source_personally_read_and_unchanged=True),no_old_publication_helper_execution_or_help=True,no_future_or_paper_exclusions=True),f,indent=2);f.write('\n')
with (OWN/'CHECKPOINT_LOG.md').open('a') as f:f.write('\n'+release['UTC']+' — Fresh programme mutable3 pins and separate nativeM ignore pin exact before inherited immutable assertions. Release metadata and full saved-source reading bound; only actual overlayauditor/productionprepare/own excluded; frozen pentagonwriter19/1 included. Earlier constructor/PLAN V1 retained unexecuted; root authorized administrative scope V2 before first invocation. No checker/helper/Git/network attempt yet. Checkpoint30%; scientific145/203=71.428571%, native144; programme active/incomplete.\n')
print(json.dumps(dict(closed_roots=len(roots),key_files=len(important),private_cache_paths=len(caches),active=active,current_pins_exact=True,no_helper_Git_network_yet=True)))

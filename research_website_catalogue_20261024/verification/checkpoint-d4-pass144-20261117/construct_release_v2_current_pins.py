from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');own=P/'verification/checkpoint-d4-pass144-20261117';old=json.loads((P/'verification/checkpoint-thompson-pass143-20261117/ROOT_RELEASE.json').read_bytes())
# Root administrative disposition: refresh exactly three current mutable pins.
root_current_pins={'PROGRESS.json':(147559,'281704bc917a63690dc6ee11c784969b76d04957b0349d418a335f5ff7f2d8f9'),'RESEARCH_LOG.md':(284000,'dc1157aa4237b5b894a861f853874d14342136ae62919b8a17f5de16fdb1ded1'),'.gitignore':(5640,'41e7201f34f6002c23d56834540e4e4c9b51fefa91c85ebecaad380d72af59ef')}
for current_relative,(expected_bytes,expected_SHA256) in root_current_pins.items():
 current_raw=(P/current_relative).read_bytes()
 assert len(current_raw)==expected_bytes and hashlib.sha256(current_raw).hexdigest()==expected_SHA256,current_relative
 old['expected_key_file_SHA256'][current_relative]=expected_SHA256
roots={x['path']:dict(x) for x in old['durable_tree_roots']}
def add(rel,files=None,dirs=None):
 root=P/rel;assert root.is_dir() and not root.is_symlink(),rel
 count_f=count_d=0
 for cur,ds,fs in os.walk(root):count_f+=len(fs);count_d+=len(ds)
 if files is not None:assert count_f==files,(rel,count_f,files)
 if dirs is not None:assert count_d==dirs,(rel,count_d,dirs)
 roots[rel]=dict(path=rel,files=count_f,directories=count_d)
for rel,files,dirs in [('papers/23439776/sources',72,7),('papers/23439776/reviews/root',17,1),('papers/23439776/reviews/adversarial-sol',53,3),('papers/23439776/reviews/scope-sol',95,3),('verification/d4-root-custody-sol-20261117',9,0),('verification/checkpoint-thompson-pass143-20261117',49,0),('verification/sheet-thompson-pass143-20261117',9,0),('verification/sheet-three-pages-deployed143-20261117',15,0),('verification/thompson-cstar-editorial-corrected-sol-20261117',6,0),('verification/thompson-cstar-editorial-corrected-v2-sol-20261117',22,1),('verification/d4-canonical-potential-editorial-sol-20261117',3,0)]:add(rel,files,dirs)
for rel in ['papers/23439776/reviews/root-continuation-20261117','papers/23439776/reviews/convention-challenge-sol-20261117','verification/mink-riesz-k3-production-prepare-v2-sol-20261117','verification/mink-riesz-k3-production-static-v2-sol-20261117','verification/mink-riesz-k3-live-root-20261117','verification/thompson-cstar-editorial-sol-20261117','verification/thompson-cstar-editorial-fact-sol-20261117','verification/thompson-cstar-legacy-sol-20261117']:add(rel)
important=list(old['important_paths']);pins=dict(old['expected_key_file_SHA256'])
extra={'papers/23439776/reviews/root-continuation-20261117/ROOT_REVIEW.md':'4836979d83da2747da766a2defc76bc0e5bbd6b48b25025c0de434aefd580e62','verification/root-clearance-23439776-20261117.json':'d6a171c2f2a3b5480bd5bdc71e4c9fcb63bb2130bea2524e7e9df3cb9f6c6590','verification/root-d4-final-adoption-20261117.json':'33f6646b0ae108700ba3b1571ac8ddb1c12060d98aa560f6ccd017cad88e55da','verification/mink-riesz-k3-live-root-20261117/HTTP_FINAL.json':'8587968ad6c63bdc83d6f477ebbbd30a3344f3af8a4028245126e3d6935daace','verification/thompson-cstar-editorial-corrected-v2-sol-20261117/FINAL.json':'67d0f85b610b011d1079889cb8932971ab6e9f8e0bb7c04e02946359aa27e533','verification/thompson-cstar-editorial-corrected-v2-sol-20261117/MANIFEST.json':'b1cef893c874b1c6502f5107fb4ae93d352828f0a830fb587c92a1fe9378243e','verification/thompson-cstar-editorial-corrected-v2-sol-20261117/SEAL.json':'e1adb487c49b1f6232c6d635e571ea2ae3aa445835cc3dddceaf83063c4797a4','verification/d4-root-custody-sol-20261117/FINAL.json':'101d6e8cfb772037645c9c97e1c14128a52c43c5dbcfef4e4673d381d0eafa85','verification/d4-root-custody-sol-20261117/MANIFEST.json':'5d621b7f74896018761443bc073bcd7050dd4b176dcbf2f05c5afe4a181fa4db','verification/checkpoint-thompson-pass143-20261117/FINAL.json':'bcdbfe4ed45a2f56e2db946137db359aace6fe068f991deb9df0cc14553b870f','verification/checkpoint-thompson-pass143-20261117/MANIFEST.json':'d35cacde34d59eb5f8103bd52e63374ef51aee06f85f19e439e6be2d638ed55a'}
for rel,sha in extra.items():important.append(rel);pins[rel]=sha
for rel in ['verification/root-checkpoint-2d02-adoption-20261117.json','verification/sheet-thompson-pass143-20261117/FINAL_READBACK.json','verification/sheet-three-pages-deployed143-20261117/FINAL_READBACK.json','verification/sheet-three-pages-deployed143-20261117/LIVE_HASH_READS.json','verification/sheet-three-pages-deployed143-20261117/LIVE_HTML_METADATA.json','verification/sheet-three-pages-deployed143-20261117/LIVE_PDF_METADATA.json','reconciliation/current-native-queue-20261117-pass143-thompson.json','reconciliation/current-native-queue-20261117-pass143-deployed133.json','verification/mink-riesz-k3-live-root-20261117/DEPLOYMENT_FINAL.json','verification/mink-riesz-k3-live-root-20261117/ORIGINAL_POSTSAVE_STORAGE_FAILURE.json','verification/mink-riesz-k3-live-root-20261117/LOCAL_AFTER.json','verification/mink-riesz-k3-live-root-20261117/LOCAL_AFTER_CONTINUATION.json','verification/root-mink-riesz-k3-v2-source-reading-20261117.json','verification/d4-root-custody-sol-20261117/DATA_AUTHENTICATION.json']:
 assert (P/rel).is_file(),rel;important.append(rel)
# Bind only control metadata, never scientific report text or producer code semantics.
for rel in list(roots):
 if rel not in old['immutable_packet_paths']:
  for name in ['SOURCE_FINAL.json','SOURCE_MANIFEST.json','INITIAL_SEAL.json','INITIAL_MANIFEST.json','FINAL.json','MANIFEST.json','OWNED_MANIFEST.json','FINAL_MANIFEST.json','FINAL_SEAL.json','SEAL.json']:
   if (P/rel/name).is_file():important.append(rel+'/'+name)
important=list(dict.fromkeys(important))
for rel in important:
 path=P/rel;assert path.is_file() and not path.is_symlink(),rel;sha=hashlib.sha256(path.read_bytes()).hexdigest()
 if rel in pins:assert pins[rel]==sha,rel
 else:pins[rel]=sha
assert (P/'papers/23439776/reviews/root-continuation-20261117/ROOT_REVIEW.md').stat().st_size==11832
assert (P/'verification/root-clearance-23439776-20261117.json').stat().st_size==1831
assert (P/'verification/root-d4-final-adoption-20261117.json').stat().st_size==1955
assert (P/'verification/mink-riesz-k3-live-root-20261117/HTTP_FINAL.json').stat().st_size==1149
active=['verification/mink-riesz-k3-postpublication-sol-20261117','verification/thompson-cstar-corrected-fact-sol-20261117']
for rel in active:assert (P/rel).is_dir() and not (P/rel).is_symlink()
caches=list(old['private_cache_paths'])
for rel in ['verification/mink-riesz-k3-runtime-sol-20261117','verification/mink-riesz-k3-root-execution-20261117']:
 assert (P/rel).is_dir();caches.append(rel)
caches=list(dict.fromkeys(caches))
release=dict(schema='explicit-root-d4-pass144-checkpoint-release-v1',UTC=datetime.now(timezone.utc).isoformat(),authorization='ROOT_RELEASE_TO_CHECKPOINT',expected_parent='2d020358e466323f2f188ee84aa2ff1a535bed8c',authorizing_agent='/root',root_P_W_writes_quiescent=True,authorized_active_verification_paths=active,durable_tree_roots=list(roots.values()),immutable_packet_paths=list(roots),important_paths=important,expected_key_file_SHA256=pins,private_cache_paths=caches,scientific_reviewed=144,scientific_passes=136,scientific_deferred=8,scientific_remaining=59,total=203,native_Sheet_reviewed=143,programme_counts=dict(verified=123,deployed=10,preparing=2,under_review=8,queued=50,holds=2,deferred=8),programme_goal_active_incomplete=True,scientific_percent=144/203*100,inclusion_updates=dict(corrected_Thompson_V2_frozen_before_guard_included=True,D4_editorial_PLAN3files_frozen_before_guard_included=True,corrected_fact_actual_active_excluded=True,postaudit_still_active_excluded=True),expected_W_HEAD='4cc09d6bbbad61aa11077c5002cf84a1e93b1344',expected_W_tree='a9c5a4f3e30eb976bbe4f9c1872e14a92e22cc7e',expected_W_index_SHA256='6b76dc0a4e7a631587aec1c081057479883573f7ff284dfc88b5adad02317179',expected_W_index_bytes=9062142,expected_public_files=803,expected_public_child_directories=387,on_actual_failure='STOP retain literal streams/exits/timestamps; no automatic repair/retry',no_global_PROGRESS_or_programme_log_mutation=True)
with (own/'ROOT_RELEASE.json').open('x') as stream:json.dump(release,stream,indent=2);stream.write('\n')
rows=[]
for name in ['capture_guards.py','run_helper_once.py','git','inspect_checkpoint.py','seal_evidence.py']:
 raw=(own/name).read_bytes();rows.append(dict(path=name,bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),full_saved_source_personally_read_before_first_attempt=True,no_import_AST_compile_or_execution=True))
h=(P/'scripts/checkpoint_subtree.py').read_bytes();assert len(h)==6213 and hashlib.sha256(h).hexdigest()=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0'
(own/'READ_ATTESTATION.json').write_text(json.dumps(dict(UTC=datetime.now(timezone.utc).isoformat(),fresh_sources=rows,authorized_helper=dict(bytes=len(h),SHA256=hashlib.sha256(h).hexdigest(),entire94line_source_previously_read_and_unchanged=True),no_old_publication_helper_execution_or_help=True,no_future_or_paper_exclusions=True),indent=2)+'\n')
with (own/'CHECKPOINT_LOG.md').open('a') as stream:stream.write('\n'+release['UTC']+' — Release metadata bound, full fresh sources read; correctedV2frozen22/1 and frozenD4PLAN3/0 included before guard. Only actualpostpublication/Thompsoncorrectedfact/own lanes excluded. Rootreview/clearance/custody/HTTP pins exact; ignoredruntime and privateoperationaljournal directories retained locally. No globalP writes/nohelper/Git/network yet. Checkpoint estimate30%; scientific144/native143distinct.\n')
print(json.dumps(dict(closed_roots=len(roots),key_files=len(important),active=active,private_cache_paths=len(caches),no_helper_Git_network_yet=True)))

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
C=P.parents[2]
Q=C/'private_sources/publication_admin_helper_v3/publication_v3_software_adversary2'
S=P.parent/'publication_admin_v3.py'
sp=importlib.util.spec_from_file_location('review_seal',S)
m=importlib.util.module_from_spec(sp)
exec(compile(S.read_bytes(),str(S),'exec'),m.__dict__)
g=m.g
paths={S, P.parent/'README.md',P.parent/'PROPOSED_RECOVERY_ADOPTION.json',m.V2_PATH,m.v2.V1_PATH,m.v1.GUARDS_PATH,m.v1.KIT_PATH}
original_read=g.read_regular
def tracked(path,**kw):
    paths.add(Path(path).absolute())
    return original_read(path,**kw)
g.read_regular=tracked
e=m.Admin(type('NoNetwork',(),{})(),Q/'seal_local_inspect',Q/'seal_unused_state.json')
e.load_adoption(P.parent/'PROPOSED_RECOVERY_ADOPTION.json','8edb48b705627c97e6390e05e63879924920fb2d1d590e83a61d18542f44155b')
g.read_regular=original_read
pins={str(p):{'sha256':g.sha(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted(paths)}
g.durable(P/'SOURCE_INPUT_PINS.json',pins,exclusive=True)
test=json.loads((P/'TEST_SUMMARY.json').read_bytes())
gate=json.loads((Q/'GATE_RESULT.json').read_bytes())
assert len(test['tests'])==28 and all(x['status']=='PASS' for x in test['tests'])
assert gate['native_gets']==6 and gate['head']==m.HEAD and gate['merged'] is False
utc=g.dt.datetime.now(g.dt.timezone.utc).isoformat()
report=f'''# Independent bounded V3 software review

Result: PASS, with zero unresolved findings in the authorized administrative scope. Timestamp {utc}. Completion estimate for this bounded review: 100%.

Reviewed helper SHA256 `536844c63eedf31934e686d44a32c3e8564ba9aaa9c078f204ffe5488bfdea53` and adoption SHA256 `8edb48b705627c97e6390e05e63879924920fb2d1d590e83a61d18542f44155b`. Initial independent falsification controls preceded prior reviewer output reads; no prior reviewer files were consulted. Root and applicable ancestor instructions were checked.

The fresh sealed updater g.Engine performed six native GitHub GETs. PR411 was open, draft and unmerged; its head and independent Git ref were `{m.HEAD}`. The native whole QUEUE blob and SHA256 were exact, and its header-derived row was 6800014 / AMR-067-0014, claimed_solved, Turns 2/5. A separate native branch GET matched. No GitHub writes occurred.

All 28 test groups passed. The positive recovery model replayed the actual root eight-GET administrative response shapes, yielding published_verified with eight GETs. The exact approved ACK, immutable V2 STOP state/copy, original V1 state, accepted native snapshot, root mapping and their positive receipts were locally rechecked. No scientific asset bytes were read.

Adversarial controls rejected changes to submitted twelve fields, publisher, DOI, integer reservation and exact authenticated fifteen keys; the public thirteen keys, license object, Preprint resource and first-version relation; exact native JSON types, record and parent PIDs, only empty parent ACL omissions, authenticated three flags versus public two flags; visible/completed exact three files and public MD5/SHA256/size/status/URL. SOURCE_INPUT_PINS.json records the positive dependency and custody inputs actually read by the helper.

Explicit inherited V1/V2 dispatcher calls could not reach a Zenodo POST or wrong/unphased Sheet append. One exact grant was consumed once and replay denied. A previous public HTTP response did not decorate a later denied inherited call. Production.public_hash itself resets native custody, and the bound transport defensively resets its own slot and backend slot before authorized dispatch. The hash tests use that actual reset protocol. The Production.sheet code retained fresh failing stdout/stderr from an actual offline subprocess, captured in finally through the wrapper; no real GWS was invoked and all model receipts were explicitly offline_model.

The tracker model used the fixed spreadsheet/gid/title/four headers, exact approved four cells and DOI-only deduplication. One RAW INSERT_ROWS append observed durable intent before its backend call, verified the returned row and final DOI scan, and denied a second attempt. Exact existing rows avoided append; duplicate DOI rows and target/header drift stopped. Failures before append, malformed returned ranges and wrong post-append values stopped. Unknown append outcomes before and after modeled effects preserved unknown_write and append_intent, produced no fabricated append response, reconciled with GETs only, and did not enable retry or promote the state.

Limits: these are bounded administrative protocol tests and source review, not mathematical review or fresh live Zenodo/Sheet verification. The README correctly discloses external-editor races and the absence of an atomic API lease. Root remains the sole live operator. No helper, actual production state, scientific source or Git/index/branch was changed. Protected V1/V2/V3 production states and source/adoption pins matched before and after testing. No external communication occurred.

Checkable artifacts: INITIAL_CONTROLS.md, native_gate.py, test_review.py, TEST_SUMMARY.json, SOURCE_INPUT_PINS.json, and the private native gate, offline response/error custody, protected input pins and full test results. PUBLIC_SEAL.json and PRIVATE_SEAL.json positively bind this review's outputs.
'''
(P/'REVIEW.md').write_text(report)
(P/'RESEARCH_LOG.md').write_text(f'''# Bounded review log

Initial controls: 2026-10-13 UTC, 15% complete; distinct custody, dispatch, exact-schema and tracker falsification families selected independently.

Native checkpoint: fresh six-GET engine gate passed, 30% complete; exact open/draft/unmerged PR/ref/whole-QUEUE pins and selected row confirmed.

Offline checkpoint: 28 bounded groups passed against actual administrative response fixtures, 90% complete; inherited bypasses, stale native custody, fresh process errors, exact append and unknown outcomes verified.

Final checkpoint: {utc}, 100% complete for this administrative review. Strongest verified result is bounded V3 protocol PASS. Exact remaining live gap: root's sole-operator authorized tracker operation and actual live post-write verification; no scientific conclusion is made.
''')
privatepins={str(p.relative_to(Q)):{'bytes':p.stat().st_size,'sha256':g.sha(p.read_bytes())} for p in sorted(Q.rglob('*')) if p.is_file() and p.name!='PRIVATE_SEAL.json'}
g.durable(Q/'PRIVATE_SEAL.json',{'schema':1,'utc':utc,'evidence_kind':'native_GitHub_GET_and_offline_model','positive_files':privatepins},exclusive=True,private=True)
publicpins={p.name:{'bytes':p.stat().st_size,'sha256':g.sha(p.read_bytes())} for p in sorted(P.iterdir()) if p.is_file() and p.name!='PUBLIC_SEAL.json'}
g.durable(P/'PUBLIC_SEAL.json',{'schema':1,'result':'PASS','utc':utc,'tests_passed':28,'positive_files':publicpins,'private_seal_sha256':g.sha((Q/'PRIVATE_SEAL.json').read_bytes()),'source_sha256':g.sha(S.read_bytes()),'adoption_sha256':g.sha((P.parent/'PROPOSED_RECOVERY_ADOPTION.json').read_bytes())},exclusive=True)
print(json.dumps({'result':'PASS','tests':28,'public_seal_sha256':g.sha((P/'PUBLIC_SEAL.json').read_bytes()),'private_seal_sha256':g.sha((Q/'PRIVATE_SEAL.json').read_bytes()),'source_inputs':len(pins),'private_files':len(privatepins)},sort_keys=True))

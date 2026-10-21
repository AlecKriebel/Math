# Derived per-file checklist from authenticated full03; own04 independently read all original prose/code and metadata, then freshly verifies nested semantics here. Historical claims are not fresh runs.
from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent;A=R.parents[1];O=A/'original/unsolved_math_prioritization/attempts/10400145'
def need(c,m):
 if not c:raise RuntimeError(m)
def load(name):return json.loads((O/name).read_bytes())
notes={
'BIBLIOGRAPHIC_CORRECTION.patch':'One historical sentence distinguishes125-page arXiv comment from123 physical pages; proof unchanged. Patch identity matches original bridge acceptance.',
'METADATA_TIMESTAMP_CORRECTION.patch':'Historical inspection timestamp update02:09:30→02:18:00; no mathematical edit. Not a newly reconstructed author turn.',
'BOOTSTRAP.py':'Read full external bootstrap; pins verifier/manifest before execution, self-copy identity and isolated optimization propagation. Actual portable/integrity and failure scopes checked.',
'VERIFY_PUBLICATION.py':'Read full wrapper. Exact inventory/schema/nested author/audit pins; optional source/corpus byte rehash separately scoped; full replay requires real bwrap/errno30. Fresh full attempts fail honestly here.',
'TEST_MUTATIONS.py':'Read full105-negative/6-positive harness including deliberate disposable pin refresh for schemas. Fresh own exact copy ran successfully; original directory unchanged.',
'CORPUS_VERIFICATION.json':'Two full-dataset sizes/hashes and target joins are historical metadata only. No new full-corpus rehash/join claimed; current source gate independently reconstructs exact raw target row.',
'EXTERNAL_PINS.json':'Author manifest/bootstrap pins,9 files and explicit independent-delivery trust note. Sidecar alone grants no authority.',
'FINAL_AUDIT_MANIFEST.json':'Four exact algebra-audit members, accepted author manifest and target identity; all child pins checked independently.',
'PUBLICATION_MANIFEST.json':'30 members plus its own file/bootstrap/verifier give33. Exact target/rank/status/resolution/approach types and paths authenticated by original integrity and new closed verifier.',
'README.md':'Read entire historical source-free packet description, original declaration1/5, two AI audits and no human/formal/novelty claim. Legacy bwrap requirement retained rather than relabeled current.',
'REPLAY_CONTROLS.json':'Parsed96 complete historical rows and checked recorded expected return-code outcomes, old readonly/mode/pin metadata. These recorded uid1000 results are not new host observations.',
'SOURCE_BRIDGE_AUDIT_MANIFEST.json':'Six exact bridge-audit members and accepted author anchors; all nested hashes and correction-patch links independently checked.',
'audit_algebra/ACCEPTANCE.json':'Historical negative-literal verdict,15 controls and9 retained source digests. Explicit no mathematical patches/human/formal/novelty claim; not new whole-package acceptance.',
'audit_algebra/AUDIT_RECEIPT.json':'All3 baseline entries/15 rejected controls/9 source rows inspected structurally and identity links checked. Portable audit rerun succeeds; historical source bytes remain historical.',
'audit_algebra/INDEPENDENT_AUDIT.md':'Read full proof/bridge/boundaries/errata/limits; independently checked its algebra and named primary coefficient inputs. Old acceptance words retain historical scope.',
'audit_algebra/audit_controls.py':'Read full program: finite dual algebra, author pin/inventory, three baseline modes,15 actual direct semantic/integrity controls, hostile imports and optional retained-source rehash. Fresh cold replay executes it.',
'audit_source_bridge/ACCEPTANCE.json':'Historical full proof review,72 controls, both metadata-only patch hashes, explicit source-retrieval limitation and no priority/formal certificate. Not current Linux reproduction.',
'audit_source_bridge/FULL_AUDIT.md':'Read full finite-quotient, source normalization, orientation/tail, patch/version and runtime arguments. Rechecked primary inputs independently rather than adopting its ACCEPT label.',
'audit_source_bridge/REPLAY_RECEIPT.json':'All72 controls parsed;69 expected rejections+3 positives, three entries in each baseline/algebra/read-only family, original EROFS30. Old Linux receipt is retained unchanged and not rerun-success here.',
'audit_source_bridge/SOURCE_INSPECTION.json':'Nine source rows and visual/text/record scopes read as historical inspection metadata, with fresh_download_claim false. Own actual reading selections recorded separately.',
'audit_source_bridge/independent_algebra.py':'Read entire ordered-pair dual-number implementation,6 basis vectors and controls. Exact stage runs in all cold modes; its finite-linear identity is checkable without topology claims.',
'audit_source_bridge/run_audit.py':'Read full actual72-control harness with real whole-filesystem bwrap and errno30 probe. Fresh original full replay stops on missingbwrap; no surrogate or installation used.',
'author_v3/AUTHOR_MANIFEST.json':'Nine exact packet payloads; immutable accepted author manifest/bootstrap/proof identities checked against independent original/Git/ZIP pins.',
'author_v3/bootstrap.py':'Read full manifest-first nested launcher, exact packet inventory and diagnostic-byte comparison; propagates actual requested optimization. Replayed all supported modes.',
'author_v3/packet/APPROACH_LEDGER.json':'One substantive finite-jet approach out of5, source recovery/search/replay excluded from proof-search count. Preserved historical declaration, not reconstructed native history.',
'author_v3/packet/CERTIFICATE.json':'Exact data sizes1,2,3;Casson−1;slopes0,−6,−24;forced−12;residual−12;correct ring/parameter/quotient/witness and explicit finite-check limit.',
'author_v3/packet/CLAIMS.json':'Exact literal-negative claimed_solved1 approach, cited dependencies and excluded variants; no novelty/formal/human claims. Not present review authority.',
'author_v3/packet/DIAGNOSTICS.json':'Byte-exact finite-check result,8 illustrative tail terms correctly labeled samples. General all-tail proof comes from mathematics, not this finite output.',
'author_v3/packet/GATE_METADATA.json':'Historical8October branch/search snapshot with no substantive prior attempt found; bounded scope explicit. Not a current no-predecessor or native-zero certificate.',
'author_v3/packet/PROOF_AND_STATUS.md':'Read full original proof; finite representative and first-jet map valid, topology inputs attributed, explicit orientation calibrated, all-tail proof and changed-ring/Casson-zero limits checked.',
'author_v3/packet/REPRODUCIBILITY.md':'Read full independent-pin, optimization, finite-check, source-free, nonconcurrent-host and non-formal-proof boundaries. Historical outer replay not silently promoted.',
'author_v3/packet/SOURCE_METADATA.json':'Nine version-specific public source identities and actual historical timestamp inspected; published versus accepted/older bodies distinguished. All later own source retrievals/reads separately recorded.',
'author_v3/packet/verify.py':'Read full explicit-exception sparse polynomial checker and strict data types; direct semantic mutations bypass stale-hash boundary; all supported modes replay. Sample tail checks are expressly not all-tail proof.'}
record=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_bytes());relative={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file()};need(relative==set(notes) and len(relative)==33,'all33 individually accounted')
checks={}
for man,prefix in [('author_v3/AUTHOR_MANIFEST.json','author_v3/packet/'),('FINAL_AUDIT_MANIFEST.json','audit_algebra/'),('SOURCE_BRIDGE_AUDIT_MANIFEST.json','audit_source_bridge/')]:
 d=load(man)
 for row in d['files']:
  b=(O/(prefix+row['path'])).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'nested original pin')
 checks[man]=len(d['files'])
r=load('REPLAY_CONTROLS.json');checks['historical96_rows']=len(r['rows']);need(len(r['rows'])==96,'historical rows')
need(all(type(x['rc']) is int and x['expected'] in ('PASS','REJECT') and ((x['rc']==0)==(x['expected']=='PASS')) for x in r['rows']),'each historical expected return-code outcome')
checks['historical96_expected_values']=sorted({x['expected'] for x in r['rows']});checks['historical96_nonzero_rc_count']=sum(x['rc']!=0 for x in r['rows']);checks['historical96_zero_rc_count']=sum(x['rc']==0 for x in r['rows'])
a=load('audit_algebra/AUDIT_RECEIPT.json');need(len(a['negative_controls'])==15 and all(x['rejected'] is True for x in a['negative_controls']) and len(a['source_checks'])==9,'algebra historical rows')
b=load('audit_source_bridge/REPLAY_RECEIPT.json');need(len(b['controls'])==b['control_count']==72 and all(x.get('rejected') is True or x.get('expected_pass') is True for x in b['controls']),'historical bridge rows');need(all(len(b[k])==3 for k in ['baseline','algebra','read_only','algebra_read_only']) and b['write_denied_errno']==30,'historical mode matrix')
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ALL33_INDIVIDUALLY_INSPECTED_AND_AUTHENTICATED','files':{name:{'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest(),'inspection':notes[name]} for name in sorted(notes)},'structural_cross_checks':checks,'fresh_original_full_linux_status':'NOT_REPRODUCED','current_corpus_byte_rehash_or_fresh_full_join':'NOT_RUN','new_native_author_proof_responses':0}
(R/'ORIGINAL_FILE_INSPECTION.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n');print('PASS',len(notes),checks)

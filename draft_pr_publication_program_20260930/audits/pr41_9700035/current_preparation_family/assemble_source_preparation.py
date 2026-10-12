#!/usr/bin/env python3
"""Own read/static-only preparation author; never imports or runs the builder."""
import ast
import datetime as dt
import hashlib
import json
import math
from pathlib import Path, PurePosixPath

HERE=Path(__file__).resolve().parent
A=HERE.parent
UTC=dt.datetime.now(dt.timezone.utc).isoformat()
PINS={
 'primary_scope_family':'7d8318e0b7f7009ead1e19ae8c58008139da96c1b35ecfbbdf9fbe109ec830a8',
 'network_tail_measure_family':'1b99b3ad334b970985ed3ba5f11d113fc4ed77793f7922b7b0142479821b750d',
 'root_original_actual_reproduction':'d8fb8a576676a690f9cb365f426bf3f344780bc1d03fbdc02f8534a44f3487f7',
 'root_family_controls_actual_reproduction':'35f6efc31439e33795820b19d6df7a49451f649e6ccd71fac71956b4d0556840'}
FLAGS=['original_mathematical_body_fully_read','operative_primary_definitions_and_target_fully_read',
 'imported_source_proof_qualifications_fully_read_and_accepted','full_raw_SQL_and_present_prior_actual_evidence_fully_read',
 'unchanged_original_helper_actual_reproductions_fully_read','both_closed_independent_families_fully_read',
 'closed_input_manifests_and_retained_evidence_exactly_checked','scoped_scientific_conclusions_accepted']
READ=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def decode(b):
 def pairs(rows):
  out={}
  for k,v in rows:
   if k in out:raise ValueError('Duplicate JSON key: '+k)
   out[k]=v
  return out
 def floating(v):
  n=float(v)
  if not math.isfinite(n):raise ValueError('Nonfinite decoded JSON number')
  return n
 return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
def encode(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def canonical(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def path_ok(name):
 p=PurePosixPath(name)
 assert type(name) is str and name and not p.is_absolute() and p.as_posix()==name and '\\' not in name
 assert not {'.','..','.git','__pycache__'}.intersection(p.parts)
 return name
def read(name):
 p=A/path_ok(name);assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
 b=p.read_bytes();r={'path':name,'bytes':len(b),'sha256':sha(b)}
 if not any(x['path']==name for x in READ):READ.append(r)
 if p.suffix=='.json':decode(b)
 return b
def row(name):
 b=read(name);return {'path':name,'bytes':len(b),'sha256':sha(b)}
def rows(raw):
 result=[];names=set()
 for r in raw:
  assert set(r)=={'path','size','sha256'} and type(r['size']) is int and r['size']>=0
  assert r['path'] not in names;names.add(path_ok(r['path']))
  result.append({'path':r['path'],'bytes':r['size'],'sha256':r['sha256']})
 return result
def closure(directory,members):
 root=A/directory;names={r['path'] for r in members};assert len(names)==len(members)
 actual=set();dirs=set()
 for p in root.rglob('*'):
  assert not p.is_symlink()
  if p.is_file():actual.add(path_ok(p.relative_to(root).as_posix()))
  else:assert p.is_dir();dirs.add(p.relative_to(root).as_posix())
 assert actual==names,(directory,sorted(actual-names),sorted(names-actual))
 expected={q.as_posix() for name in names for q in PurePosixPath(name).parents if q.as_posix()!='.'}
 assert dirs==expected,(directory,sorted(dirs-expected))
 for r in members:
  b=read(directory+'/'+r['path']);assert len(b)==r['bytes'] and sha(b)==r['sha256']
def put(name,obj):
 p=HERE/name
 assert not p.exists() and not p.is_symlink()
 with p.open('xb') as f:f.write(obj.encode() if isinstance(obj,str) else encode(obj))

families={}
for family in ['primary_scope_family','network_tail_measure_family']:
 m=row(family+'/FIRST_PARTY_MANIFEST.json');assert m['sha256']==PINS[family]
 j=decode(read(m['path']));authored=rows(j['files'])
 if family=='primary_scope_family':
  assert j['root_only_self_exclusion']=='FIRST_PARTY_MANIFEST.json' and j['excluded_root_directories']==['foreign_primary_cache']
  foreign=decode(read(family+'/FOREIGN_CACHE_MANIFEST.json'))
  assert foreign['root']=='foreign_primary_cache' and foreign['first_party'] is False
  foreign_rows=[dict(r,path='foreign_primary_cache/'+r['path']) for r in rows(foreign['files'])]
  assert len(authored)==127 and len(foreign_rows)==21
 else:
  assert j['self_excluded']==['FIRST_PARTY_MANIFEST.json'] and j['foreign_root']=='foreign_primary'
  foreign_rows=rows(j['foreign_files']);assert len(authored)==115 and len(foreign_rows)==8
 assert not {r['path'] for r in authored}.intersection(r['path'] for r in foreign_rows)
 closure(family,authored+foreign_rows+[dict(m,path='FIRST_PARTY_MANIFEST.json')])
 families[family]={'manifest':dict(m,path='FIRST_PARTY_MANIFEST.json'),'first_party_count':len(authored),'foreign_count':len(foreign_rows),
                   'members':authored,'foreign_members':foreign_rows,'foreign_bodies_copied_into_current':False,
                   'recursive_exclusion':'None except the literal root self; foreign members individually hash-bound and excluded only from copied outputs'}

root_support={}
for label,directory,count,receipt in [('original','root_original_actual_reproduction',130,'ROOT_REPRODUCTION.json'),
                                      ('families','root_family_controls_actual_reproduction',15,'ROOT_FAMILY_REPRODUCTION.json')]:
 m=row(directory+'/MANIFEST.json');assert m['sha256']==PINS[directory]
 j=decode(read(m['path']));assert j['self_excluded']==['MANIFEST.json'] and type(j['files_count']) is int and j['files_count']==count
 assert len(j['files'])==count and all(set(r)=={'path','bytes','sha256'} for r in j['files'])
 closure(directory,j['files']+[dict(m,path='MANIFEST.json')]);rr=row(directory+'/'+receipt)
 root_support[label]={'directory':directory,'member_count':count,'manifest_sha256':m['sha256'],'manifest_bytes':m['bytes'],
                      'members':j['files'],'receipt':receipt,'receipt_sha256':rr['sha256']}

snapshot_raw=read('snapshot_manifest.json');assert sha(snapshot_raw)=='feef9bf6433c165296d3cdea883ceb74440048e17ff87f03ef636a99338cb3e6'
snapshot=decode(snapshot_raw);assert len(snapshot['files'])==16 and len(snapshot['changed_paths'])==17
original=[]
for r in snapshot['files']:
 b=read('source_snapshot/'+r['path']);assert len(b)==r['size'] and sha(b)==r['sha256']
 original.append({'path':r['path'],'bytes':r['size'],'sha256':r['sha256']})
closure('source_snapshot',original)
qualification=row('primary_scope_family/SOURCE_PROOF_QUALIFICATIONS.md')
assert qualification['sha256']=='69196e84de0d627b31b6f2a20a3745ba33048969cb93efba92a886bfedf8bc7e'
root_sources=[row(name) for name in ['reproduce_original_checks.py','reproduce_family_controls.py']]
observed_certificate=row('ROOT_PARTIAL_SCOPE_CERTIFICATE.md')
diff=row('pr_input/diff.patch');assert diff['bytes']==201709
metadata=row('pr_input/metadata.json')
builder=(HERE/'prepare_current_packet.py').read_bytes();tree=ast.parse(builder)
assert not any(isinstance(n,(ast.Import,ast.ImportFrom)) and any(a.name.startswith(('primary_scope_family','network_tail_measure_family','prepare_current_packet')) for a in n.names) for n in ast.walk(tree))
assert 'if __name__==\'__main__\':main()' in builder.decode()
assert "stdin=subprocess.DEVNULL" in builder.decode() and 'publish_absent(stage,destination)' in builder.decode()
assert "parsed.utcoffset()==dt.timedelta(0)" in builder.decode() and "math.isfinite(result)" in builder.decode()

put('INPUT_PINS.json',{'schema':'PR41_SOURCE_PREPARATION_FIXED_INPUTS_v1','utc':UTC,
 'status':'SOURCE_ONLY_FIXED_INPUTS_FUTURE_ROOT_PREREQUISITES_PENDING','current_or_future_root_verdict_claimed':False,
 'original_head':snapshot['head'],'original_base':snapshot['base'],'snapshot_manifest_sha256':sha(snapshot_raw),
 'original16':original,'original_changed_paths':snapshot['changed_paths'],'diff_sha256':diff['sha256'],'auxiliary':[metadata],
 'whole_source_JSON':canonical(decode(read('source_snapshot/source_record.json'))),
 'whole_prior_JSON':canonical(decode(read('source_snapshot/prior_report.json'))),
 'families':families,'qualification':qualification,'root_support':root_support,'root_sources':root_sources,
 'family_result_pairs':[['primary_scope_family/finite_controls_actual_capture_v2/RESULT.json','root_family_controls_actual_reproduction/primary_finite_RESULT.json'],
                        ['network_tail_measure_family/NETWORK_MEASURE_CONTROL_RESULTS.json','root_family_controls_actual_reproduction/network_measure_finite/NETWORK_MEASURE_CONTROL_RESULTS.json']],
 'observed_root_certificate_not_a_fixed_future_approval_pin':observed_certificate,
 'future_ROOT_files_not_yet_supplied_or_approved':['ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json'],
 'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0})

put('DRAFT_ROOT_SCIENCE_CARD.json',{'schema':'PR41_DRAFT_ROOT_SCIENCE_CARD_NOT_APPROVAL_v1','utc':UTC,
 'status':'PENDING_ROOT_FULL_READING_AND_APPROVAL','partial_valid':False,'full_problem_solved':False,'novelty_claimed':False,
 'root_flags':{key:False for key in FLAGS},'scope_certificate_sha256':None,'read_ledger_sha256':None,
 'proof_qualifications_sha256':qualification['sha256'],'actual_replay_receipt_sha256':root_support['original']['receipt_sha256'],
 'actual_replay_manifest_sha256':root_support['original']['manifest_sha256'],
 'actual_family_replay_manifest_sha256':root_support['families']['manifest_sha256'],'current_input_manifest_sha256':None,
 'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,
 'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'current_verdict':None,'new_whole_current_gate':'PENDING',
 'instruction':'ROOT must author separate genuine approved card after full reading. Do not rename this draft or infer approval from historical PASS.'})

put('DRAFT_ROOT_READ_LEDGER.json',{'schema':'PR41_DRAFT_ROOT_READ_LEDGER_NOT_APPROVAL_v1','utc':UTC,
 'reading_completed':False,'scope_certificate_sha256':None,'proof_qualifications_sha256':qualification['sha256'],
 'actual_replay_manifest_sha256':root_support['original']['manifest_sha256'],
 'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,
 'root_flags':{key:False for key in FLAGS},'instruction':'A source preparer cannot attest ROOT reading; ROOT must author the real external prerequisite.'})

put('CURRENT_OVERVIEW.md',"""# Proposed PR41 current packet

Full indexed 2012 Open Problem35 remains **UNSOLVED**. The strongest audited
partial is the unconditional expected in-square all-pair route-union law and
full-length lower bound, plus the full expected-length law under the explicit
additional `t^4 P(D>t)->0` hypothesis. A finite fourth moment suffices. The
published2014 Problem9 asks what extra assumptions suffice; that wording does
not resolve the stronger indexed target. Span counts prescribed route union,
including exterior excursions, with shared length counted once; it is not a
Steiner minimum. Ell is the unit-Poisson sampled-network length intensity.

The exterior argument uses the full SIRSN assumption of finite major-road
intensity p(1). A merely weak SIRSN does not automatically supply it. The
unconditional remaining gap is o(k) expected total exterior length under the
ordinary axioms. Scalar tail and escaping-measure controls are not admissible
SIRSN counterexamples. No necessity, novelty, exhaustive priority or external
human peer-review claim is made.

The original16 files remain byte-exact in original_archive. The main PROOF,
both original checker sources, full saved results, imported source/prior,
provenance and two-entry ledger remain exact in current mathematical anchors.
Only clearly marked current presentation receives the ancillary imported
Kahn proof note: joint events instead of conditioning on dependent geodesic
time, T_n radius/indexing and shifted moment sums, corrected geometric
inequality directions/constants for the required time tail, and speed times
time for slow length. The credited q<gamma-1 moment range survives these
qualifications; gamma>5 supplies a fourth moment, gamma=5 is not covered.
Foundational model existence/uniqueness remains a credited import. The main
conditional theorem does not depend on this ancillary model citation.

Existing actual ROOT captures contain211/3809 original diagnostics and1326/122
independent family controls, plus full149266659-byte raw-data/all15458 joined
SQL-row evidence. This source preparation binds them as historical completed
evidence; it neither executes them nor supplies a future current verdict.
Finite checks supplement analytic proof reading. Complete captured sources,
streams and old failed ancillary controls are retained, not replaced.

This folder is SOURCE ONLY. No candidate freeze, future whole-source-first
review, final reconciliation or merge has run here. Every draft ROOT flag is
false, partial_valid is false in the approval draft, and future approval pins
are null. The actual builder requires four separate genuine ROOT CLI SHA pins.
Current model, reasoning, deadline and verdict remain present nulls. A NEW
entire-current source-first adversary is required after the freeze; original
reviews never transfer that verdict.

Original substantive attempts2/5, new target attempts0, native audit records0.
No paper, new DOI, tracker row, release, canonical/native/Git/remote mutation or
outside contact is performed. ROOT publishes owned checkpoint work. This
preparer has prior candidate/report exposure and does not claim a newly blind
mathematical review. Source preparation completion is estimated90%; full
unconditional discovery estimate0%.
""")

put('EXECUTION_CONTRACT.md',"""# Proposed administrative freeze contract

SOURCE ONLY; execution is reserved to ROOT after complete source/contract and
closed-input review. Run the fully read `prepare_current_packet.py` with
`/usr/bin/python3 -B`, `--execute`, and all four lowercase SHA256 CLI options:
`--root-scope-certificate-sha256`, `--root-read-ledger-sha256`,
`--root-science-card-sha256`, `--root-current-input-manifest-sha256`.
Each fixes the bytes of the corresponding external audit-root prerequisite.
Those files are not authored or approved by this source preparer. Drafts in
this folder are never valid prerequisites.

The approved external ROOT_PRIMARY_READ_LEDGER.json must record
reading_completed:true, the exact scope_certificate_sha256,
proof_qualifications_sha25669196e84de0d627b31b6f2a20a3745ba33048969cb93efba92a886bfedf8bc7e,
actual_replay_manifest_sha256d8fb8a576676a690f9cb365f426bf3f344780bc1d03fbdc02f8534a44f3487f7,
original_substantive_attempts2,new_substantive_attempts0,audit_turns0.
ROOT's actual scientific card must have statusUNSOLVED, partial_valid:true,
full_problem_solved:false, novelty_claimed:false, original2, limit5,new0/audit0,
the eight exact root_flags in the adjacent draft all genuinely true, and all
scope/ledger/qualification/actual-receipt/actual-original-manifest/
actual-family-manifest/current-native13 pins exact. Current model, reasoning,
deadline and verdict are null; new_whole_current_gate is PENDING. These flags
certify the completed mathematical/evidence reading, never the future current
packet, whole review or integration.

The external ROOT_CURRENT_INPUT_PREIMAGES.json needs approved_by_root:true,
a substantive reason (a bare yes/approved/PASS/ok is rejected), aware UTC
created_utc not in the future, the actual current_head, and exactly13 unique
path/bytes/SHA rows. Bytes must match the dated actual replay input_preimages
and the actual live paths. Fresh HEAD may include routine audit-publication
commits; it need not equal dated replay HEAD33a08009b078d43c4e560c144cf75361bd0f4c0a.
If earlier PR integration changes native inputs, do not bypass this guard:
ROOT must prepare properly reviewed updated actual evidence or an explicitly
reviewed source revision before freezing PR41.

The builder performs read-only Git branch/object/mode/diff and HEAD checks;
every actual command preserves argv/cwd, aware UTC clocks, complete stdout/
stderr and failures under a fresh audit/tmp attempt. It imports/runs no proof
or family helpers, performs no scientific search, and has no network or Git
mutation operation. Its stdin is DEVNULL. ROOT's outer actual capture must
retain the full prelaunch builder source, real PID/argv/cwd/UTC clocks,
complete stdout/stderr and exit. Never infer execution from this contract.

The only publication target is a new absent reviewed_candidate directory.
Original16/current immutable math remain exact; full root130+15 and both
closed first-party family evidence are copied as read-only0444 archives.
Foreign21+8 primary bodies are individually bound dependencies only, never
redistributed as authored current files. Dependences resolve from the fixed
repository-relative PR41 audit root, including after canonical copying, not
from transient scratch. Duplicate JSON keys, nonfinite decoded numbers,
boolean integer substitutions, duplicate/unsafe paths, symlinks, special
files, changed rows and extra empty directories are rejected. Repeated reads
must preserve path/bytes/SHA; multiple semantic roles are explicitly retained.

The prospective queue changes only named Status, Turns, Findings: queued0/5
to unsolved2/5 and the qualified finding. Every other row/column, Chat and DOI
is byte-preserved. This writes only local proposed files, never the live queue.
Current/future runtime claims and actual whole verdict remain null/PENDING.

The builder stages complete files in a unique retained attempt, checks exact
self-only recursive membership and every0444 size/SHA, then publishes with
macOS renamex_np(RENAME_EXCL). Existing/appearing target is never overwritten.
Failed commands/stages remain retained, and no failed current manifest is a
valid positive packet. Success does not perform canonical/shared/remote
writes or a merge and does not satisfy the NEW whole-source-first gate.
""")

put('ROOT_READ_EXPECTATIONS.md',"""# Remaining ROOT reading and approval requirements

This document requests no new attestation from the source preparer. ROOT must
personally read the submitted mathematical body, literal primary definitions
and both target formulations, operative imported qualifications and their
limits, both completed independent families, and the entire retained actual
reproduction evidence. Full JSON means whole typed objects and every stored
check, not selected grep matches or counts. Full data evidence includes all
raw bytes/all SQLite joins, actual PRESENT prior, exact original16/Git modes/
full17-path diff and actual unchanged helper outputs. Read all proposed builder
source and contracts, and independently recheck the exact closed manifests
and individual foreign exclusions. Original old reviews/captures are dated
evidence, not certificates of future operations.

Only then author external ROOT_PRIMARY_READ_LEDGER.json and ROOT_SCIENCE_CARD.json
with the eight exact flags listed in the draft, correct pins and accounting.
Author the genuinely current native13 manifest with actual current HEAD,
reason/UTC and exact preimages. The current builder retains old replay HEAD
as historical evidence and separately checks the new approved current HEAD.
No merely renamed draft, true flag copied from an old review, inferred model,
future whole verdict or simulated capture is acceptable.

After actual ROOT freeze and full read of the resulting closed current packet,
assign a distinct source-first whole-current adversarial reviewer. Its scope
must include all provenance, archives, copied families, complete actual streams,
source guards, current qualifications, JSON types/nulls and prospective queue.
Any required repair must be global in current presentation and re-reviewed.
Final actual reconciliation/canonical integration/merge remain separate ROOT
gates. The accepted outcome must retain UNSOLVED/partial and original2/5,
new0/audit0, without a paper, new DOI or publication-tracker row.
""")

put('SOURCE_PREPARATION_RESEARCH_LOG.md',UTC+" — resumed unclosed stopped preparation; fully read proposed builder, ROOT scope certificate, original proof/source/review, both independent reports, exact imported qualification and actual root receipts. Independently rehashed every bound closed member and individual foreign body; parsed complete JSON bytes. No proposed helper was imported or executed; no native/canonical/Git/remote mutation. Source-preparation90%, unconditional discovery0%. Original2/5,new0/audit0. Prior report/candidate exposure disclosed. An exploratory readonly manifest-schema query used foreign_artifacts instead of foreign_files and exited1; corrected by reading the literal schema, no files changed and no failed candidate run occurred. Strengthened source-only builder for ordered UTC, nonfinite overflow, explicit stdin, exact directories, distinct actual channels and immutable repeated-read identities with multiple roles. Actual freeze and NEW whole-source-first review remain pending.\n")
put('STATIC_INPUT_INSPECTION.json',{'schema':'PR41_OWN_READ_STATIC_PREPARATION_INSPECTION_v1','utc':UTC,
 'status':'PASS_READ_STATIC_ONLY_NOT_BUILDER_EXECUTION','input_files_read':len(READ),'whole_bytes':sum(r['bytes'] for r in READ),
 'files':sorted(READ,key=lambda r:r['path']),'builder_ast_parsed':True,'builder_imported':False,'builder_executed':False,
 'proposal_helpers_imported_or_executed':False,'native_or_canonical_writes':False,'Git_or_remote_writes':False,
 'foreign_individually_bound':29,'first_party_family_members':242,'root_actual_retained_members':145,
 'actual_future_current_or_whole_verdict_claimed':False,'draft_root_flags_all_false':True,
 'source_preparation_completion_estimate_percent':90,'unconditional_discovery_estimate_percent':0,
 'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0})
print(json.dumps({'status':'PASS_OWN_STATIC_SOURCE_PREPARATION','files_read':len(READ),'bytes_read':sum(r['bytes'] for r in READ),
 'known_closed_manifests':PINS,'builder_sha256':sha(builder),'builder_executed':False,'helpers_imported_or_executed':False,
 'future_current_whole_verdict':'PENDING','new_substantive_attempts':0,'audit_turns':0},indent=2))

"""Seal this authored-only review after rechecking its frozen inputs."""
from pathlib import Path
import datetime, hashlib, json

O=Path(__file__).resolve().parent
R=O.parent
bindings=json.loads((O/'INPUT_BINDINGS.json').read_text())
for row in bindings['inputs']:
    raw=(R/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
frozen=json.loads((R/'FROZEN_INPUTS.json').read_text())
for row in frozen['submission_files']:
    raw=(R/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
assert frozen['release_cleared'] is False
render=json.loads((O/'RENDER_BINDING.json').read_text())
assert len(render['fresh_comparison'])==11 and all(r['identical'] for r in render['fresh_comparison'])
replay=json.loads((O/'PORTABLE_REPLAY.json').read_text())
assert replay['all_programs_passed'] and replay['package_members_hash_verified']==167
assert len(replay['programs'])==7 and replay['original_reported_exact_assertions']==2156
assert json.loads((O/'INDEPENDENT_CONTROLS_RESULT.json').read_text())['all_passed']
pkg=json.loads((O/'PACKAGE_CHECK_RESULT.json').read_text())
assert pkg['members']==168 and pkg['verified_payloads']==167
assert pkg['all_hashes_verified'] and pkg['no_extra_or_missing_members']
prov=json.loads((O/'NATIVE_HISTORY_REPAIR_CHECKS.json').read_text())
assert prov['all31_native_head_bytes_verified'] and prov['old_review_seal_valid_and_archived_identically']
assert prov['D1_globally_fixed'] and prov['D2_globally_fixed']
sources=json.loads((O/'SOURCE_PINS.json').read_text())
for row in sources['primary_sources']:
    p=R.parent/'initial_review_20261015'/row['path_relative_to_initial_review']
    raw=p.read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
verdict={'utc':now,'review':'fresh_review_02','review_type':'Independent AI-assisted internal full-manuscript/package adversarial review',
 'mathematical_review':'PASS_NO_BLOCKER_IDENTIFIED','whole_package_review':'PASS_NO_REMAINING_FINDING_IDENTIFIED',
 'mandatory_findings':[],'optional_findings':[],'earlier_D1_D2':'Globally fixed in active files and generator; original bytes and earlier verdict retained',
 'all_384_tex_lines_read':True,'all_11_current_pdf_pages_actually_viewed':True,'fresh_renders_identical_to_viewed_pngs':True,
 'members':168,'payload_hashes_verified':167,'all31_native_head_original_files_verified':True,
 'all_seven_portable_programs_passed':True,'independent_symbolic_rational_controls_passed':True,
 'priority_certified':False,'source_access_limits':['Named2022/2023 dynamic manuscript not located','Rahola2000 full article unavailable','Goepfert2024 full thesis uninspected','Some broader classical originals unavailable; no comprehensive historical exclusion'],
 'supported_contribution':'Credited independent exact-model proof/application under(G) and separate fixed compact-support scope obstruction',
 'not_supported':'First-priority certificate; wholly new general theory; unrestricted compact-support convergence; necessary geometry classification; rates; varying-frequency limit; individual Jordan-block preservation',
 'publication_cleared':False,'remaining_parent_work':'Explicit final clearance/release workflow; retain all stated credit and priority limitations',
 'frozen_inputs_unchanged_at_seal':True,'completion_percent_of_assigned_bounded_review':100}
(O/'REVIEW_VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
with (O/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+now+' — Completed report, verified all frozen inputs unchanged, and sealed authored-only review. No mandatory or optional finding remains; prior D1/D2 closed without relabeling historical review. Completion estimate:100% of assigned bounded review; historical priority remains unproved.\n')
rows=[]
for p in sorted(O.iterdir()):
    if not p.is_file() or p.name=='SAFE_AUTHORED_MANIFEST.json':continue
    assert not p.is_symlink() and p.suffix in ['.json','.md','.py']
    raw=p.read_bytes();rows.append({'path':p.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
manifest={'utc':now,'scope':'Authored review report, reconstruction, code, research log and computed receipts only; excludes private source/extraction/render assets and this manifest itself.',
          'safe_authored_files':rows,'publication_clearance':False}
(O/'SAFE_AUTHORED_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'sealed':True,'authored_files':len(rows),'findings':0,'completion_percent':100,'input_pins_unchanged':True},indent=2))

"""Build a private six-line target-only checker correction; no original writes."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,difflib,ast
R=Path(__file__).resolve().parent;P=R.parents[1]
S=P/'verification/local-ambient-block-modulus-stage-sol-20261025'
A=P/'verification/audit-ambient-block-modulus-code-sol-20261025'
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
IDS=['23333353','23416806','23441617']
def info(p):
 d=p.read_bytes();return {'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
if (R/'BEFORE.json').exists():raise RuntimeError('preserve baseline')
protected=set()
for base in [S,A]:
 m=json.loads((base/'FINAL_MANIFEST.json').read_text())
 for x in m['files']:
  p=Path(x['path']);p=p if p.is_absolute() else base/p
  wanted=x.get('sha256',x.get('SHA256'))
  if info(p)['sha256']!=wanted:raise RuntimeError('original owned binding '+str(p))
 protected.update(p for p in base.rglob('*') if p.is_file())
for rid in IDS:
 q=P/'papers'/rid
 protected.update(q/n for n in ['publication.json','promotion.json'])
 protected.update(P/'verification'/f'{prefix}-{rid}-20261025.json' for prefix in ['root-clearance','root-editorial'])
 protected.update(p for p in (q/'reviews/editorial').rglob('*') if p.is_file())
for name in ['render_page.py','published_assets.py','bosonic_source.py','dipole_source.py','cfh_source.py','cylinder_discotope_source.py','spanning_sos_gin_source.py']:
 p=P/'scripts'/name
 if p.exists():protected.add(p)
protected.add(P/'verification/final-content-check.py')
protected.update(p for p in LIVE.rglob('*') if p.is_file())
before={'utc':datetime.now(timezone.utc).isoformat(),'files':{str(p):info(p) for p in sorted(protected)},
 'stage_file_set':[str(p.relative_to(S)) for p in sorted(S.rglob('*'))if p.is_file()],
 'audit_file_set':[str(p.relative_to(A)) for p in sorted(A.rglob('*'))if p.is_file()],
 'current_public_file_set':[str(p.relative_to(LIVE)) for p in sorted(LIVE.rglob('*'))if p.is_file()],
 'no_stale_mutable_baselines_followed':True}
(R/'BEFORE.json').write_text(json.dumps(before,indent=2)+'\n')
src=(S/'final-content-check.proposed.py').read_text()
if info(S/'final-content-check.proposed.py')['sha256']!='81ca32b424e66d536a3f96344c44d1f5a7b47b3617a74abf5791c8727bec8fa0':raise RuntimeError('exact checker base')
needle="  test('exact_visible_h1',contract.headings==[c['title']])\n"
insertion='''  heading_fragments=re.findall(r'<h1>(.*?)</h1>',h,re.S)
  heading_anchors=ABMBodyText('<body>'+''.join(heading_fragments)+'</body>').anchors
  test('exact_h1_selflink_destination',len(heading_fragments)==1 and [(attrs.get('href'),label) for attrs,label in heading_anchors]==[('/research/'+c['slug']+'/',c['title'])])
  main_navigation=re.findall(r'<nav aria-label="Main navigation">(.*?)</nav>',h,re.S)
  research_anchors=[(attrs.get('href'),label) for attrs,label in ABMBodyText('<body>'+''.join(main_navigation)+'</body>').anchors if label=='Research']
  test('exact_main_Research_destination',len(main_navigation)==1 and research_anchors==[('/research/','Research')])
'''
if src.count(needle)!=1:raise RuntimeError('unique ABM insertion')
proposed=src.replace(needle,needle+insertion)
if proposed.replace(insertion,'',1)!=src:raise RuntimeError('all old source bytes must match')
ast.parse(proposed)
(R/'final-content-check.proposed.py').write_text(proposed)
(R/'navigation-guard.diff').write_text(''.join(difflib.unified_diff(src.splitlines(True),proposed.splitlines(True),fromfile='stage/final-content-check.proposed.py',tofile='correction/final-content-check.proposed.py')))
old="R=Path(__file__).resolve().parents[1]\n";new='R=Path('+repr(str(P))+')\n'
if proposed.count(old)!=1:raise RuntimeError('one private-root override')
stage=proposed.replace(old,new)
(R/'final-content-check.stage.py').write_text(stage)
(R/'private-execution-only.diff').write_text(''.join(difflib.unified_diff(proposed.splitlines(True),stage.splitlines(True),fromfile='proposed',tofile='private-execution-only')))
(R/'INSERTION.txt').write_text(insertion)
(R/'STATIC_BINDING.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'exact_record_ids':IDS,
 'original_proposed_checker':{'path':str(S/'final-content-check.proposed.py'),**info(S/'final-content-check.proposed.py')},
 'new_proposed_checker':info(R/'final-content-check.proposed.py'),'new_private_executable_checker':info(R/'final-content-check.stage.py'),
 'inserted_lines':len(insertion.splitlines()),'only_existing_ABM_IDS_branch_changed':True,
 'removing_exact_insertion_restores_all_original_bytes':True,'every_old_branch_source_byte_preserved':True,
 'private_override_only_one_R_assignment':True,'helper_renderer_body_contract_originals_unchanged':True,
 'schema_and_legacy_suites_replayed':False,'renderer_executed':False},indent=2)+'\n')
(R/'RESEARCH_LOG.md').write_text('# Bounded navigation-guard correction\n\n'+before['utc']+' — Full stage/audit reports, relevant complete actual checker branch/parser/dispatch, all three full public copies and actual retained fault driver/receipts read before proposal. Fresh read-only baseline captured; no old suite or rendering. Exact six-line guard addition proposed in ABM_IDS branch only. Completion estimate35%; root keeps integration authority.\n')
print(json.dumps({'protected':len(protected),'stage_files':len(before['stage_file_set']),'audit_files':len(before['audit_file_set']),'public_files':len(before['current_public_file_set']),'new_code_lines':len(insertion.splitlines())}))

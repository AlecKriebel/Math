"""Record only the root-integrated, bounded mathematical/source disposition."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
D=Path(__file__).resolve().parent;P=D.parents[2]
families=['source_scope_adversary_01','geometry_algebra_adversary_01','meromorphic_divisor_adversary_01']
pins=[]
for name in families:
 folder=D/name;manifest=folder/'AUTHORED_MANIFEST.json';obj=json.loads(manifest.read_text())
 rows=obj.get('files',obj.get('entries'))
 for row in rows:
  path=(folder/row['relative_path']) if 'relative_path' in row else (D/row['path']);raw=path.read_bytes()
  assert path.resolve().is_relative_to(folder.resolve()) and not path.is_symlink()
  assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
 pins.append(dict(family=name,manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),report_sha256=hashlib.sha256((folder/'REPORT.md').read_bytes()).hexdigest(),authored_files=len(rows)))
for name in ['ROOT_ADDITIONAL_REPLAYS.json','ROOT_NEW_MATH_REPLAYS.json']:
 r=json.loads((D/name).read_text());assert r['status']=='PASS' and all(x['semantic_exact_replay'] and x['byte_identical'] for x in r['isolated_replays'])
assert json.loads((D/'ROOT_AUTHOR_REPLAY_ACCEPTANCE.json').read_text())['byte_identical']
proof=D/'submitted/unsolved_math_prioritization/attempts/5100063/PROOF.md'
assert hashlib.sha256(proof.read_bytes()).hexdigest()=='9640ed4bc6c6b0b56f0235c0e28513e9c3ca94c53cb75d2cb2eecee5b45b075e'
t=datetime.now(timezone.utc).isoformat()
result=dict(utc=t,status='PASS for the exact nondegenerate confocal-ellipse k904,a theorem',PR=211,head='9d7b623203b525386da3d9d91548c79e7445a11c',proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest(),families=pins,root_full_derivations_reports_controls_and_source_read=True,all_five_programs_replayed_in_isolated_folders=True,all_five_result_files_byte_identical=True,mechanism='Actual outer-tangent geometry and original-focus inverse edge identity; complete Jacobi fibers and N3 order; pointwise quadratic cancellation; two-pole torus divisor and opposite-focus half-period',source_domain='Strict nondegenerate confocal ellipse pair a>b>0; every odd least period N>=3 and every coprime star turning number; repeated odd traversals by r^2 area-product scaling',mathematical_gaps_identified=[],required_documentary_clarifications=['Explicit repeated-odd-traversal corollary','Reconcile stale pending metadata while preserving historical originals','Retain exact arXiv-v11 versus smaller journal-companion distinction and actual10/20 table date','Do not propagate Stachel auxiliary dn real-shift typo'],priority_verdict='not yet audited',preprint_preparation_cleared=False,preprint_upload_cleared=False,counts=[42,19,19,0],completion_percent=35,full_goal_active_incomplete=True)
(D/'ROOT_MATHEMATICAL_SOURCE_ACCEPTANCE.json').write_text(json.dumps(result,indent=2)+'\n')
state=json.loads((D/'CURRENT_AUDIT_STATE.json').read_text());state.update(utc=t,stage='mathematics_and_source_accepted_extensive_priority_pending',mathematical_verdict=result['status'],source_verdict='PASS for exact source object and regular confocal ellipse domain',completion_percent=35);(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
g=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text());g.update(utc=t,current_stage=state['stage'],mathematical_verdict=result['status'],source_verdict=state['source_verdict'],case_completion_percent=35,mathematical_repairs_required=[],documentary_clarifications_required=result['required_documentary_clarifications']);(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(g,indent=2)+'\n')
line='\n## '+t+' — PR211 mathematical/source checkpoint35%\n\nThree new independent mathematical/source families sealed, all authored hashes validated, full derivations/reports/source inputs independently read and checked by root. All five programs reproduced in isolated folders with byte-identical receipts: author and inherited controls, new Cartesian source suite, new geometry and complete meromorphic suites. Exact all-period proof accepted for original-focus outer signed-area product, all primitive odd stars/N3, with explicit repeated-odd extension. No mathematical blocker; documentary repetition/status/source clarifications retained. Historical priority remains unevaluated, no paper/deposit/tracker/Queue/PR mutation or publication clearance. Counts42/19/19/0, held293/292/280/239 unchanged, full goal active/incomplete.\n'
for path in [D/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with path.open('a') as f:f.write(line)
print(json.dumps(result,indent=2))

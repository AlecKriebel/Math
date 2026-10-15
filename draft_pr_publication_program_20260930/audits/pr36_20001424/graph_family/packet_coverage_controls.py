#!/usr/bin/env python3
"""Execute unchanged original checks against actual source/prose/output corruptions.
All mutations occur privately; each observed blind spot is recorded, not promoted.
A SHA binding detects only edits to a pinned artifact, not mathematical correctness.
"""
from pathlib import Path
import subprocess,sys,json,hashlib,datetime,shutil
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
SOURCE=AUDIT/'source_snapshot'
FROZEN=json.loads((AUDIT/'snapshot_manifest.json').read_text())
PINS={r['path']:r['sha256'] for r in FROZEN['files']}
def digest(b):return hashlib.sha256(b).hexdigest()
def read_payload():return {p:(SOURCE/p).read_bytes() for p in PINS}
def bind(data):return {p:digest(data[p])==h for p,h in PINS.items()}
def original_runs(work):
 rows=[]
 for code,receipt in [('verify_graph.py','graph_verification.json'),('review/independent_checks.py','review/independent_results.json')]:
  p=subprocess.run([sys.executable,str(work/code)],cwd=work,capture_output=True)
  rows.append({'code':code,'exit':p.returncode,'stdout_sha256':digest(p.stdout),'stdout_exact_original':p.stdout==(SOURCE/receipt).read_bytes(),'stdout_full_json_exact_original':json.loads(p.stdout)==json.loads((SOURCE/receipt).read_bytes()) if p.returncode==0 else False,'stderr':p.stderr.decode()})
 return rows
def materialize(path,data):
 path.mkdir(parents=True,exist_ok=True)
 for name,b in data.items():
  p=path/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def mutate_json(data,path,callback):
 obj=json.loads(data[path]);callback(obj);data[path]=(json.dumps(obj,indent=2)+'\n').encode()
def main():
 data=read_payload();baseline=bind(data);assert all(baseline.values())
 mutants=[]
 def execute(name,fn,expected_original_pass=True):
  altered=dict(data);fn(altered)
  work=HERE/'executed_controls'/name;materialize(work,altered)
  runs=original_runs(work);fails=[p for p,ok in bind(altered).items() if not ok]
  assert fails
  if expected_original_pass:assert all(r['exit']==0 and r['stdout_exact_original'] and r['stdout_full_json_exact_original'] for r in runs)
  else:assert any(r['exit']!=0 for r in runs)
  row={'name':name,'actual_materialized_path':str(work.relative_to(HERE)),'mutant_hashes':{p:digest(altered[p]) for p in fails},'pinned_artifact_binding_rejects':fails,'unchanged_original_check_execution':runs,'original_code_covers_changed_source':not expected_original_pass,'interpretation':'Finite graph-checker blind spot; artifact hash rejects changed payload, not false mathematics.' if expected_original_pass else 'Corrupted hardcoded graph data rejects during original assertions.'}
  (work/'execution_receipt.json').write_text(json.dumps(row,indent=2)+'\n');mutants.append(row)
 def literal(d):
  def change(o):
   for k in ('statement','original_statement','clean_statement'):o['problem'][k]='Are all rigid PCF maps with odd postcritical cardinality defined over their field of moduli?'
  mutate_json(d,'source_record.json',change)
 execute('literal_target_narrowed',literal)
 def false_degree(d):
  before=b'There exists a degree-11 rational map';after=b'There exists a degree-12 rational map';assert before in d['CANDIDATE.md'];d['CANDIDATE.md']=d['CANDIDATE.md'].replace(before,after,1)
 execute('false_candidate_degree12',false_degree)
 def false_arc(d):
  before=b'Therefore these Tischler faces are paired without fixed faces.'
  after=b'Therefore these Tischler faces are fixed individually by A, and choosing arbitrary arcs in them automatically gives an A-invariant graph.'
  assert before in d['CANDIDATE.md'];d['CANDIDATE.md']=d['CANDIDATE.md'].replace(before,after,1)
 execute('false_candidate_equivariant_arcs',false_arc)
 def fake_aut(d):
  before=b'its holomorphic dynamical automorphism group is trivial.'
  # Upper-case source phrase occurs in numbered main claim.
  before=b'Its holomorphic dynamical automorphism group is trivial.'
  assert before in d['CANDIDATE.md'];d['CANDIDATE.md']=d['CANDIDATE.md'].replace(before,b'Its holomorphic dynamical automorphism group has order 2.',1)
 execute('false_candidate_nontrivial_aut',fake_aut)
 def saved_receipt(d):mutate_json(d,'graph_verification.json',lambda o:o.update(ramification_total=19))
 execute('saved_receipt_ramification19',saved_receipt)
 def bad_svg(d):
  before=b'cx="120" cy="180"';assert before in d['graph.svg'];d['graph.svg']=d['graph.svg'].replace(before,b'cx="110" cy="180"',1)
 execute('diagram_coordinate_corruption',bad_svg)
 def ref(d):
  def bad(o):o['reference_hashes']['hlushchanka2019.pdf']='0'*64
  mutate_json(d,'source_manifest.json',bad)
 execute('primary_reference_hash_corruption',ref)
 def rot(d):
  before=b'if i<2 else';assert before in d['verify_graph.py'];d['verify_graph.py']=d['verify_graph.py'].replace(before,b'if i<3 else',1)
 execute('hardcoded_rotation_corruption',rot,False)
 def coord(d):
  before=b'(-2,0),(0,-2),(0,-3)';assert before in d['review/independent_checks.py'];d['review/independent_checks.py']=d['review/independent_checks.py'].replace(before,b'(-3,0),(0,-2),(0,-3)',1)
 execute('old_review_coordinate_corruption',coord,False)
 # Actual operative primary-source text corruption, distinct from numeric-ID statement corruption.
 primary=HERE/'private_sources/hlushchanka.txt'
 if primary.exists():
  text=primary.read_text();before='connected planar\nembedded graphs with at least one edge and no loops.'
  assert before in text
  altered=text.replace(before,'possibly disconnected planar\nembedded graphs with at least one edge, including loops.',1)
  work=HERE/'executed_controls/operative_primary_theorem_corruption';materialize(work,data)
  (HERE/'private_sources/operative_theorem_source_mutant.txt').write_text(altered)
  runs=original_runs(work)
  assert all(r['exit']==0 and r['stdout_exact_original'] for r in runs)
  mutants.append({'name':'operative_primary_theorem_corruption','actual_materialized_path':str(work.relative_to(HERE)),'source_before_sha256':digest(text.encode()),'source_after_sha256':digest(altered.encode()),'source_binding_detects_difference':digest(text.encode())!=digest(altered.encode()),'unchanged_original_check_execution':runs,'original_code_covers_primary_theorem_text':False,'interpretation':'The disconnected/loop-inclusive classification is false: source binding records text corruption, graph checkers do not read it. No mathematical theorem is certified by hash equality.'})
 # Repeat self-authored exact independent audit. This has no claim to detecting source prose.
 independent=subprocess.run([sys.executable,str(HERE/'independent_graph_audit.py')],cwd=HERE,capture_output=True)
 assert independent.returncode==0
 # Necessary finite boundary diagnostics showing source hypotheses matter.
 disconnected_edges=[(2*k,2*k+1) for k in range(5)]
 disconnected_vertices={v for edge in disconnected_edges for v in edge}
 disconnected_degree=len(disconnected_edges)+1
 assert len(disconnected_vertices)>disconnected_degree+1
 loop_edges=[(0,0)];loop_valence=sum(edge.count(0) for edge in loop_edges);loop_degree=len(loop_edges)+1
 assert loop_valence+1>loop_degree
 boundary={'five_disjoint_edges':{'connected':False,'vertices':10,'edges':5,'blowup_degree':6,'fixed_point_form_degree':7,'critical_fixed_vertices':10,'realization_impossible_by_10_distinct_fixed_points_exceeding_degree7_form':True},'one_loop':{'loopless':False,'vertices':1,'edges':1,'blowup_claim_degree':2,'loop_vertex_valence':2,'claimed_local_degree':3,'local_degree_exceeds_total_degree':True},'notes':'These concrete controls falsify overgeneralized hypotheses. They are not a proof of the universal realization theorem.'}
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_pinned_payload_intact':all(baseline.values()),'original_payload_files':len(PINS),'original_research_attempts_added':0,'mutants_actually_executed':mutants,'meaningful_exact_boundary_controls':boundary,'independent_finite_audit_rerun_exit':independent.returncode,'code_coverage_boundary':'Both original scripts hardcode their graph/coordinates. They read neither CANDIDATE, source_record, source_manifest, diagram, nor saved JSON receipts. A passing execution therefore does not detect false prose, a narrowed target, or corrupted source citations. Full-byte replay comparisons and pinned artifact bindings add reproducibility coverage only; written proof and primary-source reading supply mathematical coverage.'}
 (HERE/'packet_coverage_results.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'mutants_actually_executed':len(mutants),'false_prose_and_source_controls_unnoticed_by_original_code':sum(r.get('original_code_covers_changed_source')==False for r in mutants)+sum(r.get('original_code_covers_primary_theorem_text')==False for r in mutants),'hardcoded_data_controls_rejected':sum(r.get('original_code_covers_changed_source')==True for r in mutants),'pins_reject_every_original_artifact_mutant':all(r.get('pinned_artifact_binding_rejects',True) for r in mutants),'finite_boundaries_executed':True},indent=2))
if __name__=='__main__':main()

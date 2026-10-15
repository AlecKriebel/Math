#!/usr/bin/env python3
"""Frozen original16 byte binding, unchanged replays, full receipts, independent crosschecks."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,subprocess,sys,shutil,datetime,xml.etree.ElementTree as XML
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
SOURCE=AUDIT/'source_snapshot'
sha=lambda b:hashlib.sha256(b).hexdigest()
def cycle(xs):return min(tuple(xs[k:]+xs[:k]) for k in range(len(xs)))
def main():
 m=json.loads((AUDIT/'snapshot_manifest.json').read_text());bindings=[]
 for row in m['files']:
  b=(SOURCE/row['path']).read_bytes()
  git=subprocess.run(['git','show',m['head']+':unsolved_math_prioritization/attempts/20001424/'+row['path']],capture_output=True,check=True).stdout
  blob=subprocess.run(['git','hash-object','--stdin'],input=b,capture_output=True,check=True).stdout.decode().strip()
  item={'path':row['path'],'sha256':sha(b),'size':len(b),'snapshot_hash_matches':sha(b)==row['sha256'],'git_head_byte_matches':git==b,'git_blob_matches':blob==row['git_blob']}
  assert all(item[k] for k in ('snapshot_hash_matches','git_head_byte_matches','git_blob_matches'));bindings.append(item)
 assert len(bindings)==16
 diff=(AUDIT/'pr_input/diff.patch').read_bytes();paths=[line.decode().split(' b/',1)[1] for line in diff.splitlines() if line.startswith(b'diff --git ')]
 assert sha(diff)==m['diff_sha256'] and len(diff)==m['diff_bytes'] and paths==m['changed_paths'] and len(paths)==17
 replay=HERE/'original_replay';replay.mkdir(exist_ok=True);(replay/'review').mkdir(exist_ok=True);receipts=[]
 for code,res in [('verify_graph.py','graph_verification.json'),('review/independent_checks.py','review/independent_results.json')]:
  shutil.copyfile(SOURCE/code,replay/code)
  run=subprocess.run([sys.executable,str(replay/code)],cwd=replay,capture_output=True)
  (replay/res).write_bytes(run.stdout);(replay/(code.replace('/','_')+'.stderr.txt')).write_bytes(run.stderr)
  before=(SOURCE/res).read_bytes()
  row={'code':code,'result':res,'exit':run.returncode,'unchanged_source_bytes':(replay/code).read_bytes()==(SOURCE/code).read_bytes(),'stdout_byte_exact':run.stdout==before,'stdout_json_full_exact':json.loads(run.stdout)==json.loads(before),'stderr_empty':not run.stderr,'source_sha256':sha((SOURCE/code).read_bytes()),'receipt_sha256':sha(run.stdout)}
  assert run.returncode==0 and row['unchanged_source_bytes'] and row['stdout_byte_exact'] and row['stdout_json_full_exact'] and row['stderr_empty'];receipts.append(row)
 summary=json.loads((SOURCE/'review/review_summary.json').read_text())
 links={key:sha((SOURCE/path).read_bytes())==summary[key] for key,path in [('reviewed_sha256','CANDIDATE.md'),('review_sha256','review/REVIEW.md'),('independent_check_sha256','review/independent_checks.py'),('independent_receipt_sha256','review/independent_results.json')]};assert all(links.values())
 status=json.loads((SOURCE/'status.json').read_text())
 statuslinks={k:sha((SOURCE/path).read_bytes())==status[k] for k,path in [('proof_sha256','CANDIDATE.md'),('verifier_sha256','verify_graph.py'),('review_sha256','review/REVIEW.md')]};assert all(statuslinks.values())
 refs=json.loads((SOURCE/'source_manifest.json').read_text())['reference_hashes']
 foreign=HERE/'private_sources/hlushchanka.pdf';hhash=sha(foreign.read_bytes()) if foreign.exists() else None
 if hhash:assert hhash==refs['hlushchanka2019.pdf']
 svg=XML.parse(SOURCE/'graph.svg').getroot();circles=svg.findall('.//{http://www.w3.org/2000/svg}circle')
 points=[(Q(1),Q(0)),(Q(0),Q(1)),(Q(-1),Q(0)),(Q(0),Q(-1)),(Q(1,2),Q(0)),(Q(0),Q(1,2)),(Q(0),Q(1,3)),(Q(-2),Q(0)),(Q(0),Q(-2)),(Q(0),Q(-3))]
 positions=[(Q(c.attrib['cx']),Q(c.attrib['cy'])) for c in circles[1:]]
 expected=[(270+75*x,180-75*y) for x,y in points];assert positions==expected
 assert circles[0].attrib=={'cx':'270','cy':'180','r':'75'}
 path=svg.findall('.//{http://www.w3.org/2000/svg}path')[0].attrib['d']
 assert path=='M345 180 L307.5 180 M270 105 L270 142.5 L270 155 M195 180 L120 180 M270 255 L270 330 L270 405'
 ind=json.loads((HERE/'independent_graph_results.json').read_text());a=json.loads((SOURCE/'graph_verification.json').read_text());b=json.loads((SOURCE/'review/independent_results.json').read_text())
 ours={tuple(r['permutation']):r['local_signs'] for r in ind['original']['abstract_automorphisms']}
 assert ours=={tuple(r['vertex_images']):r['root_orientation_signs'] for r in a['automorphisms']}
 assert ours=={tuple(r['vertex_images']):r['trivalent_signs'] for r in b['automorphisms']}
 assert all(cycle(a['rotation_system'][str(v)])==cycle(b['exact_coordinate_rotations'][str(v)])==cycle(ind['rotation'][str(v)]) for v in range(10))
 assert {cycle([tuple(d) for d in f]) for f in ind['original']['faces']}=={cycle([tuple(d) for d in f]) for f in a['face_boundaries']}
 assert a['critical_local_degrees']==b['critical_local_degrees'] and a['candidate_degree']==b['degree']==11 and a['ramification_total']==b['ramification_total']==20
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_head':m['head'],'frozen_base':m['base'],'diff17_exact_binding':{'sha256':sha(diff),'size':len(diff),'paths':paths},'all_original_16_files_bound':bindings,'unchanged_original_code_replays':receipts,'review_summary_hash_links':links,'status_hash_links':statuslinks,'current_hlushchanka_v2_pdf_sha256':hhash,'hlushchanka_manifest_hash_matches':hhash==refs['hlushchanka2019.pdf'] if hhash else None,'other_four_foreign_reference_hashes':'Not reretrieved by this graph family; no claim to reproducing them.','diagram_marker_affine_binding_exact':True,'diagram_circle_and_paths_exact':True,'independent_vs_original_full_automorphism_sign_maps_match':True,'independent_vs_original_rotations_cyclic_exact':True,'independent_vs_original_face_cycles_exact_up_to_start':True,'old_review_full_receipt_assertions':b['assertions'],'old_review_full_receipt_search_nodes':b['search_nodes']}
 (HERE/'original_binding_and_replay.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'all_original16_git_and_hash_match':True,'diff17_hash_and_path_list_match':True,'both_original_code_replays_byte_exact':True,'old_review_status_hash_links_pass':True,'hlushchanka_pdf_matches_original_manifest':result['hlushchanka_manifest_hash_matches'],'diagram_exact_coordinate_binding':True,'independent_crosschecks_pass':True},indent=2))
if __name__=='__main__':main()

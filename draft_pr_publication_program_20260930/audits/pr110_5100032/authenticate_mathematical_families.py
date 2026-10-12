from pathlib import Path
import json,hashlib,os,datetime
A=Path(__file__).resolve().parent;C=A.parents[2]
def need(x,m):
 if not x:raise RuntimeError(m)
def pin(p):b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def cp(p):return {'path':str(p.relative_to(C)),**pin(p)}
families=[]
for name,sha in [('algebraic_identity_adversary_20261006','d3155bbd8744941887e9c2ec24c6a7a8ad9bafb89f2e91ea50c53925b16e890a'),('geometric_edge_cases_adversary_20261006','3ecaf65a0a7c5275e4a4ee3958a92de4219be30ffafc543e31b20199621f127b'),('literal_source_scope_adversary_20261006','67a62d911122d332edb93ff466e1a7ac69a4ce2dad3eef05ef2cc703a330e4a5')]:
 D=A/name;m=json.loads((D/'OUTPUT_MANIFEST.json').read_bytes());v=json.loads((D/'VERDICT.json').read_bytes());seal=json.loads((D/'SEAL_RECEIPT.json').read_bytes())
 need(pin(D/'OUTPUT_MANIFEST.json')['sha256']==sha,'Manifest seal')
 need(v['required_findings']==v['optional_findings']==[],'Unresolved verdict findings')
 for metadata in [m,seal]:
  if 'required_findings' in metadata:need(metadata['required_findings']==metadata['optional_findings']==[],'Unresolved explicit envelope findings')
 for r in m['files']:
  rel=r.get('path',r.get('relative_path'));need(pin(D/rel)=={k:r[k] for k in ['bytes','sha256']},'Payload changed '+rel);need(not rel.startswith(('private_review_materials/','private_source_extracts/')),'Private source in public manifest')
 for role in ['REPORT','VERDICT']:
  r=seal[role];need(pin(D/r.get('path',r.get('relative_path')))=={k:r[k] for k in ['bytes','sha256']},'Report seal changed')
 families.append({'family':name,'REPORT':cp(D/'REPORT.md'),'VERDICT':cp(D/'VERDICT.json'),'OUTPUT_MANIFEST':cp(D/'OUTPUT_MANIFEST.json'),'SEAL_RECEIPT':cp(D/'SEAL_RECEIPT.json'),'payload_count':len(m['files']),'required_findings':[],'optional_findings':[],'root_complete_REPORT_VERDICT_read':True})
D=A/'algebraic_identity_adversary_20261006';p=json.loads((D/'EXACT_CONTROL_PROCESS_RECEIPTS.json').read_bytes())['processes']
for r,pid in zip(p,[1080,1081]):
 mode=r['mode'];need(r['PID']==pid and r['exit_code']==0 and r['reaped'] and not r['timed_out'],'Algebra actual')
 for k,suffix in [('stdout','json'),('stderr','txt')]:need(pin(D/(mode+'.'+k+'.'+suffix))=={'bytes':r[k+'_bytes'],'sha256':r[k+'_sha256']},'Algebra streams')
 x=json.loads((D/(mode+'.stdout.json')).read_bytes());need(x['PID']==pid and x['checks']==699 and x['purposeful_admissible_cases']==15 and x['negative_controls_detected']==33,'Algebra controls')
D=A/'geometric_edge_cases_adversary_20261006'
for mode,pid in [('normal',1558),('optimized',2256)]:
 R=D/'process_receipts'/('controls_'+mode);r=json.loads((R/'RECEIPT.json').read_bytes());need(r['child_pid']==pid and r['exit_code']==0 and r['reaped'],'Geometry actual')
 for n,q in r['full_output_pins'].items():need(pin(R/n)==q,'Geometry streams')
 x=json.loads((R/'stdout.txt').read_bytes());need(x['checks']==4037 and x['mode']==mode and len(x['exact_chords'])==21 and len(x['closed_cycle_controls'])==9,'Geometry controls')
R=D/'process_receipts/seal_final';r=json.loads((R/'RECEIPT.json').read_bytes());need(r['child_pid']==5702 and r['exit_code']==0 and r['reaped'],'Actual geometry sealer')
for n,q in r['full_output_pins'].items():need(pin(R/n)==q,'Sealer outputs')
D=A/'literal_source_scope_adversary_20261006';rows=json.loads((D/'PROCESS_JOURNAL.json').read_bytes());need(len(rows)==15 and all(r['exit_code']==0 for r in rows),'Source actualprocesses')
for r,pid in zip(rows[-2:],[935,936]):
 need(r['actual_child_PID']==pid,'Source modePID')
 for k in ['stdout','stderr']:need(pin(D/r[k]['path'])=={t:r[k][t] for t in ['bytes','sha256']},'Source control streams')
for f,pid in [('EXACT_SCOPE_CONTROLS.json',935),('EXACT_SCOPE_CONTROLS_OPTIMIZED.json',936)]:
 x=json.loads((D/f).read_bytes());need(x['actual_operator_PID']==pid and x['checks']==83,'Source controls')
O=A/'original_head_authentication_20261006/original_attempt';sourcepair=json.loads((A/'original_head_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json').read_bytes());body=pin(O/'PROOF.md');need(body=={'bytes':6990,'sha256':'8478d2a792944c5fb9e8a53324e0c6bce8eba317de29c31a6fcbd6ca0205709d'},'Proof changed')
auth={'schema':'pr110-root-three-independent-mathematical-families-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'families':families,'all_65_payloads_and_closing_envelopes_authenticated':True,'root_complete_REPORT_VERDICT_read':True,'normal_optimized_checks_by_family':{'algebra':699,'geometry':4037,'literal_source_scope':83},'required_mathematical_findings':[],'optional_mathematical_findings':[],'original_budget':'2/5','new_central_proof_search_turns':0,'original_PROOF':cp(O/'PROOF.md'),'mathematical_clearance':True,'priority_or_publication_clearance':False}
(A/'ROOT_MATHEMATICAL_FAMILY_AUTHENTICATION_20261006.json').write_text(json.dumps(auth,sort_keys=True,indent=2)+'\n')
gate={'schema':'pr110-root-complete-literal-source-mathematical-gate/v1','UTC':auth['UTC'],'actual_operator_PID':os.getpid(),'PR':110,'id':5100032,'code':'AMR-050-0032','original_head':'3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35','review_hash':sourcepair['catalog_selected']['review_hash'],'statement_hash':sourcepair['catalog_selected']['statement_hash'],'dataset_revision':sourcepair['dataset_revision'],'original_status':'claimed_solved','original_effort':'2/5','original_prior_report_nonempty_and_preserved':True,'new_central_proof_search_turns':0,'exact_claim':'For every regular closed billiard/Poncelet orbit between an outer ellipse a>b>0 and a fixed strictly nested confocal ellipse 0<lambda<b², the sums of ordinary Euclidean distances from each outer focus to consecutive antipedal supporting-line intersections are finite, positive and equal; literal k603 ratio1, all admissible periods/windings, including stars, reversals and repeated traversals.','root_independent_derivation':cp(A/'ROOT_INDEPENDENT_DERIVATION_20261006.md'),'original_PROOF':cp(O/'PROOF.md'),'full_sourcepair_authentication':cp(A/'original_head_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json'),'fresh_family_authentication':cp(A/'ROOT_MATHEMATICAL_FAMILY_AUTHENTICATION_20261006.json'),'primary_download_pins':cp(A/'PRIMARY_SOURCE_DOWNLOAD_PINS_20261006.json'),'source_and_mathematics_percent':100,'mathematical_clearance':True,'required_mathematical_findings':[],'priority_clearance':False,'novelty_established':False,'publication_ready':False,'operational_checksum_repair':cp(A/'ROOT_ORIGINAL_STALE_README_CHECKSUM_FINDING_20261006.json'),'required_later_package_propagations':['Use repaired current README checksum while retaining historical original SHA256SUMS.','Publication verification checks must remain effective under Python optimization; historical assertion counts are normal-mode evidence only.'],'next_step':'Deep independent priority audit against current primary literature and prior general mechanisms. No paper or publication until bounded novelty established.'}
(A/'ROOT_MATHEMATICAL_GATE_20261006.json').write_text(json.dumps(gate,sort_keys=True,indent=2)+'\n');print(json.dumps({'math_source_clearance':True,'root_actual_PID':os.getpid(),'families':3,'checks_each_mode':4819,'priority_clearance':False}))


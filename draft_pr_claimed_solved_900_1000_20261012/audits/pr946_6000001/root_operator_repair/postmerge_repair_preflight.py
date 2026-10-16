"""Read-only actual postmerge closure after operator02 repairs; not approval."""
import sys
if not sys.flags.isolated or not sys.flags.no_site or sys.flags.optimize or not sys.dont_write_bytecode:
    raise RuntimeError('Use -I -S -B')
import ast,hashlib,json
from pathlib import Path
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012'
A=P/'audits/pr946_6000001';D=A/'preprint';O=A/'root_operator_repair'
fp=lambda b:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
raw=(P/'accept_pr946.py').read_bytes()
if fp(raw)['sha256']!='8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7':raise RuntimeError('Core drift')
N={'__name__':'_root_operator02_readonly_preflight_','__file__':str(P/'accept_pr946.py')}
exec(compile(raw,N['__file__'],'exec',dont_inherit=True,optimize=0),N)
context=N['capture_inventory']('f4742eca6ddd628ecac1e704fed772a17837d42d4d0fdef42c73d3cda3bed254')
freeze_pin='9af8f2570af53b6a6658a7998ac08927829c8747be7c764a8d2c392dc6c6afe1'
freeze=N['freeze_check'](N['read_regular'](D/'FREEZE.json'),freeze_pin,context)
accepted=N['load'](A/'ACCEPTANCE.json')
N['need'](len(accepted['full_package_reviews'])==6,'original six-round approval must remain unchanged')
destination=N['merged_gate'](accepted,freeze);_,originals=N['original_check']()
archive=N['archive_check'](freeze,originals)
chain=N['load'](A/'ROOT_FULL_REVIEW_07_CHAIN_VERIFICATION.json')
N['need'](chain['status']=='PASS_ADVERSE_PACKET_INTEGRITY' and chain['ready_to_approve'] is False,'adverse seventh review preserved')
specs=[f"{row['round']:02d}:"+row['manifest_sha256'] for row in chain['all_review_packets']]
N['candidate_state_check'](freeze,freeze_pin,context)
N['review_state_check'](specs,freeze,freeze_pin,context)
operator=N['read_regular'](A/'publication_operator.py')
N['need'](fp(operator)=={'bytes':9912,'sha256':'d085ec080ee6c2f1239f49f724e7a71ef6d86b3d994fbe9b4039371181a61aef'},'repaired operator external pin')
N['need'](operator==N['read_regular'](A/'publication_operator_versions/operator02.py'),'version02 preservation')
old=ast.parse(N['read_regular'](A/'publication_operator_versions/operator01.py'))
new=ast.parse(operator)
unchanged=[]
for left,right in zip(old.body,new.body):
    if isinstance(left,(ast.FunctionDef,ast.ClassDef)) and left.name not in ['run','ExistingDraftClient']:
        N['need'](ast.dump(left)==ast.dump(right),'unexpected function change '+left.name);unchanged.append(left.name)
unit=N['load'](A/'PUBLICATION_OPERATOR_TESTS.json')
baseline=N['load'](O/'OPERATOR_INTEGRATION.json');repaired=N['load'](O/'REPAIRED_OPERATOR_INTEGRATION.json')
N['need'](unit['status']=='PASS' and unit['case_count']==36 and unit['operator_sha256']==fp(operator)['sha256'],'focused tests')
N['need'](baseline['status']=='NONCLEAN' and baseline['case_count']==11 and repaired['status']=='PASS' and repaired['case_count']==24,'independent old/new controls')
N['need'](baseline['actual_external_mutations']==repaired['actual_external_mutations']==0,'fake services only')
record={'utc':N['utc_now'](),'status':'PASS_ACTUAL_POSTMERGE_REPAIR_PREFLIGHT_NOT_APPROVAL',
    'scientific_candidate_revision':6,'freeze_sha256':freeze_pin,'scientific_payloads':len(freeze['files']),
    'immutable_evidence':len(freeze['evidence_files']),'old_seven_dependencies_unchanged':True,
    'operator01':fp(N['read_regular'](A/'publication_operator_versions/operator01.py')),
    'operator02':fp(operator),'unchanged_operator_functions':unchanged,
    'changed_operator_scope':['startup no_site requirement','final-GET closure before POST/return','additional source/reviewer identity at every closing guard'],
    'original_six_round_approval_preserved':True,'seventh_adverse_packet_preserved':True,
    'fresh_merged_destination':destination,'originals':33,'archive':archive,
    'focused_tests':36,'independent_old_cases':11,'independent_repaired_cases':24,
    'new_entire_review_required':8,'required_prior_issue_count':34,
    'publication_permitted':False,'external_mutations':0,'new_proof_responses':0}
N['save'](A/'ROOT_OPERATOR02_POSTMERGE_PREFLIGHT.json',record,exclusive=True)
print(json.dumps({'status':record['status'],'operator':fp(operator),'fresh_main':destination['observed_remote_main'],'publication_permitted':False}))

"""Root's read-only PR946 chain authentication; never accepts or publishes."""
import sys
if not sys.flags.isolated:raise RuntimeError('Use Python -I -B')
import argparse,hashlib,json
from pathlib import Path
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';D=A/'preprint'
p=argparse.ArgumentParser();p.add_argument('--core-sha256',required=True);p.add_argument('--operations-sha256',required=True);p.add_argument('--freeze',required=True);p.add_argument('--review',action='append',required=True);p.add_argument('--output',required=True);args=p.parse_args()
source=P/'accept_pr946.py';raw=source.read_bytes()
if hashlib.sha256(raw).hexdigest()!=args.core_sha256:raise RuntimeError('External root core pin differs')
N={'__name__':'_root_readonly_review_auth_','__file__':str(source)};exec(compile(raw,str(source),'exec',dont_inherit=True,optimize=0),N)
context=N['capture_inventory'](args.operations_sha256);freeze=N['freeze_check'](N['read_regular'](D/'FREEZE.json'),args.freeze,context);N['disposition_check']();pr,parent,sg,originals=N['premerge_gate'](freeze,require_draft=True);N['archive_check'](freeze,originals)
# Public packet capture and authentication precede assessment of its verdict.
packets=[]
for item in args.review:
 number,pin=item.split(':');folder=A/'reviews'/('full_package_'+number);raw=N['read_regular'](folder/'MANIFEST.json');N['need'](N['sha'](raw)==pin,'external root review manifest pin');mapping=N['strict_json'](raw);files=mapping['files'];N['need'](set(files)==set(mapping['explicit_public_allowlist']),'review exact public allowlist')
 for name,want in files.items():N['need'](N['safe'](name),'safe review name');N['read_regular'](folder/name,pin=want)
 result=N['load'](folder/'RESULT.json');packets.append({'round':number,'manifest_sha256':pin,'public_payloads':len(files),'result':result})
reviews,latest=N['review_check'](args.review,freeze,args.freeze,context,originals)
pr,parent,sg,originals=N['premerge_gate'](freeze,require_draft=True);N['require_complete_review_history'](args.review);pr.pop('body',None)
record={'utc':N['utc_now'](),'status':'PASS_READONLY_FULL_CHAIN_GATES','pr':946,'problem_id':'6000001','freeze_sha256':args.freeze,'operations_inventory_sha256':args.operations_sha256,'candidate_revision':freeze['revision_candidate'],'all_review_packets':packets,'authenticated_review_chain':reviews,'latest_exact_theorem':latest['strongest_verified_theorem'],'live_PR':pr,'fresh_main':parent,'fresh_source_gate':sg,'all33_actual_original_Git_disk_archive_checked':True,'all_prior_required_optional_findings_resolved':True,'canonical_review_history_complete':True,'acceptance_created':False,'external_mutations':0,'new_proof_responses':0}
output=A/args.output;N['need'](output.parent==A and args.output.endswith('.json'),'own simple receipt name');N['save'](output,record,exclusive=True);print(json.dumps({'status':record['status'],'rounds':len(reviews),'candidate_revision':freeze['revision_candidate'],'latest_theorem':latest['strongest_verified_theorem'],'fresh_main':parent,'acceptance_created':False}))

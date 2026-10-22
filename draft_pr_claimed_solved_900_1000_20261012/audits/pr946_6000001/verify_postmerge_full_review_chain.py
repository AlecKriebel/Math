"""Root read-only postmerge authentication; never approves or publishes.

An expected nonclean terminal result authenticates a completed adverse packet,
not permission to proceed. All acceptance/publication guards remain unchanged.
"""
import sys
if not sys.flags.isolated or not sys.flags.no_site or sys.flags.optimize or not sys.dont_write_bytecode:
    raise RuntimeError('Use Python -I -S -B at optimization zero')
import argparse, hashlib, json
from pathlib import Path
R=Path('/Users/alec/Documents/Math')
P=R/'draft_pr_claimed_solved_900_1000_20261012'
A=P/'audits/pr946_6000001';D=A/'preprint'
p=argparse.ArgumentParser(description=__doc__)
for name in ['core-sha256','operations-sha256','freeze','operator-sha256','output']:
    p.add_argument('--'+name,required=True)
p.add_argument('--review',action='append',required=True)
p.add_argument('--expected-nonclean',action='store_true')
args=p.parse_args()
source=P/'accept_pr946.py';raw=source.read_bytes()
if hashlib.sha256(raw).hexdigest()!=args.core_sha256:
    raise RuntimeError('External core pin differs')
N={'__name__':'_root_postmerge_readonly_','__file__':str(source)}
exec(compile(raw,str(source),'exec',dont_inherit=True,optimize=0),N)
context=N['capture_inventory'](args.operations_sha256)
freeze=N['freeze_check'](N['read_regular'](D/'FREEZE.json'),args.freeze,context)
N['disposition_check']()
accepted=N['load'](A/'ACCEPTANCE.json')
destination=N['merged_gate'](accepted,freeze)
N['need'](destination['merge_commit']=='918948421d00b1184a88ca07017134726b466adb','exact actual merged result')
_,originals=N['original_check']();N['archive_check'](freeze,originals)
packets=[]
for spec in args.review:
    number,pin=spec.split(':');folder=A/'reviews'/('full_package_'+number)
    seal=N['read_regular'](folder/'MANIFEST.json')
    N['need'](N['sha'](seal)==pin,'external complete packet seal')
    manifest=N['strict_json'](seal)
    N['need'](set(manifest['files'])==set(manifest['explicit_public_allowlist']), 'complete public allowlist')
    for name,want in manifest['files'].items():
        N['need'](N['safe'](name),'safe review member')
        N['read_regular'](folder/name,pin=want)
    latest=N['load'](folder/'RESULT.json')
    packets.append({'round':int(number),'manifest_sha256':pin,
        'public_payloads':len(manifest['files']),'required_issues':latest['required_issues'],
        'optional_issues':latest['optional_issues']})
operator=N['read_regular'](A/'publication_operator.py')
N['need'](N['sha'](operator)==args.operator_sha256 and N['exact'](
    latest.get('inspected_publication_operator'),N['fingerprint'](operator)),
    'latest complete reviewer exact separate operator pin')
checked=None;expected_rejection=None
try:
    checked,last=N['review_check'](args.review,freeze,args.freeze,context,originals)
except RuntimeError as error:
    N['need'](args.expected_nonclean and str(error)==
        'PR946 guard: latest complete review must clear exact current package with no findings',
        'unexpected full-chain rejection: '+str(error))
    expected_rejection=str(error)
if args.expected_nonclean:
    N['need'](expected_rejection is not None and latest['clean_for_preprint'] is False
        and bool(latest['required_issues']+latest['optional_issues']),
        'nonclean packet must actually reject readiness')
else:
    N['need'](expected_rejection is None and checked is not None,'clean full chain required')
destination=N['merged_gate'](accepted,freeze)
N['original_check']();N['archive_check'](freeze,originals)
N['candidate_state_check'](freeze,args.freeze,context)
N['review_state_check'](args.review,freeze,args.freeze,context)
N['read_regular'](A/'publication_operator.py',pin=N['fingerprint'](operator))
record={'utc':N['utc_now'](),'status':'PASS_ADVERSE_PACKET_INTEGRITY' if args.expected_nonclean else 'PASS_READONLY_FULL_CHAIN_GATES',
    'pr':946,'problem_id':'6000001','candidate_revision':freeze['revision_candidate'],
    'freeze_sha256':args.freeze,'operations_inventory_sha256':args.operations_sha256,
    'publication_operator':N['fingerprint'](operator),'all_review_packets':packets,
    'authenticated_review_chain':checked,'latest_result':latest,
    'expected_readiness_rejection':expected_rejection,'ready_to_approve':not args.expected_nonclean,
    'fresh_merged_destination':destination,'originals_checked':33,
    'acceptance_created_or_changed':False,'external_mutations':0,'new_proof_responses':0}
output=A/args.output
N['need'](output.parent==A and args.output.endswith('.json'),'own simple receipt name')
N['save'](output,record,exclusive=True)
print(json.dumps({'status':record['status'],'rounds':len(packets),
    'ready_to_approve':record['ready_to_approve'],'acceptance_changed':False,
    'fresh_main':destination['observed_remote_main']}))

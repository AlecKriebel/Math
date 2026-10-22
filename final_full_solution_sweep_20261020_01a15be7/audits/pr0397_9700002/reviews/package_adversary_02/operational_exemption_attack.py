"""Offline falsifier: no account, network, ledger or canonical writes."""
from pathlib import Path
import importlib.util, hashlib, json, shutil, types, sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'publication_live_gates.py'
# Capture the exact tested helper before the independently reported repair.
BOUND=HERE/'operational_initial_publication_live_gates.py'
if not BOUND.exists():shutil.copyfile(SOURCE,BOUND)
sys.path.insert(0,str(HERE.parents[3]))
spec=importlib.util.spec_from_file_location('initial_publication_gates',BOUND)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
fixture=HERE/'operational_attack_fixture';fixture.mkdir(exist_ok=True)
m.ROOT=fixture;m.AUDIT=fixture
metadata={'title':'Synthetic unrelated city-area theorem','description':'No transport result'}
record={'id':101,'metadata':metadata,'files':[{'key':'congestion-fragmentation.pdf','checksum':'md5:SYNTHETIC_TARGET_MATCH'}]}
prior={'all_broad_Aldous_leads_cleared_as_distinct':[{'record':101,'metadata_sha256':m.digest(metadata)}],'ledger_leads':[]}
(fixture/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').write_text(json.dumps(prior))
(fixture/'account_complete.json').write_text(json.dumps({'records':[record]}))
gate={'raw_receipts':'.','unexpected_account_matches':[{'id':101}], 'ledger_matches':[],
      'local_deposit_state_matches':[],'receipt':str(fixture/'gate.json'),'operation':'synthetic'}
(fixture/'gate.json').write_text(json.dumps(gate))
m.subprocess.run=lambda *a,**k:types.SimpleNamespace(stdout=json.dumps(gate))
accepted=False
try:
    m.collect('before_publish','0'*40)
    accepted=True
except Exception as error:
    rejection=repr(error)
result={'tested_helper_sha256':hashlib.sha256(BOUND.read_bytes()).hexdigest(),
        'synthetic_fixture':True,'network_or_live_mutation':False,
        'previously_cleared_metadata_unchanged':True,'target_file_identity_newly_present':True,
        'unexpected_known_record_accepted':accepted,
        'finding':'OPS-01: known-record metadata-only exemption does not bind file identities',
        'suggested_repair':'Bind/reconcile known record file identities as well as metadata against original cleared snapshot.'}
if not accepted:result['rejection']=rejection
(HERE/'OPERATIONAL_EXEMPTION_ATTACK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

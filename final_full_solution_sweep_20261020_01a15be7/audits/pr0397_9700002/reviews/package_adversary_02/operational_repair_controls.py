"""Offline regression of OPS-01 repair against bound synthetic identities."""
from pathlib import Path
import importlib.util,hashlib,json,copy,types,sys,shutil
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'publication_live_gates.py'
BOUND=HERE/'operational_repaired_publication_live_gates.py';shutil.copyfile(SOURCE,BOUND)
sys.path.insert(0,str(HERE.parents[3]))
spec=importlib.util.spec_from_file_location('repaired_gates',BOUND)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
fixture=HERE/'operational_repair_fixture';fixture.mkdir(exist_ok=True)
m.ROOT=m.AUDIT=fixture
baseline={'id':101,'metadata':{'title':'Synthetic distinct city theorem'},
          'files':[{'key':'unrelated.pdf','size':123,'checksum':'md5:unrelated'}]}
known={'record':101,'metadata_sha256':m.digest(baseline['metadata']),
       'metadata_and_files_sha256':m.digest(m.identity_projection(baseline))}
(fixture/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').write_text(json.dumps({'all_broad_Aldous_leads_cleared_as_distinct':[known],'ledger_leads':[]}))
gate={'raw_receipts':'.','unexpected_account_matches':[{'id':101}], 'ledger_matches':[],
      'local_deposit_state_matches':[],'receipt':str(fixture/'gate.json'),'operation':'synthetic'}
(fixture/'gate.json').write_text(json.dumps(gate))
m.subprocess.run=lambda *a,**k:types.SimpleNamespace(stdout=json.dumps(gate))
results=[]
def trial(label,record,should_accept):
    (fixture/'account_complete.json').write_text(json.dumps({'records':[record]}))
    try:m.collect('before_publish','0'*40);accepted=True;reason=None
    except Exception as e:accepted=False;reason=str(e)
    assert accepted==should_accept,(label,reason)
    results.append({'label':label,'accepted':accepted,'expected_accept':should_accept,'reason':reason})
trial('exact unchanged non-target record',baseline,True)
for label,mutate in [
    ('new target filename/checksum',lambda x:x['files'].append({'key':'congestion-fragmentation.pdf','checksum':'md5:SYNTHETIC_TARGET'})),
    ('changed checksum',lambda x:x['files'][0].update(checksum='md5:SYNTHETIC_TARGET')),
    ('changed size',lambda x:x['files'][0].update(size=124)),
    ('changed filename',lambda x:x['files'][0].update(key='congestion-fragmentation.pdf')),
    ('changed metadata',lambda x:x['metadata'].update(title='congestion theorem')),
    ('changed files schema',lambda x:x.update(files={})),
    ('changed metadata schema',lambda x:x.update(metadata=[])),
    ('removed file',lambda x:x.update(files=[])),
]:
    record=copy.deepcopy(baseline);mutate(record);trial(label,record,False)
result={'all_assertions_passed':True,'helper_sha256':hashlib.sha256(BOUND.read_bytes()).hexdigest(),
        'controls':results,'network_or_live_mutation':False,'OPS-01':'closed by exact metadata-and-files binding'}
(HERE/'OPERATIONAL_REPAIR_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

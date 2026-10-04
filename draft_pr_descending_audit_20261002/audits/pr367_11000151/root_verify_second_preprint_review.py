"""Read every sealed review byte, full retained child output, and rank record."""
from pathlib import Path
from datetime import datetime,timezone
import base64,gzip,hashlib,json,subprocess
A=Path(__file__).resolve().parent;D=A/'preprint_review_02';P=A/'preprint';V=P/'verification'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
m=load(D/'IMMUTABLE_MANIFEST.json');s=load(D/'FINAL_SEAL.json')
assert sha((D/'IMMUTABLE_MANIFEST.json').read_bytes())=='2db771880e2fbe3ed9373815d91a77dc0722a03e562529e23addf9ecf044f8cf'==s['manifest_sha256']
assert len(m['files'])==34
for r in m['files']:
    b=(D/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
status=load(D/'REVIEW_STATUS.json');assert status['verdict']=='PASS_EXACT_REPAIRED_BYTES_CLEARED_FOR_PUBLICATION' and status['mandatory_remaining_changes']==[]
sealed=load(P/'REPAIRED_REVIEW_PACKAGE_02.json')['sealed_files']
assert sealed==m['candidate_bindings']==status['candidate_bindings']
for r in sealed:
    b=(P/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
for rank in range(1,7):
    original=V/'certificates'/('30_action_records.txt.gz' if rank==6 else f'rank{rank}_action_records.txt.gz')
    assert gzip.decompress(original.read_bytes())==gzip.decompress((D/f'terminal_rank{rank}_records.txt.gz').read_bytes())
replay=load(D/'PACKAGE_REPLAY.json');assert replay['status']=='PASS'
begin=datetime.fromisoformat(replay['utc_started']);end=datetime.fromisoformat(replay['utc_finished'])
rows=[json.loads(line) for line in gzip.decompress((D/'package_child_outputs.jsonl.gz').read_bytes()).splitlines()]
inventory=load(D/'PACKAGE_CHILD_OUTPUT_INVENTORY.json');assert len(rows)==len(inventory)==11
labels=[]
for row,entry in zip(rows,inventory):
    assert row['returncode']==0 and begin<=datetime.fromisoformat(row['utc_started'])<=datetime.fromisoformat(row['utc_finished'])<=end
    stdout=base64.b64decode(row['stdout_b64'],validate=True);stderr=base64.b64decode(row['stderr_b64'],validate=True)
    assert stderr==b'' and len(stdout)==entry['stdout_bytes'] and sha(stdout)==entry['stdout_sha256']
    assert {k:v for k,v in row.items() if k not in {'stdout_b64','stderr_b64'}}=={k:v for k,v in entry.items() if k not in {'stdout_bytes','stdout_sha256','stderr_bytes'}}
    args=row['args'];name=Path(args[-1]).name
    if args[0]=='g++':assert stdout==b'';label='compile'
    elif args[-1]=='--stream':
        records=gzip.decompress((V/'certificates/30_action_records.txt.gz').read_bytes());parts=stdout.splitlines(keepends=True)
        assert b''.join(line for line in parts if line.startswith(b'S|'))==records
        assert json.loads(parts[-1])=={'status':'PASS','reachable_states':234368,'outgoing_edges':711342,'coaccessible_states':90921,'coaccessible_edges':261810};label='all_cpp_records'
    elif name.startswith('check_turn_'):
        n=name[len('check_turn_'):-3];assert stdout==(V/f'reference/TURN_{n}_CHECKS.json').read_bytes();label=name
    elif name=='verify_turn_4_cpp.py':assert stdout==(V/'reference/TURN_4_CPP_CHECKS.json').read_bytes();label=name
    elif name=='independent_check.py':assert stdout==(V/'reference/review/INDEPENDENT_CHECKS.json').read_bytes();label=name
    elif name=='verify_publication.py':assert stdout==b'PASS: all frozen public bytes, four Python receipts, C++ full stream, and independent review controls\n';label=name
    else:
        if name=='independent_20_30.py':actual=json.loads(stdout);expected=load(V/'independent_expected.json')
        else:
            assert name=='independent_ranks1_6.py';decoder=json.JSONDecoder();text=stdout.decode();values=[]
            while text.strip():
                value,index=decoder.raw_decode(text.lstrip());values.append(value);text=text.lstrip()[index:]
            expected=load(V/'independent_ranks_expected.json');assert len(values)==7 and values[:6]==expected['ranks'];actual=values[-1]
        assert datetime.fromisoformat(row['utc_started'])<=datetime.fromisoformat(actual['utc'])<=datetime.fromisoformat(row['utc_finished'])
        assert actual.keys()==expected.keys() and {k:v for k,v in actual.items() if k!='utc'}=={k:v for k,v in expected.items() if k!='utc'};label=name
    labels.append(label)
r=subprocess.run(['python3','-B',str(D/'verify_seal.py')],capture_output=True);assert r.returncode==0 and r.stderr==b''
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_ENTIRE_SECOND_REVIEW_AND_FULL_CHILD_OUTPUTS','sealed_review_files':34,'complete_child_outputs':11,'every_terminal_rank1_6_record_byte_equal':True,'all_direct_cpp90921_records_and_terminal_literal_equal':True,'complete_output_labels':labels,'submission_bindings':sealed,'seal_stdout':r.stdout.decode(),'mandatory_remaining_findings':0}
(A/'root_second_review_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'submission_bindings','complete_output_labels','seal_stdout'}},indent=2))

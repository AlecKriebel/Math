"""Preserve v1 and prepare distinct future v2 bytes with stage-only transforms."""
from pathlib import Path
import datetime as dt
import hashlib
import json
from prepare_operational_bytes import TRANSFORMS

A = Path(__file__).resolve().parent
R = A.parents[3]
SOURCE = A.parent / 'attributed_prior_result_preparation_v2_20261004'

def sha(b): return hashlib.sha256(b).hexdigest()

def main():
    packet = json.loads((SOURCE / 'MANIFEST.json').read_bytes())
    if len(packet['files']) != 4 or {x['name'] for x in packet['files']} != set(TRANSFORMS) | {'DISPOSITION_PROPOSAL.json'}:
        raise RuntimeError('V2 packet scope differs')
    for row in packet['files']:
        if set(row) != {'name','bytes','sha256'}: raise RuntimeError('V2 packet pin schema differs')
        b = (SOURCE / row['name']).read_bytes()
        if len(b) != row['bytes'] or sha(b) != row['sha256']: raise RuntimeError('V2 prospective body drift')
    dest = A / 'planned_final_documents_v2'
    dest.mkdir(exist_ok=False)
    rows = []
    for name, edits in TRANSFORMS.items():
        source = (SOURCE / name).read_bytes(); text = source.decode()
        for old,new in edits:
            if text.count(old) != 1: raise RuntimeError('V2 operational literal not unique: ' + name)
            text = text.replace(old,new)
        final = text.encode(); (dest / name).write_bytes(final)
        rows.append({'source_path':str((SOURCE/name).relative_to(R)), 'source_bytes':len(source), 'source_sha256':sha(source), 'planned_path':str((dest/name).relative_to(R)), 'planned_bytes':len(final), 'planned_sha256':sha(final), 'literal_edits':[{'old':old,'new':new,'required_occurrences':1} for old,new in edits]})
    plan = {'UTC':dt.datetime.now(dt.timezone.utc).isoformat(), 'stage':'PLANNED_FUTURE_BYTES_NOT_NATIVE_ACCEPTANCE_OR_MERGE_RECEIPT', 'PR':66, 'version':2, 'previous_plan_retained':'OPERATIONAL_BYTE_PLAN.json', 'title':'10400033: verified tournament bound; prior resolution credited', 'scientific_changes':False, 'prospective_inputs_unchanged':True, 'files':rows}
    with (A / 'OPERATIONAL_BYTE_PLAN_V2.json').open('x') as f: f.write(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in plan.items() if k!='files'},indent=2))
    print(json.dumps([{k:v for k,v in x.items() if k!='literal_edits'} for x in rows],indent=2))

if __name__ == '__main__': main()

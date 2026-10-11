"""Prepare future document bytes only; never writes native files or Git state."""
from pathlib import Path
import datetime as dt
import hashlib
import json

A = Path(__file__).resolve().parent
SOURCE = A.parent / 'attributed_prior_result_preparation_20261004'
TRANSFORMS = {
    'CURRENT_RESULT.md': [
        ('Prospective current assessment, prepared for independent adversarial review.\nThis file is not a merge receipt or publication clearance.',
         "Current accepted assessment after ROOT's final scientific adjudication and\nindependent adversarial review. The actual merge and acceptance are recorded\nin `acceptance.json`; this disposition provides no publication clearance."),
        ('Accordingly the proposed current problem status is `already_solved`, accepted',
         'Accordingly the current accepted problem status is `already_solved`, accepted'),
        ('proof/checker bodies, source wrapper, and historical review outcomes are to be\npreserved. Current corrections belong in separate acceptance records.',
         'proof/checker bodies, source wrapper, and historical review outcomes are\npreserved. Current corrections are recorded in separate acceptance records.'),
    ],
    'CURRENT_PRIORITY_SPECIALIZATION.md': [
        ('Prospective attribution correction for PR66; no final integration is recorded.',
         'Current attribution correction accepted for PR66; `acceptance.json` records\nactual integration.'),
        ('The frozen\nproof is to remain untouched; this precision belongs in the current assessment.',
         'The frozen\nproof remains untouched; this precision belongs in the current assessment.'),
    ],
    'PR_BODY.md': [
        ('The current audited outcome is proposed as **already_solved**:',
         'The current accepted outcome is **already_solved**:'),
        ('The proposed acceptance is attributed partial program progress,',
         'The acceptance is attributed partial program progress,'),
        ('Separate current acceptance files are to govern the corrected outcome.',
         'Separate current acceptance files govern the corrected outcome.'),
        ('This prepared body records a proposal, not an\nactual merge or completed acceptance.',
         'The exact original head has been merged; the separate current acceptance\nrecord binds the corrected outcome to that merge.'),
    ],
}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def main():
    manifest = json.loads((SOURCE / 'MANIFEST.json').read_bytes())
    if {p['path'] for p in manifest['files']} != set(TRANSFORMS) | {'DISPOSITION_PROPOSAL.json'}:
        raise RuntimeError('Unexpected prospective packet scope')
    for p in manifest['files']:
        b = (SOURCE / p['path']).read_bytes()
        if len(b) != p['bytes'] or sha(b) != p['sha256']:
            raise RuntimeError('Prospective input drift')
    dest = A / 'planned_final_documents'
    dest.mkdir(exist_ok=False)
    rows = []
    for name, edits in TRANSFORMS.items():
        source = (SOURCE / name).read_bytes()
        current = source.decode('utf-8')
        for old, new in edits:
            if current.count(old) != 1:
                raise RuntimeError('Operational literal is not unique: ' + name)
            current = current.replace(old, new)
        final = current.encode('utf-8')
        (dest / name).write_bytes(final)
        rows.append({'source_path':str((SOURCE/name).relative_to(A.parents[3])),
                     'source_bytes':len(source),'source_sha256':sha(source),
                     'planned_path':str((dest/name).relative_to(A.parents[3])),
                     'planned_bytes':len(final),'planned_sha256':sha(final),
                     'literal_edits':[{'old':old,'new':new,'required_occurrences':1} for old,new in edits]})
    plan = {'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
            'stage':'PLANNED_FUTURE_BYTES_NOT_NATIVE_ACCEPTANCE_OR_MERGE_RECEIPT',
            'PR':66,'title':'10400033: verified tournament bound; prior resolution credited',
            'scientific_changes':False,'prospective_inputs_unchanged':True,'files':rows}
    (A/'OPERATIONAL_BYTE_PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'stage':plan['stage'],'files':[{k:v for k,v in p.items() if k!='literal_edits'} for p in rows]},indent=2))

if __name__ == '__main__':
    main()

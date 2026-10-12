"""Extend the exact audit checkpoint selection with actual concurrency evidence."""
from pathlib import Path
import datetime, hashlib, json, os
A = Path(__file__).resolve().parent
C = A.parents[2]
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
previous = json.loads((A/'ROUND2_ADJUDICATION_CHECKPOINT_SELECTION.json').read_text())
receipt = json.loads((A/'remote_main_reconciliation_round2_20261006/RECEIPT.json').read_text())
if not receipt['selected_bytes_unchanged'] or receipt['new'] != '1f86990dcae793167b35c1cfff2e310758404886':
    raise RuntimeError('Reconciliation receipt mismatch')
selected = {C/rel for rel in previous['paths']}
for folder in ['actual_operations/checkpoint_round2_adjudication',
               'actual_checkpoints/round2_adjudication',
               'actual_operations/fetch_remote_for_round2_adjudication',
               'actual_operations/reconcile_round2_checkpoint_remote',
               'remote_main_reconciliation_round2_20261006',
               'actual_operations/prepare_round2_adjudication']:
    selected.update(p for p in (A/folder).rglob('*') if p.is_file() and not p.is_symlink())
selected.update([A/'ROUND2_ADJUDICATION_CHECKPOINT_SELECTION.json',
                 A/'reconcile_round2_checkpoint_remote.py', Path(__file__).resolve()])
with (A/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n### '+now+' — checkpoint concurrent advance reconciled\n'
                 'The first Round2 adjudication checkpoint (actual child62302exit1) stopped before staging because remote main advanced. Actual private reconciliation63197exit0 verified ad789fad as ancestor of1f86990d, all275 concurrent changes belong exclusively to the other descending-audit folder, all360 selected working bodies remain byte-identical, and the private index is empty. Only this isolated checkout\'s main/index advanced; primary checkout and the other workflow files were not written. Retry retains both successful audit and actual stopped operation evidence. PR97 qualified package accepted; priority/publication disposition still unresolved, no service or native mutation. Completion estimates: PR97workflow60%; program13/99=13.13%; original author2/5 and extra proof-search0.\n')
rows=[]
for p in sorted(selected):
    if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(C.resolve()):
        raise RuntimeError('Unsafe selected body')
    b=p.read_bytes()
    rows.append({'path':p.relative_to(C).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
out={'schema':'pr97-round2-adjudication-concurrent-retry-selection/v1','UTC':now,
     'operator_PID':os.getpid(),'expected_main':receipt['new'],
     'paths':[r['path'] for r in rows],'pins':rows,
     'publication_authorized':False,'third_party_extracted_bodies_and_fixture_links_private':True}
with (A/'ROUND2_ADJUDICATION_CHECKPOINT_RETRY_SELECTION.json').open('x') as stream:
    stream.write(json.dumps(out,indent=2)+'\n')
print(json.dumps({'UTC':now,'operator_PID':os.getpid(),'selected_files':len(rows),
                  'selected_bytes':sum(r['bytes'] for r in rows),'expected_main':receipt['new']}))

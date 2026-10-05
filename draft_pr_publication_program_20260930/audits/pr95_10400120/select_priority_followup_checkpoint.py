from pathlib import Path
import datetime, hashlib, json, re, os
A = Path(__file__).resolve().parent
C = A.parents[2]
P = A.parents[1]
D = A / 'priority_later_version_followup_20261005'
T = A / 'priority_thesis_repository_followup_20261005'
files = [P/'CURRENT_PROGRESS.json']
files += [A/n for n in ['PRIORITY_STATUS.md','RESEARCH_LOG.md','ROOT_PRIORITY_DISPOSITION_20261005.json','ROOT_PRIORITY_FOLLOWUP_ADJUDICATION_20261005.json','ROOT_PRIORITY_LATER_SOURCE_SCOPES_20261005.json','ROOT_PRIORITY_LATER_RETRIEVAL_METADATA_20261005.json','ROOT_AUTHENTICATED_PRIORITY_LATER_FOLLOWUP_20261005.json','verify_later_followup.py','finalize_priority_followup.py','select_priority_followup_checkpoint.py']]
files += [f for f in T.iterdir() if f.is_file()]
files += [D/n for n in ['REPORT.md','RESEARCH_LOG.md','INDEPENDENT_OBLIGATIONS.md','ACCEPTED_PARENT_MATHEMATICAL_GATE.json','INPUT_MANIFEST.json','VERSION_COMPARISON_INPUTS.json','SELECTED_VERSION_COMPARISON.json','SELECTED_SIGN_COMPARISON_SUCCESS.json','SEARCH_SCOPE.json','PROCESS_LIMITATIONS.md','retrieve_extract.py','close_packet.py','INTEGRITY_CHECK.json','CLOSED_MANIFEST.json','CLOSURE.json']]
files += [f for f in (D/'adversarial_review').iterdir() if f.is_file() and f.suffix in ['.md','.json']]
files += [f for f in (D/'processes').glob('*.json') if not f.name.startswith('retrieval_')]
for op in ['checkpoint_priority','root_thesis_osaka_retrieval','root_thesis_close','root_later_followup_integrity','root_priority_followup_finalize']:
    files += [f for f in (A/'actual_operations'/op).iterdir() if f.is_file()]
files += [A/'actual_checkpoints/closed_priority/RECEIPT.json',A/'actual_checkpoints/closed_priority/PROCESS_JOURNAL.json']
files = sorted(set(files))
for f in files:
    if not f.is_file() or f.is_symlink() or not f.is_relative_to(C):
        raise RuntimeError('invalid selected path: '+str(f))
    b = f.read_bytes()
    if re.search(br'(?i)(set-cookie\s*:|authorization\s*:\s*(bearer|basic)|access_token\s*[=:]|refresh_token\s*[=:])',b):
        raise RuntimeError('unreviewed sensitive retrieval metadata: '+str(f))
    if b.startswith(b'%PDF-') or f.suffix in ['.pdf','.png','.jpg'] or 'private_sources' in f.parts:
        raise RuntimeError('private source artifact selected')
paths = [str(f.relative_to(C)) for f in files]
pins = [{'file':str(f.relative_to(C)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]
plan = {'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'paths':paths,'pins':pins,'selection_scope':'Authored findings, code, closed metadata and actual nonsecret operation receipts only; raw primary source files, full extractions, renders, browser responses and HTTP retrieval headers excluded. Prior checkpoint byte streams remain local; receipt and process-journal hashes are released.','private_closed_manifest_members_remain_local_evidence':True,'primary_checkout_mutation':False,'branch':'main','priority_clearance':False,'publication_clearance':False}
dest=A/'PRIORITY_FOLLOWUP_CHECKPOINT_SELECTION_20261005.json'
dest.write_text(json.dumps(plan,indent=2)+'\n')
plan['paths'].append(str(dest.relative_to(C)))
dest.write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps({'selected_files':len(plan['paths']),'pinned_payloads':len(pins),'total_bytes_without_selection':sum(r['bytes'] for r in pins),'actual_operator_PID':os.getpid()}))

from pathlib import Path
import hashlib,json,datetime
f=Path('draft_pr_publication_program_20260930/audits/pr32_6800007/integral_action_family')
j=json.loads((f/'original_inputs_receipt.json').read_text());p=f.parent/'source_snapshot'
for v in j['files']:assert hashlib.sha256((p/v['path']).read_bytes()).hexdigest()==v['sha256']
assert hashlib.sha256((f/'EARLY_INTEGRAL_SEAL.md').read_bytes()).hexdigest()=='d62c9962acbd293d0318518739f8d58aad91917d4cccae6bd90309033f30cf16'
pr30=Path('draft_pr_publication_program_20260930/audits/pr30_30003955/geometric_family')
assert hashlib.sha256((pr30/'artifact_manifest.json').read_bytes()).hexdigest()=='21e46f56cf0a188560c124a92a4f4e80111a85b231d458b0d8a0bd6cfebede60'
old=json.loads((pr30/'artifact_manifest.json').read_text())
for v in old['members']:assert hashlib.sha256((pr30/v['path']).read_bytes()).hexdigest()==v['sha256']
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all15_PR32_original_hashes_unchanged':True,'PR32_early_seal_unchanged':True,'closed_PR30_manifest_sha256':'21e46f56cf0a188560c124a92a4f4e80111a85b231d458b0d8a0bd6cfebede60','all26_PR30_first_party_members_unchanged':True,'PR30_ignored_tmp_not_modified_by_this_family':True,'ledger_original_rows':len((p/'turns.jsonl').read_text().splitlines()),'limit':5,'audit_new_substantive_rows':0}
(f/'protected_inputs_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt)

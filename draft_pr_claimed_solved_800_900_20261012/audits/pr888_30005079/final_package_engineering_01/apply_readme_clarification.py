from pathlib import Path
import datetime,hashlib,json
H=Path(__file__).absolute().parent;C=H.parent/'candidate';T=H/'private_tmp'
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
oldindex=(C/'verification/package_index.json').read_bytes();oldreadme=(C/'README.md').read_bytes();newreadme=(H/'PACKAGE_README.md').read_bytes()
archive=T/'build/rank-two-fano-verification.zip';prior=T/'build_before_readme_clarification';prior.mkdir()
archive.rename(prior/archive.name)
for name in ('DEFAULT_BUILD_PUBLIC_STDOUT.json','DEFAULT_BUILD_PUBLIC_STDERR.txt','DEFAULT_BUILD_EXECUTION_RECEIPT.json'):
    (H/name).rename(T/('before_readme_'+name))
for name in ('default_build_raw.stdout','default_build_raw.stderr'):(T/name).rename(T/('before_readme_'+name))
(C/'README.md').write_bytes(newreadme);(C/'verification/README.md').write_bytes(newreadme)
index=json.loads(oldindex)
for row in index['files']:
    if row['path']=='README.md':row.update(pin(newreadme))
raw=(json.dumps(index,indent=2,sort_keys=True)+'\n').encode();(C/'verification/package_index.json').write_bytes(raw)
receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_estimate_percent':55,'scope':'Parent-requested README outer/extracted-ZIP clarification only; no frozen inputs or tool changed.','previous_package_index':pin(oldindex),'current_package_index':pin(raw),'previous_README':pin(oldreadme),'current_README':pin(newreadme),'preclarification_actual_default_build':'PASS; raw/public receipt and archive retained privately, excluded from final-core successful replay totals.','preclarification_build_stdout':pin((T/'before_readme_default_build_raw.stdout').read_bytes()),'preclarification_archive':pin((prior/archive.name).read_bytes()),'changed_candidate_files':['README.md','verification/README.md','verification/package_index.json'],'actual_final_default_build_required_again':True}
(H/'README_CLARIFICATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'UPDATED_REQUIRES_FRESH_DEFAULT_BUILD','current_package_index':pin(raw)},indent=2))

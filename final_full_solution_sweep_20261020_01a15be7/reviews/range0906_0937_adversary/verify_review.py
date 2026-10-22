from pathlib import Path,PurePosixPath
import json,hashlib
W=Path(__file__).resolve().parent

def require(t,message):
 if not t:raise ValueError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def files(root,exclude):return sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and not any(part=='__pycache__' for part in p.relative_to(root).parts) and p.relative_to(root).as_posix() not in exclude)
def verify(root,m):
 names=[]
 for x in m['files']:
  p=PurePosixPath(x['path']);require(not p.is_absolute() and '..' not in p.parts and str(p)==x['path'],'unsafe pin');f=root/x['path'];require(f.is_file() and not f.is_symlink(),'nonregular pin');b=f.read_bytes();require(len(b)==x['bytes'] and digest(b)==x['sha256'],'hash '+x['path']);names.append(x['path'])
 require(len(names)==len(set(names)),'duplicate inventory');return sorted(names)
public=json.loads((W/'PUBLIC_MANIFEST.json').read_text());seal=json.loads((W/'FINAL_SEAL.json').read_text());require(digest((W/'PUBLIC_MANIFEST.json').read_bytes())==seal['public_manifest_sha256'],'public seal');names=verify(W,public);actual=[x for x in files(W,{'PUBLIC_MANIFEST.json','FINAL_SEAL.json'}) if not x.startswith('private/')];require(names==actual,'public exact closure')
private=json.loads((W/'private/PRIVATE_MANIFEST.json').read_text());pseal=json.loads((W/'PRIVATE_MANIFEST_SEAL.json').read_text());require(digest((W/'private/PRIVATE_MANIFEST.json').read_bytes())==pseal['sha256'],'private seal');pnames=verify(W/'private',private);require(pnames==files(W/'private',{'PRIVATE_MANIFEST.json'}),'private exact closure')
scope=json.loads((W/'SCOPE_CHECKS.json').read_text())['cases'];require(len(scope)==32 and [x['pr'] for x in scope]==list(range(906,938)),'scope counts');require(all(x['path_cache_equal'] and x['added_rows_cache_equal'] and x['all_blob_ids_match'] and x['own_row_count']==1 and x['own_path_count']==x['path_count']-1 and x['own_row_status_matches_disposition'] for x in scope),'scope failure');require(sum(x['path_count'] for x in scope)==1158,'path count')
packages=json.loads((W/'PACKAGE_CHECKS.json').read_text());require(len(packages)==4 and all(not x['errors'] and x['safe_unique_regular_crc_closed'] and x['all_original_blobs_exact'] and x['original_tree_archive_closed'] and x['external_embedded_pdf_equal'] for x in packages),'package failure');require(sum(x['original_tree_count'] for x in packages)==111,'original count')
ledger=json.loads((W/'LEDGER_CHECKS.json').read_text());require(ledger['returned_rows']==178 and ledger['data_rows']==177 and not ledger['pr932_exact_match'],'ledger count');require(all(all(v for k,v in row.items() if isinstance(v,bool)) for row in ledger['cases']),'ledger mismatch')
coherence=json.loads((W/'INPUT_COHERENCE.json').read_text());require(all(all(v for k,v in row.items() if k!='pr') for row in coherence['cases']),'input mismatch')
r=json.loads((W/'PR0932_CHECKS.json').read_text());require(not r['errors'] and r['immutable_originals_exact']==29 and r['proof_recheck01']['normal_copied_complete_certificate_equal'] and r['priority_recheck01']['normal_and_optimized_copied_replay_equal'] and not r['local_deposit_state']['matches'],'932 mismatch')
after=json.loads((W/'CONTEXT_AFTER.json').read_text());require(after['scoped_32_journal_records_unchanged'] and after['scoped_inventory_rows_unchanged'],'context scope changed')
print(json.dumps({'status':'BOUNDED_PASS','public_artifacts':len(names),'private_artifacts':len(pnames),'public_manifest_sha256':seal['public_manifest_sha256'],'private_manifest_sha256':pseal['sha256'],'cases':32,'scope':'Review artifact integrity and saved result consistency only, no global/mathematical/novelty/human certification'},indent=2))

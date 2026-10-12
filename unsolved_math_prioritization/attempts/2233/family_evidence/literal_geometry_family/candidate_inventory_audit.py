"""Read and check all immutable snapshot bytes and all submitted receipt entries."""
import difflib, hashlib, json, pathlib, stat
ROOT=pathlib.Path(__file__).resolve().parent
SNAP=ROOT.parent/'source_snapshot_v2'
manifest=json.loads((ROOT.parent/'snapshot_manifest_v2.json').read_text())
rows=[]
for entry in manifest['files']:
 p=SNAP/entry['path']; b=p.read_bytes(); digest=hashlib.sha256(b).hexdigest()
 assert digest==entry['sha256'] and len(b)==entry['size']
 assert stat.S_IMODE(p.stat().st_mode)==0o444
 # Decode every full text file; parse each full JSON/JSONL without executing helpers.
 text=b.decode()
 if p.suffix=='.json': parsed=json.loads(text)
 elif p.suffix=='.jsonl': parsed=[json.loads(line) for line in text.splitlines()]
 else: parsed=None
 rows.append({'path':entry['path'],'bytes':len(b),'sha256':digest,'read_complete':True,
              'json_type':type(parsed).__name__ if parsed is not None else None})
assert (SNAP/'check_spectra.py').read_bytes()==(SNAP/'review/submitted_check_spectra.py').read_bytes()
assert (SNAP/'check_results.json').read_bytes()==(SNAP/'review/submitted_results.json').read_bytes()
receipt=json.loads((SNAP/'review/independent_results.json').read_text())
assert len(receipt['checks'])==receipt['passed']==1263 and receipt['failed']==0
assert set(receipt['checks'].values())=={'PASS'}
old=(SNAP/'review/PARTIAL.md').read_text(); final=(SNAP/'PARTIAL.md').read_text()
diff=''.join(difflib.unified_diff(old.splitlines(True),final.splitlines(True),fromfile='review/PARTIAL.md',tofile='PARTIAL.md'))
(ROOT/'candidate_header_only_diff.patch').write_text(diff)
body_old=old.split('\n',3)[3];body_new=final.split('\n',3)[3]
assert body_old==body_new
pinned=json.loads((ROOT.parent/'pinned_problem.json').read_text())
source=json.loads((SNAP/'source_record.json').read_text())
assert source==pinned
result={'original_head':manifest['head'],'actual_base':manifest['base'],
 'snapshot_manifest_sha256':hashlib.sha256((ROOT.parent/'snapshot_manifest_v2.json').read_bytes()).hexdigest(),
 'files':rows,'all_original_modes_0444':True,'helper_scripts_executed':False,
 'author_receipts_byte_identical':True,'all_1263_independent_result_keys_parsed':True,
 'old_to_final_difference':diff,'pinned_source_deep_equal':True,
 'pinned_prior_report':json.loads((ROOT.parent/'pinned_prior_report.json').read_text()),
 'prior_qualification':'{} is ROOT-provided SQL fallback because raw prior key is absent; not a fetched prior result',
 'historical_model_runtime_claims':'Read as unverified historical assertions, not attested by this audit'}
(ROOT/'candidate_inventory.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2))
print('Read and checked all 17 immutable snapshot files:',len(rows))

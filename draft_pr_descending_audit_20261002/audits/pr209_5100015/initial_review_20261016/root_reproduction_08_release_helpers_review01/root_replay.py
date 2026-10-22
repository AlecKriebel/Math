from pathlib import Path
import datetime,hashlib,json,runpy,shutil,zipfile
HERE=Path(__file__).resolve().parent
original_rmtree=shutil.rmtree
checks=[]
def checked_rmtree(path,*a,**k):
 target=Path(path).resolve()
 assert target==HERE/'probe_runs_v2'
 expected={p.relative_to(HERE).as_posix():p.read_bytes() for p in target.rglob('*') if p.is_file()}
 with zipfile.ZipFile(HERE/'PROBE_FIXTURES_FINAL.zip') as z:
  assert z.testzip() is None
  assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(expected)
  for n,b in expected.items():assert z.read(n)==b
 checks.append(dict(files=len(expected),all_bytes_roundtrip_verified_before_removing_owned_fixture_tree=True))
 original_rmtree(target,*a,**k)
shutil.rmtree=checked_rmtree
runpy.run_path(str(HERE/'REPRODUCE.py'),run_name='__main__')
original=HERE.parent.parent/'release_helpers_adversary_01'
comparisons=[]
for n in ['PROBE_RESULTS.json','ADDITIONAL_PROBE_RESULTS.json','FINAL_PROBE_RESULTS.json']:
 actual=json.loads((HERE/n).read_text());prior=json.loads((original/n).read_text())
 assert len(actual)==len(prior)
 assert actual==prior,(n,actual,prior)
 comparisons.append(dict(path=n,all_observations_exact=True,checks=len(actual)))
receipt=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),synthetic_only=True,live_provider_calls=0,source_modules_changed=False,comparisons=comparisons,fixture_roundtrip=checks,source_manifest=json.loads((HERE/'ROOT_INPUT_BINDINGS.json').read_text()))
(HERE/'ROOT_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(dict(root_replay='PASS',expected_outcomes=29,fixture_roundtrip=checks)))

"""Run the sealed-source audit in a fresh copy of this owned audit folder.

Uses only the existing standard Python runtime. Providers remain stubbed by the
harnesses. Generated synthetic fixtures are compressed after preserving all of
their bytes; the uncompressed owned fixture trees are then removed.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,zipfile

HERE=Path(__file__).resolve().parent
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
for row in json.loads((HERE/'FROZEN_SOURCES.json').read_text())['rows']:
 raw=(HERE/row['path']).read_bytes()
 assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
assert not (HERE/'probe_runs_v2').exists(),'Use a fresh audit-folder copy; preserve prior generated fixtures first'
execution=[]
for name in ['probes.py','additional_probes.py','final_probes.py']:
 result=subprocess.run([PY,'-B',str(HERE/name)],cwd=HERE,capture_output=True,text=True,timeout=90)
 (HERE/(name+'.stdout.jsonl')).write_text(result.stdout)
 (HERE/(name+'.stderr.txt')).write_text(result.stderr)
 execution.append(dict(script=name,returncode=result.returncode))
 assert result.returncode==0,result.stderr
rows=[]
for name in ['PROBE_RESULTS.json','ADDITIONAL_PROBE_RESULTS.json','FINAL_PROBE_RESULTS.json']:rows.extend(json.loads((HERE/name).read_text()))
assert len(rows)==29 and all(row['status']=='PASS' for row in rows),rows
with zipfile.ZipFile(HERE/'PROBE_FIXTURES_FINAL.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for path in sorted((HERE/'probe_runs_v2').rglob('*')):
  if path.is_file():archive.write(path,path.relative_to(HERE).as_posix())
shutil.rmtree(HERE/'probe_runs_v2')
(HERE/'REPRODUCTION_RESULT.json').write_text(json.dumps(dict(execution=execution,check_count=len(rows),all_expected_outcomes_reproduced=True,providers='in-memory stubs only',fixture_archive='PROBE_FIXTURES_FINAL.zip'),indent=2)+'\n')
print(json.dumps(dict(check_count=len(rows),all_expected_outcomes_reproduced=True)))

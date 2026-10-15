import datetime, hashlib, json, pathlib, sys
root=pathlib.Path(__file__).resolve().parent
assert sys.flags.optimize==0
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
captures=[]
for p in sorted((root/'process_evidence').glob('*/execution.json')):
 r=json.loads(p.read_text())
 assert isinstance(r['actual_child_pid'],int) and r['actual_child_pid']>0
 assert r['exit_code']==0
 assert r['cwd']==str(root)
 assert not any(a in ('-O','-OO') for a in r['argv'])
 for name in ('stdout.bin','stderr.bin'):
  q=p.parent/name
  assert q.stat().st_size==r[name]['bytes'] and sha(q)==r[name]['sha256']
 captures.append(str(p.parent.relative_to(root)))
ip=json.loads((root/'INPUT_PINS.json').read_text())
origins=[]
for r in ip['inputs']:
 assert sha(root/r['copy'])==r['sha256']
 origin=pathlib.Path(r['source'])
 origins.append(dict(source=str(origin),frozen_sha256=r['sha256'],
                     current_sha256=sha(origin),unchanged_since_freeze=sha(origin)==r['sha256']))
assert sha(root/'CRITERIA.md')==ip['criteria_sha256']
cp=json.loads((root/'CURRENT_NOTE_COMPARISON.json').read_text())
assert sha(root/cp['original_copy'])==cp['original_sha256']
assert sha(root/cp['current_copy'])==cp['current_sha256']
assert sha(pathlib.Path(cp['current_origin']))==cp['current_sha256']
sr=json.loads((root/'SEMANTIC_NOTE_REVIEW.json').read_text())
assert sr['initial_sha256']==cp['original_sha256']
assert sr['later_sha256']==cp['current_sha256']
assert sr['mathematical_verdict_applies_to_both_pinned_versions']
sp=json.loads((root/'SOURCE_PINS.json').read_text())
for r in sp['sources']:
 assert sha(root/r['path'])==r['sha256']
 assert 'http_code=200' in (root/r['download_capture']/'stdout.bin').read_text()
assert json.loads((root/'CONTROL_RESULTS.json').read_text())['checks_passed']
assert not any(p.is_symlink() for p in root.rglob('*'))
result=dict(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            python_optimization_level=sys.flags.optimize,captured_procedures_verified=captures,
            original_input_comparison=origins,checks_passed=True,
            later_note_pin=cp['current_sha256'],semantic_comparison_verified=True,
            scope='Frozen note only. Mathematical proof checked independently; controls are supporting stress examples.')
(root/'FINAL_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

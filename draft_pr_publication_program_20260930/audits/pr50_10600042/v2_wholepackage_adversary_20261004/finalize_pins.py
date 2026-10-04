import datetime, hashlib, json, pathlib, shutil, sys
root=pathlib.Path(__file__).resolve().parent
repo=root.parents[3]
package=root.parent/'publication_package_v2'
initial=json.loads((root/'INPUT_PINS.json').read_text())
changes=[]
for row in initial['inputs']:
    path=repo/row['path']
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=row['sha256']: changes.append({'path':row['path'],'new_sha256':digest})
extra=[repo/'unsolved_math_prioritization/QUEUE.md', root.parent/'original/turns.jsonl',root.parent/'original/status.json',
       root/'private/primary/lambropoulou_rourke.pdf']
extra+=sorted(root.glob('*.py'))
extra+=sorted((root/'private/commands').glob('*.stdout'))
extra+=sorted((root/'private/commands').glob('*.stderr'))
extra+=sorted((root/'private/commands').glob('*.json'))
extra+=sorted((root/'private/primary').glob('*.txt'))
extra+=sorted((root/'private/primary').glob('*.png'))
extra+=sorted((root/'private').glob('web_*.json'))
rows=[]
for p in extra:
    body=p.read_bytes()
    rows.append({'path':str(p.relative_to(repo)),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
tools=[]
for name in ('python3','git','gh','tectonic','pdftoppm','pdftotext','curl'):
    p=pathlib.Path(shutil.which(name)).resolve(); body=p.read_bytes()
    tools.append({'name':name,'resolved_path':str(p),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
binary=pathlib.Path('/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3').resolve()
body=binary.read_bytes(); tools.append({'name':'bundled_python3','resolved_path':str(binary),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
payload_changes=[r for r in changes if not r['path'].endswith('/publication_package_v2/RESEARCH_LOG.md')]
output={'pinned_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'initial_input_hash_changes':changes,
        'released_payload_hash_changes':payload_changes,
        'ancillary_change_explanation':'ROOT reported its genuine 01:10:59 preparation checkpoint appended only the v2 administrative research log after the initial independent pins. This file is not a ZIP member or released upload.',
        'supplemental_inputs_and_evidence':rows,'runtime_binary_pins':tools,'orchestrating_python_version':sys.version,
        'limitations':['TeX/fonts and transitive installed library bodies are not fully vendored by this audit',
                       'Recorded executable hashes and exact page-pixel readback establish this local reproduction; universal build equivalence is not claimed']}
(root/'FINAL_INPUT_PINS.json').write_text(json.dumps(output,indent=2)+'\n')
assert not payload_changes,payload_changes
print(json.dumps({'status':'PASS_RELEASED_INPUTS_UNCHANGED_WITH_DISCLOSED_ANCILLARY_LOG_DRIFT','ancillary_changes':changes,'supplemental_pins':len(rows),'binary_pins':tools,'python':sys.version},indent=2))

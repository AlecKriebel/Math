import datetime, hashlib, json, pathlib
root=pathlib.Path(__file__).resolve().parent
base=root.parent
inputs={
 'AGENTS.md':pathlib.Path('/Users/alec/Documents/Math/AGENTS.md'),
 'TURN_2.md':base/'snapshot/unsolved_math_prioritization/attempts/30003508/TURN_2.md',
 'TIKHONOV_EXISTENCE_REDUCTION.md':base/'priority_mechanism_adversary_01/TIKHONOV_EXISTENCE_REDUCTION.md',
}
(root/'inputs').mkdir(exist_ok=True)
rows=[]
for name,p in inputs.items():
 data=p.read_bytes(); (root/'inputs'/name).write_bytes(data)
 rows.append(dict(source=str(p),copy='inputs/'+name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
result=dict(frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=rows,
            criteria_sha256=hashlib.sha256((root/'CRITERIA.md').read_bytes()).hexdigest())
(root/'INPUT_PINS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

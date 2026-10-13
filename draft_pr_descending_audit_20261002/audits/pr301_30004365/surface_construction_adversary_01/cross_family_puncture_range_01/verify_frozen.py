#!/usr/bin/env python3
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent.parent
m=json.loads((root/'ARTIFACT_MANIFEST.json').read_text())
result={p:hashlib.sha256((root/p).read_bytes()).hexdigest()==v['sha256'] for p,v in m['files'].items()}
assert all(result.values())
(pathlib.Path(__file__).resolve().parent/'FROZEN_PRESERVATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

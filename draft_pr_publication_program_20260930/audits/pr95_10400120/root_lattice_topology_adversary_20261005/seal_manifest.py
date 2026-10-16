#!/usr/bin/env python3
"""Seal finite evidence inventory; no writes outside the audit directory."""
import datetime,hashlib,json,os,pathlib,sys
root=pathlib.Path(__file__).resolve().parent
began=datetime.datetime.now(datetime.timezone.utc).isoformat()
excluded={'EVIDENCE_MANIFEST.json','SHA256SUMS'}
entries=[]
for p in sorted(root.rglob('*')):
    if p.is_file() and p.relative_to(root).as_posix() not in excluded:
        data=p.read_bytes()
        entries.append(dict(path=p.relative_to(root).as_posix(),size=len(data),sha256=hashlib.sha256(data).hexdigest()))
receipts=[]
for p in sorted((root/'executions').glob('*.json')):
    r=json.loads(p.read_text())
    if not all(k in r for k in ['pid','argv','cwd','started_utc','ended_utc','exit_code','stdout_path','stderr_path']):
        raise RuntimeError('incomplete execution receipt: '+str(p))
    for stream in ['stdout','stderr']:
        f=p.parent/r[stream+'_path']
        if hashlib.sha256(f.read_bytes()).hexdigest()!=r[stream+'_sha256']:
            raise RuntimeError('stream hash mismatch: '+str(f))
    receipts.append(p.relative_to(root).as_posix())
for name,code in [('sealed_exact',0),('sealed_optimized',0),('sealed_false_normal',1),('sealed_false_optimized',1)]:
    r=json.loads((root/'executions'/f'{name}.json').read_text())
    if r['exit_code']!=code:
        raise RuntimeError('unexpected sealed receipt exit: '+name)
    current=hashlib.sha256((root/'root_lattice_check.py').read_bytes()).hexdigest()
    if r['input_sha256_at_execution'].get(str(root/'root_lattice_check.py'))!=current:
        raise RuntimeError('sealed checker hash mismatch: '+name)
if (root/'executions/sealed_exact.stdout').read_bytes()!=(root/'executions/sealed_optimized.stdout').read_bytes():
    raise RuntimeError('normal/optimized stdout differ')
manifest=dict(schema='closed-internal-audit-v1',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),root=str(root),incoming_head='6534ad01e519c719628a18984b108e73cf2e8ead',closure_exclusions=sorted(excluded),closure_explanation='Manifest itself and detached SHA256SUMS excluded to avoid circular hashes; all preexisting regular files included.',files=entries,execution_receipts=receipts,authoritative_final_receipts=['executions/sealed_exact.json','executions/sealed_optimized.json','executions/sealed_false_normal.json','executions/sealed_false_optimized.json'],source_urls={'hansen_takata_0209403v2.pdf':'https://arxiv.org/pdf/math/0209403v2','ohtsuki_2002_problems.pdf':'https://msp.org/gtm/2002/04/gtm-2002-04-024p.pdf'},manifest_generation=dict(pid=os.getpid(),argv=sys.argv,cwd=os.getcwd(),started_utc=began,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=0,stdout_full='',stderr_full=''),verification='all inventory and stream checks passed')
data=(json.dumps(manifest,indent=2)+'\n').encode()
(root/'EVIDENCE_MANIFEST.json').write_bytes(data)
checks=[(e['sha256'],e['path']) for e in entries]
checks.append((hashlib.sha256(data).hexdigest(),'EVIDENCE_MANIFEST.json'))
(root/'SHA256SUMS').write_text(''.join(h+'  '+p+'\n' for h,p in checks))

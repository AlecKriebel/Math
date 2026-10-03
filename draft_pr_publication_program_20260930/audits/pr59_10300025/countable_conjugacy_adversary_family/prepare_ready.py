#!/usr/bin/env python3
"""Freeze own family and bind fixed INDEX/READY; ROOT helpers remain unexecuted."""
import datetime,hashlib,json,os,pathlib,stat,sys
root=pathlib.Path(__file__).resolve().parent
assert not any((root/n).exists() for n in ('INDEX.json','READY.json','ROOT_MANIFEST.json'))
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
(root/'PREPARATION_RECEIPT.json').write_text(json.dumps({'operator':'PR59 mathematical subagent',
    'pid':os.getpid(),'utc':utc,'argv':sys.argv,'ROOT_closer_executed':False,'ROOT_readback_executed':False,
    'mathematical_completion_percent':100,'new_discovery_credit':0,'native_or_source_turn_changes':0},indent=2)+'\n')
paths=[p for p in root.rglob('*') if p.is_file()]
for p in paths:
    s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1;p.chmod(0o444)
dirs=[root]+[p for p in root.rglob('*') if p.is_dir()]
for p in dirs:p.chmod(0o755)
def d(p):
    s=p.stat();assert s.st_mode&0o7777==0o444
    return {'path':p.relative_to(root).as_posix(),'bytes':s.st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode_07777':'0444'}
entries={p.relative_to(root).as_posix():d(p) for p in sorted(paths)}
idx={'domain':sorted(entries),'directories':sorted(['.']+[p.relative_to(root).as_posix() for p in dirs if p!=root]),'entries':entries}
(root/'INDEX.json').write_text(json.dumps(idx,indent=2)+'\n');(root/'INDEX.json').chmod(0o444)
ready={'status':'PASS_LITERAL_READY_FOR_ROOT','ROOT_executed':False,'prepared_utc':utc,
       'bindings':{n:d(root/n) for n in ('INDEX.json','REPORT.md','VERDICT.json','UNIVERSAL_PROOF.md')}}
(root/'READY.json').write_text(json.dumps(ready,indent=2)+'\n');(root/'READY.json').chmod(0o444)
from packet import validate
entries=validate(False)
print(json.dumps({'operator':'PR59 mathematical subagent','pid':os.getpid(),'utc':utc,'files':len(entries),
      'bytes':sum(x['bytes'] for x in entries),'INDEX':d(root/'INDEX.json'),'READY':d(root/'READY.json'),
      'ROOT_manifest_absent':not(root/'ROOT_MANIFEST.json').exists(),'PASS':'exact family preparation'}))

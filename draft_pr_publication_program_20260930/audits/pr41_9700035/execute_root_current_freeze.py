"""ROOT actual freeze capture after complete source and mathematical review."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];S=A/'current_preparation_family'
sha=lambda b:hashlib.sha256(b).hexdigest()
source=S/'prepare_current_packet.py';raw=source.read_bytes()
assert sha(raw)=='b54462a367464e3459d9451b01666070afa6d090f910b76fcef60822f973095e'
assert sha((S/'PREPARATION_MANIFEST.json').read_bytes())=='bc6412589fa2d94c3728247735319cf980440cc976d609c138a6bbb3c0aa9e13'
prep=json.loads((S/'PREPARATION_MANIFEST.json').read_bytes());assert len(prep['files'])==23
for z in prep['files']:
 p=S/z['path'];assert p.is_file() and not p.is_symlink();b=p.read_bytes()
 assert len(b)==z['size'] and sha(b)==z['sha256']
before=json.loads((A/'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes())
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
assert head==before['current_head']
for z in before['files']:
 b=(R/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
ledger=json.loads((A/'ROOT_PRIMARY_READ_LEDGER.json').read_bytes())
card=json.loads((A/'ROOT_SCIENCE_CARD.json').read_bytes())
assert len(ledger['root_flags'])==8 and ledger['root_flags']==card['root_flags']
assert all(v is True for v in ledger['root_flags'].values())
argv=['/usr/bin/python3','-B',str(source),'--execute']
reviewed=[]
for flag,name in [('root-scope-certificate','ROOT_PARTIAL_SCOPE_CERTIFICATE.md'),
                  ('root-read-ledger','ROOT_PRIMARY_READ_LEDGER.json'),
                  ('root-science-card','ROOT_SCIENCE_CARD.json'),
                  ('root-current-input-manifest','ROOT_CURRENT_INPUT_PREIMAGES.json')]:
 b=(A/name).read_bytes();reviewed.append(dict(path=name,bytes=len(b),sha256=sha(b)))
 argv.extend(['--'+flag+'-sha256',sha(b)])
O=A/'root_current_freeze_actual_capture';O.mkdir(exist_ok=False)
(O/'prelaunch_source.py').write_bytes(raw)
row=dict(argv=argv,cwd=str(A),source_sha256=sha(raw),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
         actual_execution=False,completed=False,stdin_supplied=False,head_before=head,
         fresh_native13_before=before['files'],complete_reviewed_prerequisites=reviewed)
child=None;out=err=b''
try:
 child=subprocess.Popen(argv,cwd=A,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 row.update(pid=child.pid,actual_execution=True)
 try:out,err=child.communicate(timeout=180)
 except subprocess.TimeoutExpired:
  child.kill();out,err=child.communicate();row['timed_out']=True
 row.update(completed=True,exit_code=child.returncode)
except OSError as error:row.update(pid=None,exit_code=None,launch_error=str(error))
finally:
 row['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
 for channel,b in [('stdout',out),('stderr',err)]:
  p=O/(channel+'.bin');p.write_bytes(b);row[channel]=dict(path=p.name,bytes=len(b),sha256=sha(b))
 after=[]
 for z in before['files']:
  b=(R/z['path']).read_bytes();after.append(dict(path=z['path'],bytes=len(b),sha256=sha(b)))
 row['fresh_native13_after']=after
 row['head_after']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
 row['source_and_prerequisites_unchanged']=source.read_bytes()==raw and all(len((A/z['path']).read_bytes())==z['bytes'] and sha((A/z['path']).read_bytes())==z['sha256'] for z in reviewed)
 row['native13_and_HEAD_unchanged']=after==before['files'] and row['head_after']==head
 row['status']='PASS' if row.get('exit_code')==0 and not row.get('timed_out') and row['source_and_prerequisites_unchanged'] and row['native13_and_HEAD_unchanged'] else 'FAIL'
 (O/'CAPTURE.json').write_text(json.dumps(row,indent=2)+'\n')
assert row['status']=='PASS'
result=json.loads(out);assert result['status']=='CURRENT_PACKET_FROZEN_NEW_WHOLE_GATE_PENDING'
print(json.dumps(dict(status=row['status'],pid=row['pid'],exit_code=row['exit_code'],capture_sha256=sha((O/'CAPTURE.json').read_bytes()),entire_child_stdout=result)))

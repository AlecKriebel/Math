"""Preserve the complete author streams in this review folder."""
import subprocess,sys,json,hashlib
from pathlib import Path
root=Path(__file__).parent.parent
packet=root/'raw_sources'/'frozen_packet'
out=root/'checks'/'author_streams';out.mkdir(exist_ok=True)
records=[]
for name in ['verify_turn1.py','verify_turn2.py','verify_turn3.py','verify_turn4.py','verify_turn5.py','hessian_certificate.py','REPLAY_ALL.py']:
 r=subprocess.run([sys.executable,str(packet/name)],cwd=packet,capture_output=True)
 (out/(name+'.stdout.txt')).write_bytes(r.stdout)
 (out/(name+'.stderr.txt')).write_bytes(r.stderr)
 records.append({'program':name,'exit_code':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_bytes':len(r.stderr)})
 assert r.returncode==0,(name,r.stderr.decode())
print(json.dumps(records,indent=2,sort_keys=True))

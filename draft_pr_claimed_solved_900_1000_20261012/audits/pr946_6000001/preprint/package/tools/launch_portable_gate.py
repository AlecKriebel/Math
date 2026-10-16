"""Externally authenticate this regular launcher BEFORE execution. No OS sandbox.
Untrusted gate/worker/comparator paths are nonblocking-read, bounded and hashed first.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('REJECTED: launcher requires python -I -S -B')
import argparse,hashlib,os,stat,tempfile,runpy,json
from pathlib import Path
TOOL_CAP=262144
STAGE='arguments'
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def opened_dir(path):
 fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NONBLOCK)
 try:
  for part in Path(os.path.abspath(path)).parts[1:]:
   nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd);os.close(fd);fd=nxt
  return fd
 except BaseException:os.close(fd);raise
def anchored(path,pin):
 require(len(pin)==64 and all(c in '0123456789abcdef' for c in pin),'Malformed external pin')
 parent=opened_dir(path.parent)
 try:fd=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent)
 finally:os.close(parent)
 try:
  info=os.fstat(fd);require(stat.S_ISREG(info.st_mode),'Executable path is not regular');require(0<=info.st_size<=TOOL_CAP,'Executable exceeds 262144-byte cap')
  chunks=[];remaining=TOOL_CAP+1
  while remaining:
   raw=os.read(fd,min(65536,remaining))
   if not raw:break
   chunks.append(raw);remaining-=len(raw)
  raw=b''.join(chunks);require(len(raw)<=TOOL_CAP and len(raw)==info.st_size,'Executable changed during bounded read')
 finally:os.close(fd)
 require(hashlib.sha256(raw).hexdigest()==pin,'External executable anchor mismatch '+str(path));return raw
def main():
 global STAGE
 p=argparse.ArgumentParser();p.add_argument('packet',type=Path);p.add_argument('--gate',type=Path,required=True);p.add_argument('--gate-sha256',required=True);p.add_argument('--worker',type=Path,required=True);p.add_argument('--worker-sha256',required=True);p.add_argument('--comparator',type=Path,required=True);p.add_argument('--comparator-sha256',required=True);p.add_argument('--scratch',type=Path,required=True);p.add_argument('--worker-optimize',type=int,choices=(0,1,2),default=0);p.add_argument('--test-corrupt-copy',action='store_true');p.add_argument('--test-false-assert',action='store_true');a=p.parse_args()
 print(json.dumps(dict(launcher_outer_optimize=sys.flags.optimize,isolated=sys.flags.isolated,debug=__debug__,bytecode_disabled=sys.dont_write_bytecode)),file=sys.stderr)
 STAGE='nonblocking executable authentication';gate=anchored(a.gate,a.gate_sha256);worker=anchored(a.worker,a.worker_sha256);comp=anchored(a.comparator,a.comparator_sha256)
 fd=opened_dir(a.scratch);os.close(fd)
 with tempfile.TemporaryDirectory(prefix='trusted6000001-launch-',dir=a.scratch) as td:
  top=Path(td);paths=[top/'gate.py',top/'worker.py',top/'comparator.py']
  for path,raw in zip(paths,[gate,worker,comp]):path.write_bytes(raw)
  for path,pin in zip(paths,[a.gate_sha256,a.worker_sha256,a.comparator_sha256]):anchored(path,pin)
  sys.argv=[str(paths[0]),str(a.packet),'--gate-sha256',a.gate_sha256,'--worker',str(paths[1]),'--worker-sha256',a.worker_sha256,'--comparator',str(paths[2]),'--comparator-sha256',a.comparator_sha256,'--scratch',str(a.scratch),'--worker-optimize',str(a.worker_optimize)]+(['--test-corrupt-copy'] if a.test_corrupt_copy else [])+(['--test-false-assert'] if a.test_false_assert else [])
  STAGE='authenticated gate execution';module={'__file__':str(paths[0]),'__name__':'__main__'};exec(compile(gate,str(paths[0]),'exec'),module)
if __name__=='__main__':
 try:main()
 except Exception as exc:raise SystemExit('REJECTED at '+STAGE+': '+str(exc))

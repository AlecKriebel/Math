import sys,os,stat,hashlib
from pathlib import Path
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
 raise RuntimeError("Trusted launch requires -I -S -B")
root=Path("/Users/alec/Documents/Math")
program=root/"draft_pr_claimed_solved_900_1000_20261012"
audit=program/"audits/pr967_2616"
expected={
 program/"close_pr967.py":(71687,"4a9a273e37d43b7d987dea29319aaa4ca70f14432e6bafb568ee5f6af9130c88"),
 program/"finalize_pr967_and_gate_next.py":(7225,"59f46a1f29140fc2018f9bb10ea3f2989dbaf0313ab33acf32f02ba05b787533"),
 audit/"CLOSURE_OPERATIONS_INVENTORY.json":(538,"1aec2d70a27a8ef251c8478932d1cd578c0a259e075fec591edc345c19d8745a")}
captured={}
for path,(size,digest) in expected.items():
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 try:
  info=os.fstat(fd)
  if not(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and info.st_size==size):
   raise RuntimeError("Trusted launch input type/size mismatch: "+str(path))
  chunks=[];total=0
  while total<=size:
   chunk=os.read(fd,min(1048576,size+1-total))
   if not chunk:break
   chunks.append(chunk);total+=len(chunk)
  raw=b"".join(chunks)
  if len(raw)!=size or hashlib.sha256(raw).hexdigest()!=digest:
   raise RuntimeError("Trusted launch input byte mismatch: "+str(path))
  captured[path]=raw
 finally:os.close(fd)
if len(sys.argv)<2 or sys.argv[1] not in ("close","finalize"):
 raise RuntimeError("Trusted launch requires explicit close or finalize action")
action=sys.argv[1]
target=program/("close_pr967.py" if action=="close" else "finalize_pr967_and_gate_next.py")
sys.argv=[str(target),"--operations-sha256","1aec2d70a27a8ef251c8478932d1cd578c0a259e075fec591edc345c19d8745a","--disposition-sha256","1c783ed45d2b15500ec4ebf83f071373ea1e49cd342ec1f8a3cbfbf102c86160",*sys.argv[2:]]
namespace={"__name__":"__main__","__file__":str(target)}
exec(compile(captured[target],str(target),"exec",dont_inherit=True,optimize=0),namespace)

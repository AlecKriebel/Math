import sys,os,stat,hashlib
from pathlib import Path
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
 raise RuntimeError("Trusted launch requires -I -S -B")
root=Path("/Users/alec/Documents/Math")
program=root/"draft_pr_claimed_solved_900_1000_20261012"
audit=program/"audits/pr967_2616"
expected={
 program/"close_pr967.py":(71524,"c6231a47758a6b037ed005883d39e374946e38bd9aec0c74eb33df3afe2d2a45"),
 program/"finalize_pr967_and_gate_next.py":(7062,"47520f8f86889db8c5b85fc7000486773d2ca4e8601ad00531bad2fdce5143cb"),
 audit/"CLOSURE_OPERATIONS_INVENTORY.json":(538,"ad94d62072583e62092215bf919c974f237d52efb1f048e60bbee5724a370d0d")}
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
sys.argv=[str(target),"--operations-sha256","ad94d62072583e62092215bf919c974f237d52efb1f048e60bbee5724a370d0d","--disposition-sha256","2d3e28bd446adc1707af8dc8b006c767ca2b09c9ca55658cf33b5717b58e8393",*sys.argv[2:]]
namespace={"__name__":"__main__","__file__":str(target)}
exec(compile(captured[target],str(target),"exec",dont_inherit=True,optimize=0),namespace)

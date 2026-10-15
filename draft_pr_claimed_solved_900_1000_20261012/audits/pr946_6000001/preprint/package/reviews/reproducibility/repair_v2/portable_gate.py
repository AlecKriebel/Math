"""Separate portable replay gate. Externally authenticate gate, worker and comparator before use.
Only the 33 unchanged original files belong in PACKET. No OS sandbox is supplied.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('REJECTED: gate requires python -I -S -B')
import argparse,hashlib,json,os,stat,tempfile,subprocess
from pathlib import Path
EXPECTED={'ACCEPTANCE.md': {'bytes': 3416, 'sha256': 'db5c4d918a77535b9485a6c3ca99554173917a25d7364ee1c979622733f8b248'}, 'PUBLIC_MANIFEST.json': {'bytes': 5553, 'sha256': '29cb50b07af6a65b633516b5d86eed1dae93d57cf2abfb264b18eb9555a29903'}, 'README.md': {'bytes': 4345, 'sha256': '7d5ae98a7d715e98ceaeadce5261779307bc55567c63c1d5f9d9263a1e158050'}, 'RESEARCH_LOG.md': {'bytes': 1672, 'sha256': 'b9a799a364ab5a4286673af1bd0d27b788eeaf083f2f573d3b19b42aa42b68c5'}, 'independent_audit_b/public/ACCEPTANCE.json': {'bytes': 3532, 'sha256': '1c35f2e82a70e0ea2d2593246dc2c59917105626a59a0a87bd4b181d05e93e30'}, 'independent_audit_b/public/AUTHOR_FREEZE_VERIFICATION.json': {'bytes': 3734, 'sha256': '767f76d9e887f21605325bfeb522b87826690b9b0d23510eca99af0eaae9b5e0'}, 'independent_audit_b/public/CITATION_SCOPE_NOTE.md': {'bytes': 1224, 'sha256': '317c4a42368a0c91851b62b0bed5f06bb0c1492a14d206bcaf8f172bee14c4d2'}, 'independent_audit_b/public/FULL_REPORT.md': {'bytes': 17587, 'sha256': '30835bc1fc35af2ec92efe4ebdbe63682c5616018a0a5918fec79da4984ca5af'}, 'independent_audit_b/public/INDEPENDENT_CHECKS.json': {'bytes': 2408, 'sha256': '66bd954a41dd207b7c2ba3dbe6bb3bd0a676743ef464f62196e6a7809a634d8d'}, 'independent_audit_b/public/MANIFEST.json': {'bytes': 1846, 'sha256': '8bbb5b62a4610881e7b1f78a52f7c208723529304dd0e8ab341a1be9f1283459'}, 'independent_audit_b/public/README.md': {'bytes': 2288, 'sha256': 'e0b7f9a9e538171d227fe024acc84f484cfc2c0c6f70bc85db3247e1226592ea'}, 'independent_audit_b/public/SOURCE_METADATA.json': {'bytes': 6214, 'sha256': 'bbe5fa5a629dc56ca19821924dc9a1dd5868dcb386a0ffaaf4e469cfc3d47042'}, 'independent_audit_b/public/independent_checks.py': {'bytes': 8093, 'sha256': '7dd8f4f84487d58857d83bd7c8a1f2e869ff196e36b3dc18fcc71a09a1244913'}, 'independent_audit_b/public/verify_audit.py': {'bytes': 2716, 'sha256': '5e4fb7cc63318cc0f7ad0819afd649cf0e04b86ec251f0a5da47bdb6048b54ee'}, 'independent_global_audit/public/ACCEPTANCE.json': {'bytes': 3736, 'sha256': 'de437fc1e013369caafa7c04851c3aac2a2f1bc4ada202556e27b0c7d5a4fe9d'}, 'independent_global_audit/public/GLOBAL_AUDIT.md': {'bytes': 21816, 'sha256': 'e994d88460adb511bc1b77e040ff0251146713247bd2bcd422a98527a343fdcc'}, 'independent_global_audit/public/INDEPENDENT_CONTROLS.json': {'bytes': 2335, 'sha256': '0840bcf082043f84427cd92be2bbcd60f4cb7aab8d6252db7ff9a1b318ce2d53'}, 'independent_global_audit/public/MANIFEST.json': {'bytes': 1481, 'sha256': '22d1bab327e70db3d594c2580f592256bb342bd33c1081fa07beb1c197f0edff'}, 'independent_global_audit/public/README.md': {'bytes': 2583, 'sha256': '75f406ead984e7568ed1b09ef8d1ba4b577375e019c8314850d487a060ee81d4'}, 'independent_global_audit/public/SOURCE_METADATA.json': {'bytes': 6450, 'sha256': '15981b701db9969079cd4071e008fa5f1533ad637902847c209c88cb41f42430'}, 'independent_global_audit/public/independent_controls.py': {'bytes': 7391, 'sha256': 'dadd66968031fe3f22d1a9caad47680cc2d2ffa50c35cfe794d432f2b0b3fa90'}, 'independent_global_audit/public/verify_audit_packet.py': {'bytes': 2483, 'sha256': '811b3cfe9cc5b83581412babe800f71ba39151f3bcf1c2ba74630bf8c2ac97f4'}, 'mutation_tests.py': {'bytes': 6272, 'sha256': 'ea39250778445149237fb6fd03581f21eff7059d7cd71895fa5cb7874a8e0b64'}, 'public/APPROACH_LEDGER.md': {'bytes': 4713, 'sha256': '25b12a76a78750a9e22f05053817b12ad328a6d3add610651b0fa03f9ac8cf42'}, 'public/INHERITED_CHECK_SUMMARY.json': {'bytes': 2290, 'sha256': '919018bf129312dc0cf8eae8fdd42cf18617a0b76dc2cdce5b8186ed4a8d27df'}, 'public/MANIFEST.json': {'bytes': 1433, 'sha256': '7df56d745e4c57a30d0303388b1adda3e52d1c99190d2f96fe50b6d616b1cf3f'}, 'public/PROOF.md': {'bytes': 17635, 'sha256': 'a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2'}, 'public/README.md': {'bytes': 2344, 'sha256': 'a6b9b20a372ce977f74ed007e47414003790d72ca9916368090dbb69ed767f4c'}, 'public/SOURCE_METADATA.json': {'bytes': 3593, 'sha256': '76aa5c4a2267d062fdd76505295500bbfb4a3dfb68e54c30478943954207ca0f'}, 'public/VERIFICATION.json': {'bytes': 1541, 'sha256': '2596ca22343e5e4716272935288eff0bbcd377a59a842b875c5e0ae5f144e7b5'}, 'public/verify_math.py': {'bytes': 5145, 'sha256': '473fa4a62edb79721a685413c5eb3c541a7b6ed03eebbaf5786100ca07ee2ad3'}, 'public/verify_packet.py': {'bytes': 1010, 'sha256': '9d72df978e6645bad9d984cc162cc3b202ba4c40213a5b833eac5a8625f5673e'}, 'verify_publication.py': {'bytes': 11681, 'sha256': '7b0c100d43d1296afa01279476688391bc35a2291ea5858915b70ef2c1810625'}}
DIRS={'public','independent_global_audit','independent_global_audit/public','independent_audit_b','independent_audit_b/public'}
TOOL_CAP=262144
STAGE='arguments'
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def bounded_read(fd,limit,expected_size=None):
 info=os.fstat(fd)
 require(stat.S_ISREG(info.st_mode),'Opened object is not a regular file')
 require(0<=info.st_size<=limit,'File exceeds bounded byte cap')
 if expected_size is not None:require(info.st_size==expected_size,'Original byte size differs before reading')
 chunks=[];remaining=limit+1
 while remaining:
  block=os.read(fd,min(65536,remaining))
  if not block:break
  chunks.append(block);remaining-=len(block)
 data=b''.join(chunks)
 require(len(data)<=limit and len(data)==info.st_size,'File changed or exceeded byte cap during read')
 if expected_size is not None:require(len(data)==expected_size,'Original read length differs')
 return data
def anchored(path,pin):
 require(type(pin) is str and len(pin)==64 and all(x in '0123456789abcdef' for x in pin),'Malformed external pin')
 fd=opened_dir(path.parent)
 try:
  child=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
  try:
   data=bounded_read(child,TOOL_CAP)
  finally:os.close(child)
 finally:os.close(fd)
 require(sha(data)==pin,'External executable anchor mismatch '+str(path));return data
def opened_dir(path):
 # Open every ancestor without following links, then traverse descriptor-relative.
 absolute=os.path.abspath(path);fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NONBLOCK)
 try:
  for part in Path(absolute).parts[1:]:
   nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NONBLOCK|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  return fd
 except BaseException:os.close(fd);raise
def snapshot(path):
 fd=opened_dir(path);found={};dirs=set()
 def walk(current,prefix=''):
  with os.scandir(current) as entries:
   for ent in entries:
    name=prefix+ent.name;mode=ent.stat(follow_symlinks=False).st_mode
    if stat.S_ISDIR(mode):
     require(name in DIRS,'Unexpected directory '+name);dirs.add(name)
     child=os.open(ent.name,os.O_RDONLY|os.O_DIRECTORY|os.O_NONBLOCK|os.O_NOFOLLOW,dir_fd=current)
     try:walk(child,name+'/')
     finally:os.close(child)
    else:
     require(stat.S_ISREG(mode) and name in EXPECTED,'Unexpected, linked or special file '+name)
     child=os.open(ent.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=current)
     try:
      raw=bounded_read(child,EXPECTED[name]['bytes'],EXPECTED[name]['bytes'])
     finally:os.close(child)
     row=EXPECTED[name];require(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'Original payload differs '+name);found[name]=raw
 try:walk(fd)
 finally:os.close(fd)
 require(set(found)==set(EXPECTED) and dirs==DIRS,'Closed inventory mismatch');return found
BOOT='''import sys,json,runpy
print(json.dumps(dict(optimize=sys.flags.optimize,debug=__debug__,isolated=sys.flags.isolated,bytecode_disabled=sys.dont_write_bytecode)),file=sys.stderr)
if sys.flags.optimize!=0 or not __debug__ or not sys.flags.isolated or not sys.dont_write_bytecode:raise SystemExit('REJECTED: unsafe worker mode')
p=sys.argv[1];sys.argv=sys.argv[1:];runpy.run_path(p,run_name='__main__')
'''
def main():
 global STAGE
 p=argparse.ArgumentParser();p.add_argument('packet',type=Path);p.add_argument('--gate-sha256',required=True);p.add_argument('--worker',type=Path,required=True);p.add_argument('--worker-sha256',required=True);p.add_argument('--comparator',type=Path,required=True);p.add_argument('--comparator-sha256',required=True);p.add_argument('--scratch',type=Path,required=True);p.add_argument('--worker-optimize',type=int,choices=(0,1,2),default=0);p.add_argument('--test-corrupt-copy',action='store_true');p.add_argument('--test-false-assert',action='store_true');a=p.parse_args()
 STAGE='external executable anchors';anchored(Path(__file__),a.gate_sha256);worker=anchored(a.worker,a.worker_sha256);comparator=anchored(a.comparator,a.comparator_sha256)
 STAGE='source authentication';before=snapshot(a.packet)
 STAGE='scratch ancestors';fd=opened_dir(a.scratch);os.close(fd)
 with tempfile.TemporaryDirectory(prefix='portable6000001-',dir=a.scratch) as td:
  top=Path(td);root=top/'packet';root.mkdir(mode=0o700)
  for name,raw in before.items():
   q=root/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
  work=top/'worker.py';work.write_bytes(worker);comp=top/'comparator.py';comp.write_bytes(comparator)
  if a.test_corrupt_copy:(root/'public/verify_math.py').write_bytes(b'raise RuntimeError("copy tampered")\n')
  STAGE='copied bytes authentication';require(snapshot(root)==before,'Copied packet differs');anchored(work,a.worker_sha256);anchored(comp,a.comparator_sha256)
  STAGE='worker execution';cmd=[sys.executable,'-I','-B']+(['-'+'O'*a.worker_optimize] if a.worker_optimize else [])+['-c',BOOT,str(work),str(root),str(comp),a.comparator_sha256]+(['--test-false-assert'] if a.test_false_assert else [])
  env={k:v for k,v in os.environ.items() if not k.upper().startswith('PYTHON')};r=subprocess.run(cmd,cwd=top,env=env,capture_output=True,text=True,timeout=1200)
  require(r.returncode==0,'Worker failed\n'+r.stderr+'\n'+r.stdout);result=json.loads(r.stdout);require(result.get('status')=='PASS','Worker did not PASS')
  STAGE='post replay authentication';require(snapshot(root)==before and snapshot(a.packet)==before,'Packet changed during replay')
  print(json.dumps(dict(status='PASS',gate_outer_optimize=sys.flags.optimize,worker_bootstrap_flags=json.loads(r.stderr.splitlines()[0]),original_manifest_sha256=EXPECTED['PUBLIC_MANIFEST.json']['sha256'],proof_sha256=EXPECTED['public/PROOF.md']['sha256'],original_files=33,worker=result,limitation='Finite consistency only. Trusted local Python/runtime/site packages and process/filesystem are assumed; no OS sandbox. External pins must come from a trusted separate record; an attacker controlling that record can replace the checker.'),indent=2))
if __name__=='__main__':
 try:main()
 except Exception as exc:raise SystemExit('REJECTED at '+STAGE+': '+str(exc))

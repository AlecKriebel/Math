import sys
if not sys.flags.safe_path:raise SystemExit('safe startup')
import pathlib,os,hashlib,subprocess,tempfile,json,base64,time,datetime
R=pathlib.Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';W=A/'reviews/full_package_01';P=W/'private/cold/package'
F=json.loads((A/'preprint/FREEZE.json').read_text());rows=[]
BOOT="import sys,base64;raw=base64.b64decode(sys.argv[1]);p=sys.argv[2];N={'__name__':'_read_only_test_','__file__':p};exec(compile(raw,p,'exec'),N);N['anchored'](__import__('pathlib').Path(sys.argv[3]),'0'*64)"
with tempfile.TemporaryDirectory(dir=W/'private') as td:
 fifo=pathlib.Path(td)/'pipe';os.mkfifo(fifo)
 for label,rel in [('historical_v1','reviews/reproducibility/portable_gate.py'),('current_v2','tools/portable_gate.py')]:
  b=(P/rel).read_bytes();record=F['files']['package/'+rel]
  if len(b)!=record['bytes'] or hashlib.sha256(b).hexdigest()!=record['sha256']:raise ValueError('tool pin')
  start=time.monotonic()
  try:r=subprocess.run([sys.executable,'-I','-S','-B','-c',BOOT,base64.b64encode(b).decode(),str(P/rel),str(fifo)],capture_output=True,text=True,timeout=1)
  except subprocess.TimeoutExpired:row={'tool':label,'timed_out':True,'elapsed_seconds':time.monotonic()-start}
  else:row={'tool':label,'timed_out':False,'elapsed_seconds':time.monotonic()-start,'returncode':r.returncode,'stderr':r.stderr}
  rows.append(row)
 if not rows[0]['timed_out'] or rows[1]['timed_out'] or rows[1]['returncode']==0 or 'regular' not in rows[1]['stderr']:raise RuntimeError('FIFO behavior unexpected')
(W/'FIFO_ADVERSARY.json').write_text(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'controls':rows,'interpretation':'Historical v1 tool-open blocks before regular-file test; current v2 O_NONBLOCK open and fstat promptly reject. Historical bytes preserved. No current-universal-proof conclusion.','external_actions':0},indent=2)+'\n');print('PASS historical FIFO timeout, current v2 rejection')

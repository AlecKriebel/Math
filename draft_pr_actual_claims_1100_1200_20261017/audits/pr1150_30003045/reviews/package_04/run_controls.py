from pathlib import Path
import shutil,subprocess,hashlib,json,os,socket
D=Path(__file__).absolute().parent;B=D/'private/source';T=D/'private/controls';T.mkdir(exist_ok=True)
P='draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045'
outputs=['output/mixed-kato-counterexample-source-and-verification.zip','output/zenodo-upload-kit.zip','PACKAGE_RECEIPT.json']
def fp(p):
 if p.is_symlink():return {'type':'symlink','target':os.readlink(p)}
 if not p.exists():return {'type':'absent'}
 st=p.stat();r={'type':'file' if p.is_file() else 'directory' if p.is_dir() else 'other','inode':st.st_ino,'mtime_ns':st.st_mtime_ns}
 if p.is_file():r.update(bytes=st.st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 return r
def fresh(name):
 p=T/name
 if p.exists():shutil.rmtree(p)
 shutil.copytree(B,p);return p
def run(root,flags,prog='build_package.py'):
 r=subprocess.run(['python3','-B',*flags,str(root/prog)],cwd=root,capture_output=True,timeout=30)
 return {'exit':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr':r.stderr.decode()}
records=[]
for mode,flags in [('normal',[]),('optimized',['-O'])]:
 for idx,target in enumerate(outputs):
  for kind in ['directory','fifo','socket','symlink','hardlink']:
   label=f'{mode}-{idx}-{kind}';r=fresh(label);p=r/target;p.unlink(missing_ok=True)
   sentinel=T/(label+'.sentinel');sentinel.write_bytes(('DISTINCT OUTSIDE SENTINEL '+label+'\n').encode());before_s=fp(sentinel);sock=None
   if kind=='directory':p.mkdir()
   elif kind=='fifo':os.mkfifo(p)
   elif kind=='socket':
    sock=socket.socket(socket.AF_UNIX);prior=Path.cwd();os.chdir(r)
    try:sock.bind(target)
    finally:os.chdir(prior)
   elif kind=='symlink':p.symlink_to(sentinel)
   elif kind=='hardlink':os.link(sentinel,p)
   before={n:fp(r/n) for n in outputs};res=run(r,flags);after={n:fp(r/n) for n in outputs};outside=fp(sentinel)==before_s
   if sock:sock.close()
   expected_success=kind=='hardlink'
   preserved=all(after[n]==before[n] for n in outputs if n!=target)
   if expected_success:
    # Atomic replacement must break the target alias while leaving DIFFERENT bytes intact outside.
    okay=res['exit']==0 and outside and (r/target).read_bytes()==(B/target).read_bytes() and (r/target).stat().st_ino!=sentinel.stat().st_ino
   else:okay=res['exit']!=0 and outside and preserved
   records.append({'label':label,'destination':target,'kind':kind,'result':res,'outside_sentinel_unchanged':outside,'other_outputs_exactly_preserved':preserved,'before':before,'after':after,'PASS':okay})
   if not okay:raise ValueError(label)
 # non-directory ancestor and output directory alias preflight, before any write
 for kind in ['file-ancestor','directory-symlink']:
  label=f'{mode}-{kind}';r=fresh(label);out=r/'output';shutil.rmtree(out)
  sentinel=T/(label+'.sentinel');sentinel.write_bytes(('DIFFERENT ANCESTOR '+label).encode());before_s=fp(sentinel)
  if kind=='file-ancestor':out.write_bytes(b'not a directory')
  else:
   copied=T/(label+'-outside');shutil.copytree(B/'output',copied);out.symlink_to(copied,target_is_directory=True)
  before={n:fp(r/n) for n in outputs};res=run(r,flags);after={n:fp(r/n) for n in outputs}
  preserved=before==after and fp(sentinel)==before_s
  records.append({'label':label,'result':res,'before':before,'after':after,'outside_sentinel_unchanged':fp(sentinel)==before_s,'PASS':res['exit']!=0 and preserved})
  if not records[-1]['PASS']:raise ValueError(label)
 # runners must authenticate before executing altered mathematical code
 for kind in ['corrupt-proof','missing-listed','extra-file','extra-directory','listed-symlink','extra-directory-symlink','audit-ancestor-symlink','unsafe-allowlist']:
  label=f'{mode}-runner-{kind}';r=fresh(label);a=r/P;c=a/'pr_repair_candidate'
  if kind=='corrupt-proof':(a/'FINAL_PROOF.md').write_text('altered')
  elif kind=='missing-listed':(c/'SOURCE_AUDIT.md').unlink()
  elif kind=='extra-file':(c/'unlisted.txt').write_text('extra')
  elif kind=='extra-directory':(c/'unlisted').mkdir()
  elif kind=='listed-symlink':
   p=c/'SOURCE_AUDIT.md';q=T/(label+'.sentinel');q.write_bytes(p.read_bytes());p.unlink();p.symlink_to(q)
  elif kind=='extra-directory-symlink':(c/'unlisted').symlink_to(T,target_is_directory=True)
  elif kind=='audit-ancestor-symlink':
   q=T/(label+'-audit');a.rename(q);a.symlink_to(q,target_is_directory=True)
  elif kind=='unsafe-allowlist':
   p=r/'verification/AUDIT_MEMBERS.json';data=json.loads(p.read_text());data['../outside.txt']={'bytes':0,'sha256':hashlib.sha256(b'').hexdigest()};p.write_text(json.dumps(data))
  res=run(r,flags,'verification/verify_all.py');records.append({'label':label,'result':res,'PASS':res['exit']!=0})
  if not records[-1]['PASS']:raise ValueError(label)
 # outer builder must reject valid-payload authored-directory alias too
 label=f'{mode}-builder-audit-ancestor-symlink';r=fresh(label);a=r/P;q=T/(label+'-audit');a.rename(q);a.symlink_to(q,target_is_directory=True)
 before={n:fp(r/n) for n in outputs};res=run(r,flags);after={n:fp(r/n) for n in outputs};records.append({'label':label,'result':res,'PASS':res['exit']!=0 and before==after})
 # metadata mismatch separate from mathematical wrong-result controls
 label=f'{mode}-builder-metadata-mismatch';r=fresh(label);p=r/'zenodo-metadata.json';data=json.loads(p.read_text());data['title']='different';p.write_text(json.dumps(data));before={n:fp(r/n) for n in outputs};res=run(r,flags);after={n:fp(r/n) for n in outputs};records.append({'label':label,'result':res,'PASS':res['exit']!=0 and before==after})
(D/'PATH_INTEGRITY_CONTROLS.json').write_text(json.dumps(records,indent=2)+'\n');print('Controls',len(records),'passed',sum(r['PASS'] for r in records));print([(r['label'],r['PASS']) for r in records])

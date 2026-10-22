from pathlib import Path
import subprocess,shutil,os,json,datetime,hashlib
P=Path(__file__).absolute().parent;release=P/'private/release';base=P/'private/controls';base.mkdir(exist_ok=True)
prefix=Path('draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045');outputs=['output/mixed-kato-counterexample-source-and-verification.zip','output/zenodo-upload-kit.zip','PACKAGE_RECEIPT.json'];rows=[]
def pin(p):
 if p.is_dir():return {'directory':True}
 if not p.exists():return None
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(case,prog,opt,setup):
 name=f'{case}-{prog}-{opt}';r=base/name;shutil.copytree(release,r);outside=base/(name+'-outside');outside.mkdir();details=setup(r,outside) or {};before={n:pin(r/n) for n in outputs};sentinel=outside/'sentinel';old=sentinel.read_bytes() if sentinel.is_file() else None
 p=subprocess.run(['python3','-B',*(['-O'] if opt else []),*(['verification/verify_all.py'] if prog=='verifier' else ['build_package.py'])],cwd=r,capture_output=True,timeout=30)
 row={'case':case,'program':prog,'optimized':opt,'exit':p.returncode,'last_stderr':p.stderr.decode().splitlines()[-1] if p.stderr else '', 'outputs_unchanged':all(pin(r/n)==before[n] for n in outputs),'outside_sentinel_preserved':old is None or sentinel.read_bytes()==old,**details};rows.append(row)
 shutil.rmtree(r);shutil.rmtree(outside)

def writecorrupt(r,o):
 p=r/prefix/'FINAL_PROOF.md';p.write_bytes(p.read_bytes()+b'\nCORRUPT\n')
def missing(r,o):(r/prefix/'pr_repair_candidate/README.md').unlink()
def flatfile(r,o):(r/prefix/'pr_repair_candidate/extra').write_text('extra')
def flatdir(r,o):(r/prefix/'pr_repair_candidate/extra').mkdir()
def flatlink(r,o):(r/prefix/'pr_repair_candidate/extra').symlink_to(o,target_is_directory=True)
def ancestor(r,o):
 p=r/prefix/'reviews/norm_obstruction_01';shutil.move(str(p),str(o/'same-payload'));p.symlink_to(o/'same-payload',target_is_directory=True)
def leaf(r,o):
 p=r/prefix/'pr_repair_candidate/COUNTEREXAMPLE.md';shutil.move(str(p),str(o/'sentinel'));p.symlink_to(o/'sentinel')
def traversal(r,o):
 p=r/'verification/AUDIT_MEMBERS.json';a=json.loads(p.read_text());a['../escape']={'bytes':0,'sha256':'0'*64};p.write_text(json.dumps(a))
def baseline(r,o):
 p=r/prefix/'pr_repair_candidate/symbols_expected.json';p.write_bytes(p.read_bytes()+b' ')
for opt in [False,True]:
 for prog in ['verifier','builder']:
  for case,fn in [('proof-corruption',writecorrupt),('missing-current',missing),('flat-extra-file',flatfile),('flat-extra-directory',flatdir),('flat-extra-directory-symlink',flatlink),('authored-input-ancestor-symlink',ancestor),('current-leaf-symlink',leaf),('allowlist-traversal',traversal),('baseline-corruption',baseline)]:run(case,prog,opt,fn)
 for index,output in enumerate(outputs):
  def alias(r,o,output=output):
   for n in outputs:(r/n).write_text('PREEXISTING-'+n)
   (o/'sentinel').write_bytes(b'PRIVATE OUTSIDE SENTINEL\x00\xff');(r/output).unlink();(r/output).symlink_to(o/'sentinel');return {'destination':output,'guard_class':'output-symlink'}
  run('output-symlink-'+str(index),'builder',opt,alias)
  def hardlink(r,o,output=output):
   (o/'sentinel').write_bytes((r/output).read_bytes());(r/output).unlink();os.link(o/'sentinel',r/output);return {'destination':output,'guard_class':'hardlink-atomic-replacement'}
  run('output-hardlink-'+str(index),'builder',opt,hardlink)
  def directory(r,o,output=output):
   for n in outputs:(r/n).write_text('PREEXISTING-'+n)
   (r/output).unlink();(r/output).mkdir();return {'destination':output,'guard_class':'output-directory'}
  run('output-directory-'+str(index),'builder',opt,directory)
 for case in ['PDF-ancestor-symlink','metadata-disagreement']:
  def more(r,o,case=case):
   if case=='PDF-ancestor-symlink':
    p=r/'output/pdf';shutil.move(str(p),str(o/'same-payload'));p.symlink_to(o/'same-payload',target_is_directory=True)
   else:
    p=r/'zenodo-metadata.json';m=json.loads(p.read_text());m['title']='MISMATCH';p.write_text(json.dumps(m))
  run(case,'builder',opt,more)
(P/'PATH_CONTROLS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(rows),'guard_failures_distinct_from_18_mathematical_wrong_results':True,'controls':rows},indent=2)+'\n')
print(json.dumps({'count':len(rows),'unexpected':[r for r in rows if (r['exit']==0 and r.get('guard_class')!='hardlink-atomic-replacement') or not r['outside_sentinel_preserved'] or (r['exit']!=0 and not r['outputs_unchanged'])]},indent=2))

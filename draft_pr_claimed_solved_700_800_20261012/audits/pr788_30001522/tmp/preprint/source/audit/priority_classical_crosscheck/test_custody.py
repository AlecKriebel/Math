"""Temporary owned-copy postseal crosscheck controls; original seals stay read-only."""
from pathlib import Path
import argparse,ast,hashlib,json,os,shutil,subprocess,sys,tempfile,time
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,b):
 q=p.with_name(p.name+'.own-temp');q.write_bytes(b);os.replace(q,p)
def dump(p,d):put(p,(json.dumps(d,indent=2,sort_keys=True)+'\n').encode())
def edit(p,f):
 d=json.loads(p.read_text());f(d);dump(p,d)
def seal(w):
 rows={p.name:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}for p in sorted(w.iterdir())if p.name!='MANIFEST.json'}
 dump(w/'MANIFEST.json',{'schema':'pr788-priority-classical-crosscheck/v1','head':'3412d5a074c3f3a03f75735a9ccf1755e172204a','exceptions':{'MANIFEST.json':'Only self-hash exception; caller-held external SHA256 required.'},'files':rows})
 return sha((w/'MANIFEST.json').read_bytes())
def main(a):
 w=Path(a.packet).absolute();t=Path(a.case_root).absolute();s=Path(a.scratch).absolute()
 initial={p.name:sha(p.read_bytes())for p in w.iterdir()}
 cp=initial['custody_check.py'];mp=initial['MANIFEST.json']
 names=set(json.loads((w/'INPUT_BINDINGS.json').read_text())['files'])
 for p in (t/'priority_classical').iterdir():names.add(p.relative_to(t).as_posix())
 oldexternal=json.loads((t/'priority_classical/SOURCE_LEDGER.json').read_text())['external_scratch_files']
 names.update('priority_classical_scratch/'+n for n in oldexternal)
 protected={n:sha((t/n).read_bytes())for n in names}
 controls=['positive','wrong_manifest_pin','wrong_checker_pin','valid_checker_comment','changed_report','extra_empty_directory','report_fifo',
 'peer_report_changed','cwy_pdf_changed','cwy_pdf_fifo','original_blob_changed','nonabelian_flag_rebound','effective_only_rebound',
 'firstness_rebound','source_pin_rebound','duplicate_json_rebound']
 results=[]
 with tempfile.TemporaryDirectory(prefix='crosscheck-owned-',dir=s)as td:
  base=Path(td)
  for opt in [False,True]:
   for control in controls:
    case=base/'case';case.mkdir();cw=case/'packet';ct=case/'root';ct.mkdir();shutil.copytree(w,cw)
    for n in names:
     p=ct/n;p.parent.mkdir(parents=True,exist_ok=True);os.link(t/n,p)
    m=mp;c=cp
    if control=='wrong_manifest_pin':m='0'*64
    elif control=='wrong_checker_pin':c='0'*64
    elif control=='valid_checker_comment':
     put(cw/'custody_check.py',(cw/'custody_check.py').read_bytes()+b'\n# changed owned checker\n');ast.parse((cw/'custody_check.py').read_text())
    elif control=='changed_report':put(cw/'REPORT.md',(cw/'REPORT.md').read_bytes()+b'\nchanged\n')
    elif control=='extra_empty_directory':(cw/'empty').mkdir()
    elif control=='report_fifo':(cw/'REPORT.md').unlink();os.mkfifo(cw/'REPORT.md')
    elif control=='peer_report_changed':
     p=ct/'priority_question/REPORT.md';put(p,p.read_bytes()+b'\nchanged\n')
    elif control=='cwy_pdf_changed':
     p=ct/'priority_question_scratch/cwy2013v3.pdf';put(p,p.read_bytes()+b'\nchanged\n')
    elif control=='cwy_pdf_fifo':
     p=ct/'priority_question_scratch/cwy2013v3.pdf';p.unlink();os.mkfifo(p)
    elif control=='original_blob_changed':
     n=next(n for n in names if n.endswith('/author/PROOF.md'));p=ct/n;put(p,p.read_bytes()+b'\nchanged\n')
    elif control=='nonabelian_flag_rebound':
     edit(cw/'VERDICT.json',lambda d:d.__setitem__('nonabelian_pi1_exclusion_verified',False));m=seal(cw)
    elif control=='effective_only_rebound':
     edit(cw/'VERDICT.json',lambda d:d.__setitem__('effective_only_dismissal_valid',True));m=seal(cw)
    elif control=='firstness_rebound':
     edit(cw/'VERDICT.json',lambda d:d.__setitem__('firstness_certified',True));m=seal(cw)
    elif control=='source_pin_rebound':
     edit(cw/'SOURCE_LEDGER.json',lambda d:d['sources'][0].__setitem__('sha256','0'*64));m=seal(cw)
    elif control=='duplicate_json_rebound':
     p=cw/'VERDICT.json';put(p,p.read_bytes().replace(b'{',b'{"status":"duplicate",',1));m=seal(cw)
    args=[sys.executable,'-B']+(['-O']if opt else[])+[str(cw/'custody_check.py'),'--packet',str(cw),'--case-root',str(ct),'--expected-manifest-sha',m,'--expected-checker-sha',c]
    start=time.monotonic();r=subprocess.run(args,capture_output=True,timeout=5);diag=r.stderr.decode().strip()
    positive=control=='positive'
    if positive:
     if r.returncode or json.loads(r.stdout)['status']!='PASS':raise ValueError('Positive failed: '+diag)
    elif r.returncode==0 or not diag.startswith('CUSTODY_FAIL:'):raise ValueError('Bad control '+control+': '+diag)
    if control=='valid_checker_comment'and'External checker pin'not in diag:raise ValueError('Checker pin not exercised')
    results.append({'control':control,'optimized':opt,'exitcode':r.returncode,'diagnostic':diag,'elapsed_seconds':round(time.monotonic()-start,4),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)})
    shutil.rmtree(case)
 for n,h in initial.items():
  if sha((w/n).read_bytes())!=h:raise ValueError('Packet changed')
 for n,h in protected.items():
  if sha((t/n).read_bytes())!=h:raise ValueError('Original input/source changed')
 print(json.dumps({'status':'PASS','positive_cases':2,'negative_cases':2*(len(controls)-1),'distinct_negative_controls':len(controls)-1,
 'testing_manifest_sha256':mp,'checker_sha256':cp,'original_packet_inputs_sources_unchanged':True,'timeout_seconds':5,
 'scope':'Temporary owned paths only; read-only hardlink baselines mutated only by atomic replacement/unlink, never writes to original inodes.','results':results},indent=2,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['packet','case-root','scratch']:p.add_argument('--'+n,required=True)
 main(p.parse_args())

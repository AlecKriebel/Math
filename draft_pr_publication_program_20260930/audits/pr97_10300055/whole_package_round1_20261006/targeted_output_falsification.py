from pathlib import Path
import shutil,json,hashlib,datetime,os
from record_run import run
r=Path(__file__).resolve().parent;p=r.parent/'contingent_credited_note_v1';base=r/'targeted_output_falsification';base.mkdir(exist_ok=True);results=[]
sha=lambda data:hashlib.sha256(data).hexdigest()
good='import json\ndef ck(name,value):\n if not value:raise AssertionError(name)\nprint(json.dumps({"status":"PASS","assertions":0}))\n'
for script,leaf in [('run_diagnostics.py','author_normal.stdout.json'),('test_integrity.py','PROCESS_RECEIPTS.json'),('test_runner_custody.py','PROCESS_RECEIPTS.json')]:
 for linktype in ['symlink','hardlink']:
  for opt in [False,True]:
   label=script.removesuffix('.py')+'_'+linktype+('_O' if opt else '_normal');case=base/label;root=case/'package';out=case/'results'
   if script=='run_diagnostics.py':
    s=root/'support';(s/'review').mkdir(parents=True);shutil.copyfile(p/'publicfiles/support'/script,s/script);(s/'CANDIDATE.md').write_text('Synthetic candidate for output-boundary control.\n');(s/'verify.py').write_text(good);(s/'review/independent_checks.py').write_text(good);victim=root/'README.md';victim.write_text('MUST REMAIN UNCHANGED\n')
   else:
    shutil.copytree(p/'publicfiles',root);victim=root/'LICENSE.txt'
   out.mkdir();before=victim.read_bytes();link=out/leaf
   if linktype=='symlink':link.symlink_to(victim.resolve())
   else:os.link(victim,link)
   argv=['/usr/bin/python3','-E','-B']+(['-O'] if opt else [])+[str(root/'support'/script)]
   if script!='run_diagnostics.py':argv+=['--archive',str((p/'pr97_support.zip').resolve())]
   argv+=['--output-dir',str(out.resolve())]
   code,stdout,stderr=run(label,argv,expected=0 if script=='run_diagnostics.py' else 1)
   after=victim.read_bytes();results.append({'label':label,'script':script,'link_type':linktype,'optimized':opt,'root':str(root.resolve()),'output':str(out.resolve()),'victim':str(victim.resolve()),'leaf':leaf,'initial_bytes':before.decode(),'final_bytes':after.decode(),'initial_sha256':sha(before),'final_sha256':sha(after),'package_bytes_changed':before!=after,'wrapper_exit_code':code,'wrapper_stdout':stdout.decode(),'wrapper_stderr':stderr.decode(),'wrapper_sha256':sha((root/'support'/script).read_bytes()),'synthetic_control_only':True})
(base/'RESULT.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'finding':'Existing output leaf links bypass closed-package guards','cases':results},indent=2)+'\n')
print(json.dumps({'cases':len(results),'package_changes':sum(x['package_bytes_changed'] for x in results),'exit_codes':{x['label']:x['wrapper_exit_code'] for x in results}},indent=2))

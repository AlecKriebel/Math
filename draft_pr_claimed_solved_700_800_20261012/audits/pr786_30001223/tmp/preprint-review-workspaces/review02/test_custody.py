"""Copied review02 custody controls; all writes remain in owned scratch."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile, time
def need(x,m):
    if not x: raise ValueError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def main(a):
    packet,inputs,scratch=Path(a.packet).resolve(),Path(a.input_root).resolve(),Path(a.scratch).resolve()
    controls=['wrong_manifest_pin','wrong_checker_pin','changed_report','missing_report','extra_file',
       'extra_directory','listed_symlink','listed_fifo','manifest_fifo','changed_checker',
       'input_paper_bytes','input_zip_bytes','input_pdf_fifo','input_inventory_bytes','input_extra',
       'input_symlink','initial_position_rebound','exception_widen_rebound','duplicate_json_rebound',
       'nonfinite_json_rebound','boolean_size_rebound','unsafe_filename_rebound','verdict_firstness_rebound',
       'source_member_ledger_rebound','original_blob_ledger_rebound','source_pin_rebound',
       'builder_receipt_rebound','replay_receipt_rebound','required_removed_rebound']
    mp=sha((packet/'MANIFEST.json').read_bytes());cp=sha((packet/'custody_check.py').read_bytes());results=[]
    with tempfile.TemporaryDirectory(prefix='custody02-',dir=scratch)as work:
      work=Path(work)
      for opt in (False,True):
        opts=['-B']+(['-O'] if opt else [])
        for control in ['positive']+controls:
          case=work/'case';pk=case/'packet';shutil.copytree(packet,pk)
          ir=inputs
          if control.startswith('input_'):
              ir=case/'inputs';shutil.copytree(inputs,ir)
          m,c=mp,cp
          def rebind():
              nonlocal m
              v=json.loads((pk/'MANIFEST.json').read_text())
              for n in list(v['files']):
                  f=pk/n
                  if f.is_file() and not f.is_symlink():
                      raw=f.read_bytes();v['files'][n]={'bytes':len(raw),'sha256':sha(raw)}
              dump(pk/'MANIFEST.json',v);m=sha((pk/'MANIFEST.json').read_bytes())
          def mutate(path):path.write_bytes(path.read_bytes()+b'\nTAMPERED OWN COPY\n')
          if control=='wrong_manifest_pin':m='0'*64
          elif control=='wrong_checker_pin':c='0'*64
          elif control=='changed_report':mutate(pk/'REPORT.md')
          elif control=='missing_report':(pk/'REPORT.md').unlink()
          elif control=='extra_file':(pk/'EXTRA').write_text('extra')
          elif control=='extra_directory':(pk/'EMPTY').mkdir()
          elif control=='listed_symlink':
              target=case/'target';shutil.copyfile(pk/'REPORT.md',target);(pk/'REPORT.md').unlink();(pk/'REPORT.md').symlink_to(target)
          elif control=='listed_fifo':(pk/'REPORT.md').unlink();os.mkfifo(pk/'REPORT.md')
          elif control=='manifest_fifo':(pk/'MANIFEST.json').unlink();os.mkfifo(pk/'MANIFEST.json')
          elif control=='changed_checker':
              f=pk/'custody_check.py';f.write_bytes(f.read_bytes()+b'\n# changed checker copy\n')
          elif control=='input_paper_bytes':mutate(ir/'paper.tex')
          elif control=='input_zip_bytes':mutate(ir/'source-and-verification.zip')
          elif control=='input_pdf_fifo':(ir/'output/pdf/paper.pdf').unlink();os.mkfifo(ir/'output/pdf/paper.pdf')
          elif control=='input_inventory_bytes':mutate(ir/'REVIEW_INPUTS.json')
          elif control=='input_extra':(ir/'EXTRA').write_text('unbound')
          elif control=='input_symlink':
              target=case/'inputtarget';shutil.copyfile(ir/'paper.tex',target);(ir/'paper.tex').unlink();(ir/'paper.tex').symlink_to(target)
          elif control=='initial_position_rebound':mutate(pk/'INITIAL_WHOLE_POSITION.json');rebind()
          elif control=='exception_widen_rebound':
              v=json.loads((pk/'MANIFEST.json').read_text());v['exceptions']['REPORT.md']='omit';dump(pk/'MANIFEST.json',v);m=sha((pk/'MANIFEST.json').read_bytes())
          elif control in ('duplicate_json_rebound','nonfinite_json_rebound'):
              f=pk/'MANIFEST.json';raw=f.read_text();f.write_text(raw[:-2]+(',"head":"x"}\n' if control=='duplicate_json_rebound' else ',"invalid":NaN}\n'));m=sha(f.read_bytes())
          elif control=='boolean_size_rebound':
              v=json.loads((pk/'MANIFEST.json').read_text());v['files']['REPORT.md']['bytes']=True;dump(pk/'MANIFEST.json',v);m=sha((pk/'MANIFEST.json').read_bytes())
          elif control=='unsafe_filename_rebound':
              v=json.loads((pk/'MANIFEST.json').read_text());v['files']['../escape']={'bytes':0,'sha256':sha(b'')};dump(pk/'MANIFEST.json',v);m=sha((pk/'MANIFEST.json').read_bytes())
          elif control=='verdict_firstness_rebound':
              f=pk/'VERDICT.json';v=json.loads(f.read_text());v['firstness_certified']=True;dump(f,v);rebind()
          elif control=='source_member_ledger_rebound':
              f=pk/'SOURCE_CUSTODY.json';v=json.loads(f.read_text());v['source_members']['paper.tex']['sha256']='0'*64;dump(f,v);rebind()
          elif control=='original_blob_ledger_rebound':
              f=pk/'SOURCE_CUSTODY.json';v=json.loads(f.read_text());v['original_files'][0]['git_blob']='0'*40;dump(f,v);rebind()
          elif control=='source_pin_rebound':
              f=pk/'SOURCE_AND_VISUAL_RECEIPTS.json';v=json.loads(f.read_text());v['sources'][0]['sha256']='0'*64;dump(f,v);rebind()
          elif control=='builder_receipt_rebound':
              f=pk/'BUILD_312_NORMAL.json';v=json.loads(f.read_text());v['outputs'][0]['sha256']='0'*64;dump(f,v);rebind()
          elif control=='replay_receipt_rebound':
              f=pk/'REPLAY_312_NORMAL.json';v=json.loads(f.read_text());v['stdout']['replay_runs'].pop();dump(f,v);rebind()
          elif control=='required_removed_rebound':
              (pk/'REPORT.md').unlink();v=json.loads((pk/'MANIFEST.json').read_text());del v['files']['REPORT.md'];dump(pk/'MANIFEST.json',v);m=sha((pk/'MANIFEST.json').read_bytes())
          elif control!='positive':raise ValueError('Unknowncontrol')
          started=time.monotonic()
          r=subprocess.run([sys.executable]+opts+[str(pk/'custody_check.py'),'--packet',str(pk),'--input-root',str(ir),
              '--expected-manifest-sha',m,'--expected-checker-sha',c],capture_output=True,text=True,timeout=5)
          elapsed=time.monotonic()-started
          if control=='positive':need(r.returncode==0 and json.loads(r.stdout)['status']=='PASS','Positivefailed: '+r.stderr)
          else:need(r.returncode!=0 and 'CUSTODY_FAIL:'in r.stderr,'Negativeaccepted/notexplicit: '+control+' '+r.stderr)
          results.append({'control':control,'optimized':opt,'exitcode':r.returncode,'elapsed_seconds':round(elapsed,4),
            'expected':'PASS' if control=='positive'else'REJECT','stdout_sha256':sha(r.stdout.encode()),'stderr_sha256':sha(r.stderr.encode()),
            'diagnostic':r.stderr.strip()[-300:]})
          shutil.rmtree(case)
    return {'status':'PASS','testing_manifest_sha256':mp,'testing_checker_sha256':cp,'positive_cases':2,
       'distinct_negative_controls':len(controls),'negative_cases':2*len(controls),'all_mutations_on_owned_copies':True,
       'nonregular_timeout_seconds':5,'results':results,'scope':'Receipt added after testing manifest; final manifest pin is separately issued. Rebound controls deliberately supply new test pins to exercise internal consistency.'}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ['packet','input-root','scratch']:p.add_argument('--'+n,required=True)
    print(json.dumps(main(p.parse_args()),indent=2,sort_keys=True))

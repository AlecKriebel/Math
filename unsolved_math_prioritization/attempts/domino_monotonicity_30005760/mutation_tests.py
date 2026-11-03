from pathlib import Path
import tempfile,shutil,subprocess,json,os,sys
ROOT=Path(__file__).resolve().parent
rows=[]
def check(name,edit,semantic=False,script='domino_1890_analysis/verify.py'):
 for opt in (False,True):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'pkg';shutil.copytree(ROOT,p);edit(p)
   env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
   cmd=[sys.executable]+(['-O'] if opt else [])+[str(p/(script if semantic else 'verify_package.py'))]
   proc=subprocess.run(cmd,cwd=p,env=env,capture_output=True)
   if proc.returncode==0:raise RuntimeError('mutation survived: '+name)
   expected={'unlisted_file':'file inventory mismatch','unlisted_directory':'directory inventory mismatch','missing_file':'file inventory mismatch','symlink':'symlink rejected','FIFO':'special entry rejected'}
   if name in expected and expected[name] not in proc.stderr.decode():raise RuntimeError('wrong rejection stage: '+name)
   rows.append({'name':name,'optimized':opt,'kind':'semantic oracle with deliberately bypassed integrity' if semantic else 'inventory/integrity gate','exit_code':proc.returncode,'rejection':proc.stderr.decode().splitlines()[-1]})
def change(p,f,old,new):
 path=p/f;text=path.read_text()
 if old not in text:raise RuntimeError(old)
 path.write_text(text.replace(old,new,1))
check('unlisted_file',lambda p:(p/'unexpected.txt').write_text('untrusted'))
check('unlisted_directory',lambda p:(p/'unexpected').mkdir())
check('missing_file',lambda p:(p/'README.md').unlink())
check('symlink',lambda p:(p/'untrusted-link').symlink_to('/nonexistent/private-source'))
check('FIFO',lambda p:os.mkfifo(p/'unexpected_fifo'))
check('content_tamper',lambda p:(p/'README.md').write_text('SOLVED'))
check('whole_module_top_level_injection',lambda p:(p/'domino_1890_analysis/transfer.py').write_text((p/'domino_1890_analysis/transfer.py').read_text()+'\nraise RuntimeError("injected")\n'))
def cert(p):
 f=p/'domino_1890_analysis/basis_certificate.json';x=json.loads(f.read_text());x.pop();f.write_text(json.dumps(x))
check('remove_basis_certificate_witness',cert,True,'domino_1890_audit/independent_check.py')
def count(p):
 f=p/'domino_1890_analysis/counts_extended.json';x=json.loads(f.read_text());x[3]['counts'][1]+=1;f.write_text(json.dumps(x))
check('alter_inversion_coefficient',count,True)
check('replace_231_cell_with_213',lambda p:change(p,'domino_1890_analysis/verify.py','avoid(p[c:],(2,3,1))','avoid(p[c:],(2,1,3))'),True)
check('corrupt_singleton_insertion_rank',lambda p:change(p,'domino_1890_analysis/verify.py','p[:i]+(i+1,)','p[:i]+(i+2,)'),True)
check('corrupt_inversion_statistic',lambda p:change(p,'domino_1890_analysis/verify.py','sum(p[i]>p[j]','sum(p[i]<p[j]'),True)
check('corrupt_exact_basis_member',lambda p:change(p,'domino_1890_analysis/verify.py','(4,6,5,2,3,1)','(4,6,5,3,2,1)'),True)
# Probe that malformed inventory fails before any payload read_bytes call.
for opt in (False,True):
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/'pkg';shutil.copytree(ROOT,p);(p/'unexpected').write_text('probe')
  probe="import runpy,pathlib; g=runpy.run_path("+repr(str(p/'verify_package.py'))+"); pathlib.Path.read_bytes=lambda self: (_ for _ in ()).throw(RuntimeError('PAYLOAD_READ_TOO_EARLY')); g['verify']()"
  proc=subprocess.run([sys.executable]+(['-O'] if opt else [])+['-c',probe],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  if b'file inventory mismatch' not in proc.stderr or b'PAYLOAD_READ_TOO_EARLY' in proc.stderr:raise RuntimeError('inventory-first probe failed')
  rows.append({'name':'inventory_before_payload_read_probe','optimized':opt,'exit_code':proc.returncode,'rejection':'file inventory mismatch before payload read'})
import ast
hook=next(ast.literal_eval(n.value) for n in ast.parse((ROOT/'replay.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='HOOK' for t in n.targets))
for opt in (False,True):
 proc=subprocess.run([sys.executable]+(['-O'] if opt else [])+['-c',hook+'\nimport socket;socket.socket()'],capture_output=True)
 if proc.returncode==0 or b'network prohibited' not in proc.stderr:raise RuntimeError('socket hook failed')
 rows.append({'name':'socket_creation_rejected','optimized':opt,'exit_code':proc.returncode,'rejection':'network prohibited'})
Path(sys.argv[1]).write_text(json.dumps({'status':'PASS','normal_and_optimized':True,'tests':rows},indent=2)+'\n')
print('PASS',len(rows))

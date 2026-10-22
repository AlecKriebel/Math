#!/usr/bin/env python3
import ast,datetime,hashlib,importlib.util,json,os,shutil,subprocess,sys,time,zipfile,zlib
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
DELIVERY=BASE/'preprint_v1_0'
SCRATCH=HERE/'scratch'
SCRATCH.mkdir(exist_ok=False)
RECEIPTS=HERE/'ACTUAL_COMMAND_RECEIPTS.jsonl'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def record(cmd,cwd,expected=0):
 t=time.monotonic(); start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=subprocess.run([str(x) for x in cmd],cwd=cwd,capture_output=True,text=True,timeout=180)
  row={'utc':start,'argv':[str(x) for x in cmd],'cwd':str(cwd),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'elapsed_seconds':time.monotonic()-t,'expected':expected,'free_bytes_before_or_after':shutil.disk_usage(HERE).free}
 except Exception as exc:
  row={'utc':start,'argv':[str(x) for x in cmd],'cwd':str(cwd),'exception':repr(exc),'expected':expected}
 with RECEIPTS.open('a') as f:f.write(json.dumps(row)+'\n')
 ok=(row.get('returncode')==0) if expected==0 else row.get('returncode',0)!=0
 if not ok: raise RuntimeError('Unexpected command outcome: '+json.dumps(row))
 return row
record(['unzip','-q',DELIVERY/'verification_kit.zip','-d',SCRATCH/'clean_check'],HERE)
KIT=SCRATCH/'clean_check/verification_kit'
allow=json.loads((KIT/'ALLOWLIST.json').read_text())['members']
with zipfile.ZipFile(DELIVERY/'verification_kit.zip') as z:
 infos=z.infolist(); expected=['verification_kit/'+n for n in allow]
 if [x.filename for x in infos]!=expected:raise RuntimeError('ZIP closed order')
 rows=[]
 for i in infos:
  raw=z.read(i)
  if raw!=(KIT/i.filename.removeprefix('verification_kit/')).read_bytes():raise RuntimeError('ZIP data')
  if i.date_time!=(2026,10,14,0,0,0) or i.compress_type!=0 or i.create_system!=3 or i.external_attr!=0o100644<<16 or i.extra or i.comment or i.flag_bits:raise RuntimeError('ZIP header')
  if zlib.crc32(raw)!=i.CRC:raise RuntimeError('ZIP CRC')
  rows.append({'path':i.filename,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'crc32':i.CRC})
 if z.comment:raise RuntimeError('ZIP comment')
 (HERE/'INDEPENDENT_ZIP_MEMBER_PINS.json').write_text(json.dumps({'members':rows,'closed':True,'count':len(rows),'archive_sha256':sha(DELIVERY/'verification_kit.zip')},indent=2)+'\n')
for opt in [False,True]:
 prefix=[sys.executable,'-I','-B']+(['-O'] if opt else [])
 for script in ['verify.py','run_checks.py','fault_checks.py','output_guard_checks.py']:
  record(prefix+[KIT/script],KIT)
 out=SCRATCH/('rebuilt-O.zip' if opt else 'rebuilt.zip')
 record(prefix+[KIT/'build_archive.py','--output',out],KIT)
 record(['cmp',DELIVERY/'verification_kit.zip',out],KIT)
 record(prefix+[KIT/'verify.py','--require-binding','--binding',DELIVERY/'EXTERNAL_BINDING.json','--pdf',DELIVERY/'preprint.pdf','--archive',DELIVERY/'verification_kit.zip'],KIT)
 out.unlink()
 # Owned harness exposes exact inner stderr for the original unexplained failure.
 for repeat in range(3):
  for fault in ['word_conjugation','parity','erasing']:
   r=record(prefix+[KIT/'run_checks.py','--fault',fault],KIT,expected='nonzero')
   if 'portable reviewer guard' not in r['stderr']:raise RuntimeError('Fault failed for unrelated reason')
record([sys.executable,'-I','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',DELIVERY/'deposit_metadata.json'],HERE)
(SCRATCH/'compiled').mkdir()
record(['tectonic','--outdir',SCRATCH/'compiled',KIT/'preprint.tex'],KIT)
record(['pdfinfo',DELIVERY/'preprint.pdf'],HERE)
# Render actual delivered PDF; these fresh seven PNGs will be individually viewed.
record(['pdftoppm','-r','95','-png',DELIVERY/'preprint.pdf',SCRATCH/'page'],HERE)
# Full adapted mathematical result comparison, retaining all historical math fields.
spec=importlib.util.spec_from_file_location('own_adapter_read',KIT/'run_checks.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
math=[]
for kind,(relative,hash_expected) in mod.PROGRAMS.items():
 source=KIT/relative
 if sha(source)!=hash_expected:raise RuntimeError('source pin')
 work=SCRATCH/('full-'+kind);work.mkdir();copied=work/source.name;shutil.copyfile(source,copied)
 if kind=='surface':
  d=work/'inputs/git';d.mkdir(parents=True)
  for p in (KIT/'originals/submitted').iterdir():shutil.copyfile(p,d/p.name)
 ns={'__name__':'independent_full_output_capture','__file__':str(copied)}
 exec(compile(mod.adapt(kind,source.read_text(),None),str(copied),'exec'),ns)
 if kind in ['word','priority']:local=ns['main']()
 if kind=='priority':
  original_tree=ast.parse(source.read_text());main=next(n for n in original_tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
  expr=next(n.value for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='result' for t in n.targets))
  actual=eval(compile(ast.Expression(expr),str(copied),'eval'),ns,dict(local,verified=[]))
  expected=json.loads((source.parent/'CONTROL_RESULTS.json').read_text()); exclusions=['frozen_inputs_reverified']
 else:
  name='WORD_CONTROL_RESULTS.json' if kind=='word' else 'SANITY_RESULTS.json'
  actual=json.loads((work/name).read_text());expected=json.loads((source.parent/name).read_text());exclusions=['timestamp'] if kind=='surface' else []
 for key in exclusions:actual.pop(key,None);expected.pop(key,None)
 if actual!=expected:raise RuntimeError('Full math output mismatch '+kind)
 math.append({'kind':kind,'source_sha256':hash_expected,'disclosed_excluded_fields':exclusions,'full_mathematical_output':actual,'matches_preserved':True})
(HERE/'FULL_MATHEMATICAL_OUTPUT_COMPARISON.json').write_text(json.dumps(math,indent=2)+'\n')
print(json.dumps({'status':'PASS','actual_commands':sum(1 for _ in RECEIPTS.open()),'scratch':str(SCRATCH),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))

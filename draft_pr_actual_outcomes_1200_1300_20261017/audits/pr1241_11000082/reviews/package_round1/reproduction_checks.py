import pathlib,hashlib,os,json,subprocess,shutil,importlib.util,contextlib,io,datetime
h=pathlib.Path(__file__).resolve().parent;p=h/'_local/copy/publication'
def sha(x):return hashlib.sha256(x.read_bytes()).hexdigest()
# Only this harmless ignore-classification query is simulated; no Git runs.
bin=h/'_local/bin';bin.mkdir(exist_ok=True)
g=bin/'git';g.write_text('#!/usr/bin/env python3\nimport sys\nif sys.argv[1:]==["check-ignore","--no-index","-z","--stdin"]:\n sys.stdout.buffer.write(sys.stdin.buffer.read());sys.exit(0)\nraise SystemExit("Forbidden Git invocation")\n');g.chmod(0o700)
env={**os.environ,'PATH':str(bin)+os.pathsep+os.environ['PATH'],'PYTHONDONTWRITEBYTECODE':'1'}
before={n:sha(p/n) for n in ['Johnson_Filtration_Multiplicity_Note_v1.0.pdf','Johnson_Filtration_Multiplicity_Verification_v1.0.zip']}
r=subprocess.run(['python3','-B',str(p/'build_package.py')],cwd=h,env=env,capture_output=True,text=True,timeout=180)
(h/'BUILD_REPRODUCTION_STDOUT.txt').write_text(r.stdout);(h/'BUILD_REPRODUCTION_STDERR.txt').write_text(r.stderr)
summary={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'build_returncode':r.returncode,'original_release':before,'rebuilt_release':{n:sha(p/n) for n in before},'build_exact':all(sha(p/n)==s for n,s in before.items()),'build_limit':'git check-ignore query alone replaced by offline classification that all files under this ignored scratch copy are ignored; registered freeze files explicitly restored by production preparer. No Git operation ran.'}
cache=h/'_local/texcache';shutil.copytree('/Users/alec/Library/Caches/Tectonic',cache,dirs_exist_ok=True)
s=importlib.util.spec_from_file_location('compile_copy',p/'compile_note.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.PROGRAM=h/'_local/compile_program'
real_run=subprocess.run
class Process:
 def check_output(self,*a,**kw):return subprocess.check_output(*a,**kw)
 def run(self,args,**kw):
  if '--keep-logs' in args:args=[args[0],'--only-cached',*args[1:]];kw['env']['TECTONIC_CACHE_DIR']=str(cache)
  return real_run(args,**kw)
m.subprocess=Process()
try:
 with contextlib.redirect_stdout(io.StringIO()) as out:m.main()
 summary['compile_returncode']=0;summary['compile_receipt']=json.loads(out.getvalue());summary['compiled_pdf_exact']=sha(p/'output/pdf/main.pdf')==before['Johnson_Filtration_Multiplicity_Note_v1.0.pdf']
except Exception as e:summary['compile_error']=repr(e)
summary['compile_scope']='Original saved TeX and production compile helper on copy, with only-cached appended and TECTONIC_CACHE_DIR redirected to private copied system cache. SOURCE_DATE_EPOCH unchanged at1792267200; no network or original cache mutation.'
(h/'REPRODUCTION_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

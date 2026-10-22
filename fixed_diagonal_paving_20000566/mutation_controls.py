import sys,subprocess,tempfile,pathlib,json,shutil,hashlib,concurrent.futures,importlib.util
P=pathlib.Path(__file__).parent
mutations=[
 ('profile_identity','checks.py','I * c','2 * I * c'),
 ('witness_projection','check_witness.py','J / 3','J / 2'),
 ('symbolic_profile','exact_checks.py','-s.I * z','-2 * s.I * z'),
 ('strict_witness','strict_checks.py','J / 3','J / 2'),
 ('fractional_coupling','theorem_checks.py','s.sqrt(t*(1-t))','s.sqrt(t*(1-t))/2'),
 ('fractional_rank','theorem_checks.py','s.ceiling(a)==2','s.ceiling(a)==1'),
 ('complement_rank','theorem_checks.py',"Q[2:,2:].rank()==1","Q[2:,2:].rank()==2"),
 ('integer_rank','theorem_checks.py','(s.diag(1,0,1,0),2,1)','(s.diag(1,0,1,0),2,2)'),
 ('necessity_strict_boundary','theorem_checks.py',' < (r-1)*k+1',' <= (r-1)*k+1'),
 ('matroid_obstruction','theorem_checks.py','3>2*Q[:3,:3].rank()','3<2*Q[:3,:3].rank()'),
 ('necessity_witness_rank','theorem_checks.py',"Q[:3,:3].rank()==1","Q[:3,:3].rank()==2"),
]
def mutate(item):
 label,name,old,new=item; text=(P/name).read_text()
 if old not in text:raise RuntimeError('mutation target missing '+label)
 results=[]
 for optimized in [False,True]:
  with tempfile.TemporaryDirectory() as td:
   f=pathlib.Path(td)/name; f.write_text(text.replace(old,new,1))
   proc=subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(f)],capture_output=True,timeout=120)
   if proc.returncode==0 or b'RuntimeError' not in proc.stderr:raise RuntimeError('mutation not guard-detected '+label+str(proc.stderr))
   # Preserve complete output; replace only temporary filesystem prefix in traceback.
   results.append({'optimized':optimized,'returncode':proc.returncode,'stdout':proc.stdout.decode(),'stderr':proc.stderr.decode().replace(td,'<temporary-directory>')})
 return {'control':label,'script':name,'old':old,'new':new,'detected':True,'runs':results}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:out=list(e.map(mutate,mutations))
print(json.dumps(out,indent=2))

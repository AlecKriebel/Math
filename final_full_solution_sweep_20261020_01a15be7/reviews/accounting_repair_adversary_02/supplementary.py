from pathlib import Path
import datetime as dt,hashlib,json,os,shutil,subprocess,sys
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
R=Path(__file__).resolve().parent
F=R/'fixtures/supplementary_full_recursive_mount'
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
cases=[]
for pr,problem in [(397,'9700002'),(399,'30001179'),(280,'30000156')]:
 path=f'audits/pr{pr:04d}_{problem}/ZENODO_PUBLIC_FILE_VERIFICATION.json'
 cases.extend([(f'nested_record_http_404_{pr}',path,lambda d:d.update(record_http_status=404)),(f'nested_doi_wrong_destination_{pr}',path,lambda d:d['doi_resolution'].update(resolved_url='https://zenodo.org/records/99999999'))])
for pr,problem in [(292,'30001608'),(397,'9700002'),(399,'30001179'),(280,'30000156')]:
 path=f'audits/pr{pr:04d}_{problem}/LEDGER_PUBLICATION_VERIFICATION.json'
 cases.append((f'nested_ledger_wrong_gid_{pr}',path,lambda d:d.update(sheet_gid=1)))
results=[]
for name,path,fn in cases:
 if F.exists():shutil.rmtree(F)
 shutil.copytree(R/'inputs/current',F)
 d=json.loads((F/path).read_text());fn(d);save(F/path,d)
 c=R/'cases/supplementary'/name;save(c/'MUTATIONS.json',dict(path=path,after=d))
 for mode,flags in [('normal',[]),('optimized',['-O'])]:
  p=subprocess.run([sys.executable,'-B',*flags,str(F/'coverage_snapshot.py')],capture_output=True,cwd=R,env=os.environ)
  (c/(mode+'.stdout')).write_bytes(p.stdout);(c/(mode+'.stderr')).write_bytes(p.stderr)
  results.append(dict(name=name,mode=mode,accepted=p.returncode==0,expected_reject=True,error_tail=p.stderr.decode().splitlines()[-1] if p.stderr else None))
if F.exists():shutil.rmtree(F)
shutil.copytree(R/'inputs/current',F)
save(R/'SUPPLEMENTARY_RESULTS.json',dict(at=dt.datetime.now(dt.timezone.utc).isoformat(),results=results))
print(json.dumps(results,indent=2))

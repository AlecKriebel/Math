from pathlib import Path
import json,zipfile,hashlib,subprocess,sys,datetime
R=Path(__file__).resolve().parent;A=Path(json.loads((R/'INPUT_FREEZE.json').read_text())['root']);W=R/'scratch_local/audit';P=W/'publication';name='Johnson_Filtration_Multiplicity_Verification_v1.0.zip'
with zipfile.ZipFile(A/'publication'/name) as z:published={n.removeprefix('provenance/') for n in z.namelist() if n.startswith('provenance/')}
expanded={'sha256':hashlib.sha256((P/name).read_bytes()).hexdigest(),'bytes':len((P/name).read_bytes())}
extras=[]
for p in W.iterdir():
 if p.is_file() and p.suffix in ('.md','.json') and p.name not in published and p.name!='RESEARCH_LOG.md':extras.append(p.name);p.unlink()
# Post-build coordinator/R2 records are deliberately outside the immutable ZIP.
run=subprocess.run([sys.executable,'-B',str(P/'build_package.py')],capture_output=True,text=True,check=True);(R/'ARCHIVE_SCOPE_BUILD_STDOUT.txt').write_text(run.stdout);(R/'ARCHIVE_SCOPE_BUILD_STDERR.txt').write_text(run.stderr)
checks=[]
for n in (name,'Johnson_Filtration_Multiplicity_Note_v1.0.pdf'):
 a=(A/'publication'/n).read_bytes();b=(P/n).read_bytes();checks.append({'name':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'exact':a==b})
 if a!=b:raise RuntimeError('Frozen-input build differs '+n)
report={'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_frozen_inventory_reproduction':checks,'all_current_root_build':expanded,'post_build_records_outside_immutable_archive':sorted(extras),'scope':'Unmodified actual prepare_package and build_package run on copied inputs. First run with every current root report produced 110 archive members, adding precisely the five post-build R2/coordinator provenance records and changing the outer manifest. Reproduction of the frozen 105-member artifact uses exactly its recorded provenance input inventory. No source/PDF/eight-edition/family file altered or excluded. This distinguishes release reconstruction from preparation of a new enlarged package; any enlarged artifact would require a new review gate. No current input mutation.'}
(R/'BUILD_REPRODUCTION_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','excluded_post_build_provenance_only':sorted(extras),'artifacts_exact':True}))

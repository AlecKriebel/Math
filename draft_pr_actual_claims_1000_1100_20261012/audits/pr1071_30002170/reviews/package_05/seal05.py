from pathlib import Path
import os,stat,json,hashlib,datetime,sys
R=Path(__file__).resolve().parent;A=R.parents[1]
EXCLUDED={'OUTPUT_PINS.json','SEAL.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory():
 files=[];links=[]
 for base,ds,fs in os.walk(R,followlinks=False):
  for n in ds+fs:
   p=Path(base,n);relative=str(p.relative_to(R))
   if relative in EXCLUDED:continue
   s=p.lstat()
   if stat.S_ISREG(s.st_mode):files.append({'path':relative,'bytes':s.st_size,'sha256':sha(p),'mode':stat.S_IMODE(s.st_mode),'nlink':s.st_nlink})
   elif stat.S_ISLNK(s.st_mode):links.append({'path':relative,'kind':'owned adversarial symlink fixture','target':os.readlink(p),'mode':stat.S_IMODE(s.st_mode)})
 return sorted(files,key=lambda r:r['path']),sorted(links,key=lambda r:r['path'])
if sys.argv[1]=='pin':
 records,links=inventory();out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Every settled regular review05 output, including raw command streams, partial failed ZIP, exact checker/compiler output, owned clean extraction and seven viewed PNGs; excludes only this pin file and later separate seal. Symlink fixtures are listed separately without following them.','records':records,'symlink_fixtures':links,'count':len(records),'no_further_review_writes_expected':True}
 (R/'OUTPUT_PINS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'count':len(records),'output_pins_sha256':sha(R/'OUTPUT_PINS.json'),'symlink_fixtures':len(links)}))
elif sys.argv[1]=='seal':
 pins=json.loads((R/'OUTPUT_PINS.json').read_text());current,links=inventory()
 if current!=pins['records']or links!=pins['symlink_fixtures']:raise RuntimeError('Outputs changed after pin')
 freeze=json.loads((R/'INPUT_FREEZE.json').read_text())
 for row in freeze['files']:
  p=A/row['path'];s=p.stat()
  if p.is_symlink()or(s.st_size,sha(p),stat.S_IMODE(s.st_mode))!=(row['size'],row['sha256'],row['mode']):raise RuntimeError('Frozen input changed '+row['path'])
 out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'SEALED_COMPLETE_NEW_WHOLE05_ZERO_ACTIONABLE_PENDING_ROOT_TERMINAL_ADOPTION','output_pins':{'path':'OUTPUT_PINS.json','bytes':(R/'OUTPUT_PINS.json').stat().st_size,'sha256':sha(R/'OUTPUT_PINS.json')},'settled_regular_outputs':len(current),'symlink_fixtures':len(links),'input_regular_files_rechecked':len(freeze['files']),'inputs_size_hash_mode_unchanged':True,'report_sha256':sha(R/'REPORT.md'),'verdict_sha256':sha(R/'VERDICT.json'),'finding_counts':{'P0':0,'P1':0,'P2':0,'P3':0},'whole_reviews_completed':5,'minimum_whole_reviews_required':2,'root_terminal_adoption_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'review_completion_percent':100}
 (R/'SEAL.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'seal_sha256':sha(R/'SEAL.json'),**out},indent=2))
else:raise RuntimeError('Use pin or seal')

import datetime,json,os,pathlib,subprocess,hashlib
ROOT=pathlib.Path(__file__).resolve().parent
TASKS=[('khoule_manso_ndiaye_war2025',32),('khoule_manso_ndiaye_war2025',33),('asai2011_pa',5),('bowden2016',14),('foulon_hasselblatt_vaugon2021',5)]
records=[]
for name,page in TASKS:
 out=ROOT/(name+'_p'+str(page));cmd=['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','110','-png',str(ROOT/(name+'.pdf')),str(out)]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();cp=subprocess.run(cmd,capture_output=True);rec={'operator_pid':os.getpid(),'started_utc':start,'argv':cmd,'returncode':cp.returncode,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':cp.stdout.decode('utf-8','replace'),'stderr':cp.stderr.decode('utf-8','replace')}
 if out.with_suffix('.png').exists(): rec.update(output=out.with_suffix('.png').name,sha256=hashlib.sha256(out.with_suffix('.png').read_bytes()).hexdigest())
 records.append(rec)
(ROOT/'RENDER_PROCESS_RECORDS.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))


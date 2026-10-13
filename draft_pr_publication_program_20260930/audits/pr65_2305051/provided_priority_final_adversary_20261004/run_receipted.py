from pathlib import Path
import subprocess,datetime,json,sys,hashlib
base=Path(__file__).resolve().parent
private=Path("/Users/alec/.cache/codex-pr65-priority-20261004/provided_priority_final_adversary_20261004")
private.mkdir(parents=True,exist_ok=True)
label=sys.argv[1]
argv=sys.argv[2:]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen(argv,cwd="/Users/alec/Documents/Math",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
pid=p.pid
out,err=p.communicate()
end=datetime.datetime.now(datetime.timezone.utc).isoformat()
streams={}
for name,data in (("stdout",out),("stderr",err)):
    path=private/(label+"."+name)
    path.write_bytes(data)
    streams[name]={"private_path":str(path),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
r={"pid":pid,"argv":argv,"cwd":"/Users/alec/Documents/Math","start_utc":start,"end_utc":end,"exit_code":p.returncode,**streams}
(base/"receipts").mkdir(exist_ok=True)
(base/"receipts"/(label+".json")).write_text(json.dumps(r,indent=2)+"\n")
sys.stdout.buffer.write(out)
sys.stderr.buffer.write(err)
sys.exit(p.returncode)

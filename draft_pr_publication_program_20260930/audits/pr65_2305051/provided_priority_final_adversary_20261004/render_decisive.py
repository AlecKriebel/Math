from pathlib import Path
import subprocess,datetime,json,hashlib
base=Path(__file__).resolve().parent
root=Path("/Users/alec/.cache/codex-pr65-priority-20261004")
out=root/"provided_priority_final_adversary_20261004"/"renders"
out.mkdir(parents=True,exist_ok=True)
sets=[("hayman2019",root/"provided_primary_sources_20261004"/"hayman2019.pdf",[127,128]),("aan1999",root/"aan1999.pdf",[3,9,10,11,12]),("piranian1966",root/"provided_primary_sources_20261004"/"piranian1966.pdf",[1,6,7]),("duren1966",root/"provided_primary_sources_20261004"/"duren1966.pdf",[2,3,4])]
for label,pdf,pages in sets:
    for page in pages:
        prefix=out/(label+"_pdf"+str(page))
        argv=["/opt/homebrew/bin/pdftoppm","-f",str(page),"-l",str(page),"-r","115","-png","-singlefile",str(pdf),str(prefix)]
        start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=str(root))
        pid=child.pid
        stdout,stderr=child.communicate()
        end=datetime.datetime.now(datetime.timezone.utc).isoformat()
        streams={}
        for name,data in (("stdout",stdout),("stderr",stderr)):
            path=out/(label+"_pdf"+str(page)+"."+name)
            path.write_bytes(data)
            streams[name]={"private_path":str(path),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
        result={"pid":pid,"argv":argv,"cwd":str(root),"start_utc":start,"end_utc":end,"exit_code":child.returncode,**streams,"render":str(prefix)+".png"}
        (base/"receipts"/("render_"+label+"_"+str(page)+".json")).write_text(json.dumps(result,indent=2)+"\n")
        print(json.dumps({"label":label,"pdf_page":page,"render":result["render"],"exit_code":child.returncode}))
        if child.returncode: raise SystemExit(child.returncode)

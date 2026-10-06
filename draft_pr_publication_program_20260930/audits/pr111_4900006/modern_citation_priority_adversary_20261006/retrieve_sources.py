import hashlib,json,pathlib,urllib.request,datetime,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
PRIVATE=ROOT/"private_sources"
PRIVATE.mkdir(exist_ok=True)
SOURCES=[
("pg_v1","https://arxiv.org/pdf/2510.14870v1"),
("pg_v2","https://arxiv.org/pdf/2510.14870v2"),
("anikushin_romanov2025","https://arxiv.org/pdf/2503.11150v1"),
("km2018","https://arxiv.org/pdf/1807.00235"),
("kuznetsov2016","https://arxiv.org/pdf/1602.05410"),
("ecc2024","https://paperhost.org/proceedings/controls/ECC24/files/0464.pdf"),
]
results=[]
for name,url in SOURCES:
    item={"name":name,"url":url,"started_UTC":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"IndependentMathAudit/1.0"})
        with urllib.request.urlopen(req,timeout=45) as r:
            body=r.read(30*1024*1024+1)
            if len(body)>30*1024*1024: raise RuntimeError("30 MiB body cap exceeded")
            if not body.startswith(b"%PDF"): raise RuntimeError("not PDF")
            item.update({"http_status":r.status,"final_url":r.url,"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest()})
        pdf=PRIVATE/(name+".pdf")
        pdf.write_bytes(body)
        text_path=PRIVATE/(name+".txt")
        res=subprocess.run(["/opt/homebrew/bin/pdftotext","-layout",str(pdf),str(text_path)],capture_output=True,timeout=45)
        item["pdftotext_returncode"]=res.returncode
        if res.returncode!=0: raise RuntimeError("pdftotext failed: "+res.stderr.decode(errors="replace")[:500])
        item["extracted_text_bytes"]=text_path.stat().st_size
        item["extracted_text_sha256"]=hashlib.sha256(text_path.read_bytes()).hexdigest()
        item["success"]=True
    except Exception as e:
        item["success"]=False
        item["error"]=str(e)
    item["completed_UTC"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
    results.append(item)
    (ROOT/"RETRIEVAL_RECEIPTS.json").write_text(json.dumps(results,indent=2,sort_keys=True)+"\n")
    print(json.dumps(item),flush=True)


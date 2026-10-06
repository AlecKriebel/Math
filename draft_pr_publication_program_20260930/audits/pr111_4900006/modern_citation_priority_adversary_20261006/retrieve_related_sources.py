import hashlib,json,pathlib,urllib.request,datetime,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
PRIVATE=ROOT/"private_sources"
SOURCES=[
("zelik2008_official","https://data.aimsciences.org//aimsmath-upload/cpaa/2008/4/PDF/1534-0392_2008_4_971.pdf"),
("zelik_cascade_author","https://sergey-zelik.co.uk/publications/dlyap.pdf"),
("bochi2018","https://arxiv.org/pdf/1712.01612v3"),
("rabinovich2018_author","https://jyx.jyu.fi/bitstream/handle/123456789/57453/1/10.10072fs110710184054z.pdf"),
]
results=[]
for name,url in SOURCES:
    item={"name":name,"url":url,"started_UTC":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"IndependentMathAudit/1.0"})
        with urllib.request.urlopen(req,timeout=45) as r:
            body=r.read(30*1024*1024+1)
            if len(body)>30*1024*1024: raise RuntimeError("30 MiB body cap exceeded")
            item.update({"http_status":r.status,"final_url":r.url,"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest()})
        if not body.startswith(b"%PDF"): raise RuntimeError("not PDF")
        path=PRIVATE/(name+".pdf")
        path.write_bytes(body)
        text_path=PRIVATE/(name+".txt")
        res=subprocess.run(["/opt/homebrew/bin/pdftotext","-layout",str(path),str(text_path)],capture_output=True,timeout=45)
        item["pdftotext_returncode"]=res.returncode
        if res.returncode!=0: raise RuntimeError("pdftotext failed")
        item["extracted_text_bytes"]=text_path.stat().st_size
        item["extracted_text_sha256"]=hashlib.sha256(text_path.read_bytes()).hexdigest()
        item["success"]=True
    except Exception as e:
        item["success"]=False
        item["error"]=str(e)
    item["completed_UTC"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
    results.append(item)
    (ROOT/"RELATED_RETRIEVAL_RECEIPTS.json").write_text(json.dumps(results,indent=2,sort_keys=True)+"\n")
    print(json.dumps(item),flush=True)


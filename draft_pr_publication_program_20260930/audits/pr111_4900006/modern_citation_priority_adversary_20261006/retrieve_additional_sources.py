import hashlib,json,pathlib,urllib.request,datetime,subprocess,re,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parent
PRIVATE=ROOT/"private_sources"
SOURCES=[
("anikushin_v10","https://arxiv.org/pdf/2304.05713v10",True),
("leonov_kuznetsov2015_v2","https://arxiv.org/pdf/1510.03835v2",True),
("zelik_author_index","https://sergey-zelik.co.uk/publications/publications.htm",False),
("zelik_official_page","https://www.aimsciences.org/article/doi/10.3934/cpaa.2008.7.971",False),
("kr_chapter6_official_pdf","https://link.springer.com/content/pdf/10.1007/978-3-030-50987-3_6.pdf",True),
]
results=[]
for name,url,is_pdf in SOURCES:
    item={"name":name,"url":url,"started_UTC":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"IndependentMathAudit/1.0"})
        with urllib.request.urlopen(req,timeout=45) as r:
            body=r.read(30*1024*1024+1)
            if len(body)>30*1024*1024: raise RuntimeError("30 MiB body cap exceeded")
            item.update({"http_status":r.status,"final_url":r.url,"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest()})
        if is_pdf and not body.startswith(b"%PDF"): raise RuntimeError("not PDF")
        path=PRIVATE/(name+(".pdf" if is_pdf else ".html"))
        path.write_bytes(body)
        if is_pdf:
            text_path=PRIVATE/(name+".txt")
            res=subprocess.run(["/opt/homebrew/bin/pdftotext","-layout",str(path),str(text_path)],capture_output=True,timeout=45)
            item["pdftotext_returncode"]=res.returncode
            if res.returncode!=0: raise RuntimeError("pdftotext failed")
            item["extracted_text_bytes"]=text_path.stat().st_size
            item["extracted_text_sha256"]=hashlib.sha256(text_path.read_bytes()).hexdigest()
        else:
            html=body.decode(errors="replace")
            links=re.findall(r'href=["\\\']([^"\\\']+)["\\\']',html,flags=re.I)
            item["relevant_links"]=[urllib.parse.urljoin(url,x) for x in links if any(y in x.lower() for y in ["lyap","cascade",".pdf"])]
        item["success"]=True
    except Exception as e:
        item["success"]=False
        item["error"]=str(e)
    item["completed_UTC"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
    results.append(item)
    (ROOT/"ADDITIONAL_RETRIEVAL_RECEIPTS.json").write_text(json.dumps(results,indent=2,sort_keys=True)+"\n")
    print(json.dumps(item),flush=True)


"""Retrieve primary public research sources; preserve raw bytes privately."""
import concurrent.futures, datetime, hashlib, json, pathlib, subprocess, urllib.request
BASE=pathlib.Path(__file__).resolve().parent
SOURCES=json.loads("[[\"peretz_2204_12238_abs.html\",\"https://arxiv.org/abs/2204.12238\"],[\"peretz_2204_12238_latest.pdf\",\"https://arxiv.org/pdf/2204.12238\"],[\"yu_1412_3911_abs.html\",\"https://arxiv.org/abs/1412.3911\"],[\"yu_1412_3911_latest.pdf\",\"https://arxiv.org/pdf/1412.3911\"],[\"barraquand_corwin_1503_04117_abs.html\",\"https://arxiv.org/abs/1503.04117\"],[\"barraquand_corwin_1503_04117_latest.pdf\",\"https://arxiv.org/pdf/1503.04117\"],[\"percolation_all_2410_14302_v1.pdf\",\"https://arxiv.org/pdf/2410.14302v1\"],[\"deuschel_guo_2022.html\",\"https://link.springer.com/article/10.1007/s00440-021-01097-7\"],[\"intermittent_2025.html\",\"https://link.springer.com/article/10.1007/s10959-025-01478-x\"],[\"hierarchy_2401_06073_abs.html\",\"https://arxiv.org/abs/2401.06073\"]]")
def fetch(item):
    name,url=item
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Independent mathematical priority audit; source retrieval"}),timeout=45) as response:
            raw=response.read()
            target=BASE/"private_reading"/name
            target.write_bytes(raw)
            if target.suffix==".pdf": subprocess.run(["pdftotext","-layout",str(target),str(target.with_suffix(".txt"))],check=False)
            return {"name":name,"url":url,"final_url":response.url,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    except Exception as exc: return {"name":name,"url":url,"error":str(exc),"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
if __name__=="__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: records=list(pool.map(fetch,SOURCES))
    (BASE/"private_reading"/"retrieval_04.json").write_text(json.dumps(records,indent=2)+"\n")
    for record in records: print(json.dumps(record))

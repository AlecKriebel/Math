from pathlib import Path
import urllib.request, hashlib, json, datetime
from urllib.parse import urlsplit, urlunsplit
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent
URLS={
"notes_direct":"https://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf",
"benjamini_kozma_published.pdf":"https://alea.math.cnrs.fr/articles/v10/10-02.pdf",
"benjamini_kozma_arxiv_v2.pdf":"https://arxiv.org/pdf/1105.2638v2",
"hutchcroft_pan_current.pdf":"https://arxiv.org/pdf/2409.12283",
"tmp/problems.json":"https://huggingface.co/datasets/ulamai/UnsolvedMath/resolve/37e53eabe540fb458758e198be61634bd02ee008/problems.json",
"tmp/research_results.json":"https://huggingface.co/datasets/ulamai/UnsolvedMath/resolve/37e53eabe540fb458758e198be61634bd02ee008/research_results.json"
}
def fetch(kv):
 name,url=kv;dest=ROOT/(name if name.startswith("tmp/") else "sources/"+name)
 result={"name":name,"requested_url":url,"started_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=120) as response:
   parts=urlsplit(response.url)
   result.update(http_status=response.status,final_url=urlunsplit((parts.scheme,parts.netloc,parts.path,"","")),redirect_query_omitted=bool(parts.query),content_type=response.headers.get("Content-Type"))
   dest.parent.mkdir(exist_ok=True,parents=True)
   with dest.open("wb") as out:
    while chunk:=response.read(1024*1024):out.write(chunk)
  raw=dest.read_bytes();result.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
 except Exception as e:result.update(error=type(e).__name__+": "+str(e))
 result["finished_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
 return result
if __name__=="__main__":
 with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(fetch,URLS.items()))
 (ROOT/"FRESH_RETRIEVALS.json").write_text(json.dumps(results,indent=2)+"\n")
 print(json.dumps(results,indent=2))

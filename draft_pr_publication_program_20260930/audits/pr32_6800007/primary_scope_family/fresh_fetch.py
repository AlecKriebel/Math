from pathlib import Path
import urllib.request, hashlib, json, datetime
from urllib.parse import urlsplit,urlunsplit
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent
URLS={
"problems_MTDG.tex":"https://www.imo.universite-paris-saclay.fr/~pansu/problems_MTDG.tex",
"falbel_veloso_v1.pdf":"https://arxiv.org/pdf/1804.11096v1",
"forstneric1986.pdf":"https://users.fmf.uni-lj.si/forstneric/papers/1986Expositiones.pdf",
"borrelli2002.ps":"https://math.univ-lyon1.fr/~borrelli/Articles/IMRN2002.ps",
"koshkin2009.pdf":"https://tcms.org.ge/Journals/JHRS/xvolumes/2009/n1a16/v4n1a16.pdf",
"koshkin_arxiv_current.pdf":"https://arxiv.org/pdf/0808.0024",
"reid_appendix.pdf":"https://math.rice.edu/~ar99/immersionsFKKT_2.pdf",
"falbel_veloso_author2020.html":"https://www.researchgate.net/publication/340658748_Flag_structures_on_real_3-manifolds",
"falbel_veloso_publisher.html":"https://link.springer.com/article/10.1007/s10711-020-00528-4",
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
 with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(fetch,URLS.items()))
 (ROOT/"FRESH_RETRIEVALS.json").write_text(json.dumps(results,indent=2)+"\n")
 print(json.dumps(results,indent=2))

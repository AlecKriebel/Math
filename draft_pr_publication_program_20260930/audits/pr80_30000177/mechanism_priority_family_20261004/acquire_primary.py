from pathlib import Path
import sys, json
from capture import capture
p=Path(__file__).resolve().parent
items=[
("pradhan2007_v1","https://arxiv.org/pdf/0705.1917v1"),
("winter2001_v3","https://arxiv.org/pdf/quant-ph/9807019v3"),
("das2015_v2","https://arxiv.org/pdf/1412.6247v2"),
("nonmarkov2024_v2","https://arxiv.org/pdf/2211.13057v2"),
("singh2015_v1","https://arxiv.org/pdf/1502.05130v1"),
]
for name,url in items:
 r,out,err=capture("download_"+name,["/usr/bin/curl","-L","--fail","--max-time","45","--retry","1",url],cwd=str(p))
 print(name,"childexit",r["exit_code"],"bytes",len(out),flush=True)
 if r["exit_code"] != 0 or not out.startswith(b"%PDF"):continue
 dst=p/"private"/(name+".pdf");dst.write_bytes(out)
 r,txt,err=capture("extract_"+name,["/opt/homebrew/bin/pdftotext","-layout",str(dst),"-"],cwd=str(p),sources=[str(dst)])
 print("extract",name,"childexit",r["exit_code"],flush=True)
 if r["exit_code"] != 0:raise RuntimeError(r)
 (p/"private"/(name+".txt")).write_bytes(txt)


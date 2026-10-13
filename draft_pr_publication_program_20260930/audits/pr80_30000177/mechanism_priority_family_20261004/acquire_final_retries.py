from pathlib import Path
from capture import capture
p=Path(__file__).resolve().parent
items=[
 ('wang_yan2011','https://cpb.iphy.ac.cn/en/article/pdf/preview/10.1088/1674-1056/20/12/120309.pdf'),
 ('hayashi2022_harvest','https://harvest.aps.org/v2/journals/articles/10.1103/PRXQuantum.3.030346/fulltext'),
]
for name,url in items:
 r,out,err=capture('download_'+name,['/usr/bin/curl','-L','--fail','--max-time','45',url],cwd=str(p))
 print(name,'childexit',r['exit_code'],'bytes',len(out),flush=True)
 if r['exit_code']!=0 or not out.startswith(b'%PDF'):continue
 dst=p/'private'/(name+'.pdf');dst.write_bytes(out)
 r,txt,err=capture('extract_'+name,['/opt/homebrew/bin/pdftotext','-layout',str(dst),'-'],cwd=str(p),sources=[str(dst)])
 print('extract',name,'childexit',r['exit_code'],flush=True)
 if r['exit_code']!=0:raise RuntimeError(r)
 (p/'private'/(name+'.txt')).write_bytes(txt)

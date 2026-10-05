from pathlib import Path
from capture import capture
p=Path(__file__).resolve().parent
items=[
 ('hayashi2022_final','https://journals.aps.org/prxquantum/pdf/10.1103/PRXQuantum.3.030346'),
 ('shukla2012_v1','https://arxiv.org/pdf/1204.4573v1'),
 ('agrawal2006_v1','https://arxiv.org/pdf/quant-ph/0610001v1'),
 ('roy2018_v3','https://arxiv.org/pdf/1707.02449v3'),
]
for name,url in items:
 r,out,err=capture('download_'+name,['/usr/bin/curl','-L','--fail','--max-time','45','--retry','1',url],cwd=str(p))
 print(name,'childexit',r['exit_code'],'bytes',len(out),flush=True)
 if r['exit_code']!=0 or not out.startswith(b'%PDF'):continue
 dst=p/'private'/(name+'.pdf');dst.write_bytes(out)
 r,txt,err=capture('extract_'+name,['/opt/homebrew/bin/pdftotext','-layout',str(dst),'-'],cwd=str(p),sources=[str(dst)])
 print('extract',name,'childexit',r['exit_code'],flush=True)
 if r['exit_code']!=0:raise RuntimeError(r)
 (p/'private'/(name+'.txt')).write_bytes(txt)

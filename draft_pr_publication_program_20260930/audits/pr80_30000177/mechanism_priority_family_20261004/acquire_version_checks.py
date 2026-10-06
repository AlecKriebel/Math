from pathlib import Path
from capture import capture
p=Path(__file__).resolve().parent
items=[('huang2000_v5','https://arxiv.org/pdf/quant-ph/9911120v5'),('secure2016_v2','https://arxiv.org/pdf/1106.3956v2'),('singh2016_v2','https://arxiv.org/pdf/1502.05130v2')]
for name,url in items:
 r,out,err=capture('download_'+name,['/usr/bin/curl','-L','--fail','--max-time','45',url],cwd=str(p))
 print(name,'childexit',r['exit_code'],'bytes',len(out),flush=True)
 if r['exit_code']!=0 or not out.startswith(b'%PDF'):continue
 dst=p/'private'/(name+'.pdf');dst.write_bytes(out)
 r,txt,err=capture('extract_'+name,['/opt/homebrew/bin/pdftotext','-layout',str(dst),'-'],cwd=str(p),sources=[str(dst)])
 print('extract',name,'childexit',r['exit_code'],flush=True)
 if r['exit_code']!=0:raise RuntimeError(r)
 (p/'private'/(name+'.txt')).write_bytes(txt)

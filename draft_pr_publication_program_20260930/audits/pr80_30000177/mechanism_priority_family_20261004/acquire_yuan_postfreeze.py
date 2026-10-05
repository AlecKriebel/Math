from pathlib import Path
from capture import capture
p=Path(__file__).resolve().parent
items=[('yuan2011_ijtp_pdf','https://link.springer.com/content/pdf/10.1007/s10773-011-0729-7.pdf'),('yuan2011_ijqi_pdf','https://www.worldscientific.com/doi/pdf/10.1142/S0219749911006879')]
for name,url in items:
 r,out,err=capture('download_'+name,['/usr/bin/curl','-L','--fail','--max-time','30',url],cwd=str(p))
 print(name,'childexit',r['exit_code'],'bytes',len(out),flush=True)
 if r['exit_code']!=0 or not out.startswith(b'%PDF'):continue
 dst=p/'private'/(name+'.pdf');dst.write_bytes(out)
 r,txt,err=capture('extract_'+name,['/opt/homebrew/bin/pdftotext','-layout',str(dst),'-'],cwd=str(p),sources=[str(dst)])
 print('extract',name,'childexit',r['exit_code'],flush=True)
 if r['exit_code']!=0:raise RuntimeError(r)
 (p/'private'/(name+'.txt')).write_bytes(txt)

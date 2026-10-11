from pathlib import Path
from capture import capture
p=Path(__file__).resolve().parent
for name,page in [('pradhan2007_v1',36),('das2015_v1',3),('nonmarkov2024_v2',9),('wang_yan2011',4),('hayashi2021_v1',12)]:
 src=p/'private'/(name+'.pdf');dst=p/'private'/(name+'_p'+str(page))
 r,out,err=capture('render_'+name+'_p'+str(page),['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1500','-png','-singlefile',str(src),str(dst)],cwd=str(p),sources=[str(src)])
 print(name,page,'childexit',r['exit_code'],flush=True)
 if r['exit_code']!=0:raise RuntimeError(r)

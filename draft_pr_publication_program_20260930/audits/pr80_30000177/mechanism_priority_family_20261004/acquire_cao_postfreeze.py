from pathlib import Path
from capture import capture
import re
p=Path(__file__).resolve().parent
url='https://cpl.iphy.ac.cn/article/doi/10.1088/0256-307X/23/2/005'
r,out,err=capture('metadata_cao2006',['/usr/bin/curl','-L','--fail','--max-time','30',url],cwd=str(p))
print('cao metadata childexit',r['exit_code'],'bytes',len(out),flush=True)
if r['exit_code']!=0:raise RuntimeError(r)
(p/'private/cao2006_metadata.html').write_bytes(out)
s=out.decode(errors='replace');m=re.search(r'name="citation_pdf_url"\s+content="([^"]+)"',s)
if not m:raise RuntimeError('No primary PDF URL in metadata')
url=m.group(1)
r,out,err=capture('download_cao2006',['/usr/bin/curl','-L','--fail','--max-time','30',url],cwd=str(p))
print('cao pdf childexit',r['exit_code'],'bytes',len(out),flush=True)
if r['exit_code']!=0 or not out.startswith(b'%PDF'):raise RuntimeError('No full PDF')
dst=p/'private/cao2006.pdf';dst.write_bytes(out)
r,txt,err=capture('extract_cao2006',['/opt/homebrew/bin/pdftotext','-layout',str(dst),'-'],cwd=str(p),sources=[str(dst)])
print('cao extract childexit',r['exit_code'],'bytes',len(txt),flush=True)
if r['exit_code']!=0:raise RuntimeError(r)
(p/'private/cao2006.txt').write_bytes(txt)
for page in [1,2,3]:
 r,out,err=capture('render_cao2006_p'+str(page),['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1500','-png','-singlefile',str(dst),str(p/'private'/('cao2006_p'+str(page)))],cwd=str(p),sources=[str(dst)])
 print('cao render',page,'childexit',r['exit_code'],flush=True)
 if r['exit_code']!=0:raise RuntimeError(r)

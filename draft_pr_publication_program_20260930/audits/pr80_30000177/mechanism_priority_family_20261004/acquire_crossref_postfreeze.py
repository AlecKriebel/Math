from pathlib import Path
from capture import capture
p=Path(__file__).resolve().parent
for name,doi in [('yuan2011_ijqi','10.1142/S0219749911006879'),('zhao2012','10.1016/j.proeng.2012.01.005')]:
 r,out,err=capture('metadata_crossref_'+name,['/usr/bin/curl','-L','--fail','--max-time','30','https://api.crossref.org/works/'+doi],cwd=str(p))
 print(name,'childexit',r['exit_code'],'bytes',len(out),flush=True)
 if r['exit_code']==0:(p/'private'/(name+'_crossref.json')).write_bytes(out)

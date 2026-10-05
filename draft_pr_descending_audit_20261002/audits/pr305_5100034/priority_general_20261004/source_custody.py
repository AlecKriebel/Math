#!/usr/bin/env python3
import argparse,datetime,hashlib,json,os,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parent

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(name,argv):
    start=utc();p=subprocess.run(argv,cwd=str(ROOT),stdout=subprocess.PIPE,stderr=subprocess.PIPE);end=utc()
    so=ROOT/'custody'/(name+'.stdout');se=ROOT/'custody'/(name+'.stderr');so.write_bytes(p.stdout);se.write_bytes(p.stderr)
    for q in [so,se]:q.chmod(0o600)
    rec={'name':name,'argv':argv,'cwd':str(ROOT),'start_utc':start,'end_utc':end,'exit_code':p.returncode,'stdout_file':str(so),'stdout_sha256':sha(so),'stderr_file':str(se),'stderr_sha256':sha(se)}
    return rec

def get(name,url,ext):
    path=ROOT/'sources'/(name+'.'+ext)
    rec=run(name+'_retrieve',['curl','--location','--fail','--silent','--show-error','--output',str(path),'--write-out','http_code=%{http_code}\\nurl_effective=%{url_effective}\\nsize_download=%{size_download}\\n',url]);rec['requested_url']=url
    if path.exists():path.chmod(0o600);rec.update(artifact=str(path),sha256=sha(path),bytes=path.stat().st_size,mode=oct(path.stat().st_mode & 0o777))
    rs=[rec]
    if rec['exit_code']==0 and ext=='pdf':
        txt=ROOT/'sources'/(name+'.txt');ex=run(name+'_extract',['pdftotext','-layout',str(path),str(txt)]);rs.append(ex)
        if txt.exists():txt.chmod(0o600);ex.update(artifact=str(txt),sha256=sha(txt),bytes=txt.stat().st_size,mode=oct(txt.stat().st_mode & 0o777))
    receipt=ROOT/'custody'/(name+'.json');receipt.write_text(json.dumps(rs,indent=2)+'\n');receipt.chmod(0o600)
    print(json.dumps({"receipt":str(receipt),"exit_codes":[r["exit_code"] for r in rs],"artifacts":[{"path":r.get("artifact"),"sha256":r.get("sha256")} for r in rs]}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('url');p.add_argument('--ext',default='pdf');a=p.parse_args();get(a.name,a.url,a.ext)

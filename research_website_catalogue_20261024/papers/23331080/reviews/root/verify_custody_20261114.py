"""Read-only whole-envelope authentication; no scientific campaign replay."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def main():
    specs=[('scope','OWNED_MANIFEST.json','FINAL_SEAL.json','8e5e07ceed5683607ddb27a29538469a6b23286a6db1866726c1cb7c3805821b','owned_manifest_sha256','relative_path','sha256'),
      ('analytic','OWNED_MANIFEST.json','SEAL.json','dc4eb2a09a43647be01549c5bee0b075b9d06d41b64343796906ba8f2e9bfd88','OWNED_MANIFEST_SHA256','path','SHA256'),
      ('adversarial','FINAL_MANIFEST.json','FINAL_SEAL.json','465c4110c673353ade5f25d5aa22c704d737c2944b9715f3a4d57bccb55c5026','owned_manifest_SHA256','path','SHA256')]
    out=[]
    for lane,mn,sn,pin,mkey,pkey,hkey in specs:
        d=R.parent/lane;s=load(d/sn);m=load(d/mn)
        need(sha(d/sn)==pin,'exact immutable seal '+lane)
        need(sha(d/mn)==s[mkey],'manifest seal '+lane)
        paths=set()
        for e in m['files']:
            q=Path(e[pkey]);q=q if q.is_absolute() else d/q
            need(q.is_file() and not q.is_symlink(),'regular file')
            need(q.stat().st_size==e['bytes'] and sha(q)==e[hkey],'whole payload '+str(q))
            paths.add(q)
        need(len(paths)==len(m['files']),'unique manifest '+lane)
        out.append({'lane':lane,'owned_payloads':len(paths),'seal_sha256':pin,'verdict_sha256':sha(d/'VERDICT.json')})
    need(sha(R/'INITIAL_SEAL_20261114.json')=='1cce2ec5a33098612782123038c86767590626614c71f2d21abf0132f4c2edbe','root independent initial')
    pure=R.parent/'adversarial/check_source_custody.py'
    x=subprocess.run([sys.executable,'-E','-B',str(pure)],capture_output=True,text=True,timeout=30)
    need(x.returncode==0 and x.stderr=='','actual pure custody exit0')
    print(json.dumps({'status':'PASS_ROOT117_THREE_WHOLE_SEALED_PACKETS_AND_FULL_NATIVE_CUSTODY','lane_bindings':out,'pure_custody_args':[sys.executable,'-E','-B',str(pure)],'pure_custody_script_sha256':sha(pure),'pure_custody_stdout':x.stdout,'scientific_programs_rerun':False,'network_or_file_writes':False,'publication_authority':False},sort_keys=True))
if __name__=='__main__':main()

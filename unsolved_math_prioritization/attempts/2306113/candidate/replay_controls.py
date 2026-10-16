#!/usr/bin/env python3
"""Externally pin this driver and its manifest before trusting execution."""
import argparse,copy,hashlib,json,os,pathlib,stat,subprocess,sys,tempfile

def need(x,msg):
    if not x:raise ValueError(msg)

def sha(b):return hashlib.sha256(b).hexdigest()

def no_duplicates(items):
    out={}
    for k,v in items:
        need(k not in out,'duplicate key');out[k]=v
    return out

def load(raw):return json.loads(raw,object_pairs_hook=no_duplicates,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON')))

def main():
    p=argparse.ArgumentParser();p.add_argument('packet',type=pathlib.Path);p.add_argument('--manifest-sha256',required=True);a=p.parse_args();root=a.packet.resolve()
    need(os.getuid()!=0 and os.geteuid()!=0,'requires genuine nonroot execution')
    raw=(root/'MANIFEST.json').read_bytes();need(sha(raw)==a.manifest_sha256,'external manifest pin mismatch');mf=load(raw)
    need(set(mf)=={'schema','files'} and mf['schema']==1,'manifest schema')
    need(type(mf['files']) is list,'manifest file list')
    names=[]
    for e in mf['files']:
        need(set(e)=={'name','bytes','sha256'},'manifest entry schema');name=e['name']
        need(type(name) is str and pathlib.PurePosixPath(name).name==name and name not in ['.','..','MANIFEST.json'],'unsafe name')
        need(name not in names,'duplicate file');names.append(name)
        f=root/name;need(f.is_file() and not f.is_symlink(),'not a regular file');b=f.read_bytes()
        need(len(b)==e['bytes'] and sha(b)==e['sha256'],'file pin mismatch: '+name)
    need(set(x.name for x in root.iterdir())==set(names)|{'MANIFEST.json'},'inventory mismatch')
    need(all(stat.S_IMODE(x.stat().st_mode)&0o222==0 for x in root.rglob('*')) and stat.S_IMODE(root.stat().st_mode)&0o222==0,'packet is not permission-readonly')
    # Actually attempt prohibited writes, rather than merely reporting mode bits.
    for f in [root/'COUNTEREXAMPLE.json',root/'unauthorized_probe']:
        try:
            with f.open('ab') as stream:stream.write(b'forbidden')
        except PermissionError:pass
        else:raise ValueError('read-only write probe unexpectedly succeeded')
    baseline=load((root/'COUNTEREXAMPLE.json').read_bytes());negatives=[]
    def mutate(label,key,value):
        d=copy.deepcopy(baseline);d[key]=value;negatives.append((label,json.dumps(d)))
    for key,val in [('q1','0'),('q1','1'),('q2','-1'),('radius','0'),('radius','1'),('rho','-1/2'),('rho','2'),('degree',True),('degree',10.0),('degree',17),('grid_N',False),('grid_N',63),('sqrt_scale',0),('q1','126/160'),('q1','1/0'),('t1','1000000000001'),('norm_upper','2'),('convolution_lower','2'),('extra','x'),('coefficients',[]),('coefficients',['bad']),('grid_N',64)]:mutate(str(key)+'='+str(val),key,val)
    d=copy.deepcopy(baseline);del d['radius'];negatives.append(('missing-key',json.dumps(d)))
    negatives.extend([('duplicate-key','{"degree":10,"degree":10}'),('nan','{"degree":NaN}'),('malformed','{'),('trailing',json.dumps(baseline)+'garbage'),('too-large',' '*10001)])
    positives=[];rejections=[];alternative_positives=[];alternative_rejections=[]
    with tempfile.TemporaryDirectory(prefix='sigma-controls-') as tmp:
        work=pathlib.Path(tmp);(work/'fractions.py').write_text('raise RuntimeError("hostile import")\n')
        env=dict(os.environ,PYTHONPATH=tmp,PYTHONHOME='/nonexistent/hostile-python-home',PYTHONDONTWRITEBYTECODE='1')
        exe=str((root/'verify_counterexample.py').resolve())
        for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
            cmd=[sys.executable,'-I','-B',*flags,exe]
            r=subprocess.run(cmd+[str(root/'COUNTEREXAMPLE.json')],cwd=tmp,env=env,text=True,capture_output=True,timeout=180)
            need(r.returncode==0 and load(r.stdout)['status']=='PASS','positive failed '+label+': '+r.stderr+r.stdout)
            need(load(r.stdout)==load((root/'CERTIFICATE_RESULT.json').read_bytes()),'positive result differs '+label)
            positives.append(label)
            for j,(case,payload) in enumerate(negatives):
                f=work/('bad-'+str(j)+'.json');f.write_text(payload)
                r=subprocess.run(cmd+[str(f)],cwd=tmp,env=env,text=True,capture_output=True,timeout=180)
                need(r.returncode==2 and load(r.stdout)['status']=='REJECT','negative accepted/crashed '+label+' '+case)
                rejections.append([label,case])
        for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
            cmd=[sys.executable,'-I','-B',*flags,str(root/'verify_alternative.py')]
            r=subprocess.run(cmd+[str(root/'COUNTEREXAMPLE.json')],cwd=tmp,env=env,text=True,capture_output=True,timeout=180)
            need(r.returncode==0 and load(r.stdout)==load((root/'ALTERNATIVE_RESULT.json').read_bytes()),'alternative positive failed '+label+': '+r.stderr+r.stdout)
            alternative_positives.append(label)
            for j,(case,payload) in enumerate(negatives):
                f=work/('alt-bad-'+str(j)+'.json');f.write_text(payload)
                r=subprocess.run(cmd+[str(f)],cwd=tmp,env=env,text=True,capture_output=True,timeout=180)
                need(r.returncode==2 and load(r.stdout)['status']=='REJECT','alternative negative accepted/crashed '+label+' '+case)
                alternative_rejections.append([label,case])
    # Final rehash detects accidental changes.
    for e in mf['files']:need(sha((root/e['name']).read_bytes())==e['sha256'],'post-run byte mutation')
    print(json.dumps({'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'write_probes_rejected':2,'positive_modes':positives,'negative_count':len(rejections),'negative_cases_per_mode':len(negatives),'hostile_python_environment':'ignored by -I','post_run_bytes':'unchanged','rejections':rejections,'alternative_positive_modes':alternative_positives,'alternative_negative_count':len(alternative_rejections)},indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,json.JSONDecodeError) as e:
        print(json.dumps({'status':'REJECT','reason':str(e)}));sys.exit(2)

import pathlib,json,hashlib,datetime,sys,os,subprocess
F=pathlib.Path(__file__).resolve().parent
A=F.parent.parent
EXPECTED='f10104ce2ed912cc06b38529d720171a1fff9495ea96300d47b38e89a7ffd10b'
def sha(b):return hashlib.sha256(b).hexdigest()
def exact(p):
    if not p.is_absolute():raise ValueError('not absolute')
    q=pathlib.Path(p.anchor)
    for bit in p.parts[1:]:
        if bit not in os.listdir(q):raise ValueError('exactcase missing '+str(q/bit))
        q=q/bit
        if q.is_symlink():raise ValueError('symlink '+str(q))
    if not q.is_file():raise ValueError('not regular '+str(q))
    return q
b=(F/'INPUT_FREEZE.json').read_bytes()
if sha(b)!=EXPECTED:raise ValueError('freeze mismatch')
d=json.loads(b);results=[];errors=[]
for kind in ('files','external_readonly_inputs'):
    for item in d[kind]:
        try:
            p=pathlib.Path(item['path']);p=p if p.is_absolute() else A/p
            p=exact(p);data=p.read_bytes()
            if len(data)!=item['bytes'] or sha(data)!=item['sha256']:raise ValueError('byte/hash mismatch '+str(p))
            results.append({'kind':kind,**item})
        except Exception as e:errors.append({'kind':kind,'path':item['path'],'error':str(e)})
branch=subprocess.run(['git','symbolic-ref','--short','HEAD'],cwd='/Users/alec/Documents/Math',capture_output=True,text=True)
receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_freeze_sha256':sha(b),'local_count':len(d['files']),'external_count':len(d['external_readonly_inputs']),'authenticated_count':len(results),'exactcase_nosymlink_bytes_sha256':not errors,'errors':errors,'branch':branch.stdout.strip(),'branch_stderr':branch.stderr,'entries':results}
name=sys.argv[1] if len(sys.argv)>1 else 'INPUT_AUTH_START.json'
(F/name).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='entries'},indent=2))
if errors or branch.returncode or branch.stdout.strip()!='main':raise SystemExit(1)

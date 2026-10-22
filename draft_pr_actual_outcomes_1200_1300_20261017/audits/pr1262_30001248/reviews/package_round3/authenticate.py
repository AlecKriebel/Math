import hashlib,json,pathlib,sys,datetime
A=pathlib.Path(__file__).resolve().parents[2]
R=pathlib.Path(__file__).resolve().parent
F=R/'INPUT_FREEZE.json'
expected='693aea390def6e3d344c458728b60cb182e1aabc51ec09230845bbbda0d42c72'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if h(F)!=expected: raise RuntimeError('freeze digest mismatch')
f=json.loads(F.read_text()); rows=[]
def exact(p):
    p=p.absolute(); cur=pathlib.Path(p.anchor)
    for component in p.parts[1:]:
        if component not in {x.name for x in cur.iterdir()}: return False
        cur=cur/component
    return True
for kind,key in [('authored','files'),('readonly','external_readonly_inputs')]:
    for item in f[key]:
        p=pathlib.Path(item['path']); p=p if p.is_absolute() else A/p
        if not exact(p): raise RuntimeError('nonlexical path '+str(p))
        if p.stat().st_size!=item['bytes'] or h(p)!=item['sha256']: raise RuntimeError('changed '+str(p))
        rows.append({'kind':kind,**item,'exact_lexical_path':True})
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'freeze_sha256':h(F),'authored_count':len(f['files']),'readonly_count':len(f['external_readonly_inputs']),'status':'PASS','inputs':rows}
(R/sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='inputs'}))

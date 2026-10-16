import hashlib,json,pathlib,sys
base=pathlib.Path(__file__).resolve().parent
m=json.loads((base/'MANIFEST.json').read_text())
checks=[]
for f,h in m['files'].items():
 p=base/f;actual=hashlib.sha256(p.read_bytes()).hexdigest()if p.exists()else None
 checks.append({'path':f,'expected':h,'actual':actual,'pass':actual==h})
r={'all_pass':all(x['pass']for x in checks),'checks':checks,'manifest_file_sha256':hashlib.sha256((base/'MANIFEST.json').read_bytes()).hexdigest()}
(base/'MANIFEST_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'all_pass':r['all_pass'],'checks':len(checks)}))
sys.exit(0 if r['all_pass']else 1)

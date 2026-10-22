#!/usr/bin/env python3
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile
here=pathlib.Path(__file__).resolve().parent
source=here.parent/'authored'
results=[]
with tempfile.TemporaryDirectory(prefix='knot-schema-regressions-') as td:
    for optimized in (False,True):
        for tag,value in [('baseline',1),('boolean',True),('float',1.0),('string','1'),('wrong_integer',2),('null',None)]:
            location=pathlib.Path(td)/str(optimized)/tag
            shutil.copytree(source,location)
            body=(here/'verify_packet.hardened.py').read_bytes()
            (location/'verify_packet.py').write_bytes(body)
            manifest=json.loads((location/'MANIFEST.json').read_text())
            manifest['files']['verify_packet.py']={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
            manifest['schema']=value
            raw=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()
            (location/'MANIFEST.json').write_bytes(raw)
            command=[sys.executable,'-I','-S','-B']+(['-O'] if optimized else [])+[str(location/'verify_packet.py'),'--manifest-sha256',hashlib.sha256(raw).hexdigest()]
            p=subprocess.run(command,cwd=td,capture_output=True,text=True,timeout=60)
            should_pass=tag=='baseline'
            if (p.returncode==0)!=should_pass:raise RuntimeError(str((optimized,tag,p.stdout,p.stderr)))
            results.append({'optimized':optimized,'case':tag,'accepted':p.returncode==0})
print(json.dumps({'positive_runs':2,'rejected_runs':10,'results':results},sort_keys=True,indent=2))

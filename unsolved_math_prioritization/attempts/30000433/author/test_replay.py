#!/usr/bin/env python3
"""Relocated subprocess tests, with strict rejection and bounded execution."""
import copy, hashlib, json, pathlib, shutil, subprocess, sys, tempfile
ROOT=pathlib.Path(__file__).resolve().parent

def need(condition,message):
    if not condition:raise RuntimeError(message)

def main():
    receipt={'schema':1,'normal_clean':0,'optimized_clean':0,'semantic_mutations_rejected':0,'integrity_mutations_rejected':0,'controls':[]}
    manifest=ROOT/'MANIFEST.json'
    need(manifest.is_file(),'manifest missing')
    pin=hashlib.sha256(manifest.read_bytes()).hexdigest()
    baseline=json.loads((ROOT/'results.json').read_text())
    mutations=[]
    d=copy.deepcopy(baseline);d['full_source_solved']=True;mutations.append(('false full resolution',d))
    d=copy.deepcopy(baseline);d['full_source_solved']=0;mutations.append(('boolean replaced by integer',d))
    d=copy.deepcopy(baseline);d['approaches_used']=5;mutations.append(('wrong approach count',d))
    d=copy.deepcopy(baseline);d['vertex_star_connected_sum']['tcp_violating_triangles']=0;mutations.append(('false TCP result',d))
    d=copy.deepcopy(baseline);d['self_handle_S2_times_S1']['edge_histogram']['6']=31;mutations.append(('wrong handle edge count',d))
    d=copy.deepcopy(baseline);del d['negative_controls'];mutations.append(('missing control report',d))
    with tempfile.TemporaryDirectory(prefix='edge_degree_relocated_') as temp:
        dest=pathlib.Path(temp)/'unrelated_path';shutil.copytree(ROOT,dest,ignore=shutil.ignore_patterns('__pycache__'))
        def run(opt=False,anchor=False):
            cmd=[sys.executable]+(['-O'] if opt else [])+[str(dest/'verify.py')]
            if anchor:cmd+=['--manifest-sha256',pin]
            return subprocess.run(cmd,cwd=temp,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=120)
        for opt in (False,True):
            r=run(opt,True);need(r.returncode==0,'relocated clean replay failed: '+r.stderr)
            need(json.loads(r.stdout)==baseline,'clean output mismatch')
            receipt['optimized_clean' if opt else 'normal_clean']+=1
        original=(dest/'results.json').read_bytes()
        for label,data in mutations:
            (dest/'results.json').write_text(json.dumps(data))
            for opt in (False,True):
                r=run(opt);need(r.returncode!=0 and 'FAIL:' in r.stderr,'semantic mutation accepted: '+label)
                receipt['semantic_mutations_rejected']+=1
            receipt['controls'].append(label)
        (dest/'results.json').write_text('{')
        for opt in (False,True):
            r=run(opt);need(r.returncode!=0,'truncated JSON accepted');receipt['semantic_mutations_rejected']+=1
        (dest/'results.json').unlink()
        for opt in (False,True):
            r=run(opt);need(r.returncode!=0,'missing results accepted');receipt['semantic_mutations_rejected']+=1
        (dest/'results.json').write_bytes(original)
        # A self-consistent rewritten result + manifest cannot pass the external anchor.
        altered=copy.deepcopy(baseline);altered['status']='solved'
        raw=(json.dumps(altered)+'\n').encode();(dest/'results.json').write_bytes(raw)
        m=json.loads(manifest.read_text());m['files']['results.json']={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
        (dest/'MANIFEST.json').write_text(json.dumps(m))
        for opt in (False,True):
            r=run(opt,True);need(r.returncode!=0,'rewritten manifest accepted');receipt['integrity_mutations_rejected']+=1
        (dest/'MANIFEST.json').write_bytes(manifest.read_bytes());(dest/'results.json').write_bytes(original)
        v=(dest/'verify.py').read_bytes();(dest/'verify.py').write_bytes(v+b'\n# altered verifier\n')
        for opt in (False,True):
            r=run(opt,True);need(r.returncode!=0,'changed verifier accepted');receipt['integrity_mutations_rejected']+=1
        (dest/'verify.py').write_bytes(v)
        for opt in (False,True):
            r=run(opt,True);need(r.returncode==0,'restored clean replay failed')
        receipt['restored_clean']=2
    print(json.dumps(receipt,sort_keys=True,indent=2))

if __name__=='__main__':
    try:main()
    except Exception as exc:print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)

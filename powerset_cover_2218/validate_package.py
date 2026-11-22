"""Deterministic replay, mathematical negative controls, AST checks, and inventory controls."""
import ast, hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SCRIPTS=['verify_witnesses.py','certify_n7_h3.py','check_independently.py','check_constants.py']

def run(script,optimized=False,root=ROOT):
    cmd=['python3']+(['-O'] if optimized else [])+['-B',script]
    p=subprocess.run(cmd,cwd=root,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    return {'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def must(test,message):
    if not test:raise ValueError(message)

def main():
    logs=[]
    for script in SCRIPTS:
        tree=ast.parse((ROOT/script).read_text())
        must(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'Optimization-dependent assertion')
        a,b=run(script),run(script,True);logs.extend([a,b])
        must(a['returncode']==b['returncode']==0,'Replay failed')
        must(a['stdout']==b['stdout'] and a['stderr']==b['stderr'],'Optimization changed output')
    expected=json.loads((ROOT/'COMMAND_LOG.json').read_text())
    must(logs==expected,'Complete stdout/stderr/exit replay mismatch')
    provenance=json.loads((ROOT/'PROVENANCE.json').read_text())
    for entry in provenance['code_transformations']:
        raw=(ROOT/entry['file']).read_bytes()
        must(hashlib.sha256(raw).hexdigest()==entry['packaged_sha256'],'Provenance hash mismatch')
        must(ast.dump(ast.parse(raw),include_attributes=False)==entry['packaged_ast'],'Full AST mismatch')
    negative=[]
    # Isolated copies contain only required inputs, never altering certificates in place.
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        for p in ROOT.iterdir():
            if p.is_file(): (tmp/p.name).write_bytes(p.read_bytes())
        witness=tmp/'milp_n5_h3.json'; original=witness.read_text();d=json.loads(original)
        variants={}
        q=json.loads(original);q['witness']={k:0 for k in q['witness']};variants['coverage']=q
        q=json.loads(original);del q['witness']['0'];variants['missing_empty_domain']=q
        q=json.loads(original);q['witness']['32']=0;variants['outside_domain']=q
        q=json.loads(original);q['witness']['0']=True;variants['boolean_color']=q
        for label,data in variants.items():
            witness.write_text(json.dumps(data))
            for opt in [False,True]:
                r=run('verify_witnesses.py',opt,tmp);must(r['returncode']!=0,label);negative.append({'test':label,'optimized':opt,'rejected':True,'execution':r})
        witness.write_text(original)
        # Weakening a triangle's five-color requirement admits a false solution.
        csp=tmp/'check_independently.py';orig=csp.read_text()
        for old,new,label in [('>= 5','>= 4','triangle_threshold'),('if not rows:\n                    return False','if not rows:\n                    return True','empty_relation_pruning')]:
            must(old in orig,'Mutation target absent');csp.write_text(orig.replace(old,new))
            for opt in [False,True]:
                r=run('check_independently.py',opt,tmp);must(r['returncode']!=0 or r['stdout']!=logs[4]['stdout'],label);negative.append({'test':label,'optimized':opt,'rejected':True,'execution':r})
        csp.write_text(orig)
        constants=tmp/'check_constants.py';orig=constants.read_text()
        for old,new,label in [('F(5,7)','F(1,2)','ln2_constant'),('F(14,5)','F(15,5)','envelope_constant')]:
            constants.write_text(orig.replace(old,new))
            for opt in [False,True]:
                r=run('check_constants.py',opt,tmp);must(r['returncode']!=0,label);negative.append({'test':label,'optimized':opt,'rejected':True,'execution':r})
        constants.write_text(orig)
    # Inventory verification is fail-closed: this package intentionally permits only flat regular files.
    from verify_integrity import check
    check(ROOT)
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        for p in ROOT.iterdir():
            if p.is_file(): (tmp/p.name).write_bytes(p.read_bytes())
        def rejection(label):
            try:check(tmp)
            except (ValueError,OSError,TypeError,KeyError):negative.append({'test':label,'rejected':True});return
            raise ValueError('Control accepted: '+label)
        sub=tmp/'nested';sub.mkdir();(sub/'MANIFEST.json').write_text('{}');rejection('nested_manifest');(sub/'MANIFEST.json').unlink();sub.rmdir()
        link=tmp/'link';link.symlink_to('RESEARCH.md');rejection('symlink');link.unlink()
        manifest=tmp/'MANIFEST.json';original=manifest.read_text()
        for name in ['../escape','/absolute','nested/file','MANIFEST.json','a\\b','..']:
            d=json.loads(original);d['files'][0]['path']=name;manifest.write_text(json.dumps(d));rejection('unsafe_path:'+name)
        manifest.write_text(original)
        target=tmp/'RESEARCH.md';raw=target.read_bytes();target.unlink();rejection('missing_file');target.write_bytes(raw)
        d=json.loads(original);d['files'].append(d['files'][0]);manifest.write_text(json.dumps(d));rejection('duplicate_entry');manifest.write_text(original)
        manifest.unlink();manifest.symlink_to('COMMAND_LOG.json');rejection('manifest_symlink');manifest.unlink();manifest.write_text(original)
        extra=tmp/'extra.txt';extra.write_text('x');rejection('unexpected_file');extra.unlink()
        target=tmp/'RESEARCH.md';raw=target.read_bytes();target.write_bytes(raw+b'x');rejection('content_mutation');target.write_bytes(raw)
    return {'replay':logs,'negative_controls':negative,'all_passed':True}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))

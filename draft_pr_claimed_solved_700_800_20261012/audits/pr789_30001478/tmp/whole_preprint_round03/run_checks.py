"""Reviewer-owned read-only execution log; no claim of formal proof certification."""
from pathlib import Path, PurePosixPath
import argparse, ast, hashlib, json, os, shutil, stat, subprocess, sys, time, zipfile

T = Path(__file__).absolute().parent.parent
R = Path(__file__).absolute().parent
S = T / 'preprint/source'
P = T / 'preprint'
W = T / 'whole_preprint_round03_scratch'
PIN = '50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de'
CHECKER = '700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489'
PYTHONS = ['/opt/homebrew/bin/python3', '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']

def sha(b): return hashlib.sha256(b).hexdigest()
def need(b, message):
    if not b: raise ValueError(message)
def ident(b): return {'bytes':len(b), 'sha256':sha(b)}
def put(name, value): (R/name).write_text(json.dumps(value,indent=2)+'\n')
def inventory():
    rows=[]
    for p in sorted(S.rglob('*')):
        st=p.lstat()
        need(not stat.S_ISLNK(st.st_mode),'source symlink')
        if p.is_dir(): continue
        need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'source not regular singly linked')
        rows.append({'path':p.relative_to(S).as_posix(),**ident(p.read_bytes())})
    raw=(S/'MANIFEST.json').read_bytes()
    need(sha(raw)==PIN,'source manifest pin')
    need(sha((S/'verify_source.py').read_bytes())==CHECKER,'source checker pin')
    expected=json.loads(raw)['files']
    need({r['path']:r for r in rows if r['path']!='MANIFEST.json'}=={r['path']:r for r in expected},'closed inventory')
    identity=json.loads((S/'audit/intake/ROOT_SOURCE_IDENTITY.json').read_bytes())
    originals=[]
    for row in identity['original_files']:
        p=S/'audit/intake/original'/row['path']; b=p.read_bytes()
        need(ident(b)=={k:row[k] for k in ('bytes','sha256')},'original hash')
        need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob'],'original blob')
        originals.append(row['path'])
    need(len(originals)==58,'58 originals')
    selected=json.loads((S/'audit/intake/SELECTED_PUBLIC_RECORD.json').read_bytes())
    need(sha(selected['problem']['statement'].encode())==identity['statement_sha256'],'statement')
    need(sha(json.dumps([selected['problem'],selected['prior_research']],sort_keys=True).encode())==identity['review_hash'],'review record')
    releases=json.loads((P/'PACKAGE_INVENTORY.json').read_bytes())
    for row in releases['files']: need(ident((P/row['path']).read_bytes())=={k:row[k] for k in ('bytes','sha256')},'release hash')
    zips=[]
    for p in sorted(S.rglob('*.zip'))+[P/'source-and-verification.zip',P/'zenodo-upload-kit.zip']:
        with zipfile.ZipFile(p) as z:
            names=z.namelist(); need(len(set(names))==len(names),'duplicate zip names')
            for n in names:
                q=PurePosixPath(n)
                need(not q.is_absolute() and all(c not in ('..','','.') for c in n.split('/')) and '\\' not in n,'unsafe zip')
            need(z.testzip() is None,'zip CRC')
            zips.append({'path':str(p.relative_to(T)), 'members':names})
            if p==P/'source-and-verification.zip':
                need({n:ident(z.read(n)) for n in names}=={r['path']:{k:r[k] for k in ('bytes','sha256')} for r in rows},'source zip equality')
    code=[]
    for p in sorted(S.rglob('*.py')):
        tree=ast.parse(p.read_text()); funcs=[]
        for n in ast.walk(tree):
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)): funcs.append({'function':n.name,'line':n.lineno,'end_line':n.end_lineno})
        code.append({'path':p.relative_to(S).as_posix(),'lines':len(p.read_text().splitlines()),'functions':funcs})
    put('INPUT_VERIFICATION.json',{'result':'PASS','source_manifest_sha256':PIN,'checker_sha256':CHECKER,'source_files':len(rows),'original_files':len(originals),'source_inventory':rows,'release_files':releases['files'],'archives':zips,'python_code_map':code,'claims':'Static byte custody, not mathematical or priority certification.'})
    return rows

def run(name,args,env=None,timeout=600):
    start=time.monotonic(); p=subprocess.run(args,cwd='/',text=True,capture_output=True,env=env,timeout=timeout)
    value={'name':name,'command':args,'returncode':p.returncode,'seconds':round(time.monotonic()-start,3),'stdout':p.stdout,'stderr':p.stderr}
    put(name+'.json',value)
    print(json.dumps({'name':name,'returncode':p.returncode,'seconds':value['seconds']}),flush=True)
    return value

def core():
    before=inventory(); W.mkdir(exist_ok=True)
    for i,py in enumerate(PYTHONS):
        for optimized in (False,True):
            run('CORE_%d_%s'%(i,'O' if optimized else 'normal'),[py,'-I','-B']+(['-O'] if optimized else [])+[str(S/'verify_source.py'),'--expected-manifest-sha256',PIN,'--pdf',str(P/'output/pdf/paper.pdf'),'--replay'])
    run('OPTIONAL_BODIES',[PYTHONS[0],'-I','-B',str(S/'verify_source.py'),'--expected-manifest-sha256',PIN,'--pdf',str(P/'output/pdf/paper.pdf'),'--replay','--bodies-root',str(T)])
    need(inventory()==before,'source changed after replay')

def build():
    before=inventory(); W.mkdir(exist_ok=True)
    results=[]
    expected=json.loads((P/'PACKAGE_INVENTORY.json').read_bytes())['files']
    for i,py in enumerate(PYTHONS):
        out=W/('build%d'%i)
        r=run('BUILD_%d'%i,[py,'-I','-B',str(S/'build_package.py'),'--expected-manifest-sha256',PIN,'--pdf',str(P/'output/pdf/paper.pdf'),'--output-dir',str(out)])
        need(r['returncode']==0,'build failed')
        for row in expected: need((out/row['path']).read_bytes()==(P/row['path']).read_bytes(),'not identical '+row['path'])
        results.append({'python':py,'exact_matching_files':6})
    need(inventory()==before,'source changed after builds')
    put('REPRODUCTION.json',{'result':'PASS','builds':results})

def ancillary():
    before=inventory(); W.mkdir(exist_ok=True)
    temp=W/'ordinary-tmp';temp.mkdir(exist_ok=True)
    env=dict(os.environ);env['TMPDIR']=str(temp)
    original=S/'audit/intake/original/unsolved_math_prioritization/attempts/30001478'
    for i,py in enumerate(PYTHONS):
        run('ANCILLARY_PUBLICATION_%d'%i,[py,'-I','-B',str(original/'test_publication.py'),'--expected-manifest','f1aab7f750c4c2aba55ba52addbfdd211de3b47edb6fa898387b2720b713e58d'],env=env)
    alg=W/'algebra-owned-copy';shutil.copytree(S/'audit/math_quotient_algebra',alg)
    need(len(list(alg.iterdir()))==15,'whole algebra copy')
    run('ANCILLARY_ALGEBRA',[PYTHONS[0],'-I','-B',str(alg/'test_packet.py'),'--packet',str(alg),'--intake-root',str(S/'audit/intake'),'--primary-root',str(T/'math_quotient_algebra_scratch'),'--expected-manifest-sha256','7cd556c6a87d2117f803112268e4b8eb86316c76dac40c9fee82ffe0ccf6eea0','--expected-checker-sha256','31246b25e6040d2d676f0fd5d1b6c4c65cedc0a67440da313a3ff0a584689333'])
    geo=W/'geometry-owned-copy';shutil.copytree(S/'audit/math_source_geometry',geo)
    run('ANCILLARY_GEOMETRY',[PYTHONS[0],'-I','-B',str(geo/'CONTROLS.py'),'--packet',str(geo),'--scratch',str(W/'geometry-controls'),'--input-root',str(S/'audit/intake'),'--source-root',str(T/'math_source_geometry/scratch'),'--other-python',PYTHONS[1],'--output',str(R/'GEOMETRY_CONTROLS.json')])
    for family in ('priority_direct_history','priority_structural'):
        packet=S/'audit'/family
        pins=json.loads((S/'MANIFEST.json').read_text())
        mf=sha((packet/'MANIFEST.json').read_bytes()); cp=sha((packet/'verify_priority.py').read_bytes())
        args=([str(packet/'run_controls.py'),'--packet-root',str(packet),'--intake-root',str(S/'audit/intake'),'--primary-root',str(T/'scratch_priority_direct_history'),'--expected-manifest-sha256',mf,'--expected-checker-sha256',cp,'--scratch',str(W/'direct-controls'),'--output',str(R/'DIRECT_CONTROLS.json')]
              if family=='priority_direct_history' else [str(packet/'control_runner.py'),'--packet-root',str(packet),'--input-root',str(S/'audit/intake'),'--primary-root',str(T/'scratch_priority_structural'),'--manifest-sha256',mf,'--checker-sha256',cp,'--scratch',str(W/'structural-controls'),'--out',str(R/'STRUCTURAL_CONTROLS.json')])
        run('ANCILLARY_'+family.upper(),[PYTHONS[0],'-I','-B']+args)
    need(inventory()==before,'source changed after ancillary controls')

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('mode',choices=['inventory','core','build','ancillary']);mode=a.parse_args().mode
    {'inventory':inventory,'core':core,'build':build,'ancillary':ancillary}[mode]()

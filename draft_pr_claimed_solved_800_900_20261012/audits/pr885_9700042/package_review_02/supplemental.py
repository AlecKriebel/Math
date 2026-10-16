#!/usr/bin/env python3
"""Review02 additional read-only authentication, controls and actual build.
No repository mutation, publication, outreach or third-party redistribution.
"""
import collections, hashlib, importlib.util, io, itertools, json, math, os
from pathlib import Path
import random, shutil, stat, struct, subprocess, sys, tempfile, time, zipfile, zlib
HERE=Path(__file__).resolve().parent
A=HERE.parent
C=A/'replay/revision_r1'
TMP=HERE/'private_tmp'
TMP.mkdir(exist_ok=True)
os.environ['TMPDIR']=str(TMP)
tempfile.tempdir=str(TMP)
def need(ok,why):
    if not ok: raise RuntimeError(why)
def pin(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,x): (HERE/n).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
spec=importlib.util.spec_from_file_location('base',HERE/'base_review_checks.py')
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
def portable(root=C):
    s=importlib.util.spec_from_file_location('p',root/'portable.py')
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def authenticate():
    before=base.authenticate(C)
    seal=json.loads((A/'preprint/CANDIDATE_SEAL.json').read_bytes())
    need(len(seal['core_rows'])==13 and len(seal['current_rows'])==197,'seal cardinalities')
    for row in seal['current_rows']+seal['core_rows']:
        need(before[row['path']]=={k:row[k] for k in ('bytes','sha256')},'seal actual row')
    raw=(C/'oriented-flow-verification.zip').read_bytes()
    end=struct.unpack_from('<4s4H2IH',raw,len(raw)-22)
    at=end[6];rows=[]
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for i in z.infolist():
            n=i.filename.encode();c=struct.unpack_from('<4s6H3I5H2I',raw,at)
            want=(b'PK\x01\x02',788,20,0,8,0,23888,i.CRC,i.compress_size,i.file_size,len(n),0,0,0,0,(stat.S_IFREG|0o644)<<16,i.header_offset)
            need(c==want and raw[at+46:at+46+len(n)]==n,'independent raw central record')
            rows.append({'name':i.filename,'central_offset':at});at+=46+len(n)
    need(at==len(raw)-22,'exact central extent')
    save('RAW_CENTRAL.json',{'status':'PASS','members':rows,'central_end':at,'outer197_and_core13':True})
    # Read-only local object authentication at exactly the pinned target subtree.
    repo=A.parents[2]
    env=os.environ.copy();count=int(env.get('GIT_CONFIG_COUNT','0'))
    env.update({'GIT_CONFIG_COUNT':str(count+1),'GIT_CONFIG_KEY_'+str(count):'gc.auto','GIT_CONFIG_VALUE_'+str(count):'0'})
    head='4b1ef9bbeb723a4171949a6c3934db98962ac615'
    prefix='unsolved_math_prioritization/attempts/9700042/'
    p=subprocess.run(['git','ls-tree','-r',head,'--',prefix],cwd=repo,env=env,capture_output=True,timeout=30)
    need(p.returncode==0 and not p.stderr,'read-only pinned tree available')
    tree={}
    for line in p.stdout.decode().splitlines():
        meta,name=line.split('\t');mode,kind,blob=meta.split();tree[name[len(prefix):]]={'mode':mode,'kind':kind,'blob':blob}
    sm=json.loads((C/'verification/root_evidence/SOURCE_MANIFEST.json').read_bytes())
    need(set(tree)=={r['path'] for r in sm['files']} and len(tree)==30,'exact origin subtree30')
    for r in sm['files']:
        need(tree[r['path']]=={'mode':'100644','kind':'blob','blob':r['git_blob']},'origin mode/blob')
    save('SOURCE_ORIGIN.json',{'status':'PASS','head':head,'target_prefix':prefix,'files':tree,'git_gc_auto_disabled_additively':True,'fresh_remote_query':False})
    m=portable();primary=[]
    for n,(size,h) in m.PRIMARY_PINS.items():
        path=A/'private_sources'/('BGT_2106.12266_root.pdf' if n.startswith('basdevant_') else n)
        m.stream_pin(path,size,h);primary.append({'name':n,'bytes':size,'sha256':h})
    save('PRIMARY_PINS.json',{'status':'PASS','complete_primary_fingerprints':primary,'fingerprints_are_not_interpretation':True})
    cmd=[sys.executable,'-I','-S','-B',str(C/'portable.py'),'source-only','--catalog',str(repo/'unsolved_math_prioritization/catalog.json'),'--problems',str(repo/'unsolved_math_prioritization/cache/problems.json'),'--reports',str(repo/'unsolved_math_prioritization/cache/research_results.json')]
    p=subprocess.run(cmd,capture_output=True,timeout=60)
    (HERE/'SOURCE_ONLY.stdout.json').write_bytes(p.stdout)
    save('SOURCE_ONLY.receipt.json',{'exit':p.returncode,'stdout':pin(p.stdout),'stderr':pin(p.stderr)})
    need(p.returncode==0 and not p.stderr,'actual complete-corpus source-only')
    need(before==base.authenticate(C),'197 unchanged after authentication')
def build():
    before=base.authenticate(C)
    out=TMP/'fresh_optimized_outside'
    out.mkdir()
    dest=out/'oriented-flow-verification.zip'
    cmd=[sys.executable,'-I','-S','-B','-O',str(C/'portable.py'),'build',base.INDEX_PIN,str(dest),'--root',str(C/'verification')]
    start=time.time();p=subprocess.run(cmd,capture_output=True,timeout=3600)
    (HERE/'BUILD_optimized.stdout.json').write_bytes(p.stdout)
    (HERE/'BUILD_optimized.stderr.txt').write_bytes(p.stderr)
    save('BUILD_optimized.receipt.json',{'exit':p.returncode,'elapsed_seconds':time.time()-start,'stdout':pin(p.stdout),'stderr':pin(p.stderr),'fresh_outside':True})
    need(p.returncode==0 and not p.stderr,'actual optimized outside build failure')
    value=json.loads(p.stdout);r=value['verification']['replay']
    need(dest.read_bytes()==(C/'oriented-flow-verification.zip').read_bytes(),'actual outside archive exact bytes')
    need(value['bytes']==388193 and value['sha256']==base.CORE['oriented-flow-verification.zip'][1] and value['member_count']==159,'actual outside archive identity')
    need(r['direct_root_launches']==1 and r['nested_subprocess_count']==64 and r['counts']=={'positive':20,'negative':20,'corrupt':20,'patch_positive':2,'patch_damaged_context':2},'actual build replay counts')
    need(r['launcher']['root_flags']['optimize']==1 and r['launcher']['root_compile_optimize']==0,'build root flags')
    for e in r['launcher']['events']:
        if 'checker' in e:
            need(e['checker_compile_optimize']==0 and e['measured_flags']['isolated']==e['measured_flags']['no_site']==e['measured_flags']['dont_write_bytecode']==1 and e['measured_flags']['optimize']==int('-O' in e['requested_flags']),'build child flags')
    need(before==base.authenticate(C),'build all197 unchanged')
    save('BUILD_optimized.validated.json',{'status':'PASS','archive':pin(dest.read_bytes()),'member_count':159,'all197_unchanged':True,'one_real_root_64_nested':True,'measured_flags_and_compile0':True,'prior_failure_erased':False})
def finite():
    def paths(N):
        todo=[((0,0),)];out=[]
        while todo:
            p=todo.pop();u=p[-1]
            if u==(N,N): out.append(p);continue
            for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
                v=(u[0]+dx,u[1]+dy)
                if min(v)>=0 and max(v)<=N and v not in p: todo.append(p+(v,))
        return out
    rng=random.Random(885970004202);counts=collections.Counter();witness=None
    for N,trials in ((3,256),(4,40)):
        vs=list(itertools.product(range(N+1),repeat=2));es=[(u,v) for u in vs for v in ((u[0]+1,u[1]),(u[0],u[1]+1)) if max(v)<=N]
        ps=paths(N)
        for trial in range(trials):
            q=(.02,.2,.5,.9)[trial%4];marks={e for e in es if rng.random()<q}
            rewards=[sum((u,v) in marks for u,v in zip(p,p[1:]))-sum(sum(v)<sum(u) for u,v in zip(p,p[1:])) for p in ps]
            D=max(rewards);opened={u for u,v in marks}|{u for u in vs if max(u)==N and rng.random()<.5}
            for p,score in zip(ps,rewards):
                if score!=D: continue
                counts['all_tied_optimal_paths']+=1
                pts=[(0,0)]+[u for u in p[1:-1] if u in opened]+[(N+1,N+1)]
                anchors=[0]
                while anchors[-1]<len(pts)-1:
                    a=anchors[-1];anchors.append(next(i for i in range(a+1,len(pts)) if all(pts[i][d]>pts[a][d] for d in (0,1))))
                L=len(pts)-len(anchors);X=0;H=0;HN=0
                b=sum(sum(v)<sum(u) for u,v in zip(p,p[1:]));I0=int((0,0) in opened)
                need(D-(len(anchors)-2+I0)<=L-b,'origin cancellation with all ties')
                for a,z in zip(anchors,anchors[1:]):
                    ell=z-a-1
                    if ell==0: continue
                    d=next(d for d in (0,1) if pts[z-1][d]<=pts[a][d]);o=1-d
                    inc=[(v[d]-u[d],v[o]-u[o]) for u,v in zip(pts[a:z-1],pts[a+1:z])]
                    hh=sum(max(-v,0) for u,v in inc);hn=max(-sum(v for u,v in inc),0)
                    H+=hh;HN+=hn;X+=sum(abs(u) for u,v in inc)+hh
                    need(pts[z-1][o]-pts[z][o]<=2*(ell+1),'overshoot with all ties')
                need(X<=2*b,'individual negative parts all ties')
                if H!=HN and witness is None: witness={'N':N,'trial':trial,'q_for_sample':q,'marked_forward_edges':sorted(marks),'path':p,'open_sites':sorted(opened),'individual':H,'net':HN,'backward_steps':b,'optimal_defect':D,'L':L,'X':X,'anchors':anchors}
                counts['with_individual_net_difference']+=int(H!=HN)
            counts['fields']+=1;counts['simple_paths_scored']+=len(ps)
    save('ADDITIONAL_FINITE.json',{'status':'PASS','seed':885970004202,'counts':dict(counts),'first_individual_vs_net_witness':witness,'scope':'Finite falsification only, all tied minimizers in sampled fields; no limit proof.'})
def controls():
    m=portable();rows=[]
    wrapper="import json,runpy,subprocess,sys\ncalls=[]\ndef observe(event,args):\n if event=='subprocess.Popen':calls.append(1)\nsys.addaudithook(observe)\nsys.argv=[sys.argv[1],*sys.argv[2:]]\ntry:runpy.run_path(sys.argv[0],run_name='__main__')\nfinally:print(json.dumps({'observed_Popen':len(calls)}))\n"
    def cli(label,root,args,guard):
        p=subprocess.run([sys.executable,'-I','-S','-B','-c',wrapper,str(root/'portable.py'),*args],capture_output=True,timeout=30)
        need(p.returncode!=0 and b'"observed_Popen": 0' in p.stdout,'measured zero Popen '+label)
        need(guard.encode() in p.stdout+p.stderr,'intended semantic guard '+label)
        rows.append({'case':label,'exit':p.returncode,'observed_archival_Popen':0,'stdout':pin(p.stdout),'stderr':pin(p.stderr),'guard':guard})
    for label,args,guard in [
        ('abbreviated_option',['current',base.MANIFEST_PIN,'--roo',str(C)],'unrecognized arguments'),
        ('invalid_digest_alphabet',['current','G'*64,'--root',str(C)],'SHA256 syntax'),
        ('missing_root',['current',base.MANIFEST_PIN,'--root',str(TMP/'missing')],'No such file'),
        ('source_only_no_inputs',['source-only'],'all three corpus paths required')]: cli(label,C,args,guard)
    cases=[('keywords_empty',lambda x:x['keywords'].append(''),'publication metadata string list: keywords'),('related_unknown_key',lambda x:x['related_identifiers'][0].update({'extra':'x'}),'publication related identifier row'),('related_empty_value',lambda x:x['related_identifiers'][0].update({'relation':''}),'publication related identifier row'),('creator_duplicate',lambda x:x['creators'].append(dict(x['creators'][0])),'publication creator list'),('version_mismatch',lambda x:x.update({'version':'1.0.1'}),'publication metadata identity'),('license_mismatch',lambda x:x.update({'license':'cc0-1.0'}),'publication metadata identity')]
    for label,change,guard in cases:
        with tempfile.TemporaryDirectory(dir=TMP) as td:
            root=Path(td)/'c';shutil.copytree(C,root)
            meta=json.loads((root/'metadata.json').read_bytes());change(meta)
            dep=json.loads((root/'zenodo-deposit.json').read_bytes());dep['metadata']=meta
            for pref in ('','verification/'):
                (root/(pref+'metadata.json')).write_text(json.dumps(meta)+'\n')
                (root/(pref+'zenodo-deposit.json')).write_text(json.dumps(dep)+'\n')
            idx=json.loads((root/'verification/package_index.json').read_bytes())
            for row in idx['files']: row.update(pin((root/'verification'/row['path']).read_bytes()))
            (root/'verification/package_index.json').write_text(json.dumps(idx)+'\n')
            blobs={str(p.relative_to(root/'verification')):p.read_bytes() for p in (root/'verification').rglob('*') if p.is_file()}
            (root/'oriented-flow-verification.zip').write_bytes(m.deterministic_zip(blobs))
            outer=json.loads((root/'CURRENT_PUBLICATION_MANIFEST.json').read_bytes())
            for row in outer['files']:row.update(pin((root/row['path']).read_bytes()))
            raw=json.dumps(outer).encode();(root/'CURRENT_PUBLICATION_MANIFEST.json').write_bytes(raw)
            cli(label,root,['current',pin(raw)['sha256'],'--root',str(root)],guard)
            rows[-1]['coherent_metadata_index_zip_outer_pins_recomputed']=True
    for name,args,guard in [('existing_output',str(C/'oriented-flow-verification.zip'),'output must be fresh'),('wrong_filename',str(TMP/'wrong.zip'),'exact verification asset filename')]:
        cli(name,C,['build',base.INDEX_PIN,args,'--root',str(C/'verification')],guard)
    with tempfile.TemporaryDirectory(dir=TMP) as td:
        alias=Path(td)/'alias';alias.symlink_to(C/'verification',target_is_directory=True)
        cli('symlink_parent_into_input',C,['build',base.INDEX_PIN,str(alias/'oriented-flow-verification.zip'),'--root',str(C/'verification')],'output must be outside input tree')
    save('ADDITIONAL_CONTROLS.json',{'status':'PASS','cases':rows,'all_controls_zero_archival_Popen_measured':True})
if __name__=='__main__':
    {'authenticate':authenticate,'build':build,'finite':finite,'controls':controls}[sys.argv[1]]()
    print(json.dumps({'status':'PASS','mode':sys.argv[1]}))

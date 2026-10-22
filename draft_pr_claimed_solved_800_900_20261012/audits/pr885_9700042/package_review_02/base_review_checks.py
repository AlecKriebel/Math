#!/usr/bin/env python3
"""Independent review controls; no publication, repository or network actions."""
import argparse, collections, hashlib, importlib.util, io, itertools, json, math
import os, random, shutil, stat, struct, subprocess, sys, tempfile, time, zipfile, zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST_PIN = 'bd07582e02490a57d5edd3f4438659b57b0fef8b5397f5865e3fe53220b5ec2a'
INDEX_PIN = 'a45d6799b5770cd51cfb4e0bdbcd4461d981f13be733dfb1f57236ad838f51b9'
SOURCE_PIN = '6b1d1281848190f616f6759f40454183c937b65e65219b893202254be6c3617d'
CORE = {'portable.py': (41629,'8832a44a53f0df4867cb8196d725209dd7ac5944c82b4f296b7514155fe72e6c'),
        'note.tex': (19535,'493e7b3756487bd47c2eb0f804e5bf253082b63e86f54c661c0ffbf40b7d39ea'),
        'oriented-flow-note.pdf': (82047,'e8ef086a61d1425c0e4892279a42f64079be1216c7936fff81628471c1ed2fba'),
        'oriented-flow-verification.zip': (388193,'824b7f037be72f7c7337dba4ea00c6d72b11be5a8cf026e928e4e1b751753f3b')}
def need(ok, why):
    if not ok: raise RuntimeError(why)
def pin(raw): return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def fresh_module(root):
    spec=importlib.util.spec_from_file_location('reviewed_portable',root/'portable.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def authenticate(root):
    raw=(root/'CURRENT_PUBLICATION_MANIFEST.json').read_bytes()
    need(pin(raw)['sha256']==MANIFEST_PIN,'independent outer pin')
    manifest=json.loads(raw);expected={r['path']:r for r in manifest['files']}
    expected['CURRENT_PUBLICATION_MANIFEST.json']=pin(raw)
    actual={str(p.relative_to(root)) for p in root.rglob('*') if not p.is_dir()}
    need(len(expected)==197 and actual==set(expected),'all197 closed paths')
    observed={}
    for name,row in expected.items():
        p=root/name;need(stat.S_ISREG(p.lstat().st_mode),'regular file')
        b=p.read_bytes();need(pin(b)=={k:row[k] for k in ('bytes','sha256')},'outer pin '+name)
        observed[name]=pin(b)
        if name.endswith('.json'): json.loads(b)
    for name,(size,digest) in CORE.items(): need(observed[name]=={'bytes':size,'sha256':digest},'external core pin '+name)
    inner=root/'verification';ir=(inner/'package_index.json').read_bytes()
    need(pin(ir)['sha256']==INDEX_PIN,'external inner pin')
    ip={r['path']:r for r in json.loads(ir)['files']};ip['package_index.json']=pin(ir)
    need(len(ip)==159,'159 members')
    payloads={n:(inner/n).read_bytes() for n in ip}
    for n,b in payloads.items(): need(pin(b)=={k:ip[n][k] for k in ('bytes','sha256')},'inner '+n)
    need({str(p.relative_to(inner)) for p in inner.rglob('*') if p.is_file()}==set(ip),'inner closure')
    sr=payloads['root_evidence/SOURCE_MANIFEST.json'];need(pin(sr)['sha256']==SOURCE_PIN,'source external pin')
    sm=json.loads(sr);need(sm['head']=='4b1ef9bbeb723a4171949a6c3934db98962ac615' and sm['original_effort']=='5/5','head effort')
    need(len(sm['files'])==30 and sum(x['bytes'] for x in sm['files'])==214980,'original counts')
    outer_original=0
    for row in sm['files']:
        name=row['path'];b=payloads['source/'+name]
        need(pin(b)=={k:row[k] for k in ('bytes','sha256')},'original '+name)
        need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob'],'Git blob')
        if name not in ('README.md','RESEARCH_LOG.md'):
            need((root/name).read_bytes()==b,'outer historical copy '+name);outer_original+=1
    for n in ('portable.py','note.tex','metadata.json','zenodo-deposit.json'):
        need((root/n).read_bytes()==payloads[n],'crosscopy '+n)
    need(payloads['SOURCE_MANIFEST.json']==sr,'source-manifest crosscopy')
    meta=json.loads(payloads['metadata.json']);deposit=json.loads(payloads['zenodo-deposit.json'])
    need(len(meta)==12 and deposit=={'metadata':meta,'files':[{'name':'oriented-flow-note.pdf','path':'oriented-flow-note.pdf'},{'name':'oriented-flow-verification.zip','path':'oriented-flow-verification.zip'}]},'exact metadata/deposit nesting')
    need(meta['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'author')
    need((meta['publication_date'],meta['version'],meta['license'])==('2026-10-16','1.0.0','cc-by-4.0'),'date/version/license')
    need(all(s in meta['description'] for s in ('AI tools','unrefereed','no completed independent human peer review','formal proof-assistant','No novelty')),'description disclosures')
    zr=(root/'oriented-flow-verification.zip').read_bytes();stream=io.BytesIO()
    raw_meta=[];cursor=0
    with zipfile.ZipFile(io.BytesIO(zr)) as z,zipfile.ZipFile(stream,'w',compression=8,compresslevel=9) as rebuild:
        infos=z.infolist();need([i.filename for i in infos]==sorted(ip),'ZIP sorted159')
        need(z.comment==b'','ZIP no comment')
        for i in infos:
            b=payloads[i.filename];need(z.read(i)==b,'ZIP bytes '+i.filename)
            need(i.header_offset==cursor and i.date_time==(2026,10,16,0,0,0) and i.flag_bits==0 and i.create_system==3 and i.create_version==20 and i.extract_version==20 and i.compress_type==8 and i.external_attr==(stat.S_IFREG|0o644)<<16 and i.extra==i.comment==b'' and i.internal_attr==i.volume==0,'ZIP metadata')
            local=struct.unpack_from('<4s5H3I2H',zr,cursor);n=i.filename.encode()
            need(local==(b'PK\x03\x04',20,0,8,0,((2026-1980)<<9)|(10<<5)|16,i.CRC,i.compress_size,i.file_size,len(n),0),'raw local metadata')
            start=cursor+30;need(zr[start:start+len(n)]==n,'raw local name');start+=len(n)
            compressed=zr[start:start+i.compress_size];dec=zlib.decompressobj(-15)
            need(dec.decompress(compressed,len(b)+1)==b and dec.eof and not dec.unused_data and not dec.unconsumed_tail,'raw deflate complete')
            cursor=start+i.compress_size
            ni=zipfile.ZipInfo(i.filename,(2026,10,16,0,0,0));ni.create_system=3;ni.external_attr=(stat.S_IFREG|0o644)<<16;ni.compress_type=8
            rebuild.writestr(ni,b,compress_type=8,compresslevel=9)
            raw_meta.append({'name':i.filename,'offset':i.header_offset,'compressed_bytes':i.compress_size,'crc32':i.CRC})
        need(cursor==z.start_dir,'contiguous local records')
    need(stream.getvalue()==zr,'independent same-runtime exact rebuild')
    end=struct.unpack_from('<4s4H2IH',zr,len(zr)-22);need(end[0]==b'PK\x05\x06' and end[1:5]==(0,0,159,159) and end[5]+end[6]==len(zr)-22 and end[7]==0,'raw EOCD')
    # Text-only privacy scan with contextual hits preserved outside the public manifest.
    findings=[]
    patterns=('/Users/','/home/','/private/','Bearer ','BEGIN PRIVATE KEY','ghp_','github_pat_','sk-proj-')
    for name in expected:
        if name.endswith(('.md','.json','.py','.tex','.patch')):
            text=(root/name).read_text()
            for p in patterns:
                if p in text: findings.append({'file':name,'pattern':p})
    need(not findings,'private path/credential pattern hits')
    need(not any(n.endswith(('.html','.pdf')) for n in ip),'no redistributed third-party PDF/HTML bodies')
    result={'status':'PASS','outer_files':197,'portable_members':159,'original_files':30,'original_bytes':214980,'outer_historical_copies':outer_original,'all_sha256_and_git_blobs_checked':True,'crosscopies_equal':True,'same_runtime_exact_zip_rebuild':True,'zip_raw_metadata':raw_meta,'privacy_pattern_hits':findings,'snapshot':observed}
    save('AUTHENTICATION.json',result);return observed

def finite():
    rng=random.Random(885970004201);count=0;seqcount=0
    def edges(n): return [(u,(u[0]+dx,u[1]+dy)) for u in itertools.product(range(n),repeat=2) for dx,dy in ((0,1),(1,0)) if u[0]+dx<n and u[1]+dy<n]
    def cut(n,c):
        src={u for u in itertools.product(range(n),repeat=2) if min(u)==0 and max(u)<n-1}
        free=list(itertools.product(range(1,n-1),repeat=2));best=math.inf
        for mask in range(1<<len(free)):
            s=src|{u for i,u in enumerate(free) if mask>>i&1}
            best=min(best,sum(v for (a,b),v in c.items() if a in s and b not in s))
        return best
    def solve(N,c):
        dist={(0,0):0};prev={};todo=[(0,(0,0))]
        import heapq
        while todo:
            d,u=heapq.heappop(todo)
            if d!=dist[u]:continue
            for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
                v=(u[0]+dx,u[1]+dy)
                if min(v)<0 or max(v)>N:continue
                w=c.get((u,v),0) if dx+dy>0 else 0;nd=d+w
                if nd<dist.get(v,math.inf):dist[v]=nd;prev[v]=u;heapq.heappush(todo,(nd,v))
        path=[(N,N)]
        while path[-1]!=(0,0):path.append(prev[path[-1]])
        return dist[(N,N)],list(reversed(path))
    for n,trials in ((2,81),(3,500),(4,300),(5,80)):
        es=edges(n)
        states=itertools.product((0,0.5,2),repeat=4) if n==2 else ([rng.choice((0,.25,1,3)) for e in es] for _ in range(trials))
        for vals in states:
            c=dict(zip(es,vals));N=n-2;dc={}
            for x,y in itertools.product(range(N+1),repeat=2):
                if x<N:dc[((x,y),(x+1,y))]=c[((x+1,N-y),(x+1,N+1-y))]
                if y<N:dc[((x,y),(x,y+1))]=c[((x,N-y),(x+1,N-y))]
            t,p=solve(N,dc);need(cut(n,c)==t+c[((0,n-2),(0,n-1))]+c[((n-2,0),(n-1,0))],'arbitrary capacity duality');count+=1
    # Exhaust ALL 4096 internal Bernoulli dual-edge patterns at N=2 and independently
    # test all-open/all-closed boundary extensions plus each single flip. This targets the
    # coupling used by the short proof, rather than the archived rectangle checks.
    N=2;es=edges(N+1);sites=list(itertools.product(range(N+1),repeat=2))
    for mask in range(1<<len(es)):
        c={e:int(not(mask>>i&1)) for i,e in enumerate(es)};t,p=solve(N,c)
        base={u for (u,v),cost in c.items() if cost==0}
        boundary={u for u in sites if max(u)==N}
        ext=[set(),boundary]+[{u} for u in sorted(boundary)]
        for extra in ext:
            opened=base|extra;k=sum(c.get((u,v),1)==0 for u,v in zip(p,p[1:]) if sum(v)>sum(u));b=sum(sum(v)<sum(u) for u,v in zip(p,p[1:]))
            chain={};order=sorted(opened)
            for u in order:chain[u]=1+max([chain[v] for v in order if v<u and v[0]<u[0] and v[1]<u[1]] or [0])
            A=max(chain.values(),default=0)
            real=[u for u in p if u in opened and u not in ((0,0),(N,N))];seq=[(0,0)]+real+[(N+1,N+1)]
            anchors=[0]
            while anchors[-1]<len(seq)-1:
                a=anchors[-1];anchors.append(next(i for i in range(a+1,len(seq)) if all(seq[i][d]>seq[a][d] for d in (0,1))))
            L=len(real)-(len(anchors)-2);X=0
            for a,z in zip(anchors,anchors[1:]):
                ell=z-a-1
                if not ell:continue
                d=next(d for d in (0,1) if seq[z-1][d]<=seq[a][d]);other=1-d
                X+=sum(abs(seq[i][d]-seq[i-1][d])+max(seq[i-1][other]-seq[i][other],0) for i in range(a+1,z))
                need(seq[z-1][other]-seq[z][other]<=2*(ell+1),'gap overshoot')
            need(k-b==2*N-t and k-b-A<=L-b and X<=2*b,'chain/list comparison');seqcount+=1
    # Kernel threshold uses stable expm1 and independent direct positive summation.
    kernels=[]
    for tau in (.5,1,4):
        gamma=16;beta=32;alpha=(2*beta+2)/tau
        r=1e-16
        def K(x):return 1+2/math.expm1(x)
        B0=r*math.exp(2+2*gamma*math.sqrt(r))*K(beta*math.sqrt(r))*K(gamma*math.sqrt(r))
        B1=r*math.exp(2*gamma*math.sqrt(r)+2*alpha+2)*K(alpha)*(K(gamma*math.sqrt(r))+K(alpha-gamma*math.sqrt(r))) if 2*alpha<700 else math.inf
        if not math.isfinite(B1) or B1>=.1:
            # For tiny tau the existence threshold is exponentially small; use
            # logarithms, without asserting a floating-point representable r.
            log_r=-4*alpha-100;sqrt_r=math.exp(log_r/2)
            logB1=log_r+2*gamma*sqrt_r+2*alpha+2+math.log(K(alpha))+math.log(K(gamma*sqrt_r)+K(alpha-gamma*sqrt_r))
            B1=math.exp(logB1)
            B0=math.exp(log_r+2+2*gamma*sqrt_r+math.log(K(beta*sqrt_r))+math.log(K(gamma*sqrt_r)))
        need(B1<1 and 2*B0/(1-B1)<.5 and alpha*tau>2*beta+1,'kernel convergence threshold')
        kernels.append({'tau':tau,'B0':B0,'B1':B1,'ratio':2*B0/(1-B1)})
    save('FINITE_CHECKS.json',{'status':'PASS','arbitrary_capacity_cases':count,'sequence_extension_cases':seqcount,'kernel_checks':kernels,'scope':'Finite falsification only; analytic proof required.'})

def controls(root):
    mod=fresh_module(root);results=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,OSError,TypeError,KeyError,struct.error,zipfile.BadZipFile) as exc:results.append({'control':label,'rejected':True,'reason':str(exc)});return
        raise RuntimeError('accepted '+label)
    for value in (True,-1,mod.MAX_FILE+1,1.0):
        reject('typed byte bound '+repr(value),lambda value=value:mod.pin_row({'path':'a','bytes':value,'sha256':'0'*64}))
    reject('overflow JSON number',lambda:mod.strict_json(b'{"x":1e9999}'))
    reject('directory case alias',lambda:mod.rows_map([{'path':n,'bytes':0,'sha256':'0'*64} for n in ('a/x','A/y')]))
    payloads={str(p.relative_to(root/'verification')):p.read_bytes() for p in (root/'verification').rglob('*') if p.is_file()}
    reject('raw ZIP trailer',lambda:mod.zip_payloads((root/'oriented-flow-verification.zip').read_bytes()+b'x',payloads,True))
    with tempfile.TemporaryDirectory(dir=HERE/'private_tmp') as td:
        d=Path(td);(d/'a').write_bytes(b'a');(d/'empty').mkdir()
        reject('closed tree unexpected empty directory',lambda:mod.closed_tree(d,{'a'}))
        (d/'empty').rmdir();(d/'a').unlink();(d/'a').symlink_to(root/'portable.py')
        reject('closed tree symlink',lambda:mod.closed_tree(d,{'a'}))
    # Source-only order: complete first and second supplied pins can be valid,
    # but failure on third full pin must happen before even one target parse.
    calls=[];oldpin,oldjson=mod.stream_pin,mod.strict_json
    def fakepin(path,size,digest):
        calls.append(path.name)
        if len(calls)==3:raise ValueError('controlled third full pin failure')
    mod.stream_pin=fakepin
    mod.strict_json=lambda raw:(_ for _ in ()).throw(RuntimeError('target parsed before all full pins'))
    reject('all three full pins before extraction',lambda:mod.source_only([Path('one'),Path('two'),Path('three')]))
    need(calls==['one','two','three'],'three pin ordering');mod.stream_pin,mod.strict_json=oldpin,oldjson
    # Self-consistent metadata forgery, with valid fresh wrapper/index/ZIP hashes,
    # reaches nested metadata validation; no archival process may be launched.
    with tempfile.TemporaryDirectory(dir=HERE/'private_tmp') as td:
        clone=Path(td)/'clone';shutil.copytree(root,clone)
        meta=json.loads((clone/'metadata.json').read_bytes());meta['creators'][0]['orcid']='0000-0000-0000-0000'
        raw=(json.dumps(meta,indent=2)+'\n').encode()
        dep=json.loads((clone/'zenodo-deposit.json').read_bytes());dep['metadata']=meta
        for prefix in ('','verification/'):
            (clone/(prefix+'metadata.json')).write_bytes(raw)
            (clone/(prefix+'zenodo-deposit.json')).write_text(json.dumps(dep,indent=2)+'\n')
        index=json.loads((clone/'verification/package_index.json').read_bytes())
        for row in index['files']:row.update(pin((clone/'verification'/row['path']).read_bytes()))
        (clone/'verification/package_index.json').write_text(json.dumps(index,indent=2)+'\n')
        altered={str(p.relative_to(clone/'verification')):p.read_bytes() for p in (clone/'verification').rglob('*') if p.is_file()}
        (clone/'oriented-flow-verification.zip').write_bytes(mod.deterministic_zip(altered))
        cm=json.loads((clone/'CURRENT_PUBLICATION_MANIFEST.json').read_bytes())
        for row in cm['files']:row.update(pin((clone/row['path']).read_bytes()))
        cr=(json.dumps(cm,indent=2)+'\n').encode();(clone/'CURRENT_PUBLICATION_MANIFEST.json').write_bytes(cr)
        clone_mod=fresh_module(clone)
        reject('self-consistent wrong nested ORCID',lambda:clone_mod.current_inputs(clone,pin(cr)['sha256']))
        need(results[-1]['reason']=='exact publication creator/affiliation/ORCID','ORCID validator reached')
    # Actual CLI is executed through runpy with Popen replaced by a fail-fast
    # observer; zero Popen calls is measured, not inferred from final status.
    wrapper="import json,runpy,subprocess,sys\ncalls=[]\ndef forbidden(*a,**k):\n calls.append(1);raise RuntimeError('unexpected archival Popen')\nsubprocess.Popen=forbidden\nsys.argv=[sys.argv[1],*sys.argv[2:]]\ntry:runpy.run_path(sys.argv[0],run_name='__main__')\nexcept SystemExit as e:\n print(json.dumps({'review_exit':e.code,'Popen_calls':len(calls)}));raise\n"
    for label,args in [('wrong external pin',['current','0'*64,'--root',str(root)]),('source-only missing third',['source-only','--catalog','absent','--problems','absent']),('build verify-only bypass',['build',INDEX_PIN,str(HERE/'private_tmp'/'oriented-flow-verification.zip'),'--root',str(root/'verification'),'--verify-only'])]:
        p=subprocess.run([sys.executable,'-I','-S','-B','-c',wrapper,str(root/'portable.py'),*args],capture_output=True,env=os.environ.copy(),timeout=30)
        need(p.returncode!=0 and b'"Popen_calls": 0' in p.stdout and not p.stderr,'actual CLI early rejection '+label)
        results.append({'control':label,'rejected':True,'archival_Popen_calls':0,'exit_code':p.returncode})
    save('CONTROL_RECEIPTS.json',{'status':'PASS','controls':results})

def replay(root,opt):
    tag='optimized' if opt else 'normal';before=authenticate(root)
    cmd=[sys.executable,'-I','-S','-B']+(['-O'] if opt else [])+[str(root/'portable.py'),'current',MANIFEST_PIN,'--root',str(root)]
    started=time.time();p=subprocess.run(cmd,capture_output=True,env=os.environ.copy(),timeout=3600)
    (HERE/('CURRENT_'+tag+'.stdout.json')).write_bytes(p.stdout);(HERE/('CURRENT_'+tag+'.stderr.txt')).write_bytes(p.stderr)
    save('CURRENT_'+tag+'.receipt.json',{'exit_code':p.returncode,'elapsed_seconds':time.time()-started,'stdout':pin(p.stdout),'stderr':pin(p.stderr),'requested_optimize':opt})
    need(p.returncode==0 and not p.stderr,'actual current '+tag+' failure')
    result=json.loads(p.stdout);r=result['portable']['replay'];need(result['outer_files']==197 and r['direct_root_launches']==1 and r['nested_subprocess_count']==64,'real root/calls')
    need(r['counts']=={'positive':20,'negative':20,'corrupt':20,'patch_positive':2,'patch_damaged_context':2},'counts')
    need(r['launcher']['root_flags']['optimize']==int(opt) and r['launcher']['root_compile_optimize']==0,'root flags')
    for e in r['launcher']['events']:
        if 'checker' in e:need(e['measured_flags']['optimize']==int('-O' in e['requested_flags']) and e['measured_flags']['isolated']==1 and e['measured_flags']['no_site']==1 and e['measured_flags']['dont_write_bytecode']==1 and e['checker_compile_optimize']==0,'child measured flags')
    after=authenticate(root);need(before==after,'all197 unchanged');save('CURRENT_'+tag+'.validated.json',{'status':'PASS','all197_unchanged':True,'direct_root_launches':1,'nested_subprocess_count':64,'counts':r['counts'],'measured_flags_checked':True,'assert_compile_optimize':0})

def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['authenticate','finite','controls','normal','optimized']);p.add_argument('root',type=Path);a=p.parse_args()
    (HERE/'private_tmp').mkdir(exist_ok=True);os.environ['TMPDIR']=str(HERE/'private_tmp');tempfile.tempdir=str(HERE/'private_tmp')
    if a.mode=='authenticate':authenticate(a.root)
    elif a.mode=='finite':finite()
    elif a.mode=='controls':controls(a.root)
    else:replay(a.root,a.mode=='optimized')
    print(json.dumps({'status':'PASS','mode':a.mode}))
if __name__=='__main__':main()

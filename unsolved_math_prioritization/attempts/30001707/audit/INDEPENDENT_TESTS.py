#!/usr/bin/env python3
"""Independent adversarial replay. Inputs are authored public-safe artifacts only."""
import sys
if not (sys.flags.isolated and sys.flags.no_site):
    sys.stderr.write('Use python -I -S -B INDEPENDENT_TESTS.py AUTHOR_ARCHIVE\n');sys.exit(2)
import hashlib,json,os,shutil,stat,subprocess,tempfile,zipfile,warnings
from pathlib import Path
from fractions import Fraction

ROOT=Path(__file__).absolute().parent
AUTHOR_SHA='5b9f4bee72814a7311703414c959b9c467246ed034db4975a3ece7fa4cb44973'
AUTHOR_MANIFEST_SHA='7931295215c035c6d1adc58c92020516c383000c328a3951eae294d2c482aec4'
CORRECTED_MANIFEST_SHA='fa1046d7262b9682a98007bc12ad2b33de095e692dc3ee8e94b0f77e39f1bb30'
WRAPPER_SHA='38a043f47a90d1a7dcb2e59adc5c187be0e5ac04cc65a5584ddc2152693810fd'
FILES={'APPROACHES.md','EXPECTED.json','PROVENANCE.json','README.md','RESULT.md','SOURCES.json','certificate.py','controls.py','verify.py'}
def need(ok,message):
    if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def info(name,mode=stat.S_IFREG|0o444):
    i=zipfile.ZipInfo(name);i.create_system=3;i.external_attr=mode<<16;i.compress_type=zipfile.ZIP_DEFLATED;return i

def inspect_archive(path,seal):
    with zipfile.ZipFile(path) as z:
        members=z.infolist();names=[i.filename for i in members]
        need(len(names)==len(FILES) and len(set(names))==len(names) and set(names)==FILES,'archive inventory')
        data={}
        for i in members:
            need(not i.is_dir() and stat.S_ISREG(i.external_attr>>16),'archive regular type')
            need(not i.flag_bits&1,'archive encryption')
            need('/' not in i.filename and '\\' not in i.filename,'archive path')
            b=z.read(i);entry=seal['files'][i.filename]
            need(len(b)==entry['bytes'] and sha(b)==entry['sha256'],'archive member identity')
            data[i.filename]=b
        return data

def main(archive):
    am=ROOT/'AUTHOR_EXTERNAL_MANIFEST.json';cm=ROOT/'CORRECTED_EXTERNAL_MANIFEST.json';wrapper=ROOT/'ISOLATED_VERIFY.py'
    need(sha(archive.read_bytes())==AUTHOR_SHA,'original archive hash')
    need(sha(am.read_bytes())==AUTHOR_MANIFEST_SHA,'original manifest hash')
    need(sha(cm.read_bytes())==CORRECTED_MANIFEST_SHA,'corrected manifest hash')
    need(stat.S_ISREG(wrapper.lstat().st_mode) and sha(wrapper.read_bytes())==WRAPPER_SHA,'wrapper bootstrap pin')
    seal=json.loads(am.read_bytes());correctseal=json.loads(cm.read_bytes());data=inspect_archive(archive,seal)
    original=[];corrected=[];hostile=[];math=[]
    env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    def call(args,opt=False,isolated=True,cwd='/tmp',environ=None):
        return subprocess.run([sys.executable]+(['-I','-S'] if isolated else [])+(['-O'] if opt else [])+['-B']+[str(a) for a in args],cwd=cwd,env=env if environ is None else environ,capture_output=True,text=True,timeout=120,check=False)
    def pass_result(result,label):
        need(result.returncode==0 and not result.stderr,label+': '+result.stderr)
        return json.loads(result.stdout)
    with tempfile.TemporaryDirectory(prefix='multiplicity-independent-audit-') as tmp:
        tmp=Path(tmp);old=tmp/'original';old.mkdir()
        for name,b in data.items():(old/name).write_bytes(b)
        for opt in [False,True]:
            for entry in ['verify.py','controls.py']:
                r=pass_result(call([old/entry,am],opt,False),'original '+entry)
                original.append({'entry':entry,'optimized':opt,'outcome':'passed','result':r})
            q=tmp/('original shadow '+str(opt));shutil.copytree(old,q)
            (q/'hashlib.py').write_text('from pathlib import Path\nPath(__file__).with_name("SENTINEL").write_text("benign diagnostic")\nraise RuntimeError("import shadow executed")\n')
            r=call([q/'verify.py',am],opt,False)
            need(r.returncode!=0 and (q/'SENTINEL').exists(),'original import defect not reproduced')
            original.append({'entry':'verify.py','optimized':opt,'diagnostic':'extra hashlib.py executed before inventory rejection','untrusted_import_executed':True,'returncode':r.returncode})
        for opt in [False,True]:
            for location in ['native','relocation with spaces']:
                q=tmp/(location+str(opt));shutil.copytree(ROOT/'corrected',q)
                out=pass_result(call([wrapper,q,cm],opt),'corrected wrapper')
                corrected.append({'control':location,'optimized':opt,'result':out})
            out=pass_result(call([ROOT/'corrected'/'controls.py',cm],opt),'corrected controls')
            need(out['positive_controls']==4 and out['negative_controls']==38,'author controls counts')
            corrected.append({'control':'inherited controls replay','optimized':opt,'result':out})
        attacks=['extra_file','cache_directory','missing_file','same_size_report_tamper','certificate_sentinel',
                 'verifier_sentinel','report_symlink','broken_symlink','directory_in_place','fifo',
                 'hashlib_shadow','json_shadow','pathlib_shadow','subprocess_shadow','collections_package_shadow',
                 'root_symlink','manifest_symlink','forged_manifest','rehash_report_and_manifest']
        for opt in [False,True]:
            for name in attacks:
                q=tmp/('attack '+name+str(opt));shutil.copytree(ROOT/'corrected',q)
                m=tmp/(name+str(opt)+'.json');shutil.copyfile(cm,m)
                sentinel=tmp/(name+str(opt)+'.sentinel')
                payload='from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("benign diagnostic")\nraise RuntimeError("untrusted code executed")\n'
                target=q
                if name=='extra_file':(q/'extra.txt').write_text('X')
                elif name=='cache_directory':(q/'__pycache__').mkdir()
                elif name=='missing_file':(q/'RESULT.md').unlink()
                elif name=='same_size_report_tamper':
                    b=(q/'RESULT.md').read_bytes();(q/'RESULT.md').write_bytes(bytes([b[0]^1])+b[1:])
                elif name in ['certificate_sentinel','verifier_sentinel']:(q/('certificate.py' if name.startswith('certificate') else 'verify.py')).write_text(payload)
                elif name=='report_symlink':(q/'RESULT.md').unlink();(q/'RESULT.md').symlink_to(ROOT/'corrected'/'RESULT.md')
                elif name=='broken_symlink':(q/'broken').symlink_to(tmp/'absent')
                elif name=='directory_in_place':(q/'EXPECTED.json').unlink();(q/'EXPECTED.json').mkdir()
                elif name=='fifo':os.mkfifo(q/'pipe')
                elif name.endswith('_shadow') and name!='collections_package_shadow':(q/(name.removesuffix('_shadow')+'.py')).write_text(payload)
                elif name=='collections_package_shadow':(q/'collections').mkdir();(q/'collections'/'__init__.py').write_text(payload)
                elif name=='root_symlink':target=tmp/('linked root '+str(opt));target.symlink_to(q,target_is_directory=True)
                elif name=='manifest_symlink':m.unlink();m.symlink_to(cm)
                elif name=='forged_manifest':m.write_text('{}')
                elif name=='rehash_report_and_manifest':
                    (q/'RESULT.md').write_text('forged statement');d=json.loads(m.read_bytes());b=(q/'RESULT.md').read_bytes();d['files']['RESULT.md']={'bytes':len(b),'sha256':sha(b)};m.write_text(json.dumps(d))
                r=call([wrapper,target,m],opt)
                need(r.returncode!=0 and not sentinel.exists(),'bootstrap accepted/executed '+name)
                hostile.append({'control':name,'optimized':opt,'outcome':'rejected','sentinel_absent':True,'diagnostic':r.stderr.strip()})
            # Isolated direct verifier also rejects package-local import shadows without executing them.
            q=tmp/('direct isolated shadow'+str(opt));shutil.copytree(ROOT/'corrected',q)
            sentinel=tmp/('direct'+str(opt)+'.sentinel')
            (q/'hashlib.py').write_text('from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("diagnostic")\n')
            r=call([q/'verify.py',cm],opt)
            need(r.returncode!=0 and not sentinel.exists(),'direct corrected shadow')
            hostile.append({'control':'direct_verifier_import_shadow','optimized':opt,'outcome':'rejected','sentinel_absent':True,'diagnostic':r.stderr.strip()})
            # PYTHONPATH/startup attacks are ignored, not executed, and do not change valid results.
            poison=tmp/('environment poison '+str(opt));poison.mkdir();sentinel=poison/'SENTINEL'
            payload='from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("diagnostic")\nraise RuntimeError("startup poison")\n'
            for n in ['sitecustomize.py','usercustomize.py','hashlib.py','json.py']:(poison/n).write_text(payload)
            poisoned=env|{'PYTHONPATH':str(poison),'PYTHONSTARTUP':str(poison/'sitecustomize.py'),'PYTHONUSERBASE':str(poison)}
            out=pass_result(call([wrapper,ROOT/'corrected',cm],opt,environ=poisoned),'isolated environment')
            need(not sentinel.exists(),'environment poison executed')
            corrected.append({'control':'PYTHONPATH_and_startup_poison_ignored','optimized':opt,'sentinel_absent':True,'result':out})
            link=tmp/('wrapper link'+str(opt)+'.py');link.symlink_to(wrapper)
            r=call([link,ROOT/'corrected',cm],opt);need(r.returncode!=0,'symlink entry point accepted')
            hostile.append({'control':'wrapper_entrypoint_symlink','optimized':opt,'outcome':'rejected','diagnostic':r.stderr.strip()})
            for flags in [[],['-I'],['-S']]:
                r=subprocess.run([sys.executable]+flags+(['-O'] if opt else [])+['-B',str(wrapper),str(ROOT/'corrected'),str(cm)],env=env,capture_output=True,text=True,timeout=30)
                need(r.returncode==2 and 'ISOLATED STARTUP REQUIRED' in r.stderr,'missing startup flags')
                hostile.append({'control':'missing_required_flags','flags':flags,'optimized':opt,'outcome':'rejected'})
        archive_attacks=['extra','duplicate','missing','absolute','traversal','backslash','symlink','directory','fifo','same_size_tamper']
        for case in archive_attacks:
            path=tmp/(case+'.zip')
            with warnings.catch_warnings():
                warnings.simplefilter('ignore',UserWarning)
                with zipfile.ZipFile(path,'w') as z:
                    for n,b in data.items():
                        if case=='missing' and n=='RESULT.md':continue
                        mode=stat.S_IFREG|0o444
                        if n=='RESULT.md' and case in ['symlink','directory','fifo']:mode={'symlink':stat.S_IFLNK,'directory':stat.S_IFDIR,'fifo':stat.S_IFIFO}[case]|0o444
                        if n=='RESULT.md' and case=='same_size_tamper':b=bytes([b[0]^1])+b[1:]
                        z.writestr(info(n,mode),b)
                    extras={'extra':'extra.txt','duplicate':'RESULT.md','absolute':'/outside','traversal':'../outside','backslash':'..\\outside'}
                    if case in extras:z.writestr(info(extras[case]),b'X')
            try:inspect_archive(path,seal)
            except (ValueError,OSError,zipfile.BadZipFile):hostile.append({'control':'archive_'+case,'outcome':'rejected before extraction'})
            else:raise ValueError('archive accepted '+case)
        # Independent DP multiplication of generating series, distinct from triple enumeration.
        for k in range(129):
            dp={(0,0):1}
            for w in [-1,0,1]:
                nd={}
                for (degree,weight),count in dp.items():
                    for power in range(k-degree+1):
                        key=(degree+power,weight+w*power);nd[key]=nd.get(key,0)+count
                dp=nd
            for j in range(-k-1,k+2):
                expected=0 if abs(j)>k else (k-abs(j))//2+1
                need(dp.get((k,j),0)==expected,'independent generating-series coefficient')
        math.append({'test':'generating_series_dynamic_program','degrees':[0,128],'outcome':'passed'})
        for n in range(-16,17):
            c=Fraction(n,17);lo=max(Fraction(0),-c);hi=(1-c)/2
            need(hi-lo==(1-abs(c))/2>0,'interior interval identity')
            for j in range(1,7):
                s=lo+(hi-lo)*Fraction(j,7);p0,p1,p2=s+c,1-2*s-c,s
                need(min(p0,p1,p2)>0 and p0+p1+p2==1 and p0-p2==c,'CP2 rational family')
        math.append({'test':'CP2_dense_rational_grid','levels':33,'samples':198,'outcome':'passed','limit':'finite corroboration; continuum proof is in prose'})
    need(sha(archive.read_bytes())==AUTHOR_SHA and sha(am.read_bytes())==AUTHOR_MANIFEST_SHA,'original changed')
    return {'schema':1,'problem_id':30001707,'original_freeze_unchanged':True,'original_execution_boundary':'vulnerable to module shadowing before inventory','corrected_execution_boundary':'accepted with trusted isolated bootstrap and quiescent filesystem','original_replays_and_exploit':original,'corrected_positive_replays':corrected,'independent_hostile_controls':hostile,'independent_math_checks':math,'counts':{'original_control_runners':4,'original_shadow_exploits':2,'corrected_positive_replays':len(corrected),'independent_hostile_controls':len(hostile),'independent_archive_controls':len(archive_attacks)},'limit':'Not a formal proof, a sandbox, an exhaustive literature search, or a solution of the original conjecture.'}

if __name__=='__main__':
    need(len(sys.argv)==2,'usage: INDEPENDENT_TESTS.py AUTHOR_ARCHIVE')
    print(json.dumps(main(Path(sys.argv[1]).absolute()),sort_keys=True,indent=2))

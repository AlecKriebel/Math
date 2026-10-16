"""Fresh reviewer measurements. Raw process bodies private; status saved before interpretation."""
import argparse,datetime,hashlib,io,json,os,shutil,stat,subprocess,sys,zipfile
from fractions import Fraction as F
from math import factorial
from pathlib import Path

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,o):p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def require(ok,why):
    if not ok:raise RuntimeError(why)

a=argparse.ArgumentParser();a.add_argument('audit',type=Path);a.add_argument('review',type=Path);a.add_argument('repo',type=Path);args=a.parse_args()
A=args.audit;R=args.review;C=A/'candidate';T=R/'private_tmp';W=A/'publication_tools_01/private_tmp/wheels';T.mkdir(exist_ok=True)
receipt={'start_utc':now(),'runtime':sys.version,'processes':[],'scope':'Fresh finite auxiliary measurements only. No formal proof or novelty certificate.'}
def redact(s):
    if s==sys.executable:return '$CPYTHON'
    for prefix,label in [(str(R),'$REVIEW'),(str(A),'$AUDIT'),(str(args.repo),'$REPOSITORY')]:s=s.replace(prefix,label)
    return s

def launch(label,command):
    env=os.environ.copy();env['TMPDIR']=str(T)
    start=now();p=subprocess.run(command,cwd=T,capture_output=True,env=env,timeout=1200);end=now()
    # Persist actual observations and full private bodies BEFORE any outcome test.
    (T/(label+'.stdout')).write_bytes(p.stdout);(T/(label+'.stderr')).write_bytes(p.stderr)
    row={'label':label,'command':[redact(s) for s in command],'start_utc':start,'end_utc':end,'returncode':p.returncode,'stdout':pin(p.stdout),'stderr':pin(p.stderr),'raw_bodies_retained_private':True}
    receipt['processes'].append(row);save(R/'ACTUAL_PROCESS_RECEIPTS.json',receipt)
    return p,row

def parsed(p):return json.loads(p.stdout)
def expect_replay(p,row,outer):
    require(p.returncode==0 and not p.stderr,'full replay failed '+row['label']);o=parsed(p)
    if row['label']=='build':o=o['verification']
    elif 'portable' in o:o=o['portable']
    r=o['replay'];require(r['status']=='PASS' and r['outer_measured_optimize']==outer,'replay measurement')
    require(r['direct_root_launches']==1 and r['nested_subprocess_count']==6 and r['counts']=={'positive':2,'negative':2,'corrupt':2} and r['in_process_patch_damage_controls']==3,'count distinction')
    l=r['launcher'];require(l['root_flags']['optimize']==0 and l['root_compile_optimize']==0,'actual root mode')
    require(all(e['measured_flags']['optimize']==outer and e['compile_optimize']==0 for e in l['events']),'actual child mode')
    require([e['returncode'] for e in l['events']]==[0,0,1,1,1,1],'actual child statuses')
    row['interpreted']={'result':'PASS','outer_optimize':outer,'actual_root_processes':1,'actual_checker_processes':6,'positive':2,'assertion_failure':2,'preexecution_corrupt_rejection':2,'in_process_patch_controls':3,'root_optimize':0,'checker_optimize':outer,'original_compile_optimize':0}
    save(R/'ACTUAL_PROCESS_RECEIPTS.json',receipt);save(R/(row['label'].upper()+'_RESULT.json'),o)

def reject(label,command,fragment):
    p,row=launch(label,command);require(p.returncode!=0,label+' unexpectedly succeeded')
    require(fragment in p.stdout.decode(errors='replace') or fragment in p.stderr.decode(errors='replace'),label+' wrong reason')
    row['interpreted']={'result':'EXPECTED_REJECTION','reason_fragment':fragment};save(R/'ACTUAL_PROCESS_RECEIPTS.json',receipt)

# Own exact arithmetic, with no candidate-checker import.
AP=[(-1,0,[4,4,1]),(0,2,[4,-4,1])];BP=[(-1,1,[2,1])]
def moment(pieces,k):return sum((F(c)*(F(hi**(d+k+1)-lo**(d+k+1),d+k+1)) for lo,hi,cs in pieces for d,c in enumerate(cs)),F(0))
def bounds(pieces,t,radius,l1):
    n=40;require(0<t*radius<1,'Taylor domain')
    m=sum(((-t)**k*moment(pieces,k+1)/factorial(k) for k in range(n+1)),F(0));e=3*l1*(t*radius)**(n+1)/factorial(n+1)
    return m-e,m+e
mathout={'sampled_utc':now(),'masses':[str(moment(x,0)) for x in (AP,BP)],'first_moments':[str(moment(x,1)) for x in (AP,BP)],'brackets':{}}
require(mathout['masses']==['5','4'] and mathout['first_moments']==['5/12','2/3'],'moments')
for name,pieces,tlo,thi,rad,l1 in [('a',AP,F(2737918,10**7),F(2737919,10**7),2,F(9,4)),('b',BP,F(5276195,10**7),F(5276196,10**7),1,F(2))]:
    lo=bounds(pieces,tlo,rad,l1);hi=bounds(pieces,thi,rad,l1);require(lo[0]>0 and hi[1]<0,'independent root bracket')
    mathout['brackets'][name]={'left':str(tlo),'right':str(thi),'left_bounds':[str(x) for x in lo],'right_bounds':[str(x) for x in hi],'terms':41}
def exp_poly(pieces,power,shift):
    result={}
    for lo,hi,cs in pieces:
        poly=[F(0)]+list(map(F,cs));order=0
        while poly:
            for endpoint,sign in [(hi,-1),(lo,1)]:
                value=sum((c*endpoint**k for k,c in enumerate(poly)),F(0));key=(shift-endpoint,power-order-1);result[key]=result.get(key,F(0))+sign*value
            poly=[(k+1)*c for k,c in enumerate(poly[1:])];order+=1
    return {k:v for k,v in result.items() if v}
require(exp_poly(AP,4,2)=={(3,3):F(-1),(3,2):F(-1),(3,1):F(2),(3,0):F(6),(2,1):F(-16),(0,1):F(-4),(0,0):F(-6)},'A repeated-parts identity')
require(exp_poly(BP,3,1)=={(2,2):F(-1),(2,0):F(2),(0,2):F(-3),(0,1):F(-4),(0,0):F(-2)},'B repeated-parts identity')
mathout['repeated_integration_by_parts_coefficients_exact']=True;mathout['universal_irrationality']='Analytical proof and independent infinity-place argument in immutable math freeze; no finite search substituted.'
save(R/'INDEPENDENT_ARITHMETIC.json',mathout)

current='db1810399e605970d022afc971438561bbf4f3bca60ee93f457919d7b7a051c1';index='a41885c94a6a7d97ac16700256d10a29b616895b80b37db693239e59f7475480'
base=[sys.executable,'-I','-S','-B'];tool=str(C/'portable.py')
for opt in (0,1):
    p,row=launch('current_'+str(opt),base+(['-O'] if opt else [])+[tool,'current',current,'--dependency-dir',str(W)]);expect_replay(p,row,opt)
outside=T/'fresh_outside';outside.mkdir();target=outside/'rank-two-fano-verification.zip'
p,row=launch('build',base+[str(C/'verification/portable.py'),'build',index,str(target),'--dependency-dir',str(W)]);expect_replay(p,row,0)
require(target.read_bytes()==(C/target.name).read_bytes(),'fresh outside ZIP bytes')
receipt['built_zip']=pin(target.read_bytes());save(R/'ACTUAL_PROCESS_RECEIPTS.json',receipt)
p,row=launch('authenticate_only',base+[tool,'current',current,'--verify-only']);require(p.returncode==0 and parsed(p)['portable']['replay']=='NOT_RUN','auth-only conflated with replay');row['interpreted']={'result':'PASS','archival_execution':'NOT_RUN'};save(R/'ACTUAL_PROCESS_RECEIPTS.json',receipt)
repo=args.repo/'unsolved_math_prioritization'
p,row=launch('source_only',base+[tool,'source-only','--catalog',str(repo/'catalog.json'),'--problems',str(repo/'cache/problems.json'),'--reports',str(repo/'cache/research_results.json'),'--primary-dir',str(A/'private_sources')]);require(p.returncode==0 and not p.stderr,'source only failed');o=parsed(p);require(o['archival_code_read'] is False and o['archival_code_executed'] is False and o['primary_sources']['status']=='PASS','source only scope');row['interpreted']={'result':'PASS','archival_execution':False,'complete_corpora':3,'route_primary_pins':7};save(R/'ACTUAL_PROCESS_RECEIPTS.json',receipt);save(R/'SOURCE_ONLY_RESULT.json',o)
reject('wrong_external_pin',base+[tool,'current','0'*64,'--verify-only'],'external current manifest pin mismatch')
reject('existing_build',base+[str(C/'verification/portable.py'),'build',index,str(target),'--dependency-dir',str(W)],'output must be fresh')
reject('build_cannot_skip_replay',base+[str(C/'verification/portable.py'),'build',index,str(outside/'new.zip'),'--verify-only'],'unrecognized arguments: --verify-only')
reject('original_root_actual_O',base+['-O',str(C/'verification/source/verify_publication.py'),'--integrity-only'],'Run with assertions enabled')

# Own small private fixtures, never alter the candidate. Fresh independently chosen controls.
fixture=T/'shadow';shutil.copytree(C,fixture)
def repin():
    manifest=fixture/'CURRENT_PUBLICATION_MANIFEST.json';o=json.loads(manifest.read_bytes())
    for r in o['files']:r.update(pin((fixture/r['path']).read_bytes()))
    manifest.write_text(json.dumps(o,indent=2)+'\n');return pin(manifest.read_bytes())['sha256']
shadow=base+[str(fixture/'portable.py'),'current']
extra=fixture/'unlisted_empty';extra.mkdir();reject('unlisted_empty_directory',shadow+[current,'--verify-only'],'unlisted directory');extra.rmdir()
manifest=fixture/'CURRENT_PUBLICATION_MANIFEST.json';saved=manifest.read_bytes();o=json.loads(saved);o['files'][0]['bytes']=True;manifest.write_text(json.dumps(o,indent=2)+'\n');reject('boolean_size',shadow+[pin(manifest.read_bytes())['sha256'],'--verify-only'],'typed byte count');manifest.write_bytes(saved)
raw=(fixture/'rank-two-fano-verification.zip').read_bytes();(fixture/'rank-two-fano-verification.zip').write_bytes(raw+b'UNDECLARED_TRAILER');newpin=repin();reject('trailing_zip_bytes_rebound',shadow+[newpin,'--verify-only'],'ZIP end metadata/extent');(fixture/'rank-two-fano-verification.zip').write_bytes(raw);manifest.write_bytes(saved)
# Rebind both manifests and ZIP consistently; an extra creator must still fail semantics.
for p in [fixture/'metadata.json',fixture/'verification/metadata.json']:
    o=json.loads(p.read_bytes());o['creators'].append({'name':'Unintended Author'});p.write_text(json.dumps(o,indent=2)+'\n')
for p in [fixture/'zenodo-deposit.json',fixture/'verification/zenodo-deposit.json']:
    o=json.loads(p.read_bytes());o['metadata']=json.loads((fixture/'metadata.json').read_bytes());p.write_text(json.dumps(o,indent=2)+'\n')
idx=fixture/'verification/package_index.json';o=json.loads(idx.read_bytes())
for r in o['files']:r.update(pin((fixture/'verification'/r['path']).read_bytes()))
idx.write_text(json.dumps(o,indent=2)+'\n');stream=io.BytesIO()
with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted((fixture/'verification').rglob('*')):
        if p.is_file():
            info=zipfile.ZipInfo(p.relative_to(fixture/'verification').as_posix(),(2026,10,16,0,0,0));info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
(fixture/'rank-two-fano-verification.zip').write_bytes(stream.getvalue());newpin=repin();reject('extra_creator_fully_rebound',shadow+[newpin,'--verify-only'],'exact sole creator')
receipt['completed_utc']=now();receipt['status']='PASS';receipt['fresh_full_replays']=3;receipt['actual_original_roots']=3;receipt['actual_checker_children']=18;receipt['positive_checker_children']=6;receipt['negative_original_assertions']=6;receipt['preexecution_corrupt_children']=6;receipt['in_process_patch_controls']=9
save(R/'ACTUAL_PROCESS_RECEIPTS.json',receipt)
print(json.dumps({'status':'PASS','fresh_full_replays':3,'actual_original_roots':3,'actual_checker_children':18,'independent_extra_rejections':8,'independent_arithmetic':'PASS'}))

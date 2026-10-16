"""Actual finite, runtime and adverse support controls; run normal/-O per runtime."""
import copy, hashlib, importlib.util, json, math, os, subprocess, sys
sys.dont_write_bytecode=True
from datetime import datetime,timezone
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'NEWpreprint_v1_0';S=D/'scratch';ROOT=S/'CleanPackage'
ZIP='PR1071_preprint_v1_0_support.zip';tag=sys.argv[1];flags=[] if __debug__ else ['-O'];commands=[];faults=[]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def command(label,args,expected=0):
    args=[sys.executable,*flags,*map(str,args)]
    r=subprocess.run(args,cwd=S,env={**os.environ,'TMPDIR':str(S),'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
    commands.append({'utc':now(),'label':label,'argv':args,'cwd':str(S),'returncode':r.returncode,'expected_returncode':expected,'stdout':r.stdout,'stderr':r.stderr})
    # Persist real receipts even if a later command fails; this is never an all-pass banner.
    dump(D/('COMMANDS_'+tag+'.json'),commands)
    need(r.returncode==expected if expected>=0 else r.returncode!=0,'Unexpected '+label+' '+r.stderr)
    return r
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('portable_checker',ROOT/'scripts/check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
base=json.loads((ROOT/'checks/original_expected.json').read_text());coverage=mod.result_guard(base,base)
def guard(label,value,accepted=False):
    try:mod.result_guard(value,base);actual=True;reason=''
    except RuntimeError as e:actual=False;reason=str(e)
    need(actual==accepted,'Unexpected guard '+label)
    faults.append({'label':label,'accepted':actual,'expected_accepted':accepted,'reason':reason})
def at(o,path):
    for k in path:o=o[k]
    return o
def paths(o,path=()):
    if type(o) is dict:items=o.items()
    elif type(o) is list:items=enumerate(o)
    else:return
    for k,v in items:
        if not path and k=='utc':continue
        yield path+(k,),v
        yield from paths(v,path+(k,))
def alter(path,v):
    b=copy.deepcopy(base);at(b,path[:-1])[path[-1]]=v;return b
for path,v in paths(base):
    name='/'.join(map(str,path));b=copy.deepcopy(base);del at(b,path[:-1])[path[-1]];guard('delete '+name,b)
    guard('type-null '+name,alter(path,None))
    if type(v) is float:
        for label,bad in [('NaN',float('nan')),('+inf',float('inf')),('-inf',-float('inf')),('gross perturbation',v+1.0)]:guard(label+' '+name,alter(path,bad))
        if mod.float_policy(path)[2]=='exact_float':guard('one-ulp input '+name,alter(path,math.nextafter(v,math.inf)))
    elif type(v) in (str,int):guard('exact mutation '+name,alter(path,'changed' if type(v) is str else v+1))
b=copy.deepcopy(base);b['utc']='ignored';guard('utc-only',b,True);del b['utc'];guard('utc absent',b,True)
b=copy.deepcopy(base);b['extra']=0;guard('extra root',b)
b=copy.deepcopy(base);b['constant_float_checks'][0]['extra']=0;guard('extra nested',b)
for sign in (-1,1):
    b=copy.deepcopy(base);r=b['finite_covariance_identity_float_cross_checks'][0]
    r['direct']+=sign*mod.COVARIANCE_ABS_TOL;r['grouped']=r['direct'];r['difference']=0.0
    guard('absolute boundary '+str(sign),b,True)
    r['direct']=r['grouped']=math.nextafter(r['direct'],math.inf if sign>0 else -math.inf);guard('absolute next outside '+str(sign),b)
    old=base['L1_fthird_numeric'];v=old/(1-sign*mod.DERIVED_REL_TOL)
    while abs(v-old)>mod.DERIVED_REL_TOL*max(abs(v),abs(old)):v=math.nextafter(v,old)
    outside=math.nextafter(v,math.inf if sign>0 else -math.inf)
    need(abs(outside-old)>mod.DERIVED_REL_TOL*max(abs(outside),abs(old)),'Relative adjacent boundary')
    guard('relative last inside '+str(sign),alter(('L1_fthird_numeric',),v),True)
    guard('relative adjacent outside '+str(sign),alter(('L1_fthird_numeric',),outside))
guard('within-tolerance inconsistent residual',alter(('finite_covariance_identity_float_cross_checks',0,'difference'),mod.COVARIANCE_ABS_TOL/2))
for i in range(len(base['constant_float_checks'])):
    for key in ('D_H','Pbar_f','Pbar_g','c_H'):
        for v in (0.0,-1.0):guard('nonpositive '+str(i)+'/'+key+'/'+str(v),alter(('constant_float_checks',i,key),v))
guard('pairing tozero',alter(('exact_area_pairing',),'0'))
tex=(ROOT/'paper.tex').read_text();q=(ROOT/'custody/ROOT_CURRENT_SOURCE_QUALIFICATION.md').read_text();add=(ROOT/'custody/ROOT_SOURCE_VERSION_ADDENDUM_20261014.md').read_text()
mod.source_guard(tex,q,add);sourcefaults=[]
for label,t,qq,aa in [('conjugation',tex.replace(r'\overline{\widehat h(\xi)}',r'\widehat h(\xi)'),q,add),('source-version',tex,q,add.replace('Eq30','removed')),('convergence',tex,q.replace('little-o','removed'),add)]:
    try:mod.source_guard(t,qq,aa)
    except RuntimeError as e:sourcefaults.append({'label':label,'rejected':True,'reason':str(e)})
    else:raise RuntimeError('Source escaped '+label)
dump(D/('GUARDS_'+tag+'.json'),{'coverage':coverage,'faults':faults,'source_faults':sourcefaults})
out=S/('checker-'+tag);command('clean documented checker',[ROOT/'scripts/check.py','--out',out])
receipt=json.loads((out/'CHECK_RECEIPT.json').read_text())
for mode in ('normal','optimized'):
    actual=json.loads((out/mode/'FINITE_CHECKS.json').read_text());mod.result_guard(actual,base);dump(D/('RESULT_'+tag+'_'+mode+'.json'),actual)
need(mod.canonical(json.loads((out/'normal/FINITE_CHECKS.json').read_text()))==mod.canonical(json.loads((out/'optimized/FINITE_CHECKS.json').read_text())),'Runtime modes differ')
command('clean default absent bindings',[ROOT/'scripts/verify_package.py'])
command('canonical current strict default bindings',[P/'scripts/verify_package.py'])
command('explicit valid required binding',[ROOT/'scripts/verify_package.py','--require-bindings','--bindings',P/'UPLOAD_BINDINGS.json','--archive',P/ZIP])
missing=S/('missing-binding-'+tag)
command('optional missing binding',[ROOT/'scripts/verify_package.py','--bindings',missing])
command('required missing binding',[ROOT/'scripts/verify_package.py','--require-bindings','--bindings',missing],-1)
rebuilt=S/('rebuilt-'+tag+'.zip');command('documented deterministic build',[ROOT/'scripts/build_archive.py','--out',rebuilt]);need(rebuilt.read_bytes()==(P/ZIP).read_bytes(),'Rebuild mismatch')
binding=json.loads((P/'UPLOAD_BINDINGS.json').read_text());badbind=S/('binding-'+tag+'.json')
for kind in ('PDF','ZIP','manifest','malformed','missing-archive','symlink'):
    b=copy.deepcopy(binding)
    if kind=='PDF':b['pdf']['sha256']='0'*64
    elif kind=='ZIP':b['archive']['sha256']='0'*64
    elif kind=='manifest':b['manifest_sha256']='0'*64
    if kind=='malformed':badbind.write_text('{')
    elif kind=='symlink':badbind.symlink_to(P/'UPLOAD_BINDINGS.json')
    else:dump(badbind,b)
    command('strict reject '+kind,[ROOT/'scripts/verify_package.py','--bindings',badbind,'--archive',S/'missing-archive' if kind=='missing-archive' else P/ZIP],-1);badbind.unlink()
mp=ROOT/'PACKAGE_MANIFEST.json';mb=mp.read_bytes();manifest=json.loads(mb)
sp=ROOT/'PORTABILITY_REPAIR_STATUS.json';sb=sp.read_bytes();status=json.loads(sb)
def coherent(name):
    m=copy.deepcopy(manifest);r=next(r for r in m['members'] if r['path']==name);r.update(bytes=(ROOT/name).stat().st_size,sha256=sha(ROOT/name));dump(mp,m)
for key,bad in [('state','READY'),('fresh_whole_package_reviews_completed',2),('minimum_fresh_reviews_required',1),('new_complete_whole_review_required',3),('new_complete_whole_review_completed',True),('latest_complete_review_findings',{'P0':0,'P1':0,'P2':0,'P3':0}),('bounded_repair_findings_fixed',[]),('root_repair_adoption_required',False),('root_terminal_adoption_required',False),('publication_ready',True),('issues_resolved',True),('published',True),('services_held_after_pr',1033),('source_evidence','CASE_ALIAS_SOURCE_EVIDENCE.json')]:
    b=copy.deepcopy(status);b[key]=bad;dump(sp,b);coherent('PORTABILITY_REPAIR_STATUS.json');command('semantic status '+key,[ROOT/'scripts/verify_package.py'],-1);sp.write_bytes(sb);mp.write_bytes(mb)
alias=S/'CLEANPACKAGE';need(alias.samefile(ROOT),'Case identity premise')
case={'canonical':str(ROOT),'alias':str(alias),'samefile':True,'canonical_resolve':str(ROOT.resolve()),'alias_resolve':str(alias.resolve()),'device':ROOT.stat().st_dev,'inode':ROOT.stat().st_ino}
canary=S/('canary-'+tag);canary.write_text('unchanged\n');cb=canary.read_bytes()
sentinel=S/('sentinel-'+tag);mark=S/('compiler-would-run-'+tag)
sentinel.write_text('#!/bin/sh\n: > '+"'"+str(mark)+"'"+'\nexit 91\n');sentinel.chmod(0o700)
existing=S/('existing-'+tag);existing.mkdir()
link=S/('link-'+tag);link.symlink_to(canary);dangling=S/('dangling-'+tag);dangling.symlink_to(S/'no-such-leaf');hard=S/('hard-'+tag);os.link(canary,hard)
parentlink=S/('parentlink-'+tag);parentlink.symlink_to(S,target_is_directory=True)
targets=[('internal',ROOT/('forbidden-'+tag)),('case alias',alias/('forbidden-'+tag)),('nested alias',alias/'CUSTODY'/('forbidden-'+tag)),('multilevel internal',alias/'absent-one/absent-two'/('forbidden-'+tag)),('traversal',S/'..'/S.name/('traversal-'+tag)),('existing file',canary),('existing dir',existing),('symlink',link),('dangling',dangling),('hardlink',hard),('symlink parent',parentlink/('forbidden-'+tag)),('absent parent',S/'absent-parent'/('forbidden-'+tag))]
def writer(name,target,root=ROOT):
    args=[root/'scripts'/name,'--out',target]
    if name=='build_pdf.py':args+=['--tectonic',sentinel]
    return args
for script in ('check.py','build_archive.py','build_pdf.py'):
    for label,target in targets:
        command(script+' reject '+label,writer(script,target),-1);need(not mark.exists() and canary.read_bytes()==cb,'Rejected writer side effect')
    command(script+' reversed alias spelling',writer(script,ROOT/('reverse-'+tag),alias),-1);need(not mark.exists(),'Reverse compiler side effect')
children=['normal/original_finite_checks.py','normal/FINITE_CHECKS.json','normal/stdout.txt','normal/stderr.txt','optimized/original_finite_checks.py','optimized/FINITE_CHECKS.json','optimized/stdout.txt','optimized/stderr.txt','CHECK_RECEIPT.json','paper.tex','paper.pdf','paper.log','compile.stdout.txt','compile.stderr.txt']
for i,child in enumerate(children):
    target=S/('reused-'+tag+'-'+str(i));leaf=target/child;leaf.parent.mkdir(parents=True);leaf.symlink_to(canary)
    command('child canary '+child,writer('check.py' if i<9 else 'build_pdf.py',target),-1);need(canary.read_bytes()==cb and not mark.exists(),'Child alias side effect')
safezip=S/('alias-safe-'+tag+'.zip');command('safe alias-root archive',writer('build_archive.py',safezip,alias));need(safezip.read_bytes()==(P/ZIP).read_bytes(),'Alias ZIP')
pdfout=S/('sentinel-positive-'+tag);command('safe PDF reaches sentinel without compile',writer('build_pdf.py',pdfout),91);need(mark.is_file(),'Sentinel positive not reached');mark.unlink()
held=S/('held-manifest-'+tag);held.write_bytes(mb)
for kind in ('identical-symlink','malformed-symlink','directory'):
    mp.unlink()
    if kind=='directory':mp.mkdir()
    else:held.write_bytes(mb if kind=='identical-symlink' else b'{');mp.symlink_to(held)
    target=S/('bootstrap-'+kind+'-'+tag+'.zip')
    command('bootstrap '+kind+' verify',[ROOT/'scripts/verify_package.py'],-1);command('bootstrap '+kind+' build',writer('build_archive.py',target),-1);need(not target.exists(),'Bootstrap wrote output')
    if kind=='directory':mp.rmdir()
    else:mp.unlink()
    mp.write_bytes(mb)
paper=ROOT/'paper.tex';pb=paper.read_bytes();paper.unlink();paper.symlink_to(P/'paper.tex');command('member symlink',[ROOT/'scripts/verify_package.py'],-1);paper.unlink();paper.write_bytes(pb)
for r in manifest['members']:need((ROOT/r['path']).stat().st_size==r['bytes'] and sha(ROOT/r['path'])==r['sha256'],'Clean extraction restore '+r['path'])
need(mp.read_bytes()==mb,'Manifest restore')
dump(D/('CONTROLS_'+tag+'.json'),{'utc':now(),'status':'PASS','runtime':sys.version,'wrapper_optimized':not __debug__,'coverage':coverage,'guard_controls':len(faults),'source_controls':sourcefaults,'actual_checker_receipt':receipt,'case_identity':case,'actual_commands':len(commands),'all_clean_members_restored_exact':True,'canary_unchanged':True,'compiler_sentinel_positive':True,'actual_PDF_compile':False,'meaning':'Finite support controls; not whole04 or interval/universal certificate.'})
print(json.dumps({'tag':tag,'status':'PASS','commands':len(commands),'guard_controls':len(faults),'coverage':coverage}))

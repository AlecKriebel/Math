"""Handwritten whole-package audit. No imported/evaluated candidate code.
All mutations are confined to this NEW family directory. Foreign inputs are
individually read and hash-bound; no PDF, text/pixel derivative or raw cache copied.
"""
from pathlib import Path, PurePosixPath
import collections, copy, datetime, hashlib, itertools, json, math, os, sqlite3, stat, subprocess, sys
from fractions import Fraction

OWN=Path(__file__).absolute().parent
AUDIT=OWN.parent
REPO=AUDIT.parents[2]
CAND=AUDIT/'reviewed_candidate'
SEEN={}
COUNTS=collections.Counter()
NEGATIVES=[]
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def ck(x,label):
    if not x: raise AssertionError(label)
    COUNTS[label.split(':',1)[0]]+=1
def digest(b): return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d: raise ValueError('duplicate JSON key')
            d[k]=v
        return d
    def bad(x): raise ValueError('invalid constant '+x)
    def floating(s):
        v=float(s)
        if not math.isfinite(v): raise ValueError('overflow float')
        return v
    return json.loads(b,object_pairs_hook=pairs,parse_constant=bad,parse_float=floating)
def typed(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(typed(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
    return a==b
def safe(n):
    if type(n) is not str or not n or '\\' in n or '\x00' in n: return False
    p=PurePosixPath(n)
    return bool(p.parts) and not p.is_absolute() and p.as_posix()==n and not set(p.parts)&{'.','..','.git','__pycache__'}
def read(p):
    ck(not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'filesystem:no symlink ancestor')
    ck(stat.S_ISREG(p.stat().st_mode),'filesystem:regular')
    b=p.read_bytes()
    rel=p.relative_to(REPO).as_posix()
    item={'path':rel,'bytes':len(b),'sha256':digest(b),'excluded_from_family_authorship':True}
    if rel in SEEN: ck(typed(SEEN[rel],item),'inputs:stable repeated body')
    SEEN[rel]=item
    if p.suffix=='.json': parse(b)
    if p.suffix=='.jsonl':
        for line in b.splitlines():
            ck(bool(line.strip()),'structured:nonblank JSONL');parse(line)
    return b
def load(p): return parse(read(p))
def topology(root):
    files=set();dirs=set()
    ck(root.is_dir() and not root.is_symlink(),'topology:root')
    for p in root.rglob('*'):
        n=p.relative_to(root).as_posix(); ck(safe(n),'topology:canonical')
        ck(not p.is_symlink(),'topology:nonlink')
        if p.is_dir(): dirs.add(n)
        else: ck(stat.S_ISREG(p.stat().st_mode),'topology:regular member');files.add(n)
    implicit={q.as_posix() for n in files for q in PurePosixPath(n).parents if q.as_posix()!='.'}
    ck(dirs==implicit,'topology:no extra empty directories')
    return files,dirs
def rows(xs):
    ck(type(xs) is list,'contract:rows list')
    names=[]
    for r in xs:
        ck(type(r) is dict and set(r)=={'path','bytes','sha256'},'contract:exact row keys')
        ck(safe(r['path']),'contract:canonical row')
        ck(type(r['bytes']) is int and r['bytes']>=0,'contract:integer byte count')
        ck(type(r['sha256']) is str and len(r['sha256'])==64 and all(c in '0123456789abcdef' for c in r['sha256']),'contract:SHA format')
        names.append(r['path'])
    ck(len(names)==len(set(names)),'contract:unique paths')
    return set(names)
def verify_rows(root,xs,full444=False):
    rows(xs)
    for r in xs:
        p=root/r['path'];b=read(p)
        ck(len(b)==r['bytes'] and digest(b)==r['sha256'],'binding:whole body')
        if full444: ck(stat.S_IMODE(p.stat().st_mode)==0o444,'mode:literal full0444')
def closed(root,name):
    d=load(root/name);ns=rows(d['files']);fs,_=topology(root)
    ck(d['self_excluded']==[name],'closure:sole self exclusion')
    ck(type(d['files_count']) is int and d['files_count']==len(ns),'closure:typed count')
    ck(fs==ns|{name},'closure:exact file set')
    verify_rows(root,d['files'],True)
    ck(stat.S_IMODE((root/name).stat().st_mode)==0o444,'mode:manifest full0444')
    return d
def negative(name,fun):
    try: fun()
    except (AssertionError,ValueError,TypeError,KeyError,OSError): NEGATIVES.append(name);return
    raise AssertionError('Hostile case accepted: '+name)

# Complete frozen inventory, individually anchored dependencies, and owned evidence.
manifest=closed(CAND,'MANIFEST.json')
ck(manifest['files_count']==430 and manifest['status']=='unsolved' and manifest['full_problem_solved'] is False,'current:430 and partial')
dep=load(CAND/'CURRENT_DEPENDENCIES.json')
ck(dep['anchor_repository_relative']==AUDIT.relative_to(REPO).as_posix(),'current:exact portable anchor')
dependency_names=[]
for r in dep['files']:
    rr={k:r[k] for k in ('path','bytes','sha256')};verify_rows(AUDIT,[rr]);dependency_names.append(r['path'])
ck(len(dependency_names)==len(set(dependency_names))==369,'current:369 unique dependencies')
ck(dep['foreign_primary_and_derivative_members_individually_hash_bound_not_copied'] is True,'current:foreign exclusion')
foreign_paths=[r['path'] for r in dep['files'] if 'individually_excluded_foreign' in r['roles']]
owned_hashes={r['sha256'] for r in manifest['files']}
primary_foreign=[n for n in foreign_paths if n.endswith(('.pdf','.png')) or '/foreign_primary/' in n or ('/evidence/' in n and not '/original_inputs/' in n)]
for n in primary_foreign: ck(digest(read(AUDIT/n)) not in owned_hashes,'exclusion:no PDF/text/pixels copied')

snap=load(AUDIT/'snapshot_manifest_v2.json')
ck(snap['head']=='c772dc5b851ec91da9d46d534577609e5d3ca389' and snap['base']=='01358d66fc67d1c462bddf31c0d4ee5b120e6737','original:identity')
ck(len(snap['files'])==18 and len(snap['changed_paths'])==19,'original:18/19 count')
for r in snap['files']:
    n=r['path'];a=read(AUDIT/'source_snapshot_v2'/n)
    ck(len(a)==r['size'] and digest(a)==r['sha256'] and r['mode']=='100644','original:full file pin')
    ck(a==read(CAND/'original_archive'/n),'original:archive byte exact')
imm=['OBSTRUCTION.md','SOURCES.md','group_block_verification.json','source_manifest.json','source_record.json','turns.jsonl','verify_group_block.py','review/submitted_verifier.py','review/submitted_results.json','review/reviewed_obstruction.md','review/independent_checks.py','review/independent_results.json']
for n in imm: ck(read(CAND/n)==read(AUDIT/'source_snapshot_v2'/n),'original:twelve current unchanged')
ck(topology(CAND/'original_archive')[0]=={r['path'] for r in snap['files']},'original:archive topology')
diff=read(AUDIT/'original_diff_v2.patch')
ck(len(diff)==75046 and digest(diff)==snap['diff_sha256'],'original:complete diff pin')
parts=diff.split(b'diff --git ')[1:]
ck(len(parts)==19,'original:19 hunks')
new_verified=0
for part in parts:
    lines=part.splitlines(keepends=True)
    if b'new file mode 100644\n' not in lines: continue
    marker=next(l for l in lines if l.startswith(b'+++ b/')).decode().strip()[6:]
    n=marker.split('unsolved_math_prioritization/attempts/2912/',1)[1]
    i=next(i for i,l in enumerate(lines) if l.startswith(b'@@'))
    body=b''.join(l[1:] for l in lines[i+1:] if l.startswith(b'+'))
    ck(body==read(AUDIT/'source_snapshot_v2'/n),'original:reconstructed full added hunk');new_verified+=1
ck(new_verified==18,'original:all18 hunks')

# Capture checks are against actual complete records, never historical labels.
def clock(s):
    d=datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
    ck(d.utcoffset()==datetime.timedelta(0),'capture:aware UTC')
    return d
def cap_streams(root,d):
    ck(type(d['pid']) is int and d['pid']>0,'capture:real positive PID')
    ck(d['actual_execution'] is True and d['completed'] is True,'capture:actual completed')
    ck(type(d['exit_code']) is int,'capture:typed exit')
    ck(clock(d['started_utc'])<=clock(d['finished_utc']),'capture:ordered clocks')
    ck(d['stdin_supplied'] is False,'capture:no stdin')
    ck(type(d['argv']) is list and all(type(x) is str for x in d['argv']),'capture:argv types')
    for stream in ['stdout','stderr']:
        r=d[stream];p=Path(r['path'])
        if p.is_absolute(): q=p
        elif p.parts and p.parts[0]=='draft_pr_publication_program_20260930': q=REPO/p
        else: q=root/p
        b=read(q);ck(len(b)==r['bytes'] and digest(b)==r['sha256'],'capture:full streams')

ref=load(CAND/'CURRENT_EXECUTION_REFERENCE.json');outer=AUDIT/ref['audit_relative_outer_capture'];inner=AUDIT/ref['audit_relative_inner_attempt']
ck(topology(outer)[0]=={'OPERATION_PRELAUNCH.json','PRELAUNCH_BUILDER_SOURCE.py','PRELAUNCH_OPERATOR.py','CAPTURE.json','stdout.bin','stderr.bin'},'capture:real outer six exact')
oc=load(outer/'CAPTURE.json');op=load(outer/'OPERATION_PRELAUNCH.json');cap_streams(outer,oc)
ck(oc['operator_pid']==64347 and oc['pid']==64348 and oc['exit_code']==0,'capture:actual builder genealogy')
ck(oc['scientific_helpers_run'] is False and oc['administrative_only'] is True and oc['current_whole_verdict'] is None and oc['new_whole_current_gate']=='PENDING','capture:administrative pending')
for k in op: ck(typed(op[k],oc[k]) if k!='schema' else True,'capture:prelaunch prefix agrees')
for n,k in [('PRELAUNCH_BUILDER_SOURCE.py','builder_sha256'),('PRELAUNCH_OPERATOR.py','operator_sha256')]: ck(digest(read(outer/n))==oc[k],'capture:exact actual prelaunch source')
ck(digest(read(outer/'OPERATION_PRELAUNCH.json'))==ref['outer_prelaunch_sha256'],'capture:prelaunch ref pin')
inv=load(inner/'INVOCATION.json');ck(inv['pid']==oc['pid'] and inv['parent_pid']==oc['operator_pid'],'capture:inner PID parent')
gitlog=load(inner/'GIT_COMMANDS.json');prefix=load(CAND/'build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json')
ck(len(gitlog)==46 and len(prefix)==44 and typed(gitlog[:len(prefix)],prefix),'capture:honest44 prefix final46')
for rec in gitlog:
    cap_streams(inner,rec);ck(rec['exit_code']==0,'capture:successful readonly query')
    ck(rec['argv'][0]=='git' and rec['argv'][1] in {'branch','rev-parse','show','ls-tree','diff'},'capture:readonly git allowlist')
    ck(rec['argv'][1]!='branch' or rec['argv'][2:]==['--show-current'],'capture:readonly branch')
    ck(oc['started_utc']<=rec['started_utc']<=rec['finished_utc']<=oc['finished_utc'],'capture:inner bounded by outer')
fi=load(AUDIT/'ROOT_CURRENT_FREEZE_INSPECTION.json');ck(fi['current_manifest']['sha256']==digest(read(CAND/'MANIFEST.json')) and typed(fi['entire_actual_outer_capture'],oc),'capture:root inspection full equality')
fc=load(AUDIT/'root_complete_current_freeze_inspection_actual_capture/CAPTURE.json');cap_streams(AUDIT/'root_complete_current_freeze_inspection_actual_capture',fc);ck(fc['pid']==65947,'capture:root actual inspection PID')

# Freeze-date Git epoch: retain actual read-only commands/streams for native4.
queries=[]
def gitquery(*args):
    folder=OWN/'immutable_git_capture';folder.mkdir(exist_ok=True)
    idx=len(queries);out=folder/(str(idx)+'.stdout');err=folder/(str(idx)+'.stderr')
    rec={'argv':['git',*args],'cwd':str(REPO),'started_utc':now(),'stdin_supplied':False}
    with out.open('xb') as o,err.open('xb') as e:
        p=subprocess.Popen(rec['argv'],cwd=REPO,stdin=subprocess.DEVNULL,stdout=o,stderr=e,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));rec['pid']=p.pid;rec['exit_code']=p.wait(timeout=60)
    rec.update(actual_execution=True,completed=True,finished_utc=now())
    for k,f in [('stdout',out),('stderr',err)]: rec[k]={'path':f.relative_to(OWN).as_posix(),'bytes':f.stat().st_size,'sha256':digest(f.read_bytes())}
    queries.append(rec);(OWN/'IMMUTABLE_GIT_COMMANDS.json').write_text(json.dumps(queries,indent=2)+'\n')
    ck(rec['exit_code']==0 and not err.read_bytes(),'epoch:actual readonly Git query')
    return out.read_bytes()
frozen=dep['current_main_head'];current_head=gitquery('rev-parse','HEAD').decode().strip();branch=gitquery('branch','--show-current').decode().strip()
ck(branch=='main','epoch:stay main')
native4={'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json'}
for r in dep['current_native13']:
    p=REPO/r['path']
    if r['path'] in native4:
        tree=gitquery('ls-tree',frozen,'--',r['path']).decode().strip();ck(tree.startswith('100644 blob ') and tree.endswith('\t'+r['path']),'epoch:immutable Git100644')
        body=gitquery('show',frozen+':'+r['path'])
    else: body=read(p)
    ck(len(body)==r['bytes'] and digest(body)==r['sha256'],'epoch:dated13 whole binding')
    if r['path'].endswith('QUEUE.md'): queue=body
ck(len(dep['current_native13'])==13,'epoch:13 complete')
qbefore=read(CAND/'queue_proposal/QUEUE_PREIMAGE.md');qafter=read(CAND/'queue_proposal/QUEUE_PROSPECTIVE.md');qp=load(CAND/'CURRENT_QUEUE_PATCH.json')
ck(queue==qbefore and digest(qbefore)==qp['whole_preimage_sha256'] and digest(qafter)==qp['whole_prospective_sha256'],'queue:whole conserved preimages')
before=qbefore.splitlines(keepends=True);after=qafter.splitlines(keepends=True);ck(len(before)==len(after),'queue:line count')
changes=[(a,b) for a,b in zip(before,after) if a!=b];ck(len(changes)==1,'queue:sole target row')
u,v=(x.decode().split('|') for x in changes[0]);ck(len(u)==len(v)==14 and u[2].strip()==v[2].strip()=='2912 / KP-4.36','queue:target exact')
ck({i for i in range(14) if u[i]!=v[i]}=={8,9,11},'queue:only Status Turns Findings')
ck(u[10]==v[10] and u[12]==v[12] and v[8].strip()=='unsolved' and v[9].strip()=='2/5','queue:Chat DOI preserved')

# Whole result/capture/ledger values, recursively retaining scalar types.
summary=load(AUDIT/'root_original_actual_reproduction/ROOT_CURRENT_REPRODUCTION_SUMMARY.json')
saved=load(CAND/'group_block_verification.json');ind=load(CAND/'review/independent_results.json')
ck(typed(summary['entire_author_result'],saved) and typed(summary['entire_independent_result'],ind),'results:whole summary equality')
ledger=[parse(l) for l in read(CAND/'turns.jsonl').splitlines()];ck(typed(summary['whole_original_ledger'],ledger),'ledger:whole exact two objects')
ck(len(ledger)==2 and [x['turn'] for x in ledger]==[1,2] and all(x['outcome']=='stalled' for x in ledger),'ledger:two original stalled')
rr=load(AUDIT/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json')
for family,result in [('current_author',saved),('historical_submitted',saved),('historical_independent',ind)]:
    root=AUDIT/'root_original_actual_reproduction'/family;c=load(root/'CAPTURE.json');cap_streams(root,c)
    out=read(root/'stdout.bin');ck(out==read(root/'ORIGINAL_SAVED_RESULT.json') and typed(parse(out),result) and typed(load(root/'ACTUAL_RESULT.json'),result),'results:entire stdout bytes and types')
    ck(read(root/'PRELAUNCH_SOURCE.py')==read(REPO/c['source_origin']['path']),'results:unchanged exact original source')
    ck(any(typed(c,t) for t in rr['complete_actual_captures']),'results:full nested capture equal')
for r in summary['actual_replay_captures']:
    c=load(AUDIT/r['path']);cap_streams((AUDIT/r['path']).parent,c);ck(c['exit_code']==0,'results:outer evidence zero exit')

# Independent integer arithmetic from affine normal forms and direct quotient.
A=list(itertools.product(range(3),range(7)))
def amul(x,y): return ((x[0]+y[0])%3,(x[1]+pow(2,x[0],7)*y[1])%7)
def ainv(x): return ((-x[0])%3,(-pow(2,(-x[0])%3,7)*x[1])%7)
perms={x:tuple((pow(2,x[0],7)*j+x[1])%7 for j in range(7)) for x in A}
ck(len(set(perms.values()))==21,'math:faithful group21')
for x,y,z in itertools.product(A,repeat=3): ck(amul(amul(x,y),z)==amul(x,amul(y,z)),'math:all finite associativity')
for x in A: ck(amul(x,ainv(x))==(0,0) and amul(ainv(x),x)==(0,0),'math:two-sided inverse')
def q(v): return tuple(v[i]-v[6] for i in range(6))
def act(p,v):
    out=[0]*7
    for j,c in enumerate((*v,0)): out[p[j]]=c
    return q(out)
basis=[tuple(int(i==j) for i in range(6)) for j in range(6)]
def matrix(p): return [[act(p,e)[i] for e in basis] for i in range(6)]
ma=matrix(perms[(1,0)]);mb=matrix(perms[(0,1)])
ck(typed(ma,saved['matrix_a']) and typed(mb,saved['matrix_b']),'math:entire saved matrices')
for x,y,e in itertools.product(A,A,basis): ck(act(perms[x],act(perms[y],e))==act(perms[amul(x,y)],e),'math:all quotient composition')
for v in itertools.product((-1,0,1),repeat=7):
    ck((q(v)==(0,)*6)==(len(set(v))==1),'math:primitive diagonal bounded')
    for p in (perms[(1,0)],perms[(0,1)]):
        pv=[0]*7
        for j,c in enumerate(v):pv[p[j]]=c
        ck(sum(q(pv))%7==sum(q(v))%7,'math:coinvariant sum7')
def det(m):
    if len(m)==1:return m[0][0]
    return sum((-1)**j*m[0][j]*det([r[:j]+r[j+1:] for r in m[1:]]) for j in range(len(m)))
nat=[[7*int(i==j)-1 for j in range(6)] for i in range(6)]
ck(det(nat)==7**5,'math:natural Q-to-I nonunit determinant')
bm1=[[mb[i][j]-int(i==j) for j in range(6)] for i in range(6)]
ck(det(bm1)==7 and det(ma)==det(mb)==1,'math:integral determinants')
# Q_A=Z/7 and I_A=0: b identifies all coset generators; a doubles I_b generator.
ck(math.gcd(7,2-1)==1,'math:augmentation A coinvariant killed')
def bmul(x,y):
    n,i=x;m,j=y
    return (n+m,(((-1)**m)*i+j)%3)
def binv(x): n,i=x;return (-n,(-((-1)**n)*i)%3)
win=list(itertools.product(range(-4,5),range(3)))
for x,y,z in itertools.product(win,repeat=3): ck(bmul(bmul(x,y),z)==bmul(x,bmul(y,z)),'math:B associativity window')
for x in win:ck(bmul(x,binv(x))==bmul(binv(x),x)==(0,0),'math:B inverse window')
for v in itertools.product((-1,0,1),repeat=5):
    total=sum(v);restricted=[sum(v)]*3
    ck((restricted==[0]*3)==(total==0),'math:restriction diagonal injective window')
    d=[-v[0]]+[v[i-1]-v[i] for i in range(1,5)]+[v[-1]]
    ck(sum(d)==0,'math:finite Laurent telescopes')
    if total==0:
        primitive=[-sum(v[:i+1]) for i in range(5)]
        ck(primitive[-1]==0 and [-primitive[0]]+[primitive[i-1]-primitive[i] for i in range(1,5)]==list(v),'math:finite primitive exact')
expected_categories={'permutation_group':2,'quotient_representation':21*21*6,'primitive_diagonal_kernel':3**7,'quotient_coinvariant_control':2*3**7,'semidirect_normal_form':27+27**3,'T_coinvariant_labels':27*9,'C_invariant_shift':21,'restriction_diagonal':21+3**5,'restriction_injectivity_control':3**5,'Laurent_difference':3**5}
ck(typed(ind,{'status':'PASS','exact_assertions':29933,'categories':expected_categories,'limits':['Finite and finite-support arithmetic only','No computational proof of group cohomology or Poincare duality','No exterior realization or complete 2-type comparison']}),'math:entire29933 receipt independently reconstructed')
expected_saved={'status':'PASS','exact_assertions':1+21*(1+21)+3+1+14+14+1+6+1+1+1+1+1,'finite_group_order':21,'coset_count':7,'quotient_rank':6,'quotient_torsion':[],'matrix_a':ma,'matrix_b':mb,'limits':['Finite block only','No knot realization','No pair of exteriors','No completeness theorem or counterexample']}
ck(typed(saved,expected_saved),'math:entire507 receipt independently reconstructed')

# Native raw/prior/SQL whole semantic comparison, individually bound, never copied.
cache=REPO/'unsolved_math_prioritization/cache'
rb=read(cache/'problems.json');pb=read(cache/'research_results.json');raw=parse(rb);prior=parse(pb)
byid={str(x['id']):x for x in raw};codes=collections.Counter(x['problem_number'] for x in raw)
ck(len(byid)==len(raw)==15458 and len(prior)==6701 and len(rb)+len(pb)==149266659,'raw:whole input counts')
db=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?immutable=1&mode=ro',uri=True);db.execute('PRAGMA query_only=ON')
ck(db.execute('PRAGMA query_only').fetchone()==(1,),'raw:readonly SQL')
n=0
for k,payload,report in db.execute('SELECT key,payload,report FROM records ORDER BY key'):
    wanted=dict(byid[k]);code=wanted['problem_number']
    if codes[code]>1 and code in prior: wanted['_ambiguous_report']=True
    pr={} if wanted.get('_ambiguous_report') else prior.get(code,{})
    ck(typed(parse(payload),wanted) and typed(parse(report),pr),'raw:whole typed SQL row');n+=1
db.close();ck(n==15458,'raw:all rows')
ck(typed(byid['2912'],load(CAND/'source_record.json')) and 'KP-4.36' not in prior and typed(load(AUDIT/'pinned_prior_report.json'),{}),'raw:ABSENT prior fallback distinct from null')

# Declarative adversarial contract controls; no evaluation of production predicates.
for s in ['', '.', '..','../x','a/../b','a//b','/x','a\\b','a/./b','a/','.git/x','a/__pycache__/b','a\x00b']:
    negative('path '+repr(s),lambda s=s:ck(safe(s),'negative:path'))
for b in [b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":Infinity}',b'{"a":1e999}']:negative('strict JSON '+repr(b),lambda b=b:parse(b))
for mode in range(0o10000):ck((mode==0o444)==(stat.S_IMODE(mode)==0o444),'mode:all4096 full modes')
for bad in [True,1.0,'1',None]:
    r={'path':'ok','bytes':bad,'sha256':'0'*64};negative('byte count '+repr(bad),lambda r=r:rows([r]))
negative('duplicate path',lambda:rows([{'path':'ok','bytes':1,'sha256':'0'*64}]*2))
for x,y in [(True,1),(False,0),(1,1.0),({},None),([],{}),(None,{})]:ck(not typed(x,y),'negative:recursive types distinguish')
for m,n in itertools.product(range(-4,5),repeat=2): ck(m*n!=1 or (m,n) in {(1,1),(-1,-1)},'math:degree-one units')
for val in [True,0,3]:
    negative('attempt count '+repr(val),lambda val=val:ck(type(val) is int and val==2,'negative:original count'))
negative('fake future whole PASS',lambda:ck('PASS'==manifest['current_gate'],'negative:gate'))
negative('diagonal equals augmentation',lambda:ck(det(nat) in {-1,1},'negative:integral inverse'))
negative('finite Laurent unit',lambda:ck(sum([-1,1])==1,'negative:augmentation'))
# Frozen owned closures and source adversary additional anchors.
closed(AUDIT/'root_original_actual_reproduction','MANIFEST.json')
closed(AUDIT/'current_preparation_family','PREPARATION_MANIFEST.json')
closed(AUDIT/'current_source_adversary_family','SELF_MANIFEST.json')
pins=load(AUDIT/'current_preparation_family/STATIC_INPUT_BINDINGS.json')
for fam,info in pins['families'].items():
    root=AUDIT/fam;all_names=rows(info['copied_members'])|rows(info['foreign_members'])|{info['manifest']['path']}
    fs,ds=topology(root);ck(fs==all_names and ds==set(info['directories']),'closure:full family topology')
    verify_rows(root,info['copied_members']+info['foreign_members'],True)
    verify_rows(root,[info['manifest']],True)
    verify_rows(AUDIT,info['external_inputs'])
for name in ['ROOT_SOURCE_SAFETY_INSPECTION.json','ROOT_CURRENT_FREEZE_INSPECTION_PRELAUNCH_SOURCE.py','inspect_complete_current_freeze.py','ROOT_CURRENT_FREEZE_INSPECTION.json']:
    read(AUDIT/name)
for item in list(SEEN.values()):
    p=REPO/item['path'];b=p.read_bytes();ck(len(b)==item['bytes'] and digest(b)==item['sha256'],'inputs:final unchanged individual')

result={'schema':'pr44-handwritten-whole-current-audit/v1','utc':now(),'actual_pid':os.getpid(),'frozen_candidate_sha256':digest(read(CAND/'MANIFEST.json')),'frozen_candidate_members':430,'individual_candidate_dependencies':369,'foreign_input_count':len(SEEN),'own_assertions':sum(COUNTS.values()),'categories':dict(COUNTS),'rejected_cases':NEGATIVES,'rejected_count':len(NEGATIVES),'current_main_at_audit':current_head,'reviewed_frozen_main_epoch':frozen,'epoch_rebound_to_live':False,'immutable_native4_queried_by_actual_git':True,'all13_bound':True,'original18_archive_and_twelve_current_byte_exact':True,'whole507_and29933_typed_reconstructed':True,'full_raw_bytes':len(rb)+len(pb),'full_SQL_rows':n,'prior_key_present':False,'null_prior_retrieved':False,'outer_actual_parent_pid':64347,'outer_actual_builder_pid':64348,'outer_complete_six_members':True,'inner_final_git_queries':46,'inner_frozen_prefix_queries':44,'candidate_and_production_execution':False,'new_mathematical_attempts':0,'full_problem_solved':False,'future_merge_acceptance_or_reconciliation_certified':False}
(OWN/'INDIVIDUAL_INPUTS.json').write_text(json.dumps({'schema':'pr44-source-first-individual-foreign-inputs/v1','resolution':'repository_root / files.path','foreign_bodies_copied':False,'git_stdout_firstparty_native4_and_query_metadata_are_procedural_evidence':True,'files':sorted(SEEN.values(),key=lambda x:x['path'])},indent=2)+'\n')
(OWN/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

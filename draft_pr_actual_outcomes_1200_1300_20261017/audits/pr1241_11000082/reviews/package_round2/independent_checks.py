"""New exact finite controls and independent nested-inventory probes; no live calls."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import copy,datetime,hashlib,json,shutil,subprocess,zipfile
HERE=Path(__file__).resolve().parent;A=HERE.parents[1];S=HERE/'scratch_local'
def need(c,m):
    if not c:raise RuntimeError(m)
def save(n,d):(HERE/n).write_text(json.dumps(d,indent=2)+'\n')
def binding(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def mul(a,b):return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
def inv(a):return (a[3],-a[1],-a[2],a[0])
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
def tr(a):return a[0]+a[3]
def pwr(a,n):
    z=(1,0,0,1)
    while n:
        if n%2:z=mul(z,a)
        a=mul(a,a);n//=2
    return z
def iw(w):return tuple(-x for x in w[::-1])
def reduce(w):
    s=[]
    for x in w:
        if s and x==-s[-1]:s.pop()
        else:s.append(x)
    return tuple(s)
def cyc(w):
    w=reduce(w)
    while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
    return w
def rot(w):
    n=len(w);s=w+w;i,j,t=0,1,0
    while i<n and j<n and t<n:
        if s[i+t]==s[j+t]:t+=1;continue
        if s[i+t]>s[j+t]:i+=t+1;i=i+1 if i==j else i
        else:j+=t+1;j=j+1 if i==j else j
        t=0
    i=min(i,j);return s[i:i+n]
def word(e):
    w=(1,)
    for m,sign in enumerate(e,1):
        u=w if sign==1 else iw(w);v=iw(u)
        w=v+(2,)*(2*m)+u+(2,)*(2*m-1)+v+(2,)*(2*m)+u
    return w
def evaluate(w,a,b):
    lookup={1:a,-1:inv(a),2:b,-2:inv(b)};z=(1,0,0,1)
    for x in w:z=mul(z,lookup[x])
    return z

generic=0;qzero=0
for mu in [F(-3),F(0),F(1),F(2),F(4),F(5,3)]:
    v=(1,0,-mu,1)
    for h,j,l in product(range(-3,4),repeat=3):
        c=mul(mul((1,h,0,1),(1,0,j,1)),(1,l,0,1));p,q,r,s=c;actual=comm(v,c)
        need(actual==(1+mu*q*s,-mu*q*q,mu*(s*s-1)-mu*mu*q*s,1-mu*q*s+mu*mu*q*q),'generic commutator')
        need(tr(actual)==2+mu*mu*q*q,'trace formula');generic+=1
        if q==0:need(tr(actual)==2,'q-zero control');qzero+=1
deep=[]
for mu in [4,6,8,10]:
    v=(1,0,-mu,1);c=(1,mu,0,1)
    for r in range(2,8):
        c=comm(v,c);need(c[1]==-mu**(2**r-1) and tr(c)==2+mu**(2**r),'deep formula')
        selected=None
        for m in range(1,6):
            d=mul(mul(pwr(v,m),c),inv(pwr(v,m)))
            if tr(comm(c,d))!=2:selected=m;break
        need(selected is not None,'disjoint endpoint finite certificate')
        deep.append({'mu':mu,'r':r,'endpoint_M':selected,'criterion':'tr([C,V^M C V^-M]) != 2 excludes a common complex eigenline, hence a shared endpoint','trace_bits':tr(c).bit_length()})
families=[]
reps=[((F(2),F(1,2),F(2),F(1)),(F(3),F(2),F(1),F(1))),((1,0,0,1),(1,0,0,1)),((-1,-4,0,-1),(1,0,-4,1))]
for m in range(1,6):
    ws=[word(e) for e in product((-1,1),repeat=m)];cs=[cyc(w) for w in ws]
    need(len({rot(w) for w in cs})==2**m,'distinct oriented classes')
    for w in cs:
        j=next(i for i,x in enumerate(w) if abs(x)==1);w=w[j:]+w[:j];ys=[];i=0
        while i<len(w):
            if abs(w[i])==2:
                x=w[i];j=i+1
                while j<len(w) and w[j]==x:j+=1
                ys.append((j-i)*(1 if x>0 else -1));i=j
            else:i+=1
        need(ys.count(2*m-1)==1 and -(2*m-1) not in ys and ys.count(4*m)==1,'cyclic markers')
    controls=[]
    for a,b in reps:
        traces={tr(evaluate(w,a,b)) for w in ws};need(len(traces)==1,'universal-trace finite consistency')
        controls.append({'trace_is_2':next(iter(traces))==2,'changed_final_y_detected':tr(evaluate(ws[-1]+(2,),a,b)) not in traces})
    need(any(q['changed_final_y_detected'] for q in controls),'mutated-word control')
    families.append({'m':m,'classes':len(ws),'markers':'PASS','representations':controls})
need(rot(cyc((1,1)))!=rot(cyc((1,1,1))) and rot(cyc((1,)))!=rot(cyc((-1,))),'proper-power and inversion controls')
save('INDEPENDENT_MATH_RESULTS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generic_cases':generic,'q_zero_controls':qzero,'deep_and_endpoint_controls':deep,'word_families':families,'limits':'Finite consistency controls only. mu values here are algebraic inputs; geometric realizability not inferred. Rational/trivial/lift-sign representations challenge the trace claim but cannot prove universality or ambient nonconjugacy. Full written proof reviewed separately.'})

root=S/'archive';z=A/'publication/Johnson_Filtration_Multiplicity_Verification_v1.0.zip'
with zipfile.ZipFile(z) as archive:
    names=archive.namelist();need(len(names)==len(set(names))==105,'ZIP unique inventory')
    manifest=json.loads(archive.read('MANIFEST.json'));need(len(manifest['files'])==104,'root manifest member count')
    for e in manifest['files']:need(binding(archive.read(e['path']))=={'bytes':e['bytes'],'sha256':e['sha256']},'outer binding')
    context=json.loads(archive.read('provenance/CURRENT_PR1241_CONTEXT.json'));reg=context['authored_freezes'];nested=[]
    for spec in reg:
        raw=archive.read(spec['path']);need(hashlib.sha256(raw).hexdigest()==spec['sha256'],'actual family outside anchor');entries=json.loads(raw)[spec['entries_key']]
        for e in entries:need(binding(archive.read(spec['base']+'/'+e[spec['path_key']]))=={'bytes':e['bytes'],'sha256':e['sha256']},'actual family member')
        nested.append({'path':spec['path'],'base':spec['base'],'entries_key':spec['entries_key'],'path_key':spec['path_key'],'count':len(entries)})
    need(len(nested)==7 and sum(e['count'] for e in nested)==53,'seven/53 families')
    snapshot=json.loads(archive.read('provenance/SUBMITTED_SNAPSHOT.json'));blobchecks=[]
    for e in snapshot['files']:
        n=Path(e['path']).name;b=archive.read('original_submitted/'+n)
        need(b==(A/'submitted'/n).read_bytes(),'original source copy')
        need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['blob'],'original Git blob identity');blobchecks.append(n)
        need(archive.read('current_edition/'+n)==(A/'current_edition'/n).read_bytes(),'current source copy')
    for folder in ['current_edition','original_submitted']:
        obj=json.loads(archive.read(folder+'/MANIFEST.json'));need(len(obj['entries'])==7,'edition seven nonself entries')
        for e in obj['entries']:need(binding(archive.read(folder+'/'+e['file']))=={'bytes':e['bytes'],'sha256':e['sha256']},'edition nested binding')
    for n,text in context['edition_text'].items():need(archive.read('current_edition/'+n).decode()==text,'explicit prose matches current')
    need(archive.read('original_submitted/PROOF.md') in archive.read('current_edition/PROOF.md'),'historical proof verbatim inclusion')
    need(archive.read('manuscript/main.tex')==(A/'publication/manuscript/main.tex').read_bytes(),'TeX exact archive copy')
probes=[]
for spec in reg:
    freeze=root/spec['path'];frozen=freeze.read_bytes();obj=json.loads(frozen);entry=obj[spec['entries_key']][0];payload=root/spec['base']/entry[spec['path_key']];old=payload.read_bytes();outer=root/'MANIFEST.json';originalouter=outer.read_bytes()
    for coupled_nested in [False,True]:
        payload.write_bytes(old+b'\nCORRUPTION ON COPY\n')
        if coupled_nested:
            entry.update(binding(payload.read_bytes()));freeze.write_text(json.dumps(obj,indent=2)+'\n')
        updated=json.loads(originalouter)
        for e in updated['files']:
            if e['path'] in {str(payload.relative_to(root)),spec['path']}:e.update(binding((root/e['path']).read_bytes()))
        outer.write_text(json.dumps(updated,indent=2)+'\n')
        run=subprocess.run(['python3','-B',str(root/'verify.py')],capture_output=True,text=True,timeout=180)
        need(run.returncode!=0,'coupled corruption accepted '+spec['path'])
        probes.append({'family':spec['path'],'coupled_nested_manifest':coupled_nested,'returncode':run.returncode,'error':run.stderr.strip().splitlines()[-1]})
        payload.write_bytes(old);freeze.write_bytes(frozen);outer.write_bytes(originalouter)
save('PACKAGE_INTEGRITY_RESULTS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'zip_unique_safe_members':105,'outer_bound_members':104,'actual_nested_families':nested,'frozen_members':53,'edition_manifests_checked':2,'original_Git_blob_ids_checked':blobchecks,'local_archive_current8_exact':True,'historical_original_proof_contained_verbatim':True,'TeX_exact':True,'coupled_corruption_probes':probes,'all_14_corruptions_rejected':True,'scope':'All mutations on the independently extracted copy; outer inventory rewritten deliberately, and then nested freeze rewritten too while outside context anchor stays fixed. No Git command or live integration.'})
print(json.dumps({'math_generic_cases':generic,'deep_cases':len(deep),'word_levels':len(families),'nested_families':len(nested),'coupled_corruptions_rejected':len(probes)}))

#!/usr/bin/env python3
"""Independent CAS/polynomial-extension audit. No imports of author code.
Usage: python -B INDEPENDENT_VERIFY.py [frozen_packet_directory]
Writes nothing; emits deterministic JSON. Requires SymPy. Packet mutations occur
only in disposable private temporary copies. The frozen packet is read-only.
"""
from pathlib import Path
import hashlib, itertools, json, shutil, subprocess, sys, tempfile
import sympy as S

ANCHOR='5ae79fd9ca09fc095a33d7acfa27818377163c1eb2161977ff172cf641420616'
PROOF='76d197a8fc07f7e3796d67a24308531aa315b0aa03a69f3a2122c3bdf7f77b68'
NAMES={'APPROACH_LOG.md','CHECK_PACKET.py','MANIFEST.json','PROOF.md','README.md','RESULTS.json','SOURCES.json','SOURCE_GATE.md','STATUS.json','VERIFY.py'}
CHECKS=[]
def require(ok,label):
    if not bool(ok): raise AssertionError(label)
    CHECKS.append(label)

def unique(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValueError('duplicate JSON key')
        out[k]=v
    return out

def authenticate(root):
    if {p.name for p in root.iterdir()}!=NAMES: raise ValueError('membership')
    if any((root/n).is_symlink() or not (root/n).is_file() for n in NAMES):raise ValueError('file type')
    d=(root/'MANIFEST.json').read_bytes()
    if hashlib.sha256(d).hexdigest()!=ANCHOR:raise ValueError('external manifest anchor')
    m=json.loads(d,object_pairs_hook=unique)
    if len(m['files'])!=9 or {r['path'] for r in m['files']}!=NAMES-{'MANIFEST.json'}:raise ValueError('manifest membership')
    for r in m['files']:
        data=(root/r['path']).read_bytes()
        if len(data)!=r['bytes'] or hashlib.sha256(data).hexdigest()!=r['sha256']:raise ValueError('file bytes')
    if hashlib.sha256((root/'PROOF.md').read_bytes()).hexdigest()!=PROOF:raise ValueError('external proof anchor')
    return True

x,y,z,w,s,t=S.symbols('x y z w s t', nonzero=True)
vectors=[(1,0),(0,1),(-1,-1)]
cones=[{1,2},{0,2},{0,1}]
B=[S.Matrix([[1,0,0],[-1,1,0],[0,-1,1]]), S.Matrix([[1,1,0],[0,-1,1],[0,0,-1]]), S.eye(3)]
U=[[(-1,-2),(-2,0),(-2,3)],[(4,-3),(0,-3),(-1,-1)],[(4,-2),(0,0),(-1,3)]]
def frames(bases,weights):return [b*S.diag(*[x**(-a)*y**(-c) for a,c in row]) for b,row in zip(bases,weights)]
def transitions(F):return {(i,j):(F[i].inv()*F[j]).applyfunc(S.expand) for i,j in itertools.permutations(range(3),2)}
def terms(expr,variables):
    """Exact Laurent coefficient collection; leaves no variables in coefficients."""
    ans={}
    for term in S.Add.make_args(S.expand(expr)):
        if term==0:continue
        p=term.as_powers_dict();ex=tuple(int(p.get(v,0)) for v in variables)
        coeff=S.cancel(term/S.prod(v**k for v,k in zip(variables,ex)))
        if any(coeff.has(v) for v in variables):raise ValueError('not Laurent polynomial')
        ans[ex]=S.expand(ans.get(ex,0)+coeff)
    return {a:c for a,c in ans.items() if c!=0}
def regular(G):
    for (i,j),M in G.items():
        ray=vectors[next(iter(cones[i]&cones[j]))]
        for q in M:
            for (a,b) in terms(q,(x,y)):
                if a*ray[0]+b*ray[1]<0:return False
    return True

def convert(q,chart):
    if chart==0:return S.expand(q.subs({x:1/w,y:z/w},simultaneous=True))
    if chart==1:return S.expand(q.subs({x:s/t,y:1/t},simultaneous=True))
    return S.expand(q)
vars_by_chart=[(z,w),(s,t),(x,y)]
def extension_matrix(F,bounds):
    """Use arbitrary chart-3 polynomial coefficients, then ban all poles in charts 1/2.
    No weightspace or filtration-intersection routine is used.
    """
    monoms=[(j,a,b) for j,D in enumerate(bounds) for a in range(D+1) for b in range(D+1-a)]
    local=[]
    for j,a,b in monoms:
        q=S.zeros(3,1);q[j]=x**a*y**b;local.append(q)
    equations={}
    for chart in [0,1]:
        T=F[chart].inv()*F[2]
        for col,q in enumerate(local):
            coeff=T*q
            for comp in range(3):
                for powers,c in terms(convert(coeff[comp],chart),vars_by_chart[chart]).items():
                    if min(powers)<0:
                        row=equations.setdefault((chart,comp,powers),[S.Integer(0)]*len(monoms));row[col]+=c
    A=S.Matrix(list(equations.values())) if equations else S.zeros(0,len(monoms))
    kernel=A.nullspace()
    out=[]
    for v in kernel:
        q=S.zeros(3,1)
        for c,m in zip(v,local):q+=c*m
        out.append(q.applyfunc(S.expand))
    return A,out,monoms

def local_sections(F,sections,chart):
    return [((F[chart].inv()*F[2])*v).applyfunc(lambda q:convert(q,chart)) for v in sections]
def jet_matrix(F,sections,chart,order):
    sec=local_sections(F,sections,chart);coords=vars_by_chart[chart]
    labels=[(j,a,b) for j in range(3) for a in range(order+1) for b in range(order+1-a)]
    return S.Matrix([[terms(v[j],coords).get((a,b),S.Integer(0)) for v in sec] for j,a,b in labels]),labels

def check_extension(F,section):
    for i in range(3):
        v=local_sections(F,[section],i)[0]
        if any(min(p)<0 for q in v for p in terms(q,vars_by_chart[i])):return False
    return True

def section_data(F,sec):
    ans=[]
    for q in sec:
        rational=(F[2]*q).applyfunc(S.expand)
        support={exp for entry in rational for exp in terms(entry,(x,y))}
        require(len(support)==1,'independent solution vector has one Laurent weight')
        a,b=next(iter(support));v=[S.cancel(c/(x**a*y**b)) for c in rational]
        first=next(c for c in v if c);v=[c/first for c in v]
        ans.append({'weight':[-a,-b],'vector':[int(c) for c in v],'chart3':[str(S.cancel(c/first)) for c in q]})
    return sorted(ans,key=lambda a:a['weight'])

def main():
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'toric_jets_30001603'
    require(authenticate(root),'external anchors and all 10 frozen files authenticate')
    replay=subprocess.run([sys.executable,'-B',str(root/'VERIFY.py')],capture_output=True,check=True)
    require(replay.stdout==(root/'RESULTS.json').read_bytes() and not replay.stderr,'author verifier exact byte replay')
    author=json.loads(replay.stdout);require(author['assertions']==79,'author reported 79 assertions')
    integrity=subprocess.run([sys.executable,'-B',str(root/'CHECK_PACKET.py')],capture_output=True,check=True)
    ir=json.loads(integrity.stdout);require(ir['rejected_integrity_mutations']==['modify','remove','add'],'author 3 integrity negative controls replay')
    F=frames(B,U);G=transitions(F)
    require(regular(G),'all six Laurent transitions regular on exact fan overlaps')
    for i,j in itertools.permutations(range(3),2):
        require((G[i,j]*G[j,i]).applyfunc(S.simplify)==S.eye(3),f'CAS inverse {i+1},{j+1}')
    for i,j,k in itertools.permutations(range(3),3):
        require((G[i,j]*G[j,k]-G[i,k]).applyfunc(S.simplify)==S.zeros(3),f'CAS cocycle {i+1},{j+1},{k+1}')
    require(G[2,1]==S.Matrix([[y,x**4*y,0],[0,-y**3,x*y],[0,0,-y**4]]),'displayed G32')
    require(G[2,0]==S.Matrix([[x**5,0,0],[-x*y**2,x**2,0],[0,-x*y**3,x]]),'displayed G31')
    G21=G[1,0].applyfunc(lambda a:convert(a,1))
    require(G21==S.Matrix([[0,0,s**6],[s,0,-s**2*t**4],[0,s,-s*t**3]]),'displayed G21 in s,t coordinates')
    require([S.factor(G[2,1].det()),S.factor(G[2,0].det()),S.factor(G21.det())]==[y**8,x**8,s**8],'unit overlap determinants')
    restrictions=[G[2,1].subs(x,0),G[2,0].subs(y,0),G21.subs(t,0)]
    degrees=[]
    for M,coord in zip(restrictions,[y,x,s]):
        require(all(sum(v!=0 for v in M.row(i))==1 for i in range(3)) and all(sum(v!=0 for v in M.col(i))==1 for i in range(3)),'curve transition monomial permutation matrix')
        degrees.append(sorted([int(v.as_powers_dict().get(coord,0)) for v in M if v],reverse=True))
    require(degrees==[[4,3,1],[5,2,1],[6,1,1]],'independent divisor restrictions')
    require(min(sum(degrees,[]))==1,'tau exactly 1')
    A,sec,monoms=extension_matrix(F,[5,3,5])
    require((A.cols,A.rank(),len(sec))==(52,40,12),'52-variable polynomial extension system has rank40 and nullity12')
    require(all(check_extension(F,q) for q in sec),'all kernel sections extend regularly')
    records=section_data(F,sec)
    expected={(-1,-2):(1,-1,0),(0,-3):(1,-1,0),(0,-2):(1,-1,0),(-2,0):(0,1,-1),(-1,-1):(0,1,-1),(-1,0):(0,1,-1),(-2,3):(0,0,1),(-1,2):(0,0,1),(-1,3):(0,0,1),(3,-2):(1,0,0),(4,-3):(1,0,0),(4,-2):(1,0,0)}
    require({tuple(r['weight']):tuple(r['vector']) for r in records}==expected,'ungraded solution recovers all 12 claimed weights and vectors')
    values=[jet_matrix(F,sec,i,0)[0].rank() for i in range(3)]
    jets=[jet_matrix(F,sec,i,1)[0].rank() for i in range(3)]
    require(values==[3,3,2] and jets==[9,9,7],'independent values and derivative ranks')
    J,labels=jet_matrix(F,sec,2,1)
    missing=[list(q) for i,q in enumerate(labels) if all(c==0 for c in J.row(i))]
    require(missing==[[1,0,0],[1,0,1]],'only e2 value and e2 y rows are zero')
    require(J.rank()==len(labels)-len(missing),'other seven jet directions independent')
    badU=[[tuple(q) for q in row] for row in U];badU[0][2]=(-2,4)
    require(not regular(transitions(frames(B,badU))),'changed local weight rejected by overlap poles')
    badG=dict(G);badG[2,0]=G[2,0].copy();badG[2,0][0,1]+=1
    require((badG[2,0]*badG[0,1]-badG[2,1]).applyfunc(S.simplify)!=S.zeros(3),'independently changed transition rejected by cocycle')
    require(not check_extension(F,S.Matrix([0,1,0])),'false e2 constant does not extend')
    for name,u,dim,jr in [
        ('O^3',[[(0,0)]*3]*3,3,3),
        ('O(1)^3',[[(-1,0)]*3,[(0,-1)]*3,[(0,0)]*3],9,9),
        ('O(-1)^3',[[(1,0)]*3,[(0,1)]*3,[(0,0)]*3],0,0)]:
        FF=frames([S.eye(3)]*3,u);require(regular(transitions(FF)),name+' glues')
        _,SS,_=extension_matrix(FF,[3,3,3]);require(len(SS)==dim,name+' H0 dimension')
        rr=[jet_matrix(FF,SS,i,1)[0].rank() if SS else 0 for i in range(3)]
        require(rr==[jr]*3,name+' first jet ranks')
    correct=F[2].inv()*S.Matrix([1,-1,0])*x*y**2
    incorrect=F[2].inv()*S.Matrix([1,-1,0])*x/y**2
    require(check_extension(F,correct),'source vertex (-1,-2) gives genuine section')
    require(not check_extension(F,incorrect),'synthetically sign-flipped vertex (-1,2) rejected')
    modes=['append_proof','same_length_proof','remove_source','add_unlisted','symlink_source','duplicate_manifest_key','rehash_tampered_proof','replace_results']
    rejected=[]
    for mode in modes:
        with tempfile.TemporaryDirectory(prefix='audit698-integrity-') as tmp:
            copy=Path(tmp)/'packet';shutil.copytree(root,copy)
            if mode=='append_proof':(copy/'PROOF.md').write_bytes((copy/'PROOF.md').read_bytes()+b'\n')
            elif mode=='same_length_proof':
                p=copy/'PROOF.md';d=p.read_bytes();p.write_bytes(b'!'+d[1:])
            elif mode=='remove_source':(copy/'SOURCES.json').unlink()
            elif mode=='add_unlisted':(copy/'payload.txt').write_text('unlisted')
            elif mode=='symlink_source':(copy/'SOURCES.json').unlink();(copy/'SOURCES.json').symlink_to(root.resolve()/'SOURCES.json')
            elif mode=='duplicate_manifest_key':
                p=copy/'MANIFEST.json';p.write_bytes(p.read_bytes().replace(b'{',b'{"schema":"false",',1))
            elif mode=='rehash_tampered_proof':
                p=copy/'PROOF.md';p.write_bytes(p.read_bytes()+b'\n');m=json.loads((copy/'MANIFEST.json').read_text())
                for r in m['files']:
                    if r['path']=='PROOF.md':r.update(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                (copy/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
            else:(copy/'RESULTS.json').write_text('{"result":"PASS"}\n')
            try:authenticate(copy)
            except ValueError:rejected.append(mode)
            else:raise AssertionError('mutation accepted: '+mode)
    require(rejected==modes,'all eight independently anchored corruption controls rejected')
    require(authenticate(root),'original frozen bytes unchanged after audit')
    print(json.dumps({'schema':'toric-jets-independent-cas-audit-v1','result':'PASS_MATHEMATICS_SOURCE_CORRECTION_REQUIRED','sympy_version':S.__version__,'author_manifest_sha256':ANCHOR,'author_proof_sha256':PROOF,'author_assertions_replayed':author['assertions'],'independent_assertions':len(CHECKS),'checks':CHECKS,'algorithm':'Independent symbolic rational frame multiplication and ungraded chart-polynomial pole cancellation; no import of author modules.','section_system':{'unknowns':A.cols,'constraints':A.rows,'rank':A.rank(),'nullity':len(sec),'component_total_degree_bounds':[5,3,5]},'global_sections':records,'splitting_degrees':degrees,'tau':1,'value_ranks':values,'first_jet_ranks':jets,'bad_chart_zero_rows':missing,'independent_corruption_controls':rejected,'source_correction':'Both inspected PDFs print (-1,-2). The author packet falsely labels the synthetic sign flip (-1,2) as a published typo.','proof_limit':'Finite exact checks corroborate the separately reasoned geometric proof and do not prove nefness by themselves.'},indent=2,sort_keys=True))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Read-only independent folding/inverse and exact-custody checks.
The Bogopolski–Maslakova basis algorithm is imported in the proof, not run here.
"""
from pathlib import Path
from itertools import product,permutations
import hashlib,json,random
P=Path(__file__).resolve().parent
HEAD='b50aa7e9aabcd15247cb0463af742a0e9cf49653'
BASE='4b27092a448d53b61408355ce44ec38d103a1ce4'
def need(c,m):
    if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((P/n).read_text())
def red(w):
    a=[]
    for x in w:
        if a and a[-1]==-x:a.pop()
        else:a.append(x)
    return tuple(a)
def inv(w):return tuple(-x for x in reversed(w))
def apply(images,w):
    a=()
    for x in w:a=red(a+(images[x-1] if x>0 else inv(images[-x-1])))
    return a
def compose(a,b):return tuple(apply(a,w) for w in b)
def words(n,L):
    out=[()];level=[()]
    for _ in range(L):
        level=[w+(a,) for w in level for a in range(-n,n+1) if a and (not w or w[-1]!=-a)]
        out.extend(level)
    return out

def recognize(n,images):
    if not isinstance(n,int) or n<0 or len(images)!=n:return False
    if any(not isinstance(x,int) or not 0<abs(x)<=n for w in images for x in w):return False
    ws=[red(w) for w in images]
    if n==0:return True
    if any(not w for w in ws):return False
    edges=[];nv=1
    for w in ws:
        v=0
        for j,label in enumerate(w):
            if j==len(w)-1:t=0
            else:t=nv;nv+=1
            edges.append((v,t,label));v=t
    parent=list(range(nv));active=set(range(len(edges)));drops=0;steps=0
    def find(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]];a=parent[a]
        return a
    while True:
        seen={};conflict=None
        for eid in sorted(active):
            a,b,l=edges[eid];a=find(a);b=find(b)
            for s,t,label in [(a,b,l),(b,a,-l)]:
                key=(s,label)
                if key in seen and seen[key][0]!=eid:
                    conflict=(seen[key][0],eid,seen[key][1],t);break
                seen[key]=(eid,t)
            if conflict:break
        if not conflict:break
        keep,remove,a,b=conflict;a=find(a);b=find(b)
        if a!=b:parent[b]=a
        else:drops+=1
        active.remove(remove);steps+=1
        need(steps<=len(edges),'fold termination guard')
    base=find(0);adj={}
    for eid in active:
        a,b,l=edges[eid];a=find(a);b=find(b)
        adj[(a,l)]=b;adj[(b,-l)]=a
    ok=all(adj.get((base,i))==base for i in range(1,n+1))
    if ok:
        need(drops==0 and len(active)==n,'accepted folds preserve rank')
        need(all(find(a)==base and find(b)==base for i in active for a,b,_ in [edges[i]]),'accepted final rose')
    return ok

def inverse_certificate(images,search):
    n=len(images);targets={(i,):i-1 for i in range(1,n+1)};ans=[None]*n
    for w in search:
        image=apply(images,w)
        if image in targets:
            i=targets[image]
            if ans[i] is None:ans[i]=w
        if all(w is not None for w in ans):break
    need(all(w is not None for w in ans),'finite inverse search cap exceeded')
    ans=tuple(ans);identity=tuple((i,) for i in range(1,n+1))
    need(compose(images,ans)==identity and compose(ans,images)==identity,'two-sided inverse certificate')
    return max(map(len,ans),default=0)

def math_checks():
    wl=words(2,2);wr=words(2,3);search=words(2,6);accepted=0;max_inverse=0
    need(len(wl)==17 and len(wr)==53,'reduced enumeration counts')
    for pair in product(wl,wr):
        if recognize(2,pair):
            accepted+=1;max_inverse=max(max_inverse,inverse_certificate(pair,search))
    signed=0
    for n in range(1,5):
        for perm in permutations(range(1,n+1)):
            for signs in product((-1,1),repeat=n):
                alpha=tuple((a*s,) for a,s in zip(perm,signs))
                need(recognize(n,alpha),'signed permutation recognition');signed+=1
    need(signed==442,'signed permutation count')
    rank3_count=0
    for triple in product(words(3,1),repeat=3):
        expected=all(len(w)==1 for w in triple) and len({abs(w[0]) for w in triple})==3
        need(recognize(3,triple)==expected,'rank3 norm1 complete classification');rank3_count+=1
    for w in words(1,8):need(recognize(1,(w,))==(len(w)==1),'rank-one proper-power guard')
    need(recognize(0,()) and not recognize(1,((),)),'rank0/L0 boundary')
    bad=((1,),(2,1,2,-1,-2))
    exponent=lambda w,j:sum((1 if x>0 else -1) for x in w if abs(x)==j)
    det=exponent(bad[0],1)*exponent(bad[1],2)-exponent(bad[0],2)*exponent(bad[1],1)
    need(det==1 and not recognize(2,bad),'determinant-one nonautomorphism rejected')
    need(not recognize(2,((1,),(1,))) and not recognize(2,((1,1),(2,))),'redundancy/proper-power rejected')
    # Known automorphisms generated with independently tracked inverses.
    rng=random.Random(1237);generated=0
    for _ in range(100):
        n=3;identity=tuple((i,) for i in range(1,n+1));a=identity;b=identity
        for _ in range(1+rng.randrange(8)):
            i,j=rng.sample(range(n),2);tau=list(identity);back=list(identity);kind=rng.randrange(3)
            if kind==0:tau[i]=(-i-1,);back[i]=(-i-1,)
            elif kind==1:tau[i],tau[j]=tau[j],tau[i];back=list(tau)
            else:tau[i]=(i+1,j+1);back[i]=(i+1,-j-1)
            a=compose(a,tuple(tau));b=compose(tuple(back),b)
        need(compose(a,b)==identity and compose(b,a)==identity,'generated inverse certificates')
        need(recognize(n,a),'generated Nielsen automorphisms must be recognized');generated+=1
    inner=0
    for k in range(51):
        g=(2,)*k+(1,)+(-2,)*k
        alpha=tuple(red(g+(i,)+inv(g)) for i in (1,2))
        back=tuple(red(inv(g)+(i,)+g) for i in (1,2))
        need(compose(alpha,back)==((1,),(2,)) and compose(back,alpha)==((1,),(2,)),'inner inverse')
        need(recognize(2,alpha) and apply(alpha,g)==g,'inner fixed generator')
        need(len(g)==2*k+1 and max(map(len,alpha))==(3 if k==0 else 4*k+3),'based norm formula')
        cyclic=g
        while len(cyclic)>1 and cyclic[0]==-cyclic[-1]:cyclic=cyclic[1:-1]
        need(cyclic==(1,),'based/cyclic negative control')
        inner+=1
    return {'asymmetric_rank2_tuples':len(wl)*len(wr),'accepted_two_sided_inverse_certified':accepted,
            'inverse_search_cap':6,'max_inverse_length_seen':max_inverse,'rank3_norm1_tuples':rank3_count,
            'signed_permutations':signed,'generated_Nielsen_automorphisms':generated,'inner_basing_controls':inner,
            'negative_controls':['determinant_one_nonautomorphism','redundant_tuple','proper_power','empty_basis_image','outer_vs_based_length'],
            'basis_algorithm_A_implemented':False,'general_B_values_computed':False}

def entrycheck(entries,base,exclude=None):
    names=[e['file'] for e in entries];need(len(names)==len(set(names)),'duplicate seal entry')
    for e in entries:
        rel=Path(e['file']);need(not rel.is_absolute() and '..' not in rel.parts,'unsafe seal path')
        q=base/rel;need(q.is_file() and not q.is_symlink(),'member missing/symlink');d=q.read_bytes()
        need(len(d)==e['bytes'] and sha(d)==e['sha256'],'sealed digest '+e['file'])
    actual=set()
    for q in base.rglob('*'):
        need(not q.is_symlink(),'symlink closure')
        if q.is_file() and q!=exclude:actual.add(q.relative_to(base).as_posix())
    need(set(names)==actual,'exact recursive closure membership')

def custody():
    b=load('PR_BINDING.json');pr=load('private/pr.json');final=load('private/pr_final.json')
    need(b['head']==HEAD and b['base']==BASE and b['state']=='open' and b['draft'] and not b['queue_changed'],'PR binding')
    for r in [pr,final]:need(r['head']['sha']==HEAD and r['base']['sha']==BASE and r['state']=='open' and r['draft'],'live PR identity')
    need(pr['body']==final['body'] and sha(pr['body'].encode())==b['body_sha256'],'body binding')
    fs={r['filename']:r for r in load('private/files.json')};need(len(fs)==len(b['eight_blobs'])==8,'eight files')
    names=set()
    for e in b['eight_blobs']:
        path=e['path'];need(path.startswith('unsolved_math_prioritization/attempts/1101206/') and 'QUEUE' not in path,'scope')
        names.add(Path(path).name);d=(P/'private'/Path(path).name).read_bytes();f=fs[path]
        need(f['status']=='added' and f['sha']==e['git_blob_sha']==hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest(),'Git blob')
        need(len(d)==e['bytes'] and sha(d)==e['sha256'],'exact payload')
    m=load('private/MANIFEST.json');need(set(m['members'])==names and {e['file'] for e in m['entries']}==names-{'MANIFEST.json'},'nested manifest set')
    for e in m['entries']:
        d=(P/'private'/e['file']).read_bytes();need(len(d)==e['bytes'] and sha(d)==e['sha256'],'nested manifest digest')
    proof=(P/'private/PROOF.md').read_text();need(proof[proof.index('## Conclusion and scope'):] in (P/'private/AUDIT.md').read_text(),'shared complete argument')
    raw=(P/'private/GWS_FULL43.json').read_bytes();g=json.loads(raw);clear=load('GWS_CLEARANCE.json');v=g['valueRanges'][0]
    need(sha(raw)==clear['sha256']=='fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1','own fresh tracker')
    need(v['dataFilters']==[{'gridRange':{'endColumnIndex':43,'sheetId':1254632077,'startColumnIndex':0}}],'43 numeric columns')
    need(len(v['valueRange']['values'])==191 and not clear['unresolved_duplicate_leads'],'tracker clearance')
    for token in load('SOURCE_ALIASES.json')['no_hit_tokens']:
        need(not any(token.casefold() in '\t'.join(map(str,r)).casefold() for r in v['valueRange']['values']),'unresolved alias '+token)
    errors=[]
    for e in load('PRIMARY_RECEIPT.json')['sources']:
        if 'error' in e:errors.append(e['name']);continue
        d=(P/'private'/e['name']).read_bytes();need(e['http']==200 and len(d)==e['bytes'] and sha(d)==e['sha256'],'primary receipt')
    need(set(errors)=={'doi_response.html','author_final.pdf'},'source access limits disclosed')
    x=load('private/crossref.json')['message'];need(x['DOI']=='10.1142/s0218196716500028' and x['volume']=='26' and x['issue']=='01' and x['page']=='29-67','journal DOI identity')
    need([a['family'] for a in x['author']]==['Bogopolski','Maslakova'] and x['published-print']['date-parts']==[[2016,2]],'journal authors/date')
    landing=(P/'private/arxiv_landing.html').read_text();need('1204.6728v6' in landing and '1204.6728v7' not in landing,'current v6 version')
    prop=load('CELL_PROPOSAL.json');need(len(prop['values'])==1 and len(prop['values'][0])==4 and prop['values'][0][1]=='','literal four cells Bblank')
    need(prop['values'][0][2]=='https://doi.org/10.1142/S0218196716500028' and prop['service_write_performed'] is False,'existing DOI only')
    entrycheck(load('PRIVATE_BODY_SEAL.json')['entries'],P/'private');entrycheck(load('REVIEW_SEAL.json')['entries'],P,P/'REVIEW_SEAL.json')
    return {'head':HEAD,'eight_added_blobs':8,'own_tracker_rows':191,'journal_metadata_authenticated':True,
            'publisher_DOI_HTTP200_claimed':False,'entire_BM_proof_independently_audited':False,
            'private_and_exact_recursive_seals':'PASS','author_programs_executed':False,'service_writes':False}

if __name__=='__main__':
    try:need(False,'deliberate guard probe')
    except RuntimeError:pass
    else:raise RuntimeError('guard disabled')
    print(json.dumps({'status':'PASS','algebra':math_checks(),'custody':custody()},indent=2,sort_keys=True))

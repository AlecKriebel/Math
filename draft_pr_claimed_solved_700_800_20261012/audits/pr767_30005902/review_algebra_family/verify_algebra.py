#!/usr/bin/env python3
"""Independent exact structure-constant checks. Stdlib, no writes, no assert."""
from itertools import product
import json

P=3
B=list(product(range(3),repeat=3)); I={e:i for i,e in enumerate(B)}
o=(0,0,0); x=(1,0,0); y=(0,1,0); z=(0,0,1)
def need(ok,name):
    if not ok: raise RuntimeError(name)
def atom(e): return {e:1}
def clean(a,p=P): return {e:c%p for e,c in a.items() if c%p}
def add(*terms,p=P):
    a={}
    for t in terms:
        for e,c in t.items(): a[e]=(a.get(e,0)+c)%p
    return clean(a,p)
def sc(a,s,p=P): return clean({e:c*s for e,c in a.items()},p)
def mul(a,b,p=P):
    d={}
    for u,c in a.items():
        for v,f in b.items():
            e=tuple(i+j for i,j in zip(u,v))
            if max(e)<3: d[e]=(d.get(e,0)+c*f)%p
    return clean(d,p)
def power(a,n,p=P):
    v={(0,)*len(next(iter(a))):1}
    for _ in range(n): v=mul(v,a,p)
    return v
def monomap(e,images):
    v={(0,)*len(next(iter(images[0]))):1}
    for n,g in zip(e,images): v=mul(v,power(g,n))
    return v
G=[add(atom(g+o),atom(o+g)) for g in (x,y,z)]
G[2]=add(G[2],atom(x+y))
D={e:monomap(e,G) for e in B}
SG=[sc(atom(x),-1),sc(atom(y),-1),add(sc(atom(z),-1),atom((1,1,0)))]
S={e:monomap(e,SG) for e in B}
def lin(a,A): return add(*(sc(A[e],c) for e,c in a.items()))
def eps(a): return a.get(o,0)
def lift(t,side,ds=D):
    a={}
    for q,c in t.items():
        u,v=q[:3],q[3:]
        exp={w+v:d for w,d in ds[u].items()} if side==0 else {u+w:d for w,d in ds[v].items()}
        a=add(a,sc(exp,c))
    return a
def conv(e,left=True,ss=S):
    a={}
    for q,c in D[e].items():
        u,v=q[:3],q[3:]
        a=add(a,sc(mul(ss[u],atom(v)) if left else mul(atom(u),ss[v]),c))
    return a
def counit(t,side):
    a={}
    for q,c in t.items():
        u,v=q[:3],q[3:]
        if (u if side==0 else v)==o:
            e=v if side==0 else u; a[e]=(a.get(e,0)+c)%P
    return clean(a)
def trans(f,right):
    A={}
    for e in B:
        a={}
        for q,c in D[e].items():
            u,v=q[:3],q[3:]; target,test=(v,u) if right else (u,v)
            if test==f: a[target]=(a.get(target,0)+c)%P
        A[e]=clean(a)
    return A
def compose(A,C): return {e:lin(C[e],A) for e in B}
def comm(A,C):
    ac,ca=compose(A,C),compose(C,A)
    return {e:add(ac[e],sc(ca[e],-1)) for e in B}
def maps(A,c): return {e:sc(v,c) for e,v in A.items()}
def deriv(A):
    return all(lin(mul(atom(a),atom(b)),A)==add(mul(A[a],atom(b)),mul(atom(a),A[b])) for a,b in product(B,repeat=2))
def rank(rows):
    a=[[v%P for v in row] for row in rows]; r=0
    if not a: return 0
    for j in range(len(a[0])):
        q=next((i for i in range(r,len(a)) if a[i][j]),None)
        if q is None: continue
        a[r],a[q]=a[q],a[r]; inv=pow(a[r][j],-1,P); a[r]=[(v*inv)%P for v in a[r]]
        for i in range(r+1,len(a)):
            if a[i][j]:
                c=a[i][j]; a[i]=[(v-c*w)%P for v,w in zip(a[i],a[r])]
        r+=1
    return r
def df(f,a,b): return ((a==o)*(b==f)-mul(atom(a),atom(b)).get(f,0)+(a==f)*(b==o))%P
def fmt(a): return [{'exp':list(e),'coefficient':a[e]} for e in sorted(a)]
def main():
    counts={}
    need(all(power(g,3)=={} for g in G+SG),'quotient relation images')
    counts['generator_cubes_coproduct_and_antipode']=6
    for a,b,c in product(B,repeat=3):
        need(mul(mul(atom(a),atom(b)),atom(c))==mul(atom(a),mul(atom(b),atom(c))),'associativity')
    counts['associativity_basis_triples']=27**3
    for a,b in product(B,repeat=2):
        ab=mul(atom(a),atom(b))
        need(lin(ab,D)==mul(D[a],D[b]),'delta multiplication')
        need(lin(ab,S)==mul(S[b],S[a]),'S antimultiplication')
        need(eps(ab)==eps(atom(a))*eps(atom(b)),'epsilon multiplication')
    counts['multiplication_basis_pairs_each_of_three_checks']=27**2
    for e in B:
        need(lift(D[e],0)==lift(D[e],1),'coassociativity')
        need(counit(D[e],0)==atom(e)==counit(D[e],1),'counits')
        need(conv(e,True)==conv(e,False)==(atom(o) if e==o else {}),'antipodes')
        need(lin(S[e],S)==atom(e),'S squared')
    counts['basis_inputs_each_coassoc_counits_antipodes_involution']=27
    need(D[o]==atom(o+o) and S[o]==atom(o),'unit')
    matrix=[[df(f,a,b) for f in B] for a,b in product(B,repeat=2)]
    r=rank(matrix); need(r==24,'bar differential rank')
    need(all(df(t,a,b)==0 for t in (x,y,z) for a,b in product(B,repeat=2)),'three scalar cocycles')
    d0=[[(int(a==o)*c-c*int(a==o))%P for a in B] for c in range(P)]
    need(rank(d0)==0,'scalar boundaries')
    irr={q for a,b in product(B[1:],repeat=2) for q in mul(atom(a),atom(b))}
    need(len(irr)==23,'I square rank independent check')
    R={t:trans(t,True) for t in (x,y,z)}; L={t:trans(t,False) for t in (x,y,z)}
    need(all(deriv(v) for v in list(R.values())+list(L.values())),'six Leibniz checks')
    RC=comm(R[x],R[y]); LC=comm(L[x],L[y])
    need(RC==maps(R[z],-1),'right commutator')
    need(LC==L[z],'left commutator')
    need(all(eps(R[t][e])==int(e==t) for e in B for t in (x,y,z)),'epsilon splitting')
    bracket={e:eps(RC[e]) for e in B}
    need(bracket[z]==2 and sum(bool(c) for c in bracket.values())==1,'minus fz cochain')
    need(all(sum(row[I[e]]*bracket[e] for e in B)%P==0 for row in matrix),'bracket scalar cocycle')
    dual={e:(D[e].get(x+y,0)-D[e].get(y+x,0))%P for e in B}
    need(all(dual[e]==int(e==z) for e in B),'independent dual convolution commutator')
    counts['scalar_delta1_matrix_shape']=[729,27]
    counts['derivation_basis_pairs_per_map']=729;counts['translation_maps_checked']=6
    controls={}
    tau={q[3:]+q[:3]:c for q,c in D[z].items()}; diff=add(D[z],sc(tau,-1))
    need(bool(diff),'false cocommutativity detected')
    controls['false_cocommutativity_and_R1_quasitriangularity']={'detected':True,'delta_z_minus_flip':fmt(diff)}
    badS=dict(S);badS[z]=sc(atom(z),-1);w=conv(z,True,badS);need(bool(w),'false antipode detected')
    controls['omit_xy_in_antipode']={'detected':True,'left_convolution_z':fmt(w)}
    need(RC!=R[z] and LC!=maps(L[z],-1),'wrong orientation sign detected')
    controls['opposite_translation_orientation_sign']={'detected':True,'R_comm_z':fmt(RC[z]),'L_comm_z':fmt(LC[z])}
    need(df(o,o,o)!=0,'false constant cocycle detected')
    controls['constant_functional_not_cocycle']={'detected':True,'delta_1_1':df(o,o,o)}
    char5=power(G[0],3,5);need(bool(char5),'characteristic5 quotient failure')
    controls['same_cubic_quotient_char5_fails']={'detected':True,'delta_x_cubed':fmt(char5)}
    badG=list(G);badG[2]=add(atom(z+o),atom(o+z),atom(x+(0,2,0)))
    badD={e:monomap(e,badG) for e in B};w=add(lift(badD[z],0,badD),sc(lift(badD[z],1,badD),-1))
    need(bool(w),'false coproduct detected')
    controls['cross_x_tensor_y_squared_fails_coassociativity']={'detected':True,'coassociator_z':fmt(w)}
    return {'field':'F3','dimension':27,'all_positive_checks_pass':True,'counts':counts,
      'cohomology':{'delta0_rank':0,'delta1_rank':r,'C1_dimension':27,'H1_dimension':27-r,'I_squared_dimension':len(irr),'bracket_minus_fz_at_z':bracket[z],'fz_at_z':1},
      'translation_values':{side:{str(t):{str(g):fmt(A[t][g]) for g in (x,y,z)} for t in (x,y,z)} for side,A in [('R',R),('L',L)]},
      'dual_primitive_commutator':'fx*fy-fy*fx=fz; R reverses convolution composition',
      'negative_controls':controls,
      'limits':['Finite checks alone do not certify the source monoidal Ext bracket comparison.','No priority, formal verification, or characteristic-zero extension is certified.']}
if __name__=='__main__': print(json.dumps(main(),indent=2,sort_keys=True))

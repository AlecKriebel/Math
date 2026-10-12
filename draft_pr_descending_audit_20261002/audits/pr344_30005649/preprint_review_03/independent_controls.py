"""New independent adversary: direct polynomial arithmetic, actual kernels,
full nontriangular coordinate changes, rational evaluation of integral identities.
No author code imports. All computations are finite corroborating controls.
"""
from fractions import Fraction
from functools import lru_cache
import itertools,json,random
COUNT=0
def require(c,msg):
    global COUNT;COUNT+=1
    if not c:raise ValueError(msg)
class K:
    def __init__(self,p,poly):
        self.p=p;self.poly=tuple(poly);self.d=len(poly)-1;self.q=p**self.d
        self.z=(0,)*self.d;self.o=(1,)+(0,)*(self.d-1)
    def encode(self,n):return tuple((n//self.p**i)%self.p for i in range(self.d))
    def add(self,a,b):return tuple((x+y)%self.p for x,y in zip(a,b))
    def neg(self,a):return tuple(-x%self.p for x in a)
    def sub(self,a,b):return self.add(a,self.neg(b))
    @lru_cache(maxsize=None)
    def mul(self,a,b):
        v=[0]*(2*self.d-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):v[i+j]+=x*y
        for i in range(len(v)-1,self.d-1,-1):
            for j,c in enumerate(self.poly[:-1]):v[i-self.d+j]-=v[i]*c
        return tuple(x%self.p for x in v[:self.d])
    def pow(self,a,n):
        o=self.o
        for bit in bin(n)[2:]:
            o=self.mul(o,o)
            if bit=='1':o=self.mul(o,a)
        return o
    def inv(self,a):
        require(a!=self.z,'zero inverse');return self.pow(a,self.q-2)
    def frob(self,a,n=1):return self.pow(a,self.p**(n%self.d))
    def certify(self):
        for x in range(1,self.q):
            a=self.encode(x);require(self.mul(a,self.inv(a))==self.o,'reducible field modulus')
        t=self.encode(self.p)
        require(all(self.frob(t,j)!=t for j in range(1,self.d)),'Frobenius order lower than degree')
def zero(n,m,k):return [[k.z for _ in range(m)] for _ in range(n)]
def eye(n,k):return [[k.o if i==j else k.z for j in range(n)] for i in range(n)]
def trans(a):return [list(c) for c in zip(*a)]
def mm(a,b,k):
    out=zero(len(a),len(b[0]),k)
    for i,row in enumerate(a):
        for j,col in enumerate(trans(b)):
            for x,y in zip(row,col):out[i][j]=k.add(out[i][j],k.mul(x,y))
    return out
def tw(a,k,n):return [[k.frob(x,n) for x in row] for row in a]
def cat(a,b):return [x+y for x,y in zip(a,b)]
def rref(a,k):
    a=[r[:] for r in a];piv=[]
    for j in range(len(a[0])):
        s=len(piv);i=next((i for i in range(s,len(a)) if a[i][j]!=k.z),None)
        if i is None:continue
        a[i],a[s]=a[s],a[i];inv=k.inv(a[s][j]);a[s]=[k.mul(inv,x) for x in a[s]]
        for i in range(len(a)):
            if i==s:continue
            c=a[i][j];a[i]=[k.sub(x,k.mul(c,y)) for x,y in zip(a[i],a[s])]
        piv.append(j)
        if len(piv)==len(a):break
    return a,piv
def rank(a,k):return len(rref(a,k)[1])
def inv(a,k):
    rr,piv=rref(cat(a,eye(len(a),k)),k);require(piv==list(range(len(a))),'matrix inverse singular')
    return [r[len(a):] for r in rr]
def ker(a,k):
    rr,piv=rref(a,k);free=[j for j in range(len(a[0])) if j not in piv];b=zero(len(a[0]),len(free),k)
    for j,c in enumerate(free):
        b[c][j]=k.o
        for i,p in enumerate(piv):b[p][j]=k.neg(rr[i][c])
    return b
def arrow(n,edges,k):
    a=zero(n,n,k)
    for i,j in edges:a[j][i]=k.o
    return a
def delta(a,b,k):return rank(a,k)+rank(b,k)-rank(cat(a,b),k)
def squares(f,v,k):return mm(f,tw(f,k,1),k),mm(v,tw(v,k,-1),k)
def pairing(f,v,k,wrong=False):
    fd=trans(v) if wrong else trans(tw(v,k,1));vd=trans(f) if wrong else trans(tw(f,k,-1))
    rng=random.Random(3442003);fail=0
    for _ in range(40):
        x=[[k.encode(rng.randrange(k.q))] for _ in range(len(f))];phi=[[k.encode(rng.randrange(k.q))] for _ in range(len(f))]
        lf=mm(trans(mm(fd,tw(phi,k,1),k)),x,k)[0][0]
        rf=k.frob(mm(trans(phi),mm(v,tw(x,k,-1),k),k)[0][0],1)
        lv=mm(trans(mm(vd,tw(phi,k,-1),k)),x,k)[0][0]
        rv=k.frob(mm(trans(phi),mm(f,tw(x,k,1),k),k)[0][0],-1)
        fail+=(lf!=rf or lv!=rv)
    return fail
def fields():
    rows=[]
    for p,poly in [(5,[1,2,0,1]),(3,[1,2,0,1]),(2,[1,0,1,0,0,1])]:
        k=K(p,poly);k.certify();f=arrow(6,[(0,1),(1,2),(3,4)],k);v=arrow(6,[(0,5),(3,2),(5,4)],k)
        rng=random.Random(34403);out={'p':p,'q':k.q,'modulus':poly,'basis_controls':[]}
        for label in ('shear','full_nontriangular'):
            P=eye(6,k);P[0][1]=k.encode(p)
            if label=='full_nontriangular':
                P=P[::-1]
                for _ in range(24):
                    i,j=rng.sample(range(6),2);c=k.encode(rng.randrange(1,k.q));P[i]=[k.add(x,k.mul(c,y)) for x,y in zip(P[i],P[j])]
            Q=inv(P,k);require(mm(P,Q,k)==eye(6,k)==mm(Q,P,k),'P inverse');F=mm(mm(Q,f,k),tw(P,k,1),k);V=mm(mm(Q,v,k),tw(P,k,-1),k)
            require(mm(F,tw(V,k,1),k)==zero(6,6,k)==mm(V,tw(F,k,-1),k),'complex relations')
            C,D=squares(F,V,k);FD,VD=trans(tw(V,k,1)),trans(tw(F,k,-1));CD,DD=squares(FD,VD,k)
            KF,KV=tw(ker(C,k),k,-2),tw(ker(D,k),k,2)
            require(mm(C,tw(KF,k,2),k)==zero(6,5,k),'actual F squared kernel')
            require(mm(D,tw(KV,k,-2),k)==zero(6,5,k),'actual V squared kernel')
            invariant=delta(C,D,k);direct=delta(CD,DD,k);correct=delta(trans(tw(D,k,2)),trans(tw(C,k,-2)),k);actual=6-rank(cat(KF,KV),k);bare=delta(trans(C),trans(D),k)
            require((invariant,direct,correct,actual)==(0,1,1,1),'dual formula/basis invariant')
            require(pairing(F,V,k)==0,'direct evaluation duality');bad_pairing=pairing(F,V,k,True);require(bad_pairing>0,'bare transpose mutant')
            if label=='shear':require(bare==0,'old bare row formula mutant')
            out['basis_controls'].append({'name':label,'delta':invariant,'direct_dual_delta':direct,'correct_formula':correct,'actual_kernel_codimension':actual,'bare_formula':bare,'wrong_transpose_pairing_failures':bad_pairing})
        # Generic formula for unrelated random endomorphisms, beyond this one module.
        for _ in range(12):
            A=[[k.encode(rng.randrange(k.q)) for _ in range(4)] for _ in range(4)];B=[[k.encode(rng.randrange(k.q)) for _ in range(4)] for _ in range(4)]
            C,D=squares(A,B,k);CD,DD=squares(trans(tw(B,k,1)),trans(tw(A,k,-1)),k)
            KF,KV=tw(ker(C,k),k,-2),tw(ker(D,k),k,2)
            require(delta(CD,DD,k)==delta(trans(tw(D,k,2)),trans(tw(C,k,-2)),k)==4-rank(cat(KF,KV),k),'generic unrelated endomorphism formula')
        rows.append(out)
    k=K(5,[2,0,0,0,1]);k.certify();t=k.encode(5);require(k.frob(t,6)!=t,'six-step coefficient mutant nondegenerate')
    return rows,{'field':625,'sigma6_of_t':k.frob(t,6),'t':t,'sigma6_not_identity':True}
def prime_flag():
    rows=[]
    for p in (5,7,13,103):
        k=K(p,[0,1]);F=arrow(6,[(0,1),(1,2),(3,4)],k);V=arrow(6,[(0,5),(3,2),(5,4)],k)
        T=trans([[k.encode(x%p) for x in row] for row in [[0,1,0,1,0,1],[0,0,1,0,1,0],[0,2,0,1,0,0],[0,0,1,0,0,0],[1,0,0,0,0,0],[0,1,0,0,0,0]]]);Ti=inv(T,k)
        for A in (F,V):
            B=mm(mm(Ti,A,k),T,k)
            for size in (2,4):require(all(B[i][j]==k.z for i in range(size,6) for j in range(size)),'stable module flag')
            for s in (0,2,4):require([[B[i][j] for j in range(s,s+2)] for i in range(s,s+2)]==arrow(2,[(0,1)],k),'exact elliptic factors')
        L=trans([eye(6,k)[i] for i in (0,3,5)]);require(rank(cat(F,L),k)==6 and rank(mm(V,L,k),k)==3,'Honda complement')
        badL=trans([eye(6,k)[i] for i in (0,1,3)]);require(rank(cat(F,badL),k)<6 and rank(mm(V,badL,k),k)<3,'bad Honda mutant rejected')
        broken=[r[:] for r in V];broken[5][0]=k.z;require(rank(F,k)+rank(broken,k)<6,'broken arrow exactness mutant')
        rows.append({'p':p,'flag_factors':3,'Honda':True,'bad_Honda_rejected':True,'missing_V_arrow_rejected':True})
    return rows
def rational_mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in trans(b)] for row in a]
def rational_inv(a):
    n=len(a);r=[[Fraction(x) for x in row]+[Fraction(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        q=next(i for i in range(j,n) if r[i][j]);r[j],r[q]=r[q],r[j];c=r[j][j];r[j]=[x/c for x in r[j]]
        for i in range(n):
            if i!=j:c=r[i][j];r[i]=[x-c*y for x,y in zip(r[i],r[j])]
    return [row[n:] for row in r]
def integral_basis(p,a):
    cols=[[0,1,0,1,0,1],[p,0,1,0,1,0],[0,-a[3],0,a[1],0,0],[-p*a[2],0,a[0],0,0,0],[Fraction(1,a[0]),0,0,0,0,0],[0,Fraction(1,a[1]),0,0,0,0]]
    return trans(cols)
def rational_det(T):
    n=len(T);v=0
    for perm in itertools.permutations(range(n)):
        s=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n));term=Fraction(s)
        for i,j in enumerate(perm):term*=T[i][j]
        v+=term
    return v
def integral():
    rows=[]
    for p in (5,7,11):
        for a in ([1,5,2,7,-3,-12],[2,1,9,3,-11,-4]):
            F=[[0]*6 for _ in range(6)];V=[[0]*6 for _ in range(6)]
            for j,w in enumerate((0,0,1,0,1,1)):F[(j+1)%6][j]=p**w;V[j][(j+1)%6]=p**(1-w)
            T=integral_basis(p,a);Q=rational_inv(T);sig=a[1:]+a[:1];tau=a[-1:]+a[:-1]
            require(rational_det(T)==1,'integral full determinant')
            for A,b in ((F,sig),(V,tau)):
                C=rational_mm(rational_mm(Q,A),integral_basis(p,b))
                for d in (2,4):require(all(C[i][j]==0 for i in range(d,6) for j in range(d)),'integral flag stable')
                for s in (0,2,4):require([[C[i][j] for j in range(s,s+2)] for i in range(s,s+2)]==[[0,p],[1,0]],'integral actual S factor')
            plain=rational_mm(rational_mm(Q,F),T);require(any([[plain[i][j] for j in range(s,s+2)] for i in range(s,s+2)]!=[[0,p],[1,0]] for s in (0,2,4)),'unshifted coefficient mutant')
            pi=[[a[0],0,p*a[2],0,p*a[4],0],[0,a[1],0,a[3],0,a[5]]]
            for A,b in ((F,sig),(V,tau)):
                pis=[[b[0],0,p*b[2],0,p*b[4],0],[0,b[1],0,b[3],0,b[5]]]
                require(rational_mm(pi,A)==rational_mm([[0,p],[1,0]],pis),'twelve quotient semilinear coefficient identities')
            # Wrong trace keeps a valid morphism but no longer places D1 in its kernel.
            bad=a[:];bad[4]+=1;badpi=[[bad[0],0,p*bad[2],0,p*bad[4],0],[0,bad[1],0,bad[3],0,bad[5]]]
            require(any(x!=0 for row in rational_mm(badpi,[row[:2] for row in T]) for x in row),'trace-zero-kernel mutation')
            badT=[row[:] for row in T]
            for row in badT:row[0]*=p
            require(rational_det(badT)==p,'unsaturated flag mutation nonunit')
            rows.append({'p':p,'a':a,'determinant':1,'six_factors_checked':True,'quotient_identities':True,'unshifted_coefficients_rejected':True,'wrong_trace_rejected':True,'nonunit_determinant_rejected':True})
    return rows
def finite_kernel_failure():
    rows=[]
    for p in (5,7):
        middle=[x for x in range(p*p) if p*x%(p*p)==0];image={x%p for x in middle}
        require(image=={0} and len(middle)==p,'finite p-kernel not right exact')
        rows.append({'p':p,'Z_p2_p_kernel_image':sorted(image),'quotient_p_kernel_size':p,'right_exactness_rejected':True})
    return rows
def main():
    fields_rows,cycle=fields();result={'status':'PASS','field_controls':fields_rows,'six_step_scalar_negative':cycle,'finite_flag_and_Honda_controls':prime_flag(),'integral_rational_evaluations':integral(),'finite_kernel_negative':finite_kernel_failure(),'checks':COUNT,'limitations':'Fresh finite independent arithmetic corroborates symbolic proof; rational evaluations do not prove Laurent universality; no author code imported, no external classification or priority certified.'}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()

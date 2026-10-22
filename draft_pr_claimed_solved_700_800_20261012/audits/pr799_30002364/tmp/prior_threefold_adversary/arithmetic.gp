\\ Exact arithmetic for the prior threefold route. Requires PARI/GP.
\\ This checks arithmetic and invariant-space dimensions, not the cited theorems.
check(c,s)=if(!c,error(s));
P=x^6-2*x^5+x^4+2*x^2-8*x+8;
R=x^3-2*x^2-5*x+8;
check(polisirreducible(P),"P is reducible");
check(simplify(x^3*subst(R,x,x+2/x)-P)==0,"Weil transform");
check(polsturm(R,[-14/5,14/5])==3,"Real roots not isolated");
check((14/5)^2<8,"Isolating interval outside Weil interval");
check(polgalois(P)[1]==12,"Wrong Galois group order");

\\ A degree-12 field in which all six roots split is the normal closure.
L=y^12-14*y^10+109*y^8-356*y^6+452*y^4-352*y^2+1024;
check(polisirreducible(L),"L is reducible");
N=nfinit(L);
rr=nfroots(N,P);
check(#rr==6,"P does not split in L");
check(nfrootsof1(N)[1]==2,"Unexpected roots of unity");
check(polresultant(P,subst(P,x,-x),x)==33554432,"Opposite root control");
for(i=1,6,for(j=i+1,6,check(rr[i]/rr[j]!=1 && rr[i]/rr[j]!=-1,"Root ratio torsion")));

pr=idealprimedec(N,2);
check(#pr==6,"Wrong number of 2-adic primes");
for(j=1,#pr,check(pr[j][3]==2 && pr[j][4]==1,"Wrong local e,f"));
M=matrix(6,#pr,i,j,idealval(N,rr[i],pr[j]));
check(matrank(M)==3,"Wrong Frobenius multiplicative rank");
check(vecsort(vector(6,i,M[i,1]/2))==[0,0,1/2,1/2,1,1],"Wrong slopes");
partners=vector(6,i,0);
for(i=1,6,for(j=1,6,if(rr[i]*rr[j]==2,partners[i]=j)));
for(i=1,6,check(partners[i]!=0 && partners[i]!=i,"Conjugate partner missing"));

\\ Factor P over Q(u), u^2=-8, and independently exhibit an exotic wedge.
u=Mod(y,y^2+8);
C1=x^3-x^2-u*x/2+u;
C2=x^3-x^2+u*x/2-u;
check(C1*C2==P,"Quadratic cubic factorization");
S=[];
for(i=1,4,for(j=i+1,5,for(k=j+1,6,if((rr[i]*rr[j]*rr[k])^2==-8,S=[i,j,k]))));
check(#S==3,"Exotic triple missing");
for(i=1,3,for(j=i+1,3,check(partners[S[i]]!=S[j],"Triple contains a conjugate pair")));
alpha=prod(i=1,3,rr[S[i]]);
check(alpha^2/2^3==-1,"Wrong normalized wedge eigenvalue");
check((alpha^2/2^3)^2==1,"Wedge not Tate after quadratic extension");
bad=S;bad[1]=partners[S[1]];
control=prod(i=1,3,rr[bad[i]])^2/2^3;
check(control!=1 && control!=-1,"Swapped-root negative control is Tate");

\\ Enumerate exponent vectors on A^m; binomial factors count exterior wedges.
\\ A Tate exponent has zero valuations after the q^r twist. Kronecker gives
\\ a root of unity; the exact roots-of-unity computation restricts it to +-1.
counts(m)={
  my(T=vector(3*m+1,i,0),D=vector(3*m+1,i,0),e,d,r,w,tate,paired);
  for(n=0,(m+1)^6-1,
    e=vector(6,i,(n\(m+1)^(i-1))%(m+1));d=sum(i=1,6,e[i]);
    if(d%2==0,
      r=d/2;w=prod(i=1,6,binomial(m,e[i]));
      tate=1;for(j=1,#pr,if(sum(i=1,6,e[i]*M[i,j])!=2*r,tate=0));
      paired=1;for(i=1,6,if(e[i]!=e[partners[i]],paired=0));
      if(tate,T[r+1]+=w);if(paired,D[r+1]+=w);
      check(!paired || tate,"Divisor monomial failed to be Tate")
    )
  );[T,D]
};
one=counts(1);two=counts(2);
check(one==[[1,3,3,1],[1,3,3,1]],"A itself control failed");
check(two==[[1,12,51,90,51,12,1],[1,12,51,88,51,12,1]],"Square invariant count failed");
print("pari_version=",version());
print("P=",P);print("normal_closure=",L);
print("prime_valuation_matrix=",M);
print("angle_rank=",matrank(M)-1);
print("root_of_unity_order=",nfrootsof1(N)[1]);
print("conjugate_partners=",partners);
print("witness_root_indices=",S);
print("normalized_witness_eigenvalue=",alpha^2/2^3);
print("A_tate_divisor_dimensions=",one);
print("A_square_tate_divisor_dimensions=",two);
print("AUDIT_OK");

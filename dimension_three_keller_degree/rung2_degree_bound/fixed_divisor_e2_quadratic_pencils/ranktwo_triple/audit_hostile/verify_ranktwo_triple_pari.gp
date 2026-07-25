\\ Independent hostile PARI/GP audit of the fixed-divisor e=2,
\\ rank-two triple-companion exclusion.

die(msg) = { print(Str("FAIL: ", msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };
checkeq(got,want,msg) =
{
  if(got!=want,die(Str(msg, ": got ",got,", want ",want)));
};

xyz = [x,y,z];

homexps(n) =
{
  my(out=List());
  forstep(i=n,0,-1,
    forstep(j=n-i,0,-1,
      listput(out,[i,j,n-i-j])
    )
  );
  Vec(out);
};

monoms(n) =
{
  my(E=homexps(n));
  vector(#E,i,x^E[i][1]*y^E[i][2]*z^E[i][3]);
};

coeffxyz(f,e) =
{
  polcoeff(polcoeff(polcoeff(f,e[1],x),e[2],y),e[3],z);
};

hcoeffs(f,n) =
{
  my(E=homexps(n));
  vector(#E,i,coeffxyz(f,E[i]));
};

coeffmon(f,m) =
{
  coeffxyz(f,[poldegree(m,x),poldegree(m,y),poldegree(m,z)]);
};

jacvec(hh) = matrix(3,3,i,j,deriv(hh[i],xyz[j]));
jac3(f,g,h) = matdet(jacvec([f,g,h]));

zero_vars(f,vv) =
{
  my(g=f);
  for(i=1,#vv,g=subst(g,vv[i],0));
  g;
};

subst_many(f,vv,ww) =
{
  my(g=f);
  check(#vv==#ww,"subst_many length mismatch");
  for(i=1,#vv,g=subst(g,vv[i],ww[i]));
  g;
};

is_affine_linear(f,n,vv) =
{
  my(cc=hcoeffs(f,n));
  for(i=1,#cc,
    my(rebuilt=zero_vars(cc[i],vv));
    for(j=1,#vv,rebuilt+=deriv(cc[i],vv[j])*vv[j]);
    if(cc[i]!=rebuilt,return(0));
  );
  1;
};

linear_system(f,n,vv) =
{
  my(cc=hcoeffs(f,n));
  my(M=matrix(#cc,#vv,i,j,deriv(cc[i],vv[j])));
  my(rhs=vector(#cc,i,-zero_vars(cc[i],vv))~);
  [M,rhs];
};

vector_complement(n,indices) =
{
  my(L=List(),S=Set(indices));
  for(i=1,n,if(!setsearch(S,i),listput(L,i)));
  Vec(L);
};

pivot_solution(M,rhs,unknowns,rows,pivots) =
{
  my(free=vector_complement(#unknowns,pivots));
  my(square=vecextract(M,rows,pivots));
  my(freepart=if(#free,
    vecextract(M,rows,free)*vector(#free,i,unknowns[free[i]])~,
    vector(#rows)~));
  my(pivotvalues=matsolve(square,vecextract(rhs,rows)-freepart));
  my(sol=unknowns~);
  for(i=1,#pivots,sol[pivots[i]]=pivotvalues[i]);
  [sol,pivots,free,M*sol-rhs];
};

lookup_solution(vv,ww,target) =
{
  for(i=1,#vv,if(vv[i]==target,return(ww[i])));
  die(Str("solution lookup failed for ",target));
};

is_rational_constant(v) =
{
  type(v)=="t_INT" || type(v)=="t_FRAC";
};

is_nested_polynomial(v) =
{
  my(T=type(v));
  if(T=="t_INT" || T=="t_FRAC",return(1));
  if(T!="t_POL",return(0));
  for(i=0,poldegree(v),if(!is_nested_polynomial(polcoeff(v,i)),return(0)));
  1;
};

associate(a,b) =
{
  if(a==0 || b==0,return(a==0 && b==0));
  my(ratio=simplify(a/b));
  is_rational_constant(ratio) && a==ratio*b;
};

check_residual_generators(residual,targets,label) =
{
  my(seen=vector(#targets),nonzero=0);
  for(i=1,#residual,
    if(residual[i]!=0,
      nonzero++;
      my(hit=0);
      for(j=1,#targets,
        if(associate(residual[i],targets[j]),seen[j]=1;hit=1)
      );
      check(hit,Str(label,": unexpected residual ",residual[i]));
    )
  );
  check(nonzero>0,Str(label,": no compatibility residuals"));
  for(j=1,#targets,check(seen[j],Str(label,": missing target ",targets[j])));
};

cleared_left_data(M,rhs) =
{
  my(N=matker(M~),pairs=List(),vectors=List());
  for(j=1,matsize(N)[2],
    my(den=1,v,pair);
    for(i=1,matsize(N)[1],den*=denominator(N[i,j]));
    v=den*N[,j];
    for(i=1,#v,checkeq(denominator(v[i]),1,
      Str("cleared left vector ",j," is not polynomial")));
    checkeq(M~*v,vector(matsize(M)[2])~,
      Str("cleared left vector ",j," is not a syzygy"));
    pair=v~*rhs;
    listput(vectors,v);
    listput(pairs,pair);
  );
  [Vec(vectors),Vec(pairs)];
};

direction_column(direction) =
{
  concat(concat(hcoeffs(direction[1],3),hcoeffs(direction[2],3)),
         hcoeffs(direction[3],2))~;
};

m2=monoms(2);
m3=monoms(3);
aall=[a0,a1,a2,a3,a4,a5];
ball=[b0,b1,b2,b3,b4,b5];
ell=[l0,l1,l2,l3,l4,l5,l6,l7,l8];
alllower=concat(concat(aall,ball),ell);
Lmat=matrix(3,3,i,j,ell[3*(i-1)+j]);

P=x^4;
Q=x^2*y*z;
R=x^3;

weighted_determinant(U,V,W) =
{
  my(H2=[sum(i=1,6,aall[i]*m2[i]),sum(i=1,6,ball[i]*m2[i]),W]);
  my(H3=[U,V,R],H4=[P,Q,0]);
  matdet(Lmat+t*jacvec(H2)+t^2*jacvec(H3)+t^3*jacvec(H4));
};

print("PARI hostile audit: raw E7 completeness and legal gauges");

uu=[u0,u1,u2,u3,u4,u5,u6,u7,u8,u9];
vv=[v0,v1,v2,v3,v4,v5,v6,v7,v8,v9];
ww=[ww0,ww1,ww2,ww3,ww4,ww5];
rawvars=concat(concat(uu,vv),ww);
rawU=sum(i=1,10,uu[i]*m3[i]);
rawV=sum(i=1,10,vv[i]*m3[i]);
rawW=sum(i=1,6,ww[i]*m2[i]);
rawE7=jac3(P,Q,rawW)+jac3(P,rawV,R)+jac3(rawU,Q,R);
checkeq(jac3(P,Q,R),0,"top E8 identity");
check(is_affine_linear(rawE7,7,rawvars),"raw E7 nonlinear");
rawsys=linear_system(rawE7,7,rawvars);
rawM=rawsys[1]; rawrhs=rawsys[2];
checkeq(matsize(rawM),[36,26],"raw E7 matrix shape");
checkeq(rawrhs,vector(36)~,"raw E7 inhomogeneous");
checkeq(matrank(rawM),8,"raw E7 rank");
rawrows=[2,3,4,6,7,8,9,10];
rawcols=[2,3,4,6,7,8,9,10];
checkeq(matdet(vecextract(rawM,rawrows,rawcols)),236196, \
  "raw E7 maximal minor");

translations=[ \
  [deriv(P,x),deriv(Q,x),deriv(R,x)], \
  [deriv(P,y),deriv(Q,y),deriv(R,y)], \
  [deriv(P,z),deriv(Q,z),deriv(R,z)] \
];
gauges=[[R,0,0],[0,R,0],translations[1],translations[2],translations[3]];
normals=[ \
  [4/3*x^2*y,0,x*y], \
  [4/3*x^2*z,0,x*z], \
  [4/3*x*y^2,0,y^2], \
  [0,0,y*z], \
  [4/3*x*z^2,0,z^2], \
  [x*y*z,0,0], \
  [0,x*y^2,0], \
  [0,x*y*z,0], \
  [0,x*z^2,0], \
  [0,y^3,0], \
  [0,y^2*z,0], \
  [0,y*z^2,0], \
  [0,z^3,0] \
];
dirs=concat(gauges,normals);
rawK=matrix(26,18,i,j,direction_column(dirs[j])[i]);
checkeq(rawM*rawK,matrix(36,18),"raw claimed kernel directions");
checkeq(matrank(rawK),18,"raw kernel direction independence");
krows=[1,2,3,4,5,6,11,12,13,14,15,16,17,18,19,20,21,25];
checkeq(matdet(vecextract(rawK,krows,[1..18])),256/27, \
  "raw kernel independence minor");
checkeq(26-matrank(rawM),18,"raw E7 nullity");
gaugeK=matrix(26,5,i,j,direction_column(gauges[j])[i]);
checkeq(matrank(gaugeK),5,"five legal gauge vectors independent");
checkeq(matrank(concat(gaugeK, \
  matrix(26,13,i,j,direction_column(normals[j])[i]))),18, \
  "gauge and normal direct sum");

\\ Explicitly check what the five transformations do at degrees (3,3,2).
checkeq(gauges[1],[R,0,0],"first target shear");
checkeq(gauges[2],[0,R,0],"second target shear");
for(j=1,3, \
  checkeq(gauges[j+2], \
    [deriv(P,xyz[j]),deriv(Q,xyz[j]),deriv(R,xyz[j])], \
    Str("source-translation tangent ",j)) \
);

U=A*x*y*z+4/3*(w1*x^2*y+w2*x^2*z+w3*x*y^2+w5*x*z^2);
V=B1*x*y^2+B2*x*y*z+B3*x*z^2+B4*y^3+B5*y^2*z+B6*y*z^2+B7*z^3;
W=w1*x*y+w2*x*z+w3*y^2+w4*y*z+w5*z^2;
normal_display=[U,V,W];
normal_pars=[w1,w2,w3,w4,w5,A,B1,B2,B3,B4,B5,B6,B7];
normal_combo=vector(3,i,sum(j=1,13,normal_pars[j]*normals[j][i]));
checkeq(normal_combo,normal_display,"normal-form reconstruction");

print("PASS raw E7: rank 8/nullity 18; five legal gauges plus thirteen normals form the full kernel");

print("PARI hostile audit: global E6 compatibility");

weighted=weighted_determinant(U,V,W);
for(k=7,9,checkeq(polcoeff(weighted,k,t),0,Str("normal E",k)));
E6=polcoeff(weighted,6,t);
check(is_affine_linear(E6,6,alllower),"general E6 nonlinear in lower data");
sys6=linear_system(E6,6,alllower);
M6=sys6[1]; rhs6=sys6[2];
checkeq(matrank(M6),4,"general E6 rank");
rows6=[2,3,4,6];
cols6=[2,3,4,6];
checkeq(matdet(vecextract(M6,rows6,cols6)),324, \
  "general E6 constant maximal minor");
solve6=pivot_solution(M6,rhs6,alllower,rows6,cols6);
res6=solve6[4];
check(sum(i=1,#res6,associate(res6[i],w3^2))>0, \
  "global E6 missing w3^2 compatibility");
check(sum(i=1,#res6,associate(res6[i],w5^2))>0, \
  "global E6 missing w5^2 compatibility");
res6reduced=vector(#res6,i,subst(subst(res6[i],w3,0),w5,0));
check_residual_generators(res6reduced, \
  [(9*A-12*w4)*B4, \
   (9*A-12*w4)*B5+(-3*A+8*w4)*w1, \
   (9*A-12*w4)*B6+(-3*A+8*w4)*w2, \
   (9*A-12*w4)*B7], \
  "global E6");

print("PASS E6: constant pivot makes w3=w5=0 and the K/M split specialization-safe");

print("PARI hostile audit: K!=0 compatibility and resultant");

openw4=(9*A-K)/12;
openM=(9*A-2*K)/3;
openU=A*x*y*z+4/3*(w1*x^2*y+w2*x^2*z);
openV=B1*x*y^2+B2*x*y*z+B3*x*z^2 \
      -openM*w1/K*y^2*z-openM*w2/K*y*z^2;
openW=w1*x*y+w2*x*z+openw4*y*z;
openweighted=weighted_determinant(openU,openV,openW);
for(k=7,9,checkeq(polcoeff(openweighted,k,t),0,Str("K-open E",k)));
opensys6=linear_system(polcoeff(openweighted,6,t),6,alllower);
openM6=opensys6[1]; openrhs6=opensys6[2];
checkeq(matrank(openM6),4,"K-open E6 rank");
checkeq(matdet(vecextract(openM6,rows6,cols6)),324, \
  "K-open E6 constant minor");
opensolve6=pivot_solution(openM6,openrhs6,alllower,rows6,cols6);
checkeq(opensolve6[4],vector(28)~,"K-open E6 residual");
openE5=subst_many(polcoeff(openweighted,5,t),alllower,opensolve6[1]);
openfree=vector(#opensolve6[3],i,alllower[opensolve6[3][i]]);
check(is_affine_linear(openE5,5,openfree),"K-open E5 nonlinear");
opensys5=linear_system(openE5,5,openfree);
openM5=opensys5[1]; openrhs5=opensys5[2];
checkeq(matrank(openM5),6,"K-open E5 generic rank");
openleft=cleared_left_data(openM5,openrhs5);
openpairs=openleft[2];
openS=(9*A-2*K)*(9*A-K);
opentargets=[ \
  w1*(3*B1*K+4*w1^2), \
  w2*(3*B3*K+4*w2^2), \
  -B1*openS+4*K*w1^2, \
  -B3*openS+4*K*w2^2, \
  A*w1*openS/K, \
  A*w2*openS/K \
];
for(j=1,#opentargets, \
  check(sum(i=1,#openpairs,associate(openpairs[i],opentargets[j]))>0, \
    Str("K-open E5 missing target ",j)) \
);
checkeq(sum(i=1,#openpairs,openpairs[i]!=0),6, \
  "K-open E5 nonzero compatibility count");

openresultant=polresultant(3*B1*K+4*w1^2, \
  -B1*openS+4*K*w1^2,B1);
openH=81*A^2-27*A*K+5*K^2;
checkeq(openresultant,4*w1^2*openH,"K-open resultant");
checkeq(subst(openH,A,0),5*K^2,"K-open A=0 value");
checkeq(subst(openH,A,2*K/9),3*K^2,"K-open 9A=2K value");
checkeq(subst(openH,A,K/9),3*K^2,"K-open 9A=K value");

print("PASS K!=0 E5: polynomial left syzygies and exact resultant force w1=w2=0, leaving only S=0");

print("PARI hostile audit: aligned K!=0 determinant exit");

alignU=A*x*y*z;
alignV=B2*x*y*z;
alignW=w4*y*z;
alignweighted=weighted_determinant(alignU,alignV,alignW);
alignsys6=linear_system(polcoeff(alignweighted,6,t),6,alllower);
alignsolve6=pivot_solution(alignsys6[1],alignsys6[2], \
  alllower,rows6,cols6);
checkeq(alignsolve6[4],vector(28)~,"aligned E6 residual");
alignE5=subst_many(polcoeff(alignweighted,5,t),alllower,alignsolve6[1]);
alignfree=vector(#alignsolve6[3],i,alllower[alignsolve6[3][i]]);
alignsys5=linear_system(alignE5,5,alignfree);
alignM5=alignsys5[1]; alignrhs5=alignsys5[2];
checkeq(matrank(alignM5),6,"aligned E5 generic rank");
alignidx=matindexrank(alignM5);
alignminor=matdet(vecextract(alignM5,alignidx[1],alignidx[2]));
alignD=-3*A+4*w4;
checkeq(alignminor, \
  -4/9*(3*A-8*w4)^2*(3*A-4*w4)^4, \
  "aligned E5 localized pivot");
alignsolve5=pivot_solution(alignM5,alignrhs5,alignfree, \
  alignidx[1],alignidx[2]);
checkeq(alignsolve5[4],vector(21)~,"aligned E5 residual");
alignsub6=alignsolve6[1];
alignsub5=alignsolve5[1];
alignE4=subst_many( \
  subst_many(polcoeff(alignweighted,4,t),alllower,alignsub6), \
  alignfree,alignsub5);
checkeq(lookup_solution(alignfree,alignsub5,ell[8]),0, \
  "aligned E5 l32");
checkeq(lookup_solution(alignfree,alignsub5,ell[9]),0, \
  "aligned E5 l33");
aligncy=coeffmon(alignE4,x^3*y);
aligncz=coeffmon(alignE4,x^3*z);
aligncommon=3*B2*alignD+9*aall[5];
checkeq(aligncy, \
  (alignD^2*ell[5]+aligncommon*ell[2])/alignD, \
  "aligned E4 x3y coefficient");
checkeq(aligncz, \
  -(alignD^2*ell[6]+aligncommon*ell[3])/alignD, \
  "aligned E4 x3z coefficient");
alignminorL=ell[2]*ell[6]-ell[3]*ell[5];
checkeq(ell[2]*(-alignD*aligncz)-ell[3]*(alignD*aligncy), \
  alignD^2*alignminorL,"aligned E4 elimination identity");
alignLdet=subst_many( \
  subst_many(matdet(Lmat),alllower,alignsub6),alignfree,alignsub5);
checkeq(alignLdet,ell[7]*alignminorL, \
  "aligned determinant factorization");

print("PASS aligned nonresonant K!=0: E5 localization is exactly (3A-8w4)(3A-4w4), and E4 forces det(L)=0");

print("PARI hostile audit: 9A=2K resonance, including its aligned rank drop");

r2aU=A*x*y*z;
r2aV=B1*x*y^2+B2*x*y*z+B3*x*z^2;
r2aW=3/8*A*y*z;
r2aw=weighted_determinant(r2aU,r2aV,r2aW);
r2as6=linear_system(polcoeff(r2aw,6,t),6,alllower);
r2asol6=pivot_solution(r2as6[1],r2as6[2],alllower,rows6,cols6);
checkeq(r2asol6[4],vector(28)~,"9A=2K E6 residual");
r2aE5=subst_many(polcoeff(r2aw,5,t),alllower,r2asol6[1]);
r2afree=vector(#r2asol6[3],i,alllower[r2asol6[3][i]]);
r2as5=linear_system(r2aE5,5,r2afree);
checkeq(matrank(r2as5[1]),4,"9A=2K E5 rank");
r2aidx=matindexrank(r2as5[1]);
r2amin=matdet(vecextract(r2as5[1],r2aidx[1],r2aidx[2]));
checkeq(r2amin,-81/2*B3*A^3,"9A=2K nonzero-end E5 pivot");
r2asol5=pivot_solution(r2as5[1],r2as5[2],r2afree,r2aidx[1],r2aidx[2]);
checkeq(r2asol5[4],vector(21)~,"9A=2K E5 residual");
r2aE4=subst_many( \
  subst_many(polcoeff(r2aw,4,t),alllower,r2asol6[1]), \
  r2afree,r2asol5[1]);
checkeq(coeffmon(r2aE4,z^4),3/8*A^2*B3^2, \
  "9A=2K nonzero-end obstruction");
checkeq(subst(subst(subst(r2aU,y,zz),z,y),zz,z),r2aU, \
  "9A=2K U y/z invariance");
checkeq(subst(subst(subst(P,y,zz),z,y),zz,z),P, \
  "P y/z invariance");
checkeq(subst(subst(subst(Q,y,zz),z,y),zz,z),Q, \
  "Q y/z invariance");
checkeq(subst(subst(subst(R,y,zz),z,y),zz,z),R, \
  "R y/z invariance");
checkeq(subst(subst(subst(r2aV,y,zz),z,y),zz,z), \
  B3*x*y^2+B2*x*y*z+B1*x*z^2, \
  "9A=2K V swaps the two ends");

r2bU=A*x*y*z;
r2bV=B2*x*y*z;
r2bW=3/8*A*y*z;
r2bw=weighted_determinant(r2bU,r2bV,r2bW);
r2bs6=linear_system(polcoeff(r2bw,6,t),6,alllower);
r2bsol6=pivot_solution(r2bs6[1],r2bs6[2],alllower,rows6,cols6);
checkeq(r2bsol6[4],vector(28)~,"9A=2K aligned E6 residual");
r2bE5=subst_many(polcoeff(r2bw,5,t),alllower,r2bsol6[1]);
r2bfree=vector(#r2bsol6[3],i,alllower[r2bsol6[3][i]]);
r2bs5=linear_system(r2bE5,5,r2bfree);
checkeq(matrank(r2bs5[1]),4,"9A=2K aligned E5 rank");
r2bidx=matindexrank(r2bs5[1]);
r2bmin=matdet(vecextract(r2bs5[1],r2bidx[1],r2bidx[2]));
checkeq(r2bmin,81/4*A^4,"9A=2K aligned E5 pivot");
r2bsol5=pivot_solution(r2bs5[1],r2bs5[2],r2bfree, \
  r2bidx[1],r2bidx[2]);
checkeq(r2bsol5[4],vector(21)~,"9A=2K aligned E5 residual");
r2alignedE4=subst_many( \
  subst_many(polcoeff(r2bw,4,t),alllower,r2bsol6[1]), \
  r2bfree,r2bsol5[1]);
r2alignedDet=subst_many( \
  subst_many(matdet(Lmat),alllower,r2bsol6[1]),r2bfree,r2bsol5[1]);
checkeq(coeffmon(r2alignedE4,x^2*y^2),-4/3*ell[8]^2, \
  "9A=2K aligned E4 l32 square");
checkeq(coeffmon(r2alignedE4,x^2*z^2),4/3*ell[9]^2, \
  "9A=2K aligned E4 l33 square");
r2zeroE4=subst(subst(r2alignedE4,ell[8],0),ell[9],0);
r2T=3*B2-6*aall[5]/A;
r2cy=coeffmon(r2zeroE4,x^3*y);
r2cz=coeffmon(r2zeroE4,x^3*z);
checkeq(r2cy,r2T*ell[2]-3/2*A*ell[5], \
  "9A=2K aligned x3y row");
checkeq(r2cz,-r2T*ell[3]+3/2*A*ell[6], \
  "9A=2K aligned x3z row");
r2minorL=ell[2]*ell[6]-ell[3]*ell[5];
checkeq(ell[3]*r2cy+ell[2]*r2cz,3/2*A*r2minorL, \
  "9A=2K aligned elimination");
checkeq(subst(subst(r2alignedDet,ell[8],0),ell[9],0), \
  ell[7]*r2minorL,"9A=2K aligned determinant factorization");

print("PASS 9A=2K: nonzero ends are excluded by z4 after y/z symmetry; the freshly solved aligned rank-drop chart also forces det(L)=0");

print("PARI hostile audit: 9A=K resonance");

r1U=A*x*y*z;
r1V=B1*x*y^2+B2*x*y*z+B3*x*z^2;
r1W=0;
r1weighted=weighted_determinant(r1U,r1V,r1W);
r1sys6=linear_system(polcoeff(r1weighted,6,t),6,alllower);
r1solve6=pivot_solution(r1sys6[1],r1sys6[2],alllower,rows6,cols6);
checkeq(r1solve6[4],vector(28)~,"9A=K E6 residual");
r1E5=subst_many(polcoeff(r1weighted,5,t),alllower,r1solve6[1]);
r1free=vector(#r1solve6[3],i,alllower[r1solve6[3][i]]);
r1sys5=linear_system(r1E5,5,r1free);
checkeq(matrank(r1sys5[1]),6,"9A=K E5 rank");
r1idx=matindexrank(r1sys5[1]);
r1minor=matdet(vecextract(r1sys5[1],r1idx[1],r1idx[2]));
checkeq(r1minor,324*B3*A^5,"9A=K E5 localized pivot");
r1solve5=pivot_solution(r1sys5[1],r1sys5[2],r1free, \
  r1idx[1],r1idx[2]);
checkeq(r1solve5[4],vector(21)~,"9A=K E5 residual");
checkeq(lookup_solution(r1free,r1solve5[1],ell[8]),0, \
  "9A=K E5 l32");
checkeq(lookup_solution(r1free,r1solve5[1],ell[9]),0, \
  "9A=K E5 l33");
r1E4=subst_many( \
  subst_many(polcoeff(r1weighted,4,t),alllower,r1solve6[1]), \
  r1free,r1solve5[1]);
r1cy=coeffmon(r1E4,x^3*y);
r1cz=coeffmon(r1E4,x^3*z);
checkeq(r1cy,-3*(A*B3*ell[5]-ball[6]*ell[2])/B3, \
  "9A=K x3y row");
checkeq(r1cz,3*(A*B3*ell[6]-ball[6]*ell[3])/B3, \
  "9A=K x3z row");
r1minorL=ell[2]*ell[6]-ell[3]*ell[5];
checkeq(ell[2]*(B3*r1cz/3)+ell[3]*(B3*r1cy/3), \
  A*B3*r1minorL,"9A=K elimination");
r1det=subst_many( \
  subst_many(matdet(Lmat),alllower,r1solve6[1]),r1free,r1solve5[1]);
checkeq(r1det,ell[7]*r1minorL,"9A=K determinant factorization");

print("PASS 9A=K: B3-localized solve forces det(L)=0; y/z symmetry covers B1-only, and the zero pair lies in the nonresonant aligned chart");

print("PARI hostile audit: K=0, A!=0 rank drop");

k0U=A*x*y*z;
k0V=B1*x*y^2+B2*x*y*z+B3*x*z^2+B4*y^3+B5*y^2*z+B6*y*z^2+B7*z^3;
k0W=3/4*A*y*z;
k0weighted=weighted_determinant(k0U,k0V,k0W);
k0sys6=linear_system(polcoeff(k0weighted,6,t),6,alllower);
k0solve6=pivot_solution(k0sys6[1],k0sys6[2],alllower,rows6,cols6);
checkeq(k0solve6[4],vector(28)~,"K=0,A!=0 E6 residual");
k0E5=subst_many(polcoeff(k0weighted,5,t),alllower,k0solve6[1]);
k0free=vector(#k0solve6[3],i,alllower[k0solve6[3][i]]);
k0sys5=linear_system(k0E5,5,k0free);
checkeq(matrank(k0sys5[1]),5,"K=0,A!=0 E5 generic rank");
k0left=cleared_left_data(k0sys5[1],k0sys5[2]);
k0pairs=k0left[2];
k0targets=[A^2*B1,A^2*B3,A^2*B4,A^2*B5,A^2*B6,A^2*B7];
for(j=1,#k0targets, \
  check(sum(i=1,#k0pairs,associate(k0pairs[i],k0targets[j]))>0, \
    Str("K=0,A!=0 missing E5 target ",j)) \
);
checkeq(sum(i=1,#k0pairs,k0pairs[i]!=0),6, \
  "K=0,A!=0 nonzero compatibility count");

k0aU=A*x*y*z;
k0aV=B2*x*y*z;
k0aW=3/4*A*y*z;
k0aw=weighted_determinant(k0aU,k0aV,k0aW);
k0as6=linear_system(polcoeff(k0aw,6,t),6,alllower);
k0asol6=pivot_solution(k0as6[1],k0as6[2],alllower,rows6,cols6);
checkeq(k0asol6[4],vector(28)~,"K=0 aligned E6 residual");
k0aE5=subst_many(polcoeff(k0aw,5,t),alllower,k0asol6[1]);
k0afree=vector(#k0asol6[3],i,alllower[k0asol6[3][i]]);
k0as5=linear_system(k0aE5,5,k0afree);
checkeq(matrank(k0as5[1]),4,"K=0 aligned E5 rank");
k0aidx=matindexrank(k0as5[1]);
k0amin=matdet(vecextract(k0as5[1],k0aidx[1],k0aidx[2]));
checkeq(k0amin,9*A^2,"K=0 aligned E5 pivot");
k0asol5=pivot_solution(k0as5[1],k0as5[2],k0afree, \
  k0aidx[1],k0aidx[2]);
checkeq(k0asol5[4],vector(21)~,"K=0 aligned E5 residual");
for(j=2,3, \
  checkeq(lookup_solution(k0afree,k0asol5[1],ell[j]),0, \
    Str("K=0 aligned first-row zero ",j)) \
);
for(j=8,9, \
  checkeq(lookup_solution(k0afree,k0asol5[1],ell[j]),0, \
    Str("K=0 aligned third-row zero ",j)) \
);
k0adet=subst_many( \
  subst_many(matdet(Lmat),alllower,k0asol6[1]),k0afree,k0asol5[1]);
checkeq(k0adet,0,"K=0 aligned determinant");

print("PASS K=0,A!=0: six E5 compatibilities leave only B2, and a fresh A-localized solve zeros four entries of L");

print("PARI hostile audit: K=A=0 cubic-tail syzygies");

origU=4/3*(w1*x^2*y+w2*x^2*z);
origV=B1*x*y^2+B2*x*y*z+B3*x*z^2+B4*y^3+B5*y^2*z+B6*y*z^2+B7*z^3;
origW=w1*x*y+w2*x*z;
origweighted=weighted_determinant(origU,origV,origW);
origsys6=linear_system(polcoeff(origweighted,6,t),6,alllower);
origsolve6=pivot_solution(origsys6[1],origsys6[2],alllower,rows6,cols6);
checkeq(origsolve6[4],vector(28)~,"origin E6 residual");
origE5=subst_many(polcoeff(origweighted,5,t),alllower,origsolve6[1]);
origfree=vector(#origsolve6[3],i,alllower[origsolve6[3][i]]);
origsys5=linear_system(origE5,5,origfree);
origleft=cleared_left_data(origsys5[1],origsys5[2]);
origpairs=origleft[2];
origtargets=[ \
  w1^2*(9*B4*w2-3*B5*w1+2*w1^2), \
  w1*(9*B4*w2^2-3*B6*w1^2+2*w1^2*w2), \
  -B4*w2^3+B7*w1^3 \
];
origindices=[3,4,5];
origconstants=[-4/81,4/81,-4/9];
for(j=1,3, \
  my(polyvector=B4*origleft[1][origindices[j]]); \
  for(i=1,#polyvector, \
    check(is_nested_polynomial(polyvector[i]), \
      Str("origin cross-multiplied vector ",j," entry ",i," is rational")) \
  ); \
  checkeq(origsys5[1]~*polyvector,vector(#origfree)~, \
    Str("origin polynomial left syzygy ",j)); \
  checkeq(polyvector~*origsys5[2],origconstants[j]*origtargets[j], \
    Str("origin cross-multiplied target ",j)) \
);

openorigU=4/3*s*(x^2*y+r*x^2*z);
openorigV=B1*x*y^2+B2*x*y*z+B3*x*z^2+C*y^3 \
  +(3*C*r+2/3*s)*y^2*z+(3*C*r^2+2/3*r*s)*y*z^2+C*r^3*z^3;
openorigW=s*x*y+r*s*x*z;
openorigweighted=weighted_determinant(openorigU,openorigV,openorigW);
openorigsys6=linear_system(polcoeff(openorigweighted,6,t),6,alllower);
openorigsolve6=pivot_solution(openorigsys6[1],openorigsys6[2], \
  alllower,rows6,cols6);
checkeq(openorigsolve6[4],vector(28)~,"origin open E6 residual");
openorigE5=subst_many(polcoeff(openorigweighted,5,t), \
  alllower,openorigsolve6[1]);
openorigfree=vector(#openorigsolve6[3],i, \
  alllower[openorigsolve6[3][i]]);
openorigsys5=linear_system(openorigE5,5,openorigfree);
checkeq(matrank(openorigsys5[1]),5,"origin open E5 rank");
openorigidx=matindexrank(openorigsys5[1]);
openorigminor=matdet(vecextract(openorigsys5[1], \
  openorigidx[1],openorigidx[2]));
checkeq(openorigminor,384*C*r^2*s^3, \
  "origin open E5 localized pivot");
openorigsolve5=pivot_solution(openorigsys5[1],openorigsys5[2], \
  openorigfree,openorigidx[1],openorigidx[2]);
checkeq(openorigsolve5[4],vector(21)~,"origin open E5 residual");
openorigE4=subst_many( \
  subst_many(polcoeff(openorigweighted,4,t),alllower,openorigsolve6[1]), \
  openorigfree,openorigsolve5[1]);
checkeq(coeffmon(openorigE4,y^4),4/27*s^4, \
  "origin open E4 y4 obstruction");

print("PASS K=A=0 open chart: necessary tail parametrization and an exact localized E5 solve give 4*s^4/27");

c0U=4/3*s*(x^2*y+r*x^2*z);
c0V=B1*x*y^2+B2*x*y*z+B3*x*z^2 \
  +2/3*s*y^2*z+2/3*r*s*y*z^2;
c0W=s*x*y+r*s*x*z;
c0weighted=weighted_determinant(c0U,c0V,c0W);
c0sys6=linear_system(polcoeff(c0weighted,6,t),6,alllower);
c0solve6=pivot_solution(c0sys6[1],c0sys6[2],alllower,rows6,cols6);
checkeq(c0solve6[4],vector(28)~,"origin C=0 E6 residual");
c0E5=subst_many(polcoeff(c0weighted,5,t),alllower,c0solve6[1]);
c0free=vector(#c0solve6[3],i,alllower[c0solve6[3][i]]);
c0sys5=linear_system(c0E5,5,c0free);
c0left=cleared_left_data(c0sys5[1],c0sys5[2]);
for(i=1,#c0left[1][3], \
  check(is_nested_polynomial(c0left[1][3][i]), \
    Str("origin C=0 left vector entry ",i," is rational")) \
);
checkeq(c0sys5[1]~*c0left[1][3],vector(#c0free)~, \
  "origin C=0 polynomial left syzygy");
checkeq(c0left[2][3],-4/9*s^3, \
  "origin C=0 literal s-cube obstruction");

r0U=4/3*s*x^2*y;
r0V=B1*x*y^2+B2*x*y*z+B3*x*z^2+C*y^3+2/3*s*y^2*z;
r0W=s*x*y;
r0weighted=weighted_determinant(r0U,r0V,r0W);
r0sys6=linear_system(polcoeff(r0weighted,6,t),6,alllower);
r0solve6=pivot_solution(r0sys6[1],r0sys6[2],alllower,rows6,cols6);
checkeq(r0solve6[4],vector(28)~,"origin r=0 E6 residual");
r0E5=subst_many(polcoeff(r0weighted,5,t),alllower,r0solve6[1]);
r0free=vector(#r0solve6[3],i,alllower[r0solve6[3][i]]);
r0sys5=linear_system(r0E5,5,r0free);
checkeq(matdet(vecextract(r0sys5[1],[2,3,4,6],[1,2,11,16])), \
  -96*B3*s^2,"origin r=0,B3!=0 explicit E5 pivot");
r0left=cleared_left_data(r0sys5[1],r0sys5[2]);
r0polyvector=B3*r0left[1][3];
for(i=1,#r0polyvector, \
  check(is_nested_polynomial(r0polyvector[i]), \
    Str("origin r=0,B3!=0 cross-multiplied vector entry ",i, \
        " is rational")) \
);
checkeq(r0sys5[1]~*r0polyvector,vector(#r0free)~, \
  "origin r=0,B3!=0 polynomial left syzygy");
checkeq(r0polyvector~*r0sys5[2],-4/9*B3*s^3, \
  "origin r=0,B3!=0 cross-multiplied cube obstruction");

r00U=4/3*s*x^2*y;
r00V=B1*x*y^2+B2*x*y*z+C*y^3+2/3*s*y^2*z;
r00W=s*x*y;
r00weighted=weighted_determinant(r00U,r00V,r00W);
r00sys6=linear_system(polcoeff(r00weighted,6,t),6,alllower);
r00solve6=pivot_solution(r00sys6[1],r00sys6[2],alllower,rows6,cols6);
checkeq(r00solve6[4],vector(28)~,"origin r=0,B3=0 E6 residual");
r00E5=subst_many(polcoeff(r00weighted,5,t),alllower,r00solve6[1]);
r00free=vector(#r00solve6[3],i,alllower[r00solve6[3][i]]);
r00sys5=linear_system(r00E5,5,r00free);
checkeq(matrank(r00sys5[1]),4,"origin r=0,B3=0 E5 rank");
r00idx=matindexrank(r00sys5[1]);
r00minor=matdet(vecextract(r00sys5[1],r00idx[1],r00idx[2]));
checkeq(r00minor,144*C*s^2,"origin r=0,B3=0 E5 pivot");
r00solve5=pivot_solution(r00sys5[1],r00sys5[2],r00free, \
  r00idx[1],r00idx[2]);
checkeq(r00solve5[4],vector(21)~,"origin r=0,B3=0 E5 residual");
r00E4=subst_many( \
  subst_many(polcoeff(r00weighted,4,t),alllower,r00solve6[1]), \
  r00free,r00solve5[1]);
checkeq(coeffmon(r00E4,y^4),4/27*s^4, \
  "origin r=0,B3=0 E4 y4 obstruction");

print("PASS K=A=0 rank drops: C=0 is global; r=0 splits safely into B3!=0 cross-multiplied E5 and B3=0 fresh E4 charts");

print("PARI hostile audit: K=A=w1=w2=0 terminal chart");

zeroU=0;
zeroV=B1*x*y^2+B2*x*y*z+B3*x*z^2+B4*y^3+B5*y^2*z+B6*y*z^2+B7*z^3;
zeroW=0;
zeroweighted=weighted_determinant(zeroU,zeroV,zeroW);
zerosys6=linear_system(polcoeff(zeroweighted,6,t),6,alllower);
zerosolve6=pivot_solution(zerosys6[1],zerosys6[2],alllower,rows6,cols6);
checkeq(zerosolve6[4],vector(28)~,"terminal E6 residual");
zeroE5=subst_many(polcoeff(zeroweighted,5,t),alllower,zerosolve6[1]);
zerofree=vector(#zerosolve6[3],i,alllower[zerosolve6[3][i]]);
zerosys5=linear_system(zeroE5,5,zerofree);
checkeq(matrank(zerosys5[1]),3,"terminal E5 rank");
zeroidx=matindexrank(zerosys5[1]);
zerominor=matdet(vecextract(zerosys5[1],zeroidx[1],zeroidx[2]));
checkeq(zerominor,54*B1,"terminal generic E5 localized minor");
checkeq(coeffmon(zeroE5,x^4*y),3*ell[2],"terminal global E5 l12");
checkeq(coeffmon(zeroE5,x^4*z),-3*ell[3],"terminal global E5 l13");
checkeq(coeffmon(zeroE5,x^3*y^2),-6*B1*aall[5], \
  "terminal global E5 B1 row");
checkeq(coeffmon(zeroE5,x^3*z^2),6*B3*aall[5], \
  "terminal global E5 B3 row");
checkeq(coeffmon(zeroE5,x^2*y^3),-9*B4*aall[5], \
  "terminal global E5 B4 row");
checkeq(coeffmon(zeroE5,x^2*y^2*z),-3*B5*aall[5], \
  "terminal global E5 B5 row");
checkeq(coeffmon(zeroE5,x^2*y*z^2),3*B6*aall[5], \
  "terminal global E5 B6 row");
checkeq(coeffmon(zeroE5,x^2*z^3),9*B7*aall[5], \
  "terminal global E5 B7 row");

zeroE4base=subst_many(polcoeff(zeroweighted,4,t), \
  alllower,zerosolve6[1]);
zeroE4rows=subst(subst(zeroE4base,ell[2],0),ell[3],0);
zeroE4a0=subst(zeroE4rows,aall[5],0);
checkeq(coeffmon(zeroE4a0,x^2*y^2),-4/3*ell[8]^2, \
  "terminal a4=0 E4 l32 square");
checkeq(coeffmon(zeroE4a0,x^2*z^2),4/3*ell[9]^2, \
  "terminal a4=0 E4 l33 square");

zeroends=[B1,B3,B4,B5,B6,B7];
zeroE4anonzero=zeroE4rows;
for(i=1,#zeroends,zeroE4anonzero=subst(zeroE4anonzero,zeroends[i],0));
checkeq(coeffmon(zeroE4anonzero,x*y^2*z),2*aall[5]*ell[8], \
  "terminal a4!=0 E4 l32 row");
checkeq(coeffmon(zeroE4anonzero,x*y*z^2),-2*aall[5]*ell[9], \
  "terminal a4!=0 E4 l33 row");

zerodetbase=subst_many(matdet(Lmat),alllower,zerosolve6[1]);
checkeq(subst(subst(subst(subst(zerodetbase, \
  ell[2],0),ell[3],0),ell[8],0),ell[9],0),0, \
  "terminal determinant");

print("PASS terminal chart: global literal E5 rows split on a4, and both branches force l32=l33 without the unsafe B1 localization");

print("ALL HOSTILE PARI/GP RANK-TWO e=2 TRIPLE-COMPANION CHECKS PASSED");

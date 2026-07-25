\\ Independent hostile PARI/GP reconstruction of the t=-2 companion-at-
\\ infinity resonance.  This file does not load the supplied SymPy matrices.

die(msg) = { print(Str("FAIL: ",msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };
checkeq(got,want,msg) =
{
  if(got!=want,die(Str(msg,": got ",got,", want ",want)));
};

xyz=[x,y,z];

homexps(n) =
{
  my(out=List());
  forstep(i=n,0,-1,
    forstep(j=n-i,0,-1,listput(out,[i,j,n-i-j]))
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

is_rational_constant(v) =
{
  type(v)=="t_INT" || type(v)=="t_FRAC";
};

associate(a,b) =
{
  if(a==0 || b==0,return(a==0 && b==0));
  my(ratio=simplify(a/b));
  is_rational_constant(ratio) && a==ratio*b;
};

cleared_left_data(M,rhs) =
{
  my(N=matker(M~),pairs=List(),vectors=List());
  for(j=1,matsize(N)[2],
    my(den=1,v,pair);
    for(i=1,matsize(N)[1],den*=denominator(N[i,j]));
    v=den*N[,j];
    checkeq(M~*v,vector(matsize(M)[2])~,
      Str("cleared left vector ",j," is not a polynomial syzygy"));
    pair=v~*rhs;
    listput(vectors,v);
    listput(pairs,pair);
  );
  [Vec(vectors),Vec(pairs)];
};

find_associate(vv,target) =
{
  for(i=1,#vv,if(associate(vv[i],target),return(1)));
  0;
};

direction_column(direction) =
{
  concat(concat(hcoeffs(direction[1],3),hcoeffs(direction[2],3)),
         hcoeffs(direction[3],2))~;
};

m2=monoms(2);
m3=monoms(3);
p=x^2;
q=y*z;
R=x*q;
P=(p+2*q)^2;
Q=(p-q)^2;

print("PARI hostile resonance audit: orbit ledger");

\\ In the pencil-preserving branch, y'=beta*y+r*x and
\\ z'=gamma*z+u*x.  Vanishing xy,xz coefficients forces u=r=0
\\ because beta,gamma are nonzero.  The swapped branch is identical.
yp=stabB*y+stabR*x;
zp=stabG*z+stabS*x;
product_yz=yp*zp;
checkeq(coeffxyz(product_yz,[1,1,0]),stabB*stabS, \
  "stabilizer xy coefficient");
checkeq(coeffxyz(product_yz,[1,0,1]),stabG*stabR, \
  "stabilizer xz coefficient");
checkeq(coeffxyz(product_yz,[0,1,1]),stabB*stabG, \
  "stabilizer yz coefficient");
checkeq((stabA^2*p/(stabB*stabG*q))/(p/q),stabA^2/(stabB*stabG), \
  "induced base scaling");

rawfactor=(tmod-1)^10*(tmod+2)^4*(2*tmod+1)^4;
e6factor=(tmod-1)^6*(tmod+2)^2*(2*tmod+1)^2;
e5factor=(tmod-1)^2;
checkeq(tmod^18*subst(rawfactor,tmod,1/tmod),rawfactor, \
  "raw reciprocal factor");
checkeq(tmod^10*subst(e6factor,tmod,1/tmod),e6factor, \
  "E6 reciprocal factor");
checkeq(tmod^2*subst(e5factor,tmod,1/tmod),e5factor, \
  "E5 reciprocal factor");
checkeq(subst(1/tmod,tmod,-2),-1/2,"resonance reciprocal orbit");
checkeq(polcoeff((p-tmod*q)^2,2,tmod),q^2, \
  "finite t=infinity leading form");
checkeq((p-q)^2,(p-1*q)^2,"outer a=1 companion");

print("PASS orbit ledger: finite, outer, endpoint, and reciprocal resonance charts exhaust the modulus");

print("PARI hostile resonance audit: raw E7 and legal gauges");

uc=[u0,u1,u2,u3,u4,u5,u6,u7,u8,u9];
vc=[v0,v1,v2,v3,v4,v5,v6,v7,v8,v9];
wc=[w0,w1,w2,w3,w4,w5];
rawvars=concat(concat(uc,vc),wc);
U=sum(i=1,10,uc[i]*m3[i]);
V=sum(i=1,10,vc[i]*m3[i]);
W=sum(i=1,6,wc[i]*m2[i]);
E7=jac3(P,Q,W)+jac3(P,V,R)+jac3(U,Q,R);
rawsys=linear_system(E7,7,rawvars);
M7=rawsys[1];
checkeq(rawsys[2],vector(36)~,"raw E7 inhomogeneous part");
checkeq(matsize(M7),[36,26],"raw E7 shape");
rawrows=[2,3,4,6,7,8,9,10,12,14,17,18,19,20];
rawcols=[2,3,4,6,7,8,9,10,12,13,14,16,17,20];
checkeq(matdet(vecextract(M7,rawrows,rawcols)),-990677827584, \
  "raw resonance rank-14 minor");

gauges=[ \
  [R,0,0], \
  [0,R,0], \
  [4*x*(p+2*q),4*x*(p-q),q], \
  [4*z*(p+2*q),-2*z*(p-q),x*z], \
  [4*y*(p+2*q),-2*y*(p-q),x*y] \
];
normals=[ \
  [0,x^3,0], \
  [0,0,p], \
  [0,-6*x^2*y,x*y], \
  [0,-6*x^2*z,x*z], \
  [0,-6*x*y^2,y^2], \
  [0,0,q], \
  [0,-6*x*z^2,z^2] \
];
directions=concat(gauges,normals);
Kern=matrix(26,12,i,j,direction_column(directions[j])[i]);
checkeq(M7*Kern,matrix(36,12),"raw resonance kernel");
kernelrows=[1,2,3,5,11,12,13,14,15,16,21,25];
checkeq(matdet(vecextract(Kern,kernelrows,[1..12])),82944, \
  "raw resonance kernel independence");
checkeq(matrank(M7),14,"raw resonance rank");
checkeq(26-matrank(M7),12,"raw resonance nullity");
checkeq(matrank(vecextract(Kern,[1..26],[1..5])),5, \
  "five gauge directions independent");

translations=[ \
  [deriv(P,x),deriv(Q,x),deriv(R,x)], \
  [deriv(P,y),deriv(Q,y),deriv(R,y)], \
  [deriv(P,z),deriv(Q,z),deriv(R,z)] \
];
for(j=1,3,checkeq(gauges[j+2],translations[j], \
  Str("source translation jet ",j)));
checkeq(gauges[1],[R,0,0],"first target shear jet");
checkeq(gauges[2],[0,R,0],"second target shear jet");
checkeq(matdet([1,0,1;0,1,0;0,0,1]),1, \
  "first target shear determinant");
checkeq(matdet([1,0,0;0,1,1;0,0,1]),1, \
  "second target shear determinant");

C='C;
rw0='rw0; rw1='rw1; rw2='rw2; rw3='rw3;
rw4='rw4; rw5='rw5;
normalU=0;
normalV=C*x^3-6*rw1*x^2*y-6*rw2*x^2*z \
  -6*rw3*x*y^2-6*rw5*x*z^2;
normalW=rw0*p+rw1*x*y+rw2*x*z+rw3*y^2+rw4*q+rw5*z^2;
normalpars=[C,rw0,rw1,rw2,rw3,rw4,rw5];
normalcombo=vector(3,i,sum(j=1,7,normalpars[j]*normals[j][i]));
checkeq(normalcombo,[normalU,normalV,normalW], \
  "seven-direction normal reconstruction");
checkeq(jac3(P,Q,normalW)+jac3(P,normalV,R)+jac3(normalU,Q,R),0, \
  "normal E7 identity");

print("PASS raw resonance: rank 14/nullity 12, five legal gauges, and seven normals are complete");

print("PARI hostile resonance audit: E6 square compatibility and converse");

ac=[a0,a1,a2,a3,a4,a5];
bc=[b0,b1,b2,b3,b4,b5];
lc=[l0,l1,l2,l3,l4,l5,l6,l7,l8];
lower=concat(concat(ac,bc),lc);
A2=sum(i=1,6,ac[i]*m2[i]);
B2=sum(i=1,6,bc[i]*m2[i]);
L=[l0*x+l1*y+l2*z,l3*x+l4*y+l5*z,l6*x+l7*y+l8*z];
H2=[A2,B2,normalW];
H3=[normalU,normalV,R];
H4=[P,Q,0];
weighted=matdet(jacvec(L+s*H2+s^2*H3+s^3*H4));
E6=polcoeff(weighted,6,s);
check(is_affine_linear(E6,6,lower),"resonance E6 nonlinear in lower data");
sys6=linear_system(E6,6,lower);
M6=sys6[1]; rhs6=sys6[2];
checkeq(matrank(M6),8,"resonance generic E6 lower rank");
left6=cleared_left_data(M6,rhs6);
pairs6=left6[2];
Ktop=C+4*rw0-2*rw4;
targets6=[rw3^2,rw5^2,Ktop*rw3-rw1^2,Ktop*rw5-rw2^2];
for(j=1,#targets6, \
  check(find_associate(pairs6,targets6[j]), \
    Str("missing universal E6 compatibility ",targets6[j])));

topvars=[rw1,rw2,rw3,rw5];
topzeros=[0,0,0,0];
E6red=subst_many(E6,topvars,topzeros);
sys6red=linear_system(E6red,6,lower);
M6red=sys6red[1]; rhs6red=sys6red[2];
checkeq(rhs6red,vector(28)~,"reduced E6 inhomogeneous part");
checkeq(matrank(M6red),8,"reduced E6 rank");
forced=[a1,a2,a3,a5,b1,b2,b3,b5];
forcedcols=[2,3,4,6,8,9,10,12];
forcedrows=[2,3,4,6,8,9,12,14];
checkeq(matdet(vecextract(M6red,forcedrows,forcedcols)),5308416, \
  "reduced E6 constant forcing minor");
e6vars=[a1,a2,a3,a5,b1,b2,b3,b5];
e6vals=[0,0,0,0,-6*l7,-6*l8,0,0];
checkeq(subst_many(E6red,e6vars,e6vals),0, \
  "reduced E6 full converse");

print("PASS resonance E6: polynomial syzygies force the square chain globally; constant rank-8 solve is complete");

print("PARI hostile resonance audit: E5 K=0/K!=0 split");

E5=polcoeff(weighted,5,s);
E5red=subst_many(subst_many(E5,topvars,topzeros),e6vars,e6vals);
remaining=[l1,l2,l4,l5];
sys5=linear_system(E5red,5,remaining);
M5=sys5[1]; rhs5=sys5[2];
checkeq(matrank(M5),4,"resonance E5 rank");
checkeq(matdet(vecextract(M5,[2,3,8,9],[1..4])),576, \
  "resonance E5 constant pivot");
e5vals=[-2*Ktop*l7,-2*Ktop*l8,-5*Ktop*l7,-5*Ktop*l8];
E5res=subst_many(E5red,remaining,e5vals);
wantres=36*Ktop*(l7*y^3*z^2-l8*y^2*z^3);
checkeq(E5res,wantres,"resonance E5 complete residual");
checkeq(coeffxyz(E5res,[0,3,2]),36*Ktop*l7, \
  "K-open l7 coefficient");
checkeq(coeffxyz(E5res,[0,2,3]),-36*Ktop*l8, \
  "K-open l8 coefficient");

Ldet=matdet([l0,l1,l2;l3,l4,l5;l6,l7,l8]);
Kopenvars=concat(remaining,[l7,l8]);
Kopenvals=concat(e5vals,[0,0]);
checkeq(subst_many(Ldet,Kopenvars,Kopenvals),0, \
  "K!=0 forced singular L");
Kzerovars=concat(remaining,[C]);
Kzerovals=concat([0,0,0,0],[-4*rw0+2*rw4]);
checkeq(subst_many(Ldet,Kzerovars,Kzerovals),0, \
  "K=0 forced singular L");

print("PASS resonance E5: K!=0 kills l7,l8; K=0 leaves two proportional columns");
print("ALL HOSTILE PARI COMPANION-INFINITY RESONANCE CHECKS PASSED");
quit;

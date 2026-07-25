\\ Independent exact PARI/GP reconstruction of the smooth-secant tau family.

die(msg) = { print(Str("FAIL: ",msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };
checkeq(got,want,msg) =
{
  if(got!=want,die(Str(msg,": got ",got,", want ",want)));
};

x='x; y='y; z='z; tt='tt; k='k;
AA='AA; BB='BB; WW='WW;
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
  my(exps=homexps(n));
  vector(#exps,i,x^exps[i][1]*y^exps[i][2]*z^exps[i][3]);
};

coeffxyz(f,e) =
{
  polcoeff(polcoeff(polcoeff(f,e[1],x),e[2],y),e[3],z);
};

hcoeffs(f,n) =
{
  my(exps=homexps(n));
  vector(#exps,i,coeffxyz(f,exps[i]));
};

jacvec(hh) = matrix(3,3,i,j,deriv(hh[i],xyz[j]));
jac3(f,g,h) = matdet(jacvec([f,g,h]));

zero_vars(f,vv) =
{
  my(g=f);
  for(i=1,#vv,g=subst(g,vv[i],0));
  g;
};

linear_system(f,n,vv) =
{
  my(cc=hcoeffs(f,n));
  my(M=matrix(#cc,#vv,i,j,deriv(cc[i],vv[j])));
  my(rhs=vector(#cc,i,-zero_vars(cc[i],vv))~);
  [M,rhs];
};

direction_column(direction) =
{
  concat(concat(hcoeffs(direction[1],3),hcoeffs(direction[2],3)),
         hcoeffs(direction[3],2))~;
};

subst_many(f,vv,ww) =
{
  my(g=f);
  check(#vv==#ww,"subst_many length mismatch");
  for(i=1,#vv,g=subst(g,vv[i],ww[i]));
  g;
};

m2=monoms(2);
m3=monoms(3);

h=x^2+y*z;
s=x^2;
P=h^2;
Q=h*s;
R=x*(h+k*s);
qq=9*k^2+6*k-1;

uu=[u0,u1,u2,u3,u4,u5,u6,u7,u8,u9];
vv=[v0,v1,v2,v3,v4,v5,v6,v7,v8,v9];
ww=[w0,w1,w2,w3,w4,w5];
rawvars=concat(concat(uu,vv),ww);
U0=sum(i=1,10,uu[i]*m3[i]);
V0=sum(i=1,10,vv[i]*m3[i]);
W0=sum(i=1,6,ww[i]*m2[i]);
E7=jac3(P,Q,W0)+jac3(P,V0,R)+jac3(U0,Q,R);
sys7=linear_system(E7,7,rawvars);
M7=sys7[1];
checkeq(matsize(M7),[36,26],"tau raw E7 shape");
checkeq(sys7[2],vector(36)~,"tau raw E7 rhs");
checkeq(matrank(M7),18,"tau raw E7 generic rank");

cols7=[2,3,4,6,7,8,9,10,12,13,14,16,17,18,19,20,24,26];
rows7q=[2,3,4,6,7,8,9,10,12,14,17,18,19,20,24,26,32,33];
rows7l=[2,3,4,6,7,8,9,10,12,14,18,19,24,26,31,32,33,34];
checkeq(matdet(vecextract(M7,rows7q,cols7)), \
  -557256278016*k^8*qq^2,"tau E7 q-pivot");
checkeq(matdet(vecextract(M7,rows7l,cols7)), \
  -557256278016*k^8*(3*k-1)^2,"tau E7 linear-pivot");
checkeq(gcd(qq,3*k-1),1,"tau E7 pivot cover gcd");
checkeq(matrank(subst(M7,k,0)),14,"tau=0 E7 boundary rank");

trans=[[deriv(P,x),deriv(Q,x),deriv(R,x)], \
       [deriv(P,y),deriv(Q,y),deriv(R,y)], \
       [deriv(P,z),deriv(Q,z),deriv(R,z)]];
dirs=[[R,0,0],[0,R,0],trans[1],trans[2],trans[3], \
      [x^3,0,0],[0,x^3,0],[0,0,x^2]];
K=matrix(26,8,i,j,direction_column(dirs[j])[i]);
checkeq(M7*K,matrix(36,8),"tau legal E7 directions");
checkeq(matrank(K),8,"tau legal E7 basis rank");
checkeq(matdet(vecextract(K,[1,2,3,5,11,15,21,25],[1..8])),-4, \
  "tau legal E7 basis minor");

aall=[a0,a1,a2,a3,a4,a5];
ball=[b0,b1,b2,b3,b4,b5];
ell=[l0,l1,l2,l3,l4,l5,l6,l7,l8];
lower=concat(concat(aall,ball),ell);
Lmat=matrix(3,3,i,j,ell[3*(i-1)+j]);
H2=[sum(i=1,6,aall[i]*m2[i]),sum(i=1,6,ball[i]*m2[i]),WW*x^2];
weighted=matdet(Lmat+tt*jacvec(H2) \
  +tt^2*jacvec([AA*x^3,BB*x^3,R])+tt^3*jacvec([P,Q,0]));
for(j=7,9,checkeq(polcoeff(weighted,j,tt),0,Str("tau top E",j)));
E6=polcoeff(weighted,6,tt);
sys6=linear_system(E6,6,lower);
M6=sys6[1];
checkeq(matsize(M6),[28,21],"tau E6 shape");
checkeq(sys6[2],vector(28)~,"tau E6 has a compatibility residual");
checkeq(matrank(M6),10,"tau E6 generic rank");

cols6=[2,3,4,6,8,9,10,12,20,21];
rows6q=[2,3,4,6,8,9,12,14,18,19];
rows6l=[2,3,4,6,8,9,18,19,24,26];
checkeq(matdet(vecextract(M6,rows6q,cols6)), \
  -331776*k^4*qq^2,"tau E6 q-pivot");
checkeq(matdet(vecextract(M6,rows6l,cols6)), \
  -331776*k^4*(3*k-1)^2,"tau E6 linear-pivot");
checkeq(matrank(subst(M6,k,0)),8,"tau=0 E6 boundary rank");

loww=vector(21);
loww[14]=1; loww[18]=1; loww[19]=1;
witness=subst_many(subst_many(weighted,[AA,BB,WW],[0,0,0]),lower,loww);
checkeq(polcoeff(witness,0,tt),1,"tau witness det L");
for(j=6,9,checkeq(polcoeff(witness,j,tt),0,Str("tau witness E",j)));
E5w=polcoeff(witness,5,tt);
checkeq(coeffxyz(E5w,[4,1,0]),3*k-1,"tau witness x4y");
checkeq(coeffxyz(E5w,[4,0,1]),6*k+2,"tau witness x4z");
checkeq(gcd(3*k-1,6*k+2),1,"tau witness sharpness");

print("PASS PARI tau family: k survives E7/E6 with no compatibility");
quit;

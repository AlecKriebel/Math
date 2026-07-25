\\ Independent exact PARI/GP certificate for the unmarked c=3 resonance.

x='x; y='y; z='z; ss='ss;
p=x^2; q=y^2+x*z;
P=(p-q)^2; Q=(p+q)^2; R=x*(p-3*q);

fail(message) = { print(Str("FAIL: ",message)); quit(1); };
check(condition,message) = if(!condition,fail(message));
checkzero(value,message) = check(value == 0,message);
checkequal(value,expected,message) = checkzero(value-expected,message);

gradmap(V) = matrix(3,3,i,j,deriv(V[i],[x,y,z][j]));
jac3(f,g,h) = matdet(gradmap([f,g,h]));
wcoef(L,H2,H3,H4,k) = polcoef( \
  matdet(gradmap(L+ss*H2+ss^2*H3+ss^3*H4)),k,ss);
cf(f,i,j,k) = polcoef(polcoef(polcoef(f,i,x),j,y),k,z);
monomial(ex) = x^ex[1]*y^ex[2]*z^ex[3];
cfexp(f,ex) = cf(f,ex[1],ex[2],ex[3]);
exponents(d) = {
  my(out=List());
  forstep(i=d,0,-1,
    forstep(j=d-i,0,-1,
      listput(out,[i,j,d-i-j])
    )
  );
  Vec(out)
};
form(coefficients,exps) =
  sum(i=1,#coefficients,coefficients[i]*monomial(exps[i]));
suball(pol,vars,vals) = {
  my(out=pol);
  for(i=1,#vars,out=subst(out,vars[i],vals[i]));
  out
};
coeffcolumn(direction,e3,e2) = {
  concat(
    concat(
      vector(#e3,i,cfexp(direction[1],e3[i])),
      vector(#e3,i,cfexp(direction[2],e3[i]))
    ),
    vector(#e2,i,cfexp(direction[3],e2[i]))
  )~
};

e2=exponents(2); e3=exponents(3); e6=exponents(6); e7=exponents(7);
uc=[u30,u31,u32,u33,u34,u35,u36,u37,u38,u39];
vc=[v30,v31,v32,v33,v34,v35,v36,v37,v38,v39];
wc=[w20,w21,w22,w23,w24,w25];
unknowns=concat(concat(uc,vc),wc);
Uraw=form(uc,e3); Vraw=form(vc,e3); Wraw=form(wc,e2);
E7=jac3(P,Q,Wraw)+jac3(P,Vraw,R)+jac3(Uraw,Q,R);
M7=matrix(#e7,#unknowns,i,j,deriv(cfexp(E7,e7[i]),unknowns[j]));

checkzero(jac3(P,Q,R),"top E8 identity");
delta(h)=2*y*deriv(h,z)-x*deriv(h,y);
compact=2*( \
  8*x*(p-q)*(p+q)*delta(Wraw) \
  +3*(p+q)*(q-3*p)*delta(Uraw) \
  +3*(p-q)*(p+q)*delta(Vraw));
checkzero(E7-compact,"compact E7 identity");
checkequal(matrank(M7),14,"raw E7 rank");
rows7=[1,2,3,4,5,6,7,8,9,10,11,12,14,16];
cols7=[2,3,5,6,7,8,9,10,12,13,15,16,19,20];
checkequal(matdet(vecextract(M7,rows7,cols7)),-1039973956284579840, \
  "raw E7 constant maximal minor");

tx=[deriv(P,x),deriv(Q,x),deriv(R,x)];
ty=[deriv(P,y),deriv(Q,y),deriv(R,y)];
dirs=[ \
  [R,0,0],[0,R,0],tx,ty, \
  [x*q,0,0],[0,x*q,0], \
  [y*(p-q),y*(3*p-q),0], \
  [z*(p-q),z*(3*p-q),0], \
  [0,0,p], \
  [0,8*x^2*z,3*y^2], \
  [0,-8*x*y*z,3*y*z], \
  [0,-8*x*z^2,3*z^2]];
K=matrix(26,12,i,j,coeffcolumn(dirs[j],e3,e2)[i]);
checkzero(M7*K,"twelve raw E7 kernel directions");
checkequal(matrank(K),12,"raw kernel independence");
krows=[1,2,3,4,11,12,13,14,15,16,21,23];
checkequal(matdet(vecextract(K,krows,[1..12])),49152, \
  "raw kernel independence minor");
G=matrix(4,4,i,j, \
  if(i==1,cfexp(dirs[j][1],[3,0,0]), \
    if(i==2,cfexp(dirs[j][2],[3,0,0]), \
      if(i==3,cfexp(dirs[j][3],[1,1,0]), \
        cfexp(dirs[j][3],[1,0,1])))));
checkequal(matdet(G),-36,"four-coordinate gauge determinant");

AA='AA; BB='BB; CC='CC; DD='DD;
ee='ee; ff='ff; gg='gg; ww='ww;
u0='u0; uq='uq; du1='du1; du2='du2; du3='du3; du4='du4;
v0='v0; vq='vq; dv1='dv1; dv2='dv2; dv3='dv3; dv4='dv4;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4; l5='l5;
l6='l6; l7='l7; l8='l8;

U3=AA*x*q+CC*y*(p-q)+DD*z*(p-q);
V3=BB*x*q+CC*y*(3*p-q)+DD*z*(3*p-q) \
  +8*ee*x^2*z-8*ff*x*y*z-8*gg*x*z^2;
W2=ww*p+3*ee*y^2+3*ff*y*z+3*gg*z^2;
U2=u0*p+uq*q+du1*x*y+du2*x*z+du3*y*z+du4*z^2;
V2=v0*p+vq*q+dv1*x*y+dv2*x*z+dv3*y*z+dv4*z^2;
H4=[P,Q,0]; H3=[U3,V3,R]; H2=[U2,V2,W2];
L=[l0*x+l1*y+l2*z,l3*x+l4*y+l5*z,l6*x+l7*y+l8*z];
lower=[u0,uq,du1,du2,du3,du4,v0,vq,dv1,dv2,dv3,dv4,l7,l8];
E6=wcoef(L,H2,H3,H4,6);

clearvec(M,N,j) = {
  my(den=1,v);
  for(i=1,matsize(N)[1],den*=denominator(N[i,j]));
  v=den*N[,j];
  for(i=1,#v,checkequal(denominator(v[i]),1, \
    Str("polynomial left vector denominator, column ",j)));
  checkzero(M~*v,Str("cleared left-kernel identity, column ",j));
  v
};
clearpair(M,c,N,j) = clearvec(M,N,j)~*c;

compatpairs(substitutions,values) = {
  my(E=suball(E6,substitutions,values));
  my(M=matrix(#e6,#lower,i,j,deriv(cfexp(E,e6[i]),lower[j])));
  my(c=vector(#e6,i, \
    suball(cfexp(E,e6[i]),lower,vector(#lower)))~);
  my(N=matker(M~));
  my(out=vector(#N,j,clearpair(M,c,N,j)));
  [M,c,out,N]
};

C0=compatpairs([],[]);
checkequal(matrank(C0[1]),8,"generic E6 lower rank");
check(matrank(concat(C0[1],C0[2]))>8,"generic E6 augmented incompatibility");
checkzero(C0[3][12]-192*gg^2,"division-free E6 certificate forcing g=0");
checkequal(cf(E6,1,1,4),192*gg^2,"literal E6 coefficient forcing g=0");
C1=compatpairs([gg],[0]);
checkzero(C1[3][15]-C1[3][6]-144*ff^2, \
  "division-free E6 certificate forcing f=0");
E6g=subst(E6,gg,0);
checkequal(-cf(E6g,2,1,3)+cf(E6g,0,5,1),144*ff^2, \
  "literal E6 combination forcing f=0");
C2=compatpairs([gg,ff],[0,0]);
checkzero(C2[3][4]+C2[3][6]+48*(DD+2*ee)^2, \
  "division-free E6 certificate forcing D=-2e");
E6gf=suball(E6,[gg,ff],[0,0]);
checkequal( \
  cf(E6gf,4,1,1)-cf(E6gf,3,3,0)-2*cf(E6gf,3,1,2) \
  +cf(E6gf,2,3,1)+cf(E6gf,2,1,3), \
  -48*(DD+2*ee)^2,"literal E6 combination forcing D=-2e");
C3=compatpairs([gg,ff,DD],[0,0,-2*ee]);
checkzero(C3[3][4]-24*CC^2, \
  "division-free E6 certificate forcing C=0");
E6gfd=suball(E6,[gg,ff,DD],[0,0,-2*ee]);
checkequal( \
  cf(E6gfd,5,1,0)-cf(E6gfd,3,3,0)-cf(E6gfd,3,1,2) \
  +cf(E6gfd,2,3,1),24*CC^2, \
  "literal E6 combination forcing C=0");

U3s=AA*x*q-2*ee*z*(p-q);
V3s=BB*x*q+2*ee*z*(p+q);
W2s=ww*p+3*ee*y^2;
U2s=u0*p+uq*q+AA*ee*x*z+ee^2*z^2;
V2s=v0*p+vq*q-8/3*l7*x*y \
  +(BB*ee+8*ee^2-8/3*l8)*x*z+ee^2*z^2;
H3s=[U3s,V3s,R]; H2s=[U2s,V2s,W2s];
E6surv=suball(E6,[gg,ff,DD,CC],[0,0,-2*ee,0]);
M6s=matrix(#e6,#lower,i,j,deriv(cfexp(E6surv,e6[i]),lower[j]));
checkequal(matrank(M6s),8,"surviving E6 rank");
rows6=[1,2,3,4,5,6,7,9]; cols6=[3,4,5,6,9,10,11,12];
checkequal(matdet(vecextract(M6s,rows6,cols6)),5159780352, \
  "surviving E6 constant maximal minor");
checkzero(wcoef(L,H2s,H3s,H4,6),"surviving E6 direct complete solution");

E5=wcoef(L,H2s,H3s,H4,5);
cx5=cf(E5,5,0,0);
cx4z=cf(E5,4,0,1);
cx3z2=cf(E5,3,0,2);
checkequal(cx5, \
  (12*AA-4*BB-32*ee-32/3*ww)*l7+18*l1-6*l4, \
  "E5 x5 coefficient");
checkequal(cx4z, \
  (2*AA+2*BB+32*ee+32/3*ww)*l7+12*l1, \
  "E5 x4z coefficient");
checkequal(cx3z2,-2*(AA-BB)*l7-6*l1+6*l4, \
  "E5 x3z2 coefficient");
colvars=[l1,l4,l7]; colcoeffs=[cx5,cx4z,cx3z2];
Mcol=matrix(3,3,i,j,deriv(colcoeffs[i],colvars[j]));
resonance=-6*AA+3*BB+48*ee+16*ww;
checkequal(matdet(Mcol),-96*resonance,"E5 column-two determinant");
checkequal(subst(cx4z,l7,0),12*l1,"E5 l7=0 first pivot");
checkequal(suball(cx3z2,[l7,l1],[0,0]),6*l4, \
  "E5 l7=l1=0 second pivot");

BBbranch=2*AA-16*ee-16/3*ww;
E5b=subst(E5,BB,BBbranch);
e5vars=[l1,l2,l4,l5];
M5=matrix(#exponents(5),4,i,j, \
  deriv(cfexp(E5b,exponents(5)[i]),e5vars[j]));
checkequal(matrank(M5),4,"resonant E5 rank");
checkequal(matdet(vecextract(M5,[1,2,3,5],[1..4])),20736, \
  "resonant E5 constant maximal minor");
l1s=-AA*l7/2;
l4s=(-15*AA+96*ee+32*ww)*l7/18;
l2s=AA*(3*ee^2-l8)/2+ee*uq;
l5s=(15*AA-96*ee-32*ww)*(3*ee^2-l8)/18+ee*vq;
E5sol=suball(E5b,e5vars,[l1s,l2s,l4s,l5s]);
checkzero(E5sol,"resonant E5 direct complete solution");

E4=wcoef(L,H2s,H3s,H4,4);
E4b=suball(E4,[BB,l1,l2,l4,l5], \
  [BBbranch,l1s,l2s,l4s,l5s]);
checkequal(cf(E4b,2,0,2),16/3*l7*(3*ee^2-l8), \
  "E4 x2z2 first pivot");
E4c=subst(E4b,l8,3*ee^2);
checkequal(cf(E4c,3,1,0),16/3*l7^2,"E4 x3y second pivot");

print("ALL UNMARKED c=3 RESONANCE PARI CERTIFICATES PASSED");
quit;

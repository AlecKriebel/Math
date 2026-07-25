\\ Independent exact PARI/GP certificate for the companion-at-infinity chart.

x='x; y='y; z='z; s='s; t='t; a='a;
p=x^2; q=y*z; R=x*q;

fail(label,value) = { print(Str("FAIL ",label,": ",value)); quit(1); };
checkzero(value,label) = if(value != 0,fail(label,value));
checkequal(value,expected,label) = checkzero(value-expected,label);
gradmat(F) = matrix(3,3,i,j,deriv(F[i],[x,y,z][j]));
jac3(f,g,h) = matdet(gradmat([f,g,h]));
wcoef(L,H2,H3,H4,k) = polcoeff(matdet(gradmat(L+s*H2+s^2*H3+s^3*H4)),k,s);
cf(P,i,j,k) = polcoeff(polcoeff(polcoeff(P,i,x),j,y),k,z);
monomial(e) = x^e[1]*y^e[2]*z^e[3];
cfexp(P,e) = cf(P,e[1],e[2],e[3]);
exponents(d) = {
  my(L=List());
  forstep(i=d,0,-1,forstep(j=d-i,0,-1,listput(L,[i,j,d-i-j])));
  Vec(L)
};
form(coefficients,exps) = sum(i=1,#coefficients,coefficients[i]*monomial(exps[i]));
substmany(P,V,W) = {
  my(Q=P);
  for(i=1,#V,Q=subst(Q,V[i],W[i]));
  Q
};

e2=exponents(2); e3=exponents(3); e5=exponents(5); e6=exponents(6); e7=exponents(7);
uc=[u30,u31,u32,u33,u34,u35,u36,u37,u38,u39];
vc=[v30,v31,v32,v33,v34,v35,v36,v37,v38,v39];
wc=[w20,w21,w22,w23,w24,w25];
unknowns=concat(concat(uc,vc),wc);
U3=form(uc,e3); V3=form(vc,e3); W2=form(wc,e2);
e7matrix(A,B) = {
  my(E=jac3(A,B,W2)+jac3(A,V3,R)+jac3(U3,B,R));
  matrix(#e7,#unknowns,i,j,deriv(cfexp(E,e7[i]),unknowns[j]))
};
tripletcoeff(D,i) = {
  if(i<=10,cfexp(D[1],e3[i]),
    if(i<=20,cfexp(D[2],e3[i-10]),cfexp(D[3],e2[i-20])))
};
kernelmatrix(D) = matrix(26,#D,i,j,tripletcoeff(D[j],i));

\\ -------------------------------------------------------------------------
\\ 1. Both outer critical points finite: unordered pair {t,1}.

F1=(p-t*q)^2; F2=(p-q)^2;
M=e7matrix(F1,F2);
rows=[2,3,4,6,7,8,9,10,12,14,17,18,19,20,24,26,32,33];
cols=[2,3,4,6,7,8,9,10,12,13,14,16,17,18,19,20,24,26];
minor=matdet(vecextract(M,rows,cols));
expected=-347892350976*(t-1)^10*(t+2)^4*(2*t+1)^4;
checkequal(minor,expected,"finite raw E7 minor");

base=[[x^3,0,0],[x*q,0,0],[0,x^3,0],[0,x*q,0],[0,0,p],[0,0,q]];
finite_dirs=concat(base,[[-2*t*y*(p-t*q),-2*y*(p-q),x*y],[-2*t*z*(p-t*q),-2*z*(p-q),x*z]]);
K=kernelmatrix(finite_dirs);
checkzero(M*K,"finite raw E7 kernel");
checkequal(matdet(vecextract(K,[1,5,11,15,18,19,21,25],[1..8])),4,"finite kernel independence");
checkequal(matrank(subst(M,t,0)),18,"finite t=0 rank");
checkequal(matrank(subst(M,t,-2)),14,"finite t=-2 rank");
checkequal(matrank(subst(M,t,-1/2)),14,"finite t=-1/2 rank");
checkequal(matrank(subst(M,t,1)),8,"finite t=1 degenerate rank");

\\ The omitted x-translation is a base-kernel combination, and supplies
\\ the affine gauge that kills the first x^3 coefficient.
taux=[deriv(F1,x),deriv(F2,x),deriv(R,x)];
taux_expected=[4*x^3-4*t*x*q,4*x^3-4*x*q,q];
checkzero(taux-taux_expected,"finite x-translation ledger");

\\ Reciprocal normalization is exactly the unordered swap for t != 0.
rawfactor=(t-1)^10*(t+2)^4*(2*t+1)^4;
checkzero(t^18*subst(rawfactor,t,1/t)-rawfactor,"finite unordered raw factor");

\\ -------------------------------------------------------------------------
\\ 2. One outer critical point at infinity: pair {a,infinity}.

O1=(p-a*q)^2; O2=q^2;
MO=e7matrix(O1,O2);
orows=[2,3,4,6,7,8,9,10,12,14,18,19,24,26,31,32,33,34];
ominor=matdet(vecextract(MO,orows,cols));
checkequal(ominor,-5566277615616,"outer raw E7 constant minor");
outer_dirs=concat(base,[[-2*a*y*(p-a*q),2*y*q,x*y],[-2*a*z*(p-a*q),2*z*q,x*z]]);
KO=kernelmatrix(outer_dirs);
checkzero(MO*KO,"outer raw E7 kernel");
checkequal(matdet(vecextract(KO,[1,5,11,15,18,19,21,25],[1..8])),4,"outer kernel independence");
checkequal(matrank(subst(MO,a,0)),18,"outer a=0 rank");
checkequal(matrank(subst(MO,a,1)),18,"outer a!=0 representative rank");
tauxo=[deriv(O1,x),deriv(O2,x),deriv(R,x)];
checkzero(tauxo-[4*x^3-4*a*x*q,0,q],"outer x-translation ledger");

\\ -------------------------------------------------------------------------
\\ 3. Gauge-fixed E6 and E5.

C='C; w0='w0; w1='w1;
H3=[0,C*x^3,R];
H2third=w0*p+w1*q;
checkzero(wcoef([0,0,0],[0,0,H2third],H3,[F1,F2,0],7),"finite normal E7");
checkzero(wcoef([0,0,0],[0,0,H2third],H3,[O1,O2,0],7),"outer normal E7");

ac=[aa0,aa1,aa2,aa3,aa4,aa5];
bc=[bb0,bb1,bb2,bb3,bb4,bb5];
lc=[l0,l1,l2,l3,l4,l5,l6,l7,l8];
A2=form(ac,e2); B2=form(bc,e2);
L=[l0*x+l1*y+l2*z,l3*x+l4*y+l5*z,l6*x+l7*y+l8*z];
H2=[A2,B2,H2third];
lower=concat(concat(ac,bc),lc);
forced=[aa1,aa2,aa3,aa5,bb1,bb2,bb3,bb5,l7,l8];
forcedcols=[2,3,4,6,8,9,10,12,20,21];
zeros=vector(#forced,i,0);
e6matrix(E) = matrix(#e6,#lower,i,j,deriv(cfexp(E,e6[i]),lower[j]));

E6=wcoef(L,H2,H3,[F1,F2,0],6);
M6=e6matrix(E6);
frows6=[2,3,4,6,8,9,12,14,18,19];
minor6=matdet(vecextract(M6,frows6,forcedcols));
expected6=-1048576*(t-1)^6*(t+2)^2*(2*t+1)^2;
checkequal(minor6,expected6,"finite E6 minor");
checkzero(substmany(E6,forced,zeros),"finite E6 converse");
checkequal(matrank(subst(vecextract(M6,[1..#e6],forcedcols),t,0)),10,"finite t=0 E6 rank");
checkequal(matrank(subst(vecextract(M6,[1..#e6],forcedcols),t,-2)),8,"finite t=-2 E6 rank");
checkequal(matrank(subst(vecextract(M6,[1..#e6],forcedcols),t,-1/2)),8,"finite t=-1/2 E6 rank");
checkequal(matrank(subst(vecextract(M6,[1..#e6],forcedcols),t,1)),4,"finite t=1 E6 rank");
e6factor=(t-1)^6*(t+2)^2*(2*t+1)^2;
checkzero(t^10*subst(e6factor,t,1/t)-e6factor,"finite unordered E6 factor");

E6O=wcoef(L,H2,H3,[O1,O2,0],6);
M6O=e6matrix(E6O);
orows6=[2,3,4,6,8,9,18,19,24,26];
checkequal(matdet(vecextract(M6O,orows6,forcedcols)),-4194304,"outer E6 constant minor");
checkzero(substmany(E6O,forced,zeros),"outer E6 converse");
checkequal(matrank(subst(vecextract(M6O,[1..#e6],forcedcols),a,0)),10,"outer a=0 E6 rank");
checkequal(matrank(subst(vecextract(M6O,[1..#e6],forcedcols),a,1)),10,"outer a!=0 E6 rank");

E5=substmany(wcoef(L,H2,H3,[F1,F2,0],5),forced,zeros);
remaining=[l1,l2,l4,l5];
M5=matrix(#e5,#remaining,i,j,deriv(cfexp(E5,e5[i]),remaining[j]));
checkzero(substmany(E5,remaining,vector(#remaining,i,0)),"finite E5 homogeneous converse");
checkequal(matdet(vecextract(M5,[2,3,8,9],[1..4])),64*(t-1)^2,"finite E5 minor");
checkequal(matrank(subst(M5,t,0)),4,"finite t=0 E5 rank");
checkequal(matrank(subst(M5,t,-2)),4,"finite t=-2 E5 rank");
checkequal(matrank(subst(M5,t,-1/2)),4,"finite t=-1/2 E5 rank");
checkequal(matrank(subst(M5,t,1)),2,"finite t=1 E5 rank");
checkzero(t^2*subst((t-1)^2,t,1/t)-(t-1)^2,"finite unordered E5 factor");

E5O=substmany(wcoef(L,H2,H3,[O1,O2,0],5),forced,zeros);
M5O=matrix(#e5,#remaining,i,j,deriv(cfexp(E5O,e5[i]),remaining[j]));
checkzero(substmany(E5O,remaining,vector(#remaining,i,0)),"outer E5 homogeneous converse");
checkequal(matdet(vecextract(M5O,[2,3,18,19],[1..4])),64,"outer E5 constant minor");
checkequal(matrank(subst(M5O,a,0)),4,"outer a=0 E5 rank");
checkequal(matrank(subst(M5O,a,1)),4,"outer a!=0 E5 rank");

allzero=concat(forced,remaining);
checkzero(substmany(matdet([l0,l1,l2;l3,l4,l5;l6,l7,l8]),allzero,vector(#allzero,i,0)),"forced singular L");

print("PASS: independent PARI line-(2,2) companion-at-infinity certificate");
quit;

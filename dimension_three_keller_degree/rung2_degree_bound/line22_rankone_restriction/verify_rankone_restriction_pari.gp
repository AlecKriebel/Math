\\ Independent PARI/GP certificate for the rank-one-restriction line-(2,2) row.
\\ It reconstructs the polynomial coefficient matrices directly in PARI.

x='x; y='y; z='z; s='s; c='c;
p=x^2; q=y^2+x*z;

checkzero(value,label) = {
  if (value != 0,
    print(Str("FAIL ",label,": ",value));
    quit(1)
  );
  print(Str("  PASS ",label));
};
checkequal(value,expected,label) = checkzero(value-expected,label);
gradmat(F) = matrix(3,3,i,j,deriv(F[i],[x,y,z][j]));
jac3(f,g,h) = matdet(gradmat([f,g,h]));
wcoef(L,H2,H3,H4,k) = polcoeff( \
  matdet(gradmat(L+s*H2+s^2*H3+s^3*H4)),k,s);
cf(P,i,j,k) = polcoeff(polcoeff(polcoeff(P,i,x),j,y),k,z);
monomial(e) = x^e[1]*y^e[2]*z^e[3];
cfexp(P,e) = cf(P,e[1],e[2],e[3]);
exponents(d) = {
  my(L=List());
  forstep(i=d,0,-1,
    forstep(j=d-i,0,-1,
      listput(L,[i,j,d-i-j])
    )
  );
  Vec(L)
};
form(coefficients,exps) = sum(i=1,#coefficients,coefficients[i]*monomial(exps[i]));

e2=exponents(2); e3=exponents(3); e6=exponents(6); e7=exponents(7);
uc=[u30,u31,u32,u33,u34,u35,u36,u37,u38,u39];
vc=[v30,v31,v32,v33,v34,v35,v36,v37,v38,v39];
wc=[w20,w21,w22,w23,w24,w25];
unknowns=concat(concat(uc,vc),wc);
U3=form(uc,e3); V3=form(vc,e3); W2=form(wc,e2);

e7matrix(A,B,R) = {
  my(E=jac3(A,B,W2)+jac3(A,V3,R)+jac3(U3,B,R));
  matrix(#e7,#unknowns,i,j,deriv(cfexp(E,e7[i]),unknowns[j]))
};

\\ -------------------------------------------------------------------------
\\ 1. Full stabilizer: a,b are nonzero in the geometric statement.

a='a; b='b; g='g; d='d;
tx=a*x;
ty=g*x+b*y;
tz=d*x-2*b*g*y/a+b^2*z/a;
checkzero(tx^2-a^2*p,"stabilizer p transform");
checkzero(ty^2+tx*tz-b^2*q-(g^2+a*d)*p,"stabilizer q transform");
T=[a,0,0;g,b,0;d,-2*b*g/a,b^2/a];
checkequal(matdet(T),b^3,"stabilizer determinant");

\\ -------------------------------------------------------------------------
\\ 2. Raw E7 on the unmarked finite-companion family.

H41=(p-q)^2; H42=(p+q)^2; R=x*(p-c*q);
M=e7matrix(H41,H42,R);
rows=concat([1..16],[18,20]);
cols=[2,3,5,6,7,8,9,10,12,13,15,16,17,18,19,20,25,26];
openminor=matdet(vecextract(M,rows,cols));
openexpected=-769482217582755840*c^6*(c-3)^4*(c+3)^4;
checkequal(openminor,openexpected,"open raw-E7 maximal minor");

dirs=[[x^3,0,0],[x*q,0,0],[0,x^3,0],[0,x*q,0],[0,0,p],[0,0,q],[deriv(H41,x),deriv(H42,x),deriv(R,x)],[deriv(H41,y),deriv(H42,y),deriv(R,y)]];
dircoeff(i,j) = {
  if (i<=10,
    cfexp(dirs[j][1],e3[i]),
    if (i<=20,
      cfexp(dirs[j][2],e3[i-10]),
      cfexp(dirs[j][3],e2[i-20])
    )
  )
};
K=matrix(26,8,i,j,dircoeff(i,j));
checkzero(M*K,"open raw-E7 eight kernel directions");
krows=[1,2,3,4,11,13,21,23];
checkequal(matdet(vecextract(K,krows,[1..8])),-8,"kernel independence minor");

\\ Exact raw ranks on all joint-moduli strata.
checkequal(matrank(subst(M,c,0)),16,"unmarked triple raw-E7 rank");
checkequal(matrank(subst(M,c,3)),14,"unmarked plus resonance raw-E7 rank");
checkequal(matrank(subst(M,c,-3)),14,"unmarked minus resonance raw-E7 rank");
checkequal(matrank(e7matrix(H41,H42,x*q)),18,"unmarked infinity raw-E7 rank");
checkequal(matrank(e7matrix(p^2,q^2,x^3)),8,"marked triple raw-E7 rank");
checkequal(matrank(e7matrix(p^2,q^2,x*q)),18,"marked coincident mixed raw-E7 rank");
checkequal(matrank(e7matrix(p^2,q^2,x*(p-q))),18,"marked distinct mixed raw-E7 rank");

\\ -------------------------------------------------------------------------
\\ 3. Normalized E6 and decisive E5 coefficients on c*(c^2-9) != 0.

AA='AA; BB='BB; w0='w0; w1='w1;
u0='u0; uq='uq; du1='du1; du2='du2; du3='du3; du4='du4;
v0='v0; vq='vq; dv1='dv1; dv2='dv2; dv3='dv3; dv4='dv4;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4; l5='l5;
l6='l6; l7='l7; l8='l8;
U2d=u0*p+uq*q+du1*x*y+du2*x*z+du3*y*z+du4*z^2;
V2d=v0*p+vq*q+dv1*x*y+dv2*x*z+dv3*y*z+dv4*z^2;
H4=[H41,H42,0];
H3=[AA*x*q,BB*x*q,R];
H2=[U2d,V2d,w0*p+w1*q];
L=[l0*x+l1*y+l2*z,l3*x+l4*y+l5*z,l6*x+l7*y+l8*z];
E6=wcoef(L,H2,H3,H4,6);
constrained=[l7,l8,du1,du2,du3,du4,dv1,dv2,dv3,dv4];
M6=matrix(#e6,#constrained,i,j,deriv(cfexp(E6,e6[i]),constrained[j]));
rows6=[1,3,5,7,9,11,17,23,2,4];
minor6=matdet(vecextract(M6,rows6,[1..10]));
expected6=-10871635968*c^2*(c-3)^2*(c+3)^2;
checkequal(minor6,expected6,"normalized E6 forcing minor");

H2n=[u0*p+uq*q,v0*p+vq*q,w0*p+w1*q];
Ln=[l0*x+l1*y+l2*z,l3*x+l4*y+l5*z,l6*x];
checkzero(wcoef(Ln,H2n,H3,H4,6),"normalized E6 converse");
E5=wcoef(Ln,H2n,H3,H4,5);
checkequal(cf(E5,3,0,2),-2*c*(l1-l4),"E5 x3z2 difference");
checkequal(cf(E5,0,5,0),4*c*(l2-l5),"E5 y5 difference");
checkequal(cf(E5,5,0,0),2*((2*c+3)*l1+(3-2*c)*l4),"E5 x5 sum");
checkequal(cf(E5,4,1,0),-4*((2*c+3)*l2+(3-2*c)*l5),"E5 x4y sum");
checkzero(matdet([l0,0,0;l3,0,0;l6,0,0]),"forced singular linear part");

print("PASS: independent PARI rank-one-restriction line-(2,2) certificate");
quit;

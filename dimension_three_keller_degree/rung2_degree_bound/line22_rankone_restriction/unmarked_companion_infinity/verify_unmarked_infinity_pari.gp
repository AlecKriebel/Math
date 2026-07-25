\\ Independent PARI/GP certificate for the unmarked companion-at-infinity orbit.

x='x; y='y; z='z; ss='ss;
p=x^2; q=y^2+x*z;
P=(p-q)^2; Q=(p+q)^2; R=x*q;

fail(message) = { print(Str("FAIL: ",message)); quit(1); };
check(condition,message) = if(!condition,fail(message));
checkzero(value,message) = check(value == 0,message);
checkequal(value,expected,message) = checkzero(value-expected,message);

gradmap(V) = matrix(3,3,i,j,deriv(V[i],[x,y,z][j]));
jac3(f,g,h) = matdet(gradmap([f,g,h]));
wcoef(L,H2,H3,H4,k) = polcoef( \
  matdet(gradmap(L+ss*H2+ss^2*H3+ss^3*H4)),k,ss);
cf(f,i,j,k) = polcoef(polcoef(polcoef(f,i,x),j,y),k,z);
monomial(e) = x^e[1]*y^e[2]*z^e[3];
cfexp(f,e) = cf(f,e[1],e[2],e[3]);
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

e2=exponents(2); e3=exponents(3); e6=exponents(6); e7=exponents(7);
uc=[u30,u31,u32,u33,u34,u35,u36,u37,u38,u39];
vc=[v30,v31,v32,v33,v34,v35,v36,v37,v38,v39];
wc=[w20,w21,w22,w23,w24,w25];
unknowns=concat(concat(uc,vc),wc);
U3=form(uc,e3); V3=form(vc,e3); W2=form(wc,e2);
E7=jac3(P,Q,W2)+jac3(P,V3,R)+jac3(U3,Q,R);
M7=matrix(#e7,#unknowns,i,j,deriv(cfexp(E7,e7[i]),unknowns[j]));

checkzero(jac3(P,Q,R),"top E8 identity");
delta(f)=2*y*deriv(f,z)-x*deriv(f,y);
compact=2*(8*x*(p-q)*(p+q)*delta(W2)+(p+q)*(2*p-q)*delta(U3)-(p-q)*(2*p+q)*delta(V3));
checkzero(E7-compact,"compact E7 identity");
checkequal(matrank(M7),18,"raw E7 rank");
rows7=concat([1..14],[16,17,18,23]);
cols7=[2,3,5,6,7,8,9,10,12,13,15,16,17,18,19,20,25,26];
checkequal(matdet(vecextract(M7,rows7,cols7)),1709960483517235200,"raw E7 maximal minor");

tx=[deriv(P,x),deriv(Q,x),deriv(R,x)];
ty=[deriv(P,y),deriv(Q,y),deriv(R,y)];
tz=[deriv(P,z),deriv(Q,z),deriv(R,z)];
dirs=[[x^3,0,0],[x*q,0,0],[0,x^3,0],[0,x*q,0],[0,0,p],[0,0,q],tx,ty];
dircoeff(i,j) = {
  if(i<=10,
    cfexp(dirs[j][1],e3[i]),
    if(i<=20,
      cfexp(dirs[j][2],e3[i-10]),
      cfexp(dirs[j][3],e2[i-20])
    )
  )
};
K=matrix(26,8,i,j,dircoeff(i,j));
checkzero(M7*K,"eight raw E7 kernel directions");
checkequal(matrank(K),8,"kernel rank");
krows=[1,2,3,4,11,13,21,23];
checkequal(matdet(vecextract(K,krows,[1..8])),-8,"kernel independence minor");
for(i=1,3,checkzero(tz[i]+2*dirs[1][i]-2*dirs[2][i]-2*dirs[3][i]-2*dirs[4][i]-dirs[5][i],Str("third translation relation component ",i)));

AA='AA; BB='BB; w0='w0; w1='w1;
u0='u0; uq='uq; du1='du1; du2='du2; du3='du3; du4='du4;
v0='v0; vq='vq; dv1='dv1; dv2='dv2; dv3='dv3; dv4='dv4;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4; l5='l5;
l6='l6; l7='l7; l8='l8;
U2=u0*p+uq*q+du1*x*y+du2*x*z+du3*y*z+du4*z^2;
V2=v0*p+vq*q+dv1*x*y+dv2*x*z+dv3*y*z+dv4*z^2;
H4=[P,Q,0];
H3=[AA*x^3,BB*x^3,R];
H2=[U2,V2,w0*p+w1*q];
L=[l0*x+l1*y+l2*z,l3*x+l4*y+l5*z,l6*x+l7*y+l8*z];
E6=wcoef(L,H2,H3,H4,6);
constrained=[l7,l8,du1,du2,du3,du4,dv1,dv2,dv3,dv4];
M6=matrix(#e6,#constrained,i,j,deriv(cfexp(E6,e6[i]),constrained[j]));
checkequal(matrank(M6),10,"E6 constrained rank");
rows6=concat([1..9],[12]);
checkequal(matdet(vecextract(M6,rows6,[1..10])),4831838208,"E6 constant forcing minor");
zero10=vector(10);
E6zero=E6;
for(i=1,10,E6zero=subst(E6zero,constrained[i],0));
checkzero(E6zero,"E6 converse after ten forced zeros");

H2n=[u0*p+uq*q,v0*p+vq*q,w0*p+w1*q];
Ln=[l0*x+l1*y+l2*z,l3*x+l4*y+l5*z,l6*x];
checkzero(wcoef(Ln,H2n,H3,H4,6),"normalized E6 direct converse");
E5=wcoef(Ln,H2n,H3,H4,5);
checkequal(cf(E5,5,0,0),-4*(l1-l4),"E5 x5 difference");
checkequal(cf(E5,4,0,1),-2*(l1+l4),"E5 x4z sum");
checkequal(cf(E5,4,1,0),8*(l2-l5),"E5 x4y difference");
checkequal(cf(E5,3,1,1),4*(l2+l5),"E5 x3yz sum");
checkzero(matdet([l0,0,0;l3,0,0;l6,0,0]),"forced singular linear part");

print("ALL UNMARKED COMPANION-INFINITY PARI CERTIFICATES PASSED");
quit;

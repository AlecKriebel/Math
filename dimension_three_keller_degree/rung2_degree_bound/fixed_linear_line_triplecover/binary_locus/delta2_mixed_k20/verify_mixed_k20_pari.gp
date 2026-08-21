\\ Independent PARI/GP replay of the fixed-linear mixed {2,0} leaf.

default(parisizemax,512000000);
allocatemem(128000000);

checkzero(value,message) =
{
  if(value != 0,
    print(Str("FAIL: ",message));
    quit(1)
  );
};
jac2(f,g) = deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
jac3(f,g,h) = matdet([deriv(f,p),deriv(f,q),deriv(f,r);deriv(g,p),deriv(g,q),deriv(g,r);deriv(h,p),deriv(h,q),deriv(h,r)]);
jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));
cf(f,ep,eq) = polcoef(polcoef(f,eq,q),ep,p);

{
A=q^2*(a2*p+a3*q);
B=p^3+b2*p*q^2+b3*q^3;
P=p*A; Q=p*B; R=p*(c0*p^2+c2*q^2);
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
N=[deriv(P,q)/(p*q),deriv(Q,q)/(p*q),deriv(R,q)/(p*q)]~;
checkzero(N[1]-(2*a2*p+3*a3*q),"twice-divided first component");
checkzero(N[2]-(2*b2*p+3*b3*q),"twice-divided second component");
checkzero(N[3]-2*c2,"twice-divided third component");
checkzero(alpha*N[1]+beta*N[2]+gam*N[3],
          "twice-divided syzygy");

D=a2*b3-a3*b2;
C=(N[3]*jac2(P,N[2])+N[3]*jac2(N[1],Q)
   -N[2]*jac2(N[1],R)+N[1]*jac2(N[2],R))/2;
checkzero(C+3*p*((3*c0*D+4*a3*c2)*p^2-c2*D*q^2),
          "curvature factor");

f=mm*p+nn*q;
U=f*N[1]; V=f*N[2]; W=f*N[3];
K=polcoef(jac3(P,r*V,r*W)+jac3(r*U,Q,r*W)
          +jac3(r*U,r*V,R),1,r);
res=K-lm*alpha-mu*beta;

\\ First endpoint chart.
evars=[a2,a3,b2,b3,c2,c0];
evals=[1,0,0,1,1,cc];
E=vector(5,i,subst(subst(subst(subst(subst(subst(
  cf(res,5-(i-1),i-1),
  a2,1),a3,0),b2,0),b3,1),c2,1),c0,cc));
checkzero(E[1]+18*cc*mm^2,"first chart p^5");
checkzero(E[2]+2*(18*cc*mm*nn+3*cc*mu+4*lm),
          "first chart p^4q");
checkzero(E[3]+3*(6*cc*nn^2-2*mm^2-3*cc*lm),
          "first chart p^3q^2");
checkzero(E[4]-2*(6*mm*nn+mu),"first chart p^2q^3");
checkzero(E[5]-(6*nn^2+lm),"first chart pq^4");

\\ Second endpoint chart.
F=vector(5,i,subst(subst(subst(subst(subst(subst(
  cf(res,5-(i-1),i-1),
  a2,aa),a3,1),b2,bb),b3,0),c2,1),c0,cc));
EE=4-3*bb*cc;
checkzero(F[1]+6*EE*mm^2,"second chart p^5");
checkzero(F[2]+2*((24-18*bb*cc)*mm*nn+3*aa*cc*mu+EE*lm),
          "second chart p^4q");
checkzero(F[3]+3*((8-6*bb*cc)*nn^2+2*bb*mm^2+3*cc*mu),
          "second chart p^3q^2");
checkzero(F[4]-2*(-6*bb*mm*nn+aa*mu-bb*lm),
          "second chart p^2q^3");
checkzero(F[5]-(-6*bb*nn^2-mu),"second chart pq^4");

\\ Literal higher-gcd factorizations.
P0=p*q^3; Q0=p*(p^3+bb*p*q^2);
R3=p*(4*p^2/(3*bb)+q^2);
a3f=jac2(Q0,R3); b3f=-jac2(P0,R3); g3f=jac2(P0,Q0);
checkzero(a3f-2*bb*p^2*q^3,"delta-three alpha factor");
checkzero(b3f-p*q^2*(bb*q^2+12*p^2)/bb,
          "delta-three beta factor");
checkzero(g3f+4*p^2*q^2*(bb*q^2+3*p^2),
          "delta-three gamma factor");

R4=p*(p^2/(3*bb)+q^2);
G=3*p^2+bb*q^2;
a4f=jac2(Q0,R4); b4f=-jac2(P0,R4); g4f=jac2(P0,Q0);
checkzero(a4f-2*p^2*q*G,"delta-four alpha factor");
checkzero(b4f-p*q^2*G/bb,"delta-four beta factor");
checkzero(g4f+4*p^2*q^2*G,"delta-four gamma factor");

\\ Optional E5 boundary regression.
N4=[3*q,2*bb*p,2]~;
S=TT*q*N4;
H4=[P0,Q0,0];
H3=[r*S[1],r*S[2],R4];
H2=[0,3*bb*TT^2*r^2,r*S[3]];
weighted=matdet(zz*jacmap(H2)+zz^2*jacmap(H3)+zz^3*jacmap(H4));
checkzero(polcoef(weighted,7,zz),"boundary E7");
checkzero(polcoef(weighted,6,zz),"boundary E6");
checkzero(polcoef(polcoef(weighted,5,zz),2,r)-12*TT^3*q*G,
          "boundary E5 r^2");

print("PASS independent PARI mixed {2,0} reconstruction");
}
quit;

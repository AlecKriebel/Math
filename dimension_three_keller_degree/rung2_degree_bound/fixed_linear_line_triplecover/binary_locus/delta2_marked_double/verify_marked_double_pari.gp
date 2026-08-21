\\ Independent PARI/GP replay of the fixed-linear marked-double delta=2 leaf.

default(parisizemax,512000000);
allocatemem(128000000);

checkzero(value,message) =
{
  if(value != 0,
    print(Str("FAIL: ",message));
    quit(1)
  );
};
checktrue(value,message) =
{
  if(!value,
    print(Str("FAIL: ",message));
    quit(1)
  );
};
substmany(f,vars,vals) =
{
  my(g=f);
  if(#vars != #vals,error("substmany length mismatch"));
  for(i=1,#vars,g=subst(g,vars[i],vals[i]));
  g;
};
jac2(f,g) = deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
jac3(f,g,h) = matdet([deriv(f,p),deriv(f,q),deriv(f,r);deriv(g,p),deriv(g,q),deriv(g,r);deriv(h,p),deriv(h,q),deriv(h,r)]);
jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));

{
A=a0*p^3+a1*p^2*q+a2*p*q^2;
B=b0*p^3+b1*p^2*q+b2*p*q^2+q^3;
P=p*A; Q=p*B;

\\ R=p^2 q and the two divided-gradient columns.
R=p^2*q;
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
N1=[deriv(P,q)/p,deriv(Q,q)/p,deriv(R,q)/p]~;
N2=[(deriv(P,p)-q*N1[1]/3)/p,
    (deriv(Q,p)-q*N1[2]/3)/p,
    (deriv(R,p)-q*N1[3]/3)/p]~;
checkzero(alpha*N1[1]+beta*N1[2]+gam*N1[3],
          "R=p^2q first divided-gradient syzygy");
checkzero(alpha*N2[1]+beta*N2[2]+gam*N2[3],
          "R=p^2q second divided-gradient syzygy");
checkzero(deriv(P,p)-q*N1[1]/3-p*N2[1],
          "R=p^2q first gradient reconstruction");
checkzero(deriv(Q,p)-q*N1[2]/3-p*N2[2],
          "R=p^2q second gradient reconstruction");
checkzero(deriv(R,p)-q*N1[3]/3-p*N2[3],
          "R=p^2q third gradient reconstruction");

\\ Generic nonzero contact gives a literal quadratic extra gcd.
b1s=(40*a0*a2+5*a1^2+4*a1*a2*b2)/(4*a2^2);
b0s=(5*a0*a1+4*a0*a2*b2)/(4*a2^2);
G=4*a0*p^2+a1*p*q-2*a2*q^2;
vars=[b0,b1]; vals=[b0s,b1s];
checkzero(substmany(alpha,vars,vals)/p^2
          -G*((5*a1+4*a2*b2)*p+10*a2*q)/(4*a2^2),
          "R=p^2q alpha extra quadratic");
checkzero(substmany(beta,vars,vals)/p^2+p*G,
          "R=p^2q beta extra quadratic");
checkzero(substmany(gam,vars,vals)/p^2
          -G*(10*a0*p^2-5*a1*p*q-2*a2*q^2)/a2,
          "R=p^2q gamma extra quadratic");

\\ The totally ramified contact and its degree-five obstruction.
tt=t;
P0=p^4;
Q0=p*(-2*tt^2*p^2*q/75+tt*p*q^2+q^3);
R0=p^2*q;
N10=[deriv(P0,q)/p,deriv(Q0,q)/p,deriv(R0,q)/p]~;
N20=[(deriv(P0,p)-q*N10[1]/3)/p,
     (deriv(Q0,p)-q*N10[2]/3)/p,
     (deriv(R0,p)-q*N10[3]/3)/p]~;
N=T*(N20-2*tt*N10/45);
X=14*T^2/3;
Y=32*tt^3*T^2/10125;
H4=[P0,Q0,0];
H3=[r*N[1],r*N[2],R0];
H2=[X*r^2,Y*r^2,r*N[3]];
weighted=matdet(zz*jacmap(H2)+zz^2*jacmap(H3)+zz^3*jacmap(H4));
checkzero(polcoef(weighted,7,zz),"totally ramified E7");
checkzero(polcoef(weighted,6,zz),"totally ramified E6");
E5r2=polcoef(polcoef(weighted,5,zz),2,r);
expected=-4*T^3*(404*p^3*tt^3+3150*p^2*q*tt^2
                 -27000*p*q^2*tt-118125*q^3)/30375;
checkzero(E5r2-expected,"totally ramified E5 r^2 obstruction");
checkzero(polcoef(polcoef(E5r2,3,q),0,p)-140*T^3/9,
          "totally ramified q^3 r^2 coefficient");

\\ R=p^3: contact forces an extra linear gcd.
R3=p^3;
alpha3=jac2(Q,R3); beta3=-jac2(P,R3); gam3=jac2(P,Q);
b13=(4*a1*a2*b2-3*a1^2)/(4*a2^2);
L=a1*p+2*a2*q;
C3=3*a0*a1*p^3-4*a0*a2*b2*p^3-6*a0*a2*p^2*q
   -3*a1*a2*p*q^2+4*a2^2*b0*p^3-2*a2^2*q^3;
checkzero(subst(alpha3,b1,b13)/p^2
          -3*p*L*((3*a1-4*a2*b2)*p-6*a2*q)/(4*a2^2),
          "R=p^3 alpha extra line");
checkzero(subst(beta3,b1,b13)/p^2-3*p^2*L,
          "R=p^3 beta extra line");
checkzero(subst(gam3,b1,b13)/p^2+L*C3/a2^2,
          "R=p^3 gamma extra line");
checkzero(subst(alpha3,a2,0)%p^3,"R=p^3 a2=0 alpha boundary");
checkzero(subst(beta3,a2,0)%p^3,"R=p^3 a2=0 beta boundary");
checkzero(subst(gam3,a2,0)%p^3,"R=p^3 a2=0 gamma boundary");

print("PASS independent PARI marked-double reconstruction");
}
quit;

\\ Independent PARI/GP reconstruction of the cubic contact gcd jump.

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
checkmodzero(value,message) =
{
  checkzero(lift(Mod(value,C)),message);
};
jac2(f,g) = deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
jac3(f,g,h) = matdet([deriv(f,p),deriv(f,q),deriv(f,r);deriv(g,p),deriv(g,q),deriv(g,r);deriv(h,p),deriv(h,q),deriv(h,r)]);

{
C=160*a^3-384*a^2+310*a-85;
A=p*q^2+a*q^3;
B=p^3+p^2*q-5*(2*a-1)*q^3/16;
P=p*A;
Q=p*B;
R=p^3+3*p^2*q/4
  -3*(10*a^2-19*a+8)*p*q^2/20
  -(120*a^2-198*a+79)*q^3/320;

alpha=jac2(Q,R);
beta=-jac2(P,R);
gam=jac2(P,Q);
checkzero(subst(alpha,q,0),"alpha lacks the chart divisor q");
checkzero(subst(beta,q,0),"beta lacks the chart divisor q");
checkzero(subst(gam,q,0),"gamma lacks the chart divisor q");

Nu=(deriv(P,q)-deriv(P,p)/4)/q;
Nv=(deriv(Q,q)-deriv(Q,p)/4)/q;
Nt=(deriv(R,q)-deriv(R,p)/4)/q;
checkmodzero(alpha*Nu+beta*Nv+gam*Nt,
             "directional-gradient syzygy");

curvature=jac3(P,r*Nv,r*Nt)
         +jac3(r*Nu,Q,r*Nt)
         +jac3(r*Nu,r*Nv,R);
K=polcoef(curvature,1,r);
lm=2*a^2-3*a+2;
mu=-(16*a-5)/32;
checkmodzero(K-lm*alpha-mu*beta,"contact identity");

G=p^2+(5*a/2-3/4)*p*q
 +(5*a^2/2-23*a/8+15/16)*q^2;
Qa=p^2+(1-a)*p*q
 +(5*a^2/16-27*a/64+15/128)*q^2;
Qb=p^2+(1-a)*p*q
 +(a^2/2-7*a/10+17/80)*q^2;
Qc=p+(5/4-a)*q;
Afac=-12*a^2+114*a/5-177/20;

checkmodzero(alpha/q-Afac*G*Qa,"alpha common factor");
checkmodzero(beta/q-6*G*Qb,"beta common factor");
checkmodzero(gam/q+8*p^2*G*Qc,"gamma common factor");
checktrue(polcoef(polcoef(G,0,q),2,p)==1,
          "common quadratic lost its monic p^2 term");

badG=G-polcoef(G,2,q)*q^2;
checktrue(lift(Mod(beta/q-6*badG*Qb,C)) != 0,
          "common-factor mutation was not detected");

print("PASS independent PARI cubic-contact gcd reconstruction");
}
quit;

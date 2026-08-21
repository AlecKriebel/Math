\\ Independent PARI/GP replay of the unmarked a2=0 boundary.

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
jac2(f,g) = deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
jac3(f,g,h) = matdet([deriv(f,p),deriv(f,q),deriv(f,r);deriv(g,p),deriv(g,q),deriv(g,r);deriv(h,p),deriv(h,q),deriv(h,r)]);
cf(f,ep,eq) = polcoef(polcoef(f,eq,q),ep,p);

{
A=a3*q^3;
B=p^3+b1*p^2*q+b2*p*q^2+b3*q^3;
R=c0*p^3+3*b1*c0*p^2*q/4+c2*p*q^2+c3*q^3;
P=p*A;
Q=p*B;
alpha=jac2(Q,R);
beta=-jac2(P,R);
gam=jac2(P,Q);

Nu=(deriv(P,q)-b1*deriv(P,p)/4)/q;
Nv=(deriv(Q,q)-b1*deriv(Q,p)/4)/q;
Nt=(deriv(R,q)-b1*deriv(R,p)/4)/q;
checkzero(alpha*Nu+beta*Nv+gam*Nt,
          "divided directional-gradient syzygy");
curvature=jac3(P,r*Nv,r*Nt)
         +jac3(r*Nu,Q,r*Nt)
         +jac3(r*Nu,r*Nv,R);
K=polcoef(curvature,1,r);
res=K-lm*alpha-mu*beta;
D=3*b1^2*c0-24*b2*c0+32*c2;
checkzero(cf(res,5,0)+3*a3*D/4,"p5 contact coefficient");

abar=alpha/q;
bbar=beta/q;
gbar=gam/q;
checkzero(subst(abar,q,0)-D*p^4/4,"alpha endpoint");
checkzero(bbar-a3*q*(15*b1*c0*p^2*q+36*c0*p^3
          +4*c2*p*q^2-12*c3*q^3)/4,"beta reduced form");
checkzero(gbar+4*a3*p^2*q*(2*b1*p*q+b2*q^2+3*p^2),
          "gamma reduced form");

c2sol=(24*b2*c0-3*b1^2*c0)/32;
checkzero(subst(subst(abar,c2,c2sol),q,0),
          "contact alpha repeated q");
checkzero(subst(subst(bbar,c2,c2sol),q,0),
          "contact beta repeated q");
checkzero(subst(subst(gbar,c2,c2sol),q,0),
          "contact gamma repeated q");
checktrue(subst(abar,q,0)-(-24*b2*c0+32*c2)*p^4/4 != 0,
          "D mutation was not detected");

print("PASS independent PARI a2=0 repeated-divisor replay");
}
quit;

\\ Independent PARI/GP replay of the marked fixed-linear delta=1 contact.

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
cf(f,ep,eq) = polcoef(polcoef(f,eq,q),ep,p);

{
A=a0*p^3+a1*p^2*q+a2*p*q^2;
B=b0*p^3+b1*p^2*q+b2*p*q^2+q^3;
S=s0*p^2+s1*p*q+q^2;
P=p*A; Q=p*B; R=p*S;

alpha=jac2(Q,R);
beta=-jac2(P,R);
gam=jac2(P,Q);
Nu=deriv(A,q); Nv=deriv(B,q); Nt=deriv(S,q);
checkzero(alpha*Nu+beta*Nv+gam*Nt,
          "divided q-gradient is not a syzygy");

curvature=jac3(P,r*Nv,r*Nt)
         +jac3(r*Nu,Q,r*Nt)
         +jac3(r*Nu,r*Nv,R);
checkzero(polcoef(curvature,0,r),"contact curvature constant-r term");
checkzero(polcoef(curvature,2,r),"contact curvature r^2 term");
K=polcoef(curvature,1,r);
residual=K-lm*alpha-mu*beta;

\\ S=q^2: p^4 contact coefficient and the new q divisor.
double=substmany(residual,[s0,s1],[0,0])/p;
checkzero(cf(double,4,0)+8*(a0*b1-a1*b0),
          "double-root p^4 contact coefficient");
ad=substmany(alpha,[s0,s1],[0,0])/p;
bd=substmany(beta,[s0,s1],[0,0])/p;
gd=substmany(gam,[s0,s1],[0,0])/p;
checkzero(subst(ad,q,0),"double-root alpha lacks q factor");
checkzero(subst(bd,q,0),"double-root beta lacks q factor");
checkzero(subst(gd,q,0)-4*(a0*b1-a1*b0)*p^5,
          "double-root gamma endpoint");

\\ S=p^2+q^2, then a2=1 and b2=0.
square=substmany(residual,[s0,s1],[1,0])/p;
gauge=substmany(square,[a2,b2],[1,0]);
eq0=cf(gauge,4,0);
eq1=cf(gauge,3,1);
eq2=cf(gauge,2,2);
eq3=cf(gauge,1,3);
eq4=cf(gauge,0,4);
checkzero(eq4-(6+lm),"squarefree q^4 equation");
checkzero(subst(eq3,lm,-6)-2*(7*a1+mu),
          "squarefree p q^3 equation");

solvars=[lm,mu,b0,b1];
solvals=[-6,-7*a1,(7*a0-3)*a1/6,
         (72-24*a0+35*a1^2)/28];
checkzero(substmany(eq1,solvars,solvals),"squarefree p^3 q solve");
checkzero(substmany(eq2,solvars,solvals),"squarefree p^2 q^2 solve");
checkzero(substmany(eq0,solvars,solvals)
          -2/21*(a0-3)*(72*a0-7*a1^2+108),
          "squarefree final contact factor");

\\ The a2=0 boundary is inconsistent before this gauge.
boundary=substmany(square,[a2],[0]);
checkzero(cf(boundary,0,4)-lm,"a2=0 first equation");
checkzero(substmany(cf(boundary,1,3),[lm],[0])-14*a1,
          "a2=0 second equation");
checkzero(substmany(cf(boundary,3,1),[lm,a1],[0,0])-8*a0*mu,
          "a2=0 third equation");
checkzero(substmany(cf(boundary,2,2),[lm,a1,mu],[0,0,0])-24*a0,
          "a2=0 terminal equation");

\\ Literal common factors on the two contact components.
G1=3*tt*p^3-18*p^2*q-5*tt*p*q^2-2*q^3;
f1vars=[s0,s1,a2,b2,a0,a1,b0,b1];
f1vals=[1,0,1,0,3,tt,3*tt,5*tt^2/4];
checkzero(substmany(alpha,f1vars,f1vals)
          +p*(5*p*tt-2*q)*G1/4,"family one alpha factor");
checkzero(substmany(beta,f1vars,f1vals)-p^2*G1,
          "family one beta factor");
checkzero(substmany(gam,f1vars,f1vals)-p^2*(p*tt-2*q)*G1,
          "family one gamma factor");

G2=27*p^2-7*tt*p*q-3*q^2;
f2vars=[s0,s1,a2,b2,a0,a1,b0,b1];
f2vals=[1,0,1,0,7*tt^2/72-3/2,tt,
        tt*(49*tt^2-972)/432,(49*tt^2+162)/42];
checkzero(substmany(alpha,f2vars,f2vals)
          +p*G2*(49*p^2*tt^2+162*p^2+294*p*q*tt-126*q^2)/378,
          "family two alpha factor");
checkzero(substmany(beta,f2vars,f2vals)
          -p^2*(p*tt+6*q)*G2/9,"family two beta factor");
checkzero(substmany(gam,f2vars,f2vals)
          -p^2*G2*(49*p^2*tt^2-324*p^2+168*p*q*tt-504*q^2)/378,
          "family two gamma factor");

checktrue(subst(G1,tt,0) != 0 && subst(G2,tt,0) != 0,
          "common-factor nonzero mutation");
print("PASS independent PARI marked fixed-linear delta=1 contact replay");
}
quit;

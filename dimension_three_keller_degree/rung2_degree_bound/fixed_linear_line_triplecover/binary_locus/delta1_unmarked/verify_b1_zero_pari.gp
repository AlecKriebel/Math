\\ Independent PARI/GP replay of the unmarked b1=0 boundary.

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
P=p*(p*q^2+a*q^3);
Q=p*(p^3+b*q^3);
R=p^3+c*p*q^2+d*q^3;
alpha=jac2(Q,R);
beta=-jac2(P,R);
gam=jac2(P,Q);

Nu=deriv(P,q)/q;
Nv=deriv(Q,q)/q;
Nt=deriv(R,q)/q;
checkzero(alpha*Nu+beta*Nv+gam*Nt,
          "divided directional-gradient syzygy");
curvature=jac3(P,r*Nv,r*Nt)
         +jac3(r*Nu,Q,r*Nt)
         +jac3(r*Nu,r*Nv,R);
K=polcoef(curvature,1,r);
residual=K-lm*alpha-mu*beta;
dsol=a*c+3*b/4;
E=vector(6,i,subst(cf(residual,5-(i-1),i-1),d,dsol));

checkzero(E[1],"first contact coefficient");
checkzero(E[2]+2*(4*c*lm+3*mu),"second contact coefficient");
checkzero(E[3]+3*(4*a*c*lm+3*a*mu-2*b*c),
          "third contact coefficient");
checkzero(E[4]-(12*a*b*c+9*b^2+4*c*mu)/2,
          "fourth contact coefficient");

f1=4*c*lm+3*mu;
f2=4*a*c*lm+3*a*mu-2*b*c;
f3=12*a*b*c+9*b^2+4*c*mu;
checkzero(f2-a*f1+2*b*c,"division-free bc consequence");
checkzero(subst(f3,c,0)-9*b^2,"c=0 boundary implication");
checkzero(subst(f3,b,0)-4*c*mu,"b=0 complementary implication");

ac=subst(subst(alpha,b,0),d,a*c);
bc=subst(subst(beta,b,0),d,a*c);
gc=subst(subst(gam,b,0),d,a*c);
line=2*p+3*a*q;
checkzero(ac-4*c*p^3*q*line,"alpha extra line");
checkzero(bc-q*line*(3*p^3-c*p*q^2-a*c*q^3),
          "beta extra line");
checkzero(gc+4*p^4*q*line,"gamma extra line");
checktrue(gc+4*p^4*q*(2*p+2*a*q) != 0,
          "line-factor mutation was not detected");

print("PASS independent PARI b1=0 contact/gcd replay");
}
quit;

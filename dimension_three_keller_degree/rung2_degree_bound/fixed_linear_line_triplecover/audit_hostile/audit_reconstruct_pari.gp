\\ Independent exact audit of powers, signs, eigen-kernel ranks, and both
\\ determinant polarizations.

checkzero(value,message) = if(value != 0,print(Str("FAIL: ",message));quit(1));
checktrue(value,message) = if(!value,print(Str("FAIL: ",message));quit(1));
coeff3(P,ep,eq,er) = polcoef(polcoef(polcoef(P,er,r),eq,q),ep,p);

{
A = a0*p^3+a1*p^2*q+a2*p*q^2+a3*q^3;
B = b0*p^3+b1*p^2*q+b2*p*q^2+b3*q^3;
P = r*A;
Q = r*B;
gradP = [deriv(P,p),deriv(P,q),deriv(P,r)]~;
gradQ = [deriv(Q,p),deriv(Q,q),deriv(Q,r)]~;
D =
  [gradP[2]*gradQ[3]-gradP[3]*gradQ[2],
   gradP[3]*gradQ[1]-gradP[1]*gradQ[3],
   gradP[1]*gradQ[2]-gradP[2]*gradQ[1]]~;
at=a0+a1*t+a2*t^2+a3*t^3;
bt=b0+b1*t+b2*t^2+b3*t^3;
w=at*deriv(bt,t)-deriv(at,t)*bt;
Dchart=subst(subst(D,q,p*t),r,p*s);
checkzero(Dchart-p^6*s*w*[-1,-t,3*s]~,
          "full cross-product sign or p exponent");

quadmons=[p^2,p*q,q^2,p*r,q*r,r^2];
cubmons=[p^3,p^2*q,p*q^2,q^3,p^2*r,p*q*r,q^2*r,p*r^2,q*r^2,r^3];
g2c=[g20,g21,g22,g23,g24,g25];
g3c=[g30,g31,g32,g33,g34,g35,g36,g37,g38,g39];
G2=sum(i=1,6,g2c[i]*quadmons[i]);
G3=sum(i=1,10,g3c[i]*cubmons[i]);
DG2=deriv(G2,p)*D[1]+deriv(G2,q)*D[2]+deriv(G2,r)*D[3];
DG3=deriv(G3,p)*D[1]+deriv(G3,q)*D[2]+deriv(G3,r)*D[3];
g2=subst(subst(G2,q,p*t),r,p*s)/p^2;
g3=subst(subst(G3,q,p*t),r,p*s)/p^3;
checkzero(subst(subst(DG2,q,p*t),r,p*s)
          -p^7*s*w*(4*s*deriv(g2,s)-2*g2),
          "full quadratic derivation exponent");
checkzero(subst(subst(DG3,q,p*t),r,p*s)
          -p^8*s*w*(4*s*deriv(g3,s)-3*g3),
          "full cubic derivation exponent");

op2=4*s*deriv(g2,s)-2*g2;
op3=4*s*deriv(g3,s)-3*g3;
rpower2=[0,0,0,1,1,2];
rpower3=[0,0,0,0,1,1,1,2,2,3];
for (i=1,6,
  monchart=subst(subst(quadmons[i],q,p*t),r,p*s)/p^2;
  checkzero(deriv(op2,g2c[i])-(4*rpower2[i]-2)*monchart,
            "quadratic eigenvalue table");
  checktrue(4*rpower2[i]-2!=0,"quadratic zero eigenvalue")
);
for (i=1,10,
  monchart=subst(subst(cubmons[i],q,p*t),r,p*s)/p^3;
  checkzero(deriv(op3,g3c[i])-(4*rpower3[i]-3)*monchart,
            "cubic eigenvalue table");
  checktrue(4*rpower3[i]-3!=0,"cubic zero eigenvalue")
);

\\ Completely independent matrix entries for the polarizations.
L=[l0,l1,l2;l3,l4,l5;l6,l7,l8];
J2=[x0,x1,x2;x3,x4,x5;x6,x7,x8];
J3=[u0,u1,u2;u3,u4,u5;u6,u7,u8];
C=[c0,c1,c2;c3,c4,c5;0,0,0];
weighted=matdet(L+zz*J2+zz^2*J3+zz^3*C);
expectedE8=matdet([c0,c1,c2;c3,c4,c5;u6,u7,u8]);
checkzero(polcoef(weighted,8,zz)-expectedE8,"raw E8 polarization");
weightedafter=subst(subst(subst(weighted,u6,0),u7,0),u8,0);
expectedE7=matdet([c0,c1,c2;c3,c4,c5;x6,x7,x8]);
checkzero(polcoef(weightedafter,7,zz)-expectedE7,
          "raw E7 polarization after cubic exit");

print("AUDIT_FIXED_LINEAR_TRIPLECOVER_PARI_PASS_9B6E20");
}
quit;

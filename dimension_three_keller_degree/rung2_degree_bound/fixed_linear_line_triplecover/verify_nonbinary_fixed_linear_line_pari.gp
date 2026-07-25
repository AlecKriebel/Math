\\ Independent exact PARI/GP checks for the nonbinary fixed-linear
\\ line triple-cover row.

jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));
checkzero(value,message) = if(value != 0,print(Str("FAIL: ",message));quit(1));

aform = a0*p^3+a1*p^2*q+a2*p*q^2+a3*q^3;
bform = b0*p^3+b1*p^2*q+b2*p*q^2+b3*q^3;
P = r*aform;
Q = r*bform;
gradP = [deriv(P,p),deriv(P,q),deriv(P,r)]~;
gradQ = [deriv(Q,p),deriv(Q,q),deriv(Q,r)]~;
D = [gradP[2]*gradQ[3]-gradP[3]*gradQ[2],gradP[3]*gradQ[1]-gradP[1]*gradQ[3],gradP[1]*gradQ[2]-gradP[2]*gradQ[1]]~;

at = a0+a1*t+a2*t^2+a3*t^3;
bt = b0+b1*t+b2*t^2+b3*t^3;
w = at*deriv(bt,t)-deriv(at,t)*bt;
Ddehom = subst(subst(subst(D,p,1),q,t),r,s);
checkzero(Ddehom-s*w*[-1,-t,3*s]~,"cross-product normal form");

quadmons = [p^2,p*q,q^2,p*r,q*r,r^2];
cubmons = [p^3,p^2*q,p*q^2,q^3,p^2*r,p*q*r,q^2*r,p*r^2,q*r^2,r^3];
g2coeffs = [g20,g21,g22,g23,g24,g25];
g3coeffs = [g30,g31,g32,g33,g34,g35,g36,g37,g38,g39];
G2 = sum(i=1,6,g2coeffs[i]*quadmons[i]);
G3 = sum(i=1,10,g3coeffs[i]*cubmons[i]);

DG2 = deriv(G2,p)*D[1]+deriv(G2,q)*D[2]+deriv(G2,r)*D[3];
DG3 = deriv(G3,p)*D[1]+deriv(G3,q)*D[2]+deriv(G3,r)*D[3];
g2 = subst(subst(subst(G2,p,1),q,t),r,s);
g3 = subst(subst(subst(G3,p,1),q,t),r,s);
checkzero(subst(subst(subst(DG2,p,1),q,t),r,s)-s*w*(4*s*deriv(g2,s)-2*g2),"quadratic derivation formula");
checkzero(subst(subst(subst(DG3,p,1),q,t),r,s)-s*w*(4*s*deriv(g3,s)-3*g3),"cubic derivation formula");

\\ Independent determinant extraction with algebraically independent matrix
\\ entries.  This avoids reusing the polynomial derivation algorithm.
L0 = [l0,l1,l2;l3,l4,l5;l6,l7,l8];
J2 = [x0,x1,x2;x3,x4,x5;x6,x7,x8];
J3 = [u0,u1,u2;u3,u4,u5;0,0,0];
C0 = [c0,c1,c2;c3,c4,c5;0,0,0];
weighted = matdet(L0+zz*J2+zz^2*J3+zz^3*C0);
checkzero(polcoef(weighted,8,zz),"degree-eight term after cubic exit");
expectedE7 = matdet([c0,c1,c2;c3,c4,c5;x6,x7,x8]);
checkzero(polcoef(weighted,7,zz)-expectedE7,"degree-seven determinant extraction");
actualE7 = matdet([deriv(P,p),deriv(P,q),deriv(P,r);deriv(Q,p),deriv(Q,q),deriv(Q,r);deriv(G2,p),deriv(G2,q),deriv(G2,r)]);
checkzero(actualE7-DG2,"Jacobian derivation orientation");

print("nonbinary fixed-linear line triple-cover PARI/GP checks passed");
quit;

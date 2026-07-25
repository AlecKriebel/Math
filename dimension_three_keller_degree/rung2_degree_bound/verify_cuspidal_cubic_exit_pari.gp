\\ Independent exact checks for WORKING_CUSPIDAL_CUBIC_CURVE_EXIT.md.

cross3(x,y) = [x[2]*y[3]-x[3]*y[2],x[3]*y[1]-x[1]*y[3],x[1]*y[2]-x[2]*y[1]]~;
jacmap(H) = matrix(3,3,i,j,deriv(H[i],[p,q,r][j]));
thetaMap(H) = vector(3,i,-p*deriv(H[i],p)-q*deriv(H[i],q)+3*r*deriv(H[i],r))~;

A = [p^2*q,p^3,q^3]~;
Ap = vector(3,i,deriv(A[i],p))~;
Aq = vector(3,i,deriv(A[i],q))~;
S = [2*q,3*p,0]~;
T = [p^2,0,3*q^2]~;
N = [3*p*q^2,-2*q^3,-p^3]~;
Delta = cross3(Ap,Aq);

if (Delta != 3*p*N, error("ramified normal mismatch"));
if (cross3(S,T) != 3*N, error("Hilbert--Burch minors mismatch"));
if (Ap != p*S, error("A_p syzygy mismatch"));
if (Aq != T, error("A_q syzygy mismatch"));

H4 = r*A;
kvec = [-p,-q,3*r]~;
expectedAdjugate = r*kvec*Delta~/3;
if (matadjoint(jacmap(H4))-expectedAdjugate != 0, error("rank-one adjugate mismatch"));

\\ Complete degree-eight family.
Q = qa*p^2+qb*p*q+qc*q^2;
ell = laa*p+lbb*q;
mm = maa*p+mbb*q;
H3eight = S*(Q+r*ell+et*r^2)+T*(mm+be*r);
if (N~*thetaMap(H3eight) != 0, error("degree-eight syzygy family mismatch"));

\\ Specialized r=0 degree-seven square.
Q0 = aa*p^2+bb*p*q+cc*q^2;
m0 = dd*p+ee*q;
V0 = Q0*S+m0*T;
V0p = vector(3,i,deriv(V0[i],p))~;
V0q = vector(3,i,deriv(V0[i],q))~;
normalMinor = matdet(matrix(3,3,i,j,if(j==1,V0p[i],if(j==2,V0q[i],A[i]))));
expectedMinor = -18*q*(dd*p^3+(ee-aa)*p^2*q-bb*p*q^2-cc*q^3)^2;
if (normalMinor-expectedMinor != 0, error("r=0 degree-seven square mismatch"));

\\ The three raw left-kernel compatibility coefficients.  The H2
\\ coefficient rows at these monomials are zero; setting H2=0 therefore
\\ reads off their exact inhomogeneous terms.
H3pre = lm*A+r*((al*p+ga*q)*S+be*T)+et*r^2*S;
preWeighted = s^2*jacmap(H3pre)+s^3*jacmap(H4);
preSeven = polcoef(matdet(preWeighted),7,s);
c15 = polcoef(polcoef(polcoef(preSeven,2,r),5,q),0,p);
c16 = polcoef(polcoef(polcoef(preSeven,3,r),4,q),0,p);
c17 = polcoef(polcoef(polcoef(preSeven,4,r),3,q),0,p);
if (c15 != 6*ga^2, error("first left-kernel coefficient mismatch"));
if (c16 != 36*et*ga, error("second left-kernel coefficient mismatch"));
if (c17 != 30*et^2, error("third left-kernel coefficient mismatch"));

\\ Full parameterized degree-seven solution.
D2A = vector(3,i,al^2*deriv(deriv(A[i],p),p)+2*al*be*deriv(deriv(A[i],p),q)+be^2*deriv(deriv(A[i],q),q))~;
H3 = lm*A+r*(al*Ap+be*Aq);
H2 = (u*Ap+v*Aq)/3+r*D2A/2+(w*q+ka*r)*S/3;
upperWeighted = s*jacmap(H2)+s^2*jacmap(H3)+s^3*jacmap(H4);
if (polcoef(matdet(upperWeighted),7,s) != 0, error("parameterized degree-seven solution mismatch"));

\\ Degree-six solution with the arbitrary surviving entry rh.
L0 = [2*(-3*al*be*lm+al*v+be*u)/3,(3*al^2*lm-2*al*u+2*be*w+2*rh)/3,be*(3*al^2+2*ka)/3;rh,al*w,al*(al^2+ka);0,be*(-3*be*lm+2*v),be^3];
weighted = L0+s*jacmap(H2)+s^2*jacmap(H3)+s^3*jacmap(H4);
determinant = matdet(weighted);
if (polcoef(determinant,8,s) != 0, error("degree eight mismatch"));
if (polcoef(determinant,7,s) != 0, error("degree seven mismatch"));
if (polcoef(determinant,6,s) != 0, error("degree six mismatch"));

XX = (v-3*be*lm)*p^2+(3*al*lm-u)*p*q-w*q^2;
expectedFive = -4*q*(XX-ka*q*r)*(XX+ka*q*r)/3;
if (polcoef(determinant,5,s)-expectedFive != 0, error("degree-five factorization mismatch"));

\\ Degree-five compatibility specialization.
H2final = lm*(al*Ap+be*Aq)+r*D2A/2;
Lfinal = [2*al*be*lm,-al^2*lm+2*rh/3,al^2*be;rh,0,al^3;0,3*be^2*lm,be^3];
finalWeighted = Lfinal+s*jacmap(H2final)+s^2*jacmap(H3)+s^3*jacmap(H4);
finalDeterminant = matdet(finalWeighted);
for (degree=4,8,if (polcoef(finalDeterminant,degree,s) != 0,error("unexpected surviving upper coefficient")));

square = (rh-3*al^2*lm)^2;
if (polcoef(finalDeterminant,3,s) != -2*q^3*square/3, error("degree-three square mismatch"));
if (polcoef(finalDeterminant,2,s) != -2*be*q^2*square, error("degree-two square mismatch"));
if (polcoef(finalDeterminant,1,s) != -2*be^2*q*square, error("degree-one square mismatch"));
if (polcoef(finalDeterminant,0,s) != -2*be^3*square/3, error("linear determinant mismatch"));
if (matdet(Lfinal) != -2*be^3*square/3, error("direct linear determinant mismatch"));

print("cuspidal cubic-stratum exit PARI/GP checks passed");
quit;

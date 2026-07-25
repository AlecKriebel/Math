\\ Exact checks for WORKING_NODAL_CUBIC_CURVE_EXIT.md.

cross3(x,y) = [x[2]*y[3]-x[3]*y[2],x[3]*y[1]-x[1]*y[3],x[1]*y[2]-x[2]*y[1]]~;
jacmap(H) = matrix(3,3,i,j,deriv(H[i],[p,q,r][j]));

A = [p^2*q,p*q^2,p^3+q^3]~;
Ap = vector(3,i,deriv(A[i],p))~;
Aq = vector(3,i,deriv(A[i],q))~;

ell = aa*p+bb*q;
m = cc*p+dd*q;
V = ell*Ap+m*Aq;
normalMinor = matdet(matrix(3,3,i,j,if(j==1,deriv(V[i],p),if(j==2,deriv(V[i],q),A[i]))));
expectedMinor = 6*(p^3+q^3)*(cc*p^2+(dd-aa)*p*q-bb*q^2)^2;
if (normalMinor-expectedMinor != 0, error("normal-minor factorization mismatch"));

D2A = vector(3,i,alpha^2*deriv(deriv(A[i],p),p)+2*alpha*beta*deriv(deriv(A[i],p),q)+beta^2*deriv(deriv(A[i],q),q))~;
H4 = r*A;
H3 = lambda*A+r*(alpha*Ap+beta*Aq);
H2 = (u*Ap+v*Aq)/3+r*D2A/2;

L0 = [-2*alpha*beta*lambda+2*(alpha*v+beta*u)/3,-alpha^2*lambda+2*alpha*u/3,alpha^2*beta;-beta^2*lambda+2*beta*v/3,-2*alpha*beta*lambda+2*(alpha*v+beta*u)/3,alpha*beta^2;-3*alpha^2*lambda+2*alpha*u,-3*beta^2*lambda+2*beta*v,alpha^3+beta^3];

weighted = L0+s*jacmap(H2)+s^2*jacmap(H3)+s^3*jacmap(H4);
determinant = matdet(weighted);
if (polcoef(determinant,8,s) != 0, error("degree eight mismatch"));
if (polcoef(determinant,7,s) != 0, error("degree seven mismatch"));
if (polcoef(determinant,6,s) != 0, error("degree six mismatch"));

expectedDet = 4*(alpha^3+beta^3)*(alpha*v-beta*u)^2/9;
if (matdet(L0)-expectedDet != 0, error("linear determinant mismatch"));

expectedFive = 4*(p^3+q^3)*((3*beta*lambda-v)*p+(u-3*alpha*lambda)*q)^2/9;
if (polcoef(determinant,5,s)-expectedFive != 0, error("degree five mismatch"));

print("nodal cubic-stratum exit PARI/GP checks passed");
quit;

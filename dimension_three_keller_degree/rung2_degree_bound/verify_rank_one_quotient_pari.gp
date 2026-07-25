\\ Exact checks for WORKING_RANK_ONE_QUOTIENT_CUBIC.md.

L = x + 2*y + 3*z;
Q = x^3 + 2*y^3 + 3*z^3 + x*y*z;
P = L^3;
h = L*(5*P + 7*Q);

jac(f,g,k) = matdet([deriv(f,x),deriv(f,y),deriv(f,z); deriv(g,x),deriv(g,y),deriv(g,z); deriv(k,x),deriv(k,y),deriv(k,z)]);

if (jac(P,Q,h) != 0, error("exceptional normal form does not satisfy Jac(P,Q,h)=0"));

B = [p1,p2,p3; q1,q2,q3; s1,s2,s3];
C = [0,0,0; 0,0,0; r1,r2,r3];
coeff = polcoef(matdet(B + t*C),1,t);
formal_jac = matdet([p1,p2,p3; q1,q2,q3; r1,r2,r3]);
if (coeff != formal_jac, error("degree-seven determinant coefficient mismatch"));

print("rank-one quotient-cubic PARI/GP checks passed");
quit;

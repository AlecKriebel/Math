\\ Exact regressions for WORKING_RANK_ONE_COMPOSITE_EXIT.md.

jac(f,g,k) = matdet([deriv(f,x),deriv(f,y),deriv(f,z); deriv(g,x),deriv(g,y),deriv(g,z); deriv(k,x),deriv(k,y),deriv(k,z)]);
jac2(f,g) = deriv(f,x)*deriv(g,y)-deriv(f,y)*deriv(g,x);

P = p0*x^3+p1*x^2*y+p2*x*y^2+p3*y^3;
Q = q0*x^3+q1*x^2*y+q2*x*y^2+q3*y^3;
h = h0*x^4+h1*x^3*y+h2*x^2*y^2+h3*x*y^3+h4*y^4;
S = s0*x^2+s1*x*y+s2*x*z+s3*y^2+s4*y*z+s5*z^2;
T = t0*x^2+t1*x*y+t2*x*z+t3*y^2+t4*y*z+t5*z^2;
U = u0*x^2+u1*x*y+u2*x*z+u3*y^2+u4*y*z+u5*z^2;
R = r0*x^3+r1*x^2*y+r2*x^2*z+r3*x*y^2+r4*x*y*z+r5*x*z^2+r6*y^3+r7*y^2*z+r8*y*z^2+r9*z^3;
linear1 = l0*x+l1*y+l2*z;
linear2 = m0*x+m1*y+m2*z;

a = jac2(Q,h);
b = jac2(P,h);
c = jac2(P,Q);
E6 = jac(P,Q,R)+jac(P,T,h)+jac(S,Q,h);
if (E6-(a*deriv(S,z)-b*deriv(T,z)+c*deriv(R,z)) != 0, error("degree-six sign mismatch"));

S0 = subst(S,z,0);
T0 = subst(T,z,0);
R0 = subst(R,z,0);
E5 = jac(linear1,Q,h)+jac(P,linear2,h)+jac(S0,T0,h)+jac(P,Q,U)+jac(P,T0,R0)+jac(S0,Q,R0);
expectedE5 = a*deriv(linear1,z)-b*deriv(linear2,z)+c*deriv(U,z);
if (E5-expectedE5 != 0, error("degree-five mismatch"));

print("rank-one composite-exit PARI/GP checks passed");
quit;

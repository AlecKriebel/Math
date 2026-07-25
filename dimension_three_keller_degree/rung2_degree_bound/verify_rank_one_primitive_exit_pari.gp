\\ Exact regressions for WORKING_RANK_ONE_PRIMITIVE_EXIT.md.

jac(f,g,k) = matdet([deriv(f,x),deriv(f,y),deriv(f,z); deriv(g,x),deriv(g,y),deriv(g,z); deriv(k,x),deriv(k,y),deriv(k,z)]);

P = x^3;
Q = q0*x^3 + q1*x^2*y + q2*x^2*z + q3*x*y^2 + q4*x*y*z + q5*x*z^2 + q6*y^3 + q7*y^2*z + q8*y*z^2 + q9*z^3;
S = s0*x^2 + s1*x*y + s2*x*z + s3*y^2 + s4*y*z + s5*z^2;
T = t0*x^2 + t1*x*y + t2*x*z + t3*y^2 + t4*y*z + t5*z^2;
U = u0*x^2 + u1*x*y + u2*x*z + u3*y^2 + u4*y*z + u5*z^2;
R = r0*x^3 + r1*x^2*y + r2*x^2*z + r3*x*y^2 + r4*x*y*z + r5*x*z^2 + r6*y^3 + r7*y^2*z + r8*y*z^2 + r9*z^3;
linear = l0*x + l1*y + l2*z;
h = mu*x^4 + nu*x*Q;

D(f) = jac(P,Q,f);
E6 = D(R) + jac(P,T,h) + jac(S,Q,h);
K = 3*x^2*R - 3*nu*x^3*T - 4*mu*x^3*S - nu*Q*S;
if (D(K) - 3*x^2*E6 != 0, error("degree-six identity mismatch"));

Rpure = 4*mu*x*S/3;
E5 = jac(linear,Q,mu*x^4) + jac(S,T,mu*x^4) + jac(P,Q,U) + jac(P,T,Rpure) + jac(S,Q,Rpure);
W = 9*x^2*U - 2*mu*S^2 - 12*mu*x^3*linear;
if (D(W) - 9*x^2*E5 != 0, error("degree-five identity mismatch"));

f = x^3 + x*y + alpha*x + beta*y;
if (subst(subst(deriv(f,x),x,-beta),y,-3*beta^2-alpha) != 0, error("critical x derivative mismatch"));
if (subst(subst(deriv(f,y),x,-beta),y,-3*beta^2-alpha) != 0, error("critical y derivative mismatch"));
if (deriv(f,z) != 0, error("critical z derivative mismatch"));

print("rank-one primitive-exit PARI/GP checks passed");
quit;

\\ Independent PARI/GP replay for the D4-SF-11CC exclusion.
\\ This file reconstructs the determinants directly; it does not call SymPy.

assert0(value, label) =
{
  if (value != 0, error(Str("ASSERT_ZERO failed: ", label, " = ", value)));
};

subs_many(value, variables, replacements) =
{
  my(result = value);
  for (index = 1, #variables,
    result = subst(result, variables[index], replacements[index])
  );
  result;
};

jac2(f, g) = deriv(f, p) * deriv(g, q) - deriv(f, q) * deriv(g, p);

jac3(column) =
{
  matrix(3, 3, row, col,
    deriv(column[row], if(col == 1, p, if(col == 2, q, r)))
  );
};

coefficient3(poly, ip, iq, ir) =
  polcoef(polcoef(polcoef(poly, ip, p), iq, q), ir, r);

main() =
{
h = p^2 - 4*p*q + q^2;
P = h*p^2;
Q = h*q^2;
R = h*(p + q);
alpha = jac2(Q, R);
beta = -jac2(P, R);
gam = jac2(P, Q);

assert0(alpha * (-(3*p-q)/3) + beta * (-(p-3*q)/3), "sx0");
assert0(alpha * ((15*p-4*q)/9) + beta * (p/9) + gam, "sx1");
assert0(alpha * (-p*(3*p-q)/3) + beta * (-p*(p-3*q)/3), "sy0");
assert0(
  alpha * (-(p+3*q)*(3*p-q)/9)
  + beta * (-(p-3*q)*(p+3*q)/9),
  "sy1"
);
assert0(alpha * (p*(15*p-4*q)/9) + beta * (p^2/9) + gam*p, "sy2");
assert0(
  alpha * ((3*p^2+44*p*q-12*q^2)/27)
  + beta * (p^2/27)
  + gam*q,
  "sy3"
);

U2 = x0 * (-(3*p-q)/3) + x1 * ((15*p-4*q)/9);
V2 = x0 * (-(p-3*q)/3) + x1 * (p/9);
T2 = x1;
U1 = y0 * (-p*(3*p-q)/3)
     + y1 * (-(p+3*q)*(3*p-q)/9)
     + y2 * (p*(15*p-4*q)/9)
     + y3 * ((3*p^2+44*p*q-12*q^2)/27);
V1 = y0 * (-p*(p-3*q)/3)
     + y1 * (-(p-3*q)*(p+3*q)/9)
     + y2 * (p^2/9)
     + y3 * (p^2/27);
T1 = y2*p + y3*q;

topU0 = cu0*p^3 + cu1*p^2*q + cu2*p*q^2 + cu3*q^3;
topV0 = cv0*p^3 + cv1*p^2*q + cv2*p*q^2 + cv3*q^3;
topT0 = ct0*p^2 + ct1*p*q + ct2*q^2;
topU = topU0 + r*U1 + r^2*U2/2;
topV = topV0 + r*V1 + r^2*V2/2;
topT = topT0 + r*T1 + r^2*T2/2;
topA = r*(ca0*p + ca1*q) + ca2*r^2;
topB = r*(cb0*p + cb1*q) + cb2*r^2;
topL = matrix(3, 3, row, col, if(row == 3 && col == 3, cl33, 0));
topdet = matdet(
  topL
  + w*jac3([topA, topB, topT]~)
  + w^2*jac3([topU, topV, R]~)
  + w^3*jac3([P, Q, 0]~)
);
assert0(polcoef(topdet, 7, w), "top E7");
topE6 = polcoef(topdet, 6, w);

c503 = coefficient3(topE6, 3, 0, 3);
c213 = coefficient3(topE6, 2, 1, 3);
c501 = coefficient3(topE6, 5, 0, 1);
c411 = coefficient3(topE6, 4, 1, 1);
c321 = coefficient3(topE6, 3, 2, 1);
c231 = coefficient3(topE6, 2, 3, 1);

assert0(27*c503/4 - (3*x0-x1)^2, "force x first");
assert0(27*c503 + 27*c213/4 - (3*x0-4*x1)^2, "force x second");
force_y_first = 243*c501/8;
force_y_second = 189*c501 + 405*c411/8 + 27*c321/2 + 27*c231/8;
assert0(
  subst(subst(force_y_first, x0, 0), x1, 0)
  - (9*y0+3*y1-3*y2-y3)^2,
  "force y first"
);
assert0(
  subst(subst(force_y_second, x0, 0), x1, 0)
  - (3*y1-4*y3)^2,
  "force y second"
);

plane_vars = [
  x0, x1, y0, y1,
  ca0, ca1, ca2, cb0, cb1, cb2, cl33,
  cu0, cu1, cu2, cu3, cv0, cv1, cv2, cv3, ct0, ct1, ct2
];
plane_vals = [
  0,
  0,
  (y2-y3)/3,
  4*y3/3,
  0,
  0,
  -(y2^2+3*y3^2)/36,
  0,
  0,
  -(3*y2^2+y3^2)/36,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
];
assert0(subs_many(topE6, plane_vars, plane_vals), "contact-plane sufficiency");
print("D4_SF_11CC_PARI_CONTACT_PASS");

mon3 = [p^3, p^2*q, p*q^2, q^3];
mon2 = [p^2, p*q, p*r, q^2, q*r, r^2];
mon2b = [p^2, p*q, q^2];
uu = [u0, u1, u2, u3];
vv = [v0, v1, v2, v3];
tt = [t0, t1, t2];
aa = [a0, a1, a2, a3, a4, a5];
bb = [b0, b1, b2, b3, b4, b5];
ll = [l0, l1, l2, l3, l4, l5, l6, l7, l8];

U0 = sum(index = 1, 4, uu[index]*mon3[index]);
V0 = sum(index = 1, 4, vv[index]*mon3[index]);
T0 = sum(index = 1, 3, tt[index]*mon2b[index]);
A = sum(index = 1, 6, aa[index]*mon2[index]);
B = sum(index = 1, 6, bb[index]*mon2[index]);
linear = matrix(3, 3, row, col, ll[3*(row-1)+col]);

contactU = p*(4*m*p-m*q+n*q)/3;
contactV = q*(m*p-n*p+4*n*q)/3;
contactT = m*p+n*q;

fulldet = matdet(
  linear
  + w*jac3([A, B, T0+r*contactT]~)
  + w^2*jac3([U0+r*contactU, V0+r*contactV, R]~)
  + w^3*jac3([P, Q, 0]~)
);
assert0(polcoef(fulldet, 9, w), "full E9");
assert0(polcoef(fulldet, 8, w), "full E8");
assert0(polcoef(fulldet, 7, w), "full E7");

full_E6 = polcoef(fulldet, 6, w);
E6_coefficients = List();
forstep (ip = 6, 0, -1,
  forstep (iq = 6-ip, 0, -1,
    ir = 6-ip-iq;
    listput(E6_coefficients, coefficient3(full_E6, ip, iq, ir));
  );
);
E6_coefficients = Vec(E6_coefficients);
E6_variables = [
  a2, a4, a5, b2, b4, b5, l8,
  u0, u1, u2, u3, v0, v1, v2, v3, t0, t1, t2
];
E6_matrix = matrix(
  #E6_coefficients,
  #E6_variables,
  row,
  col,
  deriv(E6_coefficients[row], E6_variables[col])
);
if (matrank(E6_matrix) != 7, error("generic E6 rank is not seven"));
rank_minor = matdet(
  vecextract(
    E6_matrix,
    [2, 4, 5, 7, 8, 11, 16],
    [1, 2, 3, 4, 6, 8, 9]
  )
);
rank_factor = m^2-4*m*n+n^2;
if (rank_minor == 0, error("rank-split minor vanished identically"));
assert0(deriv(rank_minor/rank_factor, m), "rank minor m quotient");
assert0(deriv(rank_minor/rank_factor, n), "rank minor n quotient");
if (
  matrank(subst(subst(E6_matrix, m, 0), n, 0)) != 5,
  error("zero-contact E6 rank is not five")
);

solve_vars = [a2, a4, a5, b2, b5, u0, u1];
solve_vals = [
  (
    -18*b4 + 30*l8 + 3*m*t1 + 2*m*t2 + 15*m*u2 + 63*m*u3
    - 12*m*v0 - 3*m*v1 - 3*m*v2 - 6*m*v3
    + 2*n*t0 + 3*n*t1 + 3*n*u2 + 9*n*u3
    - 15*n*v0 - 6*n*v1 - 6*n*v2 - 3*n*v3
  )/18,
  -(
    -18*b4 + 24*l8 + 4*m*t1 + 8*m*t2 + 9*m*u2 + 27*m*u3
    - 3*m*v2 - 9*m*v3 - 4*n*t1 - 24*n*t2
    - 9*n*u2 - 81*n*u3 + 3*n*v2 + 27*n*v3
  )/54,
  -(m^2+3*n^2)/36,
  (
    -18*b4 + 6*l8 + 24*m*t0 + 7*m*t1 + 2*m*t2
    - 324*m*v0 - 99*m*v1 - 30*m*v2 - 9*m*v3
    - 6*n*t0 - n*t1 + 81*n*v0 + 18*n*v1 + 3*n*v2
  )/54,
  -(3*m^2+n^2)/36,
  u2 + 4*u3 + 15*v0 + 4*v1 + v2,
  -4*u2 - 15*u3 - 4*v0 - v1 + v3
];

descended = subs_many(fulldet, solve_vars, solve_vals);
assert0(polcoef(descended, 6, w), "generic E6 solution");
E5 = polcoef(descended, 5, w);
fmn = 7*m^3-6*m^2*n+3*m*n^2-2*n^3;
gmn = 2*m^3-3*m^2*n+6*m*n^2-7*n^3;
assert0(coefficient3(E5, 2, 1, 2) + 4*fmn/9, "E5 first cubic");
assert0(coefficient3(E5, 1, 2, 2) - 4*gmn/9, "E5 second cubic");

root3 = Mod(root_symbol, root_symbol^2-3);
contact_ratio = 2 + root3;
if (
  matrank(subst(subst(E6_matrix, m, contact_ratio), n, 1)) != 6,
  error("conic-contact E6 rank is not six")
);
conic_vars = [m, n, a2, a4, a5, b2, b5, u0];
conic_vals = [
  contact_ratio,
  1,
  (
    -9*b4 + 15*l8 + t0 + (3*root3/2+9/2)*t1 + (root3+2)*t2
    + (-3*root3-3)*u1 + (9/2-9*root3/2)*u2
    + (45/2-27*root3/2)*u3 + (-63/2-18*root3)*v0
    + (-9-9*root3/2)*v1 + (-6-3*root3/2)*v2 - 9*v3/2
  )/9,
  (-2*root3/27-2/27) * (
    b4*(9/4-9*root3/4) + l8*(-3+3*root3) + t1
    + t2*(4-2*root3) + 9*u2/4 + (27/2-27*root3/4)*u3
    - 3*v2/4 + (-9/2+9*root3/4)*v3
  ),
  (-5-2*root3)/18,
  (4*root3/9+7/9) * (
    b4*(-21+12*root3) + l8*(7-4*root3) + t0
    + (7/6-root3/2)*t1 + (2/3-root3/3)*t2 - 27*v0/2
    + (-12+9*root3/2)*v1 + (-13/2+3*root3)*v2
    + (-3+3*root3/2)*v3
  ),
  (-11-6*root3)/18,
  (-2+root3) * (
    u1 + (2-root3)*u2 + (7-4*root3)*u3
    + (-26-15*root3)*v0 + (-7-4*root3)*v1
    + (-2-root3)*v2 - v3
  )
];
conic_descended = subs_many(fulldet, conic_vars, conic_vals);
assert0(polcoef(conic_descended, 6, w), "conic E6 solution");
conic_E5 = polcoef(conic_descended, 5, w);
conic_first = coefficient3(conic_E5, 2, 1, 2);
conic_second = coefficient3(conic_E5, 1, 2, 2);
assert0(
  conic_first - Mod(-64-112*root_symbol/3, root_symbol^2-3),
  "conic E5 first constant"
);
assert0(
  conic_second - Mod(16+32*root_symbol/3, root_symbol^2-3),
  "conic E5 second constant"
);
if (conic_first == 0 || conic_second == 0,
  error("conic E5 obstruction vanished")
);
print("D4_SF_11CC_PARI_CONIC_PASS");

zero_vars = [m, n, a2, a4, a5, b2, b5];
zero_vals = [
  0,
  0,
  -(3*b4-5*l8)/3,
  (3*b4-4*l8)/9,
  0,
  -(3*b4-l8)/9,
  0
];
zero_descended = subs_many(fulldet, zero_vars, zero_vals);
assert0(polcoef(zero_descended, 6, w), "zero-contact E6 solution");
E4zero = polcoef(zero_descended, 4, w);
assert0(
  coefficient3(E4zero, 3, 0, 1) - 8*(3*b4-l8)^2/27,
  "E4 first square"
);
assert0(
  coefficient3(E4zero, 0, 3, 1) - 8*(3*b4-4*l8)^2/27,
  "E4 second square"
);
print("D4_SF_11CC_PARI_ZERO_PASS");
print("D4_SF_11CC_PARI_LOWER_PASS");
print("D4_SF_11CC_PARI_STRICT_PASS");
};

main();
quit;

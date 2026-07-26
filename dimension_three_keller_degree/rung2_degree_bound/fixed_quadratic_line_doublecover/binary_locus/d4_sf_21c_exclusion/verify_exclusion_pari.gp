\\ Independent PARI/GP replay for the canonical D4-SF-21C exclusion.
\\ The determinant and every obstruction are reconstructed directly.

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

coefmod(poly, exponent, variable) =
  Mod(polcoef(lift(poly), exponent, variable), root_modulus);

coefficient3(poly, ip, iq, ir) =
  coefmod(coefmod(coefmod(poly, ip, p), iq, q), ir, r);

homogeneous_coefficients(poly, degree) =
{
  my(result = List());
  forstep (ip = degree, 0, -1,
    forstep (iq = degree-ip, 0, -1,
      ir = degree-ip-iq;
      listput(result, coefficient3(poly, ip, iq, ir));
    );
  );
  Vec(result);
};

linear_data(equations, variables) =
{
  my(
    matrix_part = matrix(
      #equations,
      #variables,
      row,
      col,
      deriv(equations[row], variables[col])
    ),
    zero_values = vector(#variables, index, 0),
    constant_part = vector(
      #equations,
      row,
      subs_many(equations[row], variables, zero_values)
    )~
  );
  for (row = 1, #equations,
    assert0(
      equations[row]
      - (
        sum(col = 1, #variables, matrix_part[row, col] * variables[col])
        + constant_part[row]
      ),
      Str("linearity row ", row)
    );
  );
  [matrix_part, -constant_part];
};

pivot_solution(matrix_part, rhs, variables, pivot_rows, pivot_columns, free_columns) =
{
  my(
    pivot_matrix = vecextract(matrix_part, pivot_rows, pivot_columns),
    free_matrix = vecextract(matrix_part, pivot_rows, free_columns),
    free_vector = vecextract(variables, free_columns)~,
    effective_rhs = vecextract(rhs, pivot_rows) - free_matrix * free_vector,
    values = matsolve(pivot_matrix, effective_rhs)
  );
  [vecextract(variables, pivot_columns), Vec(values), matdet(pivot_matrix)];
};

main() =
{
root_modulus = root_symbol^2 + 5;
root = Mod(root_symbol, root_modulus);
X = p - root*q;
Y = root*p - q;
h = X*Y;
P = h*p^2;
Q = h*q^2;
R = X^2*Y;
alpha = jac2(Q, R);
beta = -jac2(P, R);
gam = jac2(P, Q);

sx0u = 4*root*p/5 - q;
sx0v = q;
sx0t = 0;
sx1u = 4*p/3 + 4*root*q/15;
sx1v = 0;
sx1t = 1;
assert0(alpha*sx0u + beta*sx0v + gam*sx0t, "degree-one syzygy zero");
assert0(alpha*sx1u + beta*sx1v + gam*sx1t, "degree-one syzygy one");

sy0u = p*sx0u; sy0v = p*q; sy0t = 0;
sy1u = q*sx0u; sy1v = q^2; sy1t = 0;
sy2u = p*sx1u; sy2v = 0; sy2t = p;
sy3u = q*sx1u; sy3v = 0; sy3t = q;
assert0(alpha*sy0u + beta*sy0v + gam*sy0t, "degree-two syzygy zero");
assert0(alpha*sy1u + beta*sy1v + gam*sy1t, "degree-two syzygy one");
assert0(alpha*sy2u + beta*sy2v + gam*sy2t, "degree-two syzygy two");
assert0(alpha*sy3u + beta*sy3v + gam*sy3t, "degree-two syzygy three");

U2 = x0*sx0u + x1*sx1u;
V2 = x0*sx0v + x1*sx1v;
T2 = x0*sx0t + x1*sx1t;
U1 = y0*sy0u + y1*sy1u + y2*sy2u + y3*sy3u;
V1 = y0*sy0v + y1*sy1v + y2*sy2v + y3*sy3v;
T1 = y0*sy0t + y1*sy1t + y2*sy2t + y3*sy3t;

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

H2 = [A, B, T0 + r*T1 + r^2*T2/2]~;
H3 = [U0 + r*U1 + r^2*U2/2, V0 + r*V1 + r^2*V2/2, R]~;
H4 = [P, Q, 0]~;
general_det = matdet(
  linear + w*jac3(H2) + w^2*jac3(H3) + w^3*jac3(H4)
);
print("D4_SF_21C_PARI_DETERMINANT_BUILT");
assert0(coefmod(general_det, 9, w), "general E9");
assert0(coefmod(general_det, 8, w), "general E8");
assert0(coefmod(general_det, 7, w), "general E7");

general_E6 = coefmod(general_det, 6, w);
assert0(
  coefficient3(general_E6, 3, 0, 3) - 6*x0^2,
  "first x square"
);
assert0(
  subst(coefficient3(general_E6, 2, 1, 3), x0, 0)
  - 4*root*x1^2/3,
  "second x square after x0"
);

lower_variables = [
  a2, a4, a5, b2, b4, b5, l8,
  u0, u1, u2, u3, v0, v1, v2, v3, t0, t1, t2
];
all_E6 = homogeneous_coefficients(
  subs_many(general_E6, [x0, x1], [0, 0]),
  6
);
nonzero_rows = [1, 2, 3, 4, 5, 7, 8, 11, 12, 16, 17, 22, 23];
reduced_E6 = vecextract(all_E6, nonzero_rows);
contact_linear = linear_data(reduced_E6, lower_variables);
contact_matrix = contact_linear[1];
contact_rhs = contact_linear[2];
if (
  matrank(subs_many(contact_matrix, [y0, y1, y2, y3], [1, 2, 3, 4])) != 9,
  error("sample contact matrix rank is not nine")
);

left0 = [0, 0, -66, 0, 9*root, 0, 5, 0, 0, 0, 0, 0, 0];
left1 = [0, 0, 32*root, 0, 15, 0, 0, 0, 5, 0, 0, 0, 0];
left2 = [0, 0, -9, 0, root, 0, 0, 0, 0, 0, 1, 0, 0];
left3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1];
left_vectors = Mat([left0~, left1~, left2~, left3~])~;
if (matrank(left_vectors) != 4, error("contact left vectors are dependent"));
assert0(left_vectors*contact_matrix, "contact left kernel");
compatibility = left_vectors*contact_rhs;

C0 = root*y0*y2 + y0*y3 - 3*y1^2/8 + y1*y2
     + y2^2/6 - root*y2*y3/6;
C1 = y0*y2 - root*y0*y3/5 + 27*root*y1^2/160
     - root*y1*y2/5 + y1*y3/4 - 23*root*y2^2/240
     - 7*y2*y3/24 - root*y3^2/48;
C2 = root*y0*y2 + y0*y3 + 9*y1^2/8 + y1*y2
     - 4*root*y1*y3/5 + 5*y2^2/12 - 4*root*y2*y3/15
     - 7*y3^2/12;
C3 = root*y1^2 + 8*y1*y3/3 - 16*root*y3^2/45;
assert0(compatibility[1] - 160*C0, "compatibility zero");
assert0(compatibility[2] - 640*C1, "compatibility one");
assert0(compatibility[3] - 32*C2, "compatibility two");
assert0(compatibility[4] - 12*C3, "compatibility three");

forced_y1 = 4*root*y3/15;
forced_y2 = root*y3/5;
assert0(C3 - root*(y1-forced_y1)^2, "force y1 square");
assert0(
  subst(C0-C2, y1, forced_y1) + (y2-forced_y2)^2/4,
  "force y2 square"
);
assert0(
  subs_many(compatibility, [y1, y2], [forced_y1, forced_y2]),
  "contact plane compatibility"
);
print("D4_SF_21C_PARI_CONTACT_PASS");

contact_values = [0, 0, m, 4*root*n/15, root*n/5, n];
contact_det = subs_many(
  general_det,
  [x0, x1, y0, y1, y2, y3],
  contact_values
);
contact_E6_coefficients = homogeneous_coefficients(coefmod(contact_det, 6, w), 6);
generic_linear = linear_data(contact_E6_coefficients, lower_variables);
generic_matrix = generic_linear[1];
generic_rhs = generic_linear[2];
generic_rows = [1, 2, 3, 4, 5, 7, 11];
generic_columns = [1, 2, 3, 4, 6, 8, 9];
generic_free = [5, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18];
generic_solution = pivot_solution(
  generic_matrix,
  generic_rhs,
  lower_variables,
  generic_rows,
  generic_columns,
  generic_free
);
rank_factor = (m-n/3)*(m+n/6);
if (generic_solution[3] == 0, error("generic rank minor vanished"));
assert0(deriv(generic_solution[3]/rank_factor, m), "generic minor m quotient");
assert0(deriv(generic_solution[3]/rank_factor, n), "generic minor n quotient");

generic_descended = subs_many(
  contact_det,
  generic_solution[1],
  generic_solution[2]
);
assert0(coefmod(generic_descended, 6, w), "generic E6 solution");
generic_E5 = coefmod(generic_descended, 5, w);
fmn = 135*m^3 + 135*m^2*n - 9*m*n^2 + n^3;
gmn = 135*m^3 + 18*m*n^2 - 2*n^3;
assert0(
  coefficient3(generic_E5, 2, 1, 2) - 8*root*fmn/225,
  "generic E5 first cubic"
);
assert0(
  coefficient3(generic_E5, 1, 2, 2) + 4*gmn/45,
  "generic E5 second cubic"
);
assert0(polresultant(fmn, gmn, m) + 1793613375*n^9, "resultant in m");
assert0(polresultant(fmn, gmn, n) - 1793613375*m^9, "resultant in n");
print("D4_SF_21C_PARI_GENERIC_PASS");

boundary_rows = [1, 2, 3, 4, 5, 7];
boundary_columns = [1, 2, 3, 4, 6, 8];
boundary_free = [5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18];
boundary_m = [1, -1];
boundary_n = [3, 6];
for (branch = 1, 2,
  specialized_det = subs_many(
    contact_det,
    [m, n],
    [boundary_m[branch], boundary_n[branch]]
  );
  specialized_E6 = homogeneous_coefficients(coefmod(specialized_det, 6, w), 6);
  specialized_linear = linear_data(specialized_E6, lower_variables);
  specialized_solution = pivot_solution(
    specialized_linear[1],
    specialized_linear[2],
    lower_variables,
    boundary_rows,
    boundary_columns,
    boundary_free
  );
  specialized_descended = subs_many(
    specialized_det,
    specialized_solution[1],
    specialized_solution[2]
  );
  assert0(coefmod(specialized_descended, 6, w), Str("boundary E6 ", branch));
  assert0(
    coefficient3(coefmod(specialized_descended, 5, w), 3, 0, 2)
    + 108/5,
    Str("boundary E5 ", branch)
  );
);
print("D4_SF_21C_PARI_BOUNDARY_PASS");

zero_det = subs_many(contact_det, [m, n], [0, 0]);
zero_E6 = homogeneous_coefficients(coefmod(zero_det, 6, w), 6);
zero_linear = linear_data(zero_E6, lower_variables);
zero_rows = [1, 2, 3, 4, 5];
zero_columns = [1, 2, 3, 4, 6];
zero_free = [5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18];
zero_solution = pivot_solution(
  zero_linear[1],
  zero_linear[2],
  lower_variables,
  zero_rows,
  zero_columns,
  zero_free
);
zero_descended = subs_many(zero_det, zero_solution[1], zero_solution[2]);
assert0(coefmod(zero_descended, 6, w), "zero E6 solution");
zero_E4 = coefmod(zero_descended, 4, w);
assert0(coefficient3(zero_E4, 3, 0, 1) - 12*b4^2, "zero E4 first square");
assert0(
  subst(coefficient3(zero_E4, 2, 1, 1), b4, 0)
  - 8*root*l8^2/3,
  "zero E4 second square"
);
forced_zero_values = subs_many(zero_solution[2], [b4, l8], [0, 0]);
for (index = 1, 4,
  assert0(forced_zero_values[index], Str("forced zero pivot ", index));
);
assert0(forced_zero_values[5], "forced zero b5");
print("D4_SF_21C_PARI_ZERO_PASS");
print("D4_SF_21C_PARI_STRICT_PASS");
};

main();
quit;

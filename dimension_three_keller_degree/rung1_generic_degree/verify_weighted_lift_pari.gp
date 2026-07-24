\\ Exact PARI/GP regression checks for the weighted-lift family.
\\ This is not a proof for all d.  See VERIFICATION.md.

collision_point(d, r) =
{
  my(s = (4 - 2^d)/(d - 2));
  my(p = (2*r - d*r^(d - 1))/(d - 2));
  my(g = s - p);
  my(xx = 1/g);
  my(u = r/g);
  my(yy = (u - 1)/xx);
  my(zz = (g - 1 + d/(d - 1)*(u - 1))/xx^2);
  [xx, yy, zz, s];
};

F_value(d, xx, yy, zz) =
{
  my(u = 1 + xx*yy);
  my(g = 1 - d/(d - 1)*xx*yy + xx^2*zz);
  my(A = ((d - 2)*u + u^2 - (d - 1)*u^d*g^(d - 2))
         / ((d - 2)*xx^2));
  my(B = ((d - 2) + 2*u - d*u^(d - 1)*g^(d - 2))
         / ((d - 2)*xx));
  [A, B, xx*g];
};

\\ Independently selected exact evaluation points.  The determinant is
\\ differentiated symbolically in PARI, then evaluated exactly.
check_degree(d) =
{
  my(u = 1 + x*y);
  my(g = 1 - d/(d - 1)*x*y + x^2*z);
  my(A = simplify(((d - 2)*u + u^2 - (d - 1)*u^d*g^(d - 2))/((d - 2)*x^2)));
  my(B = simplify(((d - 2) + 2*u - d*u^(d - 1)*g^(d - 2))/((d - 2)*x)));
  my(C = x*g);
  my(VF = [A, B, C]);
  my(VX = [x, y, z]);
  my(J = matdet(matrix(3, 3, i, j, deriv(VF[i], VX[j]))));
  forstep(k = -2, 2, 1, my(pt = [k + 3, 2*k - 1, k^2 + 1]); if(subst(subst(subst(J, x, pt[1]), y, pt[2]), z, pt[3]) != 1, error("Jacobian failure at d=", d, ", point=", pt)));
  my(P1 = collision_point(d, 1));
  my(P2 = collision_point(d, 2));
  my(T = [P1[4], P1[4], 1]);
  if(F_value(d, P1[1], P1[2], P1[3]) != T, error("first collision failure at d=", d));
  if(F_value(d, P2[1], P2[2], P2[3]) != T, error("second collision failure at d=", d));
  if(P1[1] == P2[1] && P1[2] == P2[2] && P1[3] == P2[3], error("collision points equal at d=", d));
};

for(d = 3, 8, check_degree(d));

print("PASS: exact PARI/GP evaluation and collision checks for d=3,...,8");

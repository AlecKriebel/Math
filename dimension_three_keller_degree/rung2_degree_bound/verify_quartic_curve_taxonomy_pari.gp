\\ Focused exact PARI/GP regressions for WORKING_QUARTIC_CURVE_TAXONOMY.md.

assertzero(x, label) =
{
  if (x != 0, error(Str("FAIL: ", label, ": ", x)));
};

asserttrue(x, label) =
{
  if (!x, error(Str("FAIL: ", label)));
};

cross3(u, v) =
{
  return([u[2]*v[3]-u[3]*v[2],
          u[3]*v[1]-u[1]*v[3],
          u[1]*v[2]-u[2]*v[1]]~);
};

mattrace(m) =
{
  return(sum(i=1,matsize(m)[1],m[i,i]));
};

main() =
{
  my(A, Ap, Aq, Delta, common, C, kernel, expectedAdj);
  my(Hgeneric, Bgeneric, Tgeneric, formalDet);
  my(ell, mform, Htangent, Btangent, Ttangent, V);
  my(degreeSevenAtZero, normalMinor, vars);

  A = [p^2*q,p*q^2,p^3+q^3]~;
  Ap = vector(3,i,deriv(A[i],p))~;
  Aq = vector(3,i,deriv(A[i],q))~;
  Delta = cross3(Ap,Aq);

  assertzero(Delta[1]-(3*q^4-6*p^3*q),
             "nodal normal, first component");
  assertzero(Delta[2]-(3*p^4-6*p*q^3),
             "nodal normal, second component");
  assertzero(Delta[3]-3*p^2*q^2,
             "nodal normal, third component");
  common = gcd(gcd(Delta[1],Delta[2]),Delta[3]);
  asserttrue(poldegree(common,p)==0 && poldegree(common,q)==0,
             "nodal normal has constant gcd");

  C = matrix(3,3,i,j,
    if (j==1,r*Ap[i],if (j==2,r*Aq[i],A[i])));
  kernel = [-p,-q,3*r]~;
  expectedAdj = r/3*kernel*Delta~;
  assertzero(C*kernel, "weighted Euler right kernel");
  assertzero(matadjoint(C)-expectedAdj, "rank-one adjugate formula");

  vars = [p,q,r];
  Hgeneric =
  [p^3+q*r^2,
   q^3+p*r^2,
   r^3+p*q*r]~;
  Bgeneric = matrix(3,3,i,j,deriv(Hgeneric[i],vars[j]));
  Tgeneric = vector(3,i,
    -p*deriv(Hgeneric[i],p)
    -q*deriv(Hgeneric[i],q)
    +3*r*deriv(Hgeneric[i],r))~;
  assertzero(mattrace(matadjoint(C)*Bgeneric)
             -r/3*Delta~*Tgeneric,
             "degree-eight weighted normal formula");

  formalDet = matdet(matid(3)+s^2*Bgeneric+s^3*C);
  assertzero(polcoef(formalDet,8,s)-r/3*Delta~*Tgeneric,
             "degree-eight determinant coefficient");

  ell = la*p+lb*q;
  mform = ma*p+mb*q;
  Htangent =
    Ap*(ell+alpha*r)
    +Aq*(mform+beta*r);
  Btangent = matrix(3,3,i,j,deriv(Htangent[i],vars[j]));
  Ttangent = vector(3,i,
    -p*deriv(Htangent[i],p)
    -q*deriv(Htangent[i],q)
    +3*r*deriv(Htangent[i],r))~;
  assertzero(Delta~*Ttangent,
             "full tangent cubic satisfies degree eight");

  V = Ap*ell+Aq*mform;
  degreeSevenAtZero =
    subst(mattrace(matadjoint(Btangent)*C),r,0);
  normalMinor = matdet(matrix(3,3,i,j,
    if (j==1,deriv(V[i],p),
      if (j==2,deriv(V[i],q),A[i]))));
  assertzero(degreeSevenAtZero-normalMinor,
             "degree-seven specialization is the normal minor");

  print("PASS: PARI quartic curve-taxonomy regressions");
};

main();
quit;

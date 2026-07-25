\\ Independent exact geometric branch check for
\\     g_d(X) = X^d - X^2 + X
\\ at U=1.  The finite branch polynomial is
\\     Res_X(g_d(X)+V, g_d'(X)).
\\ Degree d-1 and squarefreeness say that all d-1 finite critical values
\\ are present and distinct.  In characteristic zero, the classical Morse
\\ theorem then gives geometric monodromy S_d.

x = 'x;
v = 'v;

check_degree(d) =
{
  my(f = x^d - x^2 + x + v, fp, branch, branch_gcd, branch_degree);
  fp = deriv(f, x);
  branch = polresultant(f, fp, x);
  branch_degree = poldegree(branch, v);

  if(branch_degree != d - 1,
    error(Str("wrong branch degree for d=", d,
              ": got ", branch_degree, ", expected ", d - 1)));

  branch_gcd = gcd(branch, deriv(branch, v));
  if(poldegree(branch_gcd, v) != 0,
    error(Str("branch polynomial is not squarefree for d=", d,
              ": gcd=", branch_gcd)));

  print("PASS d=", d, ": branch degree ", branch_degree, ", squarefree");
};

for(d = 3, 20, check_degree(d));

print("PASS: exact geometric branch checks for d=3,...,20");
quit

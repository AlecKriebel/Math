\\ Exact PARI/GP replay for the LP(333) sparse-B relative-norm screen.
\\
\\ PARI/GP 2.17.4 was used for the pinned run.  The extension L/M is
\\ M(t)/(t^2+t+1), hence cyclic quadratic.  For the four rows without an
\\ inert-prime obstruction, rnfisnorm is therefore a guaranteed norm test.

allocatemem(1500000000);

{
pm = polsubcyclo(111, 12, y)[1];
expected_pm =
  y^12 - y^11 - 35*y^10 - 17*y^9 + 394*y^8 + 574*y^7
  - 1395*y^6 - 3344*y^5 + 131*y^4 + 5219*y^3
  + 4501*y^2 + 1298*y + 121;
if (pm != expected_pm || polsturm(pm) != 12,
  error("the totally real degree-12 field changed"));

pk = polcyclo(111, x);
embedding = nfisincl(pm, pk, 1);
K = Mod(x, pk);
th = Mod(embedding, pk);
ww = K^37;
H = [1, 10, 26];

etas = vector(12, rr,
  sum(jj = 1, 3,
    K^(3 * lift(Mod(2^(rr-1) * H[jj], 37)))));

\\ Express fixed-field elements from Q(zeta_111) in the power basis of pm.
power_matrix = matrix(72, 12, rr, cc,
  polcoeff(lift(th^(cc-1)), rr-1));
nf = nfinit(pm);
primes11 = idealprimedec(nf, 11);
primes101 = idealprimedec(nf, 101);
if (#primes11 != 12 || #primes101 != 12,
  error("11 or 101 no longer splits completely in M"));
if (sum(index = 1, 12,
       primes11[index].f != 1 || primes11[index].e != 1)
    || sum(index = 1, 12,
       primes101[index].f != 1 || primes101[index].e != 1),
  error("a local prime lost residue degree one"));

tt = varhigher("tt", y);
norm_data = rnfisnorminit(pm, tt^2 + tt + 1, 1);

\\ [separation, z_real, z_omega, expected status]
\\ status 11: odd valuation above 11
\\ status 101: odd valuation above 101
\\ status 1: exact relative field norm (rnfisnorm quotient q=1)
cases = [1,-2,-1,11; 1,-1,-2,1; 1,1,-1,11;
         2,-2,-1,11; 2,-1,-2,11; 2,1,-1,11;
         3,-2,-1,1; 3,-1,-2,11; 3,1,-1,11;
         4,-2,-1,101; 4,-1,-2,11; 4,1,-1,11;
         5,-2,-1,11; 5,-1,-2,11; 5,1,-1,11;
         6,-2,-1,1; 6,-1,-2,1];

obstructed_types = 0;
norm_types = 0;
obstructed_raw = 0;
norm_raw = 0;

for (case_index = 1, matsize(cases)[1],
  separation = cases[case_index, 1];
  z = cases[case_index, 2] + cases[case_index, 3] * ww;
  B = 2 + z * (etas[1] - etas[separation + 1]);
  Bstar = subst(lift(B), x, K^(-1));
  gam = 167 - B * Bstar;
  gamma_vector = Col(vector(72, coordinate,
    polcoeff(lift(gam), coordinate-1)));
  coordinates = matinverseimage(power_matrix, gamma_vector);
  if (#coordinates != 12,
    error("gamma did not map into the real fixed field"));
  gamma_M = sum(coordinate = 1, 12,
    coordinates[coordinate] * y^(coordinate-1));

  values11 = vector(12, prime_index,
    idealval(nf, gamma_M, primes11[prime_index]));
  values101 = vector(12, prime_index,
    idealval(nf, gamma_M, primes101[prime_index]));
  odd11 = sum(prime_index = 1, 12, values11[prime_index] % 2);
  odd101 = sum(prime_index = 1, 12, values101[prime_index] % 2);

  is_norm = 0;
  if (cases[case_index, 4] == 11,
    if (!odd11, error("the expected p=11 obstruction vanished"));
    obstructed_types++;
    obstructed_raw += 24,
    if (cases[case_index, 4] == 101,
      if (!odd101, error("the expected p=101 obstruction vanished"));
      obstructed_types++;
      obstructed_raw += 24,
      norm_answer = rnfisnorm(norm_data, gamma_M);
      is_norm = (norm_answer[2] == 1);
      if (!is_norm, error("an expected relative norm ceased to be a norm"));
      norm_types++;
      orbit_size = if(separation == 6
                        && cases[case_index, 2] == -1
                        && cases[case_index, 3] == -2, 12, 24);
      norm_raw += orbit_size
    )
  );

  print("row d=", separation,
        " z=(", cases[case_index, 2], ",",
                  cases[case_index, 3], ")",
        " odd11=", odd11,
        " odd101=", odd101,
        " relative_norm=", is_norm)
);

if (obstructed_types != 13 || norm_types != 4,
  error("the 13/4 field-type split changed"));
if (obstructed_raw != 312 || norm_raw != 84,
  error("the 312/84 raw split changed"));

print("locally_obstructed_types=", obstructed_types);
print("relative_norm_types=", norm_types);
print("obstructed_raw_words=", obstructed_raw);
print("relative_norm_raw_words=", norm_raw);
print("sector_closed=false");
}

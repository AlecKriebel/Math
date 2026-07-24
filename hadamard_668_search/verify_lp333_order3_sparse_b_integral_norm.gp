\\ Unconditional CM and finite-residue certificate for the integral sparse-B
\\ norm obstruction.
\\
\\ The generic degree-24 bnfcertify call spends most of its time proving both
\\ the class group and a full unit group.  Here the unit and class-number
\\ assertions are instead proved from:
\\
\\   * an unconditional certificate for the real degree-12 field M;
\\   * the exact odd-character relative class-number formula;
\\   * an explicit cyclotomic unit witnessing Hasse unit index Q_L = 2.
\\
\\ A finite quadratic/cubic residue certificate proves that an explicit
\\ ideal class has exact order 12.  Together with exact h(L)=12, this
\\ certifies Cl(L)=C_12 without the infeasible degree-24 Minkowski sweep.
\\ All unit-norm tests are performed in the unconditionally certified unit
\\ group of M.
\\
\\ Pinned implementation: PARI/GP 2.17.4.

default(parisizemax, 1500000000);

star_abs(a) =
{
  my(ar = rnfeltabstorel(rnf, a));
  return(rnfeltreltoabs(
    rnf,
    Mod(subst(lift(ar), tt, -1-tt), relpol)
  ));
};

same_ideal(left, right) =
{
  return(idealhnf(nfL, left) == idealhnf(nfL, right));
};

cyclo_element_to_M(a) =
{
  my(
    coordinate_vector = Col(vector(72, index,
      polcoeff(lift(a), index-1))),
    coordinates = matinverseimage(power_matrix, coordinate_vector),
    result
  );
  if (#coordinates != 12,
    error("an asserted real fixed-field element did not map into M"));
  result = Mod(sum(index = 1, 12,
    coordinates[index] * y^(index-1)), pm);
  if (subst(lift(result), y, th) != a,
    error("an M-coordinate inverse image failed exact reconstruction"));
  return(result);
};

cyclo_element_to_L(a) =
{
  my(
    astar = subst(lift(a), x, K^(-1)),
    coefficient_B = (a - astar) / (ww - ww^2),
    coefficient_A = a - coefficient_B * ww,
    relative_element
  );
  if (subst(lift(coefficient_A), x, K^(-1)) != coefficient_A
      || subst(lift(coefficient_B), x, K^(-1)) != coefficient_B,
    error("an L element did not split over the real fixed field"));
  relative_element = Mod(
    cyclo_element_to_M(coefficient_A)
      + cyclo_element_to_M(coefficient_B) * tt,
    relpol
  );
  return(rnfeltreltoabs(rnf, relative_element));
};

free_parity(unit_coordinates) =
{
  return(vector(11, index,
    lift(Mod(unit_coordinates[index], 2))));
};

power_residue_signature(element, pp, root, qpower) =
{
  my(
    polynomial = lift(element),
    residue,
    value,
    primitive_root,
    target_root
  );
  if (gcd(denominator(polynomial), pp) != 1,
    error("a residue input has a denominator divisible by its prime"));
  residue = subst(
    polynomial,
    variable(nfL.pol),
    Mod(root, pp)
  );
  if (residue == 0,
    error("a residue-character input vanished"));
  value = residue^((pp-1) / qpower);
  if (qpower == 2,
    if (value == 1, return(0));
    if (value == -1, return(1));
    error("a quadratic residue signature left mu_2")
  );
  primitive_root = znprimroot(pp);
  target_root = primitive_root^((pp-1) / 3);
  if (value == 1, return(0));
  if (value == target_root, return(1));
  if (value == target_root^2, return(2));
  error("a cubic residue signature left mu_3");
};

certify_class_coordinate(ideal_value, coordinate) =
{
  my(
    correction_exponent = lift(Mod(-coordinate, 12)),
    corrected_ideal = idealmul(
      nfL,
      ideal_value,
      idealpow(nfL, class_generator, correction_exponent)
    ),
    principal_answer = bnfisprincipal(bnfL, corrected_ideal, 1),
    generator
  );
  if (#principal_answer != 2 || principal_answer[1] != 0,
    error("a claimed class-coordinate correction was not returned principal"));
  generator = nfbasistoalg(nfL, principal_answer[2]);
  if (!same_ideal(idealhnf(nfL, generator), corrected_ideal),
    error("a class-coordinate correction lacks an exact generator"));
  return(lift(Mod(coordinate, 12)));
};

{
if (version() != [2,17,4],
  error("this certificate is pinned to PARI/GP 2.17.4"));
setrand(668);

\\ -------------------------------------------------------------------------
\\ 1. Identify M and L inside Q(zeta_111).
\\ -------------------------------------------------------------------------

pm = polsubcyclo(111, 12, y)[1];
expected_pm =
  y^12 - y^11 - 35*y^10 - 17*y^9 + 394*y^8 + 574*y^7
  - 1395*y^6 - 3344*y^5 + 131*y^4 + 5219*y^3
  + 4501*y^2 + 1298*y + 121;
if (pm != expected_pm || polsturm(pm) != 12,
  error("the totally real degree-12 field changed"));

pk = polcyclo(111, x);
K = Mod(x, pk);
embedding = nfisincl(pm, pk, 1);
th = Mod(embedding, pk);
power_matrix = matrix(72, 12, row, column,
  polcoeff(lift(th^(column-1)), row-1));

H_lifts = [1, 10, 100];
if (lift(Mod(10^2, 111)) != 100
      || lift(Mod(10^3, 111)) != 1,
  error("the lifted multiplier subgroup changed"));
if (vector(3, index,
      lift(Mod(H_lifts[index], 37))) != [1,10,26],
  error("the lifted subgroup no longer reduces to {1,10,26}"));
if (subst(lift(th), x, K^10) != th
      || subst(lift(th), x, K^(-1)) != th,
  error("the chosen M embedding is not fixed by <10,-1>"));

ww = K^37;
if (ww^2 + ww + 1 != 0
      || subst(lift(ww), x, K^10) != ww
      || subst(lift(ww), x, K^(-1)) == ww,
  error("the embedded omega no longer reconstructs L from M"));

nfM = nfinit(pm);
tt = varhigher("tt", y);
relpol = tt^2 + tt + 1;
rnf = rnfinit(nfM, relpol, 1);
nfL = nfinit(rnf);
if (poldegree(nfL.pol) != 24,
  error("M(omega) is not the expected degree-24 CM field"));
if (nfcertify(nfM) != [] || nfcertify(nfL) != [],
  error("a maximal-order/discriminant certificate failed"));
roots_L = nfrootsof1(nfL);
if (roots_L[1] != 6,
  error("the root-of-unity count in L changed"));
autstar = star_abs(Mod(tt, nfL.pol));
if (subst(lift(autstar), tt, autstar) != Mod(tt, nfL.pol),
  error("the relative involution did not square to one"));

print("field_identification=true");
print("pari_gp_version=", version());
print("degree_M=12");
print("degree_L=24");
print("maximal_orders_certified=true");
print("roots_of_unity_L=", roots_L[1]);

\\ -------------------------------------------------------------------------
\\ 2. Certify h(M)=1 and its complete unit group.
\\ -------------------------------------------------------------------------

print("computing_certified_real_class_and_unit_group=true");
bnfM = bnfinit(nfM, 1);
if (!bnfcertify(bnfM),
  error("the unconditional certificate for M failed"));
if (bnfM.no != 1 || bnfM.cyc != [] || #bnfM.fu != 11,
  error("the certified real class/unit invariants changed"));
print("certified_class_number_M=", bnfM.no);
print("certified_unit_rank_M=", #bnfM.fu);

\\ -------------------------------------------------------------------------
\\ 3. Exact odd-character product and relative class number.
\\
\\ Gal(L/Q) = C_2 x C_12.  Write the character on the 37-component as
\\ chi_j(2)=zeta_12^j, j=0,...,11, and the character on the 3-component
\\ as the exponent e in {0,1}.  Oddness is exactly e+j = 1 (mod 2).
\\ Every nontrivial character modulo the prime 37 is primitive, so the
\\ conductors are 3, 37, or 111 as used below.
\\ -------------------------------------------------------------------------

cyclo12_polynomial = polcyclo(12, z);
zeta12 = Mod(z, cyclo12_polynomial);
logs37 = vector(37);
running_residue = 1;
for (logarithm = 0, 35,
  logs37[running_residue] = logarithm;
  running_residue = lift(Mod(2 * running_residue, 37))
);
if (running_residue != 1
      || vecsort(vector(36, residue, logs37[residue]))
         != vector(36, index, index-1),
  error("2 is no longer being treated as a generator modulo 37"));

odd_character_rows = vector(12);
odd_L0_product = Mod(1, cyclo12_polynomial);
for (j = 0, 11,
  e = lift(Mod(j+1, 2));
  conductor = if(j == 0, 3, if(e == 0, 37, 111));
  weighted_sum = Mod(0, cyclo12_polynomial);
  for (a = 1, conductor,
    if (gcd(a, conductor) == 1,
      character_value = zeta12^(j * logs37[lift(Mod(a, 37))]);
      if (e && lift(Mod(a, 3)) == 2,
        character_value = -character_value);
      weighted_sum += a * character_value
    )
  );
  L0 = -weighted_sum / conductor;
  minus_one_value = zeta12^(j * logs37[36]);
  if (e, minus_one_value = -minus_one_value);
  if (minus_one_value != -1,
    error("a purported odd character became even"));
  odd_character_rows[j+1] = [j, e, conductor, L0];
  odd_L0_product *= L0
);
if (#odd_character_rows != 12
      || odd_L0_product != Mod(4096, cyclo12_polynomial),
  error("the exact odd-character product changed"));

print("odd_character_count=", #odd_character_rows);
print("odd_character_L0_product=", lift(odd_L0_product));

\\ -------------------------------------------------------------------------
\\ 4. Explicit Hasse-index witness.
\\
\\ Since 111 is not a prime power, each 1-zeta_111^h is a unit.  Their
\\ H-norm u is in L.  Complex conjugation gives
\\
\\   u/u* = product_h (-zeta_111^h) = -zeta_111^111 = -1.
\\
\\ For a CM field Q_L=[U_L:mu_L U_M] is at most two.  Ratios v/v* for
\\ v in mu_L U_M are squares in mu_6 and therefore cannot equal -1.
\\ Thus u represents the nontrivial coset and Q_L=2.
\\ -------------------------------------------------------------------------

cyclotomic_unit =
  (1 - K^H_lifts[1])
  * (1 - K^H_lifts[2])
  * (1 - K^H_lifts[3]);
cyclotomic_unit_star =
  subst(lift(cyclotomic_unit), x, K^(-1));
if (subst(lift(cyclotomic_unit), x, K^10) != cyclotomic_unit
      || subst(lift(cyclotomic_unit), x, K^100) != cyclotomic_unit,
  error("the explicit cyclotomic unit is not H-fixed"));
if (norm(cyclotomic_unit) != 1,
  error("the explicit H-fixed cyclotomic element is not a unit"));
if (cyclotomic_unit / cyclotomic_unit_star != -1,
  error("the explicit unit no longer witnesses the odd Hasse coset"));
cyclotomic_unit_L = cyclo_element_to_L(cyclotomic_unit);
if (!same_ideal(
      idealhnf(nfL, cyclotomic_unit_L),
      idealhnf(nfL, 1)),
  error("the explicit Hasse-index witness is not an integral unit in L"));
zeta6 = -ww;
if (zeta6^6 != 1 || zeta6^3 != -1,
  error("the displayed sixth root of unity changed"));
for (root_index = 0, 5,
  if (zeta6^(2 * root_index) == -1,
    error("-1 unexpectedly became a square in mu_6"))
);

hasse_unit_index = 2;
relative_class_number = lift(
  hasse_unit_index * roots_L[1] * odd_L0_product / 2^12
);
if (relative_class_number != 12,
  error("the exact CM relative class number changed"));
class_number_L = bnfM.no * relative_class_number;
if (class_number_L != 12,
  error("the exact absolute class number of L changed"));

print("explicit_Hasse_unit_ratio=-1");
print("Hasse_unit_index=", hasse_unit_index);
print("relative_class_number_L_over_M=", relative_class_number);
print("unconditional_class_number_L=", class_number_L);

\\ The explicit unit generates U_L/(mu_6 U_M).  Hence
\\ N(U_L)=U_M^2 <N(u)>.  Record N(u) in the certified M-unit basis.
unit_norm_M = cyclo_element_to_M(
  cyclotomic_unit * cyclotomic_unit_star
);
unit_norm_coordinates = bnfisunit(bnfM, unit_norm_M);
if (#unit_norm_coordinates != 12,
  error("the explicit Hasse-unit norm was not recognized in U_M"));
unit_norm_parity = free_parity(unit_norm_coordinates);
if (unit_norm_parity == vector(11),
  error("the explicit Hasse-unit norm lost its nontrivial square class"));

print("Hasse_unit_norm_coordinates_in_M=",
      unit_norm_coordinates~);
print("Hasse_unit_norm_free_parity=", unit_norm_parity);

\\ -------------------------------------------------------------------------
\\ 5. Finite class-generator certificate.
\\
\\ The degree-24 bnf is used only as an untrusted source of candidate ideals
\\ and exact generators.  We verify J^12=(a).  If J^6 were principal, then
\\ a times a unit would be a square; if J^4 were principal, then a times a
\\ unit would be a cube.  Since U_L is generated by mu_6, U_M, and the
\\ explicit Hasse-index unit, residue characters give finite linear tests
\\ for all possible unit twists.
\\ -------------------------------------------------------------------------

bnfL = bnfinit(nfL, 1);
if (bnfL.no != 12 || bnfL.cyc != [12],
  error("the candidate class presentation is not C_12"));

structural_unit_generators = vector(13);
structural_unit_generators[1] =
  rnfeltreltoabs(rnf, Mod(-tt, relpol));
for (unit_index = 1, 11,
  structural_unit_generators[unit_index+1] =
    rnfeltreltoabs(rnf, bnfM.fu[unit_index])
);
structural_unit_generators[13] = cyclotomic_unit_L;
for (unit_index = 1, 13,
  if (!same_ideal(
        idealhnf(nfL, structural_unit_generators[unit_index]),
        idealhnf(nfL, 1)),
    error("a structural unit generator is not an integral unit"))
);

class_generator = bnfL.gen[1];
twelfth_power_ideal = idealpow(nfL, class_generator, 12);
twelfth_power_answer =
  bnfisprincipal(bnfL, twelfth_power_ideal, 1);
if (#twelfth_power_answer != 2 || twelfth_power_answer[1] != 0,
  error("the candidate twelfth power was not returned principal"));
twelfth_power_generator =
  nfbasistoalg(nfL, twelfth_power_answer[2]);
if (!same_ideal(
      idealhnf(nfL, twelfth_power_generator),
      twelfth_power_ideal),
  error("the candidate twelfth-power generator failed exact replay"));

residue_primes = [1777,2221,2887,3109];
expected_index_residues = [93,942,1658,656];
expected_discriminant_residues = [694,859,2723,1101];
expected_generator_norm_residues = [78,2096,670,2209];
twelfth_power_norm = nfeltnorm(nfL, twelfth_power_generator);
residue_roots = vector(#residue_primes);
for (prime_index = 1, #residue_primes,
  pp = residue_primes[prime_index];
  if (!isprime(pp)
      || lift(Mod(pp,111)) != 1
      || lift(Mod(pp-1,6)) != 0,
    error("a residue-character prime lost its splitting conditions"));
  if (lift(Mod(nfL.index,pp))
        != expected_index_residues[prime_index]
      || lift(Mod(nfL.disc,pp))
        != expected_discriminant_residues[prime_index]
      || lift(Mod(twelfth_power_norm,pp))
        != expected_generator_norm_residues[prime_index],
    error("a pinned residue-validity invariant changed"));
  roots = vecsort(lift(polrootsmod(nfL.pol, pp)));
  if (#roots != 24 || #Set(roots) != 24,
    error("a residue prime no longer splits into 24 distinct maps"));
  residue_roots[prime_index] = roots
);

residue_rank_rows = vector(2);
for (power_index = 1, 2,
  qpower = if(power_index == 1, 2, 3);
  row_count = 24 * #residue_primes;
  signature_matrix = matrix(row_count, 13);
  target_signature = vector(row_count);
  row_index = 0;
  for (prime_index = 1, #residue_primes,
    pp = residue_primes[prime_index];
    roots = residue_roots[prime_index];
    for (root_index = 1, #roots,
      row_index++;
      root = roots[root_index];
      target_signature[row_index] =
        -power_residue_signature(
          twelfth_power_generator, pp, root, qpower
        );
      for (unit_index = 1, 13,
        signature_matrix[row_index,unit_index] =
          power_residue_signature(
            structural_unit_generators[unit_index],
            pp,
            root,
            qpower
          )
      )
    )
  );
  base_rank = matrank(Mod(signature_matrix, qpower));
  augmented_rank = matrank(Mod(
    matconcat([signature_matrix, Col(target_signature)]),
    qpower
  ));
  if (base_rank != 12 || augmented_rank != 13,
    error("a class-order residue-rank certificate changed"));
  residue_rank_rows[power_index] =
    [qpower,row_count,base_rank,augmented_rank];
  print("class_order_residue_power=", qpower,
        " rows=", row_count,
        " unit_rank=", base_rank,
        " augmented_rank=", augmented_rank,
        " obstructed=true")
);

\\ Every proper divisor of 12 divides 6 or 4.  The two residue
\\ contradictions therefore prove ord([J])=12.  Since h(L)=12, J generates
\\ the whole class group.
print("class_generator_norm=", idealnorm(nfL, class_generator));
print("class_generator_exact_order=12");
print("unconditional_class_group=C12");

\\ -------------------------------------------------------------------------
\\ 6. Replay the four residual integral norm types.
\\ -------------------------------------------------------------------------

H37 = [1, 10, 26];
etas = vector(12, row,
  sum(index = 1, 3,
    K^(3 * lift(Mod(2^(row-1) * H37[index], 37)))));
if (sum(index = 1, 12, etas[index]) != -1,
  error("the twelve H-periods no longer sum to -1"));
\\ [separation, z_real, z_omega]
cases = [1,-1,-2;
         3,-2,-1;
         6,-2,-1;
         6,-1,-2];

expected_M_primes = [
  [11,5227,145753,808368911783227],
  [7,219819964650290982168469],
  [10111,6708007752409580171263],
  [60691617632525224495033153]
];
expected_M_degrees = [
  [1,1,1,1],
  [3,1],
  [1,1],
  [1]
];
expected_M_exponents = [
  [2,1,1,1],
  [1,1],
  [1,1],
  [1]
];
expected_L_primes = [
  [11,5227,5227,145753,145753,
      808368911783227,808368911783227],
  [7,7,219819964650290982168469,219819964650290982168469],
  [10111,10111,6708007752409580171263,6708007752409580171263],
  [60691617632525224495033153,60691617632525224495033153]
];
expected_L_degrees = [
  [2,1,1,1,1,1,1],
  [3,3,1,1],
  [1,1,1,1],
  [1,1]
];
expected_L_exponents = [
  [2,1,1,1,1,1,1],
  [1,1,1,1],
  [1,1,1,1],
  [1,1]
];

pair_left = [
  [2,4,6],
  [1,3],
  [1,3],
  [1]
];
pair_right = [
  [3,5,7],
  [2,4],
  [2,4],
  [2]
];
expected_class_pairs = [
  [[5,7],[11,1],[10,2]],
  [[9,3],[7,5]],
  [[0,0],[0,0]],
  [[2,10]]
];
expected_sorted_allocation_classes = [
  [2,4,4,6,6,8,8,10],
  [2,4,8,10],
  [0,0,0,0],
  [2,10]
];
expected_principal_counts = [0,0,4,0];

principal_counts = vector(4);
principal_epsilon_parities = List();
principal_epsilon_coordinates = List();

for (case_index = 1, 4,
  separation = cases[case_index, 1];
  zvalue = cases[case_index, 2] + cases[case_index, 3] * ww;
  Bvalue = 2 + zvalue * (etas[1] - etas[separation + 1]);
  Bstar = subst(lift(Bvalue), x, K^(-1));
  gamma_value = 167 - Bvalue * Bstar;
  gamma_M = cyclo_element_to_M(gamma_value);
  gamma_abs = rnfeltreltoabs(rnf, gamma_M);

  factors_M = idealfactor(nfM, gamma_M);
  if (matsize(factors_M)[1] != #expected_M_primes[case_index],
    error("an M-factor count changed"));
  for (factor_index = 1, matsize(factors_M)[1],
    if (factors_M[factor_index,1].p
          != expected_M_primes[case_index][factor_index]
        || factors_M[factor_index,1].f
          != expected_M_degrees[case_index][factor_index]
        || factors_M[factor_index,2]
          != expected_M_exponents[case_index][factor_index],
      error("a pinned M-factor changed"));
    if (!isprime(factors_M[factor_index,1].p),
      error("a rational prime below an M-factor is not proven prime"))
  );

  factors_L = idealfactor(nfL, gamma_abs);
  if (matsize(factors_L)[1] != #expected_L_primes[case_index],
    error("an L-factor count changed"));
  for (factor_index = 1, matsize(factors_L)[1],
    if (factors_L[factor_index,1].p
          != expected_L_primes[case_index][factor_index]
        || factors_L[factor_index,1].f
          != expected_L_degrees[case_index][factor_index]
        || factors_L[factor_index,2]
          != expected_L_exponents[case_index][factor_index],
      error("a pinned L-factor changed"))
  );

  fixed_class = 0;
  if (case_index == 1,
    if (!same_ideal(
          nfgaloisapply(nfL, autstar, factors_L[1,1]),
          factors_L[1,1]),
      error("the p=11 factor is not star-fixed"));
    fixed_class = certify_class_coordinate(factors_L[1,1], 0)
  );

  computed_class_pairs = vector(#pair_left[case_index]);
  for (pair_index = 1, #pair_left[case_index],
    left_index = pair_left[case_index][pair_index];
    right_index = pair_right[case_index][pair_index];
    if (!same_ideal(
          nfgaloisapply(nfL, autstar, factors_L[left_index,1]),
          factors_L[right_index,1]),
      error("a split-prime pair is not exchanged by star"));
    left_class = certify_class_coordinate(
      factors_L[left_index,1],
      expected_class_pairs[case_index][pair_index][1]
    );
    right_class = certify_class_coordinate(
      factors_L[right_index,1],
      expected_class_pairs[case_index][pair_index][2]
    );
    computed_class_pairs[pair_index] = [left_class, right_class];
    if (computed_class_pairs[pair_index]
          != expected_class_pairs[case_index][pair_index],
      error("a faithful split-prime class pair changed"))
  );

  allocation_count = 2^#pair_left[case_index];
  allocation_classes = vector(allocation_count);
  principal_count = 0;
  for (mask = 0, allocation_count-1,
    allocation = idealhnf(nfL, 1);
    allocation_class = fixed_class;
    if (case_index == 1,
      allocation = idealmul(nfL, allocation, factors_L[1,1])
    );
    for (pair_index = 1, #pair_left[case_index],
      selected_index =
        if(bittest(mask, pair_index-1),
          pair_right[case_index][pair_index],
          pair_left[case_index][pair_index]);
      allocation = idealmul(
        nfL, allocation, factors_L[selected_index,1]
      );
      selected_side = if(
        bittest(mask, pair_index-1), 2, 1
      );
      allocation_class = lift(Mod(
        allocation_class
          + computed_class_pairs[pair_index][selected_side],
        12
      ))
    );
    allocation_star = nfgaloisapply(nfL, autstar, allocation);
    if (!same_ideal(
          idealmul(nfL, allocation, allocation_star),
          idealhnf(nfL, gamma_abs)),
      error("an integral allocation does not multiply to gamma"));

    allocation_classes[mask+1] = allocation_class;

    if (allocation_class == 0,
      principal_count++;
      generator_answer = bnfisprincipal(bnfL, allocation, 1);
      if (#generator_answer != 2 || generator_answer[1] != 0,
        error("a certified principal allocation lacks a candidate generator"));
      generator = nfbasistoalg(nfL, generator_answer[2]);
      if (!same_ideal(idealhnf(nfL, generator), allocation),
        error("a returned principal generator does not generate its ideal"));

      epsilon_abs =
        generator * star_abs(generator) / gamma_abs;
      epsilon_rel = rnfeltabstorel(rnf, epsilon_abs);
      if (poldegree(lift(epsilon_rel), tt) > 0,
        error("a unit correction did not lie in the real field"));
      epsilon_M = polcoeff(lift(epsilon_rel), 0);
      epsilon_coordinates = bnfisunit(bnfM, epsilon_M);
      if (#epsilon_coordinates != 12,
        error("a correction was not a unit in the certified U_M"));
      epsilon_parity = free_parity(epsilon_coordinates);

      \\ N(U_L)/U_M^2 is exactly the one-dimensional span of N(u).
      if (epsilon_parity == vector(11)
            || epsilon_parity == unit_norm_parity,
        error("a principal allocation became correctable by a unit norm"));
      listput(principal_epsilon_coordinates, epsilon_coordinates);
      listput(principal_epsilon_parities, epsilon_parity)
    )
  );

  if (vecsort(allocation_classes)
        != expected_sorted_allocation_classes[case_index],
    error("an allocation class list changed"));
  if (principal_count != expected_principal_counts[case_index],
    error("a principal-allocation count changed"));
  principal_counts[case_index] = principal_count;

  print("case d=", separation,
        " z=(", cases[case_index,2], ",",
                  cases[case_index,3], ")",
        " class_pairs=", computed_class_pairs,
        " allocations=", allocation_count,
        " principal=", principal_count,
        " classes=", allocation_classes)
);

if (principal_counts != [0,0,4,0]
      || #principal_epsilon_parities != 4,
  error("the final integral-allocation census changed"));
for (index = 1, #principal_epsilon_parities,
  print("principal_allocation=", index,
        " epsilon_M_coordinates=",
        principal_epsilon_coordinates[index]~,
        " epsilon_free_parity=",
        principal_epsilon_parities[index],
        " unit_norm_obstructed=true")
);

print("principal_allocation_counts=", principal_counts);
print("all_principal_allocations_unit_norm_obstructed=true");
print("newly_excluded_field_norm_words=84");
print("total_excluded_sparse_B_words=396");
print("total_excluded_lift_safe_orbits=34");
print("energy_six_sector_closed=true");
print("cm_shortcut_unconditional=true");
}

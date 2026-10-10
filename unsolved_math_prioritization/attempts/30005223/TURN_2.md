# Substantive turn 2: a bulk modular/size squeeze and its quantitative gap

## Route and outcome

The second route attempted to turn known simultaneous divisibility into actual vanishing by bounding character sizes on a set of uniform conjugacy classes of probability tending to one. Unlike turn1, this treats the bulk sampling measure. It gives a precise sufficient inequality and proves that the currently established modulus range falls far short of the needed scale. It supplies no limit for the zero probability and no counterexample to actual character-table behavior.

The inputs are classical character orthogonality and partition identities, together with the explicitly credited Peluse–Soundararajan2025 Theorem1.1 and 2026 Proposition3. The deductions and the limitation of combining those inputs are set out below.

## 1. A typical-column size bound valid for every row

For a partition mu of n write m_j for the multiplicity of part j, ell(mu)=sum m_j, and

z_mu=product_j j^(m_j) m_j!.

Since m_j!<=m_j^(m_j) and j m_j<=n, one has the exact inequality

z_mu<=n^(ell(mu)).                                          (1)

Column orthogonality says sum_(lambda partitions n) chi_lambda(mu)^2=z_mu. In particular every integer character value in this column has absolute value at most sqrt(z_mu).

Conjugation of partitions is a measure-preserving bijection carrying the number of parts to the largest part. For a uniform partition, the event that the largest part is at least L is contained in the union of the events that there is a part t, for L<=t<=n. Deleting one such part gives p(n-t) possibilities. Set c=pi/sqrt(6) and q=exp(-c/sqrt(n)). The uniform bound in Peluse–Soundararajan2026 Proposition3 gives

Pr(ell(mu)>=L) <= sum_(t=L)^n p(n-t)/p(n)
              <= C q^L/(1-q).                             (2)

For any fixed A>0 choose

L_n=ceil((A+1/2) sqrt(n) log(n)/c).

Then the right side is O_A(n^(-A)). Thus, outside a set of columns of probability O_A(n^(-A)), every row simultaneously satisfies

|chi_lambda(mu)| <= exp((L_n/2)log n)
                 = exp(O_A(sqrt(n)(log n)^2)).             (3)

The exceptional probability is for the intended uniform class distribution. It has not been replaced with the cycle law of a random permutation. Equation(2) uses conjugate-partition symmetry, not an unconditioned independent-geometric model.

## 2. What the known prime-power theorem actually supplies

Let

B_n=floor(10^(-3) log n/(log log n)^2),
D_n=lcm(1,2,...,B_n).

For n sufficiently large, the 2025 Theorem1.1 gives a uniform exceptional proportion O(exp(-(log log n)^2)) for divisibility by each prime power at most B_n. There are at most B_n such prime powers. A union bound, with no independence assertion, gives

Pr(D_n does not divide chi_lambda(mu))
 <= O(B_n exp(-(log log n)^2)) =: delta_n ->0.              (4)

Every prime-power factor in the lcm is within the stated range, so (4) is a valid simultaneous conclusion. But the elementary bound D_n<=B_n! gives

log D_n <= B_n log B_n = O(log n/log log n),                (5)

which is much smaller than the size scale in (3). A stronger estimate for lcm growth does not repair that scale gap. Even the improved second-moment squeeze below does not close it.

## 3. Exact quantitative squeeze criterion

Let D>=1 be any integer and let E be any set of partitions mu with z_mu<=Z. Suppose

Pr(D does not divide chi_lambda(mu))<=delta,
Pr(mu not in E)<=epsilon.

On the event chi is nonzero and divisible by D, the integer inequality chi²>=D² holds. Averaging column orthogonality over the uniform row yields

Pr(chi !=0) <= delta+epsilon+Z/[p(n)D²].                   (6)

A more precise version replaces Z by p(n)^(-1) sum_(mu in E) z_mu. Indeed the contribution of each good column is at most z_mu/[p(n)D²], and its probability is 1/p(n). No unproved conditioning of the divisibility exceptional set is used.

Thus any future modulus D_n with delta_n->0 and a good-column centralizer threshold satisfying Z_n/[p(n)D_n²]->0 would prove that the zero probability tends to1. This is a sufficient criterion only. Inserting (1)–(5) gives a bound whose last term grows without bound: log Z_n is of order sqrt(n)(log n)^2, log p(n) is of order sqrt(n), and log D_n is only O(log n/log log n). The method therefore does not establish its sufficient hypothesis, let alone the conjecturally opposite limit0.

There is also a formal scalar obstruction to inferring zero merely from (3) and (4): for all sufficiently large n, the nonzero integer random variable taking values ±D_n with equal probability satisfies divisibility by every prime power in range, satisfies the bound in (3), and even satisfies the upper second-moment bound Z_n/p(n) for that bulk threshold. It never equals zero. This example is not a character table and is not alleged to satisfy all character orthogonality identities; it proves only the logical insufficiency of these particular size/divisibility inequalities.

## 4. Finite controls and remaining mathematical question

The exact checker verifies (1), column orthogonality, and inequality(6) directly for small complete character tables, several moduli and several good-column thresholds. It tests the simultaneous prime-power/lcm equivalence on integers, including negative values and zero. It uses no numerical fit to infer an asymptotic.

The route has now isolated what it would need: quantitative divisibility by a dramatically larger simultaneous modulus, or substantially sharper nonzero-value information. Neither follows from fixed-modulus convergence, and such a result must be reconciled with the predicted density2/log n. The next route should seek anti-concentration under an exact fixed-n partition disintegration, rather than accidentally treating cycle counts as independent after conditioning their total size.

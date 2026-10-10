# Independent review: 30005223

**Verdict: PASS_SCOPED_PARTIALS. The original problem remains unsolved after five substantive author turns. No mandatory mathematical correction.**

This verdict binds FROZEN_MANIFEST.json SHA-256 `dc4bbea7a572a47a845c3ec80405db37cbe6c9556e9e461475e1515c59a4c8bb`, including RESULT.md SHA-256 `36fffe57c6e952c30525f8565bc27b632dc9621a753f26b8fcb385c89bfe4093`. The five historical snapshots also remain hash-valid. Review date: 1 October 2026.

## Scope and independence

I did not contribute to these five author routes. I read all five proofs, the consolidated result, exact source passages and all supplied programs. I independently reconstructed character values using the Frobenius alternant, rather than the author's rim-hook recursion. Review checks are verification, not a sixth proof-search turn.

The source asks about the proportion of zeros under independent uniform partitions of n. The retained work establishes scoped identities, reductions, countercontrols and a genuine finite irreducible example. It establishes no limiting value, existence of a limit, or asymptotic for the full proportion. Uniform permutations, Plancherel rows and unconditioned geometric cycle counts cannot be substituted for the source measure.

## 1. Exact family and its asymptotic mass

For the standard row (n-1,1), the character is the number of unit cycles minus one. Its hook multiset is {n,n-2,n-3,...,1,1}. For t at least 2, the number of hooks divisible by t is floor(n/t) minus the indicator that t divides n-1. With n-1=m and nu a partition of m without units, the weighted type-III inequality can hold exactly when t divides every part of nu. Thus type III is equivalent to gcd(nu)>1; types I and II in this family reduce to the single-part case.

Möbius inversion correctly treats the d=1 no-unit condition separately: the residual count is p(m)-p(m-1) plus the sum of Mobius(d)p(m/d) over divisors d>=2. The latter has absolute value at most m p(floor(m/2)), exponentially smaller than p(m)/sqrt(m). The cited uniform partition-ratio estimate has error O(m^(-3/4)) for a unit deletion, smaller than the leading m^(-1/2) difference. Consequently the stated two-conjugate-row density is correct. The rows are distinct for n>=4, and their total mass is exponentially small under uniform rows.

The beta-set explanation of sequential extinction is valid. The change of removal order in the six-letter example changes the unsigned chain count while preserving the signed character value. The separate S4 example genuinely has two cancelling canonical-order chains. Neither argument equates all zeros with strip extinction.

## 2. Bulk modulus/size reduction

The elementary bound z_mu<=n^(length(mu)) follows factor by factor from m_j!<=m_j^(m_j) and j m_j<=n. Uniform partition conjugation, deleting a large part, and the uniform ratio estimate give the claimed good-column probability and log z_mu=O(sqrt(n) log^2 n), simultaneously for every row.

All factors of p(n) and D are correct in the modular second-moment inequality. Summing column orthogonality on good columns yields the exact remainder sum(z_mu)/(p(n)^2 D^2), bounded by Z/(p(n)D^2). Failure of divisibility and the bad-column mass are ordinary union-bound terms under the uniform pair measure.

The prime-power theorem is used only in its actual uniform range. There are at most B prime powers at most B, so the union bound tends to zero for the chosen B. The simultaneous modulus is lcm(1,...,B); its elementary logarithmic upper bound is much too small for the displayed good-column estimate to make the final remainder small. This failure is a limitation of these bounds, not an obstruction to a stronger theorem. The scalar countercontrol claims only insufficiency of the named restricted inputs.

## 3. Exact fibers and trace representation

Deleting all parts 1 and 2 partitions the column set into fibers of size s+1. Conditional r is uniform, whereas the fiber itself has mass (s+1)/p(n). The source row stays independent and uniform. Deleting unit parts proves the short-fiber estimate without an independent-cycle approximation.

The elementary abelian subgroup on disjoint transpositions commutes with the fixed large-cycle permutation. Permuting the transposition pairs identifies equal-cardinality eigenspaces and their traces. The trace coefficients are rational by the projector formula and algebraic integers because the remaining operator has finite order, hence integers. Positivity is asserted only for the identity residual permutation.

Both Krawtchouk transform directions and the leading coefficient (-2)^j/j! are correct. The top nonzero trace gives the interpolation degree, and the root bound is averaged with the correct size-weighted fiber law. The finite-difference expression and the pairing with e_2^s p_1^(R-2s) p_nu have the correct sign and factor 2^s.

The sign row and the reducible regular representation are valid and explicitly limited countercontrols. In particular, the latter cannot serve as a counterexample about a typical irreducible row. Neither long fibers nor integrality proves either missing bulk condition.

## 4. Annihilator and fourth moment

The residual virtual character has Frobenius characteristic p_nu^perp s_lambda. Its specialization to p_1=x, p_2=y gives the stated coefficient denominator (R-2r)! 2^r r!, so complete fiber vanishing is precisely membership in the ideal generated by p_3,p_4,... . This does not require the unspecialized virtual character to vanish.

Differentiating the Jacobi–Trudi determinant row by row gives the labeled row-assignment formula. Repeated parts retain their multiplicities through repeated labeled derivatives. The operator p_t^perp=t*d/dp_t sends h_m to h_(m-t), so no additional t or factorial is missing.

The actual S11 example passes an independent character computation. Its complete S5 residual Schur coefficients are 2, 2 and -2 on (5), (2,1,1,1) and (2,2,1), respectively. Its only nonzero S5 values are 6 at (3,1,1) and (3,2), giving p_3(p_1^2+p_2). All three specified S11 fiber columns are zero and fail the weighted type-III test. The extension by induction is correctly described as virtual; no infinite irreducible family or positive asymptotic mass follows.

Column normalization by sqrt(z_mu) really gives an isometry. The diagonal of its orthogonal projection lies in [0,1] and sums to the number q of columns. Cauchy–Schwarz on its support gives exactly the claimed zero-row probability bound. A uniform relative fourth-moment estimate on fibers of probability tending to one would suffice. Ordinary second-moment orthogonality does not supply it; the abstract coordinate projection demonstrates the missing input without purporting to be an actual character table.

## 5. Analytic conditioning and pointwise transfer

The single-partition atom constant is 1/(2*6^(1/4)), multiplying n^(-3/4). This agrees both with the cited saddle formula and with combining the partition and product asymptotics directly. Conditioning on two independent sizes has the product loss. These are sufficient error demands for the stated elementary inequality, not necessary demands for every possible method.

The largest Boltzmann size atom is indeed O(t^(3/2)) for q=exp(-t). To check uniformity over the size index, put x=(c/t)^2. The exponent of p(m)exp(-tm) is c^2/t-t(sqrt(m)-sqrt(x))^2. On [x/2,2x], the amplitude is comparable to x^(-1), and the width is x^(3/4). The denominator therefore has order x^(-1/4)exp(c^2/t), while a single central term is at most a constant times x^(-1)exp(c^2/t). Outside that interval the same square gives exponentially small tails, including m=0. This proves the uniform atom bound and hence the vacuity of an unconditioned same-size event.

The powers-of-two sparse-spike proof is rigorous for the squared partition weights as well. The central amplitude is now comparable to x^(-2), with the same width x^(3/4); the total central mass has order x^(-5/4)exp(2c^2/t). A single normalized central atom is O(x^(-3/4)). On the lower tail there are O(x) terms, each with a fixed exponential deficit of order sqrt(x), up to polynomial factors. On the upper tail, (sqrt(m)-sqrt(x))^2 is bounded below by (1-1/sqrt(2))^2 m, yielding a summable exponential tail. The Hardy–Ramanujan asymptotic supplies uniform fixed-factor bounds after finitely many initial sizes. At most three powers of two occur in [x/2,2x]. Thus the weighted spike average tends to zero although the sequence has infinitely many values one.

The same two-sided Gaussian-scale bounds give a positive fraction of mass in every fixed positive-width window |m-n|<=a n^(3/4), including an upper bound on the full denominator. Therefore the one-sided local-regularity criterion does imply the stated pointwise conclusion. The packet neither establishes that regularity for actual character zeros nor identifies its abstract sparse sequence with them.

Both branching support inequalities survive signed cancellation: a nonzero sum has at least one nonzero summand; the induction identity gives a nonzero extension in the reverse direction. Multiplicity-free branching and maximum predecessor/successor counts give the stated bounds, including the extra unit-free columns. Dividing by p(n+1)^2 produces r_n^2 and the error 1-r_n exactly. The square-root corner factors do not yield the desired additive regularity.

## Verification and disposition

All 37 author entries, all five historical manifests and all three source PDFs match their pinned hashes. All six author outputs reproduce byte-for-byte: 38,109; 8,206; 199,590; 2,556; 388; and 17,105 exact assertions. The separate independent checker passes 21,090 exact assertions, using the Frobenius alternant and direct Boolean Fourier sums without importing author code. These are finite controls, not substitutes for the analytic proofs reviewed above.

The remaining problem is a bulk estimate outside the known zero types, or another valid route to the full uniform-table limit. No such estimate is established. The appropriate disposition is **unsolved, 5/5**, with the retained scoped deductions accepted. No novelty certification is made. Publication should retain the measure, missing moment/anti-concentration inputs, virtual-versus-irreducible distinction and pointwise-transfer limitations prominently.

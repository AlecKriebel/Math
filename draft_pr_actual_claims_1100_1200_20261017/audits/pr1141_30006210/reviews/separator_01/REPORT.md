# PR1141 separator/Markov independent adversarial review

## Verdict and exact scope

**PASS for Lemmas 1–2, their cited source interfaces, and the numerical separator-to-theorem interface.** No fatal, major, or minor mathematical defect was found in this assigned family. No repair is required in these two lemmas. This is an independent internal mathematical review, not an external peer-review or novelty determination.

Reviewed the actual affirmative claim: nonzero real multilinear f,g on {-1,1}^n of degree at most d, n,d>=1, with every full-norm relative Fourier influence at most 1/(4096d^8), have intersecting supports. The stronger necessary disjointness bound is max_i max(RelInf_i(f),RelInf_i(g))>=1/(1024d^8). Input PROOF.md is 13,567 bytes, SHA-256 20bf5956520b2b53bb4b415d7d5683a6ae1cf1273bd36372accbc49fab482da1. The same bytes were authenticated directly against source commit b1d6bc6ceb66e9c9c98cfae229ee86e5720799e2 at unsolved_math_prioritization/attempts/30006210/PROOF.md.

The independent universal reconstruction is in INDEPENDENT_CORE.md and was recorded before primary-source inspection. SOURCE_CHECK.md records literal source verification and read limits. No input AUDIT.md or earlier conclusion artifact was read. The whole proof was read to check this family's downstream interface, but the full independent adversarial review of the adaptive covariance lemma and the historical target formulation belongs to root and other reviewers.

## Mechanism and proof obligations

1. **Markov normalization:** the affine change from [-1,1] to [0,1] produces the factor 2. Bernoulli averaging turns a bounded multilinear R into a univariate P of no greater degree and gives P'(0)=sum_j(R(e_j)-R(0)). Hence b<=2m^2, including harmless zero-degree/zero-block boundaries. The example R(y1,y2)=1-y1-y2 saturates the factor 2 for m=1; dropping it would be false.
2. **Maximum-degree coefficient survival:** fixing outside a degree-deg(q) monomial leaves its coefficient intact because no strict superset can occur. Uniqueness of the multilinear cube representation turns the remaining nonzero coefficient into a nonzero vertex value. Starting at a zero of q, the witness differs on a nonempty subset of that monomial. The argument would fail for an arbitrary lower-degree monomial, and the test controls explicitly reject that false variant.
3. **Disjoint family versus maximum matching:** inclusion-maximality is exactly enough. Its union hits every degree-deg(q) monomial. A maximum-cardinality family is unnecessary. One can have a maximal singleton family {x2x3} in q=x1x2+x3x4+x2x3 while the maximum disjoint family has two members. The singleton union still reduces degree on every answer branch; exact controls confirm all four assignments.
4. **Bounded block polynomial:** choose a global maximizer of |p^2-q^2| on the current subcube. Disjointness makes its magnitude positive and its sign identify the nonzero side. Each disjoint block flips to the opposite side. Substitution by affine one-bit coordinate maps, followed by Boolean multilinearization, cannot increase total degree, including when several original coordinates depend on the same block bit. Thus m<=2D and b<=8D^2. The query union has at most 8D^2 deg(q)<=8d^3 coordinates.
5. **All branches and termination:** every answer hits each old maximum-degree monomial, so the selected opposite polynomial becomes zero or strictly loses degree. The other degree cannot increase. A branch where either restriction is zero terminates before the degree of the zero polynomial is needed. While both are nonzero, both degrees are positive. The sum decreases by at least one per batch, giving at most 2d batches and depth at most 16d^4. Every queried coordinate was free, so none repeats.
6. **Common-zero totalization:** if p is identically zero output 0, otherwise if q is zero output 1. These deterministic leaf rules cover both-zero restrictions and satisfy both support obligations. The source construction itself permits arbitrary both-zero labels. No promise restriction is silently carried into the uniform-input covariance calculation.
7. **Real coefficients and basis:** squaring removes all sign issues; normalization by a positive finite maximum removes scale issues. There is no coefficient lower bound. The affine +/-1 to 0/1 change preserves degree in both directions and queries. Degree zero, n<d, empty remaining cubes, arbitrary common zero sets, and all-input disjointness cause no gap.

These obligations are proved algebraically in INDEPENDENT_CORE.md. The exact finite checks below supplement the proof; they do not establish a universal result by enumeration.

## Exact reproducible controls

Run from this review folder:

    python3 verify_exact.py --output results.normal.json
    python3 -O verify_exact.py --output results.optimized.json

The checker uses exact integers and rational numbers, a truth-table Mobius transform, and independent minimax support-label trees. It does not reproduce the submitted separator's greedy construction. Both runs passed; RESULT_COMPARISON.json records equality of all mathematical results after excluding runtime fields.

- All 6,651 ternary truth tables on n=1,2,3: 10,206 maximum-monomial coefficient restrictions, 20,852 nonempty block witnesses, 7,806 inclusion-maximal disjoint families, and 52,968 restrictions by their query unions.
- All 391,280 pointwise disjoint signed ternary pairs on n=0,1,2,3, including 377,976 pairs with both polynomials nonzero. Independent minimax trees cover all 6,654 support labelings, of which 6,376 have common zeros. Their maximum optimal depth is 3. Every pair satisfies the submitted separator bound and exact stronger necessary influence bound. The minimum max-relative-influence within this finite signed class is 1/2 for d=1 and 1/4 for d=2 or 3; no extremality beyond this finite class is claimed.
- All 663 ternary bounded R with R(0)=1 and R(e_i)<=0 for b=0,1,2,3: 3,315 rational Bernoulli-moment equalities and derivative/bound checks. The degree-one sharp factor-2 fixture also passes.
- Deliberately wrong controls rejected in both modes: missing Markov factor 2; nonmaximal family; coefficient survival for a lower-degree monomial; wrong separator leaf; repeated coordinate query. These use explicit exceptions, so optimization cannot disable them. Separate fixtures check a maximal but nonmaximum family and three exact rational scalings, including 10^-80 and -10^80.

Numerical/runtime limits: no random sampling, floating-point inference, external solver, or unbounded exhaustive assertion. Finite enumeration is restricted exactly as above; arbitrary reals and dimensions are handled by the proof. Runs used Python 3.14.6. There are no test failures or unexplained exclusions.

## Cross-lemma constant check

For a total h, normalized u=f^2/Ef^2 and v=g^2/Eg^2 have hu=u, hv=0 and Eu=Ev=1, giving Cov(h,u)=1-Eh and Cov(h,v)=-Eh. Common zeros do not alter the identity that the absolute covariances sum to 1. With the stated adaptive covariance and resampling inequalities, each is at most T sqrt(delta), hence 1<=2T sqrt(delta)<=32d^4 sqrt(delta), and delta>=1/(1024d^8). The target threshold gives at most 1/2 on the right and therefore a strict contradiction. Full-norm normalization including the constant Fourier coefficient is necessary and is indeed the input convention. No cross-lemma inconsistency was found.

## Strongest verified result and remaining gap

This reviewer independently verifies the universal total separator theorem of depth 16d^4 for arbitrary real disjoint polynomial supports, with an elementary proof conditional only on classical univariate Markov. The source literature literally provides the required structural lemma and block inequality. The assigned separator/Markov family has no remaining mathematical gap. The full affirmative theorem additionally requires the separately reviewed adaptive covariance and Fourier resampling bounds; the target identification, historical endpoint/obstruction claims, novelty, external publication status, and remaining source literature were outside this review's independent primary-source scope.

No external individuals were contacted. No commit, push, PR change, tracker write, paper promotion, release, or Zenodo operation was performed. All files authored by this reviewer are confined to this review directory. Shared files, index, refs and main were not modified by this reviewer.

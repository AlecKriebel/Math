# PR 458: independent original-source and mathematical-scope audit

Reviewer: `/root/pr458_source_admissibility`. Problem `20000693`; PR 458; frozen head `87a39f7b4e5ef81aacf98464f86586cc95684d7f`. This review concerns the exact `claimed_solved` candidate frozen by the parent. Original proof-search attempts: **0**. No remote changes, source changes, publication, status action, or external communication were performed.

**Verdict: the explicit fixed, unshifted Dirichlet-product heuristic is mathematically coherent and admissible as a response to the original displayed example.** No blocking source mismatch, required mathematical repair, or unresolved gap in the stated local analysis was identified. This is not acceptance of a proved critical-line moment asymptotic, a universal theorem for imprimitive L-functions, or a priority claim. One optional citation correction is recorded below.

## Independent reconstruction and provenance

I read the workspace AGENTS policy, then fetched the live [AIM section 5](http://aimpl.org/zetamoments/5/) before reading the author's heuristic or historical review conclusions. The current primary object has ID `ed2f7227f2b11f99ac79c4370904ff7c`, revision `28-2823610319f29aeb692da490e32e6685`, number 5.3, and attribution C. Turnage-Butterbaugh. Its status field is empty. The live HTTP HTML is 33,521 bytes, SHA-256 `e61d05b854171b45265d2f316e6d08702cb210a3e4f8a3ad2d87b79360df5484`, matching the historical checksum independently. The HTTPS certificate fails hostname validation; the browser retrieval also failed. Neither failure was bypassed.

The task asks for a heuristic for imprimitive L-function moments or products of degree-one factors. Its displayed example is an absolute square of an unshifted critical-line Dirichlet product; it permits differing powers. The source does not specify a varying conductor, shifts, a negative-power range, lower-order terms, or a demand to prove the conjectured asymptotic. Thus a fully specified nonnegative-power, fixed-conductor answer to that displayed example is an admissible reading. The disjunctive, informal wording does not establish a theorem quantifying over every possible higher-degree imprimitive L-function.

My independent reconstruction was written to `INDEPENDENT_RECONSTRUCTION.md` before reading `author/HEURISTIC.md`. I subsequently read the entire heuristic, source gate, current README, addendum, and author verifier. I did **not** semantically read historical peer reports; their hashes were checked solely to bind the frozen input packet. All 27 source payloads match the parent receipt. No source file was edited.

Primary context was read directly, not inferred from abstracts: relevant complete pages of [Heap, arXiv:1303.6119v1](https://arxiv.org/pdf/1303.6119), [Sahay, arXiv:2103.13542v3](https://arxiv.org/pdf/2103.13542), and the [published Keating--Snaith PDF](https://people.maths.bris.ac.uk/~mancs/papers/RMTzeta.pdf). Fourteen complete pages were rendered and visually inspected, with exact page sets in `PRIMARY_INSPECTION_RECEIPT.json`. Foreign PDFs, HTML, extracted text and rendered images remain private and are excluded from the positive publication manifest. This is a bounded source audit, not an exhaustive priority search.

## Exact claim and success criterion

For finitely many characters chi_i modulo positive integers q_i and fixed real a_i >= 0, define

    I_a(T) = integral_[T,2T] product_i |L(1/2+it,chi_i)|^(2a_i) dt.

All parameters are fixed as T grows. Zero-weight factors are omitted, including at zeros. Let psi_i be the primitive inducer, M_psi = sum_(psi_i=psi) a_i, and E = sum_psi M_psi^2. The predicted leading term is

    I_a(T) ~ T A G (log T)^E,
    G = product_psi BarnesG(1+M_psi)^2 / BarnesG(1+2M_psi).

The arithmetic constant A is explicitly defined by an increasing-prime Euler product and equivalently by a positive absolutely regularized expression. Success here means: correct local identities and normalizations; a finite positive proposed constant; correct grouping; every transport from local models to actual moments labeled conjectural; explicit boundaries matching the stated response. Proving the high-moment asymptotic is a separate unsatisfied mathematical goal, not a premise secretly imported into this heuristic response.

## Analytic verification of the proposed constant

Write A_0 = sum_i a_i, Q = lcm_i q_i, and S = {p:p divides Q}. For |z|<1 set

    B_p(z) = product_i (1-chi_i(p) z)^(-a_i) = sum_(r>=0) b_p(r) z^r,
    J_p = sum_(r>=0) |b_p(r)|^2 p^(-r).

The branch analytic at zero with value one is unambiguous: every factor 1-chi_i(p)z avoids zero in the unit disk. For real a_i the squared absolute value of this branch equals the stated absolute-value power, so no complex-power choice enters the actual moment integrand.

When A_0>0, coefficientwise absolute values are bounded by d_(A_0)(r)=(A_0)_r/r!. This follows by the generalized binomial series and convolution of nonnegative majorants. These coefficients grow at most polynomially. Since p^(-1/2)<1, Parseval on that radius gives exactly

    J_p = average_theta product_i |1-chi_i(p)e^(i theta)/sqrt(p)|^(-2a_i).

The integrand is continuous, positive and bounded on the circle. In particular J_p >= 1. The coefficient b_p(1)=sum_i a_i chi_i(p), and the polynomial majorant bounds the r>=2 tail uniformly for p>=2 by a constant times p^(-2). Therefore

    J_p = 1 + |sum_i a_i chi_i(p)|^2/p + O_a(p^(-2)).

At p outside S, all characters have unit absolute value and chi_i(p)=psi_i(p). Expanding the square gives

    |sum_psi M_psi psi(p)|^2
      = E + 2 sum_(psi<phi) M_psi M_phi Re(psi(p) conjugate(phi(p))).

For distinct primitive psi and phi, rho=psi conjugate(phi), viewed on lcm of their conductors or induced to Q, is nonprincipal. Otherwise their inductions to Q would coincide and uniqueness of the primitive inducer would force psi=phi. The quotient convention is fixed explicitly by the additive clarification; an unspecified larger modulus introducing primes outside Q must not be substituted.

Define the positive local regulator

    H_p = J_p (1-1/p)^E
          product_(psi<phi) |1-rho_(psi,phi)(p)/p|^(2M_psi M_phi).

The first-order terms cancel with the **positive** displayed exponent on the absolute Euler factor; H_p=1+O_a(p^(-2)). Its product over p outside S converges absolutely to a nonzero positive number. Ordered nonprincipal Euler products at one converge for fixed modulus, and their values are nonzero; the latter is also stated in [DLMF 25.15.9](https://dlmf.nist.gov/25.15). Thus

    A = product_(p in S) (1-1/p)^E J_p
        product_(p notin S) H_p
        product_(psi<phi) |L^S(1,rho_(psi,phi))|^(2M_psi M_phi)

is finite and strictly positive. Reversing the regularizer sign leaves an uncanceled first-order term and is an actual rejected control. The original unregularized product is only claimed to converge in increasing prime order; absolute convergence is not inferred for general distinct factors. The analysis also explains why an unsupported absolute-convergence sentence in a broader Selberg-class derivation cannot substitute for the present explicit regulator.

For all-zero weights, B_p=1, J_p=1, E=0 and the Barnes product is empty. The original moment is exactly T. Adding a zero-weight character can enlarge Q and S, but does not change B_p or E. Moving a finite prime between H_p and the S-product is exactly balanced by the corresponding finite change in L^S, so the regularized expression remains invariant.

## Primitive grouping and finite Euler deletions

The exact inducing-character identity is

    L(s,chi_i) = L(s,psi_i) product_(p|q_i)(1-psi_i(p)p^(-s)).

It follows from the Euler product in Re(s)>1 and continues meromorphically; [DLMF 25.15.4](https://dlmf.nist.gov/25.15) gives the same relation. At primes dividing the primitive conductor, psi_i(p)=0 makes the extra factor one. On Re(s)=1/2 every deletion factor is nonzero because its subtracted term has absolute value at most p^(-1/2)<1.

Grouping the primitive core is therefore exact. Equal primitive inducers have the same zero factor, so their weights add **before** the square in E. Labels q_i are not independent primitive constituents. Let tilde chi_i denote the induction to Q. Then

    L(s,chi_i) = L(s,tilde chi_i)
                product_(p|Q, p not dividing q_i)(1-psi_i(p)p^(-s))^(-1).

The restoration factors are inverse Euler factors, not finite Dirichlet polynomials. The sign is independently checked coefficient by coefficient through degree 12. At each restored prime, every factor shares the phase e^(-it log p). It is incorrect to multiply separate phase expectations. Relative to the primitive-core arithmetic constant, only finitely many local factors change:

    A/A_star = product_(p|Q) J_p/J_p_star.

This is an exact identity between **defined constants**. It is not a theorem transporting actual moment asymptotics through finite factors. Boundedness of finite factors alone would provide only comparability of orders of magnitude, not this exact leading constant. The author's distinction is explicit and correct.

## Adversarial edge cases and falsification attempts

1. **Same inducer, different moduli.** Zeta and the principal character modulo 2 both induce the conductor-one character. With weights one, E=4 and the Barnes factor is 1/12. At p=2 the primitive core has J_star=(1+x)/(1-x)^3=12, x=1/2, whereas the actual remaining zeta factor has J=1/(1-x)=2. The ratio is 1/6. The predicted coefficient is consequently 1/(12*pi^2). Modulus-based independent matrices would incorrectly give exponent two.
2. **Different deletion sets on the same core.** Principal characters modulo 6 and 10 again give E=4. Relative to zeta squared, the local ratios at 2,3,5 are 1/12, 1/3 and 8/15, hence their product is 2/135. This tests overlapping and nonnested deletion sets; no common-modulus simplification may drop the restored factors.
3. **Correlated local means.** At x=1/2, two identical weight-one factors have common-phase mean 12. Separate expectations give 2*2=4. This is a concrete counterexample to the tempting factorwise averaging rule.
4. **Conjugate nonreal characters.** A quartic primitive character modulo 5 and its conjugate are distinct. With weights one, E=2, not four; their quotient is the nonprincipal quadratic square. The functional equation relates a character at t to its conjugate at -t, not two identical primitive functions at the same positive t. Real characters coincide with their conjugates and are grouped accordingly.
5. **Different conductors and fractional weights.** The suite includes primitive quadratic characters of conductors 3 and 4 with different induced moduli and weights 1/2,3/2,1/3, plus independently weighted quartic conjugates. Their formal coefficients, local lift, grouping and regularizer cancellation hold exactly. Fractional weights do not follow from analytic continuation of integer L-function moments; the paper labels them as a model extension.
6. **Single-character normalizations.** Weight one gives A=phi(q)/q, E=1 and Barnes factor one. Weight two gives A=zeta(2)^(-1) product_(p|q)(1-1/p)^3/(1+1/p), E=4 and Barnes factor 1/12. These follow from elementary geometric-series local identities and agree with the stated mean-square/fourth-moment normalizations.
7. **Zero weights.** Zero factors are omitted instead of assigning 0^0 at zeros. Entirely zero input yields the exact T identity. Several auxiliary moduli with zero weights do not alter the original local factors.
8. **Negative powers.** They are outside the stated scope. Near a zero of order r, a single absolute-value power behaves like |t-t_0|^(2ar), locally integrable only if 2ar>-1. A primitive product repeated e times has effective weight ek; a nominal outer range k>-1/2 can fail after repetition. For example e=2, k=-0.3 gives effective weight -0.6, whose simple-zero singularity is not integrable. The exclusion has mathematical content and does not hide a proved negative-moment statement.
9. **Moving parameters, shifts, smoothing, and conjugate/unbalanced moments.** Fixed conductors make product log(f_psi T)^(M_psi^2) asymptotically equivalent to (log T)^E. This does not imply uniformity when f_psi grows, determine lower-order logarithmic constants, or permit shifted inputs. A smooth-weight prediction is separately labeled heuristic, not inferred from the unweighted asymptotic without a uniform argument.
10. **Limit interchange and prime phases.** For any fixed finite prime set, integer independence of log p follows from unique factorization; the phases along t equidistribute on the corresponding torus. That exact finite-prime fact does not justify a cutoff X growing with T. The author's explicit model assumption prevents this unsupported interchange.

## Model assumptions and primary-source application

The cancellation of (e^gamma log X)^E is algebraic once the modeled prime and zero means are supplied. It does not prove either mean. The substantive unproved steps are: the growing-cutoff prime mean at the desired scale; unitary modeling of primitive zeros; independence of distinct primitive constituents; and weighted splitting of prime and zero components. Equality of primitive inducers specifically prevents invoking constituent independence between repeated factors.

[Heap](https://arxiv.org/pdf/1303.6119), printed pp.5-6 and 36-39, gives the constituent multiplicity principle and factorwise heuristic under assumptions. [Sahay](https://arxiv.org/pdf/2103.13542), pp.7-8, supplies common-modulus nonnegative integer tuples and calls its conditional Theorem 1.7 conjectural. Pages 17-18 use GRH in the intermediate zero-model derivation; the addendum preserves that attribution without asserting GRH proves the statistical assumptions. Pages 33-34 already discuss differing-modulus two-factor constants. None of these contextual checks is a first-priority certification.

The [Keating--Snaith PDF](https://people.maths.bris.ac.uk/~mancs/papers/RMTzeta.pdf), printed pp.59-60, gives the gamma product for the finite CUE mean, with Barnes-G asymptotics for nonnegative real weight. These exact random-matrix results support the model parameter range, not actual Dirichlet moment asymptotics. An individual real Dirichlet character in the t-aspect is still modeled with unitary symmetry; central-value varying-character symmetry is a different family.

## Checkable independent computation

`verify_scope.py` uses only the Python standard library and explicit runtime guards. Its logarithmic-derivative recurrence

    n c_n = sum_(j=1..n) (sum_i a_i z_i^j) c_(n-j)

is independent of the author's coefficient-convolution construction. It uses exact Gaussian rationals for degree-12 identities and character tables, plus a separate numerical phase average. It verifies primitive conductors by finite witnesses against every proper conductor divisor and quotient nonprincipality on common-modulus units.

The normal and Python `-O` runs each pass **2,344 checks** with byte-identical JSON outputs. The categories are recorded in the two result files rather than combined with historical authors' differing count conventions. There are 24 numerical phase checks on 2,048 equally spaced angles with degree-160 series; the largest relative discrepancy is `8.88178419700126e-16`. This floating-point corroboration is not a rigorous numerical error certificate and is not used as the analytic convergence proof.

Six actual mutant mechanisms are rejected in each Python mode, for 12 subprocess controls: modulus grouping, conjugacy grouping, inverse-lift direction, regularizer sign, independent local phases, and ignored deletion. Every rejection exits one, emits zero success-output bytes, and names the failed check. Integer CUE weights zero, one and two are tested using exact factorial ratios. No actual critical-line L-values, high moments, random-matrix independence, or growing-cutoff asymptotics are certified numerically. The historical assert-based author verifier is not operationally approved by this separate scope review.

## Findings, precise residual limits, and disposition boundaries

Blocking source issues: **0**. Required mathematical repairs: **0**. Unresolved mathematical gaps in the claimed local theorem and explicitly conjectural heuristic construction: **0**. Central source mismatch: **false**. The high-moment asymptotic remains unproved by design; its model assumptions must remain prominent in any proposed preprint, metadata, queue finding, or public summary.

Optional documentation correction **C1**: `author/SOURCE_GATE.md`, prior-coverage item 3, cites Keating--Snaith equations (10)-(12) for the Barnes asymptotic. In the actual published PDF those equations concern cumulants. The relevant references are (6), (15) and (16), printed pp.59-60. The formula in `HEURISTIC.md` is correct; this reference-number issue does not change mathematical acceptance. A future explanatory layer or preprint should use the correct locations while preserving frozen historical bytes when appropriate.

This report accepts only the mathematically defined heuristic and its elementary local analysis. It does not authorize a status correction, approve a publication package, certify novelty, conclude prior coverage of the entire original problem, or certify an all-L-functions result. The parent must evaluate priority independently and retain the heuristic/theorem distinction. No reviewed condition supports describing this work as a newly proved high-moment theorem or as human-refereed mathematics.

# Independent source/parity audit: PR 466

Audit scope: problem 30000999 / OWR-2042-008, frozen PR head `77a27c5da92b8f42f79b2f27e40f5c9a6403ddb9`. This report audits the literal original target, unrestricted counterexample, parity/support assumptions, and dimension/order boundaries. It does not certify historical priority or the separate high-frequency theorem on even densities.

## Verdict

**The literal inverse question is fully resolved negatively by Theorem 1 of the frozen `release/PROOF.md`.** No mathematical or source-parity defect was found. The original text admits all spherical probability measures and explicitly discusses point masses. Its transform gives the same equator measure to antipodal point masses, while ordinary spherical Wasserstein distance separates them by pi.

Counts within this audit: **0 blocking mathematical issues; 1 minor provenance wording issue; 0 unresolved gaps in the literal negative result.** Any implicit historical intention to ask an even-only question is not documented in the inspected contribution. Such an intention cannot be substituted for its stated admissible class.

Independence: `INITIAL_HYPOTHESIS.md` was written before reading the frozen proof, source gate, or any peer report. No earlier independent audit or fresh peer report was subsequently read. The official source was retrieved independently and all relevant pages were visually inspected. No Git/index/branch or remote publication action was taken.

## 1. Exact target and source parity

The source is [Stephens's contribution in official OWR 31/2008](https://ems.press/content/serial-article-files/46174), printed pp. 1762-1764. The exact mathematical definitions and final question occupy p. 1763. The independently verified byte receipt and page mapping are in `SOURCE_RECEIPT.md`.

For the standard unit sphere S = S^(n-1), write d(x,y) = arccos(x dot y) for intrinsic spherical distance. Let E(u) = {x in S : x dot u = 0}. For n >= 3, let sigma_u be surface measure on E(u) divided by its total area. In the circle extension n = 2, sigma_u assigns mass 1/2 to each of its two points. The source's function operator is

    Ff(u) = integral_E(u) f(x) d sigma_u(x),   f continuous on S.

Its spherical measure operator is the dual:

    integral_S f d(Rmu) = integral_S Ff dmu.

The admissible measures are P(S), and the source's order range is 1 <= p < infinity. Its metric is

    W_p(mu,nu) = inf_{gamma in Gamma(mu,nu)}
                     (integral d(x,y)^p dgamma(x,y))^(1/p),

where Gamma contains probability measures on S x S with marginals mu and nu. Compactness gives finite cost for every admissible pair.

The final prose question concerns a uniform bound on loss of Wasserstein distance. The displayed reverse inequality in the frozen proof is a precise formalization, rather than a formula literally displayed in the source:

    W_p(mu,nu) <= C(p,n) W_p(Rmu,Rnu) for all mu,nu in P(S),

with finite C(p,n). Equivalently, it asks for a positive uniform lower contraction factor. The counterexample below disproves either reciprocal convention.

The source writes no assumption of evenness, antipodal identification, restricted support, absolute continuity, regularity, positive densities, or zonal symmetry. The opening tomography motivation does not narrow the subsequent explicit probability-measure domain. Moreover, its moving-delta examples positively confirm the admissibility of atoms. The reference to earlier inverse-norm studies does not import a restriction into these definitions.

## 2. Checkable reconstruction of the counterexample

Fix any u in S and put mu = delta_u and nu = delta_(-u).

**Admissibility and output.** Each is a Borel probability measure. Since x dot u = 0 if and only if x dot (-u) = 0, their equators coincide, with the same normalized measure. For every continuous f,

    integral f d(R delta_u) = Ff(u) = integral f d sigma_u,
    integral f d(R delta_(-u)) = Ff(-u) = integral f d sigma_u.

Continuous functions determine Borel probability measures on a compact sphere. Thus both outputs equal sigma_u. The diagonal coupling of sigma_u with itself has cost zero, so W_p(Rmu,Rnu) = 0.

**Input distance.** Any coupling of delta_u with delta_(-u) puts full mass at (u,-u), because both marginals are point masses. Therefore

    W_p(mu,nu)^p = d(u,-u)^p = pi^p,
    W_p(mu,nu) = pi.

A finite reverse constant would imply pi <= C(p,n) * 0 = 0. This contradiction proves the negative result for every finite p in the source's range, in every source-relevant dimension. It does not use spectral asymptotics, approximation, numerical evidence, or the strengthened even-density theorem.

The dual map itself remains a probability map: F preserves nonnegativity and F1 = 1. Thus Rmu is nonnegative with mass one. There is no hidden failure of output admissibility.

## 3. Why symmetry of the kernel is not an input restriction

Let A(x) = -x. The two distinct kernel symmetries give useful independent checks:

* E(-u) = E(u) gives Ff(-u) = Ff(u), hence R(A_#mu) = Rmu.
* Each equator is itself antipodally symmetric, hence F(f composed with A) = Ff and A_#(Rmu) = Rmu.

Consequently Rmu depends only on (mu + A_#mu)/2. These are properties of the stated map; they do not restrict its domain to even measures. Nor does the fact that a hyperplane has two opposite normals replace the source's spherical transport metric with a projective metric.

For further reproduction of the frozen proof's regularity check, let sigma be normalized spherical measure and 0 < a < 1. Define mu_plus = (1+a x_1)sigma and mu_minus = (1-a x_1)sigma. Reflection gives integral x_1 d sigma = 0, so both densities normalize to one and remain at least 1-a. They are distinct smooth positive probabilities, with mu_minus = A_#mu_plus and therefore equal transforms.

The coordinate function x_1 is 1-Lipschitz for intrinsic distance: |x_1-y_1| <= |x-y| = 2 sin(d(x,y)/2) <= d(x,y). Rotational symmetry and sum_j x_j^2 = 1 give integral x_1^2 d sigma = 1/n. Hence every coupling satisfies

    integral d(x,y) dgamma >= integral x_1 d(mu_plus-mu_minus)
                            = 2a/n,

so W_1(mu_plus,mu_minus) >= 2a/n > 0. Even requiring smooth positive densities, without evenness, would not remove the counterexample mechanism.

## 4. Boundary and adversarial checks

| Candidate hidden assumption or boundary | Check and outcome |
|---|---|
| Even input measures | Not imposed in the complete Stephens contribution. The frozen note correctly treats the even theorem as a separate strengthened variant. |
| Projective sphere or quotient distance | Not the stated domain or cost. The source uses the sphere and product sphere; intrinsic antipodal distance is pi. Quotient identification would change the problem. |
| Densities only, or atoms excluded | Contradicted by explicit probability notation and moving-delta examples. Even a smooth-positive repair without evenness still fails, as reproduced above. |
| Hemisphere, cap, or other support restriction | None appears. Such restrictions might require different analysis but cannot invalidate a counterexample in the actual unrestricted class. |
| n >= 3 | The source's forward-constant denominator contains integral_0^(pi/2) sin(t)^(n-3) dt, finite only for integer n >= 3. This supports the conventional setting. The source does not explicitly write a lower dimension bound in its contribution. The antipodal proof applies throughout that setting. |
| n = 2 | Natural normalized 0-dimensional equator averaging is well defined and Theorem 1 remains true. The source's displayed strict forward-contraction formula is not literally defined here: both improper integrals diverge. The frozen proof correctly identifies this as a boundary extension. |
| n = 1 | E(u) is empty; normalized equator measure and this R are undefined. The frozen proof makes no assertion here. |
| p = infinity | Outside the source's defined range. For the usual essential-supremum transport metric, the unique antipodal coupling still has cost pi and identical outputs have cost zero. The frozen proof labels this as an extension, not a source-range claim. |

The even circle claim is also directly checkable. If J is rotation by pi/2, then

    Rmu = (J_#mu + (-J)_#mu)/2.

For even mu, (-J)_#mu = J_#(A_#mu) = J_#mu, so Rmu = J_#mu. Pushing couplings forward by J x J, and back by its inverse, preserves every cost, including the essential supremum. Thus R is an isometry on even circle probabilities for 1 <= p <= infinity. This confirms why an even-only circle question has a different answer.

## 5. Findings, gap, and publication scope

**Mathematical finding:** Theorem 1 exactly answers the literal source question. Its minimal proof is complete and independently reconstructed. It also disproves any unrestricted inverse modulus omega with omega(0) = 0, by the same identical-output example.

**Minor provenance issue (P3):** Frozen `SOURCE_GATE.md` says a catalogue citation marked 2009 conflicts with the report's 2008 title/date. The [official EMS metadata](https://ems.press/journals/owr/articles/2042) identifies the formal report as volume 5 (2008), but dates publication to 30 June 2009. A 2009 label can therefore denote publication year rather than an error. Suggested correction: distinguish the 2008 report/meeting year from the 2009 publication date. This has no effect on the transform, admissible class, or counterexample.

**Exact gap:** None for the literal unrestricted negative result. This audit does not independently certify the n >= 3 even-density construction, its quantitative exponent, a new W_infinity even result, restricted-support formulations, optimal inverse moduli, or historical priority. Those are distinct mathematical or bibliographic tasks. In particular, resolving the literal question does not by itself establish the strengthened even theorem; conversely that theorem is not needed for literal resolution.

**Source interpretation limit:** Absence of a printed even restriction does not establish what the speaker privately intended in 2008. No such undocumented intention is asserted. This report evaluates the publicly checkable literal text.

Only files positively listed in `PUBLISHABLE_MANIFEST.json` are publication candidates. Official PDFs, page renders, and extracted text are ignored and excluded. All work was confined to this audit's `reviews/source_parity/` folder. No external communication was initiated.

Final completion estimate: **100% of the assigned source/parity audit**.

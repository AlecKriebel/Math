# Reverse cross-challenge of the sealed priority audit

PR1261 / problem30003990. Review date: 2026-10-17 UTC. This is a detached review of the other priority family's initial seal, after both initial audits were frozen. It does not modify or replace either initial audit.

**Verdict: the main Totik–Varga Theorem2.1 deduction passes, relative to that named published import.** No blocking mathematical gap was found in the endpoint specialization, positive core, relative normalization, convex-volume transfer, or every-integer degree budget. The attribution distinction also passes: the audit identifies an implication assembled in2026 and does not backdate the final theorem to2012. It provides no firstness, current-openness, or new-method clearance.

Two limited clarifications are recorded below: the elementary fallback's finite small orders should be stated explicitly when that section is used alone, and the publisher-format quadratic-proxy proof is on PDF7/article6, rather than PDF6. Neither changes the main conclusion or its historical attribution.

## Inputs and authentication

The four outside anchors supplied by the parent all matched:

| Frozen manifest | SHA256 |
|---|---|
| priority/independent/MANIFEST.json | fd822340f036e804bb0c350cfe386fb35fa5db1439aa97b7e3670ae2bd522686 |
| priority/adversary/MANIFEST.json | 4a9ab52c55cd2ed713e23ddf1846d13ea549ba94efac7012ab7ee5a43178dc89 |
| reviews/spectral_family/MANIFEST.json | 048f4a88d185103dce529fb03197901bbd25f87c0be6946c23b60f201e5a2214 |
| reviews/spectral_adversary/MANIFEST.json | f81be83ca58de26e0929424a4eba7e8cc23bf1903172660c9677d571cb6db563 |

Every member listed by these manifests was authenticated at2026-10-17T21:42:23.335144+00:00:15+29+9+9=62 frozen member occurrences. They were checked again before this cross-challenge seal. This count is byte authentication, not a claim to have read or executed every member.

The other priority family's complete REPORT.md, DERIVATION.md, CLAIM_COMPARISON.md, BIBLIOGRAPHY_QA.md, VERDICT.json and SELF_REVIEW.md were read. Its source inventory and body-reading ledger were checked for scope and missing-body disclosures. The spectral report, internal adversarial review, independent spectral-adversary report, verdicts and primary-inspection records were examined for priority/method framing. Numerical scripts were not run, and their numbers are not newly certified here.

CROSS_CHALLENGE_MANIFEST.json contains exact paths, bytes and SHA256 for the read inputs and primary bodies, the initial outside anchors, the full frozen-member authentication records, and the two detached authored outputs. The manifest's own digest is delivered outside it.

## 1. Exact target and imported endpoint theorem

The audited target remains the normalized Lebesgue hierarchy over globally SOS densities of degree≤2r on each fixed compact full-dimensional convex body, for each fixed polynomial, with O(r^-2) error for every integer r≥1. An existence construction using a minimizer and one global square is sufficient. The main deduction does not assert an arbitrary-reference-measure theorem, an efficient minimizer algorithm, or a general original-objective density restriction s(f).

The actual [Totik–Varga2012 primary PDF](https://www.math.u-szeged.hu/pot/5fdp.pdf) was re-inspected, PDF2–9/printed379–386. The body is285373bytes, SHA256004361b85bbaef05716c7789a108b9b764e3e7789ba22724a029e9ee5429a7a9. Theorem2.1 has no measure assumption. Its specialization was checked as follows.

| Hypothesis or interface | Check |
|---|---|
| psi nonnegative and increasing on[0,infinity) | psi(v)=sqrt(v) satisfies both |
| psi(0+)=0 | Direct limit |
| psi(v)≤M0 psi(v/2) | Equality with M0=sqrt2 |
| integral from1 to infinity psi(v)/v² finite | Integral equals2 |
| Endpoint parameter permitted | a=0 belongs to[0,1/2] |
| Correct functional argument | m t/(sqrt(t)+sqrt(a)) becomes m sqrt(t) for t>0 |
| Resulting exponent | psi(m sqrt(t))=(m²t)^(1/4) |
| Degree and uniform bound | Degree≤m; P_m(0)=1; absolute value≤2 on[0,1] |
| Constants independent of order | The printed constants are uniform in m and the allowed parameter |
| Real polynomial | The printed construction is real; taking the real part would also preserve the needed bounds and value |

At t=0 the displayed argument need not be evaluated as0/0: the separate statement P_m(0)=1 is used. No endpoint limiting substitution changes a hypothesis.

The complete printed proof of Theorem2.1 was re-read. It imports older symmetric fast-decrease theory. Neither initial audit obtained the complete Ivanov–Totik1990 body, and this cross-challenge does not claim to reconstruct that dependency. This is ordinary reliance on the stated2012 theorem, not an unproved new endpoint lemma. The elementary fallback also supplies the needed concentration without that import.

## 2. Markov core and the relative normalized moment

The other derivation's scalar hypothesis is explicit: a finite nonzero positive measure on[0,1], positive cumulative mass F(h), and F(t)≤A(t/s)^D F(s) for0<s≤t, with F extended constantly beyond1. Constants A,D are fixed in the order.

The Markov factor on[0,1] is2m², so the bound |P_m|≤2 gives |P_m'|≤4m². With h=1/(8m²), the value at zero gives P_m≥1/2 throughout[0,h]. Thus Z=integral P_m²dmu≥F(h)/4>0. Oscillation or zeros outside this core do not threaten normalization.

The core numerator is at most4hF(h). On the jth shell(2^j h,2^(j+1)h], the three factors are bounded by2^(j+1)h, C²exp[-2c8^(-1/4)2^(j/4)], and A2^((j+1)D)F(h). Their product has exactly the other derivation's form. The shell series has ratio tending to zero for every fixed D. Its constants therefore do not grow with m and introduce no hidden logarithm.

The same F(h) occurs in the upper numerator estimate and the lower denominator estimate. It cancels legitimately. A total-mass bound in the numerator divided by an absolute small-core estimate would not suffice; that is not the argument used here. The extended cumulative distribution handles an outer shell whose right endpoint exceeds1. Empty shells are harmless. No absolute continuity, orthogonal-polynomial regularity, or interval-doubling assumption enters this proof.

## 3. Convex-body transfer and every integer order

At a minimizer a, the directional derivative along each feasible segment gives ell(x)=gradient f(a)·(x−a)≥0. Taylor's theorem and the chosen positive quadratic coefficient give0≤f−f(a)≤g. This uses convexity of K and bounded Hessian on K; f itself need not be convex. The added positive quadratic term ensures G=maxKg>0 even for a constant objective.

For u=g/G, contraction about a gives g(a+alpha(x−a))≤alpha g(x),0≤alpha≤1. Consequently the homothety with alpha=s/t injects the level set{u≤t} into{u≤s}, with determinant(s/t)^n. This proves F(t)≤(t/s)^nF(s), including t>1. It also proves F(s)≥s^n vol(K)>0 for0<s≤1. Thus every scalar-measure hypothesis is supplied by the actual Lebesgue pushforward, without a density formula.

For r≥2, m=floor(r/2) is at least1,2m≤r, and m≥r/3. The normalized witness P_m(u)² has square-root degree≤2m, total degree≤4m≤2r, and unit mass. Its positive normalizing constant can be absorbed into the polynomial square root. This is one square on all of R^n; no positivity theorem on K is being substituted for global SOS. For r=1, constant density has error≤G and is included by enlarging the constant. The lower bound follows from pointwise f≥minf and q≥0.

These checks establish the precise all-integer target in SectionsA–C of the other derivation. Normalizing Lebesgue measure rather than the density merely rescales the density by vol(K) and leaves the hierarchy value unchanged.

## 4. Standalone elementary fallback: explicit finite-order completion

SectionD's trigonometric identity and bounds are correct. With N=2m+1 and t=sin²v, its A_m equals sin(Nv)/(N sinv). The bound by1 follows from the finite sum, and the envelope1/(N sqrt(t)) follows from the numerator bound. For t≤N^-2, convexity of arcsin gives Nv≤pi/2. Hence sin(Nv)/(Nv)≥2/pi and v/sinv≥1, proving the claimed positive core. The shell sum converges when the fixed integer L>D+1.

When using SectionD alone, say explicitly that m=floor(r/(2L)) is used only for r≥2L. Then m≥r/(4L),2mL≤r, and the moment bound C/m² becomes at most16L²C/r². For1≤r<2L use constant density and enlarge the target constant by at most(2L−1)²G. This completes the standalone fallback at every order.

The main theorem is already covered by SectionsA–C. This clarification prevents an undefined m=0 substitution in the separately stated fallback; it is not a failure of that theorem.

## 5. Attribution and bibliography challenge

The other's distinction between an earlier printed ingredient and a consequence assembled now is supported by its actual derivation. The2012 theorem states endpoint polynomial concentration. The old Christoffel statement minimizes a norm under P(0)=1; it does not itself print the final arbitrary-convex-body normalized objective theorem. The2026 proof supplies the normalized first moment, convex-volume transfer, and degree conversion. No earlier explicit full-target statement was located or newly established by this cross-challenge.

The correction concerning Theorem3.2 is valid. The primary definition permits global doubling only at centers in a set. The set may be{0}; F(2s)≤2^nF(s) verifies the condition there. This gives a genuine endpoint Christoffel upper comparison. It does not turn a bare norm bound into the normalized first-moment bound. Theorems3.1/4.1 require stronger interval conditions. The other derivation's valley-weight counterexample correctly refutes the generic cumulative-to-interval implication; it is expressly not claimed to be a convex-quadratic pushforward.

The [final Totik2012 survey](https://doi.org/10.1090/conm/578/11471), printed246/PDF6, was checked directly. Its shell proof compares tails to the same small-core mass and supports the stated older mechanism overlap. It does not supply documentary evidence that the complete target was already recognized.

The prior quadratic proxy is also confirmed directly in the publisher-format2018 annealing paper, Corollary3 and proof. **Correct locator for the retained CWI PDF: one-based PDF7, printed article6.** The cover page creates the offset. The other CLAIM_COMPARISON's “publisher PDF p.6” and its source-inventory pp5–6 range do not locate this proof correctly. The named Corollary3 attribution is right, and the complete proof was verified here. The preprint's Corollary4.3 numbering remains a distinct valid locator.

The publisher-format worst-case paper was checked at its Jacobi definitions and Theorem4/Corollary2, PDF6–8. Alpha=beta=0 gives Lebesgue measure and the linear interval objective. It supports existing worst-case Theta(r^-2), not a positive lower rate for every f. The version/issue/internal-date distinctions and missing-body disclosures in the other bibliography are appropriate; no older discovery date is inferred from them.

Kroo2015 in this family's initial audit and Kroo2016 in the other are different papers. Both missing-body limitations remain. The other audit's2025-online/2026-issue homogeneous-Christoffel paper was checked at the captured opening, central-symmetry/homogeneity assumptions and theorem interfaces. Its comparison remains scope-limited; no exclusion of all possible consequences of its unread proof collection is made.

## 6. Spectral route: priority and method framing only

The authenticated spectral reports provide a different bridge: a quadratic pushforward is proved to have full local interval doubling through central projection and origin-polar density comparisons, followed by the upper part of Totik–Varga Theorem3.1, Gaussian quadrature/cardinal estimates and a compressed multiplication eigenvector. The independent spectral adversary explicitly validated this geometric bridge and its degree/indexing interfaces. This cross-challenge examined those arguments for framing; it does not replace that independent mathematical review or certify numerical experiments.

The generic cumulative-to-interval shortcut being false is compatible with the special spectral lemma. The spectral proof supplies extra geometric information, rather than inferring full doubling from the cumulative inequality alone. Thus the priority audit's “blocked” label should be read as applying to that unsupported shortcut, not as invalidating the now-validated special spectral route.

| Route | Older import / substantial overlap | Additional application-specific bridge | Priority disposition |
|---|---|---|---|
| Explicit endpoint polynomial | Totik–Varga Th2.1, Markov, shell/core comparison | Convex homothety and normalized first moment | Valid2026 assembly; earlier printed full target not located |
| Endpoint Christoffel upper at center0 | Totik–Varga Th3.2 | Still needs suitable normalized-moment construction | Bare norm substitution blocked; main endpoint proof supplies control |
| Spectral | Totik–Varga Th3.1, Christoffel/orthogonal-zero/eigenvalue machinery | Full local doubling for the specially chosen quadratic pushforward | Independently validated route; historical novelty of the geometric lemma undetermined |

The proxy and the broad classical spectral/kernel machinery should receive prior credit. Conversely, classical overlap alone is not proof that every detailed geometric bridge was already printed. Describing a geometric lemma as proved in this derivation is justified; describing it as historically new, or the whole route as a new method, is not cleared by these finite audits. Neither spectral report claims a priority clearance.

## 7. Limits, research checkpoints, and disposition

No fresh web search or HTTP retrieval was performed in this cross-challenge. Existing primary bodies and retained metadata were inspected; the original search counts are not increased. Bibliography checks are tied to the stated retained bodies and scopes, not a fresh exhaustive citation search. No new explicit full-target historical match was found. Missing bodies, unindexed work and uninspected proof sections remain possible.

Research checkpoints: at2026-10-17T21:42:23.335144+00:00 the62 frozen member occurrences authenticated and the main proof comparison was substantially complete, estimated70% of this bounded cross-challenge. At2026-10-17 21:42:47 UTC, primary theorem and bibliography/interface checks were complete, estimated90%. The final manifest records the completion checkpoint at100% of this assigned cross-challenge. These percentages do not measure the probability of novelty.

No blocking substantive gap remains in the challenged main deduction. The finite-order fallback completion and corrected proxy page locator are supplied in this detached report. No sealed original was edited; no other shard agent was contacted; no external outreach, subdelegation, Git/index/ref/PR/Zenodo/GWS mutation or publication action occurred. The result is a sealed cross-challenge, not final-paper, package, firstness, current-openness or new-method approval.


# Independent final partial-package review: 30003518

**Verdict: PASS for all explicitly scoped partial claims. No mandatory mathematical correction. The original bundled problem remains unsolved after five substantive author turns.**

Reviewed on 2026-10-01. Frozen input manifest SHA-256: `433db8e2bf5f4d068c6081cc871a178caebe11d7a3caf5be621e9ccd84f34d54`. Claim map `PARTIAL_RESULTS.md` SHA-256: `134bb09a508a54456984fa95d06c2ca174854efda6f368b3cf981bbe906bcfef`. All 34 manifest entries were checked and remain unchanged. The reviewer supplied no author lemma or derivation. Prior independent review of the one-step theorem is preserved separately and is not counted as an author turn.

This is an adversarial mathematical/source audit, not human peer review or a novelty certification. The recommended original-target disposition is unsolved, 5/5; automatic exhausted author-budget metadata should remain as history.

## Source identity and constraints

The complete Rendall contribution in [OWR 28/2017](https://ems.press/content/serial-article-files/46689), pp.1775–1776, distinguishes the Altan–Bonnet–Germain model from the François model. The final paragraph asks about the former's kinetic-proofreading module and does not enumerate its strongest simplifying assumptions. Therefore a proof for a precisely stated later core is appropriately recorded as partial, rather than as a solution of every interpretation of that paragraph.

The equations in [Brechmann's 2024 dissertation](https://openscience.ub.uni-mainz.de/bitstreams/a948dbbc-0daf-4167-bfd8-23ab6e574d64/download), Section2.4, equations(2.2)–(2.3), match the Lck-only mass-action chain used here. The rate dictionary is d0=k2; d_i=k_(6+4(i-1)) for i≥1; u_i=k_(3+4i), v_i=k_(4+4i), w_i=k_(5+4i). All are positive and independent unless the shared-rate theorem explicitly identifies them. Bound enzyme contributes to enzyme, receptor, and ligand totals. The terminal C_N has a reset reaction but no further Lck binding. These features are maintained in the reconstruction and exact witness.

The one-step equations and Theorem10 were independently rendered and inspected in the preceding audit. They remain unchanged. The thesis's pre-existing multistationarity and persistence results are credited as background, not used to assume the new certificates' conclusions.

I also checked the [2005 article](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.0030356) and statically inspected the supplied original model XML as data. It contains repeated core constants including LckBinding=10000, LckDebinding=50, and LckPhos=10.4, along with other molecular states and reactions. No XML executable was run. Equal-rate calibration, independently parameterized Lck chains, ZAP-70/protected-state extensions, and the full feedback network are not interchangeable. The author explicitly preserves these distinctions. No biological or clinical conclusion is warranted by this audit.

## 1. The unchanged N=1 theorem

The earlier full scoped PASS still applies to `SINGLE_STEP_CANDIDATE.md`, SHA `fb38e57705eeaf1c08325696905f6101318d6c5df59c2232c0549fca0b934ff3`. Its physical domain is convex and invariant; the unique equilibrium is interior; the averaged Jacobian has zero column sums and a uniformly positive strongly connected edge set supplied by that equilibrium. The time-dependent stochastic-matrix contraction proves global exponential convergence in each fixed class, including boundary initial conditions and unequal receptor/ligand totals. Rate constants may depend on that class. No higher-step assertion follows from it.

## 2. Arbitrary-N scalar reduction

The steady enzyme-complex equations give B_i=a_i e C_i with a_i=u_i/(v_i+w_i), and catalysis flux q_i e C_i with q_i=w_i a_i. Substituting those balances into each unbound complex equation yields exactly the displayed recurrence for p_i(e), including the special terminal denominator d_N.

The functions G and H correctly count bound enzyme and total bound receptor. Thus C0=(Etot-e)/(eG) and W=(Etot-e)H/(eG). The exact physical filter is essential: 0<e<Etot and W<min(Rtot,Mtot). On it every denominator and every reconstructed concentration is positive. The scalar source balance and the successive flux equations recover every original ODE, including free receptor/ligand and enzyme equations by conservation. Conversely every positive equilibrium yields those same identities. This proves a genuine bijection with the filtered roots, not just necessity.

For Q=product_(j=1)^(N-1)(d_j+q_j e), each Qp_i for i<N has degree at most N-1; Qp_N has degree N. Therefore g=QG has degree at most N-1, h=QH has degree at most N, and multiplication by e²g² gives the stated degree bound2N+2. No denominator has a zero on the physical interval. There is no extraneous physical solution caused by this clearing operation, but roots outside the filter are extraneous to the equilibrium question. The all-unit N=1 diagnostic correctly exhibits that distinction.

For completeness, positive totals and rates exclude nonnegative boundary equilibria of this precise chain: e=0 would force every B_i=0 by its balance and contradict Etot>0; r=0 or m=0 would force all C_i=0 from the free-pool reset balance, then all B_i=0, contradicting the corresponding total. With e,r,m>0, C0 cannot be zero, and the positive recurrence propagates positivity through every C_i and B_i. This is not a claim excluding arbitrary boundary omega-limit sets by itself.

## 3. Exact two-step equilibrium and stability certificate

I independently rebuilt the original reaction equations at the supplied positive rational rates and totals, rather than accepting the displayed Jacobian. Eliminating free pools and enzyme gives the same five-dimensional vector field. The scalar equation reduces to the stated degree-six polynomial with the exact listed integer coefficients. All five reconstructed ODE residuals reduce to zero modulo that polynomial, and enzyme conservation is an exact rational identity.

Independent Sturm isolation at rational interval width at most10^-30 confirms six simple real roots, all in(0,8), exhausting the polynomial degree. Rational evaluation of the reconstructed free receptor gives strict signs: roots2,3,6 are physical; roots1,4,5 have negative free receptor and ligand. Every remaining species is strictly positive on each isolating interval. Hence there are exactly three physical positive equilibria. The boundary argument above prevents an unreported nonnegative boundary equilibrium in the class.

For an independent stability computation, I used exact interval matrix powers and Newton trace identities to obtain the characteristic coefficients, followed by regular Routh elimination. This differs from the author's principal-minor enumeration and Hurwitz-determinant computation. At physical roots2 and6 the Routh first-column signs are all positive. At root3 they are positive through the penultimate entry and negative in the last. Every pivot has a strictly determined nonzero sign; there is no zero-row or imaginary-axis exceptional case. The resulting right-half-plane root counts are0,1,0. Thus the first and third physical equilibria are hyperbolic sinks and the middle one is a hyperbolic index-one saddle. The one unstable eigenvalue is real because nonreal roots come in conjugate pairs.

The author gives the correct original conservation-class Jacobian; the scalar equilibrium slope is not used as a substitute. Its stated outward integer enclosures and all exact receipts replay byte-for-byte. The strict equilibrium positivity and hyperbolicity imply persistence of the two sinks under an open perturbation of positive parameters and totals. No quantified neighborhood, complete basin partition, absence of other invariant sets, or calibrated-shared-rate bistability is claimed.

## 4. Shared-rate uniqueness for arbitrary N

The hypotheses identify every unbound reset rate with nu and the association, dissociation, and catalytic rates across steps with u,v,w respectively. Under exactly these restrictions, the geometric parameter s=q e/(nu+q e) lies in(0,1). Summing the finite geometric series, including its special terminal term, gives T=C0/(1-s) and C_N=T s^N. Therefore bound enzyme is a e T(1-s^N), as claimed.

The derivative identity

theta'(e)/a=(1-s)[sum_(j=0)^(N-1)s^j-Ns^N]

is correct and strictly positive, since each of its N summands exceeds s^N. Hence T=(Etot-e)/theta is strictly decreasing, diverges as e decreases to zero, and tends to zero as e increases to Etot. The same assertions hold for W=T+Etot-e. The unique physical threshold beta exists for all positive totals, including equal ones.

On(beta,Etot), both free pools increase strictly. Their product increases strictly, whereas nu T decreases strictly; opposite endpoint signs give exactly one crossing. The turn2 reconstruction supplies sufficiency. The proof is for equilibrium uniqueness only. It cannot be applied to the arbitrary-rate bistable witness, which violates its hypotheses, or to the source's added molecular states.

## 5. The signed-cooperativity obstruction and unresolved dynamics

In the specified retained coordinates, after eliminating only free ligand and free enzyme, the three displayed derivatives around B0→C1→B1→B0 have signs+,+,- at every interior point for N≥2. Their product is strictly negative. Diagonal sign conjugation preserves a directed cycle's sign, so it cannot produce a Metzler matrix. This is a valid no-go for coordinatewise sign switches in that representation, not for arbitrary coordinate changes, other cones, or weighted nonlinear metrics.

The zero-column-sum identity also checks exactly. A bound-enzyme column has a negative off-diagonal entry in every other bound-complex row; its ordinary l1 logarithmic-norm column value is therefore strictly positive. Thus the N=1 stochastic-matrix proof cannot simply be reused. This observation does not demonstrate instability or a nonconvergent trajectory.

The finite numerical scan is explicitly diagnostic. No all-parameter spectral or global statement is deduced from it. Higher-step global dynamics and the broader OWR module remain unresolved, so the final unsolved5/5 disposition is mathematically appropriate.

## Reproducibility and frozen evidence

- All34 frozen input hashes verified unchanged
- Independent checker: **745 exact assertions**, with fresh rational root isolation, original-ODE reconstruction, interval Newton/Routh stability, general-chain controls throughN=10, shared-rate identities throughN=30, and actual negative cycles/column sums throughN=8
- Author reduction197, two-step101, and shared-rate266 exact receipts all replay byte-identically in an isolated copy
- Prior one-step author575 and independent683 controls remain preserved in their original separate review
- No floating-point eigenvalues, numerical scans, or source-provided executable software are used as proof

The first independent checker run stopped only when serializing very large exact fractions; output was changed to outward integer bounds. The exact sign tests had not failed. The final checker and receipt are deterministic and reproducible. All input artifacts remain untouched.

The five substantive research turns are evidenced by their distinct completed arguments; this audit and its computations do not manufacture an extra author attempt. Publication, if authorized, should retain a single partial-result draft with the original target unsolved and all source/model limitations visible.

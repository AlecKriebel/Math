# Analytic adversarial review of PR207 / 5100044

**Verdict:** no mathematical gap or counterexample found in the submitted
proof under its exact hypotheses. I independently reconstructed the universal
argument; finite numerical agreement is supplementary. This verdict concerns
mathematical validity, not publication clearance or historical priority.

**Verified claim:** for a nondegenerate strictly nested confocal elliptical
caustic and billiard ellipse, every primitive family of least period N
divisible by four has constant A A_j^dagger, where both areas are signed
shoelace areas and consecutive inverted original vertices are joined by
straight segments. The reconstruction covers every admissible coprime star
turning number, either original focus, and reversal.

The main checkable artifact is [DERIVATION.md](DERIVATION.md). Its essential
points are:

- The canonical modulus is c/alpha, not c/a; the independent chord equation
  is -sn(u)x/alpha+cn(u)y/beta=1. The canonical coverage and step normalization
  agree with the primary publisher's Stachel Theorem 4.3 / (4.9).
- The cyclic dn sum on the reduced torus has exactly two simple poles and
  two forced simple zeros. At a literal lift p=iK', exactly one summand is
  singular and its residue is -i. This removes any potential ambiguity about
  summand multiplicity after reducing the real lattice.
- The inverse-edge formula follows from real Euclidean distances and two
  direct determinant/distance-product identities. Its meromorphic extension
  does not use complex conjugation. All real denominators are positive or
  bounded away from zero under the hypotheses.
- For V!=0, H=U²-k²V²sn² has precisely the two simple zeros r±delta on the
  smaller torus. The common Jacobi poles are removable zeros of B, while
  dn zeros supply at most simple poles. Reflection changes the sign of the
  double Laurent coefficient and preserves the residue.
- At each lifted cyclic pole, the relevant indices are exactly 0,1,m-1;
  the latter two are distinct for every generic case, including N=8. Their
  double coefficients cancel once each, for every coprime star order.
- V=0 is exactly primitive N=4. Its separate q/dn+t dn decomposition has
  only simple poles; reduced-lattice coalescence does not increase order.
- Residue matching leaves a holomorphic torus function, and anti-periodicity
  forces its constant to be zero. The final half-period shift follows from
  m even and tau odd. Focus exchange and reversal are exact vertex-list
  operations preserving the product.

No mandatory proof repair emerged. An optional clarification would replace
the submitted informal residue-addition wording by the exact residue -i at
the lift p, as in DERIVATION.md Section 3. The existing noncancellation claim
is sufficient for its argument; this clarification avoids a possible
misreading that lattice reduction multiplies residues.

Independent reproducibility is provided by [independent_controls.py](independent_controls.py)
and [independent_output.json](independent_output.json). Invocation:

    /opt/homebrew/bin/python3.11 -E -B -P complex_elliptic_adversary_01/independent_controls.py

The run used Python 3.11.8, SymPy 1.14.0, mpmath 1.3.0 and 100 decimal
digits. Seven exact algebraic identities passed. There were 4,081 finite
cyclic-index controls through N=400, nine direct geometric cases including
N=4, stars, near-circular k=10^-6 and near-degenerate k=0.999999, and four
complex Laurent diagnostics. The largest sampled relative product spread
was below 5e-100. The most sensitive inverse-formula comparison had error
below 4e-91. These are high-precision floating diagnostics, not interval
certificates and not the justification for arbitrary N.

Adversarial boundary controls were informative: a primitive N=6 example and
the same orbit traversed twice with twelve displayed vertices both exhibited
about 2.906% product variation across sampled phases. The analytic derivation
also proves this expected failure outside the parity/least-period conditions.
Thus the hypotheses exclude a real obstruction rather than merely reflecting
a test convention. The N=4 value four and the circle case were independently
checked in closed form.

**Exact remaining gaps:** none found for the mathematical claim just stated.
Hyperbolic or degenerate caustics, limiting extensions, unsigned union areas,
and nonprimitive displayed lengths are outside this validation. Full
literature novelty/priority, publication authorization and a source-edition
audit beyond the analytic input were not assigned here and remain unassessed.

Independence and custody: [FIRST_ASSESSMENT.md](FIRST_ASSESSMENT.md) was sealed
before any reviewer feedback. No other current mathematical review, old
independent_review, submitted checker/output, or neighboring candidate was
read. Only runtime logistics were exchanged with the parent. Original source
files remained read-only. [INPUT_PINS.json](INPUT_PINS.json) pins the five
read inputs and records the supplied native HEAD/tree; [sources/SOURCE_PINS.json](sources/SOURCE_PINS.json)
records primary-source retrievals and the retained publisher HTML hash.
No Git command, service mutation, original/global edit, or external human
communication was performed.

Completion estimate: 100% of this assigned analytic mathematical validation.

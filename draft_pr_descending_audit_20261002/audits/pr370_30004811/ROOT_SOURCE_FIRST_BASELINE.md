# Root primary-source baseline for PR370

This baseline records primary-source reading before reading any candidate proof,
program, output, terminal status, final summary, prior-resolution file, historical
review, or full new-family artifact. Independence qualification: while finishing
PR371, the root received brief unsolicited PR370 sibling summaries reporting a
negative-mass counterexample, its coefficients, and the credited physical-class
equality. Therefore this root baseline is not independent of those brief
findings. The three new reviewers recorded their own source-first and pre-code
mathematical seals independently. Their full artifacts remain unread here.
The root will derive and check the mathematics directly rather than use their
verdicts or test counts as proof. Only frozen file names and source-manifest
URL/size/hash routing fields have been inspected from the candidate so far.

## Claim, conventions and success criteria

The original source is Jauregui's contribution to Oberwolfach Report 40/2021,
printed pages 2255–2258. Printed 2257 conjectures equality of capacity–volume
mass and ADM mass for general asymptotically flat metrics. Its preceding results
and motivation concern nonnegative scalar curvature and empty or minimal
boundary. Jauregui's 2020 paper states the conjecture under its Theorem 6
assumptions explicitly. Treat the physically motivated version and the literal
unrestricted reading separately; a counterexample with negative scalar
curvature somewhere does not disprove the former.

Use normalized capacity cap(K)=(4*pi)^(-1) inf integral |grad phi|^2 dV,
phi=0 on K, phi tending to 1 at infinity. A Euclidean ball has capacity its
radius. The printed OWR prose omits the prefactor, but its displayed inequality,
Euclidean example and the 2020 primary definition fix this convention. The
root visually inspected fresh renders of original PDF pages 100 and 101.

The target mass is the supremum over exhausting bounded sets of limsup of
(3*V/(4*pi))^(1/3)-cap. It is not just the coordinate-ball mass. Jauregui's
Lemma 10 equates this global definition with the cubic normalized definition
(V-(4*pi/3)*cap^3)/(4*pi*cap^2), by reduction to efficient exhaustions; it does
not equate these expressions setwise on arbitrary inefficient sequences.
Benatti–Fogagnolo–Mazzieri's normalized p-capacity and p-isocapacitary mass
specialize at p=2 to that same cubic expression.

For a credited disposition, identify a correct hypothesis-preserving prior
chain for the physical version; do not silently remove topological, boundary,
decay, smoothness, completeness, or sign conditions. For any unrestricted
counterexample verify a smooth positive complete metric, AF decay and ADM
mass, a genuine admissible nested exhaustion, capacity minimization/flux,
volume asymptotics with error control, and a strict inequality in the global
mass. No exact global value or historical novelty follows from a lower bound.

## Primary evidence actually read

Seven fresh primary PDFs match the routed historical byte lengths and hashes.
Fresh copies, extracted text and renders are private. The acquisition receipt
records exact hashes; no source copies are public deliverables.

1. OWR 40/2021: full relevant contribution, PDF99–102; PDF100–101 visually
   inspected. Theorem1 gives mCV>=ADM under scalar curvature nonnegative outside
   a compact set. Theorem2 is an upper bound only along coordinate balls under
   nonnegative scalar curvature and empty/minimal boundary. Theorem3 upper
   bounds global mCV for harmonically flat metrics with nonnegative ADM mass.
   A negative ADM example cannot be excluded by Theorem3.
2. Jauregui 2020, arXiv:2002.08941: PDF1–6, including actual normalized
   definition, AF class, main lower/upper theorems and Lemma10. This gives the
   lower bound for the intended physical class without an H2 restriction.
3. Benatti–Fogagnolo–Mazzieri 2023, arXiv:2305.01453v2: PDF2–5 plus full
   section5 statements and derivations through the proof of Theorem1.3.
   Theorem1.3 additionally assumes H2(M,partial M;Z)=0. Independently,
   Theorem5.6 gives m_p<=miso for C0 AF manifolds with compact possibly empty
   boundary and p in (1,2], without that topology hypothesis. At p=2 this is
   the useful general upper bound. Proof references use an earlier numbering
   of the Penrose paper; locate the actual theorem in the freshly fetched
   version rather than assume its present Theorem4.13 exists.
4. Benatti 2025, arXiv:2511.11155v2: PDF1–9. Proposition3.1 establishes
   m_p<=miso under strong p-nonparabolicity; its proof treats both signs of the
   mass and uses sets containing a fixed compact core. Proposition4.1 gives
   the opposite inequality with nonnegative scalar curvature, minimal boundary,
   no other compact minimal surface, and positive Euclidean isoperimetric
   constant. This is extra context, not permission to drop these assumptions.
5. Jauregui–Lee, arXiv:1602.00732: PDF1–2 and11, exact Theorems3 and17.
   Theorem17 is a quantitative upper bound for outward-minimizing allowable
   regions under empty/minimal boundary, nonnegative scalar curvature, and no
   interior compact minimal surfaces. It is not an unconditional all-AF result.
6. Jauregui–Lee–Unger 2024, arXiv:2408.08871: PDF1–5, including complete
   proof of the all-C0-AF nonnegativity of Huisken mass. Far-out nearly Euclidean
   regions are adjoined to a core to make an exhaustion. This theorem concerns
   isoperimetric mass; do not assert its analogue for capacity mass without proof.
7. BFM Penrose paper, arXiv:2212.10215: exact introduction Theorem1.4 and
   section4.4 proof, including Remark4.13 and the infinite-mass case. Theorem1.4
   identifies miso=ADM for complete C1 AF three-manifolds, decay tau>1/2,
   nonnegative scalar curvature, and possibly empty smooth compact minimal
   boundary, without H2 restriction. This supplies the other half of the
   topology-free chain with BFM2023 Theorem5.6 and Jauregui2020 lower bound.

The strongest credited physical-class chain is therefore
ADM <= mCV = m_2 <= miso = ADM, with the cited hypotheses retained.
The 2023 Theorem1.3 alone is narrower. The original literal statement does not
justify interpreting sign-free equality as already proved by those papers.

## Adversarial checks to perform

Independently derive any smooth negative-mass fill-in and the shifted-ball
capacity, including the sign of the asymptotic potential coefficient. Check
normalization, uniqueness, finite energy, inner versus outer flux and all
large-R remainders. Verify exhaustion containment rather than substitute a
nonexhausting far-out sequence. Distinguish a strict lower bound from the
unknown supremum, and physical prior resolution from any novel unrestricted
counterexample. Audit all public source, proof, code and publication bindings.
No paper or DOI is appropriate if the disposition is credited prior resolution.

Source-baseline phase completion estimate: 20% of this PR acceptance workflow.
The overall discovery estimate has not been assigned from candidate status.

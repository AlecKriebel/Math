# Independent audit of escaping boundary points of Baker domains

## Verdict

Accept this exact packet as an **unsolved five-approach investigation**, with the nonblocking clarifications below. It supplies correct elementary reductions and countermodels to proposed proof mechanisms, together with correctly scoped citations. It does not solve the general problem and does not construct a transcendental-entire counterexample. No substantive mathematical correction to the frozen result is required at that stated scope.

This recommendation applies only to target **30001388 / OWR-4137-004**, rank 615, and to the exact release bound below. It does not transfer to another problem about Newton maps, to later edits, or to a claim of mathematical novelty.

## Exact release binding and audit scope

- Input `MANIFEST.json` SHA-256: `5f04dcc149f26a7cab938e0fdf5c649e56230667eab8c0f75ebd5c34ea67f1ad`
- Input `RESULT.md` SHA-256: `5699d79746744620edc6a428d9a8b9afe060f42c7c1fabdb5b851d4e34036ebc`
- Input result length: 16,694 bytes
- Release manifest version: 1; stated freeze time: 2026-10-04 12:38 UTC
- Review date: 4 October 2026

All nine files enumerated by the input manifest were checked against both their declared lengths and hashes. All passed. All seven consulted source PDFs matched the input source-register hashes and lengths. Their text was independently re-extracted for this review. The original verification script was inspected and rerun; its output matched the frozen result byte-for-byte. `input-verification.json` records these checks without redistributing the source documents.

Every proof and asserted deduction in `RESULT.md` was checked. Relevant original-source statements and surrounding arguments were read, including the source problem, the measure theorems, the explicit entire model, and the recent conditional results. The original OWR problem page, the explicit inner-function formula, and the 2026 expansion definition were also inspected visually. This is a proof audit of the author-created packet and a source-hypothesis check, not a new independent proof of every cited external theorem.

The author packet was not modified. This separate audit contains no source PDFs, source-page images, extracted full texts, research corpora, or private coordination material. It makes no remote changes. Prior-repository searches and historical work-accounting assertions in the readiness files were not independently rerun; the mathematical assessment does not rely on those claims. Five substantive approach families are present. Calling these 5/5 records work accounting, not five independent reviews or a quantitative probability of resolution.

## 1 The problem and source hypotheses

The source-correct problem concerns a **transcendental entire** function f and a periodic Fatou component U contained in I(f). The required conclusion is a finite point of ∂U whose complete forward orbit tends to infinity. An infinite prime-end impression, an unbounded orbit, a point in a different Julia-set component, or the point infinity itself is insufficient.

Rippon's contribution begins on printed p. 2953 with the transcendental-entire assumption; the open periodic-component case is stated on p. 2954. Thus the packet correctly restores context omitted by a short catalogue statement. The 2025 survey restates the question explicitly as Question 6.40. These checks support the packet's bounded literature claim. They are not an exhaustive certificate that no later or unindexed resolution exists. [OWR](https://doi.org/10.4171/owr/2009/54), [BR](https://arxiv.org/abs/2507.11370)

### Period reduction

The proof of I(f^p) = I(f) is sound. Escape of the full orbit implies escape of the p-step orbit. Conversely, failure of full escape supplies infinitely many orbit terms in one fixed disk. A residue class modulo p occurs infinitely often. It cannot be residue zero if the p-step orbit escapes. A convergent subsequence in a nonzero residue class, followed by the finite entire iterate f^(p−j), contradicts escape of the next p-step terms. Compactness is used in the finite plane, not at the essential singularity.

The invariant-domain boundary statement F(∂U) ⊆ ∂U, for F=f^p, is also correct. Continuity gives F(∂U) ⊆ cl(U). Boundary points belong to the Julia set, and forward invariance of that set rules out F(z) being in U. The proof uses finite-valued continuity, which is available for entire F. It does not justify an analogous assertion at a pole of a rational or meromorphic model.

An optional expository addition is that periodic Fatou components of transcendental entire functions are simply connected, so the later disk uniformization has its usual hypotheses. This standard fact is also noted in the cited sources; the packet does not use a disk uniformization for an arbitrary multiply connected meromorphic Baker domain.

## 2 Harmonic measure and growth

The cited positive results have been accurately delimited. Rippon–Stallard Theorem 1.1 applies to univalent Baker domains, with univalence of the return map in the periodic case. Barański–Fagella–Jarque–Karpińska Theorem A applies in the hyperbolic/simply parabolic cases with finite degree, and more generally a nonsingular Denjoy–Wolff point. The type assumption is not erased by the generalization. Theorem B supplies full measure of dense boundary orbits in the finite-degree doubly parabolic case, rather than emptiness of the escaping set. [RS](https://arxiv.org/abs/1411.6999), [BFJK](https://arxiv.org/abs/1511.02897)

### The logarithmic orbit estimate

For x_(n+1)=x_n+exp(−x_n), x_0=0, the substitution y_n=exp(x_n) is exact. Since y_n≥1, the parameter t=1/y_n stays in [0,1]. The inequalities 1+t≤exp(t)≤1+(e−1)t follow from the exponential series and convexity. Multiplication by y_n gives

1 ≤ y_(n+1)−y_n ≤ e−1.

Summing proves 1+n≤y_n≤1+(e−1)n and hence the stated logarithmic bounds. Their order and direction are correct. The upper logarithmic bound makes the reciprocal-square-root series divergent; for sufficiently large n it is bounded below by a positive constant times 1/sqrt(log n). One can even compare to 1/sqrt(n). Discarding the n=0 term with x_0=0 is necessary and is explicitly done. Replacing n by pn gives the same logarithmic conclusion for every fixed iterate.

The packet appropriately describes this calculation as an obstruction **along that orbit**. The growth criterion is existential in the starting point. Divergence at one starting point alone would not prove divergence for all points in U, and the audit does not promote it to such a claim. The known example's boundary measure-zero theorem already rules out using a universally positive-harmonic-measure strategy. There is no inference that a sufficient growth condition is necessary.

### Verification scope clarification

The original script checks sample bounds exp(t)≤1+2t, not the sharper exp(t)≤1+(e−1)t printed in the proof. This is not a flaw in the analytical proof, which is elementary and valid. The verification description can be more precise. The new audit script checks the actual e−1 chord coefficient at 63 interior rational points using exact Taylor enclosures, treats the endpoints as identities, and rejects an invalid extension to t=2. These remain finite controls; convexity proves the statement on the full interval.

### Measure zero is the obstruction, not the answer

The entire model z+exp(−z) has a degree-two doubly parabolic Baker domain, escaping boundary hairs, and zero harmonic measure of the escaping boundary set. Therefore a universal conclusion of *positive* harmonic measure is false even though the original existence question may have a positive answer. The packet keeps these logical levels separate. It neither mistakes full-measure recurrence for recurrence of every boundary point nor mistakes measure zero for emptiness.

## 3 The same inner function and the rational control

### Independent conjugacy check

With C(w)=(w−i)/(w+i), C^−1(ζ)=i(1+ζ)/(1−ζ), and T(w)=w−1/w, direct substitution gives

C ∘ T ∘ C^−1(ζ) = (3ζ²+1)/(ζ²+3).

The identity is valid as a rational identity, with removable or infinite values interpreted as such where appropriate. Its denominator has no zeros in the closed unit disk. The independent check uses Gaussian rational arithmetic rather than the packet's polynomial implementation. It also confirms the useful identities

|ζ²+3|² − |3ζ²+1|² = 8(1−|ζ|⁴),

g(ζ)−ζ = (1−ζ)³/(ζ²+3).

The first checks disk/circle preservation and the second the triple fixed-point equation at 1. A sign change to w+1/w fails the comparison already at ζ=0. Thus the equality is not merely a resemblance between two parabolic models.

The normalized formula in Fagella–Jové §6, p. 32 of the consulted version, is exactly this g, with φ(0)=0 and φ((−1,1))=R. Theorems A and C establish the stated escaping hairs and inaccessibility for the entire realization; the paragraph before Proposition 4.4 supplies the boundary membership of the horizontal lines used later. These are cited results, not consequences of the Cayley algebra. [FJ](https://arxiv.org/abs/2202.04969v5)

### Escape inside the upper half-plane

For w in H, Im T(w)=Im(w)(1+1/|w|²)>0. On the imaginary axis, y_(n+1)=y_n+1/y_n and

y_(n+1)²−y_n²=2+1/y_n²≥2.

The orbit from i consequently has height tending to infinity. Schwarz–Pick bounds the hyperbolic distance between its nth iterate and that of any fixed w in H by the initial distance. In H this bounds the ratio of imaginary parts above and below. Thus every orbit in H tends to infinity. The fact that hyperbolic distance is contracted, rather than Euclidean distance, is used correctly.

### Exactly which real orbits do not escape

For an orbit that remains finite and avoids the pole at every time, eventual |x_n|>1 would imply |x_(n+1)|=|x_n|−1/|x_n|<|x_n|. Such an eventually decreasing nonnegative sequence cannot tend to infinity. This proves the stated nonescape result for all-defined real orbits. It does not prove boundedness of every such orbit, and the packet does not claim that stronger conclusion.

The qualification is essential. Under the rational map's **spherical** extension, 1→0→∞→∞ is a finite-starting orbit converging to infinity. In disk coordinates this corresponds to C(1)→−1→1→1. Therefore no unqualified assertion that *every finite real starting point of the spherical rational map is nonescaping* is valid. The body of the frozen packet already excludes pole-hitting orbits. A clearer subsection title would be “The rational model has no escaping pole-avoiding real orbit.”

The equivalent disk statement follows: if a circle orbit approaches 1 without ever reaching it, Cayley inversion gives a pole-avoiding finite real T-orbit tending to infinity, which was just ruled out. Preimages of 1 are exactly the exception already allowed. Nothing here makes H a transcendental-entire Baker domain. It is a rational parabolic model and is used only to test the proposed mechanism.

### What the comparison establishes

The same abstract inner function, coupled only with interior escape, cannot supply the missing physical boundary conclusion. The conformal embedding matters. In the entire example, all finite escaping boundary points are inaccessible from U, so a strategy that selects finite radial limits alone omits the very set needed. Conversely, the Möbius embedding of H has a very different boundary extension and a finite pole in the dynamical map.

One should write φ* or specify a boundary extension before using an expression such as φ(g^n(ζ)) for ζ on the circle. In general φ itself is defined only on the open disk. Even a radial value φ*(1)=∞ does not control arbitrary boundary sequences converging to 1. The packet's warning about this missing control is correct; its displayed discussion is conceptual, not a claimed extension theorem.

A source-level caution found during visual checking: the consulted FJ p. 32 prints a derivative expression inconsistent with its immediately preceding g. Direct differentiation gives g′(ζ)=16ζ/(ζ²+3)². The packet does not copy or depend on the printed derivative. The modulus on the unit circle agrees with the intended expansion estimate, so this typographical issue supplies no objection to the packet's algebra or cited conclusions.

## 4 Escaping-set components and the topological model

The equivalence

∂U ∩ I(f) ≠ ∅ if and only if the component of I(f) containing U is larger than U

is correct. If x lies in cl(U), then U∪{x} is connected: adding a limit point to a connected set preserves connectedness. When x is also escaping, this connected set witnesses strict enlargement of the escaping-set component. Conversely, if ∂U misses I(f), then U is open and closed in the relative topology of I(f), because cl(U)∩I(f)=U. No connected subset of I(f) that meets U can then also meet its complement.

Connectedness of I(f) is therefore sufficient, using the standard fact that I(f) contains Julia points and hence is larger than the Fatou component U. Unboundedness of its components is insufficient: U is already unbounded. Connectedness after adjoining infinity also need not give a finite boundary point. This is a reformulation and a separation of hypotheses, not a solution to the original question.

The strip/vertical-line model verifies exactly those distinctions. Let S be the real-coordinate set (0,1) together with −1/m and 1+1/m for m≥1. The maximal connected subsets of S are (0,1) and the individual isolated coordinates. Continuous projection by Re forces the components of X_0 to be the strip and the separate vertical lines. Each is unbounded.

The interior of X_0 is the strip. Its closure adds the two lines with real coordinates 0 and 1. Thus its boundary consists of all the displayed external lines and those two limiting lines. X_0∩∂X_0 is dense in ∂X_0 because the external lines approach each limiting line. The strip's finite boundary is nevertheless disjoint from X_0. Finally, adjoining infinity to each constituent preserves connectedness, and all those connected sets share infinity, proving spherical connectedness of their union.

No analytic dynamical realization is supplied or needed for this negative control. It defeats the implication from the listed **topological inputs** alone; it does not refute the entire-function question or establish that actual Baker boundaries can have this configuration.

## 5 Compact coverings and the missing boundary lift

The compact-covering lemma is valid. For each N, the set E_N of points in K_0 obeying all constraints through time N is closed in K_0 by continuity of the finite iterates. It is nonempty by selecting a point in K_N and lifting backward one step at a time using F(K_j)⊇K_(j+1). The E_N form a nested family in one fixed compact set, so their intersection is nonempty. The radial lower bounds give escape at **every sufficiently late time**, not just along a subsequence. Closedness of B is harmless but redundant once all K_n are compact subsets of B and the selected iterates remain in them.

The exact missing construction is the following. For an arbitrary Baker domain U, find one fixed nonempty finite compact K_0⊂∂U and later nonempty compact K_n⊂∂U, with their minimum moduli tending to infinity, such that every y∈K_(n+1) has a preimage x∈K_n under the return map. The preimage must lie on this specified boundary, be finite, and belong to the selected compact set. Forward boundary invariance alone does not supply such preimages. Julia-set blowing-up on a neighborhood does not identify its preimages with points of ∂U. Nor do inverse branches near selected recurrent orbits force a forward orbit with the required radial growth.

Choosing singletons from an already known escaping boundary orbit would satisfy the criterion, so the unrestricted existence of such certificates is itself equivalent to the desired existence assertion. The lemma is useful for testing an actual construction. Stating it without producing the sets does not decrease the general problem's difficulty.

### Discriminating controls for the hypotheses

The packet's Boole-prefix proof is sound: x_0=R+N+2 stays greater than R for N steps since each step above 1 decreases by less than 1. The starting point depends on N and is not held in one finite compact set. The intervals [N,∞) correctly illustrate why nested closedness without compact anchoring does not suffice.

The new controls also reject two tempting weakenings of the lemma:

1. For F(x)=x/2 and K_n={2^n,2^(n+2)}, adjacent image/intersection conditions hold and min K_n→∞. But E_0, E_1, E_2 have cardinalities 2, 1, 0. Pairwise compatibility is not a covering chain. Every actual forward orbit of F converges to zero.
2. For the same F and K_n={2^n}, the reversed inclusions F(K_(n+1))⊇K_n hold exactly. They do not give forward escape.

These are elementary continuous, indeed entire linear, countermodels to weakened certificates; they are not Baker-domain counterexamples.

A second Boole stress test starts at x_0=−1/m in the fixed bounded interval (−1,0). The first image is m−1/m, permitting arbitrarily long large excursions as m increases. Its limiting starting point is the pole zero. Thus boundedness by itself is not compactness within the continuity domain. This does not contradict the lemma, whose continuity and compactness hypotheses exclude that limit failure. Separately, starts in [1,2] must leave the region x>1 in uniformly bounded time, since each such step decreases x² by more than 1.

## 6 Explicit lines, deformations, and transplantation

On Im z=±π, exp(−z)=−exp(−Re z), so the invariant-line recurrence is x_(n+1)=x_n−exp(−x_n). It is strictly decreasing. If it had a finite limit L, continuity would give exp(−L)=0, which is impossible. It therefore tends to minus infinity. With x_0=0, induction gives x_n≤−n. This scalar calculation proves escape; the fact that the lines are in the boundary of the particular U is correctly attributed to FJ rather than inferred from invariance or a plot.

For f_a(z)=z+a+exp(−z), a>0, the threshold x*=−log a is a fixed point of the scalar map on either line. Below it, the displacement a−exp(−x) is negative, and the decreasing orbit remains below its initial point. A finite limit would have to be x*, which is larger than that initial point. Hence such points escape to the left. At the threshold there is a fixed point, emphasizing the importance of the strict inequality. None of this locates the points on a specified Baker boundary after deformation. The packet explicitly preserves that missing step.

For the rational-to-entire attempt, a positively oriented circle about zero gives

∮(h−T) dz = 2πi

for every entire h, since T has residue −1. The length estimate then gives sup_|z|=r |h−T|≥1/r. The sign and normalization are correct; h(z)=z attains the lower bound. Thus uniform approximation on a full enclosing circle is impossible. The argument does not forbid approximation on a suitable one-sided set avoiding the pole, and does not rule out every conceivable entire surgery. The packet makes only the narrower obstruction claim.

## 7 Recent results and why they do not close the gap

Jové's 2024 preprint distinguishes convergence in the Carathéodory topology from ordinary escape. Its Theorem A concerns non-ergodicity/non-recurrence for hyperbolic or simply parabolic domains. Its Theorem B assumes a non-univalent domain and a crosscut neighborhood whose image avoids the postsingular set; its non-Carathéodory conclusion is not a general escaping-point theorem. Theorem D constructs periodic and other boundary behavior under related hypotheses. None supplies the missing universal assertion in this packet. [J](https://arxiv.org/abs/2410.19726v1)

The 2026 Jové–Pawelec preprint has distinct layers. Theorem A assumes a doubly parabolic domain and a nonsingular Denjoy–Wolff point. Theorem B is stated for finite degree, with a one-component-inner-function extension explained in §5.2. Theorems C/D require “expanding” domains. That definition includes the same type/nonsingularity condition, inverse branches on disks of one common radius that preserve the portion lying in U, and derivative expansion there, uniformly strengthened over finite targets. These are substantive restrictions. They are not established for arbitrary Baker domains in the packet. Their inverse-contraction and periodic-point conclusions do not themselves create a radially escaping boundary covering chain. [JP](https://arxiv.org/abs/2605.05184v1)

Current official arXiv records were checked for the cited recent papers and the survey, and focused searches for a general boundary-escape resolution produced no primary-source result overturning the packet's bounded status assessment. This remains a limited review. An unsolved label here means that this investigation has no solution; it must not be converted into an absolute claim about all current literature.

## 8 Corrections and release recommendation

### Required mathematical corrections

None found for the precise claims and explicit qualifications in the frozen result. No general proof or counterexample should be added on the strength of this audit.

### Nonblocking clarifications for a later author revision

- Add “pole-avoiding” or “all-defined” to the heading of the Boole nonescape subsection, matching the already-correct body text. Preserve the spherical prepole exception explicitly when summarizing.
- State exactly that the original exponential control samples use the weaker coefficient 2. Alternatively incorporate the audit's sharper sample checks, while retaining the analytical convexity proof.
- Keep the slow-growth calculation explicitly tied to its chosen orbit unless a further argument is supplied for all points of U.
- Use φ* or another explicitly defined extension in boundary notation, and enumerate the 2026 expansion hypotheses if those results become central to a later argument.
- The immutable input readiness file still says an independent audit is required and publication is not ready. This audit is the external mathematical review; release-process metadata can reference it separately without rewriting the frozen input. This report does not itself publish anything or validate unrelated repository-history checks.

### Recommendation

Retain **unsolved, five substantive approaches used**. The strongest validated output is a set of rigorous obstructions to overreaching arguments, with the boundary-embedding/lifting step left explicit. Accept the packet as research documentation at that scope. Do not present the controls, known entire example, component reformulation, or compactness lemma as a resolution of the general target or as a new theorem about every Baker domain.

## 9 Reproduction and evidence files

`audit_controls.py` is standard-library Python and has no network access or mutation outside its output stream. Run it as follows from this audit directory:

    python3 audit_controls.py > /tmp/baker-audit-controls.json
    cmp /tmp/baker-audit-controls.json audit-controls.json

The independent run passed 145 exact disk conjugacy samples, 81 circle samples, 638 real contraction samples, 64 compact-anchor samples, 12 bounded-near-pole prefix cases, 63 sharp chord interior samples, 16 deformation-displacement samples, two weakened-covering countermodels, and 20 sharp residue controls. It also checks the wrong-sign model and spherical prepole exceptions. Python compilation passed.

`original-controls-replayed.json` is the byte-for-byte replay of the frozen original output. `input-verification.json` binds the input files and source hashes. `MANIFEST.json` binds this separate audit's author-created files. These checks support reproducibility and catch discriminating mistakes; executing them does not establish boundary membership, harmonic measure, an infinite escaping orbit, or the unresolved theorem.

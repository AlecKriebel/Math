# Independent audit of the cellular periodicity partials

Problem 4600046 / AMR-045-0046, 9 October 2026 UTC.

## Verdict

**Accept the mathematical deductions as restricted partial results, subject to the one-line empty-set notation repair below. Do not accept any unrestricted solution or candidate.** The A/B/C full-shift questions remain unresolved by the packet. The shared five-route budget remains exhausted at 5/5. This audit does not introduce a sixth proof route, make a novelty claim, or authorize publication.

The frozen `REPORT.md` has SHA-256 `46482f55f8204eae8a7512549945b2e6f58a3b0f349f22549eff189e1d9f8fc9`, 21,526 bytes. All original files were left unchanged. `INPUT_SNAPSHOT.json` authenticates the complete original packet, and the original manifest and nine inherited input records are independently checked.

There is no substantive counterexample or missing structural hypothesis in the six propositions. There are two audit findings:

1. **Degenerate notation repair, mathematical severity minor.** Section 6 permits an arbitrary finite displacement set S, including S=∅. The expression `max(1,max_{s∈S} ||s||∞)` has an undefined inner maximum in that case. Replace it by `max({1} ∪ {||s||∞ : s∈S})`. Empty S is the identity signal rule, so the theorem then applies trivially. The exact one-line patch is in `CORRECTION.patch`; it has not been applied to the frozen report. Applied virtually, it produces a 21,541-byte report with SHA-256 `5421afb8a5d9b617774a8dd1f8f607541e16b4332e328c0430de54d487736692`. A dry run verifies that the patch applies cleanly.
2. **Verification hardening, computational severity material but not a proof defect.** The author's script uses `assert` and unconditionally emits `all_assertions_passed: true`. Under `python -O` and `python -OO`, its mathematical checks disappear. A real zero-inverse mutation is rejected normally but reports that flag as true under both optimization modes. The independent verifier uses explicit exceptions, independent Gaussian elimination and parity union-find solvers, and kills actual mathematical mutants in all three modes. This supplants the weak test certification rather than changing any theorem.

## Model and quantifier audit

- The domain is the full shift over a nonempty finite alphabet and Z^d, d≥2. There is one finite, translation-invariant local rule. No proper SFT, nonuniform rule, or arbitrary-group result is substituted.
- P is the union of Fix(n Z^d). This is equivalent to finite shift orbit: a finite-index stabilizer contains some n Z^d, and containment of n Z^d gives finite index. In dimension ≥2 a single period vector is insufficient.
- A and B preserve the specified quiescent symbol q. C carries no quiescent-symbol hypothesis.
- Onto P allows enlarging the period. It does not demand onto Fix(n Z^d) for every fixed n. The XOR examples exercise precisely this distinction.
- The finite-set argument P-injective ⇒ P-onto ⇒ globally onto is valid in all dimensions. F_q-onto ⇒ globally onto uses density of that particular F_q and closedness of the image. Neither implication supplies the missing general arrows.
- The acceptance here is restricted: A, B, C hold for fixed-control one-successor XOR rules; B and C hold for exposed-vertex-permutive rules. The latter proof does not assert A.

## Proposition 1: exact torus collar criterion

Accepted. Add dummy neighborhood sites so 0 is included and the neighborhood lies in Q_r. Fix y with support in Q_K, and an odd period 2L+1 with L>K+2r. Periodic injectivity makes every torus restriction a bijection, so its inverse x^(L) is well-defined.

If y has a q-finite preimage x, sufficiently large L contains the supports of x and y with the required margin. Every wrapped input near a fundamental-cell seam is q; periodization therefore gives the periodic target. Uniqueness identifies this periodization with x^(L), proving the eventual collar property. The threshold may depend on x and y; no uniform threshold is asserted.

Conversely, extend x^(L)|Q_L by q. For an output center in Q_(L-r), there is no seam. For a center outside that box, if an input neighbor lies in Q_L, some coordinate has absolute value greater than L-2r; that neighbor is in the stated collar. Every input is q, and the output is q. The target is also q there because K<L-2r. This includes output centers outside Q_L. Thus the finite extension maps to y.

The statement uses a sufficient 2r collar; no claim that this is minimal is needed. In particular, the thin-collar negative control in the audit concerns the *general fibre patching claim*, not a claimed optimality of Proposition 1. The proof does not show that any collar actually exists from periodic injectivity alone.

## Proposition 2: ternary marker inverse

Accepted. The displayed d-dimensional rule is exactly the one-dimensional source rule applied independently along e_1-lines. A site's input equals 2 if and only if its output does, so a finite non-2 support is fixed exactly, not merely bounded. Each finite run is solved uniquely from its right end. This gives an actual F_2 bijection.

The two target segments y_m and z_m agree on Q_(m-1), while their finite inverse values at the origin are respectively 0 and 1. Both target sequences converge to the same infinite horizontal zero line in a 2-background; their preimages converge to distinct limits. This proves failure of uniform continuity and failure of a continuous extension to X.

Important distinction: the inverse is continuous *at each point of F_2*. A fixed target has a right-hand marker at finite distance on each relevant line, so a sufficiently large finite window determines the inverse on a prescribed finite window. The packet does not claim otherwise. Its obstruction is uniform continuity across all finite targets.

For q=0, a single 1 cannot have a finite preimage. No preimage site may be 2, since markers are preserved. On the affected line the finite XOR output has even total parity, contradicting the odd target. The argument retains the declared q; it does not identify F_0 with F_2. This is not a B counterexample, because the same rule is current-site-permutive at an exposed point and Proposition 6 gives periodic lifts.

## Proposition 3: the fixed-fibre boundary bound

Accepted, with its explicitly declared Garden-of-Eden dependency. Global surjectivity implies pre-injectivity. If two preimages of the same y agree on Q_L minus Q_(L-2r), patch one into the other on Q_L. Every neighborhood entirely inside or outside the cube has the correct output. A crossing neighborhood has a coordinate whose center lies beyond L-r in absolute value, and every point of that neighborhood inside Q_L is beyond L-2r in that coordinate. Those inputs agree. The patched configuration therefore has image y and differs from the original only finitely; pre-injectivity forces equality.

Consequently the boundary restriction is injective on *patterns actually occurring in this fixed fibre*. It is not a claim that arbitrary boundary assignments occur, nor a finite cardinality assertion about the entire fibre. For an n-periodic y, grouping n-blocks makes the fibre a nonempty SFT, and the bound on boxes gives log pattern count O(L^(d-1)); dividing by volume proves zero entropy. There is no deduction of a periodic point.

A concrete failure of reducing the general patching collar to r is checked: let f(x)_(i,j)=x_(i-1,j)+x_(i+1,j) over F_2. Both the zero configuration and x'_(i,j)=1 exactly when j=0 and i is odd map to zero. They agree on the outer one-cell collar of Q_2. Patching x'|Q_2 into zero produces nonzero outputs at (±2,0). Thus a width-r collar cannot replace width 2r in this proof.

## Lemma 4.1: universal XOR surjectivity criterion

Accepted with the control-preservation quantifier intact. For every fixed control c, each active vertex contributes the equation b_v+b_successor=t_v. A finite directed cycle, including a one-vertex loop, forces even target parity. Because F preserves c exactly, a target retaining this c and violating parity cannot be rescued by another control layer. This proves necessity over all controls.

For sufficiency, first exclude loops and directed two-cycles. Only then pass to the simple underlying undirected graph: there are no hidden parallel opposite arcs. Any undirected cycle of length at least three requires one tail for each edge; outdegree at most one forces every vertex to send an edge along that cycle, hence a directed cycle. Thus each weak component is an undirected tree.

A tree component has at most one inactive vertex. On the finite path between two hypothetical inactive vertices, the first and last path edges would point toward opposite endpoints. Somewhere a vertex would need two outgoing path edges. If an inactive vertex exists, assign its bit from its terminal equation. Otherwise choose a root and assign an arbitrary bit. One may choose roots by the first vertex in a fixed enumeration of Z^d, so countably many components cause no issue.

For every other vertex there is a unique finite path to the root. Propagating the edge equations on that path defines its bit. Infinite incoming trees and infinite forward rays do not require an initial or terminal point at infinity. Every edge equation holds because its endpoints' root paths differ by that edge. This is a genuine global existence proof, not a finite-graph approximation.

## Proposition 4: winding, order and enlarged periods

Accepted after the empty-S radius notation repair. For an n-periodic control, each base quotient cycle has length ℓ≤n^d. Lift one cycle traversal from a chosen vertex. Its displacement Δ lies in n Z^d, say Δ=nk. If k=0, the lift would be an actual finite directed cycle; global surjectivity excludes this. The bound is

`0 < ||k||∞ ≤ ℓ R/n ≤ R n^(d-1) < m`.

Thus k is nonzero modulo m. For m a power of two, its additive order h in (Z/mZ)^d is an even power of two. More explicitly,

`h = lcm_j (m / gcd(m,k_j))`.

A cycle on the mn-torus projects to a base cycle and returns only after h complete traversals, so its length is hℓ. An n-periodic target contributes the same parity on each traversal, regardless of the starting vertex or transverse coset. Its total parity is h times the base parity and hence zero. Finite incoming trees then solve backwards from a solved cycle or terminal vertex. Controls stay unchanged, giving an mn-periodic full configuration.

The hypotheses are sharp for the *given sufficient order argument*. Merely nonzero integer winding is not enough modulo m; merely even m is not enough; and replacing `m>R n^(d-1)` by `m≥R n^(d-1)` is not enough. The independent mutants instantiate these failures. The report does not say the bound is optimal or that powers of two are the only possible successful covers.

The author's experiment chooses the smaller instance-dependent bound m>max_cycle ||k||∞. That is valid by the same proof, although it is not a test of the stated worst-case bound. The audit also explicitly checks the theorem's bound on the 2×2 experiments, using m=4 instead of the author's maximum m=2.

## Proposition 5: periodic injectivity and the actual q

Accepted. Periodic injectivity implies global surjectivity by the elementary torus argument, hence no finite directed control cycle. For any constant control c_0, translation covariance makes activity either everywhere or nowhere. If it were everywhere, all-zero and all-one signal layers would have the same zero output on that control. These are distinct period-one configurations. Thus the constant control is inactive.

For a q-finite target with q=(c_0,β_0), finite local dependence makes the active set finite. A forward active path cannot repeat and cannot remain in a finite active set forever; it reaches an inactive terminal. Solve with b_v=t_v at all inactive sites and recurse backwards on the finite active set. Outside that active set and the target's finite deviation support, b_v=β_0. Hence the preimage is genuinely q-finite.

No substitution β_0=0 is legitimate. In shifted signal variables δ_v=b_v+β_0 and τ_v=t_v+β_0, an active equation is `δ_v+δ_successor=τ_v+β_0`, while an inactive equation is `δ_v=τ_v`. The extra affine term for β_0=1 is why blindly zeroing the background would be wrong. The original proof avoids this error by solving in the actual b,t variables. The audit checks the β_0=1 case on a local control rule whose active vertices point directly to inactive vertices.

Therefore A and C hold in the family, and B follows from F_q-onto ⇒ globally onto. No unrestricted reduction to this family is claimed.

## Proposition 6: transverse quotient and phase

Accepted. A strict exposed vertex of a finite integer neighborhood admits a rational separating functional, then an integral one, then a primitive one by dividing the coefficient gcd. For a singleton neighborhood one may simply choose a primitive nonzero functional. Primitivity gives a basis of ker λ and a vector mapped to 1; together they form a unimodular basis. Consequently n times the new coordinate lattice is exactly n Z^d, so the transformed target retains n-periodicity in every direction.

After quotienting the transverse directions by n, the alphabet B has cardinality |A|^(n^(d-1)). All non-top inputs have strictly lower longitudinal height. Fixing those lower slices, the input coordinate at p runs over the top slice through one fixed transverse translation, a bijection of the transverse torus. Its alphabet permutation acts independently at every output coordinate, so the whole top-slice map is a permutation of B. Individual permutivity without a unique highest point would not justify this statement.

An explicit indexing convention removes any hidden phase issue. Let the stored slices be u_k through u_(k+w-1), where w=b-a. They determine all lower inputs for the output at height k-a. Top-slice permutivity uniquely solves for u_(k+w). Store also the phase `(k-a) mod n`; then move to k+1 and increment the phase. This is a total self-map on n|B|^w states. Any finite total self-map has a directed cycle. Its length T is at most the state count, and returning the stored phase forces n|T.

Repeating the cycle yields a bi-infinite input satisfying every output equation at the correct absolute phase, including when a and b are nonzero or negative. The output phase at a cycle's first state supplies its absolute alignment. The construction gives n-periods in every transverse basis direction and a T-period in the remaining direction, so the stabilizer has finite index in Z^d. This is strong spatial periodicity. It need not be period n in the original axes; since n|T, period T in all original axes is one available common choice.

When w=0, strict exposedness forces a singleton neighborhood. Invert the alphabet permutation and its spatial translation directly; the input remains n-periodic. Singleton alphabets are also harmless. No Garden-of-Eden theorem, closing theorem, group-CA result, or unproved surjectivity of an arbitrary transverse quotient is used.

## Source and theorem dependencies

The reused source PDF is Jarkko Kari's *Cellular Automata*, Spring 2026, public URL:

https://users.utu.fi/jkari/wp-content/uploads/sites/1251/2026/02/fullnotes.pdf

Its local authenticated PDF is 1,332,765 bytes, SHA-256 `f75bb1abe3102afe2d2e3e32fb6a2a69d441034c0b8224e9c40b2e4793e22bb9`. The recorded retrieval is 9 October 2026 at 00:42:31 UTC. This audit reused that frozen source rather than pretending to perform a new download.

Actually inspected: Figure 9, printed p.18 (PDF p.20), and printed p.31 (PDF p.33), visually; §2.4, printed pp.25–29, including Propositions 15, 16, 18 and Corollary 19, in extracted text; Proposition 18, printed p.29 (PDF p.31), additionally as a newly rendered page; Example 11, printed p.33 (PDF p.35), in text and as a newly rendered page. The source's r/2 radius in Proposition 18 was verified visually rather than misreading the text extraction as 2r.

Only the surjective ⇒ pre-injective direction is needed for Proposition 3 and the general finite-inverse discussion. The notes prove it by replaceable equal-image patterns and a volume-versus-boundary count. Their elementary Lemma 12 is assigned as homework, but its needed inequality is immediate independently: for s≥2 and fixed n,r,d, put M=s^(n^d). The logarithm of `(M−1)^(k^d)` is `k^d n^d log s + k^d log(1−1/M)`, while that of `s^((kn−2r)^d)` is `k^d n^d log s−O(k^(d−1))`. The strictly negative volume-order term wins for large k. The one-symbol case has no distinct pair and is trivial. This closes the stated elementary proof dependency without taking a source's homework label on trust.

Proposition 2 is proved directly in the report and matches Example 11, so no unstated property of that example is imported. Propositions 1, 4, 5 and 6 need only the elementary arguments checked here. No proof from the unavailable 2014 closing paper, the group-CA paper, Game of Life gadgets, or the Salo blog is a dependency of these partials. Those external results were not silently promoted to general theorems or independently recertified by this audit.

The visual Spring 2026 status evidence supports the inherited report's contemporary unresolved status. This audit does not turn bounded literature inspection into an exhaustive absence certificate.

## Independent verification and limits

`checks/verify_partials.py` uses no assert statements. It checks all frozen packet hashes and the original manifest, then:

- All 700 functional graphs on one through four labeled vertices, including loops and terminals, and all 10,552 binary targets. A parity union-find solver is compared with independent GF(2) elimination.
- All 1,296 terminal/zero/nearest-neighbor routing patterns on a 2×2 base torus. Of these, 425 have only nonzero-winding quotient cycles and 871 are rejected. All 6,800 targets on the accepted patterns lift at the theorem's m=4; 1,632 have an odd base-cycle parity. Rejected patterns get an explicit cycle-specific parity obstruction test.
- Long-step, negative-coordinate, diagonal and three-dimensional stress cases, including a 4,096-vertex enlarged quotient.
- All 729 ternary targets on a 3×2 patch, with independently brute-forced uniqueness on their marker support; expanding-window inverse witnesses; and a nonzero specified signal background.
- 7,928 crossing-neighborhood input incidences for the collar geometry in dimensions one through three, plus the explicit thin-fibre-collar counterexample.
- 239 exposed-vertex periodic lifts, including negative height offsets, dummy inputs, six singleton ternary permutations, and a nontrivial unimodular functional λ=(2,3). Absolute target alignment is checked by applying the actual local rule to every site of the resulting period. A co-highest-input singularity is a negative control.

`checks/run_suite.py` repeats the independent baseline under normal, -O and -OO execution, requires identical outputs, and runs eleven actual mathematical mutants under all three modes. It also checks proof-text tampering and reproduces the author's saved result only on temporary copies. Genuine read-only probes run as actual UID 1000 against a 0555 directory and a 0444 verifier file; attempted new-file and append writes must both raise PermissionError, while the stdout-only verifier must still pass. Machine-readable outcomes are in `runs/SUITE_RESULTS.json`. A separate replay in `checks/verify_readonly_inputs.py` also makes the entire 21-file required input tree read-only in a temporary workspace. All three execution modes pass with baseline-identical output, and both appending to the frozen report and creating a source-side file raise PermissionError as UID 1000. Its source copies are removed after the probe; metadata is in `runs/READONLY_INPUTS.json`.

`checks/verify_correction.py` additionally checks the patch by a nonmutating dry run, tests 274 empty-routing identity targets, and checks six singleton-alphabet exposed-vertex cases. Its output is identical under normal, -O and -OO execution.

These are finite checks of written constructions and their specified hypotheses. They do not certify global surjectivity, periodic injectivity, or finite surjectivity of an arbitrary CA by enumeration. Infinite-graph existence and every universal quantifier are established, where applicable, by the mathematical arguments above.

## Disposition

The intended research status stays **exhausted/noncandidate, 5/5 shared approaches, no unrestricted resolution**. The restricted mathematical work is accepted after the empty-S convention is made explicit. Original source bodies, source images, and private coordination material must not be included in any public patch. No GitHub operation, QUEUE change, external communication, or source-body publication occurred in this audit.

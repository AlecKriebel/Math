# Independent review: 2935 / KP 4.59

**Verdict: PASS_SCOPED_ALGEBRA_AND_COVER_LEMMA.** No required mathematical correction was found. The original topological homology-cobordism question remains unsolved. The artifact constructs neither a cobordism nor a general composite-order obstruction.

Reviewed 2026-09-30 by a separate adversarial AI reviewer (gpt-6-astra, xhigh). This is not human peer review or a novelty certificate.

Frozen PARTIAL_RESULT.md SHA-256:
9ece2d270d92b78b1029c5e59a08c3eedca92135eaa4f8e7f815d6a0ec2f30c8

## 1. Original category and source boundaries

The full [K3 author-source PDF](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf) was consulted at printed p.238, and the corresponding page of the cached primary copy was visually checked. The question expressly concerns topological homology cobordisms. The order231 pair, the prime-power result, the higher-dimensional surgery warning and the nonzero first Betti number of the finite cyclic cover all appear there.

The manuscript retains the nonzero-cover-\(b_1\) assertion as an imported result reported by K3. I did not recover and independently audit the complete original Gilmer–Livingston proof, so no new signature-obstruction certification is supplied by this review.

The full [Doig–Wehrli preprint](https://arxiv.org/abs/1505.06970v1) was read at its introduction, theorem and correction-term argument. Although its title and abstract omit the category adjective, the invariance argument uses Heegaard Floer cobordism maps and smooth four-dimensional input. Its combinatorial boundary formulas do not extend that invariance to arbitrary topological cobordisms. The submitted distinction is essential and correct.

The pair is not even unoriented-homeomorphic, so an orientation convention does not accidentally trivialize the proposed test pair. Integral homology, rather than rational homology alone, is required in the cover and graph arguments.

## 2. Independent linking and homeomorphism calculations

For the explicitly chosen linking convention, an isometry is multiplication by a unit u with
\[
86u^2=53\pmod{231}.
\]
I independently solved this by Chinese remainders. At the three prime factors, the root sets are
\[
u\bmod3\in\{1,2\},\quad
u\bmod7\in\{3,4\},\quad
u\bmod11\in\{1,10\}.
\]
Their eight combinations give exactly the list in the artifact:
10,32,67,109,122,164,199,221.
The example \(86\cdot10^2-53=37\cdot231\) is exact.

The inverse of53 modulo231 is170. The full unoriented homeomorphism orbit is therefore
\(\{53,178,170,61\}\), which excludes86. This is the standard lens-space classification, not merely a homotopy-equivalence or linking-form test.

The reciprocal convention \(q^{-1}/p\) yields an equivalent description after changing the cyclic generators. Isometry existence survives; it is not legitimate to demand that the same numerical unit represent the same abstract map in both generator conventions. The independent code verifies the transformed units.

For \(M=\{(x,10x)\}\), isotropy follows from the displayed congruence. Nonsingularity holds since both53 and86 are units. An explicit orthogonal-complement calculation removes any reliance on counting alone:
\[
53a-86\cdot10b
\equiv86\cdot10(10a-b)\pmod{231}.
\]
The coefficient \(86\cdot10\) is a unit, so orthogonality to the graph generator is equivalent to \(b=10a\). Thus \(M^\perp=M\). Its two projections are isomorphisms. This is the graph-shaped metabolizer consistent with integral homology cobordism, but it is no realization theorem.

## 3. The finite cyclic cover

Let W be a hypothetical connected oriented topological integral homology cobordism, and let V be its connected cover induced by abelianization onto \(\mathbb Z/p\). Each boundary fundamental group is itself \(\mathbb Z/p\), and its composite into \(H_1(W)\) is an isomorphism. The restricted cover is consequently the connected universal cover of each lens space. Hence the boundary has exactly two components, both \(S^3\).

Finite covering multiplicativity gives \(\chi(V)=p\chi(W)=0\). The homology cobordism assumption supplies \(\chi(W)=0\). These statements apply to compact topological manifolds using their finite homotopy type; no smooth triangulation is being assumed.

In the long exact sequence with rational coefficients, \(H_1(\partial V)=0\), while the map \(H_0(\partial V)\to H_0(V)\) has one-dimensional kernel. Therefore
\[
0\to H_1(V)\to H_1(V,\partial V)\to\mathbb Q\to0.
\]
Poincaré–Lefschetz duality gives \(b_3=b_1+1\), and Euler characteristic gives \(b_2=2b_1\). Both formulas are correct. Combining them with the separately credited source restriction \(b_1>0\) gives the two stated lower bounds, without silently re-proving that restriction.

## 4. Conditional cyclic-\(\pi_1\) h-cobordism lemma

Assume additionally \(\pi_1(W)=\mathbb Z/p\). Then V is the universal cover and is simply connected. Thus \(H_1(V;\mathbb Z)=0\) and \(b_2(V)=0\).

The integral universal coefficient theorem identifies \(H^2(V;\mathbb Z)\) with \(\operatorname{Hom}(H_2(V;\mathbb Z),\mathbb Z)\). Poincaré–Lefschetz duality and \(H_2(\partial V)=H_1(\partial V)=0\) identify that group with \(H_2(V;\mathbb Z)\). It follows that \(H_2(V;\mathbb Z)\) is torsion-free; its zero rational rank then forces it to vanish.

For clarity, the remaining integral \(H_3\) statement also follows exactly. The relative fundamental class maps
\[
H_4(V,\partial V)\cong\mathbb Z\longrightarrow
H_3(\partial V)\cong\mathbb Z^2
\]
to the two boundary fundamental classes with coefficients of absolute value one. Its image is primitive. Since \(H_3(V,\partial V)\cong H^1(V)=0\), the cokernel is \(H_3(V)\cong\mathbb Z\), and either boundary component maps isomorphically to it. Together with connectedness and the vanishing of \(H_1,H_2,H_4\), each boundary inclusion is an integral homology equivalence.

The spaces have CW homotopy type and are simply connected, so the homological Whitehead theorem makes each lifted \(S^3\to V\) a homotopy equivalence. Downstairs, each boundary map induces an isomorphism on \(\pi_1\), since its abelianization is an isomorphism between cyclic groups of order p. The universal-cover equivalence then gives isomorphisms on all higher homotopy groups. Whitehead's theorem yields homotopy equivalences downstairs. Thus W is indeed an h-cobordism.

This proves exactly the conditional statement in the artifact. It does not make W a product, construct W, or permit importing a high-dimensional h-/s-cobordism theorem into dimension4. The manuscript correctly avoids those inferences.

## 5. Reproduction and publication scope

The submitted verifier and frozen artifact were copied into an isolated replay directory. All **427,001 assertions** reproduced, with a byte-identical receipt. No author file was edited.

The independent standard-library checker passes **106,814 exact assertions**. It uses a CRT derivation of the isometry list, exact Bezout identities, orthogonal-kernel factorization, the reciprocal linking convention, and the stated homological arithmetic. Most assertions repeat the orthogonality identity over the finite group; they are diagnostics, not independent topological constructions.

No new rho-invariant or d-invariant calculation, topology realization, or proof of Gilmer–Livingston's full obstruction is included. The original remains **unsolved,3/5 approaches**, with no novelty claim. The package is suitable for a scoped unresolved draft. No mandatory mathematical correction is required.

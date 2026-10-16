# Independent audit: determinant completeness and the topological obstruction

## Verdict and pinned object

**ACCEPTED as a complete mathematical proof of the stated complex theorem and, consequently, of the perfect nonsemisimple-source / semisimple-target nonexistence assertion in problem 30005737.** No missing hypothesis, circular argument, or unresolved mathematical gap was found in this audit. This is an independent mathematical acceptance of the exact candidate below, not journal acceptance, a formal proof-assistant certificate, or a claim of historical novelty.

Audit date: 7 October 2026.

- `PROOF.md`: 10,996 bytes; SHA-256 `2ac96492f1791f7fa2d5e988a7a44f60040395f6f2994649441755559c01f7f1`.
- Supporting `SOURCES.md`: 4,483 bytes; SHA-256 `46b03c8ce7a98b555b37e29137d75eb2e2cbcfb249e9e889f36545e2bb75d25b`.

The review independently reconstructed the argument, checked its primary sources, and sought examples violating its stronger unimodular conclusion. No other mathematical audit was used as an input. The candidate's use of the word “candidate” and its historical-status caveats do not weaken its mathematical conclusion; no changes to the pinned proof are required for this acceptance.

## 1. Match to the original question

The official Oberwolfach report places the relevant assertion at the bottom of printed p.2689: immediately following nonexistence for target \(\mathfrak{sl}_3(\mathbb C)\), Burde proposes the same conclusion for arbitrary semisimple target. It concerns perfect nonsemisimple source. The nilpotent-target conjectures appearing earlier on that page are different problems. The page was checked in extracted text and in a rendered image. [Official report](https://ems.press/content/serial-article-files/48175).

The introduction of the 8 March 2024 author's version of *Post-Lie algebra structures for perfect Lie algebras* also leaves the simple and semisimple target cases open. Section 2 specifies finite-dimensional algebras; Section 3 works over \(\mathbb C\). Proposition 2.6 gives the transverse-pair characterization. Theorem 3.10 and Propositions 3.11–3.12 are compatible special cases, not resolutions of the full question. Example 3.13 has a reductive target with nonzero center and lies outside the claim. [Author's paper](https://homepage.univie.ac.at/dietrich.burde/papers/burde_78_perfect.pdf).

The pinned result covers the full complex semisimple target, including products of simple factors, arbitrary source radical, and arbitrary source dimension. It imposes no unmentioned irreducibility, faithfulness of either individual map, algebraicity, or closed-image assumption.

## 2. The algebraic reduction and signs

For a post-Lie product, the third identity makes \(L(x)\) a derivation of the target. For a finite-dimensional complex semisimple target, \(\operatorname{ad}_{\mathfrak n}:\mathfrak n\to\operatorname{Der}(\mathfrak n)\) is a linear isomorphism. Therefore \(L(x)=\operatorname{ad}(R(x))\) defines a unique linear \(R\).

The second identity gives
\[
R([x,y])=\{R(x),R(y)\}.
\]
The first gives
\[
[x,y]=\{R(x),y\}+\{x,R(y)\}+\{x,y\}.
\]
Adding these equalities verifies directly that \(R+I\) is also a homomorphism. Hence the proof's convention
\[
j_1=R+I,\qquad j_2=R,\qquad j_1-j_2=I
\]
is correct. Switching the two labels would change the difference to \(-I\) and would not change transversality, but no such switch is needed.

Perfectness gives unimodularity because \(x\mapsto\operatorname{tr}(\operatorname{ad}x)\) is linear and vanishes on every bracket. All implications here apply to the source bracket in the trace calculation and to the target bracket in the inner-derivation calculation. The two roles have not been exchanged.

## 3. Global integration and the fundamental map

Taking auxiliary connected simply connected complex groups \(G,N\) is legitimate; the original problem places no global group structure in the hypotheses. Both homomorphisms integrate into this same \(N\). Injectivity or closedness of their images is unnecessary.

The formula
\[
A_h(p)=J_1(h)pJ_2(h)^{-1}
\]
is a left action: the inverse on the right produces the correct multiplication order in \(A_hA_k=A_{hk}\). Its positive-parameter fundamental vector has left-trivialized value
\[
B_p(x)=\operatorname{Ad}_{p^{-1}}j_1(x)-j_2(x).
\]
This follows by differentiating \(\exp(tj_1(x))p\exp(-tj_2(x))\), then multiplying its tangent vector on the left by \(p^{-1}\). Conventions making fundamental vector fields a Lie algebra homomorphism can insert an overall minus sign; the proof never needs that convention, and its explicitly defined derivative and determinant are consistent.

At \(e\), \(B_e\) is an isomorphism. The orbit map therefore contains a neighborhood of \(e\) in its image. Translating this neighborhood by the action makes the whole orbit open. In particular the use of an open subset in the subsequent identity theorem is justified in the usual complex-manifold topology, not merely in an abstract immersed-orbit topology.

## 4. Determinant equivariance is correct and proves completeness

For \(q=A_h(p)\), an independent expansion gives
\[
\begin{aligned}
B_q(x)
&=\operatorname{Ad}_{J_2(h)}\operatorname{Ad}_{p^{-1}}
\operatorname{Ad}_{J_1(h)^{-1}}j_1(x)-j_2(x)\\
&=\operatorname{Ad}_{J_2(h)}
 B_p(\operatorname{Ad}_{h^{-1}}x).
\end{aligned}
\]
In the second term one uses
\(\operatorname{Ad}_{J_2(h)}j_2\operatorname{Ad}_{h^{-1}}=j_2\).
Thus the determinant identity in the candidate has the right sign, order, and source/target representations.

If a complex Lie algebra is unimodular, the differential of the complex character \(\det\operatorname{Ad}:G\to\mathbb C^\times\) is zero. A homomorphism with zero differential on a connected Lie group is constant; its value at the identity is one. Equivalently, the character is one on exponentials and a connected group is generated by an identity neighborhood. Semisimplicity supplies this property for \(N\); the explicit hypothesis supplies it for \(G\).

Consequently the globally defined holomorphic function \(f(p)=\det B_p\) is invariant under the action. It equals \(f(e)\ne0\) on the nonempty open identity orbit. The several-complex-variable identity theorem on connected \(N\) gives \(f\equiv f(e)\) on all of \(N\). No compactness, algebraicity, closedness, or density assertion is needed for this continuation.

Every \(B_p\) is therefore invertible. Applying the same inverse-function argument at each point shows that every orbit is open. A partition of a connected space into disjoint open orbits has exactly one member: if one orbit had nonempty complement, that complement would itself be open. This establishes transitivity globally.

This step does **not** presume that an arbitrary post-Lie algebra integrates to a simply transitive action. Integration of the two homomorphisms initially gives only a globally defined action with an open orbit. The determinant argument supplies the additional completeness assertion under the theorem's hypotheses.

## 5. Stabilizer, quotient, and covering

The stabilizer \(H\) of the identity is the inverse image of a closed point under the orbit map, so it is closed. Its Lie algebra is \(\ker B_e=0\), hence it is discrete. The transitive action identifies \(N\) with \(G/H\), with its standard homogeneous-space manifold structure. Because the orbit is now all of \(N\), the possible pathology of nonembedded proper orbits is irrelevant.

Right translation by a closed discrete subgroup gives a covering \(G\to G/H\). One can choose a sufficiently small identity neighborhood whose distinct right translates by \(H\) are disjoint. Translating these neighborhoods gives evenly covered neighborhoods in the quotient. Since \(N\) is simply connected and \(G\) is connected, this covering has one sheet. In particular \(H\) is trivial. The resulting orbit map is a biholomorphism, although a diffeomorphism already suffices.

The proof does not incorrectly infer a covering from a surjective local diffeomorphism alone. It establishes the homogeneous-space quotient and closed discrete stabilizer first.

## 6. Levi decomposition and homology degrees

The Lie algebra Levi action integrates to an action of the simply connected semisimple group \(S\) on the simply connected solvable group \(R\). The group \(R\rtimes S\) is simply connected, has the required Lie algebra, and is therefore the chosen \(G\) up to isomorphism. Its underlying manifold is \(R\times S\). This avoids any assumption that a Levi subgroup in an arbitrary non-simply-connected integration has a particular global form.

The candidate's solvable contractibility induction is valid. A nonzero solvable Lie algebra has a codimension-one ideal containing its derived algebra. A complementary one-dimensional subspace is a subalgebra, so the algebra is a semidirect product. Integrating the derivation gives a semidirect product of simply connected groups with underlying manifold \(\mathbb C\times R'\). Induction gives contractibility; it does not assume surjectivity or injectivity of the exponential map for a general solvable group.

Set \(d=\dim_{\mathbb C}\mathfrak g=\dim_{\mathbb C}\mathfrak n\) and \(s=\dim_{\mathbb C}\mathfrak s\). A compact real form of \(N\) is a compact connected orientable real manifold of dimension \(d\), and polar decomposition gives the same homotopy type as \(N\). Thus its fundamental class gives \(H_d(N;\mathbb Z)=\mathbb Z\). This is degree \(d\), **not** the real manifold dimension \(2d\) of \(N\).

Likewise \(G\) has the homotopy type of a compact real form of \(S\), of real dimension \(s\). If the radical is nonzero, then \(s<d\), and a compact smooth \(s\)-manifold has zero homology in degree \(d\). This contradicts the diffeomorphism \(G\simeq N\). If \(d=0\), the theorem is already immediate and all these conventions remain consistent. Therefore the radical vanishes.

The classical inputs were checked against Etingof's MIT notes: Theorems 9.12–9.13 and Corollary 9.14 for complex integration; Proposition 4.12, Corollary 4.13, and Corollary 4.16 for homogeneous spaces; Theorem 43.7 and Corollary 43.8 with the covering discussion for polar decomposition; Theorem 49.1 for solvable groups. Corollary 49.6 on printed p.266 states exactly the homotopy-type conclusion used above. That page was also visually inspected. [MIT notes](https://ocw.mit.edu/courses/18-755-lie-groups-and-lie-algebras-ii-spring-2024/mit18_755_s24_lec_full.pdf).

## 7. Adversarial boundary checks

### Dropping unimodularity really permits degeneration

Let \(\mathfrak n=\mathfrak{sl}_2(\mathbb C)\), with basis \(h,e,f\), and let the source be the direct sum of the upper Borel \(\langle h,e\rangle\) and an abelian line \(\langle f\rangle\). Define \(j_1(h)=h,j_1(e)=e,j_1(f)=0\), and \(j_2(f)=-f,j_2(h)=j_2(e)=0\). Both are homomorphisms and their difference is the identity. But the source has \(\operatorname{tr}\operatorname{ad}(h)=2\).

For \(p=\left(\begin{smallmatrix}a&b\\c&\delta\end{smallmatrix}\right)\in SL_2(\mathbb C)\), direct matrix calculation yields
\[
B_p=\begin{pmatrix}
a\delta+bc&c\delta&0\\
2b\delta&\delta^2&0\\
-2ac&-c^2&1
\end{pmatrix},\qquad
\det B_p=\delta^2(a\delta-bc)=\delta^2.
\]
It is nonzero at the identity and zero at a Weyl representative with \(\delta=0\). This independent symbolic check confirms that the proof's central step is substantive and that familiar triangular nonsemisimple-source examples do not contradict it.

### Later global examples do not contradict the theorem

The later paper by Damele and Loi, *Structural and rigidity properties of Lie skew braces*, arXiv:2507.06214v3 (25 February 2026), distinguishes global Lie skew braces from possibly nonintegrable infinitesimal post-Lie structures. Its semisimple-source rigidity statement is not the present semisimple-target conjecture. In the proof of Theorem 1.4, item 10, its mixed-source / simple-target example comes from the real Iwasawa factorization \(SL_3(\mathbb R)=KAN\), with source \(SO(3)\times AN\). [Paper](https://arxiv.org/html/2507.06214v3).

Independently, the adjoint trace on the \(AN\) factor at \(\operatorname{diag}(1,0,-1)\) is \(1+1+2=4\), using the three positive-root spaces; its action on the abelian diagonal subalgebra has trace zero. Thus this source is not unimodular. It supplies neither a counterexample nor a general resolution of the infinitesimal completeness issue.

### Stronger consequences are consistent with scope

Reductive sources are unimodular, so the theorem also excludes nonsemisimple reductive sources with semisimple targets. This is consistent with, and stronger than, the nonexistence part of Conjecture 3.5 in the 2022 rigidity paper. Obtaining the isomorphism conclusion for an already semisimple source uses the separate established rigidity theorem; a manifold diffeomorphism alone is not asserted to determine the complex Lie algebra. [2022 preprint](https://arxiv.org/abs/2205.04218).

## Final disposition

The full chain is valid: post-Lie identities give a transverse homomorphism pair; source unimodularity and semisimple-target unimodularity give a globally nonvanishing determinant; this makes the integrated action transitive; simple connectedness removes the discrete stabilizer; top-degree homology then removes the source radical. The exact pinned proof establishes the claimed full nonexistence result over \(\mathbb C\). No counterexample or mathematical repair remains outstanding. Literature searching remains bounded, and no novelty claim is certified by this acceptance.

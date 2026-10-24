# Fresh adversarial audit of the parabolic preservation countermodel

**Verdict: the stated finite-Hausdorff countermodel passes.** It disproves the proposed universal preservation lemma for the images of standard maximal proper parabolics in the central quotient \(K=B_4/Z(B_4)\). It does not decide any residual pair or Kourovka21.129. All groups in the construction remain quasi-isometric and abstractly commensurable.

One essential terminology qualification: “commensurable subgroups” here means **internally commensurable**, i.e. their intersection has finite index in both. It must not be read as “abstractly commensurable.” Indeed \(Q=\alpha(D)\cong D\), while D has finite index in \(C\cong B_3\); hence Q and C are abstractly commensurable. The draft explicitly says “as subgroups” in its algebraic paragraph, so its intended proof is valid. Carry that qualifier through any summary.

## Audited objects and reproduction

Source SHA-256 values at the audit:

| File in `../geometry/` | SHA-256 |
|---|---|
| PARABOLIC_PRESERVATION_COUNTERMODEL.md | `6dd5d8e4f157bae6da96eaf32316527cb453cdbfe186695045ce403fe623cc81` |
| check_certificates.py | `d227b5bdf527903be087c765e487b0a46a11fda347703fe2f2e6d3a5d2cd6765` |
| CERTIFICATES.json | `5b82a57ff13019edea2f917df3d6da77c5861e5c7e2be61a61053717f2914637` |

Copied the checker unchanged into `geometry_reproduction/` and executed it there, leaving the source author's files unchanged. Exit status0, empty stderr, all assertions passed; generated JSON is byte-identical to the source certificate. Full metadata and timestamp: `GEOMETRY_DELTA_REPRODUCTION.json`. This validates the finite algebra and the script's additional diagram calculations; the geometric argument needs the separate checks below. Independently generated separating functionals and full permutation-action sanity checks are in `GEOMETRY_INDEPENDENT_HOMOLOGY_CHECK.json`.

## Mapping class model and the extension to a quasi-isometry

[Charney–Crisp, §2](https://arxiv.org/pdf/math/0408412v1), manuscript p4, identifies the braid group modulo its center with the orientation-preserving punctured-sphere mapping classes fixing the capped puncture. It also describes pure orientation-preserving mapping classes as the kernel of the puncture-permutation and orientation homomorphism. Thus K is the stabilizer of0 in \(\operatorname{Mod}^+(S_{0,5})\), and \(H=P_4/Z(P_4)=\operatorname{PMod}(S_{0,5})\) is normal in the full mapping class group and has index24 in K. The pure identification is also CP Lemma6.4.

An orientation-preserving mapping class with permutation (0 1) exists, for example a half twist along an arc between those punctures. It need not have order2 as a mapping class; the argument requires only its puncture permutation. Since it normalizes H, conjugation restricts to an automorphism α of H.

For a finite set R of representatives of the right cosets Hr, choose1 for H itself and put \(p(hr)=h\). In a left-invariant word metric,

\[
d_K(hr,h)=|r|\le \max_{r\in R}|r|.
\]

Hence p is bounded distance from the identity after inclusion into K, and is a quasi-isometry between K and its finite-index subgroup H, with its induced or intrinsic word metric. The composition \(F=\iota\alpha p\) is a self-quasi-isometry of K, with coarsely dense image H, and restricts to α on H. No extension of α to a group automorphism of K is claimed or needed.

The chosen C is the B3 supported on disk punctures123. It embeds in K: if a global full-twist power lay in this B3, its linking number between strands1 and4 would be simultaneously that power and0. Therefore only the identity of the ambient center lies in C. Its pure intersection D is the embedded P3 and has index6 in C. Finite index gives \(d_{Haus}(C,D)<\infty\); the coarse Lipschitz property of F gives

\[
d_{Haus}(F(C),F(D))<\infty,\qquad F(D)=\alpha(D)=Q.
\]

This checks the finite-index-extension step independently of the support intuition.

## Rational homology and the puncture permutation

The six pairwise linking maps show \(H_1(P_4;\mathbb Z)=\mathbb Z^6\), with pure pair-twist basis \(e_{12},e_{13},e_{14},e_{23},e_{24},e_{34}\). The full twist has all six linking numbers1. Abelianization commutes with taking a quotient by a central subgroup, so

\[
H_1(H;\mathbb Q)=\mathbb Q^6/\mathbb Qv,\quad v=(1,1,1,1,1,1).
\]

There is exactly this one homology relation. D is generated in homology by e12,e13,e23, giving a three-dimensional image.

Conjugating a positive Dehn twist by an orientation-preserving mapping class gives the positive twist about the image curve. The curve surrounding {0,2} is also the boundary of the complementary disk containing finite punctures134; its twist has linking class e13+e14+e34. This homology class does not require image curves with the same enclosed punctures to be isotopic: a pure mapping class carries one such disk boundary to another, and inner conjugation by H is trivial on H's abelianization. The same argument applies to {0,3}. Thus the three images in the draft are correct, including their signs.

A further independent check uses all six images of the permutation(0 1):

\[
\begin{aligned}
e_{12}&\mapsto e_{13}+e_{14}+e_{34},\\
e_{13}&\mapsto e_{12}+e_{14}+e_{24},\\
e_{14}&\mapsto e_{12}+e_{13}+e_{23},
\end{aligned}
\qquad e_{23},e_{24},e_{34}\mapsto e_{23},e_{24},e_{34}.
\]

This matrix maps v to2v and its square induces the identity modulo v, as required because the square of the mapping class lies in H. It therefore respects the quotient relation and the known involution on abelianization.

Let a,b,c be the three displayed generators of U′. If ra+sb+tc=λv, comparison at12 and24 gives s=λ, at13 and34 gives r=λ, and at14 gives r+s=λ. Hence λ=r=s=0, and at23 gives t=0. Thus dimU′=3. The identity a+b+c=v+e14 shows e14∈U′; c=e23 gives e23∈U′ too.

## Every target parabolic and every conjugate is excluded

The rank-two maximal proper subsets of the A3 chain give exactly A2,A2,A1×A1. For any k∈K, normality of H gives

\[
(kLk^{-1})\cap H=k(L\cap H)k^{-1}.
\]

The action of k on linking classes is its permutation of the four finite strand indices; a pure braid acts by an inner automorphism on H and trivially in H1. Hence every conjugate A2 pure-intersection image is the triangle span U_T for a three-element finite subset T. Every A1×A1 pure-intersection image has dimension at most2.

Here is a rank-free separation certificate independent of the author's Gaussian elimination. In the edge order12,13,14,23,24,34, the following functionals vanish on v and on U_T, but take value1 on the indicated element of U′:

| T | Element of U′ | Functional |
|---|---|---|
|123|e14|e14*−e24*|
|124|e23|e23*−e13*|
|134|e23|e23*−e12*|
|234|e14|e14*−e12*|

Thus U′ differs from every U_T. Its dimension also excludes the A1×A1 case. If two subgroups of H are internally commensurable, every element has a positive power in their finite-index intersection. Since positive powers multiply rational homology classes by nonzero integers, their rational homology image spans must agree. Therefore Q is not internally commensurable with any target pure intersection. Finite index of H transfers this exclusion to the corresponding subgroups of K.

## Why this excludes finite Hausdorff distance from all stated cosets

For any subgroup L≤K and g∈K, the sets gL and gLg^{-1} are at Hausdorff distance at most |g|: pair gℓ with gℓg^{-1}. This converts the left-coset question into a question about a subgroup in the same allowed conjugacy family.

For subgroups A,B≤K at finite Hausdorff distance, a finite word-metric ball E gives A⊂BE and B⊂AE. For each e with A∩Be nonempty, choose a_e∈A∩Be. Then A∩Be=(A∩B)a_e, so A is covered by finitely many cosets of A∩B. Reversing A and B proves finite index on both sides. Thus A and B are internally commensurable. This lemma requires only finiteness of ambient metric balls, not undistortion or quasiconvexity of the subgroups.

Apply it to A=Q and B a conjugate of a raw target parabolic. The homology obstruction contradicts internal commensurability. Since F(C) is finite Hausdorff distance from Q, it too cannot be finite Hausdorff distance from any asserted coset. This completes the exact statement in the source note.

## Scope and remaining boundaries

The falsified route is the universal lemma that arbitrary quasi-isometries of all spherical Artin **central quotients** preserve cosets of images of standard maximal proper Artin parabolics, even up to conjugacy and finite Hausdorff distance. A statement restricted to only D6/E6, D7/E7, D8/E8, or F4/H4 is not itself disproved by this A3 example. Neither is preservation of an enlarged family containing all relevant twist centralizers disproved. The argument does not assert an extension of α to an automorphism of K, nor an explicit lift to a self-quasi-isometry of the full B4 preserving a chosen central splitting.

**No substantive mathematical repair is required.** For safe promotion, state “not internally commensurable” and keep the central-quotient and universal-lemma scope explicit. The obstruction is not a counterexample to quasi-isometry implying abstract commensurability of spherical Artin groups.

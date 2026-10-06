# Independent source-scope and torus-dynamics adversarial audit of PR126

Original head: `a1df84a64fa96d53f3a8c6fec9db8bc48bd1533c`. Target: `11000147 / AMR-109-0147`. This is a verification audit, adding **0** central proof-search turns to the original **1/5** effort. Submitted `CANDIDATE.md` and `SOURCE_AUDIT.md` were read; the submitted reviewer report and submitted independent-check artifacts were deliberately not read. No Git, main/index, native state, PR, publication, tracker, or external-outreach action was taken.

## Verdict and exact theorem

**PASS for the submitted, expressly qualified torus theorem and its match to the source's literal existential question.** No substantive source-scope, dynamical, or topological defect was found. This is not a priority or novelty clearance.

Let

\[
A=\begin{pmatrix}3&1\\2&1\end{pmatrix},\quad
B=\begin{pmatrix}1&-2\\-1&3\end{pmatrix},\quad
C=\begin{pmatrix}8&-11\\3&-4\end{pmatrix}.
\]

On the **closed oriented torus** \(T^2=\mathbb R^2/\mathbb Z^2\), the actual diffeomorphisms \(f_M([v])=[Mv]\), for \(M=A,B,C\), are three distinct, pairwise noncommuting orientation-preserving Anosov maps. Each unordered pair satisfies the alternating length-three braid relation as equality of actual maps. Their mapping classes are also distinct. Their expansion factor is \(2+\sqrt3\), with reciprocal contraction factor \(2-\sqrt3\). They supply the nonsingular torus case explicitly contemplated in the primary problem's discussion.

The theorem makes no claim for every prescribed higher genus, for a surface with pointwise-fixed boundary, for a minimal three-element generating set, or for an injective homomorphism from a triangular Artin group. Those qualifications must remain attached to any promoted result.

## Primary source and complete-context inspection

Primary: B. Wajnryb, *Relations in the mapping class group*, Chapter 8 in Benson Farb (ed.), *Problems on Mapping Class Groups and Related Topics*. Author-hosted manuscript: <https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf>. SHA-256: `f37c6a1dbc875105c2b294196de1a03a88595b75e8705e6077e9d48f066e402a`; 2,724,624 bytes. Parent-owned private source cache was read without modification. All seven chapter pages, including bibliography, were rendered and visually inspected: printed 122-128 / PDF pages 129-135 (one-based).

Checkable locators:

| Primary locator | Fact relevant to scope |
| --- | --- |
| Section 1, printed 122 / PDF 129 | Compact surfaces are permitted, including closed surfaces; orientation is preserved for oriented surfaces. Boundary fixing applies when a boundary exists. |
| Section 2, printed 123 / PDF 130 | Artin relations are defined by equal alternating words of the stated length. |
| Section 2, printed 124 / PDF 131, three consecutive Question paragraphs | The embedding question, a two-map question, and the three-map question are distinct statements. |
| Same page, paragraph immediately after the three-map question | The source explicitly discusses Anosov matrices on the torus in its pseudo-Anosov-pair construction; higher genus is treated separately. |
| Remaining chapter, printed 125-128 / PDF 132-135 | Subsequent sections concern positive relations and nonorientable surfaces; they impose no retroactive restriction on the three-map question. |

The literal target is: “Does there exist a set of at least three pseudo-Anosov homeomorpisms such that every pair satisfies a braid relation.” The chapter does not add a genus bound, nonconjugacy, generator independence, or faithfulness to that target. The nearby discussion motivates embeddings but does not make the three-map target equivalent to an embedding problem.

The source's explicit torus paragraph is decisive for the genus-one terminology. Some authors reserve “pseudo-Anosov” for surfaces of negative Euler characteristic and call this genus-one case “Anosov.” The candidate makes this distinction rather than silently relying on a general terminology convention. If a different problem were posed on a specified genus \(g\ge2\), this torus construction alone would not resolve it.

There is a small source-level order nuance: the abstract pair construction starts with an order-two element, whereas its torus variant permits \(X^2=-I\), so \(X\) has order four in \(\mathrm{SL}_2(\mathbb Z)\). The source itself states this torus variant. The candidate does not assert that its displayed \(X\) has order two, and the central \(-I\) makes the displayed pair's exact braid relation valid. Thus no mistaken order assumption is being imported into the proof.

## Actual torus maps, isotopy classes, and global foliations

For any displayed \(M\), integrality makes \([v]\mapsto[Mv]\) independent of the chosen lift: replacing \(v\) by \(v+z\), with \(z\in\mathbb Z^2\), replaces \(Mv\) by \(Mv+Mz\). Determinant one gives an integral inverse, so the induced map is a diffeomorphism rather than a covering of higher degree. Its derivative is the same real matrix everywhere and has positive determinant. Consequently it preserves orientation. Matrix multiplication matches the ordinary composition convention \(f_M\circ f_N=f_{MN}\).

The homology classes of the two coordinate loops form a basis of \(H_1(T^2;\mathbb Z)\); their images have coordinate columns equal to the columns of \(M\). Thus \((f_M)_*=M\). Since isotopic maps induce the same homology action, distinct displayed matrices give distinct mapping classes and therefore distinct actual maps. This does not depend on a finite grid, a numerical sample, or the classification of torus mapping classes.

Each matrix obeys

\[
\det M=1,\qquad \operatorname{tr}M=4,\qquad M^2-4M+I=0.
\]

The characteristic roots \(\lambda_+=2+\sqrt3\) and \(\lambda_-=2-\sqrt3\) are distinct and positive, and satisfy \(\lambda_+\lambda_-=1\). From \(1<\sqrt3<2\), one has \(0<\lambda_-<1<\lambda_+\). The two real eigenspaces split every tangent plane into contracting and expanding lines. These line fields are constant on \(\mathbb R^2\), so they descend through integer translations to a continuous invariant splitting of the entire tangent bundle of the torus. For every \(n\ge0\), vectors on the stable line are contracted by exactly \(\lambda_-^n\), while vectors on the unstable line are contracted by exactly \(\lambda_-^n\) under the inverse map. This gives the Anosov condition globally with constant 1 in the Euclidean metric restricted to each line. A large matrix entry or a nonorthogonal pair of eigenlines does not affect this argument.

Integral translation-invariant eigenline foliations on the universal cover are nonsingular. Their transverse measures are defined by integrating the absolute values of constant covectors, so the measures are independent of the choice of lifted transverse arc. If \(\ell_s\) annihilates the stable line and \(\ell_u\) annihilates the unstable line, then

\[
\ell_sM=\lambda_+\ell_s,\qquad
\ell_uM=\lambda_-\ell_u.
\]

In an unambiguous convention, these are **pullback** equations: the transverse measure of \(f_M(\gamma)\) is \(\lambda_+\) times that of \(\gamma\) for the stable foliation, and \(\lambda_-\) times for the unstable foliation. Pushforward has the inverse factors. The candidate's explicit covector equations are correct; it does not interchange the annihilated line and the relevant multiplier.

The eigenlines have irrational slope. Indeed, a rational eigenline contains a nonzero integer vector \(v\); a nonzero coordinate \(v_i\) would imply \(\lambda=(Mv)_i/v_i\in\mathbb Q\), contrary to \(2\pm\sqrt3\notin\mathbb Q\). Thus neither foliation accidentally becomes a foliation by compact rational-slope circles. No singularities are needed in the genus-one Anosov setting explicitly used by the source.

## Braid relations and boundary checks

Direct integer multiplication gives

\[
ABA=BAB=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
ACA=CAC=\begin{pmatrix}7&-10\\5&-7\end{pmatrix},\quad
BCB=CBC=\begin{pmatrix}5&-13\\2&-5\end{pmatrix}.
\]

These equalities yield equalities of actual maps through the verified composition convention. If a commuting pair \(x,y\) also satisfies \(xyx=yxy\), cancellation in \(x^2y=xy^2\) forces \(x=y\). The three distinct matrices therefore give noncommuting pairs; their least positive alternating Artin-relation length is three. Equality at length three is not a claim that longer relations never also hold.

The group-theoretic argument also checks without torsion-free or surface assumptions: \(c=aba^{-1}=b^{-1}ab\), and conjugating the original braid relation by \(a\) and by \(b^{-1}\) gives respectively the \((a,c)\) and \((c,b)\) braid relations. If \(c=a\), then \(b=a\). If \(c=b\), then \(a,b\) commute and hence agree. Thus the lemma really yields a distinct triple in any conjugacy-invariant class from a distinct length-three braid pair. For the general mapping-class statement, this is a statement about classes; it does not promise exact braid-related representatives on every higher-genus surface. The closed-torus construction separately supplies such representatives.

Adversarial scope checks and outcomes:

- Replacing the closed torus by a one-holed torus fixed on its boundary is not justified by these matrices alone; the candidate expressly avoids that claim.
- Requiring genus at least two would be a stronger, differently scoped problem; no such restriction is imposed by the quoted source target or its immediate torus discussion.
- Requiring three independent generators fails here: \(C=ABA^{-1}\), so two elements already generate the image. The candidate expressly acknowledges this.
- Requiring a faithful triangular Artin representation is not established; no such conclusion is part of the theorem.
- Requiring nonconjugate maps is incompatible with the displayed odd braid relations and is not required in the target.
- Treating a trace-two shear as Anosov, or a determinant-two integer matrix as a torus diffeomorphism, would invalidate the proof. Independent negative controls detect both failures.
- Confusing transverse-measure pushforward with pullback reverses the scale factors, but does not occur in the candidate's equations. A promoted write-up may spell out the pullback convention for clarity; no mathematical repair is required.

## Independent exact reproduction and limits

`check_dynamics.py` implements exact arithmetic in \(\mathbb Q(\sqrt3)\) as pairs of rational numbers, without importing a submitted verifier or reviewer. For each matrix it checks the two-sided integral inverse, characteristic identity, nonzero stable/unstable vectors, their transverse splitting, annihilating covectors and the correct pullback multipliers, and complementary exact spectral projectors. Three nearby invalid replacements are rejected at the actual failed prerequisite. All 46 validation guards are explicit exceptions, not removable Python assertions.

Both default and optimized Python runs passed all 46 guards. `DYNAMICS_CERTIFICATE.json` and `DYNAMICS_CERTIFICATE_O.json` record actual operator PIDs, UTC timestamps, interpreter and optimization level, exact field-valued certificates, primary PDF hash, and script hash. These computations supplement the global quotient/foliation proof above; they are not promoted as a numerical proof of Anosov dynamics.

This audit clears the **source-scope and mathematical dynamics gate only**. It does not establish when the elementary group deduction, exact matrices, or target answer first appeared, and it makes no priority, novelty, publication, or final native-status recommendation. A separate priority audit is still required by the parent workflow.

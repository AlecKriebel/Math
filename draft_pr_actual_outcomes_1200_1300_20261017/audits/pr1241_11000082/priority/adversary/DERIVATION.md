# NOW-ASSEMBLED implication from older general theory

**Authored during this audit on 17 October 2026. This is a deduction assembled now, not an assertion that the target was explicitly printed, recognized, or resolved historically in 1999, 2006, 2008, or 2015.**

## Exact claim

Fix a closed oriented surface S of genus g >= 2 and an integer k >= 3. Put Gamma_0 = pi_1(S), Gamma_(j+1) = [Gamma_0,Gamma_j], and I_g(j) = ker(Mod_g -> Out(Gamma_0/Gamma_j)). For every integer N there are N pseudo-Anosovs in this fixed I_g(k) with identical dilatation and distinct conjugacy classes in the orientation-preserving ambient Mod_g. We allow proper powers and allow the common value to depend on N.

We give a complete conservative chain using the single-curve seed explicitly stated by Aougab-Taylor. A subsequent paragraph identifies an earlier multitwist seed in FLM. The new bridge relative to the submitted proof is Kapovich's malnormal-subgroup theorem; no finite-core conjugacy-fusion lemma from the submission is used.

## Primary imports actually inspected

1. Aougab-Taylor, Lemma 2.2 and proof, PDF 3-4: every closed genus g >= 2 has a filling pair a,b of separating simple curves. Their Theorem 5.1, PDF 10, explicitly uses centrality of the Johnson filtration to place iterated commutators of the associated twists in each fixed depth. [Primary preprint](https://arxiv.org/pdf/1510.00995).
2. Leininger, Theorem 3.1 and the preceding stabilizer discussion, printed 1314 / PDF 14; Theorem 3.2, 1315 / PDF 15; rectangle construction, 1319-1321 / PDF 19-21; Lemma 6.3, 1323 / PDF 23; and freeness/Proposition 6.4, 1326 / PDF 26. These identify affine disk stabilizers, hyperbolic derivative/dilatation, uniqueness of a pseudo-Anosov's invariant disk, and the faithful two-parabolic construction with only cusp exceptions when the shear parameter exceeds 2. [Primary published body](https://arxiv.org/pdf/math/0304163).
3. Hubert-Lelièvre, Lemmas 2.1 and 2.3, PDF 7-8: for a square-tiled translation surface the relative-period vectors span a rank-two integral lattice Lambda, and its whole affine derivative group preserves Lambda. This is not a statement restricted to H(2); those lemmas and their proofs are stated for a general square-tiled surface. Appendix C, PDF 37-38, also proves square-tiled arithmeticity, but finite covolume is unnecessary here. [Primary preprint body](https://arxiv.org/pdf/math/0401056).
4. Kapovich, arXiv math/9704203v1, Theorem 7.7, PDF 29-30 (complete proof inspected): any non-elementary subgroup E of a torsion-free word-hyperbolic group G contains a rank-two free subgroup malnormal and quasiconvex in G. E is not assumed finitely generated. The theorem is called Theorem C in Anderson's later survey and the published paper's descriptions; in the inspected arXiv v1, Theorem C is a different, preparatory free-group statement. [Original primary theorem body](https://arxiv.org/pdf/math/9704203).
5. Horowitz, Example 8.2, printed 648-649 / PDF 14-15, with the universal-character convention on 636 / PDF 2: free rank two has 2^m pairwise nonconjugate nonidentity words with identical trace in every SL_2 representation. [Primary body](https://www.math.purdue.edu/~eremenko/Pdf/horowitz.pdf).
6. FLM, Proposition 4.8 proof, PDF 20, matches precisely the indexing containment used below. [Primary body](https://arxiv.org/pdf/math/0603675).

These are published/preprint mathematical imports, not claims that their underlying background proofs have all been independently reproduced.

## 1. Fixed geometry and a faithful free group

Choose the separating filling pair a,b and put A = T_a, B = T_b, F = <A,B>. If n = i(a,b), the Euler characteristic of the filling graph gives n >= 2g-1. A separating curve has even intersection with any closed curve, so n is even and n >= 4. Thus the exceptional parameter n=2 is absent, including genus two.

In Leininger's rectangle construction the intersection matrix is the one-by-one matrix [n]. Both positive rectangle coordinate vectors may be chosen equal to 1. All rectangles are therefore congruent squares. Normalize them to unit squares and denote the resulting half-translation structure by q.

The derivative images of A,B are projectively represented by
$$
 U=\begin{pmatrix}1&n\\0&1\end{pmatrix},
 \qquad V=\begin{pmatrix}1&0\\-n&1\end{pmatrix}.
$$
For n>2, Leininger's two-parabolic classification and freeness argument show F is free on A,B, its derivative map is injective, and every nonidentity element except F-conjugates of powers of A or B has hyperbolic derivative and is pseudo-Anosov. Its dilatation is the spectral radius of the derivative.

## 2. Whole ambient disk stabilizer lies in a modular overgroup

This is the place where using only integral matrices U,V would be insufficient: a mapping-class conjugator need not lie in F.

If q is globally a square of an Abelian differential, apply Hubert-Lelièvre directly. Otherwise take the canonical orientation double cover of q. Topologically, off the singularities this is the cover corresponding to the kernel of the sign holonomy pi_1(S minus singularities) -> {+1,-1}; fill in its punctures to obtain a compact translation surface (S_hat,omega). Each unit square of q lifts to two unit squares, so it is square-tiled.

An affine automorphism of q preserves this sign kernel: its constant derivative conjugates the linear holonomy, and both signs are central. It therefore lifts to the orientation cover. The lift is affine for omega and has the same projective derivative. This lifting claim is an elementary step supplied here; it is not being attributed verbatim to Hubert-Lelièvre.

By their Lemmas 2.1/2.3 all lifted derivatives preserve the single fixed rank-two relative-period lattice Lambda. In the global-square case use the corresponding Lambda on S itself. Hence every orientation-preserving affine projective derivative of q belongs to
$$
 L=SL(\Lambda)/\{\pm I\}\cong PSL_2(\mathbb Z).
$$
The determinant is one because affine maps preserve total area on the compact surface. A positive basis of Lambda identifies L with the modular group.

We have used a lattice in the orientation cover, not a two-dimensional absolute-cohomology subspace on the original Torelli surface. Indeed FLM explicitly notes that a Torelli pseudo-Anosov has nonorientable invariant foliations. No unsupported orientability assumption enters this argument.

## 3. The fixed deep image is non-elementary inside a free group

Write gamma_1(F)=F and gamma_(j+1)(F)=[F,gamma_j(F)]. Since F is in I_g(1), Johnson centrality gives gamma_j(F) <= I_g(j). In the zero-based convention of FLM Proposition 4.8, this is their (j-1)st lower-central term. Fix gamma_k(F) before varying the trace-family size.

Here is an elementary non-elementarity check, so it is not merely assumed. Set u_1=B and u_(j+1)=[A,u_j]. Inductively u_j is nontrivial. If [A,u_j]=1 then u_j is a power of A, since a basis generator's centralizer in a free group is its cyclic subgroup. For j>=2, u_j has zero abelianization, which forces that power to be the identity, contradicting induction; the first commutator is directly nontrivial.

The two elements u_k and B u_k B^{-1} do not commute. Otherwise their maximal cyclic root groups meet nontrivially; malnormality of maximal cyclic subgroups of a free group would force B into the root group of u_k. Since a nonzero power of its root has zero abelianization in torsion-free Z^2, the root, and then B, would also have zero abelianization, a contradiction. Both elements lie in gamma_k(F) by normality.

Every nonidentity element of gamma_k(F), for k>=2, has zero abelianization in the A,B basis. It cannot be conjugate to a nonzero power of A or B, so it is pseudo-Anosov and its derivative is hyperbolic.

Let E be the faithful derivative image of gamma_k(F). Since gamma_k(F) <= [F,F], E lies in K=[L,L]. The modular presentation L=C_2*C_3 identifies K with the kernel of L -> C_2 x C_3, so K is normal of index six. It is torsion-free free of rank two: its Bass-Serre quotient has 6 edges and 3+2 vertices, hence Euler characteristic -1. It is consequently a torsion-free word-hyperbolic group. E contains two noncommuting elements and is non-elementary.

Apply **Kapovich Theorem 7.7 with G=K and the subgroup E**. Obtain J <= E free of rank two and malnormal in K. Do not apply that theorem to Mod_g itself, or to PSL_2(Z) with its torsion. The inverse derivative identifies a corresponding rank-two subgroup H <= gamma_k(F) <= I_g(k). All its nonidentity elements remain pseudo-Anosov.

## 4. Published malnormality gives a uniform ambient fusion bound

A K-conjugacy class meets J in at most one J-conjugacy class. Indeed if x,y in J are nonidentity and t x t^{-1}=y for t in K, then J intersects tJt^{-1} nontrivially; malnormality forces t in J. No assumption of primitivity is used.

A single L-conjugacy class of an element in K is the union of at most six K-conjugacy classes: use six representatives of L/K and normality of K. It follows that it meets J in at most six J-conjugacy classes.

If x,y in H are conjugate by t in ambient orientation-preserving Mod_g, the pseudo-Anosov y stabilizes D(q) and tD(q). Leininger Theorem 3.2 forces tD(q)=D(q). The affine-stabilizer identification then puts t's projective derivative in L, by section 2. Thus their derivatives are L-conjugate.

Faithfulness on H consequently bounds the number of H-conjugacy classes in one ambient Mod_g class by six. The finite kernel of the derivative on the full stabilizer causes no problem: only the necessary implication from ambient conjugacy to derivative conjugacy was used.

## 5. Equal trace gives the exact required conclusion

Choose a free basis of the fixed H. The projective representation lifts to SL_2(R) by choosing lifts of its two free generators. Apply Horowitz inside this H to obtain 2^m distinct nonidentity H-conjugacy classes with common trace t_m. Because all nonidentity elements are hyperbolic, |t_m|>2. Their common dilatation is
$$
 \lambda_m=\frac{|t_m|+\sqrt{t_m^2-4}}{2}.
$$
At most six of their intrinsic classes fuse in each ambient Mod_g class, so there are at least ceil(2^m/6) ambient classes with this dilatation in the one fixed I_g(k). This tends to infinity. All choices g,k,q,F,E,J,H precede m.

This proves the exact target from the inspected old inputs. It says nothing about simple Teichmüller loops, and does not prove that the mapping classes are primitive. Neither is required. No one value is claimed to have infinite multiplicity.

## 6. Earlier-source variant using FLM's every-genus seed

Aougab-Taylor is a convenient conservative seed, but the deduction need not depend on a source first posted in 2015. FLM §2.3 (PDF 12-13) already explicitly constructs filling separating multicurves A,B for every g>=2 with a common affine representation
$$
 T_A\mapsto\begin{pmatrix}1&8\\0&1\end{pmatrix},\qquad
 T_B\mapsto\begin{pmatrix}1&0\\-8&1\end{pmatrix}.
$$
Their intersection pattern is the cyclic 4-incidence pattern; the constant positive rectangle vectors give unit squares. For small numbers of components coincident cyclic incidences must be added: with one component N=[8], and with two N has all entries 4, both giving the stated shear 8. One must not read the generic displayed sparse formula for NN^t as if coincident cyclic entries remained distinct. The argument relies on the paper's explicitly asserted all-genus geometric construction, whose Figure 4 was inspected; it does not newly draw every genus.

Their Proposition 4.8, PDF 20, already uses exactly this free multitwist group and the lower-central-to-Johnson containment. Leininger's rectangle and two-parabolic results apply to multicurves as well. Repeating sections 2-5 therefore gives the same conclusion using theorem ingredients published by 2008 (Horowitz 1972, Kapovich 1999, Leininger 2004, Hubert-Lelièvre 2006, FLM 2008).

**Historical inference boundary:** this establishes that these older theorem ingredients suffice when assembled now, with the stated elementary interfaces. It does not identify a 2008 paper stating the conclusion, prove when specialists first knew it, or authorize setting an “already solved” historical date to 2008. It is an explanation of the theorem's dependence on existing mechanisms, not a worldwide priority certificate.


# Independent mathematical audit: rank-four Torelli restriction

Target: 11000312 / AMR-109-0312, rank 1258. Audit date: 10 October 2026 UTC.

## Verdict

**PASS as a rigorously scoped, unresolved first-attempt partial result. No full resolution is accepted.** Theorems A–D are correct under their stated credited inputs. The torsion-permanence proposition is correct only with the explicit fibration input FI; that input has not been independently established at rank four in this packet. Neither nonzero restriction, surjectivity, nor nonzero canonical higher torsion has been proved.

The distributed [mathematical report](MATHEMATICAL_REPORT.md) has 22,106 bytes and SHA-256:

`8370c260c3c76006fe0c576b5dde14bdd680493398d8984a973493218c7e9b99`.

This acceptance applies to those exact distributed bytes. The report correctly limits Lindell's unconditional degree-two result to the algebraic part of stable cohomology of IA_n.

This is substantive attempt 1 of 5, and the outcome remains unresolved. This AI-assisted, unrefereed audit preserves the complete mathematical review. Scoped acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. No novelty assessment or certification of continuing openness is made.

## 1. Exact target, groups, and primary inputs

The original [Morita Problem 4.5 in the Farb volume](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf), printed p.359 / PDF p.366, was independently visually inspected. It concerns cohomological restriction

\[
H^4(\operatorname{Out}(F_4);\mathbb Q)\cong\mathbb Q
\longrightarrow H^4(\operatorname{IOut}_4;\mathbb Q)^{\operatorname{GL}(4,\mathbb Z)},
\]

and generation of its target by a suitable nonzero scalar multiple of higher torsion. The neighboring degree-eight question is separate. The one-dimensional source is also explicitly corroborated in the first-page abstract of [Conant–Vogtmann](https://arxiv.org/abs/math/0406389). The underlying graph-homology computation was not independently replayed. A theorem computing the corresponding group for Aut(F_4), without comparison to Out(F_4), would not alone suffice; the report does not make that substitution.

The exact arithmetic inputs have the right groups, coefficients, and rank ranges:

- [Brück–Miller–Patzt–Sroka–Wilson](https://arxiv.org/abs/2204.11967), Theorem B and its transfer consequence, PDF p.5, apply for n≥3 and yield H^4(GL_4(Z);Q)=0.
- [Church–Putman](https://msp.org/gt/2017/21-2/gt-v21-n2-p07-s.pdf), Theorem A, printed p.1000 / PDF p.2, explicitly includes GL_n(Z) with trivial rational coefficients for n≥3 and yields H^5(GL_4(Z);Q)=0.

These are directly inspected primary theorem statements. The original Lee–Szczarba proof is not needed to substitute for the inspected Church–Putman theorem and is not claimed to have been read.

### Outer abelianization and central sign

[Kawazumi](https://arxiv.org/abs/math/0505497), formula (6.5) and Theorem 6.2, PDF p.26, give the equivariant outer quotient. The IA theorem's proof on p.25 was also visually inspected. With H=Q^4, the precise module is

\[
H_1(\operatorname{IOut}_4;\mathbb Q)
\cong (H^*\otimes\Lambda^2H)/j(H),\qquad j(v)(h)=v\wedge h.
\]

The report correctly removes inner automorphisms. Its contraction convention gives Cj(v)=−3v at rank four, so j is injective and the quotient has dimension 24−4=20. The tensor, quotient, and dual cohomology module all have scalar −1 action by central −I. Equivariance follows from the primary outer theorem, without any stable-range hypothesis. This is H^1 of the outer Torelli group, not an uncorrected 24-dimensional IA module.

Averaging over the finite central subgroup {I,−I} then kills all H^p(GL_4(Z);H^1(N;Q)). The argument remains valid for arbitrary-dimensional characteristic-zero modules; it does not require algebraicity or finite-dimensionality.

## 2. Theorem A: page indexing and exact filtration

Use cohomological differentials d_r:(p,q)→(p+r,q−r+1). The following checks independently reproduce the report's formulas.

1. At (0,4), no incoming differential exists. The d_2 and d_3 targets are (2,3) and (3,2). The d_4 target (4,1) vanishes by the zero row, and the d_5 target (5,0) vanishes by H^5(GL_4;Q)=0. Later targets leave the first quadrant. Thus the edge image is exactly ker e inside ker a inside V.
2. At (3,2), the d_2 outgoing target (5,1) is zero. The d_2 incoming map is b from (1,3). Hence E_3^{3,2}=coker b, rather than the raw H^3(GL_4;H^2(N)). There is a possible d_3 outgoing map to (6,0); it does not alter this E_3 identification or the domain of e. The report does not incorrectly promote the entire E_3 target to E_infinity.
3. At (1,3), there are no incoming maps. After b, remaining targets (4,1) and (5,0) vanish. Consequently E_infinity^{1,3}=ker b.
4. At (2,2), the only incoming map is c from (0,3). Outgoing targets (4,1) and (5,0) vanish. Consequently E_infinity^{2,2}=coker c.
5. On total degree four, positions (3,1) and (4,0) vanish. The decreasing filtration has F^3=0, F^2=coker c, F^1/F^2=ker b, and ker r=F^1. This yields the stated natural short exact sequence. No natural splitting is claimed or needed.

The four-condition isomorphism criterion follows, as does the sum of the three associated-graded dimensions being one. Their finiteness follows from the known total group, not from an assumed finite-dimensional E_2 page. In particular this argument leaves all actual values of a,b,c,e undetermined.

## 3. Theorem B: duality and real coefficients

The universal-coefficient identifications with the full algebraic dual are correct over a field, without a finite-type hypothesis. Invariance of a functional is equivalent to annihilating all differences γx−x. Thus invariant cohomology is dual to homological coinvariants, not to invariant homology. Inclusion factors through these coinvariants because ambient conjugation acts trivially on ambient homology.

The proof that an arbitrary vector-space map is an isomorphism exactly when its algebraic dual is an isomorphism is valid. A nonzero kernel vector is detected by a functional, and a nonzero cokernel has a nonzero functional. This uses standard vector-space extension of functionals and does not incorrectly invoke finite-dimensional double duality.

The real formula is Hom_Q(W,R). In particular, W≅Q implies the invariant real cohomology is a real line. General interchange of tensoring with R and taking infinite-dimensional cohomology or invariants is not used. The source's rational dimension one does justify its own real one-dimensionality. The scalar-normalization conclusion still requires nonvanishing of the specified torsion class.

## 4. Theorem C: abelian cycles and orientation

The subgroup embedding in Out(F_n) is valid. A product fixes x_1 and x_2, so if it is inner the conjugating word lies in the trivial intersection of their cyclic centralizers. Free-product normal form then forces every left and right exponent to vanish. Commutativity follows because the generators fix w=[x_1,x_2].

Inverting x_3 exchanges L_3 with R_3^{-1} and R_3 with L_3^{-1}; all other generators are fixed. The corresponding lattice block has determinant −1, so the torus's top homology changes sign. The quotient GL_n(Z) action is well defined on Torelli homology, and rational coinvariants therefore kill its image. Ambient homology also kills it because this conjugation becomes inner. Conjugating the construction proves the same statement for all ambient Out(F_n)-conjugates. Evaluation detects the top cohomology of the free abelian subgroup, so vanishing of the pairing gives vanishing of restriction.

[Bestvina–Bux–Margalit](https://arxiv.org/abs/math/0603177), PDF pp.2,23,24, were visually checked. The source identifies its independent torus family using conjugates of the displayed subgroup and proves injectivity of top homology from its toy model. It does not assert surjectivity onto all Torelli top homology. The report maintains this essential distinction. Its conclusion eliminates a proposed detection family and does not calculate all relevant coinvariants.

## 5. Theorem D and conditional FI

With normalized cochains, H^5(GL_4;R)=0 supplies x with δx=b, and positive-degree restriction of p*x to the kernel is zero. Every solution z differs from p*x by a closed cochain. Conversely every closed cochain gives such a solution. Hence the set of restricted primitive classes is exactly im r_R, including zero. This is a correct statement about unrestricted primitive choices; it does not identify those choices with canonical Igusa torsion.

The real vanishing follows from rational vanishing by universal coefficients: the rational homology is zero because its rational dual is zero, so its real-valued dual is also zero. No finiteness assumption is needed.

Under FI, naturality makes the pulled-back degree-four fiber class survive d_2,d_3,d_4, with zero d_5. First-quadrant degree bounds then give permanence. Nonzero torsion in the real edge image implies nonzero, hence injective, restriction from the rational source line. This conditional proof is correct. The universal Whitehead-space diagram in [Morita–Sakasai–Suzuki](https://arxiv.org/abs/1512.06365), PDF p.8, was visually inspected, but Igusa's book and the full low-rank fibration-level compatibility were not independently inspected. FI therefore remains a hypothesis, not an accepted unconditional theorem of this packet.

## 6. Stable and current-source boundaries

The report preserves the relevant limitations:

- [Habiro–Katada](https://arxiv.org/abs/2211.13458), Conjectures 8.1–8.2, Remark 8.3, and Theorem 8.4 on p.26 concern conditional stable outer invariants. Their p.17 discussion explicitly records unknown torsion nontriviality in the inspected version. These are not rank-four computations.
- [Katada](https://arxiv.org/abs/2404.15901), Theorem 1.1 on p.2, computes Albanese homology of IA_n for n≥3i; degree four requires n≥12. Its whole-cohomology statement still has an algebraicity hypothesis.
- [Lindell](https://arxiv.org/abs/2404.06263), Theorem A and Corollary 1.7 on p.3, distinguish Borel-vanishing hypotheses and the algebraic part of stable degree-two IA cohomology. The report preserves this restriction.
- The retained [Gaifullin manuscript](https://arxiv.org/abs/2606.13517) concerns surface Torelli groups and symplectic quotients. Its abstract/first-page text was checked for this exclusion only; its proofs were not audited.
- Morita–Sakasai–Suzuki's Proposition 3.1 primitive-independence bound is n≥2k+4, hence n≥6 for degree four. It does not justify unrestricted rank-four primitive independence.

A short additional public search found no inspected exact resolution. Search snippets and aggregators were not used as mathematical evidence. These bounded searches cannot certify that the original problem remains open today.

## 7. Remaining proof boundary

A solution still requires actual unstable differential information or an equivalent computation of the inclusion map from H_4(N;Q)_Gamma, as well as nonzero canonical torsion. No sufficient cycle with nonzero ambient or torsion pairing is supplied. No extra invariant is supplied. The appropriate disposition is an accepted partial reduction with full target unresolved; claiming an isomorphism, a counterexample, exhaustive homology generation, or unconditional FI would exceed the evidence.

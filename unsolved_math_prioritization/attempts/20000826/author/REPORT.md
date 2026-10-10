# Connected multigraded Hilbert schemes in three variables

Problem ID: 20000826 · AIM-ARITHMETIC_GEOMETRY-0072 · queue rank 761  
Research checkpoint: 2026-10-05 UTC  
Disposition: **partial results and a material literature update; the main question is not solved.**

## Target recovered

The controlling source is Problem 25 on page 3 of the AIM workshop *Components of Hilbert schemes*, held July 19–23, 2010. It asks whether the multigraded Hilbert scheme for every grading and admissible Hilbert function in a polynomial ring with three variables is connected. The problem does not state a positivity, characteristic-zero, finite-length, or toric-Hilbert-function restriction. The adjacent remark asks for disconnected examples using fewer variables than Santos's 26-variable construction.

The catalog title, “Connected toric and square-zero classes in three variables,” describes the imported attempt's partial results; it is not the original question. The full imported report was inspected, rather than treating that title or its summary as the target. Its exact source location agrees with the primary PDF. No existing target-specific attempt directory or target-ID pull request was found in the repository reads made for this checkpoint. This is a bounded repository search, not a claim that every historical branch was searched.

Write S=k[x,y,z], let A be an abelian group, and fix an A-grading and h:A→N. H_S^h parametrizes homogeneous ideals I with locally free quotient pieces of ranks h(a), including over nonreduced base rings. The target concerns connectedness of this entire parameter scheme. Our positive results below explicitly name their additional hypotheses.

## What changed after the imported attempt

**Five variables now suffice in a published preprint.** Yairon Cid-Ruiz, *Disconnected multigraded Hilbert schemes on P²×P¹*, arXiv:2608.07704v1, submitted August 7, 2026, gives disconnected examples for the standard bigrading on a five-variable polynomial ring (Corollary 2.8). Theorem A first proves disconnectedness for the polynomial p_a(u,v)=2au+av+3a−2a², a≥2, on P²×P¹ over any field. Its complete-intersection locus is both open and closed and has a point outside it. Uniform multigraded regularity transfers the construction to a fixed-Hilbert-function scheme. This answers the workshop's request for fewer variables in the general multigraded setting. It is not a toric-Hilbert-function construction and does not settle the three-variable question. The inspected arXiv record lists v1 and no journal reference; no peer-review claim is made. [CR26]

The imported report's July 29, 2026 literature search predates this manuscript. Its statement that no smaller example was located must not be carried forward as current evidence. Nor does five give a proved minimum: two-variable schemes are smooth and irreducible, while this investigation does not resolve three or four variables.

## Five approaches and their exact outcomes

### 1. Lattice rank and the toric special case

For the toric function, h is one in every monomial degree, rather than an arbitrary function. If the grading is positive, its kernel lattice L⊂Z³ satisfies L∩N³={0}, so rank L≤2. Rank zero gives a point; rank one gives P¹ by the principal-binomial family; rank two is covered by Maclagan–Thomas, Theorem 1.1. Thus the positive toric case is smooth and geometrically irreducible. The cited rank-two theorem itself is more general than positive gradings; its paper works over arbitrary infinite fields, so geometric conclusions over any field follow after algebraic closure. [MT03]

**Obstruction:** lattice rank does not change arbitrary h into the toric function. Also a nonpositive grading may have rank-three kernel. This route does not prove the full target.

### 2. Standard grading and deformation to lex

For the standard total-degree grading, fixed-Hilbert-function connectedness is classical. An inspected exposition by Peeva, §9, describes deformation to the lex ideal while preserving the Hilbert function, under its standing ground field C. This is substantially broader than the imported attempt's one-dimensional quotient ray family. The original Pardue paper was located bibliographically but its PDF could not be inspected because the host returned a blocking page. We do not promote a stronger characteristic statement on the basis of that failed retrieval. [P22; Pa96]

**Obstruction:** general coordinate changes mix variables of different A-degrees. For example x↦x+y does not preserve a grading with deg(x)≠deg(y). Connectedness of a coarsened standard-graded parameter space does not imply connectedness of a closed refined-grading locus. The all-characteristic cubic proof in PROOFS.md is an elementary control, not a novelty claim.

### 3. Extend square-zero quotients to positive weights at most two

Let λ:A→Z satisfy λ(deg x_i)>0. If h(0)=1 and h(a)=0 outside weights 0,1,2, then H_S^h is either empty or a product of relative Grassmannians over a product of Grassmannians. Variables of weight two may share their A-degree with quadratic monomials; this resonance is allowed. The vector bundles and exact admissibility inequalities are given in Theorem 1 of PROOFS.md.

Consequently every nonempty scheme in this class is smooth and geometrically irreducible over any field. In the standard grading this specializes to

H_(1,r,s) ≅ Gr_B(s,Sym² Q),  B=Gr(r,3),

with dimension r(3−r)+s(r(r+1)/2−s). For weights (1,1,2), the relevant second-stage bundle is O⊕Sym² Q. This completes the imported attempt's proposed next layer, while giving the full scheme instead of a pointwise classification.

**Obstruction:** at weight three, multiplication of the varying quadratic kernel need not have constant rank. The subspaces span{x²,y²,z²} and span{x²,xy,xz} both have dimension three, but their products with S_1 have dimensions nine and six. An unrestricted third layer is therefore not a Grassmann bundle of fixed rank. These are exact monomial counts, not evidence of disconnectedness. This elementary classification is not claimed to be new.

### 4. Cubic contraction and a graph control

For the standard grading in n variables, every nonempty Hilbert scheme with function (1,r,s,1), zero afterwards, is geometrically connected for 1≤r≤n and 1≤s≤r(r+1)/2. A self-contained proof in PROOFS.md uses the dual of multiplication, not ordinary derivatives, and so also works in characteristics two and three. Its base is the irreducible locus of cubic functionals with contraction rank at most s; fibers are Grassmannians. It proves connectedness, not smoothness or irreducibility.

This distinction matters: the standard-graded (1,3,2,1) example has two irreducible components in the characteristic range treated by Cartwright–Erman–Velasco–Viray. [CEVV09] The independent finite-field checks here include characteristics two and three but do not assert their component decomposition.

For a genuinely finer grading, the Haiman–Sturmfels nine-point example is the scheme a_1 b_1=0 in P¹×P¹, hence two projective lines meeting once. Its three monomial points form a connected graph. The verification code checks all rational parameter points over F₂, F₃ and F₅ and every possibly nonzero multidegree. [HS04]

**Obstruction:** a Gröbner degeneration connects each ideal to a monomial ideal, but not automatically all monomial ideals to each other. An edge filter that supplies only necessary conditions is not an edge existence proof. No exhaustive graph certificate for all three-variable h was found.

### 5. Test the new disconnected construction and possible dimension reduction

The two monomial ideals in the five-variable construction have the same eventual bivariate polynomial but different small-degree Hilbert functions. The code verifies the ideal intersection, equality with p_a in a stable rectangle, and the low-degree mismatch. The equality of parameter schemes in [CR26, Corollary 2.8] uses a suitable uniform truncation, not the assertion that the original two saturated ideals have the same full Hilbert function. [MS05, Theorem 6.2 and proof]

Setting the two unused homogeneous coordinates equal to one gives ideals in three variables, but destroys the original homogeneous construction. Even if the surviving monomials are assigned the evident bigrading again, the two resulting quotients have degree-(1,0) dimensions one and two. Thus this direct dehomogenization is not a counterexample to Problem 25. No impossibility of other reductions is claimed.

## Sharper remaining boundary

Hering–Maclagan, Theorem 1.1, proves that every positively graded multigraded Hilbert scheme is equivariantly isomorphic to one with finite-support Hilbert function; the result holds over an arbitrary base ring. Their proof truncates beyond a very supportive degree set. Thus the entire positive-grading question can be reduced to finite length, with no reduction in variable number. Their introduction also states the equivalence with connectedness of the T-graph for positive grading over C. These are reductions, not proofs that the graph is connected. [HM12]

The unresolved task is to establish a grading-preserving connectedness mechanism for arbitrary admissible h in three variables, or to exhibit and certify a disconnected scheme. In the positive case it suffices to do this at finite length, but the cutoff is not uniformly two or three. Nonpositive gradings require additional treatment and must not be silently omitted.

## Terminology and evidence limits

- Connected refers to the Zariski topology of the parameter scheme; the proved geometric statements remain true after algebraic field extension. No assertion about path connectedness of k-rational points is inferred for general k.
- Irreducibility is stronger. The two-lines and (1,3,2,1) examples prevent substituting it for connectedness.
- A Gröbner stratum, the full torus-fixed locus, a punctual Hilbert scheme, and a fixed-h multigraded Hilbert scheme are different spaces. Connectedness of one is not automatically inherited by another.
- The square-zero hypothesis concerns the positive-degree ideal of the quotient; finite length alone does not make it square-zero.
- Exact finite computations are controls for stated families and identities. They are not a search of all Hilbert functions and do not establish the primary problem.
- The literature assessment is a targeted search through 2026-10-05, not an exhaustive proof that the problem remains open.
- The safe package contains authored reports, proofs, deterministic code and public verification metadata only. Source PDFs, extracts, corpus records and coordination material are excluded.

## References

- [AIM10] *Components of Hilbert schemes*, workshop problem list, Problem 25, p. 3. https://aimath.org/WWN/hilbertschemes/hilbertschemes.pdf
- [HS04] M. Haiman and B. Sturmfels, *Multigraded Hilbert Schemes*. https://arxiv.org/abs/math/0201271
- [MT03] D. Maclagan and R. R. Thomas, *The toric Hilbert scheme of a rank two lattice is smooth and irreducible*. https://arxiv.org/abs/math/0208031
- [MS10] D. Maclagan and G. G. Smith, *Smooth and irreducible multigraded Hilbert schemes*. https://arxiv.org/abs/0811.3594
- [HM12] M. Hering and D. Maclagan, *The T-graph of a multigraded Hilbert scheme*. https://arxiv.org/abs/1110.1861
- [San05] F. Santos, *Non-connected toric Hilbert schemes*. https://arxiv.org/abs/math/0204044
- [CR26] Y. Cid-Ruiz, *Disconnected multigraded Hilbert schemes on P²×P¹*, preprint v1. https://arxiv.org/abs/2608.07704v1
- [MS05] D. Maclagan and G. G. Smith, *Uniform bounds on multigraded regularity*. https://arxiv.org/abs/math/0305215
- [P22] I. Peeva, *Syzygies over a Polynomial Ring*, §9. https://pi.math.cornell.edu/~irena/papers/syz.pdf
- [Pa96] K. Pardue, *Deformation classes of graded modules and maximal Betti numbers*. https://doi.org/10.1215/ijm/1255985937 (original PDF not inspected)
- [CEVV09] D. Cartwright, D. Erman, M. Velasco and B. Viray, *Hilbert schemes of 8 points*, §3. https://arxiv.org/abs/0803.0341

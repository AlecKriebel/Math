# Independent audit: K3 Problem 3.46

## Decision and scope

**Accepted as a correct partial-result and failed-reduction report. The connected original problem remains unsolved by this attempt. No correction to the frozen author report is required.**

The inspected author archive is bound by SHA-256 `4fce64f159ae10cebc4d89ba47d8c0f28cecb8ab940952331137415f865c5cfc`, 9,990 bytes, and external-manifest SHA-256 `d7332855f96826013ce7c6024b036da3742783c53993f8c2e0bffc88c9dbae8d`. All six text/data members were inspected. The original archive was not edited. This audit is an independently authored supplement, not a replacement solution.

The accepted proposition says that if a smooth contact form on a closed connected three-manifold has finitely many simple Reeb trajectories, then its period homomorphism on **integral** homology relations has nondiscrete image. Consequently the number of simple orbits is at least two more than the rational rank of their homology span. The argument is a deduction from established ECH inputs. Its mechanism has acknowledged prior art; this audit establishes neither novelty nor new progress on the unrestricted conjecture.

## 1. Original statement and current theorem hypotheses

K3 printed page 164 was independently rendered and inspected. The displayed question omits connectedness, while its remarks describe removal of the simultaneous nondegeneracy and Chern-class restrictions as outstanding. On the intended connected interpretation the author's scope is correct. A disjoint union of two irrational ellipsoid boundaries has four simple periodic trajectories and is not a lens space. That observation addresses only the literal disconnected wording. It is not an answer to the connected question. [K]

The known inputs are properly separated:

- The lower bound of two applies without a nondegeneracy assumption. [O, Theorem 1.1]
- Exactly two simple orbits force a lens space and in fact irrational ellipticity/nondegeneracy. The convention includes the three-sphere and excludes S^1 x S^2. [T, Theorem 1.2, Corollary 1.3, footnote 1]
- The nondegenerate dichotomy permits nontorsion c1. Nondegeneracy concerns every iterate, not just simple trajectories. The cited broken-book theorem actually holds on a C1-open neighborhood of nondegenerate Reeb fields. [B, Theorem 1.2]
- The modern theorem without nondegeneracy assumes torsion c1. Its Theorem 1.1 is for closed connected three-manifolds; Section 1.4 retains removal of the torsion condition as a question. [I]

The latter statements were checked in the specified arXiv v2 and independently against its current abstract and HTML. The final publisher PDF was not inspected. The newer survey still asks the unrestricted connected question and identifies the Chern contribution to the topological complexity estimate as the obstacle. [S, Question 8.1] Bounded searches on 6 October 2026 found no verified later unrestricted theorem. This is not an exhaustive literature-absence certificate.

Thus a finite connected non-lens counterexample would need at least three simple trajectories, nontorsion c1, and some degenerate orbit, possibly only an iterate. Those three conditions are necessary, not sufficient.

## 2. ECH inputs: existence, grading, spectrality, and strictness

Write xi = ker(lambda). It is legitimate to choose an integral class Gamma with c1(xi) + 2 PD(Gamma) torsion, even when c1(xi) itself is nontorsion. Existence and a homogeneous nonzero U-sequence in that same class are explicitly supplied by the proof of [O, Corollary 2.2]. The construction does not assume that the contact invariant in Gamma=0 is nonzero. In particular, no tightness or fillability hypothesis has silently been introduced.

For U sigma_(k+1) = sigma_k, the integer grading increases by two. The spectral volume theorem therefore gives c_k^2/k tending to twice the positive contact volume. The proof uses only its weaker consequence c_k/k -> 0. A finite shift of the indexing or grading normalization changes neither limit. The grading condition is torsion of c1 + 2 PD(Gamma), not torsion of c1 alone. The spectrum extends to degenerate forms by continuity. These are precisely the hypotheses in [O, Section 2.5, Theorem 2.1 and Corollary 2.2]; see also [I, Propositions 2.10 and 2.12].

The needed inequality is c_(k+1) > c_k. The author correctly invokes [O, Lemma 3.1(b)], which allows degeneracy **under the finite-simple-orbit assumption**. Merely passing the strict nondegenerate inequality to a limit would give only a weak inequality and would not suffice. The author does not make that mistake. Nor is there a uniform positive action gap claimed: such a claim would contradict the sublinear growth. Strictness is established separately for each nonzero U-step, and the hypothetical discrete period subgroup supplies a uniform gap only in the contradiction argument.

The 2014 exposition's Fact 5 has broader informal wording. The author relies on the precise finite-orbit lemma in [O], so that wording is not imported as an unrestricted strictness theorem. Spectrality in the fixed class is also recorded by [P, Fact 2].

### Degenerate spectrality preserves integral homology

Here is a detailed independent check of the compactness step. Fix k and choose smooth positive f_j -> 1 in C-infinity with f_j lambda nondegenerate. Their Reeb fields converge smoothly to the nonvanishing Reeb field of lambda. Spectral continuity bounds their spectral actions by a common A. For each j choose a spectral orbit set of total class Gamma.

There is a common positive lower bound tau for periods of all sufficiently close fields. To see why, cover the compact manifold by finitely many smaller flow boxes. In each larger box a coordinate function has strictly positive derivative along the limiting field and, after shrinking the neighborhood of that field, along all nearby fields. Uniform speed bounds give a common short time in which a trajectory beginning in a smaller box stays in the corresponding larger one. Such a trajectory cannot close during that time. This excludes periods tending to zero.

An orbit set of action at most A therefore has at most A/tau components counted with multiplicity. Pass to a subsequence with constant number of simple components and constant positive integer weights. The periods, initial points, and parametrized loops of each component have convergent subsequences. Their positive limiting periods yield nonconstant Reeb loops for lambda. Each limiting loop is a positive iterate of one of the finitely many simple trajectories. The limiting covering orders are also bounded, since their underlying simple periods are positive.

Parametrize all loops on S^1. Uniformly close loops are freely homotopic by short geodesics in a fixed Riemannian metric, regardless of whether the limit loop is multiply covered. Consequently their **integral** homology classes agree for sufficiently large j, including torsion information. After combining components with the same simple limiting trajectory, one obtains n(k) in Z^m_(>=0) with H(n(k))=Gamma and action c_k. No ECH admissibility restriction is imposed on these degenerate limits; it is not needed. The possible empty orbit set causes no problem. If Gamma is nontorsion it cannot occur.

This argument keeps k fixed while extracting the subsequence. It does not require a common subsequence for all k or an action bound independent of k. It produces a separate finite vector for every spectral value, which is exactly what the lattice proof needs.

## 3. Integral relation lattice and nondiscrete period image

Let H: Z^m -> H_1(Y;Z) send the ith basis vector to the ith simple orbit class. Let L=ker H and ell(n)=sum n_i a_i. For the vectors just constructed, n(k)-n(1) lies in L, so every c_k-c_1 belongs to ell(L).

If ell(L)=0, strict growth is already impossible. Any nonzero discrete additive subgroup of R is delta Z for delta>0. The spectral values would then lie in the same coset c_1+delta Z and strict increase would imply c_k >= c_1+(k-1)delta. Dividing by k contradicts c_k/k -> 0. This proves nondiscreteness. A subgroup of R which is not discrete has arbitrarily small positive elements; integer multiples of these approximate every real number. Hence the image is dense.

The word integral matters. Let L_sat consist of integral vectors whose homology image is torsion. Then L_sat/L is a finite subgroup of the torsion subgroup of H_1(Y;Z). It need not be zero. For example, a single order-two homology class gives L=2Z and L_sat=Z. Spectral differences belong to the smaller actual kernel L because integral homology was preserved. Thus the argument does not lose a torsion congruence condition by rationalizing prematurely.

Since H_1(Y;Z) is finitely generated, tensoring the exact sequence 0 -> L -> Z^m -> im(H) -> 0 with Q gives rank(L)=m-r, where r=dim_Q im(H tensor Q). Torsion affects the lattice index, not this rank. A rank-zero or rank-one free abelian group has a zero or cyclic real image, necessarily discrete. Therefore m-r>=2.

This last implication is one-way. Rank at least two alone does not imply a dense real image: Z^2 mapped by (p,q) -> p+2q has discrete image. Neither rational dependence among the orbit homology classes nor the rank bound alone substitutes for the spectral contradiction. Conversely, a dense finitely generated real subgroup is completely possible: integer combinations of 1 and sqrt(2) are dense. The conclusion is a restriction, not an impossibility for every finite configuration.

Finally Gamma is represented by n(1), so its rational class lies in the orbit span. Rationalizing c1+2PD(Gamma)=torsion gives PD^(-1)c1=-2Gamma. A nontorsion Chern class therefore forces r>=1. Combined with m-r>=2, a hypothetical three-orbit example has r=1. The report does not claim an integral equality before rationalization and does not claim that such abstract data are dynamically realizable.

## 4. The J0 sign and the limits of regrading

The displayed equation (2.13) in [I] was independently rendered and read visually; the enclosing minus sign applies to the complete parenthesis 2c_tau + CZ_top(alpha) - CZ_top(beta). Thus the author's expansion has the correct signs. This matters because text extraction of that equation can lose its parenthesis.

For a closed class A and fixed orbit ends, the Chern ambiguity is <c1,A>, the intersection ambiguity is <2PD(Gamma),A>, and all endpoint Conley-Zehnder terms cancel in differences. Consequently the changes in I and J0 are respectively

    <c1 + 2PD(Gamma), A>,
    <-c1 + 2PD(Gamma), A>.

After choosing the grading class, the first vanishes and the second is -2<c1,A>. The universal coefficient theorem for a closed manifold identifies the kernel of evaluation H^2(Y;Z) -> Hom(H_2(Y;Z),Z) with a finite torsion group. Therefore nontorsion c1 pairs nontrivially with some integral A. Adding arbitrary positive and negative multiples of A makes J0 unbounded in both directions while keeping I and the ends fixed. Closed additions have zero integral of d(lambda), which is exact.

These are topological relative classes, not asserted holomorphic curves. The standard ECH relative-homology set permits adding any closed two-cycle; one must not replace it by an unrelated quotient that kills endpoint cycles. The report uses the correct ECH setting. Its conclusion is that a bound on J0 does not follow merely from fixed ends, their actions, and fixed I. It does not rule out a new geometric estimate for actual U-curves and does not assert that every topological class has a holomorphic representative.

## 5. Finite-cover and approximation approaches

### Finite covers

For a finite covering of positive degree d, cohomological transfer composed with pullback is multiplication by d. Over Q, pullback is injective. Naturality then preserves a nonzero rational c1. The argument needs neither a regular cover nor a claim that c1 is primitive. It applies to the pulled-back contact structure; it says nothing about changing to an unrelated contact structure or using an infinite cover. The author keeps those limits explicit.

### Smooth approximation

The ellipsoid model is correctly normalized. On the unit three-sphere, the weighted Liouville form has Reeb field (2/a)partial_theta1+(2/b)partial_theta2. The contraction equation holds on tangent vectors because r_1^2+r_2^2 is constant there. If a/b is irrational, a trajectory with both coordinates nonzero cannot close. The two coordinate trajectories have periods pi a and pi b, and transverse irrational rotation ratios, so all their iterates are nondegenerate. Smoothness at the axes follows from r_j^2 dtheta_j=x_j dy_j-y_j dx_j.

Irie's density theorem is explicitly generic in the positive conformal factors [D, Theorem 1.1]. One should not infer residuality inside a conformal slice merely from residuality in the larger space of all contact forms. The requisite stronger standard fact is available directly: Albers-Bramham-Wendl [A, Theorem A.1] gives Baire nondegeneracy in positive conformal factors, including multiple covers; apply it with U=M. This independently corroborates the author's intended genericity input.

The space of positive smooth factors is an open subset of a Frechet space and is Baire. The two residual sets therefore have dense intersection, allowing a sequence approaching the constant factor 1. Each approximant has a dense union of periodic trajectories; a finite union of embedded circles is closed with empty interior and cannot be dense in a three-manifold. The limit has exactly two. Thus even convergence to a nondegenerate limit does not preserve infinitude. This happens on S^3, so it only refutes the unrestricted limiting inference, not the desired non-lens theorem.

## 6. Integrity, reproducibility, and limitations

The three supplied complete corpus files were independently read. The target record is unique and its rank is 860. The research-report key is absent and is represented by an empty object. The complete-pair hash agrees with the catalog when using sorted keys and Python's otherwise default JSON serialization: SHA-256 `d6c73d5a888d1ae469ca1ee59f4f83184fd7319d8a4fc7c3314f8bf7950dfb8a`, 5,993 bytes. No corpus contents are distributed in this audit.

A separate independent data inspector validates the trusted external-manifest digest before using it, checks the archive digest and exact file inventory, rejects duplicate ZIP members and unsafe entry types, validates UTF-8 and strict duplicate-key-free finite JSON, and checks the internal manifest and terminal classification. It never imports or runs an archive member.

The author archive passed five independent positive replay configurations, including isolated normal and optimized Python, relocation with an unrelated hostile working directory and PYTHONPATH, and an irrelevant external bytecode cache. Twenty-nine negative controls were rejected. Some controls preserve the original trust anchor; others intentionally repin a synthetic manifest to exercise deeper parser and classification rejection rather than stopping at a hash mismatch. The full control suite was also run under optimized Python. Original author-validator normal and optimized runs both passed.

Those results validate specified bytes and parser behavior, not the truth of ECH theorems. No formal proof assistant was used. Package-internal entrypoint, import, and cache execution controls are inapplicable because the archive contains only Markdown and JSON. No third-party PDF/text, dataset contents, private sources, or coordination files are included. Source hashes identify locally inspected PDFs; they do not certify publisher-version equivalence. The author freeze's historical PENDING audit labels are intentionally left unchanged; this separate acceptance record supplies the later independent result.

## References

- [K] Baykur, Kirby, Ruberman, K3: A New Problem List in Low-Dimensional Topology, Problem 3.46. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [O] Cristofaro-Gardiner and Hutchings, From one Reeb orbit to two, arXiv:1202.4839v4. https://arxiv.org/abs/1202.4839v4
- [T] Cristofaro-Gardiner, Hryniewicz, Hutchings, Liu, Contact three-manifolds with exactly two simple Reeb orbits. https://arxiv.org/abs/2102.04970 ; https://doi.org/10.2140/gt.2023.27.3801
- [B] Colin, Dehornoy, Rechtman, On the existence of supporting broken book decompositions for contact forms in dimension 3, arXiv:2001.01448v4. https://arxiv.org/abs/2001.01448v4
- [I] Cristofaro-Gardiner, Hryniewicz, Hutchings, Liu, Proof of Hofer-Wysocki-Zehnder's two or infinity conjecture, arXiv:2310.07636v2. https://arxiv.org/abs/2310.07636v2 ; https://doi.org/10.1090/jams/1072
- [S] Cristofaro-Gardiner, Low-dimensional topology and symplectic dynamics, arXiv:2510.07680v1, Question 8.1. https://arxiv.org/abs/2510.07680v1
- [D] Irie, Dense existence of periodic Reeb orbits and ECH spectral invariants, arXiv:1508.07542v2. https://arxiv.org/abs/1508.07542v2
- [P] Cristofaro-Gardiner and Pomerleano, A guest post by Dans C-G and P, 24 November 2014. https://floerhomology.wordpress.com/2014/11/24/a-guest-post-by-dans-c-g-and-p/
- [A] Albers, Bramham, Wendl, On nonseparating contact hypersurfaces in symplectic 4-manifolds, Algebraic & Geometric Topology 10 (2010), 697-737, Appendix A, Theorem A.1. https://msp.org/agt/2010/10-2/agt-v10-n2-p05-s.pdf

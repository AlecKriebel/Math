# Adversarial review of high Cartier index boundary rigidity

Checkpoint: 2026-10-06 22:53 PDT (2026-10-07 05:53 UTC). Completion estimate: 100% of this scoped adversarial review; this is not a percentage of foundational theorem certification or novelty clearance. Reviewed artifact: `agent_notes/boundary_rigidity_completion.md`, SHA-256 `c28a0e3d9478c3981a49c9183a546e97c994f57f077e1aac96730775f92f2e6f`, independently rechecked unchanged during review. This agent created only this review, performed no Git or publication operation, and communicated with no external individual.

## Verdict

**Conditional pass.** I found no counterexample or logical gap in the precise positive-dimensional high Cartier index theorem, or in the holomorphic/antiholomorphic isometry and cubic polarization conclusion for the stated polarized GH boundary in dimension at least five. The arguments below independently reconstruct the critical deductions and identify why the attempted attacks fail.

This verdict accepts the stated standard splitting, vanishing, reflexive extension, GAGA, and GH algebraization/regularity results as dependencies. I checked exact source statements at their relevant locations; I did not independently certify the full proofs of those foundational papers. The identification with the entire cubic GIT quotient remains conditional on the separately audited complex/polarized GH/GIT comparison. No first-disclosure, novelty, dimension-four classification, arbitrary nonsmoothable metric-completion theorem, or publication authorization follows from this review.

The Chen–Lai comparison is substantively correct with a careful distinction: their Corollary 1.11 can hold when their word “unstable” means failure of strict stability. The preceding assertion of failure of polystability is not established by that fact. The explicit quotient calculations here demonstrate polystability for the examples actually tested; they do not classify every surface with the same singularity count.

## Exact hypotheses and the product-cover attack

The claim requires a normal irreducible projective klt Fano of positive dimension, a weak KE current in the anticanonical class with bounded potentials and smooth positive metric on the regular locus, and an actual ample Cartier root

    omega_X^[-1] ≅ L^r,    r > n/2 + 1.

“Weak KE” must retain the anticanonical-class convention. Ricci equality only on an arbitrary open manifold, with no specified global current, is not a replacement hypothesis. Finite quasi-etale covers are understood to be finite surjective maps of connected normal varieties. These are standard conventions, not extra restrictions on the cubics under review.

[DGP, arXiv:2008.05352v1](https://arxiv.org/html/2008.05352), Theorem A and Definition 2.2, supply the needed cover by a product of KE klt Fanos with stable tangent sheaves. Remark 2.3 supplies quasi-etale metric pullback. Theorem 4.14 does not require the input variety to be Q-factorial; that condition occurs in an intermediate reduction. Its hypotheses are therefore compatible with the claim.

Let f:Y→X be that cover, write M=f*L, and consider Y=W×B. A regular closed point b of B gives an ample Cartier restriction A=M|_(W×{b}). On W_reg×{b}, the ordinary smooth canonical-bundle formula gives

    omega_Y|_(W_reg×{b}) ≅ omega_(W_reg) ⊗ det(T_b*B).

The last factor is a constant one-dimensional vector space. Consequently omega_(W_reg)^[-1] ≅ A^r there. Both the canonical divisorial sheaf on normal W and A^r have unique reflexive extensions, so omega_W^[-1] ≅ A^r globally. This defeats the possible objection that one restricted a non-Cartier canonical divisor through a singular slice. The calculation begins with a line bundle and restricts only the smooth canonical formula before extending. It also works for any algebraic product quasi-etale cover; its factors are klt by testing locally after adjoining smooth coordinates at b.

For d=dim W and 1≤j≤r−1, the Cartier divisor N=−jA has N−K_W=(r−j)A ample. The exact projective klt vanishing statement is [Hacon, Theorem 2.22](https://www.math.utah.edu/~hacon/7800/Math7800-2018.pdf); it yields H^q(W,−jA)=0 for q>0. Negative ampleness excludes sections: a nonzero section would give an effective divisor of negative intersection with A^(d−1), or trivialize a nontrivial negative ample line bundle. Hence chi(W,A^(−j))=0.

[Stacks, Lemma 33.45.1](https://stacks.math.columbia.edu/tag/0BEM) supplies a polynomial on all integer twists, not just the eventual positive Hilbert function. [Section 33.45, Lemma 33.45.9 and Definition 33.45.10](https://stacks.math.columbia.edu/tag/0BEL) give its degree d and positive leading coefficient A^d/d!. It has r−1 distinct negative roots, so d≥r−1. Two positive-dimensional factors imply n≥2(r−1), contradicting the strict bound. No volume or Picard-rank inference is concealed here.

I also checked stability descent. A hypothetical saturated destabilizing subsheaf restricts to a subbundle on a big smooth open set over which f is etale. Pullback and saturated reflexive extension give a proper subsheaf upstairs. A general complete-intersection curve of n−1 sufficiently ample Cartier divisors avoids the deleted codimension-two set. Its inverse image is a finite etale curve cover; vector-bundle degrees, and therefore slopes, multiply by deg f. There is no need for a Q-Cartier determinant downstairs. This contradicts stable T_Y. Every other quasi-etale cover retains the same root and weak KE hypotheses, so the same proof applies to it. The rigidity argument can also bypass descent entirely and use simplicity on the single DGP factor.

For a cubic, r=n−1, so n≥2n−4 would be necessary for splitting. It is impossible exactly when n≥5. The equality case is deliberately excluded.

## Local curvature and reflexive extension attack

Let I be another orthogonal parallel real complex structure for g and set eta(u,v)=g(Iu,v). Orthogonality and I²=−Id make eta skew; it is parallel. Since J is parallel, alpha=eta^(2,0) is parallel too. On the exterior cotangent bundle of a KE manifold, curvature contraction acts by −p lambda on (p,0)-forms, with the sign reversed under the opposite curvature convention. This follows by contracting each cotangent factor with Ric^sharp=lambda Id and summing over the p exterior factors. A parallel section is annihilated by curvature, so alpha=0 when lambda=1.

Reality eliminates eta^(0,2) as well. The resulting identity eta(Ju,Jv)=eta(u,v) is equivalent to −JIJ=I and hence IJ=JI. This proof is pointwise and remains valid on an incomplete manifold. It does not use integration, full U(n) holonomy, or a global vanishing theorem. A Ricci-flat hyperkähler example breaks this step at lambda=0, but does not meet the theorem's hypotheses.

Commutation makes I a complex-linear endomorphism of T^(1,0). Parallelness makes it holomorphic because the Kähler Levi-Civita connection is the Chern connection. Normality and reflexivity give the extension through the codimension-two singular set. More explicitly, if j is the regular-locus inclusion, T_X^an=j*(T_X^an|_reg); adjunction extends a morphism into this sheaf from the big open set. Equivalently, its analytic End sheaf is reflexive. No additional boundedness estimate for I is required. [Serre GAGA, Theorem 2, p.19](https://numdam.org/item/10.5802/aif.59.pdf) algebraizes the extended morphism of coherent sheaves.

There is a particularly direct simplicity check requiring no potentially ambiguous claim about surjectivity of arbitrary full-rank endomorphisms. The algebraic idempotents

    P_plus = (Id − iI)/2,    P_minus = (Id + iI)/2

split the reflexive tangent sheaf into the +i and −i eigensheaves. If both have positive rank, their slopes have weighted average mu(T_X). Stability forbids both slopes being strictly smaller than that average. Thus one idempotent is zero and I=+J or −J. The same check works upstairs on the one-factor cover and descends on f^−1(X_reg). The regular locus is connected because X is normal and irreducible; a separate componentwise sign ambiguity is unavailable.

## GH regularity, isometry extension, and polarization attack

[Donaldson–Sun II, arXiv:1507.05082v1](https://arxiv.org/pdf/1507.05082v1), Proposition 2.14, identifies metric and analytic singular loci in its polarized KE limit setting. Its opening definition includes polarization, the Einstein bound, and noncollapse. Normalized smooth KE cubics fit that setting: the anticanonical line bundle supplies the integral polarization, volume is fixed, and positive Ricci gives a diameter bound and uniform noncollapse. The algebraized limit topology is the metric topology by Proposition 2.3. Proposition 2.4 treats the bounded regular-locus function extension used below. These are applications to actual GH limits, not to every weak KE Fano.

An isometry therefore preserves regular loci. At a regular point choose relatively compact regular neighborhoods on both sides. Points sufficiently close to the center can be joined by short geodesics inside the neighborhood; a path leaving the larger neighborhood incurs a fixed positive length cost. Thus the completion distance locally agrees with ordinary smooth Riemannian distance. Local distance coordinates prove the isometry and its inverse smooth, and differentiation gives F*g_Z=g_X. No global completeness or assertion about global intrinsic distances of the regular locus is needed.

I=F*J_Z is orthogonal and parallel, so the preceding argument makes F holomorphic or antiholomorphic on X_reg. For the holomorphic case, take a local analytic embedding near F(p), and use continuity to keep F(U) in its chart. Each target coordinate composed with F is holomorphic on U∩X_reg, continuous and locally bounded on U. Normal extension gives holomorphic coordinates on U; density identifies them with the original continuous map and makes the target equations hold. Apply the same procedure to the inverse. For the other sign, use conjugate(Z) as target. [GAGA, Proposition 15, p.29](https://numdam.org/item/10.5802/aif.59.pdf) then makes the resulting compact analytic isomorphism algebraic. A merely birational map on a big open set would not have supplied the continuity needed here.

[SGA2, Exposé XII, Corollary 3.7 and Remark 3.8, p.121](https://pi.math.cornell.edu/~dkmiller/bin/sga2.pdf) provide the projective complete-intersection Picard assertion without a nonsingularity hypothesis. In the n≥5 cubic scope this yields Pic(X)=Z[H_X]. Preservation of the canonical bundle gives

    (n−1)(F*H_Z − H_X)=0,

and torsion-freeness gives F*H_Z=H_X. The same calculation applies with conjugate(Z). The cubic hypersurface sequence supplies h^0(H_X)=n+2 and its given complete embedding, so a polarized isomorphism is induced by a projective linear map. Neither a merely numerical anticanonical relation nor an arbitrary Fano root-uniqueness assertion was substituted.

With the complex/polarized GH/GIT comparison assumed, the metric quotient conclusion follows from these fibers, continuity, compactness, and the Hausdorff property. Conversely conjugating J and omega simultaneously preserves g. The uniqueness of the KE metric up to automorphism is part of the accepted complex moduli comparison, rather than a new claim proved by this local argument.

## Sharpness and the symmetric-square attack

At equality, P^(r−1)×P^(r−1) has n=2r−2 and −K=rO(1,1). The equal-normalization product FS metric admits conjugation of only one factor, whose pullback complex structure is (−J_1,J_2). Both factors have positive dimension for r≥2, so this is neither ±J. It is a valid sharpness counterexample to any non-strict general index statement.

For Sym²(P²), an unordered pair maps to the symmetric matrix uv^t+vu^t. Every rank-two symmetric quadratic form factors into two linear forms over C, and rank one gives a square; unique factorization gives the unordered inverse. The source quotient and determinant hypersurface are normal, so the induced finite birational map is an isomorphism. The pulled-back hyperplane bundle is O(1,1), and H^4=binomial(4,2)/2=3. The swap's fixed diagonal has codimension two, giving the quasi-etale KE quotient and adjunction −K=3H.

Partial conjugation does not preserve swap orbits: the conjugate of the swap by (c,id) is (c,c)tau, outside {id,tau}. Equivalently {cu,v} and {cv,u} are generically different unordered pairs. This eliminates that proposed cubic-fourfold counterexample. It supplies no exhaustive result for fourfolds.

## Chen–Lai: terminology, quotient calculations, and Figure 2

[Chen–Lai, arXiv:2601.18526v1](https://arxiv.org/html/2601.18526v1), Examples 1.4–1.6, use equal slopes to assert instability; Corollary 1.9 nevertheless asserts semistability. Thus “unstable” in those passages includes strictly semistable. Corollary 1.11 is compatible with DGP in that reading. The preceding sentence claiming failure of polystability does not follow. Figure 2 refers to Example 1.5 at n=1. These are exact v1 source statements; no claim about later corrections is made.

For the four-node surface, [OSS, Section 4.1](https://arxiv.org/html/1210.0858) identifies X=(P¹×P¹)/〈(iota,iota)〉 with iota(z)=−z. The factor tangent lines are invariant under the differential of the diagonal action. They descend on the free locus and extend as rank-one reflexive F_1,F_2; equality there extends to T_X=F_1⊕F_2. Upstairs each line has degree 4 against −K=(2,2), and the cover has degree two. Hence mu(F_i)=2=mu(T_X), proving polystability and nonstability directly.

For six nodes, let G be the diagonal Klein group generated by a(z)=−z and b(z)=1/z on both factors. The fixed sets on P¹ of a,b,ab are respectively {0,infinity}, {1,−1}, {i,−i}. They are disjoint. Each nonidentity group element fixes four pairs; each has stabilizer order two and derivative (−1,−1). Their twelve points give six quotient orbits, all A_1, and no branch divisor. The descended FS metric is weak KE, K_X²=8/4=2, and the same invariant factor tangent lines give mu(F_i)=4/4=1=mu(T_X). The group never interchanges the factors; the descent argument therefore cannot lose either summand.

I also independently checked the optional six-node equation. Homogenizations of

    U=z²w²+1,    V=z²+w²,    W=2zw,
    D=(z²−w²)(z²w²−1)

are invariant sections of O(2,2),O(2,2),O(2,2),O(4,4), respectively. The first three have no common zero: W=0 forces an endpoint on at least one factor, where U or V is nonzero. They define a morphism to

    D²=(U²−W²)(V²−W²) in P(1,1,1,2).

The four branch lines have no triple intersection, giving a normal degree-two del Pezzo with six A_1 points. Pullback of its Cartier O(1)=−K is O(2,2), which is ample, so the morphism is finite. Its degree is 8/2=4. Being G-invariant, it induces a finite birational morphism from (P¹×P¹)/G onto that normal surface, hence an isomorphism. This closes the possible gap between a polynomial identity and identification of the quotient. The existing `reproducibility/verify_boundary_examples.py` was inspected and run successfully; its exact arithmetic checks the polynomial identity and branch-line incidences, while the quotient and KE deductions above remain mathematical arguments.

Finally, Example 1.5 uses two 2-blowups, hence four ordinary blowups of F_1. Its smooth resolution has K²=4 and rho=6. The orthogonal complement of the positive-square anticanonical class in its Néron–Severi space has negative dimension five. Six disjoint exceptional (−2)-curves would give a rank-six negative-definite subspace there, impossible. Therefore the Figure 2 attribution cannot produce six A_1 points as written. This is consistent with a misnumbered example and is not evidence that the full paper is false.

## Source display errors and remaining boundaries

The [published DGP paper](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.612.pdf), p.101, prints zero slopes in a proof transition whose theorem statement and preceding second-fundamental-form calculation require equal tangent slopes. Replacing both zeros by mu(T_X)=c1(X)^n/n repairs it. In Claim 28, restoring the common multinomial coefficient n!/product(d_i!) in the volume and intersection product formulas leaves the factor-volume conclusion intact. I found no substantive new obstruction from these displays; this is a scoped check, not complete certification of the proof.

The strongest verified deduction is the high Cartier index parallel-complex-structure rigidity and its stated polarized GH cubic isometry/polarization corollary. Exact limits remain: the foundational theorems are dependencies; metric regularity outside their GH setting is unverified here; the full cubic complex compactification comparison and priority clearance belong to other audits. No outreach or immutable publication is warranted by this review alone.

## Version acceptance: explicit positive dimension

Checkpoint: 2026-10-06 22:55 PDT (2026-10-07 05:55 UTC). Completion estimate: 100% of this narrowly scoped revision check.

I independently checked revised `agent_notes/boundary_rigidity_completion.md`, SHA-256 `81a0b4a6200b17a62ebce124d8b5e6e7d37108379350c85723c4448e5201a832`. Its unique phrase `of positive dimension n>=1, with a weak KE current` replaces `of dimension n, with a weak KE current`. Reversing that single replacement reproduces the original reviewed SHA-256 `c28a0e3d9478c3981a49c9183a546e97c994f57f077e1aac96730775f92f2e6f`, proving there are no other byte-level changes.

The clarification excludes a point, whose rank-zero tangent sheaf is outside the usual definition of slope stability. It matches the positive-dimensional scope already stated in this review. The n>=5 cubic statement, proof, and conditional verdict remain unchanged. I accept the revised version within exactly the same scope and dependencies.

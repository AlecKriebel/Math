# Independent derivation and falsification record

Reviewed head: `4e8565e2ec24f20b039dd9ce0b06bb3980345d9a`. This derivation uses the seven frozen PR blobs, not the mutable main-tree title or an inferred solved status.

## The actual target

The original [AIM question 8](https://aimath.org/WWN/qptsurface2/qptsurface2.pdf), printed and physical page 48, fixes a number field K, an Enriques surface X, its specified K3 double cover p:Y→X, and m in X(A_K)^Br. It already speaks of an adelic lift P on Y, then asks for assumptions on m permitting a lift orthogonal to Br(Y), or at least Br₁(Y). Its next remark suggests a nonabelian torsor explanation. The following dated update reports failures even for Br₁-orthogonal lifting. These are distinct issues. An answer to the assumptions question need not prove automatic lifting, nor provide an algorithm. Conversely, a counterexample to automatic lifting is not a classification of sufficient lifting assumptions.

## A general lemma containing the PR theorem

Let p:Y→X be a finite étale double cover of proper smooth geometrically integral varieties over a number field. Let ι be its deck involution, and let A⊂Br(Y) contain Br₀(Y). Assume A/Br₀(Y) is finite. Suppose m∈X(A_K)^Br has a point in every local fiber of this fixed p. Set

    D = Br₀(Y) + (A ∩ p*Br(X)),   B = A/D.

Then B is finite. In fact Br₀(Y)⊂p*Br(X), since both constant maps factor through the structural morphism of X, so the constant summand is redundant. Its explicit inclusion is useful for reciprocity and finiteness. Nothing here assumes injectivity of Br(K)→Br(Y), injectivity of p*, or that p*Br(X)⊂Br₁(Y).

A rational point in a finite étale degree-two fiber splits it into exactly two rational points, P_v and ιP_v. A degree-two separable cover is Galois over the given base, so ι is defined over K. Properness of Y ensures that any collection of its local points is adelic: choose a proper model over O_K with finitely many primes removed and extend each local point by the valuative criterion. There is no global gluing requirement for an adelic tuple. In particular infinitely many switches are allowed.

For each α∈Br(Y), choose n annihilating α. The Kummer sequence lifts α to H²(Y,μ_n). After removing finitely many primes, invert n, choose a proper smooth model, and spread this finite-coefficient class to the model. At each remaining finite v, every point extends integrally and its evaluation lies in Br(O_v)=0. Thus each α evaluates to zero on every local point outside its own finite exceptional set. This is a uniform-in-local-points statement, stronger than finite support at just one chosen tuple.

Choose a base lift P=(P_v). For α∈A, define its global sum and each local difference by

    c(α)=Σ_v inv_v α(P_v),
    d_v(α)=inv_v α(ιP_v)−inv_v α(P_v).

Both are homomorphisms. A constant class contributes zero to c by global reciprocity, and zero to every d_v since its two evaluations agree. A pullback p*β∈A contributes Σ_v inv_v β(m_v)=0 to c because m is orthogonal to the full Br(X); its two evaluations at each v agree, so it contributes zero to d_v. Consequently c,d_v descend to B. Individual evaluations at P_v do not in general descend to B; this distinction is essential and the PR handles it correctly.

Choose finitely many generators of B and representatives α_j in A. Take the union of their exceptional sets and all archimedean places, calling it S. Outside S, d_v vanishes on every generator, hence on B. This same S works for every base lift and every m with the stated fixed-cover hypotheses. It need not kill every representative's individual evaluation: adding constants can introduce other ramified places, while their differences still cancel. The infinite size of the constant subgroup causes no problem.

Every lift Q of this same m has Q_v=ι^{ε_v}P_v, with ε_v∈{0,1}. Its descended evaluation is exactly

    c + Σ_{v∈S} ε_v d_v.

Conversely each vector of switches on S, keeping P elsewhere, is a legitimate adelic lift. Thus the entire image of the Brauer evaluation map on the fiber is this finite binary sum set. An A-orthogonal lift exists exactly when its zero character occurs. This proves the PR theorem without using any special geometry of an Enriques surface beyond the double cover, or of a K3 surface beyond finite A/Br₀(Y).

The K3 finiteness input is genuinely available: [Skorobogatov–Zarhin, theorem 1.2](https://arxiv.org/pdf/math/0605351v4), page 2, assumes a field finitely generated over Q and a K3 surface, and concludes finiteness of Br(Y)/Br₀(Y) as well as the Galois-invariant geometric group. A number field satisfies its hypothesis. No rational point, unproved Tate conjecture, or finiteness of Br₀(Y) is required. For A=Br₁(Y), A/Br₀(Y) injects into that finite quotient. Their corollary 1.4 on page 3 already applies finiteness to the Brauer–Manin evaluation condition.

## Choice invariance and transfer

Switching the base lifts by arbitrary indicators η_v changes the data to

    c′=c+Σ_{v∈S}η_v d_v,   d′_v=(−1)^{η_v}d_v.

At each v, η_v+(−1)^{η_v}ε_v is either ε_v or 1−ε_v. This permutes the same binary choices. The common S works for all local points, so infinitely many nonzero η_v do not invalidate the equality. This is change of base *lifts*. No computation of new Brauer groups after extending the number field is asserted; the theorem itself applies separately over any number field.

For either choice of A in the PR, ι* preserves A. The étale corestriction identity

    p*cor_p(α)=α+ι*α

puts the right side in A∩p*Br(X), even when A=Br₁(Y) and cor_p(α) has not separately been proved algebraic. Hence ι* is −1 on B. Pullback functoriality and m's orthogonality yield

    Σ_{v∈S}d_v=−2c.

Complementing all switches negates the resulting character. This does not force zero to occur. Nor does it allow replacing the exact binary set by the coset of a generated subgroup. The independently selected abstract Z/5 example c=1,d=(2,1) satisfies transfer and has attainable set {1,2,3,4}; its generated coset is the whole group. There is no claimed surface realizing that example. Four small cases, 15 changes of base lift, positive cases and this decisive false-positive control are recorded in INDEPENDENT_CHECKS.json; a large cyclic matrix adds no needed mathematical assurance.

## Reproduction of the published negative arithmetic

The relevant prior paper is [Harari–Skorobogatov, Non-abelian descent and the arithmetic of Enriques surfaces](https://www.ma.imperial.ac.uk/~anskor/HS.PDF). Its geometric construction supplies a smooth proper K3 model of

    y²=(x²−5)(x²−5·13²)(t²−5)(t²−20)

and the fixed-point-free involution ι(x,t,y)=(−x,−t,−y), giving an Enriques quotient. Lemma 2.2 applies at 13: the two elliptic j-invariants have valuations −4 and 3, so the factors are geometrically nonisogenous. Proposition 2.6(ii) supplies the unramified algebraic class α=(y,5). Theorem 2.9 supplies p*Br(X)=Br₀(Y) for these parameters. These are established geometric/cohomological dependencies, not claimed consequences of our small arithmetic script.

The rational point M=(0,0,650) satisfies the affine equation exactly. At v=13 choose x=t=1/13 and y=13⁻⁴u, where

    u²=(1−5·13²)²(1−5·13⁴)(1−20·13²).

The right side is 1 modulo 13. Hensel's lemma gives a unit u≡1 modulo 13, because derivative 2 is a unit. The script also reproduces its root modulo 13¹². Set N_v=M at all other places. This is an adelic lift N, so m=p(N) is locally liftable in the very same fixed cover. Since all pullbacks of Br(X) are constant and global constants pair trivially, m∈X(A_Q)^Br.

The quaternion (650,5) has local symbols −1 at 2 and 13, +1 at 5 and infinity, and +1 at every other prime. Its total invariant is 0 in Q/Z. The invariant at 13 of the new (13⁻⁴u,5) is zero: 5 is a nonsquare unit modulo 13, its quadratic extension is unramified, and the y-valuation is the even integer −4. Replacing only the 13-component changes the global invariant to 1/2. Finally −1 is the norm of 2+√5, so (−1,5)=0 globally; ι*α=(−y,5)=α. Every switch at every place therefore has difference zero on α. All lifts of m retain invariant 1/2, ruling out even Br₁-orthogonal lifting. This is precisely the established obstruction relevant here, not merely a lack of rational approximation inferred in the wrong direction.

The exact script reproduces parameter hypotheses, rational point, j-valuations, nonsquare test, the Hensel equation and residues, norm identity, Hilbert symbols, reciprocity, and the surviving obstruction. It does not compute Br(Y), re-prove all the cited geometric results, or create a new example.

## What the earlier nonabelian criterion does imply

HS example 3 and proposition 1.6, pages 8–11, have a further qualified consequence. Suppose a universal torsor Z→Y exists over K, and let f:Z→X be the composed torsor under the resulting extension of Z/2 by the Néron–Severi torus. Proposition 1.6 identifies X(A_K)^f with the union of images of the Br₁ sets of the globally twisted covers. It does not generally assert that this extension splits, and it does not replace Br₁ by full Br.

At a point m already locally liftable to the fixed Y, a twist also lifting that same m must have trivial localization in H¹(K_v,Z/2) at every v: the original fiber's torsor class is zero and twisting adds the localized twist. The map H¹(K,Z/2)→∏_v H¹(K_v,Z/2) is injective, since a nontrivial quadratic extension has an inert prime. Thus only the trivial global twist can contribute at this m. Under the stated universal-torsor existence hypotheses, HS therefore gives

    m∈X(A_K)^f  iff  m∈p(Y(A_K)^Br₁).

This pointwise specialization respects the original fixed cover. It is a consequence of prior work, not an unconditional identity of the full fixed-cover image with the union. Existence of the universal torsor is not supplied by the PR hypotheses, so it cannot be silently imposed or treated as established for every original input. This qualified prior criterion also is not evidence for a spreadsheet row claiming a full solution of the entire original assumptions question.

## Scope and novelty judgment

The finite-support and exact binary reduction are valid mathematical content; calling the theorem a bare tautology would discard that reduction. But after the standard finite Brauer quotient input, the only remaining hypothesis deciding success is membership of zero in the image of the original Brauer evaluation map, now written in binary coordinates. The PR supplies no arithmetic result restricting that image, no new family with a verified lifting condition, and no proof relating it to a different intrinsic arithmetic/descent condition. Every stated positive consequence, including B=0, is immediate from functoriality and the quotient. The sole arithmetic example is the prior HS failure.

Accordingly this is a faithful finite structural formulation of a conditional sub-question, not a verified genuinely new full resolution. Lack of an algorithm or an unconditional existence assertion is not the reason for this classification. A further arithmetic theorem, for example proving a separately formulated condition on m sufficient and/or necessary beyond the evaluation-image condition, or computing and resolving a new meaningful class of inputs, would be a materially different contribution. The present packet explicitly makes no novelty or broader-original-solution claim. No reasonable repair of bookkeeping can supply that missing arithmetic theorem.

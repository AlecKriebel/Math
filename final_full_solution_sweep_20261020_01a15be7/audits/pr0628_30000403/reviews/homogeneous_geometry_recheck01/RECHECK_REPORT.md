# Independent homogeneous-geometry recheck of PR 628

Candidate: `677673860f9e67dffc610f52384f0bd60e65e363`, problem 30000403 / OWR-1188-004. Review date: 2026-10-21 UTC.

## Finding and scope

**No gap found in the prior-theory implication for the universal quadratic upper bound or the V4 degree-one conclusion.** In fact, the same argument gives degree one whenever the geometric cover-point stabilizer in PGL2 is noncyclic. The needed passage from a point on a compression to a point on the fixed split target is valid, provided the point is chosen in the free open. It is not enough merely to neutralize a residual gerbe; the free-open construction supplies the extra point on its associated conic, and that point trivializes the PGL2 torsor.

The independently reconstructed proof below uses an established compression mechanism. Bresciani's 2022 Proposition 2 is expressly a statement about arbitrary finite étale gerbes, while the 2023 Theorem 2 and Lemma 6 authenticate its application to a faithful finite-gerbe family unrelated to a divisor. The final split-target step is the same free-open argument displayed for divisors in 2022 Lemma 11, applied to the family constructed here. No new Hurwitz-specific mechanism is needed.

This review **does not independently authenticate historical sharpness priority**. The candidate's six-branch C2 example and alternate V4 proof are preserved, and no defect in them is asserted. Another reviewer is checking the original sharpness literature. Thus the precise review verdict is that the two upper-bound assertions are direct prior-theory consequences. A full claim that every ingredient of the exact theorem was already available must combine this verdict with an authenticated prior sharpness input. No assertion is made that either paper explicitly prints the identical Hurwitz theorem or that the candidate's coordinates were copied.

## Independence and input binding

Before reading old priority verdicts, I wrote `INDEPENDENT_DERIVATION_CHECKPOINT.md` and its hash in `INPUT_BINDINGS_INITIAL.json`. At that stage I had read only the candidate's proof and release clarifications. I independently obtained the construction, the split-target bridge, and the stronger noncyclic conclusion. I then freshly downloaded and read both complete version-specific primary-paper bodies and only afterward read `ROOT_PRIOR_IMPLICATION.md` and `PRIORITY_REJECTION_ACCEPTANCE.json`. The old verdict was compared as an adversarial target, not used as mathematical evidence.

Read-only Git object comparison confirms that the supplied proof, release clarifications and author freeze are byte-identical to their paths at the immutable candidate commit. See `IMMUTABLE_HEAD_BINDING.json`. All new work is inside this review directory. No external individual, other agent or chat was contacted. No canonical file, previous review, branch, commit, PR, provider record or spreadsheet was changed. No GWS command was invoked.

## Exact general statement

Let k have characteristic zero, let H=PGL2/k, and let F be a k-scheme or algebraic space of finite type with an H-action such that F over an algebraic closure is a single homogeneous H-orbit with finite geometric stabilizer E. Then:

1. F(K) is nonempty for an extension K/k of degree at most two.
2. If E is noncyclic, F(k) is nonempty.

The action E on the auxiliary projective line is its inclusion into PGL2, so it is faithful. E is not required to be a constant group over k, or even to have a chosen k-defined embedding before choosing a geometric orbit point. The theorem is uniform in the Galois action on E. It makes no assertion about a separate gerbe of actual marked covers.

## Proof with all bridges retained

### 1. The finite gerbe and its faithful family

Set

    R = [F/H],             U = [(F × P1)/H],

with the diagonal H-action. The projection U→R is a form of the projective line over the gerbe R. Geometrically, choosing p0 in F identifies R with BE and U with [P1/E]. R is therefore a finite étale gerbe: the stabilizers are finite and étale in characteristic zero, and geometrically there is one isomorphism class. This is a gerbe for the target orbit, not the moduli stack of G-covers.

Let Y be the coarse space of U. Geometrically, it is P1/E. That quotient is a smooth projective curve of genus zero: its function field is the invariant subfield of kbar(z), and Riemann–Hurwitz, or Lüroth together with smooth completion, gives P1. Tame coarse-space formation commutes with extension to kbar, so Y is a smooth proper geometrically connected genus-zero curve over k.

One may avoid an opaque coarse-space existence assumption in this case: the semilinear descent construction in step 5 descends the projective curve P1/E directly. It gives the same Y and makes the branch divisor's descent explicit.

Every nonidentity element of E fixes only finitely many points on P1. The complement of their union is a nonempty free open. Its image defines a nonempty open Y0 in Y on which U→Y is an isomorphism. Indeed U has trivial inertia there, hence is an algebraic space, and its coarse map is the identity coarse map. This is the essential distinction between a point on a coarse space and an actual stack object.

### 2. Why a free-open point splits the fixed-target obstruction

Fix an extension K/k and y in Y0(K). The isomorphism over Y0 gives an object of U(K). By the quotient-stack definition this is an H-torsor T over K with an H-equivariant map

    T → F × P1.

The F-component is an object of R(K). The P1-component is a K-point on the associated Brauer–Severi conic C=T×^H P1. Since C has a K-point, C is isomorphic to P1/K. The PGL2-torsor/conic correspondence now implies that T is trivial. After choosing a trivialization, the F-component gives a point of F(K).

Thus the same y supplies BOTH pieces: it neutralizes R and trivializes the particular PGL2 torsor needed to recover an ordinary point of F on the split target. Neither a central cover-descent assertion nor a section of a normalizer extension has entered.

### 3. Degree at most two in every case

A smooth genus-zero curve admits its anticanonical plane-conic model. If Y is split, its nonempty open Y0 has a k-point because k is infinite. Otherwise choose a k-line in the plane that avoids Y\Y0 and is not tangent to Y. Such lines form a nonempty open of the dual projective plane, which has a k-point over an infinite field. Its intersection with Y is a reduced degree-two zero-cycle supported in Y0. A closed point in this cycle has residue field K of degree one or two over k. Therefore Y0(K) is nonempty for [K:k]≤2, and step 2 gives F(K).

Only the index of a conic is used. No assertion that an arbitrary 2-torsion Brauer class has index two is needed.

### 4. Noncyclic E, including every V4 form

Assume E is noncyclic and write n=|E|. The cover P1→P1/E is tame. If its geometric branch values have inertia orders e1,…,eb, Riemann–Hurwitz gives

    2 − 2/n = Σ(i=1,…,b) (1 − 1/ei).

Each summand is at least 1/2, so b≤3. For n>1, b=0 or 1 is impossible. If b=2, then 1/e1+1/e2=2/n and each ei≤n, forcing e1=e2=n. Thus E fixes a point on P1. A finite characteristic-zero subgroup fixing a point injects into the multiplicative group through its tangent representation: the kernel would be finite unipotent, hence trivial. Therefore E would be cyclic, a contradiction. Consequently b=3.

The reduced branch divisor B of this auxiliary quotient cover is intrinsically determined by U→Y, so B descends to k and has degree three. This is the branch divisor of the E-action on the auxiliary P1; it is NOT the branch divisor of the original G-cover. No individual branch value must be rational. Its Galois action may be transitive of degree three.

The k-line bundle OY(B)⊗ωY has degree one. Riemann–Roch gives a nonzero k-section, since the dual term has negative degree, so Y has an effective divisor of degree one and hence a k-point. Thus Y is split. Since k is infinite, Y0(k) is nonempty, and step 2 gives F(k).

For E=V4 this works with every action of the absolute Galois group on its three involutions. It requires neither a constant normalizer nor a Galois-equivariant section S3→S4. It also proves the stronger conclusion for dihedral and exceptional noncyclic groups.

### 5. Explicit semilinear/cocycle check

This verifies the most vulnerable step independently of stack notation. Choose p0 in F(kbar) and E=StabH(p0). For each σ choose aσ in H(kbar) with

    σ(p0) = aσ^(-1) p0.

Then σ(E)=aσ^(-1)Eaσ. The map on P1/E given by

    [z] ↦ [aσ σ(z)]

is independent of the choice of aσ. The relation

    aσ σ(aτ) ∈ E aστ

shows that these maps form a semilinear descent datum. Everything is defined over a finite extension after enlarging the field to include p0, E and finitely many transition maps, so the datum is continuous and effective on the projective quotient curve. This yields Y/k and its descended nonfree divisor.

Suppose y in Y0(K), choose a geometric preimage q in P1(kbar), and restrict to σ in Gal(kbar/K). There is a unique eσ in E with

    aσ σ(q) = eσ q,

because E acts freely at q. Put bσ=eσ^(-1)aσ. Then bσ maps σ(p0,q) to (p0,q). The common stabilizer of (p0,q) is trivial, so bσ σ(bτ)=bστ exactly. The formerly E-valued cocycle defect disappears. The descended conic for this H-cocycle has the rational point represented by q, so its class is trivial. Write bσ=h^(-1)σ(h); then h p0 is K-rational. This is precisely the ordinary fixed-target point required.

This calculation checks arbitrary Galois permutation of E, the cocycle direction, the elimination of the defect by a free point, and the final PGL2 class. It does not assume that the original aσ form an H-cocycle.

## Passage to the exact Hurwitz claim

The candidate works with the ordinary inner coarse fixed-target Hurwitz space M and its geometric PGL2 quotient. For a k-rational reduced point x, the geometric quotient property says that the geometric fiber is one PGL2 orbit. This orbit is Galois-stable. Algebraic-group orbits are locally closed; the reduced orbit, with its induced structure, therefore descends to a smooth homogeneous k-space F. If a scheme-theoretic fiber has extra structure, use this descended reduced orbit; a point of it is still an ordinary coarse point of the fiber. No assertion that the full scheme-theoretic fiber is smooth is needed.

The geometric stabilizer E is a subgroup of target PGL2. Any member sends the original branch set to itself, so E lies in the finite stabilizer of that set when there are at least three distinct branch points. A transformation fixing three points is the identity, which proves finiteness. The inclusion E⊂PGL2 is faithful. In general E can be a proper subgroup of the full branch-divisor stabilizer: preserving a branch divisor need not preserve the marked cover point. The proof uses E throughout, not that larger group.

Deck transformations, including an ineffective center of the actual marked-cover stack, are already forgotten in the ordinary coarse space M. They do not become an ineffective kernel in E. Taking R=[F/PGL2] therefore does not assert that the actual marked-cover gerbe is neutral. This exactly matches the scope preserved by the candidate's release clarifications.

The assumptions that k contains the Hurwitz-data field and has characteristic zero ensure the given spaces and action are over k and all finite stabilizers are tame. No number-field, perfect-closure, algebraically closed constants, fixed conjugacy-class normalization, or special Galois-action assumption is added. Characteristic zero implies k is infinite and perfect, which is all the field argument needs. The conclusion is stable under arbitrary extension of the initial data field, so it covers rational points whose absolute field of moduli is smaller than k.

The general result gives a closed-point degree at most two in the ordinary coarse fiber. A K-point has a residue field contained in K, so it gives the stated minimum m_k(x)≤2. In the V4 stratum it gives m_k(x)=1.

## Precisely authenticated prior inputs

The complete bodies, not search snippets, were freshly retrieved and read. The files are private in `private_sources/`; hashes and retrieval receipts are in `SOURCE_RETRIEVAL.json`.

- Giulio Bresciani, *The field of moduli of a divisor on a rational curve*, arXiv:2211.03438v1, dated 7 November 2022. Proposition 2, pp. 3–4, applies to arbitrary finite étale gerbes with genus-zero geometric fibers and forces a cyclic band when the compression conic is nonsplit. Lemma 11, pp. 7–8, explicitly distinguishes a split target from a twisted genus-zero target and obtains the former from a point on the free open. [Primary PDF](https://arxiv.org/pdf/2211.03438v1).
- Giulio Bresciani, *The field of moduli of varieties with a structure*, arXiv:2303.01409v2, dated 28 November 2023. Theorem 2, p. 3, and Lemma 6, pp. 4–5, supply the general faithful-gerbe-family and twisted-quotient framework. The discussion before Definition 15, pp. 9–10, warns that mere descent to a twist does not imply descent to a specified split variety. That warning is resolved here by step 2, rather than ignored. [Primary PDF](https://arxiv.org/pdf/2303.01409v2).

These source statements are sufficient prior machinery. The report's explicit construction and proof show the claimed implication; the report does not present an explicit older printed Hurwitz statement that has not been authenticated. The general upper bound actually needs only the compression plus the elementary conic argument. Proposition 2 supplies the stronger noncyclic conclusion directly, and step 4 reproduces that conclusion using the characteristic-zero Riemann–Hurwitz mechanism.

## Comparison and recommendation

The independent proof agrees with the old `ROOT_PRIOR_IMPLICATION.md` on all material bridges. I found no hidden central automorphism issue, fixed-target obstruction left unsplit, missing Galois-stability condition, or V4 exception. The adversarial controls and boundary checks are recorded separately in `ADVERSARIAL_CHECKS.md`.

Recommend **do not revive this candidate as a novel solution of the universal upper-bound problem**. The theorem's upper-bound content, including its V4 improvement and the stronger noncyclic claim, follows directly from dated prior general theory with elementary specialization. An explicit alternate proof or executable coordinates can retain expository value, but their possible novelty does not restore novelty of that original bound. Preserve the candidate proof and explicit example unchanged. Combine this scoped verdict with the separate original-source sharpness review before describing the entire exact theorem as historically subsumed. No publication, closure, comment or tracker action is authorized or performed by this report.

This review is an independent AI mathematical recheck, not human peer review or formal proof certification.

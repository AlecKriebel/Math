# Detached followup: general corner and honest-cocycle invariance

This followup preserves the initial structural_reductions seal unchanged. It follows authorized exposure to reviews/corner_cohomology_adversary/REPORT.md. It was sealed before reading the direct_lineage findings; the subsequent root message identifying that family's sealed files and source claims is disclosed as assignment-level exposure only.

## Result

Both proposed general claims pass the direct mathematical checks below for finite abelian actions on unital C*-algebras. **Fullness in the ambient algebra suffices. Honest cocycle perturbations preserve strong approximate innerness.** No coherent group-representation condition is needed.

The first audit's phrase that the transfer needs fullness in A^alpha should be read only as a description of the submitted fixed-frame lemma. As a claimed necessary condition it is too strong. The fixed-algebra fullness hypothesis is sufficient, and the new ambient-full proof removes it. Likewise, pinching is one valid way to restore original fixed membership, but it is not necessary: for a genuine finite-abelian cocycle, finite averaging and polar decomposition work.

A new authenticated 2025 primary theorem supplies a prior general framework for precisely this weaker property, without changing it to approximate representability. The two invariance claims are checkable consequences of that framework and elementary crossed-product/corner identifications, although this bounded followup did not locate an older primary body separately stating either lemma in exactly the proposed form. This is a positive prior-consequence finding, not a novelty certificate or an assertion that the graph target was explicitly printed in that paper.

## 1. Direct check: ambient-full invariant corner

Let alpha:G -> Aut(A), with G finite abelian, p in A^alpha full in unital A. Choose a finite frame y_j in Ap with sum_j y_j y_j*=1. Replace it by the orbit frame

    x_(h,j) = |G|^(-1/2) alpha_h(y_j).

The frame identity persists because it is the average of alpha_h(1)=1. It is permuted by every alpha_k. For fixed g take corner unitaries u_n in (pAp)^alpha implementing alpha_g, and define

    V_n = sum_i alpha_g(x_i) u_n x_i*.

For each k, commutativity alpha_k alpha_g=alpha_g alpha_k and frame reindexing give alpha_k(V_n)=V_n exactly. This argument avoids any requirement that the original frame lie in A^alpha. All Gram entries x_i*x_j and coefficients x_i*a*x_j lie in pAp. Consequently

    V_n V_n* -> 1,
    V_n* V_n -> 1,
    V_n a V_n* -> alpha_g(a).

For the second identity use u_n* alpha_g(b) u_n -> b on the corner. The first uses Ad(u_n)(x_i*x_j) -> alpha_g(x_i*x_j). Both norm unitary-defect limits are required; together they make V_n eventually invertible in the unital algebra. Its polar unitary lies in A^alpha and differs from V_n in norm by a quantity tending to zero.

Conversely, for an invariant p, compression of full-algebra implementers gives z_n=p v_n p; asymptotic commutation with p makes both corner defects tend to zero. Corner polar decomposition gives fixed unitaries implementing the restriction. Fullness is not needed in this direction.

Thus restriction and lifting give an equivalence when p is invariant and ambient-full. Nothing in this proof requires separability. The source framework in §3 assumes separability, which covers all finite graph/CK algebras in the original problem but is a narrower abstract setting.

**Boundary countercheck.** On M_2, take alpha=Ad(diag(1,-1)) for G=Z_2 and p=e_11. The corner action is trivial, p is full in M_2, and the fixed algebra is the diagonal algebra, where p is not full. The action is nevertheless strongly approximately inner, implemented exactly by diag(1,-1). This disproves necessity of fixed-algebra fullness, while leaving the submitted sufficient lemma valid.

## 2. Direct check: honest cocycle perturbation

Suppose beta is strongly approximately inner, d_(gh)=d_g beta_g(d_h), d_1=1, and alpha_g=Ad(d_g) beta_g. Fix g and let v_n in A^beta implement beta_g. The unitaries t_n=d_g v_n asymptotically implement alpha_g. For every h, abelianness and the honest cocycle identity give

    alpha_h(t_n)
      = d_h beta_h(d_g) v_n d_h*
      = d_g beta_g(d_h) v_n d_h*.

Therefore

    ||alpha_h(t_n)-t_n||
      = ||beta_g(d_h)-v_n d_h v_n*|| -> 0.

The finite average z_n=|G|^(-1) sum_h alpha_h(t_n) is exactly alpha-fixed and norm-close to the unitary t_n. It is eventually invertible. Polar decomposition gives alpha-fixed unitaries with the same implementing limit. Applying the same argument to the inverse alpha-cocycle d_g* gives the converse. Thus the property is invariant under honest exterior equivalence and hence under honest cocycle conjugacy in this setting.

A scalar-projective family is different. For the trivial action, a genuine cocycle is an actual unitary representation. A projective Pauli family has d_g d_h differing from d_(gh) by nontrivial scalars and need not commute. Its induced automorphisms form an action, but this is not an honest exterior equivalence to the trivial action. The Pauli example is not a counterexample to the lemma just proved. It remains useful for rejecting the unsupported claim that all pointwise inner finite-abelian actions are strongly approximately inner.

## 3. New authenticated primary framework, available before this manuscript

Johannes Christensen, Robert Neagu and Gábor Szabó, *On a Rokhlin property for abelian group actions on C*-algebras*, [arXiv:2504.12730v1](https://arxiv.org/abs/2504.12730v1), 17 April 2025; [accepted v2](https://arxiv.org/abs/2504.12730v2), 27 November 2025. The [publisher page](https://ems.press/journals/jncg/articles/14299355) records online publication on 10 December 2025, DOI [10.4171/JNCG/648](https://doi.org/10.4171/JNCG/648). Publisher body was subscription-gated; both arXiv bodies were acquired.

Actual bodies inspected:

- v1 Definition 2.1 and Remark 2.2, p.5: the abelian Rokhlin property supplies an individual central-sequence eigenunitary for each character, without coherent multiplication between characters.
- v1 Remark 3.2 and Lemma 3.3, p.12: for unital algebras and finite abelian groups the paper's pointwise strong approximate innerness is exactly Izumi's strong approximate innerness, expressly weaker than approximate representability.
- v1 Theorem 3.7, p.15, and proof pp.15–16: pointwise strong approximate innerness is dual to the abelian Rokhlin property.
- v2 has Definition 2.1/Remark 2.2 at p.5, Definition 3.1/Remark 3.2 at p.11, Lemma 3.3 at p.12, and Theorem 3.7 at pp.15–16. Its pp.11 and 15 were also visually inspected.

This is a legitimate duality route for the target's weaker property. It does **not** assert that strong approximate innerness is dual to the usual coherent Rokhlin property. The latter would conflate the properties, which the source explicitly distinguishes.

### 3a. Honest cocycle invariance as a direct prior-theorem consequence

The honest cocycle defines an explicit isomorphism

    Psi: A crossed_alpha G -> A crossed_beta G,
    Psi(a)=a,  Psi(lambda_g^alpha)=d_g lambda_g^beta.

The cocycle identity checks multiplication; the covariance relation checks the action; the map is onto because lambda_g^beta=d_g*Psi(lambda_g^alpha). The inverse is obtained from the inverse cocycle. The dual character actions are intertwined because both sides multiply the g-th group generator by the same character value.

The abelian Rokhlin property is invariant under equivariant isomorphism, directly from its definition. Hence Theorem 3.7 and Remark 3.2 imply honest-cocycle invariance of finite-abelian strong approximate innerness, with all assumptions satisfied for the original separable graph target.

**Credit classification:** a direct consequence of the 2025 theorem plus the displayed elementary standard crossed-product isomorphism. No exact stand-alone cocycle-invariance theorem was located. The new finite-average proof is an elementary direct proof of this consequence; its independent rediscovery does not establish mechanism novelty.

### 3b. Ambient-full corner invariance as a prior-theorem consequence

For a unital B and full projection p, compression induces the canonical central-sequence isomorphism

    B_infty intersect B'  ->  (pBp)_infty intersect (pBp)'.

Here the subscript means the bounded-sequence quotient by norm-null sequences. A checkable inverse is obtained from a finite frame x_i in Bp:

    [b_n] -> [sum_i x_i b_n x_i*].

Centrality of b_n in pBp makes this map multiplicative in the quotient, unital, and central in B. It also makes compression its inverse. More explicitly, central sequences commute with the finitely many Gram entries x_i*x_j, giving multiplicativity, and the reconstructed sequence w_n satisfies w_n x_i - x_i b_n ->0. This proves centrality against arbitrary a by writing a=sum_(i,j) x_i (x_i*a*x_j) x_j*. Compression recovers b_n because p x_i lies in pBp. Injectivity of compression follows from centrality and fullness: a central sequence with p-compression zero has product with each x_i tending to zero, and the frame identity then forces the sequence to vanish.

If p is invariant under an action delta, compression is equivariant. Its inverse is consequently equivariant, even if the chosen frame is not fixed. Thus the abelian Rokhlin eigenunitary condition is equivalent for an invariant full corner and its ambient algebra.

Apply this with B=A crossed_alpha G. The invariant-corner crossed product (pAp) crossed G is canonically pBp since p is alpha-fixed. If p is full in A it is full in B, and p is fixed by the dual action. The central-sequence isomorphism and 2025 Theorem 3.7 yield the ambient-full corner equivalence for separable unital finite-abelian actions.

**Credit classification:** consequence of the 2025 theorem plus the displayed elementary full-corner central-sequence identification. This report supplies that identification rather than claiming that the 2025 paper expressly states the proposed corner lemma. Its nonseparable generalization is not covered by the paper's hypotheses; the direct frame proof in §1 covers it.

Selçuk Barlak and Gábor Szabó, *Sequentially split *-homomorphisms between C*-algebras*, [arXiv:1510.04555v3](https://arxiv.org/abs/1510.04555v3), 7 October 2016, supplies older background: Proposition 1.9 p.10 on stable invariance of central-sequence algebras; Proposition 3.8 p.27 on invariant hereditary restrictions; Lemma 3.12 p.29 on representing compact-group-fixed sequence elements by fixed sequences; Proposition 3.14 pp.29–30 on equivariant stabilization of sequential splitness. Actual bodies were inspected. These are useful infrastructure, not a separately stated 2016 strong-approximate-innerness corner theorem.

## 4. Implications for the initial audit and original target

| Item | Corrected assessment |
|---|---|
| Fullness in A^alpha | Sufficient for the submitted fixed-frame lemma; unnecessary in general |
| Original fixed algebra changes under a cocycle | True, but norm-asymptotic invariance plus averaging/polar recovers original fixed implementers |
| Pauli obstruction | Obstructs projective/pointwise-inner shortcuts; does not refute honest cocycle invariance |
| Kodaka–Teruya approximate representability theorem | Still cannot be applied directly to weaker strong approximate innerness |
| 2025 abelian Rokhlin duality | Applies to precisely the weaker property and yields the two general consequences above |
| Pinching | Valid sufficient construction; “necessary” is too strong |
| Graph target statement priority | Still not settled as an explicitly printed old full-target statement by this followup |

Combining these general consequences with the previously authenticated first-return corner and vertex-coboundary reductions removes two apparent obstacles without fixed-point simplicity or approximate-representation coherence. This identifies the original full target as a short composition of earlier specialized results and elementary deductions. It does not by itself settle whether someone had already explicitly recorded that graph consequence, or whether the precise composition is a new observation.

## 5. Evidence, boundaries, and exposure

Thirty-six new literal public queries are recorded in SEARCH_LOG.json. This was a targeted followup, not a rerun of the initial 80-query audit. Positive source findings rest on actual primary bodies, not the secondary summary that first led to the 2025 paper.

Two further Izumi 2004 Project Euclid retrieval attempts returned small HTML responses, despite HTTP 200. They were not treated as PDFs or original article-body access. The original Izumi-body access gap remains. No source-author code was executed.

Authorized pre-seal exposure includes the old structural audit and reviews/corner_cohomology_adversary/REPORT.md (provided to test Theorems A and B), plus parent assignment descriptions. While the followup was in progress, root provided the direct_lineage seal hash and a summary of its proposed Gabe–Szabó route for a later cross-challenge. No direct_lineage file or Gabe–Szabó body was read before this followup seal; the content of that assignment is nevertheless disclosed as limited later-route exposure.

The original structural_reductions output and seal files were verified unchanged. New third-party/raw material is confined to this followup's local exclusion directory. Public outputs contain authored arguments, source URLs, dates, inspection qualifications and hashes. No git mutation, publication, remote mutation, external-person communication, or current-edition edit occurred.


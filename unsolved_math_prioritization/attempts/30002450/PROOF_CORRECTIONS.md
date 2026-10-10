# Checked formulas for the twice punctured potential audit

This note makes explicit the formulas used to audit Section 4 of Geuenich–Labardini-Fragoso–Miranda-Olvera, [arXiv:2008.10168v1](https://arxiv.org/pdf/2008.10168v1), also published as [SLC 84 (2022), B84c](https://www.mat.univie.ac.at/~slc/wpapers/s84geuen.pdf). It supplies authored, AI-assisted, unrefereed local corrections and justifications of the existing argument; no external human peer review is claimed. It does not claim a new resolution, reproduce the source document, or assert that the authors issued an erratum.

## Unambiguous incidence and mate indices

Let g≥1 and n=4g. Use radial vertices v_1,…,v_n, outer vertices u_1,…,u_(2g), and v_0=v_n. For h=0,…,g−1, define

    ℓ(4h+1)=ℓ(4h+3)=2h+1,
    ℓ(4h+2)=ℓ(4h+4)=2h+2.

The arrows are

    a_j : v_j → v_(j−1),
    b_j : u_ℓ(j) → v_j,
    c_j : v_(j−1) → u_ℓ(j).

Products are read right to left. Thus T=Σ_j a_j b_j c_j. The fixed-point-free involution ι exchanges 4h+1 with 4h+3 and exchanges 4h+2 with 4h+4. Equivalently, the mate pairs are {j,j+2} for

    J={4h+1,4h+2 : 0≤h<g}.

This incidence list is the arrow numbering in the two fan figures. It has 6g vertices, 12g arrows and n triangle cycles. Each vertex has two entering and two leaving arrows. The two puncture cycles have lengths n and 2n. In particular, each is a product of distinct arrows, although powers of those cycles are allowed in a potential.

In Proposition 4.4, replace the range j=1,…,2g in each four-term or two-term mate-pair sum by j∈J. For g=1 the ranges coincide. For g=2 the printed range repeats diagonal entries 3 and 4, introduces spurious pairs {3,5} and {4,6}, and misses the actual pairs {5,7} and {6,8}; it is not a valid description of all premutations. This is an index-range correction, not a change in the intended sequence of outer-vertex mutations.

## Premutation and splitting without hidden coefficient changes

Mutate every u_k once. No original arrow joins two outer vertices, and none of the new composites has an outer endpoint. Thus later outer mutations are not obstructed by the diagonal 2-cycles already created.

For each j, define d_j=[b_j c_j] and D_j=[b_j c_ι(j)]. Define e_j=c_j* b_j*. Each pair {j,ι(j)} yields the two diagonal composites and two cross composites exactly once. Let A=a_1…a_n, let P be the long puncture cycle, and let D be its contracted cycle. For arbitrary formal series F,H with zero constant terms, the premutation of T+F(A)+H(P) is cyclically equivalent to

    Σ_j (a_j+e_j)d_j
      + F(A)
      + H(D)
      + Σ_j c_ι(j)* b_j* D_j.

All these sums now run over j=1,…,n. This form avoids any pair-representative convention. The quadratic part is Σ_j a_j d_j with invertible coefficient matrix.

Make the substitution a_j↦a_j−e_j. Set

    E=F((a_1−e_1)…(a_n−e_n))−F((-e_1)…(-e_n)).

Every cycle in E contains an a arrow. Rotate each such cycle so that a selected occurrence is first, and collect the terms as E∼cyc Σ_j a_j R_j. No division by its multiplicity is made. Each R_j has length at least n−1≥3 and involves no d or D arrow. The assignment d_j↦d_j−R_j is therefore a continuous unitriangular automorphism. It changes the displayed potential to

    Σ_j a_j d_j
      + F((-e_1)…(-e_n))
      + H(D)
      + Σ_j c_ι(j)* b_j* D_j.

The first sum is a trivial QP, and all remaining terms avoid its arrows. These formulas check the splitting directly, including for infinite F,H. The cross arrows are fixed throughout. Restriction of the reduced QP to the radial vertices deletes every reversed arrow and therefore gives exactly the potential H(D).

The radial subquiver has one arrow D_j from v_(ι(j)−1) to v_j. It is a simple directed n-cycle: starting with v_n, each block is traversed as

    v_(4h) → v_(4h+3) → v_(4h+2) → v_(4h+1) → v_(4h+4),

with indices cyclic at 0 and n. The source's coefficient-isolation argument follows, independently of any identification of the whole reduced quiver with a homeomorphic triangulation.

## The induced cycle test over an arbitrary field

Only the necessity of a nonzero primitive-cycle coefficient is needed. Restriction preserves nondegeneracy by [Labardini-Fragoso, Corollary 22](https://arxiv.org/pdf/0803.1328), page 12. For a directed cycle of length t>3, mutate a vertex and restrict to the other t−1 vertices. The resulting full subquiver is a directed cycle of length t−1; its potential is obtained by contracting the adjacent two-arrow subpath. The extra cubic mutation term disappears under restriction. Repeat to obtain a directed triangle. If the coefficient of its primitive cycle is zero, mutation leaves a directed 2-cycle with no quadratic potential term, so reduction cannot remove that 2-cycle. This contradicts nondegeneracy. The argument includes the zero potential and does not use differentiation by the exponent or a characteristic assumption.

This supplies the particular arbitrary-field extension needed when the audit uses the C-based [GLS Proposition 2.4 and Corollary 2.5](https://arxiv.org/pdf/1308.0478v3). It is not an extension of the representation-type results elsewhere in that paper.

## Normal form estimates and zero cases

- In the last estimate of Lemma 2.5, preprint page 7, the unchanged contribution to B_f is A_f. The first argument of that minimum must be short(A_f), rather than short(A_g). The defining formula B_f=A_f+(higher-order terms)_f gives the corrected bound immediately.
- In Lemma 4.3, the least q exponent is r_(q,m). The displayed short(V_m) and q-arrow coefficient use that index consistently; the unbound n in λ_(q,n) is replaced by r_(q,m). The labels Υ_(p,n) and Υ_(q,n) in this calculation refer to Υ_(p,m) and Υ_(q,m).
- If a puncture's higher-power series is zero, its least exponent is infinity only as a bookkeeping convention. Set its cancellation map and subsequent correction map to the identity. Never form G^infinity or λ_infinity. If both series vanish, all later maps are identities.
- In the finite iteration of Corollary 2.8, stop after the t-th substitution. No further use of Lemma 2.7 at parameter zero is needed.
- In the final proof of Theorem 4.1, choose the particular fan triangulation of Figures 3–4. Lemma 4.3 and Proposition 4.4 were proved for that triangulation; the preliminary finite tagged-flip transport supplies the assertion for every triangulation. The final paragraph's more general wording is unnecessary and is not used by this audit.

For the cutoff iteration in Lemma 4.3, let L_p=8g and L_q=4g. Whenever r is finite, r≥2 and Lr≥m, hence L(r−1)≥m/2. Consequently the corrected composite maps have depth at least min(m−3,m/2), which tends to infinity. An omitted zero-series step has infinite depth and does not weaken this estimate. Remainders have order at least m and converge to zero. Degreewise stabilization, compatible inverses modulo every m^N, and the closed cyclic-difference subspace justify the limiting right equivalence.

## Algebraic closure without a characteristic zero assumption

In this fan, uniform scaling of all arrows by v, followed by a scalar normalization v^−3, sends the puncture coefficients (y,z) to (y v^(4g−3), z v^(8g−3)). Their product is yz v^(12g−6). Choose a root of v^(12g−6)=(yz)^−1. Algebraic closure gives a nonzero root even when the characteristic divides 12g−6. Scaling a_1 by u and b_1 by u^−1 then transfers an arbitrary factor between the two puncture coefficients while preserving T. They can both be made one. This is the specialization of the standard-potential coefficient argument needed for the exact target; root uniqueness and separability are not required.

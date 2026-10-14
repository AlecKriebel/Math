# Independent acceptance: geometric Hecke compatibility at five

14 October 2026 UTC. Row 1777 / 30005572. Review within shared PASS4/5; no additional mathematical pass. No author proof, ledger, queue, or remote was edited.

## Verdict and frozen input

ACCEPT the stated geometric theorem and its regular-at-level refinement in `pass4_five_compatibility/FIVE_HECKE_BY_KERNEL_INCIDENCE.md`, SHA-256:

`fac5809de5e1906e52fe5518f28b6373ed229f30133c0f1bf9eae938b62f9e62`.

For every auxiliary c prime to five, the normalized genuine geometric family satisfies the full prime Hecke relation over R=Z[1/6]. The new kernel-incidence proof covers primes p prime to c, hence every p above five. For p away from five dividing c, the previously accepted connecting-map proof supplies the relation. At p prime to cN, the new proof is valid in the coefficient system regular at the primitive N-torsion orbit. This includes the required geometric good-prime-at-five case.

This acceptance does not say that every individual pullback preserves T5-fixedness. It does not provide arithmetic ray-field descent, vertical integrality, unaugmented classes, bad-level U identities, compactification, or the relative formula.

## 1. The non-Cartesian defect is computed rather than suppressed

The intrinsic operator N_K=(pr_2)_*a^* is defined by a finite étale correspondence over the model field, with all field transfers included. The Cartesian square A×_B A identifies f^*f_* with N_K; f_*f^*=deg(f) follows from the projection formula.

When K is contained in A[5], the factorization [5]=gf yields

T5_A f^*−f^*T5_B=(deg(f)Id−N_K)g_*.

The zero-cycle example deg(f)[0]−[K] is genuinely nonzero for nontrivial K. The proof correctly avoids claiming it is a counterexample in K2 or to the full Hecke relation. It shows exactly why the previously tempting pull-push interchange cannot be used.

Eventual trace invariance survives N_K after excluding its kernel from the scalar monoid. Literal T5-invariance of the result is neither assumed nor needed in the intermediate coefficient module.

## 2. The group-cohomology identity includes its correction

For N commuting with H and a left-coset system r, set A_N=ΣrNr^−1. Expanding the cocycle equation at gamma r=r'h independently gives

cor(N res z)(gamma)=A_N z(gamma)+gamma u−u,

u=Σ(rNr^−1)z(r).

The placement of r^−1 inside the correction matters. The final draft has the correct formula. This gives the cohomology identity without a false pointwise simplification or division by the subgroup index.

The revised proof explicitly uses the LSSW row-vector convention: H=Gamma_i∩f Gamma_j f^−1 and the transported target argument is f^−1 gamma f. The middle cochain in source Proposition2.1.4 is therefore exactly f^*z_j(f^−1 gamma f). This identifies the asserted operator with source T(f), rather than an unverified inverse/dual Hecke convention.

## 3. Nonprincipal components and nonsplit torsion are retained

The kernel stabilizer has index q+1 because the reduction of the two off-diagonal Hom ideals supplies the upper and lower unipotent groups over O/p. These generate SL2(O/p), which acts transitively on its projective line. Full surjectivity onto GL2(O/p) is unnecessary and was not assumed.

The conjugate kernels are the q+1 line subgroup schemes in A_i[p]. They are defined over the model field as conjugates of the original defined kernel. The alternate scalar-Galois explanation is also valid after identifying the two rank-one CM torsion representations by a prime-to-p isogeny.

The incidence identity Σ_lines N_D=qId+N_A[p] is an equality of integral correspondence cycles. Checking geometric points proves that cycle identity, and then its K-theory action; it does not rely on injectivity of K2 restriction to a torsion-splitting field. Thus no degree or Galois-order division is hidden in descent of the trace sum.

The simultaneous ideal isogeny changes both component indices. The final proof explicitly transports Gamma_i by f0^−1 Gamma_i f0=Gamma_k and applies the accepted product norm law before pulling back. This gives the central [p]^* term with the correct component system. No principal generator of the ideal p or class-number-one assumption is used.

## 4. The regular-at-N refinement checks the actual cochains

When (p,cN)=1, every point of S_i+A_i[p] has nonzero primitive N-component (0,uP). It cannot lie on the horizontal theta support, since (c,N)=1. It cannot lie on the moved graph, since its equation would force xuP=0 with x a unit modulo N. The same argument applies after Gamma_0(N) action: the relevant denominator coefficients d and c_gamma+dx remain units modulo N.

Consequently the exact residues of every z_i(gamma) avoid the enlarged orbit. Local Gersten regularity puts these values in a neighborhood of that orbit. Translation traces along line kernels are therefore regular at S_i. The explicit transfer correction u is regular as well; it was not discarded as an abstract coboundary without checking evaluation.

For sheared representatives the unsheared norm identity is replaced by a genuine comparison b_f. The pushed primitive and target primitive have the same zero-cycle boundary, are both eventual-and-T5-fixed, and avoid S_j. Their unique normalized lift is regular there. The equality f_*z_i−z_j=delta b_f holds on the intertwined subgroup and survives pullback and corestriction in the regular modules. The preimage containment f^−1(S_j)⊂S_i+A_i[p] is exactly where (p,N)=1 is required.

At the level subgroup, reduction modulo p still contains SL2 because the N-restricted root ideal surjects modulo p. Thus no high-level or admissibility hypothesis was silently substituted for the stated geometric proper-level assumptions.

## 5. Verification and remaining scope

- Read the entire initial and revised proofs and compared the final Hecke convention with LSSW Proposition2.1.4, Definitions2.4.2–2.4.3, and Lemmas3.3.1–3.3.2.
- Read and replayed the author's exact checker. The replay is `FIVE_AUTHOR_CHECK_REPLAY.json`.
- Independently checked line incidence for q=2,3,5,7,25 and the transfer formula over an integer-valued permutation module for all elements of SL2(F2). In five of six arguments the correction is nonzero, confirming why pointwise equality cannot be substituted for the cohomology statement. Results are in `INDEPENDENT_CHECK_RESULTS.json`.
- These finite computations test the algebra; the correspondence, component, and regularity arguments above supply the geometric proof review.

The proof is homogeneous in the constructed K2 cocycle. It is valid with either Gersten sign provided the convention is transported consistently; see the separate sign-transport addendum. It does not by itself settle the prescribed sign of a relative theta edge.

Public source: LSSW, *Eisenstein cocycles for imaginary quadratic fields*, https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . The source's R[1/5] theorem was not imported as an R-theorem. The full construction remains UNSOLVED.

# Adversarial priority mapping audit

**Verdict: the qualitative cutoff mapping passes.** The exact existential conclusion can be obtained by adapting the earlier primary proof. The spatial cutoff therefore does not justify a first qualitative solution claim. A further independently checked energy bootstrap, derived in this audit, also makes the adapted phase mechanism reach the frozen maximal norm and state-witness conclusions; that deduction is not itself evidence of earlier publication.

Scope is only PR 908 / problem 30006191 / current `bounded_region_v2`, original head `a35667b1bb0bafed69916709997a4684223ecc93`. All 26 original files match the parent snapshot. No candidate edit, Git mutation, external communication, comment, Sheet update, publication, or other shard was performed.

## Primary-source inspection and independence

I independently downloaded the complete versioned primary PDF, read all 21 pages, and visually inspected the relevant phase estimates and graph-domain calculation before reading the proposed `priority_family/ADAPTATION.md`. The source is Oliver Siebert, *Discontinuity of Continuum Fermion Dynamics*, [arXiv:2609.34402v1](https://arxiv.org/pdf/2609.34402v1), submitted 28 September 2026, before the candidate's 7 October date. Its stated Theorem 2.4 is a full-space difference-kernel theorem. Its Proposition 2.6 explicitly gives maximal norm 2 for a full-space constant-number interaction. The cutoff implications below are new audit deductions from the earlier proof mechanism, not statements relabeled as source theorems.

The inspected source contains no stated theorem for `K(x,y)=1_Lambda(x)1_Lambda(y)`. This is a precise scope observation about that source; it does not infer absence from the rest of the literature. Raw PDF, metadata, extraction, and page images remain ignored and excluded from the public manifest. No old `already_solved` packet or old audit body was used as mathematical evidence.

## Exact adaptation and falsification attempts

The complete equations are in `INDEPENDENT_DERIVATION.md`, with reference labels D1-D14.

| Attack | Check and outcome |
| --- | --- |
| Treat the cutoff kernel as a function of `x-y` | This fails literally: translating both particles from inside to outside the ball preserves their difference and changes the kernel. A stated-theorem application is invalid; a proof adaptation is required. |
| Remove the quadratic cutoff discrepancy by a one-body term | Impossible in all particle sectors. The allowed one-body absorption handles only the diagonal `L` correction, as in D1. |
| Factor two / half coupling / diagonal ordering mismatch | The model is the ordered sum, so adding one particle gives `2 sum_j K`. Both `k=0` and `k=1` are treated. A half interaction convention would require consistently rescaled times and diagonal term. |
| Multiply distribution-valued fields without defining them | The conclusion is bound to bounded sector multiplication operators. Ordered density pairs give `L^2`; excluding diagonal gives `L(L-1)`. The CAR contraction is exactly `V(0)L=L`. |
| Sharp boundary destroys `H^2` propagation | It does not. Bounded perturbation gives `D(h_k)=H^2` with equivalent graph norm. Smooth tests vanish near the jump, so they lie in `D(h_k^2)`; functional calculus proves D2. No general claim that the indicator multiplies `H^2` into itself is made. |
| Differentiating the discontinuous interaction in leakage | No interaction derivative is present. Both the pair kernel and external term commute with smooth localization. The sole derivative is the first-order Laplacian commutator D5. |
| Translation uniformity is a hidden essential hypothesis | For this bounded two-variable kernel, the uniform multiplier bound is simply `||K(.,y)v||<=||v||`. The packing, potential lower bound, and exact geometry are checked without translation symmetry. |
| Probe supports remain compact under evolution | They need not remain compact. The fixed smooth test has graph-domain Lipschitz propagation; its unlocalized tail is O(s), and is estimated separately. No finite propagation speed is assumed. |
| Exchange symmetry / antisymmetrization intertwining fails | `K` is symmetric. Full kinetic domain and multiplication domain are permutation invariant. The full symmetric Hamiltonian commutes with the antisymmetrizer; D6-D8 justify the unitary intertwining and comparison. |
| Lose a factor `sqrt(n)` in Duhamel | D6 weights the overlap by the actual local particle count. Leakage controls both the unweighted tail and its `N_A` weight. The global bound is used only on the distinguished-particle tail, already `O(s)`. |
| Constants depend on the packed orbital or particle count | Fixed geometry and one fixed smooth packing template give `T_initial<=Cn^(5/3)`. Localization commutator constants are fixed. Probe propagation constants involve fixed tests only. The bounds apply to every positive integer n. |
| Assume interacting clusters remain Slaters | Not used. Only the initial Slater energy and support enter; subsequent estimates use conservation and local particle counts of the interacting state. |
| Substitute strong operator continuity for operator norm | The norm is tested using varying unit vectors in growing sectors. Every fixed vector and every fixed normal state remains continuous. |
| Use source polarization to claim the exact original f | Basic two-probe polarization is existential. A direct one-probe estimate also supplies qualitative discontinuity for the frozen interior f; D13-D14 supply the stronger original-f conclusion after the new bootstrap. |
| Set a maximal phase while retaining the source's `Cn^2t^2` error | That coarse estimate alone does not prove maximal 2. The new D10-D12 bootstrap is an explicit additional estimate. |
| Invoke the source's `t<=1/n` restriction to block exact candidate times | The proof's local test estimates hold up to time one. Duhamel estimates extend uniformly to every fixed `a/n`, including `a=pi/2`; no new hypothesis is crossed. |
| Claim a cutoff maximum was explicitly published earlier | Not established by the inspected source. The full-space maximum is explicit; the cutoff strengthening here is an audit-time deduction. |

## Strongest verified mapping and exact priority limits

The basic adaptation uses the primary paper's high-density cluster, interacting leakage, localized antisymmetrization, and relative phase. It gives a fixed gauge-invariant CAR observable with a strictly positive norm lower limit, and fixed creation/annihilation discontinuity. There is no essential gap from the sharp cutoff, pair ordering, or all-space kinetic term.

The frozen plateau gives a stronger exact identity than a general pair potential. Subtracting the initial interaction energy from conservation yields

\[
 \langle T_n\rangle_s\leq Cn^{5/3}+2nF_n(s),\qquad
 F_n(s)=\langle d\Gamma(\chi_B^2)\rangle_s.
\]

The same smooth leakage derivative closes by Gronwall:

\[
 F_n(s)\leq Cn^{5/3}s^2e^{C\sqrt n|s|}.
\]

Consequently the phase comparison error is `O(n^(11/6)t^2+n^(3/2)t^2)`, tending to zero at the frozen times `pi/(2n+1-k)`. The original fixed f, packed Slater, annihilation vector witness, norm limit 2, and varying-state limit 4 follow. This strengthening has an independent adversarial verification saved under `bootstrap_review`. It does not replace or mutate the frozen proof's separate free-Slater variance method.

Required framing is therefore precise: credit the earlier mechanism, describe the cutoff proof as an adaptation or quantitative strengthening, and avoid first qualitative solution language. Maximal 2 for the full-space reference was known from the inspected primary proposition; no inspected stated theorem gives the cutoff maximum. However, maximal 2 can also be deduced by the earlier localized phase mechanism plus the explicit new energy bootstrap. Its mathematical availability through that mechanism must not be confused with historical publication. Novelty of either quantitative method, and priority over uninspected literature, remain unverified.

No mathematical assumption remains unsupported in the displayed bounded-kernel mapping. The remaining gap is historical novelty certification, which this bounded audit does not attempt to convert into a mathematical conclusion.

# Independent audit: full extension, measure scope, source dependence, and priority

Audit checkpoint: 2026-10-06, 22:13 PDT. This report was reconstructed directly from the original request and primary references. It does **not** certify the upstream finite-cut cotype theorem; it verifies the exact extension implication once uniform metric Markov cotype two of finite-dimensional real `ell_1` is established.

## Verdict

The full arbitrary-subset assertion follows rigorously from a uniform bound `N_2(ell_1^m) <= N_0`, the finite-cut reconstruction lemma, Mendel–Naor Theorem 1.11, and contractive bidual projections for real `L_1(mu)`. No separability, completeness of the source, boundedness of the original map, sigma-finiteness, semifiniteness, or localizability of `mu` is needed. The correct ultrafilter is **fine**, meaning that it contains every finite-subset tail. An arbitrary free ultrafilter is not enough.

The newly discovered priority issue is material: the all-source/all-measure scope is an immediate consequence of the already publicly announced `N_2(L_1[0,1]) < infinity`, combined with established machinery and elementary finite-data transfers. Scope alone cannot responsibly be advertised as a new solution. A distinct elementary proof requires a separate proof-method priority assessment.

## 1. Exact hypotheses of the finite extension theorem

[Mendel–Naor, *Spectral calculus and Lipschitz extension for barycentric metric spaces*](https://web.math.princeton.edu/~naor/homepage%20files/cat0-extension.pdf), Definition 1.1, printed p.2, and Definition 1.2, pp.2–3, use finite reversible stochastic matrices and probability vectors that may have zero coordinates. For exponent two, source Markov type is

`sum_ij pi_i (A^t)_ij d_X(x_i,x_j)^2 <= M^2 t sum_ij pi_i a_ij d_X(x_i,x_j)^2`.

The target cotype convention is displacement plus `t` times one-step energy, bounded by `N^2` times energy of the Cesaro average `(A+...+A^t)/t`. These match the proposed project's conventions.

Theorem 1.11, printed p.8, assumes target metric Markov cotype `p` and **W_p barycentricity only**. It does not assume `p`-barycentricity from Definition 1.4. For every finite `E subset X`, it supplies `G_E:E -> Y`, equal to the original `f` on `E intersection S`, with

`Lip(G_E) <= C_B Gamma M_2(X) N_2(Y) Lip(f)`

at `p=2`, with an absolute constant `C_B`. This is a finite-domain map; claiming that this statement itself supplies a map on `S union E` for arbitrary infinite `S` would overstate it.

The ordinary barycenter of every real Banach space has the required constant `Gamma=1`. For any coupling `lambda` of finitely supported probability measures `alpha,beta`,

`||B(alpha)-B(beta)|| <= sum_(u,v) lambda_(u,v)||u-v|| <= (sum_(u,v) lambda_(u,v)||u-v||^2)^(1/2)`.

Taking the infimum proves the W_2 condition. Only finite sums occur. The finite-probability convention in Mendel–Naor Section 1.2 imposes no restriction on the underlying measure space of an `L_1(mu)` target.

## 2. Independent full-map reconstruction

This argument works for any Banach target `Y` admitting a linear contraction `P:Y** -> Y` with `P J=Id_Y`, where `J:Y -> Y**` is canonical. Suppose a single number `K` bounds the Lipschitz constants of all finite maps above.

If `S` is empty use zero. If `Lip(f)=0` and `S` is nonempty use the constant value of `f`. If `X` is finite, apply the finite theorem to `E=X`. Assume henceforth `S` nonempty and `X` infinite. Fix `s_0 in S` and put

`I={E subset X : E finite and s_0 in E}`.

For finite `D subset X`, put `T_D={E in I : D subset E}`. These tails have the finite intersection property. Choose an ultrafilter `U` extending the tail filter; it is automatically nonprincipal for infinite `X`.

Choose a finite map `G_E` for each `E in I` and define, for all `x in X`,

`h_x(E)=G_E(x)-f(s_0)` if `x in E`, and `h_x(E)=0` otherwise.

Then `||h_x(E)|| <= K d_X(x,s_0)` for every index. Coordinatewise boundedness is all that is needed; there need not be a common bound over `x`.

Define a functional on `Y*` by

`Phi(x)(y*)=lim_U y*(h_x(E))`.

The scalar ultralimit exists in a bounded compact interval. Its linearity and the norm bound show `Phi(x) in Y**`. On the tail containing both `x,y`, the finite maps give `||h_x(E)-h_y(E)|| <= K d_X(x,y)`. Evaluating against norm-one `y*`, passing to the ultralimit, and taking the supremum proves

`||Phi(x)-Phi(y)|| <= K d_X(x,y)`.

For `s in S`, its tail gives `Phi(s)=J(f(s)-f(s_0))`. Therefore

`F(x)=f(s_0)+P Phi(x)`

belongs to the **original target**, extends `f`, and has `Lip(F)<=K`.

For an explicit ultrapower formulation, let `Y_U=ell_infinity(I;Y)/{h:lim_U||h(E)||=0}`. Then

`Q:Y_U -> Y**`, `Q([h])(y*)=lim_U y*(h(E))`,

is a well-defined linear contraction that sends constants to their canonical bidual copies. The classes `[h_x]` supply an extension into `Y_U`; composition with `P Q` gives the preceding extension. No surjectivity of `Q`, embedding of `Y**` in this ultrapower, local reflexivity, or saturation is necessary. This avoids extra issues in the more elaborate Heinrich route discussed on Mendel–Naor pp.9–10.

## 3. Absolutely arbitrary measures

An arbitrary measure space means a set `Omega`, sigma-algebra `Sigma`, and countably additive `mu:Sigma -> [0,infinity]`, with no further regularity. `L_1(mu;R)` consists of real measurable integrable functions modulo almost-everywhere equality, with the integral norm.

[Harmand–Werner–Werner, Chapter IV](https://page.mi.fu-berlin.de/werner99/mbuch/buch4.pdf), Example IV.1.1(a), printed p.158, states that `L_1(mu)` is an L-summand in its bidual; the first proof uses the AL-space/projection-band argument. Proposition IV.1.5(b), pp.161–162, proves stability under arbitrary `ell_1` sums. [Chapter I](https://page.mi.fu-berlin.de/werner99/mbuch/buch1.pdf), Definition I.1.1, p.1, explicitly covers real and complex Banach spaces and defines an L-projection by `||z||=||Pz||+||z-Pz||`; thus it is contractive.

The following elementary reduction permits use of the cited example only for **finite** measures, avoiding ambiguity about source measure conventions.

Choose by Zorn a maximal family `(E_i)_(i in J)` of measurable sets with `0<mu(E_i)<infinity` and pairwise null intersections. If there is no positive finite-measure set, `L_1(mu)={0}`: a nonzero integrable function would have a positive finite-measure level set.

For `f in L_1(mu)` and finite `H subset J`,

`sum_(i in H) integral_(E_i)|f| <= ||f||_1`.

Hence `J_f={i:integral_(E_i)|f|>0}` is countable. Let `U_f=union_(i in J_f)E_i`. If `f 1_(Omega\U_f)` were nonzero, one of its sets `D={|f 1_(Omega\U_f)|>1/n}` would have positive finite measure. It is disjoint from each active `E_i`; for inactive `E_i`, the zero integral forces `mu(D intersection E_i)=0`. This contradicts maximality. Thus `f` is supported modulo null sets in the countable union `U_f`.

Restriction is therefore an isometric isomorphism

`L_1(mu;R) ~= (direct_sum_(i in J) L_1(mu|_(E_i);R))_(ell_1)`.

For surjectivity, an `ell_1` family has only countably many nonzero coordinates. Extend those representatives by zero and sum them. Countable pairwise overlaps are null and the norm equals the sum of norms. No completion hypothesis is required.

Each finite-measure coordinate `Y_i` has a contractive canonical bidual projection `P_i`. These can be combined directly. Write `Y=(direct_sum Y_i)_(ell_1)`, so `Y*=(direct_sum Y_i*)_(ell_infinity)`. For `z in Y**`, restrict it to functionals supported on `i`, obtaining `z_i in Y_i**`. Then `sum_i ||z_i|| <= ||z||`: on each finite coordinate set choose approximate norming functionals and signs and combine them into one functional of `ell_infinity` norm at most one. Therefore

`Pz=(P_i z_i)_i`

is well defined, contractive, and satisfies `P J=Id_Y`. This verifies the exact projection required for any countably additive `mu`, including nonsemifinite and nonlocalizable measures.

An unrestricted assertion `L_1(mu)*=L_infinity(mu)` is unnecessary and should not be used for arbitrary `mu`. Nor is it necessary or correct to assert that every `L_1` is a dual space.

## 4. Quantitative sources and boundaries

[Naor–Peres–Schramm–Sheffield, author-hosted draft dated October 19, 2004](https://web.math.princeton.edu/~naor/homepage%20files/Mtype.pdf), Theorem 1.2, printed p.2, and Theorem 2.3, p.6, give

`M_2(L_p) <= 4 sqrt(p-1)`, for `2<=p<infinity`.

Theorem 2.3 also gives `M_2(X)<=4 S_2(X)`, with smoothness convention (6), p.5:

`||x+y||^2+||x-y||^2 <=2||x||^2+2 S_2(X)^2||y||^2`.

The `L_p` estimate `S_2(L_p)<=sqrt(p-1)` is measure-independent. Alternatively, approximate each finite tuple by simple functions in a common finite partition and pass finite Markov inequalities to the norm limit. Thus arbitrary source measures are also permitted. The extension implication yields `Lip(F)<=4 C_B N_0 sqrt(p-1) Lip(f)`. There is no `p=infinity` consequence.

With a literal infimum definition of `M_2`, empty and singleton source spaces may have constant zero; their extension claims are trivial and should be treated separately. Nonsingleton sources have `M_2>=1` using a two-state chain and `t=1`. Zero target and zero Lipschitz constant are trivial too. Nonclosed subsets, noncomplete sources, unbounded images, and nonseparable spaces are handled by Section 2. A projection is norm one for nonzero targets; “contractive” handles the zero target uniformly.

This argument gives no claim for arbitrary subspaces of `L_1`, noncommutative `L_1`, or Schatten one. Complex targets need a separate argument.

## 5. Priority: broad scope follows from an earlier announcement

[Naor, *De-Höldering factorization*, arXiv:2609.07564v2](https://arxiv.org/pdf/2609.07564v2), p.1 footnote 1, defines `L_p` as the Lebesgue space on `[0,1]`. The Added in proof, printed p.12, announces forthcoming Mendel–Naor work proving metric Markov cotype two of `L_1` and `e(L_q;L_1) <= C sqrt(q)`. Reference `[MN26]`, p.13, is *Metric invariants from de-Höldering factorization*. [The arXiv history](https://arxiv.org/abs/2609.07564) records v2 on September 10, 2026, at 15:15:29 UTC.

The implication to the full proposed scope is direct. Partition `[0,1]` into `m` equal intervals `I_i`. The map `(a_i)->sum_i m a_i 1_(I_i)` embeds real `ell_1^m` isometrically. Conditional averaging is a contractive projection onto its range. Metric Markov cotype passes to a 1-Lipschitz retract: apply ambient cotype to initial points in the range and retract the witnesses; displacement and witness-edge terms decrease, while initial distances stay fixed. Thus the publicly announced `N_2(L_1[0,1])<=N_0` entails uniform `N_2(ell_1^m)<=N_0`.

Weighted finite `ell_1` is isometric to ordinary `ell_1^m` after multiplying positive-weight coordinates by their weights. The project's finite-cut representation maps the cotype witnesses back through a contractive affine reconstruction, proving `N_2(L_1(mu))<=N_0` for every measure. Sections 1–3 then give arbitrary Markov-type-two sources and full arbitrary subsets with the required dependence.

Hence the **mathematical implication is complete**, but novel-publication eligibility cannot be inferred from quantifier expansion. The announcement establishes public priority of the substantive base result; it does not replace proof auditing. Whether the finite-cut proof is independently distinct and publishably new is separate; this report has not reviewed a full public MN26 manuscript.

## 6. Source custody

These are research references under `sources/`, not automatically redistributable publication payloads. Text counterparts were made with `pdftotext -layout`.

| Local PDF | SHA-256 |
|---|---|
| `mendel_naor_cat0_extension.pdf` | `caf077bec643c224e4db3ef3fd0da18daf11f595933ed0ee4b966fb1dd905dd2` |
| `hww_chapter_iv.pdf` | `e71ba24e82eddb51f0e842b3dd43efc0889cf5670bfddc34afdf2f561f38dce3` |
| `hww_chapter_i.pdf` | `9baae15974c4be1860ab84c9c5aad76265fc10b3718c788d4a4659695a14fa87` |
| `npSS_markov_type.pdf` | `40e8ce340b2af4e63e5bebd7a80139b56221015919df813900ce5d40d5f1a1e2` |
| `naor_deholdering_2609_07564v2.pdf` | `176e89d6df829642fd8555586c9e5ff553113a99ff190b0f1de142633267f2b7` |

Best-guess completion for **this audit's scope**: 100% of the full-extension implication; 0% certification of the separately assigned upstream cotype proof. Novel publication package: 0% certification by this audit, with the priority concern above.

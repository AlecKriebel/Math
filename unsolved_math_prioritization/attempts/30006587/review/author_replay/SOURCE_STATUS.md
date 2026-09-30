# The multiple-Eisenstein derivative conjecture has a posted resolution in v2

**30006587 / OWR-14299909-002. Credited literature-resolution record with a proof-audit hold. No new solution is claimed. Separate source/algebra review is pending.**

The exact derivative formula is **Main Theorem D(ii) of Bachmann–Kanno–Maesaka, arXiv:2602.08176v2**, uploaded on **13 July 2026**. The original two-author February version calls it Conjecture 4.6(ii). The latest version supplies a new analytic realization and an all-depth proof. The author's current publication list describes the paper as **submitted**; this package does not call it a refereed theorem.

We verified the source match, read the relevant full arguments, and reconstructed the final algebraic reduction below. We have **not independently certified every all-depth regularization and realization dependency**. Accordingly this is an external preprint resolution with an explicit validation hold, not a campaign proof of the full theorem. The unrelated claim that these relations generate the entire kernel remains conjectural even in v2.

## 1. Exact original conventions

The [published Oberwolfach report](https://ems.press/content/serial-article-files/53601?nt=1), Report 7/2026, contains Bachmann's contribution on printed pp. 449–450. Both pages were visually inspected, and the complete contribution was read. For every tuple with **all** entries `k_i >= 2`, it defines

\[
G_{k_1,\ldots,k_r}(\tau)
 =\lim_{M\to\infty}\lim_{N\to\infty}
 \sum_{\substack{\lambda_i\in\mathbb Z_M\tau+\mathbb Z_N\\
 \lambda_1\succ\cdots\succ\lambda_r\succ0}}
 \frac{1}{\lambda_1^{k_1}\cdots\lambda_r^{k_r}},
 \qquad \operatorname{Im}\tau>0,
\]

where `Z_M={m in Z: |m|<M}` and the lattice order first compares the coefficient of tau, then the integer coefficient. The **N-limit is taken first**. In particular, the entry 2 is included with the prescribed iterated summation; imposing `k_1 >= 3` instead would narrow the problem. The empty word evaluates to 1.

Let `H^1=Q<z_1,z_2,...>`, let `H^0` consist of the unit and words not beginning with `z_1`, and let `H^{>=2}=Q<z_2,z_3,...>`. The harmonic product has the positive merge term

\[
z_a u*z_b v=z_a(u*z_bv)+z_b(z_au*v)+z_{a+b}(u*v).
\]

The shuffle product is the ordinary shuffle in `x,y` after identifying `z_k=x^{k-1}y`. Write it as `shuffle`. Define

\[
\varphi(w)=w*z_2-w\mathbin{\shuffle}z_2,
\qquad \theta(w)=-\mathcal D(\varphi(w)),
\]

where `mathcal D` is the **specific** Hirose–Maesaka–Seki–Watanabe Drop1 operator, not an arbitrary map preserving multiple zeta values. It fixes `H^{>=2}`. The original asks for

\[
2\pi i\frac{d}{d\tau}G(w)=G(\theta(w)),
\qquad w\in H^{\ge2}.
\tag{1}
\]

The normalization is important: for `q=exp(2 pi i tau)`, the left operator is `(2 pi i)^2 q d/dq`, rather than `q d/dq`. No normalization by powers of `2 pi i` has been applied to `G`.

The lattice series in (1) do not require choosing a value for a divergent index containing 1. Such indices appear only at an intermediate algebraic stage and are removed by Drop1. The auxiliary bi-series proof does use regularized multitangent and zeta values, which must agree with the displayed classical series on the all-at-least-two subspace. The source's Drop1 reference uses increasing summation indices and last-entry admissibility; v2 writes the reversed, decreasing-index convention used here. Its Section 4.1 explicitly gives the operator in that convention.

Neither `varphi` nor theta is a derivation on the free harmonic algebra itself. In v2, theta's failure is `-R(u,v)`; the evaluated derivative property relies on actual relations. One must not assume that a free-algebra Leibniz rule proves (1).

## 2. Version history and exact scope of the newer theorem

- [Version 1](https://arxiv.org/pdf/2602.08176v1), 9 February 2026, 28 pages, by Henrik Bachmann and Hayato Kanno: Section 4.2, printed p. 20, states (1) as Conjecture 4.6(ii). Depth-one identities were already proved and credited to earlier work.
- [Version 2](https://arxiv.org/pdf/2602.08176v2), uploaded 13 July 2026 at 07:43:39 UTC, 42 pages, by Henrik Bachmann, Hayato Kanno and Takumi Maesaka: the document itself is dated 14 July. Main Theorem D on pp. 8 and 30 proves exactly (1). The proof is on p. 30; it uses Main Theorem C, Sections 3.1–3.2 and the one-1 Drop1 formula in Section 4.1. Both versions were downloaded in full.
- The [current arXiv record](https://arxiv.org/abs/2602.08176) lists v2 as latest, with no withdrawal notice visible. The [author's publication list](https://www.henrikbachmann.com/publications.html), last updated 25 September 2026, lists the three-author paper among submitted preprints. No final journal version of this paper was identified in this bounded search.
- The report still records the February talk's conjecture. The pinned August assessment says the paper did not prove it, but that statement does not describe the retrieved July v2. This is a source/version correction, not a new discovery of the identity.

**Still conjectural:** v2 Conjecture 1.8 says `DR_* = ker G`, a completeness assertion about all relations. Main Theorem D does not prove this equality. The adjacent imported records 30006588 and 30006589 concern that different relation-presentation topic and are not resolved by this record. Likewise, v2 Conjecture 4.9 concerns a broader multi-1 Drop1 description and is not needed for (1).

## 3. The final algebraic reduction, reconstructed with its inputs explicit

To avoid confusing Drop1 with a derivative, reserve `mathcal D` for Drop1 and use `partial` for the formal derivative on bi-words. A bi-letter is `[k;d]`, with `k>=1,d>=0`; harmonic merging adds both entries. Ordinary words embed by putting every lower entry equal to zero. Set

\[
\partial[k_1,\ldots,k_r;d_1,\ldots,d_r]
=\sum_{j=1}^r k_j
[k_1,\ldots,k_j+1,\ldots,k_r;
 d_1,\ldots,d_j+1,\ldots,d_r].
\]

Let I be the harmonic ideal generated by `sigma(v)-v`, where sigma is the swap involution defined by the coefficient substitution

\[
(u_1,\ldots,u_r;v_1,\ldots,v_r)
\longmapsto
(v_r,v_{r-1}-v_r,\ldots,v_1-v_2;
 u_1+\cdots+u_r,u_1+\cdots+u_{r-1},\ldots,u_1)
\]

in the generating series with monomials `u_1^{d_1}/d_1! ... u_r^{d_r}/d_r! v_1^{k_1-1} ... v_r^{k_r-1}`. The divided powers affect coefficients; in depth one, sigma sends `[k;d]` to `d!/(k-1)! [d+1;k-1]`.

The cited proof uses these specific inputs:

1. `partial(w) = varphi(w) mod I` for ordinary words. This is the earlier formal-Eisenstein result, restated as v2 Theorem 3.5. The direct identity preceding Lemma 3.6 also gives it using swap invariance.
2. For `a=z_{k_1}...z_{k_r}`, `b=z_{l_1}...z_{l_s}`, all indices at least two and `r>=1`, v2 Lemma 4.8 gives
   \[
   (\mathcal D-\mathrm{id})(az_1b)
   \equiv \rho_r(ab)-\rho_{r+1}(ab)\pmod I,
   \tag{2}
   \]
   where `rho_j` raises only lower entry j from zero to one, and an out-of-range rho is zero.
3. The analytic realization `mathscr G` of v2 Main Theorem C annihilates I, restricts to the classical G on `H^{>=2}`, and satisfies `mathscr G(partial v)=2 pi i d mathscr G(v)/d tau`.

Here is the all-word cancellation from these inputs. In `w shuffle z_2`, where `w=z_{k_1}...z_{k_r}`, a term containing 1 has exactly one such entry, not in first position. Its complete contribution is

\[
2\sum_{1\le j<i\le r+1} k_j
 z_{k_1}\cdots z_{k_j+1}\cdots z_{k_{i-1}}
 z_1z_{k_i}\cdots z_{k_r}.
\tag{3}
\]

This is obtained by inserting the two letters `xy` of `z_2` in the literal `x,y` shuffle. All other output indices are at least two and are fixed by Drop1. Apply (2) to each summand of (3). For fixed j the lower-entry contribution is

\[
\sum_{i=j+1}^{r+1}(\rho_{i-1}-\rho_i)
=\rho_j,
\]

including the terminal zero term. Hence

\[
(\mathcal D-\mathrm{id})(w\shuffle z_2)
\equiv2\partial(w)\pmod I.
\]

Since `mathcal D(w*z_2)=w*z_2`, this implies

\[
\theta(w)
\equiv w\shuffle z_2+2\partial(w)-w*z_2
=2\partial(w)-\varphi(w)
\equiv\partial(w)\pmod I.
\]

Input 3 now gives (1). The unit has `varphi(1)=theta(1)=0`, so it causes no exception. This is the preprint's proof mechanism, credited to its authors, not an independent discovery or an argument establishing the completeness conjecture.

For reproducibility, the checker computes Drop1 on the only additional kind of word required here using v2 Theorem 4.7. With S the quasi-shuffle antipode, that formula is

\[
\mathcal D(az_1b)
=az_1b+\sum_{a=a_1a_2}
 a_1*\big((S(a_2)*b)\shuffle z_1\big).
\tag{4}
\]

This is a formula for the stated Drop1 operator, not a replacement definition justified solely by preserving ordinary zeta values. The source proves it by finite harmonic/diamond sums and the cited independence theorem. Its reduction to (2) uses the antipode identity and Appendix Lemma A.3. Our exact checks include those finite-harmonic identities and bi-letter antipode controls.

## 4. Analytic realization: what was read and what remains an audit dependency

The full relevant v2 proof was read, not merely its theorem statements: the definitions and product/swap conventions, Sections 3.1–3.2, Theorem 4.7, Lemma 4.8, Main Theorem D, and Appendix Lemma A.3. The published [Bachmann–Burmester paper](https://doi.org/10.1007/s40687-023-00398-8), Theorem 6.26 and its proof on pp. 28–29, was also inspected because v2 Theorem 3.19 invokes the analogous swap-invariance manipulation.

The construction uses the modified regularized multitangent mould `Psi^+=Psi^* times delta_{pi i}`. Its nonempty coefficients have zero constant Fourier term. The v2 blocks factor as an exponential `exp(-2 pi i m sum u_j)` times a convolution of a zeta u-mould, `Psi^+(m tau)` and a reversed zeta u-mould. Blocks are summed over decreasing positive m's and then convolved with the bi-zeta mould.

The following normalization checks were made directly:

- The depth-one block is
  \[
  -2\pi i\sum_{n>0}e^{-2\pi i(mu+nv)}q^{mn}.
  \]
  The addition of `pi i` cancels the depth-one constant term. The same scaling of both variables preserves the partition-swap substitution; it does not turn the target into a differently normalized derivative formula.
- The multivariable differential operator is `sum_j partial_{u_j} partial_{v_j}`. Coefficient extraction gives `k_j` and raises both displayed entries, exactly as in the formal partial above. The divided powers supply no extra `(d_j+1)`.
- In each block, only the middle multitangent factors depend on the relevant v variables. The derivative in the corresponding u variable differentiates the exponential, giving the factor `-2 pi i m`. In deconcatenated products, coordinate blocks are disjoint, so there are no mixed derivatives between distinct blocks. The terminal bi-zeta convolution has zero same-coordinate mixed derivative.
- For a fixed coefficient and a compact subset of the upper half-plane, the multitangent Fourier expansion and its finitely many derivatives have exponential decay in m, multiplied by at most a fixed polynomial. Ordered multiple m-sums are therefore locally normally convergent, which supports termwise differentiation. This check concerns fixed coefficients, not a claim of uniform convergence over all weights and depths at once.

The remaining audit hold is **all-depth certification of the auxiliary regularized realization**, including its full swap-invariance transfer and the imported regularization/diamond-basis theorems. The published combinatorial realization alone is insufficient: its rational q-series are not the classical multiple Eisenstein series. V2 supplies the additional classical realization, and that is a substantive part of its claimed proof. We have read its proof and checked the displayed mechanism but have not independently rederived every imported mould identity and every underlying regularization theorem. No counterexample or mathematical error in those arguments is asserted.

The older Drop1 paper and the bi-zeta reference were recovered in full and their relevant definitions/theorem statements consulted. They are recorded as dependencies, not silently promoted to proofs independently rechecked in their entirety. A scanned RIMS proceedings note was downloaded but was not text-readable; it is not used as proof evidence.

## 5. Verification, attribution and disposition

`verify.py` is a standard-library rational-arithmetic checker. Its 1,111 assertions cover the exact one-1 shuffle component for every admissible word through weight 11, Drop1 output support and weight, the terminal telescoping identity, the unit, the source's three low-weight examples, earlier depth-one/all-twos formulas, 252 bi-letter antipode identities, swap divided-power normalization and 72 finite diamond-sum tests. It computes literal shuffles independently of formula (3). These bounded checks cannot establish the analytic realization or verify infinitely many derivative identities.

There were **zero new-discovery approaches**. One explicitly logged **validation/reconstruction family** checked an already-posted result. The original conjecture has an externally supplied full proof claim as of v2; our full-proof audit remains incomplete. Any queue disposition should retain that distinction, and no `claimed_solved` credit should be assigned to this campaign from this package. A conservative local status is `unsolved` with an external-preprint-resolution/source hold until a complete proof audit is accepted.

No statement here establishes the separate all-relations conjecture, a result for arbitrary divergent-index regularizations, or a new formula with a changed derivative normalization.

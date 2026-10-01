# Independent derivation and adversarial audit

**Audit scope:** the stated scalar band-splitting proposition only. No PR12 source proof, prior review, or parent notes were read.

## Exact claim and assumptions

Let `(W, F, nu)` be a measure space. Let each `rho_n : W -> (0, infinity)` be measurable, with `n in Z`. Assume there are a **single** integer `d >= 1`, a **single** `eta in (0,1)`, and a **single** `Q >= 1` such that, on one common conull subset of `W`, for every integer `n`,

\[
 Q^{-1}\le \rho_{n+1}/\rho_n\le Q,
 \qquad \min(\rho_{n-d},\rho_{n+d})\le\eta\rho_n.
\]

The common conull subset follows from separate almost-everywhere hypotheses by countable intersection. The bound `Q` must be uniform in both `n` and `w`. The result permits either support band to be zero.

The proposed conclusion holds: there is a measurable lower fiber band `M`, its complementary upper band `N`, and constants `A < infinity` and `lambda < 1`, depending only on `Q,d,eta,p`, such that

\[
 B M\subseteq M,\quad B^{-1}N\subseteq N,\quad
 \|B^k|_M\|\le A\lambda^k,\quad
 \|B^{-k}|_N\|\le A\lambda^k\qquad(k\ge0).
\]

Here `M` and `N` denote the corresponding subspaces of `L^p(W x Z)`, not merely their support sets.

## Independent discrete proof

Work first at a fixed good fiber `w`, suppressing it from the notation. Set

\[
 u_n=\log\rho_n,\qquad a=-\log\eta>0,\qquad L=\log Q.
\]

For `r = 0,...,d-1`, write

\[
 v_r(k)=u_{r+dk},\qquad
 \Delta_r(k)=v_r(k+1)-v_r(k).
\]

The drop condition is exactly

\[
 \Delta_r(k-1)\ge a\quad\text{or}\quad\Delta_r(k)\le-a.
\]

Thus `Delta_r(k) < a` implies `Delta_r(k+1) <= -a < a`. The set of nongrowth edges is an upper integer interval. Define its first edge by

\[
 t_r=\inf\{k\in\mathbb Z:\Delta_r(k)<a\}
 \in\mathbb Z\cup\{-\infty,+\infty\},
\]

with the empty-set convention `t_r = +infinity`. The recurrence gives

\[
 \Delta_r(k)\ge a\quad(k<t_r),\qquad
 \Delta_r(k)\le-a\quad(k>t_r).
\]

When finite, the single edge `k=t_r` can be intermediate; it satisfies `|Delta_r(t_r)| <= dL` by the neighboring-ratio bound. If `t_r=+infinity`, every edge grows by at least `a`; if `t_r=-infinity`, every edge decays by at least `a`.

### Residue cuts cannot separate indefinitely

The local log bound yields, for every aligned index `k`,

\[
 |v_r(k)-v_s(k)|\le |r-s|L.
\]

Suppose finite cuts satisfy `t_r < t_s`. For each edge

\[
 k=t_r+1,\ldots,t_s-1,
\]

residue `r` has a drop of at least `a` and residue `s` has a rise of at least `a`. Consequently,

\[
 [v_s(k+1)-v_r(k+1)]-[v_s(k)-v_r(k)]\ge2a.
\]

Summing over those `t_s-t_r-1` edges and bounding both endpoint differences gives

\[
 2a(t_s-t_r-1)\le 2|r-s|L,
 \qquad
 |t_r-t_s|\le1+\frac{|r-s|L}{a}.
\]

This same argument over arbitrarily long finite edge intervals rules out any finite/infinite mismatch, or opposite infinite cuts. Therefore there are exactly three possible cases:

1. Every residue cut is `+infinity`.
2. Every residue cut is `-infinity`.
3. Every residue cut is finite, with a uniform separation bound.

In the finite case, put

\[
 H=1+\left\lceil\frac{(d-1)L}{a}\right\rceil.
\]

Then `|t_r-t_0| <= H` for every `r`. This loose bound also covers `d=1`.

### A single cut and explicit exponential constants

In the finite case choose `K = d t_0`, and define the lower support by `n <= K`. If `j=r+dk <= K`, then `k <= t_0`, so at most `H` backward `d`-edges from `j` fail to be growth edges. If `j>K`, then `k>=t_0`, so at most `H+1` forward `d`-edges from `j` fail to be decay edges. Every exceptional edge has log ratio at most `dL` in either direction. It follows that, with

\[
 C_0=\left(Q^d/\eta\right)^{H+1},
\]

\[
 \rho_{j-qd}/\rho_j\le C_0\eta^q\quad(j\le K),
 \qquad
 \rho_{j+qd}/\rho_j\le C_0\eta^q\quad(j>K),
 \qquad(q\ge0).
\]

Writing an arbitrary shift as `ell = qd+s`, where `0<=s<d`, and using at most `s` neighboring-ratio bounds gives

\[
 \rho_{j-\ell}/\rho_j\le C\eta^{\ell/d}\quad(j\le K),
 \qquad
 \rho_{j+\ell}/\rho_j\le C\eta^{\ell/d}\quad(j>K),
\]

where one permissible uniform constant is

\[
 C=Q^{d-1}\left(Q^d/\eta\right)^{H+1}
      \eta^{-(d-1)/d}.
\]

If all cuts are `+infinity`, choose `K=+infinity`: every `d`-edge grows and the entire space is the lower band. If all cuts are `-infinity`, choose `K=-infinity`: every `d`-edge decays and the entire space is the upper band. The same loose constant `C` works in both cases.

### Measurability and the operator conclusion

For each integer `k`, the condition `Delta_0(k,w)<a` is measurable. Its first index `t_0(w)` is therefore extended-integer-valued measurable: for example, `{t_0 <= m}` is the countable union of the nongrowth-edge events at indices `k<=m`. Thus `K(w)=d t_0(w)` and

\[
 S_M=\{(w,n):n\le K(w)\},\qquad S_N=S_M^c
\]

are measurable. Choose any cut on the null exceptional fibers. Let `M` and `N` be the `L^p` support subspaces of these sets. The lower support is stable when the backward shift moves a source coordinate `j` to `j-1`; the upper support is stable under the inverse shift.

For `g in M`, the exact norm identity is

\[
 \|B^\ell g\|_p^p
 =\sum_{j\in\mathbb Z}\int_W
      \frac{\rho_{j-\ell}(w)}{\rho_j(w)}|g_j(w)|^p\,d\nu(w)
 \le C\eta^{\ell/d}\|g\|_p^p.
\]

The same identity with `rho_{j+ell}/rho_j` gives inverse decay on `N`. Accordingly, take

\[
 A=C^{1/p},\qquad \lambda=\eta^{1/(pd)}<1.
\]

This uses neither strict convexity nor duality and includes `p=1`. Neighboring-ratio bounds also make `B` and `B^{-1}` bounded on the entire space.

## Adversarial boundary cases

### Disagreeing residue peaks

For `d=2`, use `u_{2k}=-a|k-A|` and `u_{2k+1}=-a|k-B|`. Each residue obeys the drop condition exactly and has cut `A` or `B`. As `k` tends to the two infinities, the odd/even log difference tends to the opposite values `+a(B-A)` and `-a(B-A)`. A uniform neighboring log bound `L` therefore forces `a|B-A|<=L`. Far-separated parity peaks are incompatible with a fixed `Q`. Unequal but bounded cuts do occur; the proof must tolerate them.

### Both-direction drops

For `rho_n=exp(-c|n|)` with `c=a/d`, both `d`-neighbors drop by exactly `eta` at the peak. This creates an admissible peak, not an obstruction to a lower/upper support split. A single intermediate residue edge is already accounted for in `C_0`.

### Moving and unbounded fiber cuts

For any measurable integer-valued function `J(w)`,

\[
 \rho_n(w)=\exp[-(a/d)|n-J(w)|]
\]

has neighboring ratio bound `Q=exp(a/d)` and the drop condition at every `n`. `J` can be unbounded in both directions. The proof constructs a measurable cut and the decay constants do not depend on its location. No integrability or essential bound on the cut is required.

### Zero and full bands

The examples `rho_n=exp((a/d)n)` and `rho_n=exp(-(a/d)n)` respectively give globally decaying `B` and globally decaying `B^{-1}`. The natural complementary splitting has one zero band. If the intended conclusion required **both bands to be nonzero**, the stated hypotheses would not imply it.

### What fails without the global neighbor bound

For `d=2`, take `rho_{2k}=exp(ak)` and `rho_{2k+1}=exp(-ak)`. Each residue satisfies the drop condition, but their infinite orientations disagree and no single integer/extended cut gives the asserted two-sided decay. The neighboring ratios are unbounded. This confirms exactly where the global neighbor assumption enters.

## Strongest verified conclusion and remaining gap

The proposition, with measurable positive weights, a common global neighbor bound, integer `d`, and possibly zero bands, is verified by the complete independent argument above. No mathematical gap was found in this scalar claim. This audit does **not** verify any identification of the weights with a particular measure-theoretic model, any source-paper theorem beyond the proposition, or a stronger conclusion requiring two nonzero bands.

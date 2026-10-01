# 5100008 / AMR-050-0008: k117 is already proved

**Disposition requested:** `already_solved`, 0/5 new proof-attempt turns.
This is a primary-source status correction, not an original result. Independent
source-scope review is pending at this freeze.

## Exact target and edition reconciliation

The pinned record asks separately for constancy of
\(\prod_{i=1}^N l_i\) and \(\prod_{i=1}^N r_i\), where
\(Q_i=P_i''\), \(l_i=|P_iQ_i|\), and \(r_i=|Q_iP_{i+1}|\), for even
period in a fixed confocal elliptic billiard family.

Reznik, Garcia, and Koiller's arXiv:2004.12497v11, Table 2 (p.5), and its
published version, *Fifty New Invariants of N-Periodics in the Elliptic
Billiard*, Arnold Math. J. 7 (2021), Table 2 (p.345), both label this row
**k117**. Both initially show an unknown value and proof. The table credits
its experimental discovery to **Hellmuth Stachel**. Nearby codes do change
between editions, but this code and formula do not.

The original source's introduction defines this elliptic billiard using two
confocal **ellipses**, with positive caustic semiaxes. Its polygon areas are
signed, but no area enters k117. Neither an outer-polygon area nor its
nonvanishing is a hypothesis for this product invariant. Crossing/star
polygons are not excluded.

Sources: [arXiv v11](https://arxiv.org/pdf/2004.12497v11),
[2021 published table](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf).

## Published resolution and notation bridge

Hellmuth Stachel, *On the motion of billiards in ellipses*, European Journal
of Mathematics **8** (2022), 1602–1622, published online 24 January 2022,
[DOI 10.1007/s40879-021-00524-2](https://doi.org/10.1007/s40879-021-00524-2),
**Theorem 5.6**, p.1621 (PDF p.20), explicitly identifies k117 and proves
\[
 \prod l_i=\prod r_i=(a^2-a_c^2)^{N/2}=(b^2-b_c^2)^{N/2}.
\]
Here \(a,b\) are the outer semiaxes and \(a_c,b_c>0\) the caustic semiaxes.
Stachel's parameter is \(k_e=a^2-a_c^2=b^2-b_c^2>0\).
His Lemma 5.1 uses \(l_i=|P_iQ_i|\) but
\(r_i^{S}=|Q_{i-1}P_i|\). Thus the imported \(r_i=r_{i+1}^{S}\);
the cyclic products coincide exactly. Both products are positive lengths,
so there is no signed-length or square-root ambiguity.
The preprint [arXiv:2105.03624](https://arxiv.org/abs/2105.03624) already has
this result as **Theorem 10** (pp.17–18).

## Period and crossing boundary

The source-normalized claim uses the **primitive period** N. Stachel's
canonical parametrization has turning number \(\tau\) coprime to N
(Theorem 4.3), and the even-period arguments explicitly use that \(\tau\)
is odd. This includes admissible star polygons with \(\tau>1\), not only
simple polygons. Orientation reversal exchanges the two products and does
not change their value.

The quarter-shift underlying the proof is \(\tau K\), which is congruent
to \(K\) modulo \(2K\) for odd \(\tau\); hence the usual identity
\(\mathrm{dn}(u)\mathrm{dn}(u+K)=b_c/a_c\) works equally for stars.
Here dn has period 2K. One must not copy an erroneous sign attached to its
2K-shift in the published text. The final proof also prints `N=2n+2` in
its remaining case; its referenced Theorem 5.4 and pair indices use
`N=4n+2`. These typographical issues do not alter Theorem 5.6's statement.

The imported wording does not expressly say 'primitive' and says only
'confocal caustic'. This correction records the actual ellipse/primitive
scope rather than silently claiming a broader theorem. Repetition of a
primitive even orbit preserves the formula by taking powers. Repetition of
an odd primitive orbit until its listed length becomes even is **not**
covered by the even-primitive-period theorem. Hyperbolic or degenerate
caustics are likewise outside this source correction. No purported
counterexample from such an enlargement is attributed to the original k117.

## Prior-work gate and credit

At 2026-10-01 04:44–04:47 UTC, checks of local all-ref commit messages,
local catalog/status/history, GitHub PR searches for 5100008 and k117,
branch search for 5100008, the target attempt-directory commit history,
and the conventional dot/math-5100008 PR endpoint found no previous Alec
attempt or PR for this exact target. GitHub code search returned a desk-review
assignment entry, not a proof attempt. Related k107/k108, k114, k115, and
k120 work was not treated as an attempt on k117.

The pinned upstream report is existing third-party triage, not an earlier
Alec attempt. Its statement that no general proof was found is superseded
by Stachel's exact primary theorem. All mathematical credit remains with
Stachel and the cited source authors. No originality or novelty is claimed.

**Completion estimate:** 100% of source-status identification; external
publication awaits independent source-scope review. No unresolved research
search has been opened and no proof-attempt turn has been consumed.

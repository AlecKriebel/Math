# Independent primary-source audit: Zemyan 2003 versus PR563 / Problem 2306072

## Verdict and strongest verified conclusion

**This complete source does not supply an earlier negative resolution of either target question or the candidate's exact perturbed coefficient mechanism.** It supplies a genuine support point with nonmonotone **tangent direction**. Its constructed omitted slit has strictly monotone polar argument and strictly monotone radial angle, including the ordinary angle magnitude. Thus its counterexample is a concrete falsification of the proposed implication “tangent wavering implies target-angle nonmonotonicity.”

This conclusion is based on all six article pages, the complete proof, the remark, all figures, the conjecture, and all references, rather than on the title or abstract. The source expressly reports positive polar/radial monotonicity results for its evaluation-functional family on p. 792. The independent derivation below proves those positive properties on the entire specific omitted slit used to prove its theorem.

The source overlaps substantially in the classical support-point geometry, Schiffer trajectory method, explicit extremal realization, and study of slit turning. Those must be credited as prior tools. Its exhibited slit is not an instance of the candidate's finite coefficient construction, and its theorem does not imply the two target negative conclusions. **This is a bounded comparison with one source, not certification of literature completeness, historical firstness, the problem's present status, or publication clearance.**

## Inputs, independence, and complete coverage

The audited source is Stephen M. Zemyan, *The Existence of a Waver Point on the Omitted Arc of a Support Point of the Class S*, **Complex Variables, Theory and Application** 48(9) (2003), 791-796, DOI [10.1080/02781070310001599359](https://doi.org/10.1080/02781070310001599359). The supplied file contains seven PDF pages: a publisher wrapper followed by six article pages. The article records receipt on 15 June 2003 and final form on 24 June 2003. The wrapper's 15 September 2010 online date is separately recorded; it does not replace the 2003 journal identity.

The user-supplied download and the program's cached copy have identical SHA-256:

`a444de051594f2981e1787ed47e70dcc3401c5e0e863856243f8cb8eff382079`.

The cached input is `draft_pr_claimed_solved_500_600_20261012/sources/pr563/user_supplied_20261013/zemyan2003.pdf`. The candidate inputs were the audit's immutable original `original/unsolved_math_prioritization/attempts/2306072/PROOF.md` and preparation manuscript `publication/support_slit.tex`. Their exact hashes are in `SOURCE_INPUTS.json` and `CHECKS.json`.

I read and visually inspected the complete wrapper and all six article pages. Equations on pp. 792-794 were verified against full-page renderings, including powers, conjugation, square-root branch, and the complex exponent in the tip calculation. `SOURCE_COVERAGE.json` records each page. Raw fulltext and renderings remain under ignored `.cache/`, outside the authored seal.

`SOURCE_FIRST_DERIVATION.md` records the source's mechanism and observables before candidate comparison. No preceding priority reports, review verdicts, or other agents' findings were read. No other researcher was contacted. Work stayed in the assigned audit folder on `main`; no canonical file, branch, remote, or publication state was changed. The parent owns any subsequent repository checkpoint.

### Page-specific findings

| Article page / PDF page | Complete content and exact mathematical scope |
|---|---|
| 791 / 2 | Defines support points through a **global** maximization of a nonconstant continuous linear functional. Recalls an actual omitted analytic arc, increasing modulus, and an asymptotic half-line. Defines wavering by nonmonotonicity of `arg w'`, rather than `arg w`. |
| 792 / 3 | States an existential tangent-waver theorem. Uses Brown's actual extremizers of `max Re g(z0)`, `0<|z0|<1`, not arbitrary trajectories. Gives differential (1.2), Koebe-of-spiral parametrization (1.3), tangent derivative (1.4). Explicitly says Brown proved decreasing `arg w` and decreasing `arg(w/w')` tending to zero for this family. |
| 793 / 4 | Gives Brown's extremal differential and explicit `f=4BV/(1+V)^2`, with `V,M,Q`; identifies the finite boundary preimage. Derives the complex tip relation (1.5). The tip-preimage reasoning needs its inside-disk branch understood; that branch is checked below. |
| 794 / 5 | Gives `T` in (1.6), tip formulas (1.7)-(1.8), and the specific exact input `z0=(2/5)exp(5 pi i/6)`. Solves the scalar equation for `arg B`; reports approximate `B,T` and negative initial tangent angular velocity. Figure 1 plots that angular velocity, not either target angle. |
| 795 / 6 | Gives negative/positive tangent-velocity samples at `t=.40,.45`, continuity argument, approximate interior waver, and coordinates of tip and waver. Figures 2-3 and the geometry remark concern the same actual support slit. |
| 796 / 7 | Finishes the geometric interpretation and proposes exactly `n` interior **tangent** wavers for every positive integer `n`. This is explicitly a conjecture, not a proven general classification or a radial-angle theorem. References are Brown 1979, Brickman-Wilken 1974, Pfluger 1971. |

The theorem is existence of at least one tangent waver. The paper's displayed root and figures do not constitute a certified count of exactly one waver over the entire slit; none is needed for its theorem. Its last conjecture must not be promoted to a theorem.

## Source mechanism: a genuine point-evaluation extremizer

The source fixes a nonzero `z0` in the unit disk and uses a function maximizing `Re f(z0)` over the normalized schlicht class. Point evaluation is continuous and complex linear on the ambient analytic-function space. Compactness supplies a maximizer, and evaluation is nonconstant on the class: the small univalent perturbations `z+delta z^2` change its real part for suitable `delta`. Hence this is a genuine global support point.

On pp. 792-793 the paper invokes Brown 1979 for the complete characterization and actual omitted arc of this extremizer. Let

\[
 B=f(z_0)=b e^{i\eta},\quad 0<\eta<\pi,\qquad
 q=B^{-1/2},\quad \arg\sqrt B=\eta/2.
\]

Its parameter `t` increases **outward**, from the finite tip at `t=0` to infinity as `t` approaches `T` from below. Define

\[
 s(t)=e^{(t-T)q},\qquad
 w(t)=-4B\frac{s(t)}{(1-s(t))^2}. \tag{S1}
\]

The source differential and independently differentiated identities are

\[
 \frac{B^2}{B-w}\left(\frac{w'}w\right)^2=1,
 \quad \frac{w'}w=q\frac{1+s}{1-s},
 \quad \frac{w''}{w'}=q\frac{1+4s+s^2}{1-s^2}. \tag{S2}
\]

For example, `B-w=B(1+s)^2/(1-s)^2`, so direct substitution verifies the first identity. All these statements have the source's **actual support realization** as an input. The trajectory identity by itself would not prove univalence or global maximality of a newly invented curve. This audit independently checks the formula's normalization, branch, differential, and angular consequences; it does not replace a proof of Brown's characterization.

### Normalization and finite tip

Set

\[
 r=2/5,\quad R=\log(7/3),\quad
 \eta+R\sin\eta=5\pi/6,\quad
 b=\frac r{1-r^2}e^{R\cos\eta},\quad e=e^{-i\eta}.
\]

The symbol `e` here is Zemyan's unit phase, not the candidate's `epsilon=10^-24`. The scalar equation has a unique root because its derivative is bounded below by `1-R>0`. Directed interval evaluation brackets it by

\[
 1.79119112133250053117<\eta<1.79119112133250053118.
\]

The explicit extremal formula on p. 793 has

\[
 V(z)=\frac{z(1-r^2)M(z)^e}{z_0Q(z)},\quad
 f(z)=\frac{4BV(z)}{(1+V(z))^2},\quad
 M(0)=e^{-R},\quad Q(0)=4.
\]

Therefore

\[
 f'(0)=\frac{B(1-r^2)e^{-eR}}{z_0}=1,
\]

since the above magnitude and phase equations give `B=z0 exp(eR)/(1-r^2)`. This is an exact normalization check, with a separate interval residual in `CHECKS.json`.

The finite boundary preimage is `ztip=-z0 B/|z0 B|`. At that point, write

\[
 A_t=\sqrt{1+1/(re)},\quad C_t=\sqrt{1+r/e},\quad
 Q_t=(A_t+C_t)^2,\quad
 M_t=\frac{(C_t-rA_t)^2}{1-r^2}.
\]

The p. 794 formula becomes

\[
 T=\sqrt b\sec(\eta/2)\left[\log|Q_t|-\Re(e\log M_t)+\log\frac r{1-r^2}\right]. \tag{S3}
\]

The square roots are continued from their positive values at `z=0`. Along `z=u ztip`, `0<=u<=1`, their squared arguments are `1+u/(re)` and `1+ru/e`, in the upper half-plane for `u>0`. The roots remain in the first quadrant. Also

\[
 M(u)=\frac{1-r^2}{(C(u)+rA(u))^2},
\]

using `C(u)^2-r^2 A(u)^2=1-r^2`. Its argument stays strictly between `-pi` and `0`, so the principal logarithm is the continuous branch inherited from `M(0)>0`. No unrecorded multiple of `2 pi i` is inserted in the complex exponent.

The source's two tip representations require `-s(0)=V(ztip)`. The rational map `v/(1+v)^2` has a reciprocal ambiguity: equality at `u,v` implies `(u-v)(1-uv)=0`. The wording on p. 793 about a unique unit-circle preimage does not by itself remove this ambiguity, because the two auxiliary values being equated here lie inside the disk. For this example, interval controls prove `|s(0)|<1`, `|V(ztip)|<1`, and `|1/V(ztip)|>1`; hence equality of the tip images selects the same inside-disk value. The phase relation has a small interval residual enclosing zero. That residual is a consistency check, not a substitute for the exact branch argument.

The certified parameter values reproduce

\[
 B\simeq-0.08649982553+0.38610133999i,\quad
 T\simeq1.62521267773,\quad
 w(0)\simeq0.14175147270+0.21785807509i.
\]

The printed tip/parameter approximations agree within one unit of their last displayed digit; some are truncated rather than correctly rounded. Taylor expansion of the explicit source formula also gives

\[
 a_2=\frac{(1+r^2)/2+er}{z_0}-\frac1{2B}
 \simeq-1.27805880264+1.46249045360i,
\]

well outside the candidate's uniformly near-`a2=2` extremizers.

## Distinguishing and checking all three angles globally

Let `theta=arg w`, `phi=arg w'`, with continuous lifts, and let `beta_s=theta-phi=arg(w/w')` use the source's radial-angle convention. Its outward signed angle in the candidate's convention is `beta_out=phi-theta=-beta_s`. From (S2),

\[
 \theta'=\Im\left(q\frac{1+s}{1-s}\right),\quad
 \phi'=\Im\left(q\frac{1+4s+s^2}{1-s^2}\right),\quad
 \beta_s'=\Im\left(-\frac{2qs}{1-s^2}\right). \tag{S4}
\]

The last identity follows by subtracting the first two rational expressions. A sign reversal in the middle expression is not a sign reversal in either other expression.

Put `h=T-t>0` and `xi=hq=x-iy`, with `x,y>0`. Then `s=exp(-xi)` and

\[
 w=-B\operatorname{csch}^2(\xi/2),\quad
 \frac{w'}w=q\coth(\xi/2).
\]

Straight separation of real and imaginary parts gives the exact formulas

\[
 \theta'=\frac{x\sin y-y\sinh x}{h(\cosh x-\cos y)}, \tag{S5}
\]

\[
 \beta_s'=-\frac{x\cosh x\sin y-y\sinh x\cos y}
 {h(\sinh^2x+\sin^2y)}, \tag{S6}
\]

\[
 \frac{d}{dt}\log|w|=\Re\frac{w'}w
 =\frac{x\sinh x+y\sin y}{h(\cosh x-\cos y)}. \tag{S7}
\]

Every denominator is positive. Since `sin y<=y` and `sinh x>x`, (S5) is strictly negative for every `h>0`. In particular the entire source example's polar argument is strictly decreasing, regardless of its tangent waver.

For the radial angle, the interval calculation proves

\[
 0<y\le y_{\rm tip}=T\sin(\eta/2)/\sqrt b
 \simeq2.01679005721<\pi.
\]

If `0<y<pi/2`, dividing the numerator of (S6) by `xy cosh(x) cos(y)` reduces its sign to that of

\[
 \tan(y)/y-\tanh(x)/x>1-1=0.
\]

If `pi/2<=y<pi`, the numerator is directly positive since `sin y>0` and `cos y<=0`. Thus **`beta_s'<0` on the entire slit**. Moreover (S7) is strictly positive in this range. Combined with `theta'<0`, this places `w'/w` in the fourth quadrant and fixes

\[
 -\pi/2<\beta_{\rm out}<0,\quad
 0<\beta_s<\pi/2,\quad
 |\beta_{\rm out}|=\beta_s.
\]

The ordinary radial angle magnitude decreases strictly to zero, while the signed outward angle increases strictly to zero. Reversing traversal preserves the existence of a monotone orientation. Using an inward tangent gives the supplement of the ordinary angle; using the acute tangent-line angle gives the same `beta_s`. Those conventions also stay monotone here.

### Reproduction of the tangent waver and failed angle bridge

The source's printed proof uses approximate numbers without displayed rounding enclosures. `checks.py` supplies directed interval enclosures with sign separation for the same exact parameter input. The following displayed digits summarize those enclosures, not new numerical assumptions:

| `t` | `theta'` | `phi'` | `beta_s'` | `beta_s` |
|---|---:|---:|---:|---:|
| 0 | -0.689609751 | -0.142407074 | -0.547202677 | 0.537990636 |
| 0.40 | -0.515000887 | -0.003000845 | -0.512000042 | 0.320654067 |
| 0.45 | -0.493300601 | +0.003759350 | -0.497059951 | 0.295419963 |
| 1 | -0.258752083 | +0.008457907 | -0.267209990 | 0.082080886 |

The opposite tangent-velocity signs prove an interior sign-changing zero. The angular velocity is analytic in the regular interior and not identically zero, so sign change cannot be confined to a zero plateau. A separate high precision root reproduction gives `t_waver approximately 0.4205099769` and `w approximately 0.3368924424+0.3092158873 i`; the exact digits in `CHECKS.json` control this rounded display. These root digits are diagnostic; the two interval sample signs suffice for existence. The waver is strictly between the finite tip and infinity on the actual omitted slit.

The tangent never reverses the direction of traversal: its radial component stays outward by (S7). “Reversal” here means reversal of its **clockwise versus counterclockwise rotation**. The differences `phi=theta-beta_s` permit `phi'` to change sign while both `theta'` and `beta_s'` remain negative. This resolves the apparent conflict without weakening either target definition.

### Infinity and boundary checks

Infinity is `h->0`, not `t=0`. The exact rational-series controls give

\[
 w=-4B^2/h^2+B/3+O(h^2),
\]

\[
 \theta'=\frac h6\Im(B^{-1})-\frac{h^3}{360}\Im(B^{-2})+O(h^5),
\]

\[
 \beta_s'=\frac h6\Im(B^{-1})-\frac{7h^3}{360}\Im(B^{-2})+O(h^5),
 \quad \phi'=\frac{h^3}{60}\Im(B^{-2})+O(h^5).
\]

The leading theta/beta terms cancel in `phi'`; dropping that cancellation would give an incorrect explanation of the waver. The source root has `pi/2<eta<pi`, so `Im(B^-1)<0` and `Im(B^-2)>0`. Thus the tangent angular velocity is positive near infinity while both target derivatives remain negative. The limiting polar argument is the continuous branch of `arg(-B^2)=2 eta-pi` for this first-quadrant slit. The radial angle tends to zero from above in the source convention.

At `y=0` the strict polar and radial sign arguments degenerate, as expected for a radial limiting slit. At `eta=pi/2` the displayed leading tangent coefficient vanishes and cannot alone determine a tangent waver. Neither limiting case is being used as the source's strict example. At `h=0` the curve diverges, so derivative formulas are applied only on the regular finite slit and extended through angle limits at infinity.

## Comparison with the candidate's exact mechanism

The candidate's target is a genuine global maximizer of

\[
 L(f)=a_2(f)+i\epsilon(a_4(f)-3a_3(f)),\qquad
 \epsilon=10^{-24},\quad\sqrt\epsilon=10^{-12}.
\]

Its universal claim is over **every maximizer of this functional**, with failure of global polar-argument monotonicity and failure of both signed and unsigned radial-angle monotonicity on the actual omitted slit. It neither asserts that every support slit has these failures nor asserts a tangent-waver count.

| Feature | Zemyan 2003 | Candidate mechanism |
|---|---|---|
| Actual global support functional | Point evaluation `f(z0)` at a specified nonzero `z0` | Finite coefficients `a2+i epsilon(a4-3a3)` |
| Realization | Brown's characterized actual evaluation extremizer and explicit map | Compactness, nonconstancy, uniform coefficient bounds for all maximizers |
| Differential coordinate | Koebe image of exponential spiral; `B,T` from actual extremal and tip | `w=-v^-2`, quartic `P(v)=a-bv^2+cv^4`, inverse of `integral sqrt P` |
| Actual tip control | Explicit boundary tip and branch from Brown's map | Area-theorem proximity plus conformal-radius inequality; tip radius `<3/10` |
| Traversal parameter | `t=0` at tip, increases to infinity at `T` | `t=0` at infinity, increases inward to `7/4` |
| Proven reversal | Sign of `phi'=(arg w')'` | Opposite signs of `Im Z`, giving opposite `theta'` signs and signed radial-angle values |
| Polar argument on construction | Strictly decreasing | Nonmonotone |
| Ordinary radial angle on construction | Strictly decreasing to zero | Positive at both sample points, zero between them |

No nonzero scalar multiple of point evaluation, plus a constant on normalized functions, equals the candidate's functional on `S`. To see this, test `z+delta z^n`, with `n>=5` and `n|delta|<1`, which is univalent because its derivative has positive real part. The candidate functional is unchanged; point evaluation changes by `delta z0^n`. Equality forces the evaluation scalar to vanish, contradicting the candidate's nonzero `a2` coefficient. Thus this is not a relabeling of the source functional. A shared use of Schiffer equations does not make the extremal problems or observables the same.

### Actual-support continuation and circularity check

The candidate does not identify an arbitrary necessary trajectory as sufficient for extremality. It first obtains actual global maximizers. Its coefficient bounds put them uniformly near Koebe. Its area-theorem estimate and the correctly directed inequality

\[
 \operatorname{dist}(f(z),\partial f(D))\le(1-|z|^2)|f'(z)|
\]

bound the **actual** finite slit tip below `3/10`, without asserting continuity of tips under perturbation.

The publication manuscript obtains a zero-free square-root branch on `|v|<=3`, an odd holomorphic inverse `V`, and the trajectory `W=-V^-2` on `0<t<=7/4`. In the natural coordinate, an actual slit tail approaching infinity has `Im G=0`; the two real rays project to the same arc by oddness. This establishes initial coincidence with the actual support slit. Local trajectory uniqueness continues it at each finite regular point. The tip cannot interrupt continuation because

\[
 |W|>25/81>3/10>r_{\rm tip},\quad
 25/81-3/10=7/810.
\]

Closedness of the actual omitted arc and local openness give the connected continuation argument. The manuscript explicitly supplies this argument rather than treating simple-pole uniqueness as a converse extremality criterion. The bound `|Z-1|<223 epsilon`, `Z=tV'/V`, fixes `Re Z>0`, inward traversal, and the outward tangent `-W'`. This audit found no central transfer to an unsupported sufficiency or tip-continuity claim in that step. It remains conditional on the classical support-slit theorem as stated by the candidate; this source audit is not a fresh complete validation of every external theorem.

The source also begins with genuine support maximizers, but its realization is of a different functional. Importing the source's tangent theorem cannot supply the candidate's continuation or target sign estimates, and no such import occurs in the candidate proof.

### Direct target signs and boundary conventions

The candidate's first-order inverse polynomial and its angular factor are

\[
 d(t)=t+\tfrac12t^3-\tfrac1{10}t^5,\quad
 P_0=-2d',\quad q_c(t)=d'(t)-d(t)/t=t^2-\tfrac25t^4.
\]

Its uniform estimate is

\[
 |Z-1-i\epsilon q_c|<2000\epsilon\sqrt\epsilon.
\]

Exact rational controls independently verify

\[
 q_c(1)=3/5,\quad q_c(7/4)=-441/640,
\]

and both sign margins exceed `epsilon/2` after the stated error. They also verify the radius gap, polynomial identities, and scalar error absorptions. Therefore the candidate's mechanism directly gives

\[
 \theta'=-2\Im Z/t,\quad
 \beta_{\rm out}=\arg Z,
\]

with opposite theta-derivative signs and opposite signed radial-angle values at the two regular actual-slit points. The signed radial angle tends to zero at infinity. That limit and the two signs preclude either monotone direction. Continuity gives an interior zero of the signed angle, so the magnitude is positive-zero-positive and is nonmonotone even on the compact subarc. This reasoning correctly covers orientation and magnitude; it does not use a tangent-waver inference.

At `epsilon=0`, these strict reversals disappear and the Koebe slit is radial. The candidate's nonmonotonicity is on a bounded part of the slit and is compatible with eventual monotonicity near infinity. Zemyan 2003 supplies no claim to the contrary.

## Reproducibility, falsifiable checks, and remaining gaps

`checks.py` uses exact `fractions.Fraction` arithmetic and `mpmath` directed interval arithmetic. Its interval controls use 65 decimal digits and exact decimal input brackets. The local ignored environment used `mpmath 1.4.1`; the script records the version. Run, for example:

```
python3 -m venv .cache/venv
.cache/venv/bin/python -m pip install mpmath
.cache/venv/bin/python checks.py
python3 verify_manifest.py
```

The controls pass. They certify the root bracket and uniqueness, source parameter enclosures, actual-tip inside-disk branch consistency, published tangent-sign samples, normalization consistency, exact rational angle identities and infinity-series cancellation, and candidate sign/tip/error scalar margins. **A numerical sample grid is not being used to establish global source-angle monotonicity:** (S5)-(S7) and `ytip<pi` do that. The reciprocal tip is explicitly outside the chosen branch; the source's very own tangent waver is the adversarial control against the false bridge to the target angles.

The authored manifest excludes copyrighted source PDF, extracted text, rendered pages, and the ignored environment. It seals source identity/coverage, source-first derivation, this report, computation script/results, verdict, and research log. Final input checks confirm the compared source/candidate files retain the recorded hashes; a later edited manuscript must be compared as a new input version.

The strongest verified source conclusion is an actual globally maximizing **evaluation** support slit with a tangent waver and globally monotone target angles. The strongest bounded priority conclusion is that **this paper's complete result and construction do not settle the two target questions negatively or anticipate the exact finite coefficient construction**.

Unclosed gaps are external to that bounded conclusion: Brown's full characterization is invoked by this paper and has not been independently re-proved here; the candidate's complete classical theorem chain is outside this one-source scope; no other source's contents or later work have been cleared by this audit; no literature-wide novelty claim follows. Source references identify Brown 1979 as the precise dependency for the evaluation extremizer, not as evidence of the candidate's construction. No outreach was prepared or initiated.

# Independent audit of family 332 and the real-L1 cut adaptation

Audit completed: 2026-10-06 22:15 PDT (2026-10-07 05:15 UTC).
Auditor: internal independent AI subagent `cut_audit`.

## Verdict and exact scope

I reconstructed every inequality in the family-332 proof, including its stopped martingale and geometric-to-Cesàro comparison, rather than accepting the proposed conclusion. I found no substantive mathematical gap in its real-ell1 metric Markov cotype argument. The same construction proves, for every positive countably additive measure space `(Omega, Sigma, mu)`,

`N_2(L1(mu; R)) <= sqrt(3024) = 12 sqrt(21)`.

The estimate actually holds for every stationary stochastic matrix, not only reversible matrices. No finiteness, sigma-finiteness, semifiniteness, localizability, completeness of the measure, or separability of L1 is needed in the finite-data proof. This is the strongest fully reconstructed result of this audit.

I also independently checked the full-extension deduction at the level of its established dependencies and supplied an explicit finite-to-bidual argument below. The remaining publication questions are priority, accurate attribution, review of the eventual exact manuscript/package, and successful package production; this report does not certify novelty or a final publication candidate. In particular, the upstream historical Hilbert-extension claim must be reconciled with the September 2026 work identified by the parent researcher. A correct mathematical implication does not establish that implication's priority.

## Sources actually inspected

The complete pinned TeX manuscript, bibliography, README, and text extracted from the supplied nine-page PDF were read. Source clone HEAD was independently checked as

`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

The clone was treated as read-only. Pinned project-copy SHA256 digests:

- `build/main.tex`: `656a6f35bf6543ecf0cf2dbc38a83a7a05427592123a5eb817be24250e2e6953`.
- `build/references.bib`: `7b7ccdb61e358ef3c2f5702c898a8ee550566f59ee9095e0530631a2b0b75776`.
- `l1-markov-cotype.pdf`: `d1977f73e5a70137791d0739b58b049fa30e3ad9caa4dfeb8353142db37ab60f`.

Primary external dependencies inspected on October 6, 2026 PDT:

- [Mendel–Naor, *Spectral calculus and Lipschitz extension for barycentric metric spaces*](https://web.math.princeton.edu/~naor/homepage%20files/cat0-extension.pdf), Definitions 1.1–1.3, Theorem 1.11, its full-extension discussion, and Corollary 1.13. Definition 1.2 exactly matches the upstream cotype inequality. Theorem 1.11 requires W2 barycentricity, and its output is finite extensions with loss bounded by a universal multiple of `Gamma M_2(X) N_2(Y)`. Ordinary Banach means have `Gamma=1`. The separate stronger 2-barycentric condition is unnecessary here. The upstream Hilbert-to-ell1 implication is covered because ell1 is the dual of c0.
- [Harmand–Werner–Werner, Chapter IV](https://page.mi.fu-berlin.de/werner99/mbuch/buch4.pdf), Example IV.1.1(a), printed page 158: L1 spaces are L-summands in their biduals. The lattice proof uses that L1 is a projection band in its bidual, itself an AL-space. It gives a linear contractive projection fixing the canonical L1 copy. It imposes no sigma-finite or separability restriction in the statement. This avoids incorrectly declaring arbitrary L1 spaces to be dual spaces.

No outside individual was contacted.

## 1. Exact claim and measure conventions

Let `mu: Sigma -> [0,infinity]` be a positive countably additive measure. Let `E=L1(mu; R)` be equivalence classes modulo equality almost everywhere of measurable real functions with finite integral of their absolute value. Extended-valued integrable representatives can be changed to zero on their measurable null sets of nonfinite values, giving finite real representatives. The measure space itself need not be complete.

For all integers `n,t>=1`, stochastic `A=(a_ij)`, stationary probability vector `pi` (`pi A=pi`), and `x_1,...,x_n in E`, the exact claimed inequality is the existence of `y_1,...,y_n in E` with

```
sum_i pi_i ||x_i-y_i||_1^2
  + t sum_ij pi_i a_ij ||y_i-y_j||_1^2
<= 3024 sum_ij pi_i [(1/t) sum_{s=1}^t A^s]_ij ||x_i-x_j||_1^2.
```

When A is reversible this is precisely metric Markov cotype two. The proof below establishes the stronger stationary claim. It does not cover finitely additive set functions, signed measures used without total variation, an arbitrary closed subspace of L1, or noncommutative L1.

## 2. Finite cuts: direct reconstruction in arbitrary L1

Choose finite real measurable representatives for the finite tuple, and define

```
v(omega) = min_i x_i(omega),
b_B(omega) = (min_{i in B} x_i(omega)
              - max_{i not in B} x_i(omega))_+
```

for every nonempty proper `B subset [n]`. Finite min, max, subtraction, and positive part preserve measurability. Pointwise,

```
|v| <= sum_i |x_i|,
0 <= b_B <= 2 sum_i |x_i|.
```

Thus v and every b_B belong to E. There is no uncountable supremum, selection of a measurable ordering, or Fubini argument. Even the union of the supports of these finitely many representatives is sigma-finite: it is the union over i and m of the finite-measure sets `{|x_i|>1/m}`. This observation is optional and is not an assumption on the original measure space.

Set `w_B=integral b_B dmu`, discard zero weights, and let `Bcal` be the remaining finite family. A discarded nonnegative integrable b_B vanishes almost everywhere. Since there are finitely many discarded cuts, one can remove a single measurable null exceptional set and obtain all subsequent pointwise identities simultaneously. Define

```
z_i(B) = 1_{i in B},
T(u) = v + sum_{B in Bcal} u_B b_B,
||u||_{1,w} = sum_B w_B |u_B|,
||u||_H^2 = sum_B w_B u_B^2.
```

Positive weights make H a genuine finite-dimensional Hilbert space. T is affine, defined on all of `R^Bcal`, and takes values in E. It need not preserve a preassigned subspace containing the x_i.

Fix omega and list the distinct values of the x_i as `alpha_1<...<alpha_m`. A cut has b_B(omega)>0 exactly when every value inside B exceeds every value outside B. Such a cut is necessarily one of the upper cuts

`B_r={i: x_i(omega)>=alpha_{r+1}}`, `1<=r<m`,

and its value is exactly `alpha_{r+1}-alpha_r`. Ties cause no additional cut: a cut splitting a tied level has b_B=0. Therefore

```
x_i = v + sum_B z_i(B) b_B                      a.e.,
|x_i-x_j| = sum_B |z_i(B)-z_j(B)| b_B           a.e.
```

The second identity follows because upper cuts are nested, so all nonzero signed terms in the first difference have the same sign at each omega. Integrating the finite nonnegative sum gives

```
T(z_i)=x_i,
||x_i-x_j||_1 = ||z_i-z_j||_{1,w} = ||z_i-z_j||_H^2.
```

For arbitrary u,u', the ordinary triangle inequality gives

`||T(u)-T(u')||_1 <= sum_B |u_B-u'_B| ||b_B||_1 = ||u-u'||_{1,w}`.

Changing representatives only changes the resulting functions on a finite union of measurable null sets; the resulting E elements and weights are unchanged. If Bcal is empty, the distance identity says all original E elements coincide. For n=1 this happens automatically. Choosing all y_i equal to the common point handles that case without defining a nontrivial H.

## 3. Cubic flatness and the quartic remainder

Put `phi(r)=3r^2-2r^3` on `[0,1]`, and apply it coordinatewise to get Phi on the cube Q. For either bit d, `|phi'(r)|=6r(1-r)<=6|r-d|`. With `e in {0,1}^Bcal`, `a=u-e`, `delta=u'-u`, integrating along the segment from u to u' gives

```
|phi(u'_B)-phi(u_B)| <= 6 |a_B| |delta_B| + 3 |delta_B|^2,
||Phi(u')-Phi(u)||_{1,w}
   <= 6 ||a||_H ||delta||_H + 3 ||delta||_H^2.
```

The second line is weighted Cauchy–Schwarz. The segment stays in Q; no derivative estimate outside `[0,1]` is required.

Write `A0=||a||_H^2`, `D0=||delta||_H^2`, and `I0=<a,delta>_H`. The exact remainder is

```
R = ||a+delta||_H^4 - ||a||_H^4 - 4 A0 I0
  = 2 A0 D0 + (2 I0 + D0)^2.
```

This identity was checked by expansion. It gives `A0 D0<=R/2`. Also

```
D0^2 = [(2 I0+D0)-2 I0]^2
     <= 2(2 I0+D0)^2 + 8 I0^2
     <= 2(2 I0+D0)^2 + 8 A0 D0
     <= 4R.
```

Consequently,

```
||Phi(u')-Phi(u)||_{1,w}^2
 <= 72 A0 D0 + 18 D0^2
 <= 36 R + 72 R = 108 R.
```

No factor depends on the number of cut coordinates or the total weight. The total weight enters only a boundedness estimate later. The proof would fail if e were not binary, because the needed derivative flatness at e is then unavailable; the application supplies a binary e.

## 4. Martingale telescoping with an initial random center

For a Q-valued H-martingale M_m and a binary F_0-measurable e, the vector

`4 ||M_m-e||_H^2 (M_m-e)`

is F_m-measurable and bounded. Hence its scalar product with the martingale increment has zero expectation. Applying the preceding flatness inequality and summing from m=0 to L-1 gives

```
E sum_{m=0}^{L-1} ||Phi(M_{m+1})-Phi(M_m)||_{1,w}^2
 <= 108 [E ||M_L-e||_H^4 - E ||M_0-e||_H^4].
```

Since `||M_m-e||_H^4 <= (sum_B w_B)^2`, bounded convergence is valid when M_m converges almost surely. Monotone convergence handles the nonnegative sum of increments. Thus the terminal energy is at most `108 E||M_infinity-e||_H^4`. Randomness of e causes no conditional-expectation problem because it is known at time zero; the proof never conditions on the terminal state. There is no unbounded optional-stopping invocation.

## 5. The killed chain and the exact two-cost identity

Take `p=1/(t+1)`, `q=t/(t+1)`, and

`h_i=p sum_{s>=0} q^s sum_j (A^s)_ij z_j`.

This converges absolutely in finite-dimensional H and belongs to Q. The resolvent identity is

`h_i=p z_i+q sum_j a_ij h_j`.

From an alive state i, stop into the absorbing dead state i with probability p, or move alive to j with probability q a_ij. Attach h_i to alive i and z_i to dead i. With a filtration recording the initial state and past transitions, the attached values M_m are a martingale by the displayed identity. Start from pi. A realization by an independent A-walk X_s and independent survival trials has S successful walk transitions before death, with `P(S=s)=p q^s`. The death transition itself is an additional recorded transition. This distinction matters: it is the death jump that supplies the approximation cost.

Almost surely,

`M_0=h_{X_0}`, `M_infinity=z_{X_S}`, `e=z_{X_0}`.

Thus binary reconstruction yields

`||M_infinity-e||_H^4=||x_{X_S}-x_{X_0}||_1^2`.

Let

```
B0 = sum_i pi_i ||z_i-Phi(h_i)||_{1,w}^2,
E0 = sum_ij pi_i a_ij ||Phi(h_i)-Phi(h_j)||_{1,w}^2.
```

At chain time m, alive has probability q^m independently of the underlying walk. Stationarity gives the alive marginal pi and live pair law pi_i a_ij. Therefore the expected squared Phi jump is exactly

`p q^m B0 + q^(m+1) E0`.

Summing all m gives `B0+(q/p)E0=B0+t E0`. The indexing and the factors p,q are correct. In particular, a one-based geometric law used without a corresponding indexing change would not give this identity.

For `y_i=T(Phi(h_i))`, contractivity of T gives

```
sum_i pi_i ||x_i-y_i||_1^2
 + t sum_ij pi_i a_ij ||y_i-y_j||_1^2
<= B0+t E0
<= 108 E ||x_{X_S}-x_{X_0}||_1^2.
```

Zero coordinates of pi cause no division by zero. The resolvent is still defined at every state; zero-mass states simply contribute nothing. If pi_i=0, stationarity implies no positive-mass state can enter i with positive probability, so there is no hidden influence from such states in the weighted energy. Reducibility, periodicity, and deterministic stationary transitions cause no difficulty. Reversibility is unused.

## 6. Geometric endpoint comparison and constants

Set `D(s)=E d(x_{X_s},x_{X_0})^2`, `W=(1/t)sum_{s=1}^t D(s)`. Triangle inequality, L2 Minkowski, and stationarity of the entire pair process give

`sqrt(D(r+s))<=sqrt(D(r))+sqrt(D(s))`.

Averaging `D(t)<=2D(r)+2D(t-r)` over r=1,...,t gives `D(t)<=4W`, since D(0)=0. If `s=jt+r`, `0<=r<t`, then

`D(s)<=2j^2 D(t)+2D(r)`.

For `J=floor(S/t)` and `R=S-tJ`,

```
E J^2 <= E S^2/t^2 = (2t^2+t)/t^2 <= 3,
P(R=r) = p q^r/(1-q^t) <= 2/t.
```

The second bound uses the integer Bernoulli inequality `(1+1/t)^t>=2`, hence `q^t<=1/2`. Therefore `E D(R)<=2W`, and

`E D(S)<=2*3*4W+2*2W=28W`.

The chain endpoint expectation equals E D(S) because S is independent of the walk. For t=1, R=0; all these bounds remain valid, with slack. No monotonicity of D(s), aperiodicity, spectral estimate, or reverse transition is assumed. Multiplying the two proven constants gives `108*28=3024=(12 sqrt(21))^2`, exactly as claimed.

## 7. Median interpretation and boundary exclusions

For each fixed i, draw three independent indices from the geometric endpoint distribution. At each omega, crossing an upper cut in the median is equivalent to at least two indices lying in that cut. Its probability is `3h_i(B)^2(1-h_i(B))+h_i(B)^3=phi(h_i(B))`. Hence y_i is the finite discrete expectation of the pointwise median of the three corresponding x_j. This is also meaningful in arbitrary L1: median is a finite measurable expression, and its absolute value is bounded by the sum of the three absolute values. No vector-valued integration over a nonseparable continuum is present; there are at most n^3 possible median functions.

This construction does not show that y_i belongs to the linear span of the data or to every subspace containing them. Subspace conclusions cannot be added. It also cannot be transferred to noncommutative L1 by treating operator min/max as pointwise scalar min/max. Complex L1 is a separate possible corollary using realification and a verified distortion estimate; it is not part of this real proof. Nothing here implies a p=infinity source consequence.

## 8. Independent full-extension reconstruction

The ordinary mean barycenter satisfies the required quantitative estimate directly: for every finite coupling of probability measures alpha,beta on E,

`||bar(alpha)-bar(beta)|| <= sum_{uv} coupling(u,v)||u-v|| <= [sum_{uv} coupling(u,v)||u-v||^2]^(1/2)`.

Taking the infimum over couplings gives Gamma=1. Combined with the audited cotype construction, the established finite extension theorem provides a common bound `K=C_MN M_2(X) sqrt(3024) Lip(f)` on every finite extension.

Here is an explicit compactness argument, valid for nonseparable X, E, and arbitrary S. If S is empty, use the zero map. If Lip(f)=0, use its constant value. Otherwise choose `s0 in S`, index by the finite subsets A of X containing s0, and for each A choose an extension g_A on A agreeing with f on A intersect S and having bound K. Define g_A(x)=f(s0) off A. For each fixed x, all these values are bounded by

`||g_A(x)-f(s0)|| <= K d(x,s0)`.

Choose an ultrafilter U containing each cone `{A: D subset A}` for finite D subset X. The cones have the finite intersection property; the ultrafilter lemma supplies U. An arbitrary free ultrafilter, without the cone condition, would be insufficient. Define an element G(x) of E** by

`G(x)(ell)=lim_U ell(g_A(x))`, `ell in E*`.

The real ultralimits exist by pointwise boundedness. They are linear and bounded in ell. On the cone containing x,y, the Lipschitz inequality holds; passing to the limit and then taking the supremum over unit ell gives `||G(x)-G(y)||<=K d(x,y)`. On the cone containing s, g_A(s)=f(s), so `G(s)=j_E f(s)` for every s in S. The L-embedded projection `P:E**->j_E(E)` is contractive and fixes the canonical copy. Therefore `j_E^{-1} P G` is the required full E-valued extension, with the same K.

This proof uses the established projection theorem explicitly and does not need E to be a dual space, nor a global compatible choice of measurable representatives for f(S). It uses the usual choice principles underlying the ultrafilter lemma. There is no countability assumption on S or X and no inference that finite extension alone suffices without an appropriate compactness target and retraction.

## 9. Falsification checks and limitations of computational evidence

The following finite checks were executed under Python 3.14.6 with exact rational arithmetic, not floating point:

- For every pair u,v in `{0,1/10,...,1}` and bit e, the one-coordinate cubic/quartic inequality held: 242 cases. The largest observed quotient of squared cubic increment by nonzero R was `196/25`; this does not optimize the universal constant.
- With deterministic seed 20261006, 500 random tuples having 1–6 points and 1–9 original coordinates, rational signed coordinate values and frequent ties, satisfied every cut reconstruction identity and pair-distance identity exactly. All nonempty proper cuts were enumerated, including zero weights.

These checks are attempts to catch algebra/sign/tie errors. The rigorous proof above, not finite testing, establishes arbitrary dimension and arbitrary measures. The checks did not test a final manuscript, bibliographic priority, infinite-dimensional projection code, or formal proof compilation.

The proof was attacked specifically at: binary versus nonbinary center; random-center conditioning; death-jump indexing; stationary versus merely arbitrary initial law; modulo-geometric remainder law; t=1; n=1; all points equal; zero weights; zero pi; tied values; signed values; incomplete and nonsigma-finite measures; nonseparable targets; representative dependence; possible improper inheritance by subspaces. Every required case is covered by an explicit argument above. An arbitrary nonstationary initial law is not claimed and would invalidate the exact B0+tE0 identity.

## 10. Build and formalization evidence

A first attempted local rebuild was interrupted by temporary disk exhaustion before any source copy was made. After sufficient space was available, the unmodified TeX and bibliography were copied solely into project-local `agent_notes/cut_audit_build`, and the actual command

`/opt/homebrew/bin/tectonic --keep-logs main.tex`

was run there. Environment: Tectonic 0.16.9, LaTeX2e 2021-11-15 patch level 1, L3 2022-02-24. It failed at `glyphtounicode` line 7 because `\pdfglyphtounicode` is undefined under this engine. No pages or replacement PDF were produced. Log SHA256:

`6222c51730c9cd0a586c3ed166b171149f4c5fc115b5ed1cd3460f9adcd384f0`.

This is an engine compatibility failure, not a proof failure. No TeX engine was installed and no source-clone file was modified. The original PDF was independently extracted with pdftotext; its theorem, proof equations, constants, martingale indexing, and nine-page text matched the inspected TeX. This audit does not claim successful source-PDF reproduction or visual PDF-layout approval.

`lean/docs/332.md` is absent at the pinned clone. A recursive search over lean/docs, lean/OAI, and lean/ComparatorChallenges for metric Markov cotype and the manuscript mechanism found no corresponding formalization. The similarly named Cotype modules concern K-convexity/Rademacher cotype; MarkovType concerns a separate superreflexivity target. The comparator files inspected contain `sorry`. I did not run a Lean build, and no result of this project is being represented as formally verified.

## 11. Exact remaining work

There is no identified mathematical gap in the real-L1 cotype adaptation or in the stated full-extension deduction from the established finite extension and L-embeddedness theorems. The final author must still verify the exact eventual manuscript and package, preserve attribution to the upstream mechanism and established reductions, resolve priority against all relevant September/October sources, and produce a successfully compiled downloadable final PDF. This audit supplies mathematical evidence, not a claim of conventional human peer review or publication readiness.

## Appendix: exact finite-check reproduction

The following is the executed Python check. It uses only the standard library and writes no artifacts:

```python
import random
from fractions import Fraction as F
rng = random.Random(20261006)
phi = lambda r: 3*r*r-2*r*r*r
max_flat=F(0)
checked=0
for bit in (F(0),F(1)):
    for ui in range(11):
        for vi in range(11):
            u=F(ui,10)
            v=F(vi,10)
            a=u-bit
            d=v-u
            R=(v-bit)**4-a**4-4*a**3*d
            lhs=(phi(v)-phi(u))**2
            assert lhs<=108*R, (u,v,bit,lhs,R)
            if R:
                max_flat=max(max_flat,lhs/R)
            checked+=1
recon_checked=0
for _ in range(500):
    n=rng.randrange(1,7)
    k=rng.randrange(1,10)
    x=[[F(rng.randrange(-10,11),rng.randrange(1,6))
        for _ in range(k)] for _ in range(n)]
    v=[min(x[i][a] for i in range(n)) for a in range(k)]
    Bs=[B for B in range(1,2**n-1)]
    b={B:[max(F(0),
        min(x[i][a] for i in range(n) if B>>i&1)
        -max(x[i][a] for i in range(n) if not B>>i&1))
        for a in range(k)] for B in Bs}
    w={B:sum(b[B]) for B in Bs}
    for i in range(n):
        for a in range(k):
            assert v[a]+sum(b[B][a] for B in Bs if B>>i&1)==x[i][a]
        for j in range(n):
            assert sum(abs(x[i][a]-x[j][a]) for a in range(k))==sum(
                w[B] for B in Bs if (B>>i&1)!=(B>>j&1))
    recon_checked+=1
print({'exact_flat_grid_cases':checked,
       'max_ratio_on_grid':str(max_flat),
       'exact_cut_tuples':recon_checked,
       'all_passed':True})
```

Observed output:

```text
{'exact_flat_grid_cases': 242, 'max_ratio_on_grid': '196/25',
 'exact_cut_tuples': 500, 'all_passed': True}
```

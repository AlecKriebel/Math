# Independent finite-to-infinite bridge for hypersingular planar Riesz energy

Prepared independently on 2026-10-06 (America/Los_Angeles) for the dedicated
`openai_followon_riesz_surface_constants` effort. This file makes no
unconditional claim that the upstream universal-optimality theorem is valid.
It isolates the exact dependency and proves the new reduction conditional on
that dependency. No other agent's proof was consulted in preparing this file.

## 1. Exact dependency and conventions

Fix a real exponent `s > 2`. Let `b = sqrt(3)/2` and

\[
\Lambda=b^{-1/2}\{m(1,0)+n(1/2,b):m,n\in\mathbb Z\}.
\]

Thus `covol(Λ)=1`. Put

\[
Z_s=\zeta_\Lambda(s)=\sum_{v\in\Lambda\setminus\{0\}}|v|^{-s}.
\]

This is a per-point **ordered-pair** lattice energy. It is not to be divided
by two. If the finite energy were defined using unordered pairs, both the
finite constant and the per-point infinite energy would instead have the
corresponding factor `1/2`.

For a locally finite set `C` in the plane, let `C_R=C∩B_R`, where `B_R` is the
closed disk centered at the origin, and `n_C(R)=#C_R`. The exact infinite
functional is

\[
\mathcal H_s(C)=\liminf_{R\to\infty}\frac1{n_C(R)}
  \sum_{\substack{x,y\in C_R\\x\ne y}}|x-y|^{-s}.
\]

Centered density one means `n_C(R)/(πR²)→1`. The relevant upstream
dependency, denoted **U_s**, is

> Every locally finite set `C` of centered density one satisfies
> `H_s(C) ≥ Z_s`.

Only the **square-periodic special case** of `U_s` is required below; no
assumption about nonperiodic competitors, uniqueness, or microscopic
crystallization is needed. For each fixed `s`, the potential
`g(t)=t^(−s/2)` is smooth and completely monotone, since

\[
(-1)^r g^{(r)}(t)=(s/2)_r t^{-s/2-r}>0 \qquad (t>0,r\ge0).
\]

The read-only upstream statement used to identify `U_s` is Theorem
`thm:universal` and equation `eq:energy-definition` in
`preprints/Universal-optimality-of-the-triangular-lattice-September-23-2026/build/sections/01-uniform-gaussian-theorem.tex`
at source-clone commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. That file's SHA-256 is
`5f95e8c993801c661340c55dd3137c83750c028f0e2d734a5d8f5a4c38830869`.
Reading its theorem is not verification of its proof. Auditing that proof is
a separate pivotal dependency task.

Let `K=[0,1]²` and define

\[
\mathcal E_s(K,N)=\inf_{\substack{x_1,\ldots,x_N\in K\\x_i\ne x_j}}
  \sum_{i\ne j}|x_i-x_j|^{-s},\qquad
a_N=\frac{\mathcal E_s(K,N)}{N^{1+s/2}}.
\]

Closed-square boundary points are allowed. The gap construction below makes
distinct boundary points in neighboring copies remain distinct. Finite
minimizers exist: extend the energy to `K^N` by assigning `+∞` to collisions;
it is lower semicontinuous, `K^N` is compact, and a distinct finite competitor
has finite energy. The argument itself works for every finite competitor,
so existence is not a pivotal assumption.

## 2. Periodic configurations: density and the disk energy limit

**Lemma 1.** Let `L>0`, and let `F={f_1,…,f_q}` be a finite set of distinct
points in the half-open square `[0,L)²`. Put

\[
C=F+L\mathbb Z^2.
\]

Then `C` is locally finite, has centered density `q/L²`, and, for `s>2`,

\[
\lim_{R\to\infty}\frac1{n_C(R)}
  \sum_{\substack{x,y\in C_R\\x\ne y}}|x-y|^{-s}
=\frac1q\sum_{i=1}^q h_i,
\tag{1}
\]

where

\[
h_i=\sum_{\substack{1\le j\le q, k\in\mathbb Z^2\\(j,k)\ne(i,0)}}
       |f_i-f_j-Lk|^{-s}<\infty.
\tag{2}
\]

**Proof.** Membership in the half-open square makes the representations
unique. A bounded disk meets only finitely many square translates, hence
local finiteness. For each fixed `i`, the points `f_i+Lk` are centers of a
tiling by squares of side `L`. Write `d=L sqrt(2)/2` and
`n_i(R)=#{k:f_i+Lk∈B_R}`. The union of the square cells whose centers lie in
`B_R` contains `B_(R−d)` and is contained in `B_(R+d)`. Consequently, for
`R>d`,

\[
\frac{\pi(R-d)^2}{L^2}\le n_i(R)
       \le\frac{\pi(R+d)^2}{L^2}.
\tag{3}
\]

In particular `n_i(R)=πR²/L²+O(R/L+1)` for fixed `L`, and
`n_C(R)=Σ_i n_i(R)`. Thus `n_C(R)/(πR²)→q/L²`, and
`n_i(R)/n_C(R)→1/q`.

The terms in (2) with `||k||_∞≤1` form a finite sum with no zero
denominators. For `m=||k||_∞≥2`, coordinates of `f_i−f_j` have absolute
value `<L`, so

\[
|f_i-f_j-Lk|\ge\|f_i-f_j-Lk\|_\infty
       \ge L(m-1)\ge Lm/2.
\]

There are exactly `8m` integer vectors with `||k||_∞=m`. The corresponding
tail is bounded by

\[
q(2/L)^s\sum_{m=2}^\infty8m^{1-s}<\infty.
\tag{4}
\]

This proves every `h_i` is finite. No limit or interchange is needed to
group these nonnegative sums; Tonelli's theorem applies.

Let `S_R` denote the ordered energy in the numerator of (1). Completing
every outgoing row to the whole infinite configuration gives

\[
S_R\le\sum_i n_i(R)h_i.
\tag{5}
\]

For a fixed cutoff `T>0`, let `h_i^(T)` be the sub-sum in (2) restricted to
displacements of length at most `T`. Every outgoing interaction of that
length from a point of `C∩B_(R−T)` stays inside `B_R`. Therefore, for `R>T`,

\[
S_R\ge\sum_i n_i(R-T)h_i^{(T)}.
\tag{6}
\]

Dividing (5) and (6) by `n_C(R)` and first sending `R→∞` yields

\[
\frac1q\sum_i h_i^{(T)}\le
\liminf_{R\to\infty}\frac{S_R}{n_C(R)}\le
\limsup_{R\to\infty}\frac{S_R}{n_C(R)}\le
\frac1q\sum_i h_i.
\]

Now send `T→∞`. Monotone convergence gives `h_i^(T)↑h_i`; there are only
finitely many motif indices. This proves (1). The cutoff is removed only
**after** the disk-radius limit. In particular the prescribed liminf is an
ordinary finite limit on these periodic competitors. ∎

If `λ>0`, the same formula immediately gives

\[
\operatorname{dens}(\lambda C)=\lambda^{-2}q/L^2,
\qquad \mathcal H_s(\lambda C)=\lambda^{-s}\mathcal H_s(C).
\tag{7}
\]

Alternatively these identities follow by substituting `R/λ` for the disk
radius in the definitions. This scaling identity changes a per-point
energy by `λ^(−s)`; it does not introduce a further density factor.

## 3. Gap periodization and the lower bound

**Proposition 2 (explicit bridge).** Assuming `U_s`, for every `N≥1` and
every `ε>0`,

\[
a_N\ge(1+\varepsilon)^{-s}Z_s
       -8\varepsilon^{-s}\zeta_{\mathbb R}(s-1)N^{1-s/2}.
\tag{8}
\]

Here `ζ_R(u)=Σ_(m≥1)m^(−u)` denotes the ordinary Riemann zeta function;
it is distinguished from the lattice sum.

**Proof.** Take any distinct `N`-point configuration `X={x_i}` in `K`.
Set

\[
y_i=\sqrt N x_i,\quad F_N=\{y_i\},\quad
L_N=(1+\varepsilon)\sqrt N,\quad
C_{N,\varepsilon}=F_N+L_N\mathbb Z^2.
\]

Because `0≤(y_i)_a≤√N<L_N`, `F_N` is a valid motif in a half-open
fundamental square. It retains all original distinct points, including any
on the closed boundary. The density is

\[
N/L_N^2=(1+\varepsilon)^{-2}.
\tag{9}
\]

The within-motif contribution per point is exactly

\[
\frac1N\sum_{i\ne j}|y_i-y_j|^{-s}
  =N^{-1-s/2}\sum_{i\ne j}|x_i-x_j|^{-s}.
\tag{10}
\]

Let `I_(N,ε)` denote the contribution per point from all nonzero cell
translations, including `i=j` interactions with other copies:

\[
I_{N,\varepsilon}=\frac1N\sum_{i,j=1}^N
  \sum_{k\in\mathbb Z^2\setminus\{0\}}
       |y_i-y_j-L_Nk|^{-s}.
\tag{11}
\]

For `m=||k||_∞≥1`, choose a coordinate with `|k_a|=m`. Since
`|(y_i−y_j)_a|≤√N`,

\[
|y_i-y_j-L_Nk|\ge\sqrt N\bigl((1+\varepsilon)m-1\bigr)
                    \ge\varepsilon\sqrt N\,m.
\tag{12}
\]

The final inequality uses
`(1+ε)m−1−εm=m−1≥0`. There are `8m` translations in the `m`th sup-norm
shell and `N²` choices of `(i,j)`. Hence

\[
0\le I_{N,\varepsilon}
\le \frac{N^2}{N}(\varepsilon\sqrt N)^{-s}
      \sum_{m=1}^\infty8m\,m^{-s}
=8\varepsilon^{-s}\zeta_{\mathbb R}(s-1)N^{1-s/2}.
\tag{13}
\]

This bound is uniform over the original point configurations and requires
neither a separation bound nor an occupancy estimate within the motif.
Convergence of the shell sum uses precisely `s>2`.

By Lemma 1 the disk energy is the row average, so

\[
\mathcal H_s(C_{N,\varepsilon})
=N^{-1-s/2}\sum_{i\ne j}|x_i-x_j|^{-s}+I_{N,\varepsilon}.
\tag{14}
\]

Compress lengths by `λ=(1+ε)^(−1)` and put
`D_(N,ε)=λ C_(N,ε)`. By (7) and (9), `D_(N,ε)` has centered density one
and

\[
\mathcal H_s(D_{N,\varepsilon})
=(1+\varepsilon)^s\left[
 N^{-1-s/2}\sum_{i\ne j}|x_i-x_j|^{-s}+I_{N,\varepsilon}\right].
\tag{15}
\]

Apply `U_s` to this one fixed infinite configuration to obtain

\[
N^{-1-s/2}\sum_{i\ne j}|x_i-x_j|^{-s}
\ge(1+\varepsilon)^{-s}Z_s-I_{N,\varepsilon}.
\]

Use (13) and then take the infimum over `X`. This proves (8). ∎

For each fixed `ε>0`, `N^(1−s/2)→0`. Thus (8) gives

\[
\liminf_{N\to\infty}a_N\ge(1+\varepsilon)^{-s}Z_s.
\]

Now send `ε↓0` to obtain

\[
\liminf_{N\to\infty}a_N\ge Z_s.
\tag{16}
\]

The limit order is:

1. For each fixed `N,ε`, take the infinite disk radius `R→∞` using Lemma 1.
2. For each fixed `ε`, take `N→∞`.
3. Only then take `ε↓0`.

There is no illicit interchange of a varying family of disk-radius limits.
The case `ε=0` is not used: it would allow collisions between copies of
boundary points and invalidate the uniform nearest-box estimate.

## 4. Lattice convergence and a finite exact-N upper bound

**Lemma 3.** The lattice sum `Z_s` is finite for every `s>2`.

**Proof.** Write the lattice as `B Z²`, where `B` is the invertible matrix
with the displayed basis columns. There is `c>0` such that
`|Bk|≥c||k||_∞` for every integer vector `k`. Therefore

\[
Z_s\le c^{-s}\sum_{m=1}^\infty8m^{1-s}<\infty.
\]

This also gives a summable dominator for any reindexing of the nonnegative
lattice sum. ∎

**Proposition 4 (upper bound, independent of `U_s`).** Let `P` be a
bounded fundamental parallelogram for `Λ` and let `D>0` satisfy
`P⊂[−D,D]²`. Then for every `N≥1`,

\[
a_N\le Z_s\left(1+\frac{2D}{\sqrt N}\right)^s,
\qquad\text{and hence}\qquad
\limsup_{N\to\infty}a_N\le Z_s.
\tag{17}
\]

**Proof.** The translates `v+P`, `v∈Λ`, cover the plane and have pairwise
disjoint interiors, each of area one. If `t≥2D`, every point of
`[D,t−D]²` belongs, apart from the irrelevant cell-boundary ambiguity, to a
cell whose lattice representative lies in `[0,t]²`: indeed
`x=v+p` with `p∈P` gives coordinatewise `0≤v≤t`. It follows by area that

\[
\#(\Lambda\cap[0,t]^2)\ge(t-2D)^2.
\tag{18}
\]

Take `t_N=√N+2D`; there are at least `N` lattice points in `[0,t_N]²`.
Choose any subset `Y_N` of exactly `N` of them and scale it by `t_N^(−1)`
into `K`. At every selected site, the ordered row sum over the other
selected sites is at most the full lattice row sum `Z_s`. Therefore

\[
\mathcal E_s(K,N)\le t_N^s\sum_{\substack{x,y\in Y_N\\x\ne y}}|x-y|^{-s}
                  \le t_N^s N Z_s.
\]

Division by `N^(1+s/2)` proves (17). No unproved assertion about boundary
selection or the exact count in a lattice crop is needed. ∎

Combining (16) and (17) proves the exact conditional core reduction:

> **Theorem.** If `U_s` holds, then for the ordered-pair Riesz energy on the
> closed unit square,
> \[
> \lim_{N\to\infty}\frac{\mathcal E_s([0,1]^2,N)}{N^{1+s/2}}
>       =\zeta_\Lambda(s).
> \]

Thus any established universality theorem that identifies `C_(s,2)` with
this square limit yields `C_(s,2)=ζ_Λ(s)`. Passing to smooth embedded
surfaces, the precise manifold assumptions, area normalization, boundary
convention, and chordal/ambient distance are an **external universality
dependency**, not consequences proved in this file. In particular this
file does not silently substitute geodesic distance for ambient Euclidean
distance.

## 5. Independent thermodynamic variational formulation

There is also a fully unconditional reduction to square-periodic energy.
Let

\[
P_s=\inf\{\mathcal H_s(C):C=F+L\mathbb Z^2,
                  \ |F|/L^2=1\}.
\tag{20}
\]

Motifs in this infimum are finite and distinct modulo their period lattice.
It suffices to represent them in a half-open period square. The infimum is
finite and nonnegative, since the square lattice is one admissible
competitor. By the definition of `P_s`, the gap-periodization proof applies
with `P_s` replacing `Z_s`, without invoking `U_s`. In particular

\[
\liminf_{N\to\infty}a_N\ge P_s.
\tag{21}
\]

For the converse, fix any admissible `C=F+L Z²` of density one, with
`q=|F|=L²` and finite rows `h_i` from Lemma 1. Define
`n_i^square(t)=#{k:f_i+Lk∈[0,t]²}`. The square tiling centered at these
grid points has coordinate displacement at most `L/2`; its area bounds
give

\[
\frac{(t-L)^2}{L^2}\le n_i^{\mathrm{square}}(t)
                \le\frac{(t+L)^2}{L^2}\qquad(t\ge L),
\]

and hence `n_i^square(t)=t²/L²+O(t/L+1)`. The constants are fixed for this
one competitor. Put `t_N=√N+L`. Since

\[
\#(C\cap[0,t_N]^2)\ge\frac{q}{L^2}(t_N-L)^2=N,
\]

choose any `N`-point subset `Y_N` of that crop. Positive row sums and the
fixed finite motif imply

\[
\sum_{\substack{x,y\in Y_N\\x\ne y}}|x-y|^{-s}
 \le\sum_i n_i^{\mathrm{square}}(t_N)h_i
 =\frac{t_N^2}{L^2}\sum_i h_i+O(t_N)
 =t_N^2\mathcal H_s(C)+O(t_N).
\]

Scale the crop by `1/t_N` into the unit square. Since `t_N/√N→1`,

\[
\limsup_{N\to\infty}a_N\le\mathcal H_s(C).
\]

Taking the infimum over the fixed competitors proves

\[
\lim_{N\to\infty}a_N=P_s\le Z_s.
\tag{22}
\]

Thus existence of this square thermodynamic limit has an elementary proof
that does not calculate its value. The last inequality in (22) follows
from the separate lattice-crop upper bound, so it does not require the
triangular lattice to possess an axis-aligned square period. The triangular
lattice itself generally cannot be treated as an admissible square-periodic
motif.

This alternative route is **blocked as a resolution of the core value** at
the precise unsupported assertion `P_s=Z_s`. That assertion is equivalent
to the required square-periodic energy lower bound, rather than an easier
substitute for it. The route gives no independent reason to assert
triangular optimality.

One can also uniformly randomly translate a fixed periodic competitor by a
point of its fundamental square. Tonelli and tiling yield expected number
of points `q|Q|/L²` and expected full outgoing energy
`|Q|Σ_i h_i/L²` in any measurable bounded window `Q`. At density one these
are `|Q|` and `|Q|H_s(C)`. This identifies the same periodic energy with a
stationary per-area functional, but does not close the gap `P_s=Z_s` and
does not introduce new assumptions into the deterministic argument.

## 6. Adversarial checks and strongest verified result

- **Orientation of density rescaling:** A density `(1+ε)^(−2)` configuration
  is compressed, not expanded, to reach density one. Lengths change by
  `(1+ε)^(−1)` and energy increases by `(1+ε)^s`. Reversing this direction
  would give an incorrect constant.
- **Pair convention:** The within-cell sum and the infinite row sums both
  count ordered pairs. Cross-cell sums include `i=j` when the cell
  translation is nonzero. The chosen denominator is the number of points,
  not the area and not twice the number of points.
- **Closed-square endpoints:** The strict gap `ε√N` prevents points on
  opposite square boundaries from coinciding after periodization.
- **No uniform local separation:** Finite configurations can have arbitrarily
  close pairs. Their finite within-cell energies can be large, but every
  inter-cell denominator is still controlled by (12); Lemma 1 is used for
  one fixed finite motif, not uniformly over varying motifs.
- **No shape mismatch:** The infinite theorem uses centered disks; (3),
  (5), and (6) prove the exact disk density and disk energy limit of each
  square-periodic competitor.
- **Long tail:** The exponent in the shell sum is `1−s`. The tail converges
  exactly for `s>2`. Nothing here extends the new constant assertion to
  `s≤2`; at `s=2` the shell comparison diverges and the desired power-law
  normalization is not applicable.
- **Order of limits:** The proof removes a bounded interaction cutoff after
  the disk limit, and removes the geometric gap after `N→∞`. No Fatou
  exchange for singular kernels or arbitrary nonperiodic competitors is
  used in the reduction itself.
- **Upper bound without exact crop count:** Selecting any exact-N subset
  of a slightly oversized crop lowers the number of positive interactions.
  Equation (18), rather than an unjustified choice of radius with precisely
  `N` lattice points, provides the needed count.
- **Quantifier scope:** Each fixed real `s>2` uses its own finite constants;
  no uniform estimate as `s↓2` is asserted.
- **Central obstruction:** This bridge does not prove `U_s`. It transfers
  no additional conjectural difficulty beyond the explicitly stated
  universal-optimality input. If that upstream input has a material gap,
  the unconditional equality `C_(s,2)=ζ_Λ(s)` remains unresolved by this
  file.

**Strongest verified result in this file:** the conditional theorem and
explicit bounds (8), (17), proved by the elementary deterministic
periodization and lattice-crop arguments above; unconditionally, the
thermodynamic identity (22) and lattice upper bound (17). Mathematical
resolution of the bridge itself is estimated at 100%; resolution of the
complete project and publication package depends on other tasks and is not
estimated here.

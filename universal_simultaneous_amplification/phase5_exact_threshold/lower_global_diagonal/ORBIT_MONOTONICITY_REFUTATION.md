# The Bd-started dB orbit is not average-monotone, even by parity

Date: 2026-08-08 (America/Los_Angeles)

## Status

**FALSIFIED.**  Two natural upgrades of the exact first-orbit theorem are
false, already for a positive three-type kernel induced by a symmetric
rational weight matrix.  If

\[
 y_0=q,\qquad y_{k+1}={2Ry_k\over1+2Ry_k},
\]

where `q` is the endpoint Bd extinction vector at fitness two, then neither

\[
 E_p y_{k+1}\leq E_p y_k                                      \tag{1}
\]

nor the parity-subsequence strengthening

\[
 E_p y_{k+2}\leq E_p y_k                                      \tag{2}
\]

holds for every `k`.  The exact member below satisfies

\[
 E_p(y_{10}-y_9)>1.437\,10^{-7},\qquad
 E_p(y_{15}-y_{13})>4\,10^{-8}.                               \tag{3}
\]

Thus the proved inequality `E_p y_1 <= E_p y_0` cannot be iterated either
one step at a time or separately on the even and odd subsequences.  This
does **not** refute the endpoint conjecture `beta+sigma <= 1`: it refutes
only these proposed orbit Lyapunov functions.

## Exact rational kernel

Take

\[
 p=(0.01310931,0.48313850,0.50375219)
\]

and

\[
 W=\begin{pmatrix}
 0.354565456&1.20258024\,10^6&8.47598231\,10^{-7}\\
 1.20258024\,10^6&2.31795454\,10^{-5}&0.0173375395\\
 8.47598231\,10^{-7}&0.0173375395&1
 \end{pmatrix}.                                                \tag{4}
\]

Every displayed decimal is interpreted as an exact rational number.  Put

\[
 \delta_i=\sum_jp_jW_{ij},\qquad
 P_{ij}={p_jW_{ij}\over\delta_i},\qquad
 R=D_p^{-1}P^TD_p,qquad t=R\mathbf1.                           \tag{5}
\]

The matrix `W` is positive and symmetric, so this lies inside the
undirected-realizable adjoint-kernel sector.

## Exact enclosure

The replay encloses the subunit Bd extinction fixed point in the rational
box centered at

```text
(0.96948239826535802050938820707621778646742193737385736227345792180589513635579072,
 0.4199411432700926607783210061254230001938538469625538224507489769296075637032733,
 0.49070699498837739796609529383495858341569927656915196311175990432278933108462736)
```

with radius vector

```text
10^-60 (2,16,3).
```

For the monotone Bd extinction map

\[
 \mathcal T_B(x)_i={t_i\over t_i+2(1-(Px)_i)},                  \tag{6}
\]

exact `Fraction` arithmetic verifies

\[
 \mathcal T_B(L)\geq L,\qquad \mathcal T_B(U)\leq U.           \tag{7}
\]

The positive-kernel branching fixed-point uniqueness theorem therefore
places `q` in `[L,U]`.  The replay then propagates this box through fifteen
applications of the coordinatewise increasing dB survival map.  Every
image is rounded outward to the grid `10^-45 Z`, so numerator and
denominator sizes stay bounded without introducing any floating-point
assumption.  The resulting exact separations are

\[
\begin{aligned}
 \inf E_p y_{10}-\sup E_p y_9
 &= {14370424974932774889004778944246354765336534817
      \over10^{53}}>1.437\,10^{-7},\\
 \inf E_p y_{15}-\sup E_p y_{13}
 &= {2008353076892083891312230499245434994662937501
      \over5\,10^{52}}>4\,10^{-8}.                             \tag{8}
\end{aligned}
\]

These interval inequalities prove (3), hence refute (1) and (2).

## Replay

From the repository root run

```bash
.venv/bin/python \
  universal_simultaneous_amplification/phase5_exact_threshold/\
lower_global_diagonal/verify_orbit_monotonicity_refutation.py
```

The replay is deterministic and uses only Python integer and exact rational
arithmetic.

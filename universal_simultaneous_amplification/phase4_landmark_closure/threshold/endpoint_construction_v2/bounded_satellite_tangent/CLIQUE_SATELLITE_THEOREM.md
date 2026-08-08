# Dilute clique satellites: exact endpoint classification

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## Result

Replace each strong `K_2` satellite in the dilute pair--pendant construction
by a clique `K_s`, `s>=2`.  Give every internal satellite vertex weighted
degree `C/sigma` and connect every satellite vertex weakly and uniformly to
the large clique core.  Let the satellite count be dilute and let the hub
pendant count divided by the satellite count tend to `lambda`.

At fixed fitness `r>1`, the normalized first-order satellite corrections are

\[
 b_s(r,\sigma)
 ={s(\sigma-1)\over1+\sigma(r^s-1)},                    \tag{1}
\]

\[
 d_s(r,\sigma)
 ={s\{sr-r^s-(s-1)\sigma\}\over
        (s-1)\sigma+sr(r^{s-1}-1)}.                     \tag{2}
\]

After adding the pendant correction, the two coefficients are

\[
 b_s+{\lambda\over r-1},\qquad d_s-\lambda.             \tag{3}
\]

Thus a positive `lambda` can make both coefficients positive only if

\[
                  d_s+(r-1)b_s>0.                       \tag{4}
\]

At `r=3/2`, condition (4) holds for some `sigma>0` exactly when `s=2`.
Consequently `K_2` is the unique clique satellite capable of crossing the
three-halves endpoint in this dilute clique-satellite class.

This is a class theorem, not a universal bounded-gadget obstruction.

## Derivation from the update rules

An isolated regular `K_s` has Bd singleton fixation probabilities

\[
 a_B(r)={r^{s-1}(r-1)\over r^s-1},\qquad
 a_B(1/r)={r-1\over r^s-1}.                             \tag{5}
\]

For dB, if there are `j` mutants, the exact down/up ratio is

\[
 \gamma_j={s-1+(r-1)j\over
                 r\{s-1+(r-1)(j-1)\}}.                 \tag{6}
\]

The product telescopes.  Summing the product-odds formula gives

\[
 a_D(r)={(s-1)(r-1)r^{s-2}\over
                 s(r^{s-1}-1)}.                         \tag{7}
\]

Resolve one rare cross introduction and then let the invaded module absorb.
The successful mutant-satellite/resident-core gate odds are

\[
 Z_B=\sigma(r^s-1),\qquad
 Z_D={sr(r^{s-1}-1)\over(s-1)\sigma}.                  \tag{8}
\]

Uniform singleton initialization contributes

\[
 s\left\{{a_U(r)Z_U\over p(1+Z_U)}-1\right\},
 \qquad p=1-1/r.                                       \tag{9}
\]

Substitution of (5), (7), and (8) gives (1)--(2).  This calculation uses the
complete rare-migration trace: after the gate succeeds, the large mutant
core converts every remaining dilute satellite with probability tending to
one.  It is not merely an establishment approximation.

## Endpoint sign

At `r=3/2`, exact simplification gives for `s=2`

\[
 d_2+\tfrac12b_2
 ={-3\sigma(4\sigma-1)\over
       (2\sigma+3)(5\sigma+4)},                         \tag{10}
\]

which is positive precisely for `0<sigma<1/4`.  For `s=3` and `s=4`, the
same quantity has respectively the signs of

\[
 -(80\sigma^2-53\sigma+36),\qquad
 -(304\sigma^2-183\sigma+176).                         \tag{11}
\]

Both quadratics are strictly positive: their leading coefficients and
values at zero are positive, and their discriminants are negative.  Finally,
for every `s>=5`,

\[
                       s(3/2)-(3/2)^s<0.                \tag{12}
\]

The base case is `s=5`; multiplication by `3/2` proves the induction step.
The numerator of (2) is then negative for every `sigma>0`, so `d_s<0` and
(3) cannot have positive dB coefficient.  This exhausts all `s>=2`.

## Verification

Run `verify_clique_satellites.py`.  It checks (5)--(11) over exact symbolic
arithmetic and prints the exact endpoint signs.  The all-`s` induction in
(12) is analytic and is not inferred from finite testing.


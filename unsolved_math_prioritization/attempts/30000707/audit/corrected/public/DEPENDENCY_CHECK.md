# A narrowly scoped check of the recent finite-order theorem dependency

This is a check of one printed inference, **not a counterexample to the
statement of Theorem 7** and not a comprehensive review of its authors'
work. The present attempt does not rely on that theorem to close its gap.

## Version and location

Xiao-Min Li, Qing-Fei Zhai and Hong-Xun Yi,
*On a question of Gary G. Gundersen concerning meromorphic functions
sharing three distinct values IM and a fourth value CM*,
[arXiv:2402.03248v8](https://arxiv.org/abs/2402.03248v8), 6 January 2026.
The fetched PDF has 48 pages and SHA-256
`d25d83eee8f5cb6f3312077a975186603310410d9505d168497f6a7a01d0d607`.
Its abstract page still says 39 pages; the actual PDF is the version being
checked. Theorem 7 is on printed p.4. Lemma 13 is on p.9.
The inference examined is on printed p.39, immediately before equations
(152) and (154). The PDF pixels and text were both inspected.

The theorem claims all four values must be CM when two distinct
meromorphic functions share three values IM and a fourth CM and one
function has finite order. Combined with the rigorous finite-order
reduction in PROOF.md, that statement would resolve the target. A complete
proof certificate for that dependency has not been established here.

## Exact test of the positivity inference

Use the standard all-CM pair
\[
 f(z)=(e^z+1)/2,\qquad g(z)=(e^{-z}+1)/2.
\]
They share $0,1,1/2,\infty$ CM: the first two occur at $e^z=-1,1$
respectively, and the latter two are omitted. They are nonconstant,
distinct, entire, and of order one. In the notation of equation (28),
\[
 \frac{f'g(g-1)(g-1/2)}{g'f(f-1)(f-1/2)}=e^{-2z},
\]
so the polynomial in their Case 2 is nonconstant.

Consider the sector $-\pi/3\le\theta\le\pi/3$. Its angular exponent is
$\omega=\pi/(2\pi/3)=3/2$. Uniformly on this sector,
\[
 \log|f(re^{i\theta})|
 =r\cos\theta-\log2+O(e^{-r/2})=O(r).
\]
Consequently
\[
 r^{-\omega}\log|f(re^{i\theta})|\longrightarrow0
\]
uniformly. In particular, a claimed asymptotic leading coefficient
$c>0$ multiplying $r^\omega\sin(\omega(\theta+\pi/3))$ is impossible:
evaluation at $\theta=0$ forces $c=0$.

The antecedents relevant to this inference do not force positive $c$:

1. The sectorial logarithmic integral grows linearly in $r$, and so it
   exceeds a positive multiple of $T(r,f)/\log r$ for large $r$.
   This is the scale of their lower bound (122).
2. The angular characteristic is bounded. There are no poles. In the
   defining radial-boundary term, $\log^+|f(te^{i\theta})|=O(t+1)$ and
   the weighted integral is bounded by a constant times
   $\int_1^\infty t^{-\omega}dt<\infty$. The circular term is
   $O(r^{1-\omega})$. This verifies the relevant bounded-angular-
   characteristic hypothesis without relying on the disputed inference.
3. Lemma 13 permits a real coefficient, including zero. A lower bound on
   an $r/\log r$ scale does not force a nonzero coefficient at the larger
   scale $r^{3/2}$.

The same test applies to any smaller closed sector around the positive
real ray, where its corresponding exponent is still greater than one.
Thus the upgrades to positive constants before (152) and (154) are not
justified by the cited antecedents. Their subsequent comparison of two
positive, different powers cannot be imported here as a proof.

Relabeling the sector chosen by their spread argument does not change
this elementary scale issue. This observation does not say the theorem
is false, does not rule out a different proof, and does not certify a
complete repair. It is enough to keep the present target classified
UNSOLVED within this audited package.

## Control scope

`controls/check_controls.py` verifies the rational identity for the
canonical normalized pair and the exact power-scale inequality on the
positive ray, with illustrative numerical values. It does not attempt to
machine-formalize angular Nevanlinna theory or the 48-page manuscript.
No source PDF is included in the public deliverable.

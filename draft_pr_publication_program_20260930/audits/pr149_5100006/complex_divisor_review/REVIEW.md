# Independent adversarial review of PR149: complex divisor family

**Mathematical verdict: scoped PASS.** The cyclic-norm proof is valid for its expressly stated theorem: a nondegenerate, strictly nested confocal elliptical caustic and a billiard of **least** period `N = 2 (mod 4)`. No mathematical defect was found in its lattice, pole/zero multiplicity, cancellation, or primitive-star arithmetic. This verdict does not address priority, source-list status, or publication procedure.

Submission identifier supplied for this audit: original head `dde6ebe550ed7fe2e2fc8a1ff06fb13105be97ae`, queue label `claimed_solved2/5`. Those identifiers and the original proof are claims to audit, not mathematical authorities. This review did not read the supplied independent reviews, supplied verifier, or supplied test counts.

## Exact claim and assumptions

Let `a>b>0`, `alpha>beta>0`, and

```text
a^2-b^2 = alpha^2-beta^2 = c^2 > 0,
alpha<a, beta<b.
```

Fix the resulting nested confocal pair. Suppose its billiard map has least period `N=2m`, where `m` is odd. Then the ordinary positive Euclidean product of all `N` distances from either fixed focus is independent of the initial vertex, and the products for the two foci coincide. Primitive star polygons are included. A circle is handled directly by constant center distance.

Success criterion for this review: a checkable all-period deduction, with the full complex divisor and primitive orbit order established. Agreement at finitely many real phases is not a success criterion. Nonprimitive polygons counted with repetition, a hyperbolic caustic, and a degenerate caustic are not silently added to this claim.

## Independent reconstruction

### 1. Correct modulus and axis relation

Write `k=c/alpha`, `k'=beta/alpha`, and `K=K(k)`, `K'=K(k')`. Thus `0<k<1`. In canonical coordinates one step is `u -> u+2v` and

```text
P(u)=(-a sn(u,k), b cn(u,k)),
a=alpha dn(v,k)/cn(v,k),  b=beta/cn(v,k),  0<v<K.
```

The modulus is the caustic eccentricity. The primary parametrization is confirmed in [Stachel, Theorem 2 and (4.10)](https://arxiv.org/html/2105.03624). Here is an additional independent check of the geometric convention. Put `s=sn(t)`, `C=cn(t)`, `D=dn(t)` and denote the corresponding values at `v` by `s_v,C_v,D_v`. The [Jacobi addition formulas](https://dlmf.nist.gov/22.8) give the two endpoint vectors at `t-v,t+v`. Their chord equation simplifies to

```text
-s D_v x/(a C_v) + C y/(b C_v) = 1.
```

Substituting the axis relations yields

```text
-sn(t) x/alpha + cn(t) y/beta = 1,
```

which is exactly the tangent to the caustic at `(-alpha sn(t), beta cn(t))`. Hence the proposed axis relation gives the correct caustic and the correct step, rather than an outer-eccentricity parametrization. Also

```text
a^2-b^2
= alpha^2 (dn^2(v)-k'^2)/cn^2(v)
= alpha^2 k^2 = c^2.
```

The real map `u -> P(u)` is one-to-one modulo `4K`: the real Jacobi amplitude is strictly increasing and advances by `2pi` across that period. Therefore least period `N` is equivalent to

```text
2v = 4K tau/N,  gcd(tau,N)=1.
```

The choice `0<v<K` gives `0<tau<N/2`; orientation reversal changes no distance product. This includes every admissible primitive star turning number, not only `tau=1`.

### 2. Ordinary distance product and antipodal pairing

For a real point `(x,y)` on the outer ellipse, direct expansion using `y^2=b^2(1-x^2/a^2)` gives

```text
|P-(c,0)| = a-cx/a,
|P-(-c,0)| = a+cx/a.
```

Both expressions are strictly positive because `|x|<=a` and `a>c`. With the chosen parameter, the two distances are `a+c sn(u)` and `a-c sn(u)`.

For `N=2m`, primitivity makes `tau` odd, and

```text
m(2v)=2K tau,
P(u+2K tau)=-P(u).
```

Every focus-distance product can consequently be paired into exactly `m` products

```text
R(u)=product_{j=0}^{m-1} F(u+j delta),
F(u)=a^2-c^2 sn^2(u),  delta=2v.
```

This is an equality of ordinary positive distances. It introduces neither a complex square-root branch nor a signed-distance convention. Equality of the two focal products holds before any constancy argument.

### 3. Precise period lattice and complete divisor

The source facts needed here are compact: `sn` has periods `4K,2iK'`, changes sign under `2K`, has simple poles at `2rK+(2s+1)iK'`, and satisfies

```text
sn(z+K+iK') = dn(z)/(k cn(z)).
```

These are independently confirmed by [NIST DLMF 22.4](https://dlmf.nist.gov/22.4), including Tables 22.4.1 and 22.4.3. Therefore the nonconstant function `F` lives on

```text
T = C/Lambda,  Lambda=2K Z+2iK' Z,
```

and has precisely one pole class `p=iK'`, of order two. It cannot be removed: the `iK'` shift also gives `sn(p+epsilon)=1/(k sn(epsilon))`, so its leading Laurent term is

```text
F(p+epsilon) = -alpha^2/epsilon^2 + O(1).
```

The coefficient is nonzero. This also establishes that `Lambda` is the full period lattice of `F`, rather than merely a convenient lattice: any extra period would have to preserve its unique pole class, hence already belong to `Lambda`. Special elliptic moduli with extra automorphisms do not create extra translation periods.

At `q_+=p+K+v` and `q_-=p+K-v`, the shift identity gives

```text
F(p+K+t)=a^2-alpha^2 dn^2(t)/cn^2(t),
F(q_+)=F(q_-)=0.
```

The zero classes are distinct because their difference is `2v`, with `0<2v<2K`. Neither is the pole class, since `K+v` and `K-v` lie strictly between `0` and `2K`.

The total pole degree is two, so these distinct zeros exhaust the divisor and are both simple. There is also an independent local multiplicity check: differentiation using [DLMF 22.13](https://dlmf.nist.gov/22.13) gives

```text
F'(p+K+t) = -2 alpha^2 k'^2 sn(t) dn(t)/cn^3(t).
```

At `t=+v` or `-v` this is nonzero: `k'>0`, `sn(v)>0`, `dn(v)>0`, and `cn(v)>0`. Thus no hidden branch value, double zero, or removable pole is being assumed. The complete divisor is

```text
div(F) = [q_+]+[q_-]-2[p].
```

### 4. Translation order and norm cancellation

Since `N=2m` and `v=K tau/m`, the real translation has

```text
delta/(2K)=tau/m.
```

Because `gcd(tau,N)=1`, also `gcd(tau,m)=1`. Since `delta` is real, a nonzero imaginary lattice component cannot shorten its order. Thus its exact order on `T` is `m`.

Now `m v=K tau`, with `tau` odd, so `m v` is congruent to `K` modulo `2K`. Since `m` is odd,

```text
h_+=(m+1)/2, h_-=(m-1)/2
q_+ = p+h_+ delta  (mod Lambda),
q_- = p+h_- delta  (mod Lambda).
```

For `m>=3`, `h_+,h_-` are distinct and neither is zero modulo `m`. Hence at each point `p-j delta` the product has exactly one factor with a double pole and exactly two other factors with simple zeros. The leading pole coefficient and both leading zero coefficients are nonzero; all remaining factors are finite and nonzero there. This is a genuine removable singularity of order zero, not an unexamined `0 times infinity` expression.

Equivalently, summing translated divisors, the two zero lists are each a permutation of the same `m` pole classes. The complete norm divisor is zero. The norm is consequently a holomorphic function on the connected compact torus, and is constant. Its values for real `u` are finite and positive, proving the original claim.

No unsupported claim equivalent to the focal-product invariant was substituted for the central difficulty. The difficult step is discharged by the explicit divisor and finite subgroup arithmetic.

## Adversarial boundaries and counterexamples to broadened claims

1. **Least period `N=2` does not arise here.** Its only orientation-normalized candidate would require `v=K`, contradicting `0<v<K` and making `b=beta/cn(v)` infinite. The smallest admissible target period is six. Thus no `m=1` collision of the zero factors has been concealed.

2. **Primitive periods divisible by four fail this cancellation, and in fact are nonconstant when `c>0`.** For `N=2m` with even `m`, `tau` is odd. In coordinates divided by `2K`, a zero offset is `(m+/-tau)/(2m)`, whose numerator is odd; the pole subgroup consists of `j tau/m`, whose numerators over denominator `2m` are even. The zero and pole supports are disjoint. The paired focal product therefore has nonremovable complex poles, so cannot be constant on the real family by the identity theorem. This is an exact falsification of an attempted parity-free extension.

3. **Repeating an odd primitive orbit twice cannot be called a new primitive target orbit.** This exclusion is substantive. Let an odd primitive period be `n`, `v=2K tau/n`, and `delta=4K tau/n`. On the full `sn` torus `C/(4K Z+2iK' Z)`, `G=a+c sn(u)` has simple poles at `p,p+2K` and zeros at `p+3K+/-v`. In coordinates divided by `4K` with denominator `4n`, the zero offsets have numerators `3n+/-2tau`, which are odd. All translated pole offsets have even numerators. Consequently `product_{j=0}^{n-1} G(u+j delta)` has uncanceled poles, and is nonconstant. Its square, the product for a twice-traversed orbit, remains nonconstant because its real values are positive. A primitive triangle repeated twice supplies a concrete apparent `N=6` counterexample to a theorem stated in terms of vertex count alone. The submission correctly avoids that broader claim.

4. **Circle.** `c=0` makes every focus the center and each distance `a`; the product is `a^N`. The elliptic divisor proof is unnecessary and should not be extended by pretending a constant function retains the nonzero pole coefficient.

5. **Endpoint limits.** As `v->0`, the two zeros coalesce; as `v->K`, the finite outer-ellipse axis formulas fail. As `k->1`, the complementary period degenerates and the caustic ceases to have positive minor axis. None is an interior admissible parameter. Very small positive `k`, very large primitive star turning number below `m`, and moduli with additional elliptic-curve automorphisms introduce no extra exception to the proof.

6. **Repetition of an already admissible primitive target polygon.** The original constant product merely acquires an integer power. This is valid and separate from the odd-period reclassification above.

## Checkable artifacts, evidence status, and remaining gap

- `check_divisor.py` independently generates rational cosets and multiplicities without importing the submitted verifier. It also implements the theta-series definitions in [DLMF 22.2](https://dlmf.nist.gov/22.2) using only the Python standard library, checking real/complex norms, zero positions, regularized pole limits, ordinary focal products, and the chord-caustic convention. `independent_results.json` records the successful run of 2026-10-11 22:01 UTC.
- The finite exact run covered 1,053 primitive odd-`m` cases for `3<=m<=101`, including 1,003 primitive star cases, and 1,036 even-`m` disjoint-divisor controls. All 30 independently implemented theta diagnostics passed, with moduli `0.01,0.3,0.7,0.99,0.9999`. Maximum absolute norm error was `1.23e-15`, maximum relative norm error `1.45e-12`, maximum zero residual `2.30e-13`, and maximum regularized pole-limit error `9.39e-15`. The direct ordinary-focus product and chord-tangency checks also passed.
- Finite rational cases are exactly checked. Theta evaluations are ordinary floating-point diagnostics, explicitly **not** validated numerics and **not** a proof. The analytic argument above establishes the full stated theorem.
- Strongest verified result: all nondegenerate strictly nested confocal elliptical-caustic families of primitive least period `N=2 (mod 4)`, with every admissible coprime turning number, have equal constant ordinary one-focus products.
- Exact remaining mathematical gap within this scoped theorem: **none found**.
- Scope limitation to preserve if rewriting the theorem: use **least period** or an equivalent primitive-orbit convention. A statement counting repeated vertices without that convention is false, as item 3 proves.

Final review checkpoint: 2026-10-11 22:01:25 UTC. Completion estimate for this reviewer family's mathematical audit: 100%.

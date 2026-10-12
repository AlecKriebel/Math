# Independent extension review: complete least-period classification

**Mathematical verdict: PASS.** For a noncircular outer ellipse and a strictly nested nondegenerate confocal elliptical caustic, the ordinary product of distances to either fixed outer focus is constant over its real primitive family **if and only if its least period is `n=2 (mod 4)`**. Repetition preserves constancy exactly. No remaining mathematical gap was found in this classification.

This is a separate review of ROOT's `PERIOD_CLASSIFICATION_DERIVATION.md`; the original scoped report `REVIEW.md` is preserved. ROOT's derivation was treated as a candidate, not an authority. This review used the independently reconstructed Jacobi facts and geometric convention already checked in the first review. Its unified full-`sn` coset calculation was developed before receiving the parent's message that other reviewers had also found such a proof. Their agreement is not evidence used here. Priority and publication status are outside this review.

## Exact theorem and admissibility

Assume

```text
a>b>0, alpha>beta>0,
c^2=a^2-b^2=alpha^2-beta^2>0,
alpha<a, beta<b.
```

Put `k=c/alpha`, so `0<k<1`, and `K=K(k)`, `K'=K(sqrt(1-k^2))`. The canonical coordinate is

```text
P(u)=(-a sn(u,k), b cn(u,k)),
delta=2v, 0<v<K,
a=alpha dn(v)/cn(v), b=beta/cn(v).
```

These conventions and the caustic tangent-chord relation were independently checked in the first review, against [Stachel's Theorem 2](https://arxiv.org/html/2105.03624). The real coordinate parametrizes the entire outer ellipse modulo `4K`, and every real initial phase gives an orbit with this same step and caustic. A primitive periodic family has

```text
v=2K tau/n, delta=4K tau/n,
gcd(tau,n)=1, 0<tau<n/2.
```

Thus `n` is the least period, rather than a count with repetitions. All admissible primitive star turning numbers are included. Neither one-bounce nor two-bounce periodicity is admissible with this positive nested elliptical caustic; two-bounce periodicity would require the excluded endpoint `v=K`.

For real `u`, direct Euclidean-distance expansion gives

```text
g_+(u)=a+c sn(u)=|P(u)-(c,0)|,
g_-(u)=a-c sn(u)=|P(u)-(-c,0)|.
```

Since `|sn(u)|<=1` and `a>c`, both factors are at least `a-c>0`. Define the primitive products

```text
D_n^+(u)=product_{j=0}^{n-1} g_+(u+j delta),
D_n^-(u)=product_{j=0}^{n-1} g_-(u+j delta).
```

The theorem classifies each of these actual positive real products.

## Unified full-`sn` divisor proof, independent of parity pairing

Use the same torus for **every** least-period residue class:

```text
T0=C/Lambda0, Lambda0=4K Z+2iK' Z, p=iK'.
```

The period, simple-pole, and shift facts used here were checked independently against [NIST DLMF 22.4](https://dlmf.nist.gov/22.4) in the original review. Each `g` has exactly two simple pole classes, at `p` and `p+2K`; their leading Laurent coefficients are nonzero because `c/k=alpha>0`. The shift identity gives the complete zero sets

```text
g_- zeros: p+K+v, p+K-v,
g_+ zeros: p-K+v, p-K-v.
```

For example, `sn(p+K+/-v)=dn(v)/(k cn(v))=a/c`; the `2K` antiperiod supplies the negative value for the `g_+` roots.

Both displayed zeros of each function are nonpolar and distinct: their difference is `2v=delta`, strictly between `0` and `2K`, whereas the full real lattice period is `4K`. The relative real offsets of `g_+` lie strictly between `-2K` and `0`, and those of `g_-` strictly between `0` and `2K`, avoiding the two pole offsets. Two simple poles have total degree two. The two distinct zeros therefore exhaust each zero divisor, and both are simple. This precludes any hidden zero, branch multiplicity, or removable individual pole.

Translation by `delta` has exact order `n` on `T0`: it is real, and `delta/(4K)=tau/n` in lowest terms. Let `H` be its cyclic subgroup. Dividing real coordinates by `4K` and subtracting `p`, coprimality gives

```text
H={j tau/n mod1}={j/n mod1}.
```

The two zero offsets of each `g` differ by `delta`; consequently they generate **one and the same zero coset**, traversed twice in the norm. Its `n` points each have zero multiplicity two before cancellation. This fact holds for every `n`, including odd `n`.

The norm's pole supports are `p+H` and `p+2K+H`. The sign of translated offsets is immaterial to a complete subgroup, so these descriptions also account for the factors evaluated at `u+j delta`.

### Odd least period

When `n` is odd, `1/2` does not belong to the grid `H={j/n}`. The two pole cosets are disjoint and supply exactly `2n` distinct simple poles.

Let `epsilon=-1` for `g_+` and `epsilon=+1` for `g_-`. A representative zero offset is

```text
z=epsilon/4+tau/(2n),
n z=(epsilon n+2tau)/4.
```

Its numerator is odd. Thus `nz` is not an integer, so the zero coset misses `H`. It also misses `1/2+H`, since

```text
n(z-1/2)=((epsilon-2)n+2tau)/4
```

again has odd numerator. Neither pole coset is canceled. Each focal product has exactly `2n` uncanceled simple poles on `T0`, so each is nonconstant.

This calculation allows even or odd `tau`; no unwarranted odd-turning-number condition is imposed for odd `n`.

### Even least period

When `n` is even, primitivity forces `tau` odd, and `1/2` belongs to `H`. The two pole cosets coincide, giving `n` distinct pole positions of multiplicity two.

There is one zero coset, also of multiplicity two at each of its `n` points. It equals the pole coset precisely when

```text
n z=epsilon n/4+tau/2
```

is an integer. For `n=0 (mod 4)`, this expression is an integer plus a half-integer. For `n=2 (mod 4)`, its two half-integer terms sum to an integer. Hence:

- For `n=2 (mod 4)`, zeros cancel poles with exactly matching multiplicity two. The full norm divisor is zero. Each norm extends holomorphically across every apparent pole and is constant on the compact connected torus. Its real value is positive.
- For `n=0 (mod 4)`, the zero and pole cosets are disjoint. Each norm retains `n` uncanceled double poles on the full torus and is nonconstant.

The latter pole count agrees with ROOT's smaller-`sn^2`-torus statement: the quotient identifying `u` with `u+2K` identifies pairs of these full-torus poles and yields `n/2` double pole classes. There is no contradiction or lost multiplicity.

The manuscript's alternative congruence for `g_+`,

```text
-n+2tau = 4j tau  (mod 4n),
```

has the same criterion. Since `gcd(tau,n)=1`, `gcd(4tau,4n)=4`. Solvability requires and suffices that `4` divide `-n+2tau`. For even primitive `n`, `tau` is odd, giving exactly `n=2 (mod 4)`. For odd `n`, the analogous checks against both pole cosets fail by odd numerator parity as above.

## Why complex nonconstancy forces real-family variation

All these products are meromorphic in `u` and holomorphic in an open strip containing the entire real axis: the shifts are real, and the nearest individual poles lie at imaginary height `+/-K'`. Their restrictions to real `u` equal the actual Euclidean products themselves, because every real factor `a+/-c sn(u)` is strictly positive.

Suppose the product were constant over the entire real primitive family. Every real phase supplies a member of that family; cyclic relabeling merely identifies phases within `H` and cannot remove their values. Thus `D_n^+(u)` or `D_n^-(u)` would equal a single constant on the real axis. The identity theorem applied to any real interval forces equality to that constant as a meromorphic function on the connected complex domain. An uncanceled pole contradicts this conclusion.

In fact, a nonconstant norm here cannot be constant on any nonempty real open interval. No assumption that a sampled numerical phase happens to reveal the variation is needed.

An important adversarial distinction is satisfied: this argument would be invalid if one knew only that the **modulus** of a complex function was constant on the real line. Here the ordinary physical product equals `D` itself on that line, not merely `|D|`, so the identity-theorem step is valid.

## Both foci and repetitions

The antiperiod gives

```text
g_-(u)=g_+(u+2K),
D_n^-(u)=D_n^+(u+2K).
```

The norm is invariant under translation by `delta`, by cyclic reindexing of the factors. If `n` is even, `2K` belongs to `H`, so

```text
D_n^-(u)=D_n^+(u)
```

for every real phase, and indeed as meromorphic functions. This equality holds for even periods divisible by four as well as for the constant class. Odd `n` need not give equal focal products at a fixed phase; the classification claims that both are nonconstant, and does not claim such an equality.

For an `r`-fold traversal, with positive integer `r`, the listed product is exactly `(D_n^+/-)^r`. On the real family `D_n^+/-` is positive, and `x -> x^r` is injective on positive reals. Therefore repetition preserves constancy in both directions and cannot repair a nonconstant odd-period or four-divisible-period primitive product.

If a listed return length is `N=2 (mod 4)`, its least period divides `N` and is consequently either odd or `2 (mod 4)`. Thus the listed product is constant exactly in the latter case. A twice-traversed primitive triangle remains a counterexample to a statement in terms of counted vertices alone.

For a circle the foci coincide at the center, each distance equals the outer radius, and every listed product is `a^N`. The noncircular iff classification excludes this separate constant boundary. Hyperbolic or degenerate caustics are outside the reviewed hypotheses; no claim about them is inferred.

## Artifacts, evidence level, and exact remaining gap

- `check_classification.py` checks the full-`sn`-torus zero and pole cosets directly with `Fraction`, for both foci, without importing ROOT's code or a submitted verifier. Every admissible `(n,tau)` for `3<=n<=101` is included.
- `classification_results.json` records successful exact checks of 1,053 odd primitive pairs, 255 primitive pairs with `n=2 (mod 4)`, and 263 primitive pairs with `n=0 (mod 4)`. Both focal signs were checked for each pair. Multiplicity, total divisor degree, disjointness or cancellation, and zero-coset coincidence were checked.
- The same file records 33 supplementary theta-product cases across all residue classes, including stars, and direct checks of repetition powers `r=2,3,4`. These use only the independently implemented theta routine from the first review. They are ordinary floating-point diagnostics, **not validated numerics and not the proof**.
- An initial requirement that every nonconstant numerical case exhibit spread above `1e-12` was rejected as an unjustified numerical success criterion: small eccentricity and high star order can make variation much smaller. The final artifact reports such cases explicitly rather than treating numerical near-constancy as proof. At `k=0.1`, the `(n,tau)=(9,4)` and `(12,5)` diagnostic spreads fell below this chosen threshold for both foci. Exact uncanceled pole divisors establish their nonconstancy regardless. Variation above `1e-5` was observed for each excluded residue class and each focus elsewhere in the diagnostics.
- Strongest verified result: the complete least-period iff classification, equality of both focal products for every even primitive family, and exact preservation of constancy under positive integer repetition.
- Exact remaining mathematical gap within the stated nondegenerate nested elliptical-caustic hypotheses: **none found**. No substantive defect was found in ROOT's derivation or in its unified full-torus manuscript variant.

Final checkpoint: 2026-10-11 22:07:50 UTC. Completion estimate for this extension audit: **100%**. No Git reference, index, or remote was changed; no external individual was contacted. All new artifacts remain in this review folder.

# An explicit dyadic Riesz wavelet whose canonical tightening loses its natural affine indexing

Date: 2026-10-14. Scope: the classical single-generator, all-space, fixed-lattice and fixed-index contract in `CONSTRUCTION_CONTRACT.md` (SHA-256 `3fb43063cba5f31579efbc0f4272f39db3caab7d9bcf297874d536c76a017d90`).

## Result

Work on the complex Hilbert space H = L²(R), with

    (Df)(x) = √2 f(2x),        (T_k f)(x) = f(x−k).

Let

    h = 1_[0,1/2) − 1_[1/2,1),
    ε = 1/100,
    φ = h + ε Dh.

Then the single-generator affine family

    x_(j,k) = D^j T_k φ,             j,k ∈ Z,

is a Riesz basis, in particular a frame for all of L²(R), with frame bounds

    A₀ = (1−ε)² = 9801/10000,
    B₀ = (1+ε)² = 10201/10000.

If F is its ordinary frame operator, then

    ∥F^(−1/2) T_1 φ − T_1 F^(−1/2) φ∥ > 1/1000.

Consequently there is no generator η satisfying

    F^(−1/2)D^jT_kφ = D^jT_kη       for every j,k ∈ Z.

This assertion concerns the original translation lattice, dilation, and natural indexing. It makes no assertion about arbitrary reindexings or different lattices. It uses the inverse square root itself, not an inference from the canonical dual.

The generator is entirely explicit and compactly supported. Equivalently, up to endpoint values,

    φ(x) = 1 + √2/100     on [0,1/4),
           1 − √2/100     on [1/4,1/2),
           −1            on [1/2,1),
           0             elsewhere.

## 1. Haar coordinates and a bounded synthesis operator

Write

    e_(j,k) = D^j T_k h.

The family {e_(j,k) : j,k ∈ Z} is the orthonormal Haar basis of H; an elementary completeness proof is included in Section 5.

Define V on this basis by

    V e_(j,k) = e_(j+1,2k).

The map (j,k) ↦ (j+1,2k) is injective, so it sends an orthonormal basis to an orthonormal family. It therefore extends uniquely to an isometry V on all of H, with ∥V∥ = 1. Its adjoint is

    V* e_(j,k) = e_(j−1,k/2)     if k is even,
                 0              if k is odd.

In particular,

    V*h = e_(−1,0),     V*e_(0,1) = 0.

The physical translation/dilation convention gives the exact identity

    T_k D = D T_(2k).

Hence, for every pair j,k,

    D^jT_kφ
      = D^jT_kh + εD^jT_kDh
      = e_(j,k) + ε e_(j+1,2k)
      = (I+εV)e_(j,k).

Set A = I+εV. Since ε∥V∥ < 1, its Neumann series makes A boundedly invertible. Thus {Ae_(j,k)} is a Riesz basis for all of H. For every f ∈ H, Parseval's identity for the Haar basis gives

    Σ_(j,k) |⟨f,x_(j,k)⟩|² = ∥A*f∥².

Because ∥V*∥ = 1,

    (1−ε)∥f∥ ≤ ∥A*f∥ ≤ (1+ε)∥f∥.

Squaring proves the asserted frame bounds. The ordinary frame operator is exactly

    F = AA* = I + ε(V+V*) + ε²VV*.

All sums here are Hilbert-space frame sums; no scale or translation truncation is used.

## 2. A quantitative inverse-square-root expansion

Put

    X = F−I = ε(V+V*) + ε²VV*,
    q = 2ε+ε² = 201/10000.

Then X is self-adjoint and ∥X∥ ≤ q < 1/2. The convergent scalar binomial series

    (1+t)^(−1/2) = Σ_(n≥0) c_n t^n,
    c_n = (−1)^n binom(2n,n)/4^n,

has c_0 = 1, c_1 = −1/2 and |c_n| ≤ 1. Uniform convergence on [−q,q] and continuous functional calculus therefore give

    F^(−1/2) = I − X/2 + R,
    ∥R∥ ≤ Σ_(n≥2) q^n = q²/(1−q).

Since q < 3ε and q < 1/2,

    ∥R∥ < 18ε².

Thus we may write

    F^(−1/2) = I − (ε/2)(V+V*) + R_B,
    R_B = R − (ε²/2)VV*,
    ∥R_B∥ < (37/2)ε².

Now define

    U = F^(−1/2)A.

This is the unitary polar factor of A, although its unitarity is not needed for the defect estimate. Direct multiplication, preserving operator order, yields

    U = I + (ε/2)(V−V*) + E,

where

    E = −(ε²/2)(V+V*)V + R_B(I+εV).

Consequently,

    ∥E∥
      ≤ ε² + ∥R_B∥(1+ε)
      < [1 + (37/2)(101/100)] ε²
      = (3937/200) ε²
      < 20ε².

This is an operator-norm estimate on the full infinite-dimensional Hilbert space.

## 3. Failure of translation covariance on the forced generator

Let T = T_1. We have

    e_(0,1) = Th,
    Ve_(0,1) = e_(1,2) = T e_(1,0) = TVh,
    V*e_(0,1) = 0,
    V*h = e_(−1,0).

Using the expansion in Section 2,

    Ue_(0,1) − TUh
      = (ε/2)[Ve_(0,1) − V*e_(0,1) − TVh + TV*h]
        + Ee_(0,1) − TEh
      = (ε/2)T e_(−1,0) + Ee_(0,1) − TEh.

Since T is unitary and all the e_(j,k) are unit vectors,

    ∥Ue_(0,1) − TUh∥
      ≥ ε/2 − 2∥E∥
      > ε/2 − 40ε²
      = 1/200 − 1/250
      = 1/1000.

The vector giving the leading term can also be written explicitly as

    T e_(−1,0) = 2^(−1/2)(1_[1,2) − 1_[2,3)),

so its unit norm and nonzero character do not depend on any abstract identification.

Finally, Ah = φ and Ae_(0,1) = Tφ, by Section 1. Hence

    Ue_(0,1) − TUh
      = F^(−1/2)Tφ − TF^(−1/2)φ.

This proves the displayed quantitative failure for the actual canonical tightening of the actual affine frame.

## 4. Why no alternative generator fixes the natural indexing

Suppose a vector η satisfies the requested indexed equality

    F^(−1/2)D^jT_kφ = D^jT_kη

for every j,k. Taking j = k = 0 forces η = F^(−1/2)φ. Taking j = 0 and k = 1 would then give

    F^(−1/2)T_1φ = T_1F^(−1/2)φ,

contradicting Section 3. Thus the canonical Parseval family fails the fixed-index, same-lattice single-generator affine contract.

## 5. Elementary justification of the all-space Haar basis fact

Each e_(j,k) has unit L² norm, is supported on the dyadic interval

    I_(j,k) = [k2^(−j),(k+1)2^(−j)),

and has integral zero. Two dyadic intervals are either disjoint up to endpoints or nested. If they have different lengths and are nested, the coarser Haar function is constant on the support of the finer one; hence their inner product vanishes. Distinct Haar vectors are therefore orthogonal.

For completeness, suppose f ∈ L²(R) is orthogonal to every e_(j,k). On every dyadic interval, the integrals of f over its two halves are equal (complex conjugation, if present in the inner-product convention, does not affect this conclusion). Therefore the average of f on any dyadic interval equals the average on each successive dyadic ancestor. If I_n is such a sequence of ancestors with |I_n| → ∞, Cauchy–Schwarz gives

    |average_(I_n) f| ≤ ∥f∥₂ / √|I_n| → 0.

Thus f has integral zero over every finite dyadic interval. Finite linear combinations of indicators of dyadic intervals are dense in L²(R): for example they approximate compactly supported continuous functions by dyadic step functions, and those continuous functions are dense in L²(R). Therefore f = 0. This proves completeness on the entire space, rather than on a proper wavelet subspace.

## Audit-sensitive points

- The operator A maps Haar vectors to the affine atoms; F is AA*, not A*A.
- The expansion is for F^(−1/2), not F^(−1).
- V is an auxiliary isometry defined in Haar coordinates; it is not claimed to be the physical dilation D or to commute globally with translation.
- Both negative and positive scales, and all integer translates, are present.
- The translation failure is local at φ itself, at the fixed index (j,k) = (0,1).
- The exact perturbation coefficient is 1/100; no limiting existence claim or numerical evidence is needed.
- The assertion is an explicit mathematical counterexample to the stated operational contract. No claim of novelty or literature priority is made.

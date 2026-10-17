# Canonical-cover reduction for the fixed complex Euclidean signature

Authored mathematical audit and proof, shared pass 1. This addresses the open stratum of the frozen contract, over the constant field C. It does not make a novelty claim or address other groups/classifying pairs. Degenerate one-dimensional strata and the terminating theoretical decision procedure are proved in the companion reports.

## 1. Input and corrected normal form

Let S be a reduced integral curve in A² with its fixed coordinate functions (u,v), let D be the smooth projective normalization, and put K=C(D)=C(u,v). Assume u, v, and du are nonzero. All differentials below are meromorphic differentials, and all identities are in function fields, so singularities, infinity, and ramification are included.

Define

- η = i du/v;
- q = du²/(4uv²);
- ω = (η − du/u)/2;
- ρ = du/(2v);
- σ = du/(2uv).

The imported η and q have the correct factors and signs for z=x+iy, w=x−iy and the usual signed-curvature convention. The more economical first-order equation is dlog a=ω, rather than first adjoining a logarithmic primitive of η and then an unrelated square root.

### Frenet derivation and audit

On a local nonisotropic regular arc of a source, choose ds with ds²=dz dw. Set T=dz/ds, so dw/ds=T⁻¹. For signed curvature κ, dlog T=iκ ds. Thus R=dz/dw=T² satisfies

    dlog R = 2iκ ds.

Since u=κ² and v=κ_s, du=2κv ds. Consequently

    dlog R = i du/v = η,
    dz dw = du²/(4uv²) = q.

These identities extend from the dense local arc to the source normalization. Define the meromorphic function

    a = dz/ρ = 2v dz/du.

The product identity gives dw=a⁻¹σ, and the ratio identity gives

    R = u a²,
    dlog a = (dlog R − dlog u)/2 = ω.

Conversely, if dlog a=ω, dz=aρ, and dw=a⁻¹σ, then R=ua² has dlog R=η and dz dw=q. These are precisely the Frenet identities, with no omitted sign or factor of two.

The local arc-length choice changes the signs of κ and ds together and leaves κ_s, κ², and all displayed rational identities unchanged.

## 2. The input-derived logarithmic test

A nonzero algebraic solution of dlog a=ω exists over a finite extension of K if and only if some positive integer n and f∈K* satisfy

    nω = dlog f.                                      (L)

Necessity follows from the norm. If M/K is finite and a∈M* satisfies the equation, then dlog N_(M/K)(a)=[M:K]ω. Sufficiency follows by adjoining a root a^n=f.

Condition (L) has the following intrinsic reduction, which distinguishes the divisor obstruction from the holomorphic obstruction.

1. Every pole of ω must be simple, and every residue must belong to Q.
2. Let m be the least positive integer clearing all residue denominators (m=1 if there are no poles). Let

       A = Σ_P m Res_P(ω) P.

   This is an integral degree-zero divisor on D.
3. Its class [A] must be torsion in Pic⁰(D). Let t be its exact order, with t=1 for the zero class. Choose f∈K* with div(f)=tA.
4. Test the exact differential identity

       mt ω = dlog f.                                (H)

   The difference is holomorphic, but being holomorphic is not sufficient: it must vanish identically.

If these steps pass, the least possible exponent in (L) is

    n = mt.

Indeed, any exponent N in (L) is divisible by m, and its function has divisor (N/m)A. Hence t divides N/m. Writing N=mtℓ, that function differs by a nonzero constant from f^ℓ, so Nω−dlog(f^ℓ)=ℓ(mtω−dlog f). This proves both minimality and the impossibility of repairing a failed holomorphic test by a larger exponent.

The residue/divisor formulation is a theorem over arbitrary C. It is not, by itself, a uniform algorithm for unspecified complex-number oracles: an exact coefficient model and a terminating torsion test must accompany an algorithmic claim. A separately supplied finite torsion bound B allows testing BA for principality and then mBω=dlog f; this decides existence without an unbounded search. Once existence is known, the minimal n may be recovered from divisors of mB, or from the exact order of [A].

## 3. Preferred cover and its universality

Suppose the logarithmic test passes. Let n be the least positive exponent and choose f with nω=dlog f. Define

    L = K(a),       a^n=f,

and let C be the smooth projective curve with function field L. This cover is well defined up to K-isomorphism: changing f by a nonzero constant only rescales a by a constant in C*.

The polynomial X^n−f is irreducible. An elementary proof avoids any Kummer irreducibility criterion: if a has degree d≤n over K, then taking its norm from K(a) gives dω=dlog N(a). Minimality of n forces n≤d, hence d=n. Thus L/K is cyclic Galois of degree n, with a↦ζa for ζ∈μ_n.

Every finite extension M/K containing a solution b of dlog b=ω contains a K-isomorphic copy of L. To see this directly, b^n/f has zero differential, hence belongs to C*. Rescale b so b^n=f; irreducibility supplies the embedding. Under it, b is a constant multiple of a. There is no existential choice of an unknown finite cover remaining.

## 4. Trace lemma: further covers cannot repair exactness

Let E/F be a finite extension of one-variable function fields over C. If a meromorphic differential θ over F becomes exact over E, say θ=dh, then

    θ = d(Tr_(E/F)(h)/[E:F]).

This follows because trace commutes with derivation and Tr_(E/F)(θ)=[E:F]θ. Characteristic zero is essential. Thus meromorphic exactness descends under every finite cover. The converse is immediate.

Apply this to the two explicit differentials on the preferred cover:

    α = aρ,
    β = a⁻¹σ.

If either is not exact on C, no further finite cover of C can make it exact. This rules out both ramified and unramified repairs, at every genus. Residue vanishing alone is not substituted for exactness.

## 5. Necessary-and-sufficient criterion and reconstruction

**Theorem.** On the open stratum u v du≠0, S is the standard fixed-pair signature of an allowed source if and only if:

1. the logarithmic test in Section 2 passes; and
2. both α=aρ and β=a⁻¹σ are exact meromorphic differentials on the single preferred cover L/K.

When the test passes, choose z,w∈L with dz=α and dw=β, put x=(z+w)/2 and y=(z−w)/(2i), and take the reduced affine Zariski closure X of their image. This is an integral plane curve of degree greater than one with generically nonzero Euclidean metric. Its signature image closure is exactly S. Moreover C is its normalization; no extra field-generation condition is required.

### Necessity

Let X be an allowed realizing source and M=C(X) its function field. The signature gives an inclusion K⊂M. The Frenet audit gives b∈M* with dlog b=ω and

    dz=bρ,  dw=b⁻¹σ.

The norm proves the logarithmic test. Universality embeds L in M with b=c a for c∈C*. Hence α=c⁻¹dz and β=c dw become exact on M. The trace lemma descends exactness to L.

### Sufficiency, with field generation proved

The forms α and β are nonzero, so z and w are nonconstant. Their metric dz dw=q is nonzero. Set E=C(z,w)⊂L. It has transcendence degree one and L/E is finite.

Differential ratios computed in E agree with their pullbacks to L. Put R=dz/dw∈E*. Since R=ua² and dlog R=η, the rational Euclidean invariants of the plane image are

    U_X = −(dlog R)²/(4 dz dw) = u,
    V_X = i dU_X/(dlog R) = v.

The second denominator is nonzero because du and v are nonzero. The first identity is the rational expression for κ²; the second follows from du=2κκ_s ds and dlogR=2iκ ds. Thus the signed-curvature convention agrees with the fixed ordered pair, not merely with a coordinate change of it.

In particular K=C(u,v)⊂E. Since a=dz/ρ and both differentials in this ratio are defined over E, a∈E. Therefore

    E = K(a) = L.

This proves field generation and identifies the normalization. The invariant functions u,v induce a dominant map to S because K embeds faithfully, hence its signature closure is exactly S. A line with nonzero metric has zero curvature, whereas u is nonconstant here, so the image cannot be a line. Thus its degree is greater than one.

### In fact no additional source-cover freedom survives

For any other realizing source M, the descended primitives on L pull back to the original coordinate primitives up to constants. Consequently its z,w lie in L after a transformation

    z ↦ c z+z₀,       w ↦ c⁻¹w+w₀,

with c∈C*. These are exactly complex special-Euclidean transformations in isotropic coordinates. Because the actual plane source field is generated by z,w, it equals L. Every realizing source is thus SE(2,C)-congruent to this reconstruction, and its signature degree is n. This conclusion follows directly from the displayed identities and is not an appeal to an external completeness theorem.

## 6. Two rational equations on the original normalization

The preferred-cover exactness tests can equivalently be performed on K. They are:

    dA + ω A = ρ,            A∈K;                    (E+)
    dB − ω B = σ,            B∈K.                    (E−)

If A,B solve them, then

    z=aA,       w=a⁻¹B

are the required primitives. Conversely, if α is exact on L, project any primitive z to the a-character eigenspace of Gal(L/K). Explicitly, for τ(a)=ζa,

    z_χ = (1/n) Σ_(j=0)^(n−1) ζ^(−j) τ^j(z).

Then dz_χ=α and τ(z_χ)=ζz_χ. The eigenspace is aK, so z_χ=aA for A∈K and A satisfies (E+). The inverse character gives (E−). For n=1 the same statement is simply division by a∈K*.

This reduction leaves only two rational linear differential equations on the fixed input curve; it does not quantify over source functions on arbitrary covers. A bounded Riemann–Roch search for A and B supplies finite algebraic linear systems; the explicit pole bounds and their proof belong to the companion differential-equations report. The logarithmic test must still be imposed independently: solvability of these inhomogeneous equations alone does not force a to be algebraic.

## 7. Edge cases relevant to this proof

- ω=0 is permitted by the logarithmic test, with n=1 and a constant. It does not automatically realize a curve: the exactness tests remain necessary. For example v=iu gives α proportional to du/u, which is not meromorphically exact.
- Holomorphic ω with no poles passes only if ω=0. A nonzero holomorphic differential cannot be a rational multiple of dlog f on a complete curve.
- Poles, zeros, and branch points of a do not invalidate the trace or derivative identities; all statements live in function fields and extend meromorphically.
- Primitive choices add translations. Changing the root scale changes only a complex rotation in isotropic coordinates. Neither changes the prescribed pair (u,v).
- This theorem assumes the nonconstant open stratum. It does not divide by u or v on the degenerate strata; those require the separate short analysis in the full report.


## 8. Compact positive certificate

A positive certificate consists of the normalized input field K and its functions u,v, an integer N≥1, and f,A,B∈K with f≠0, satisfying the three exact rational differential identities

    Nω=dlog f,      dA+ωA=ρ,      dB−ωB=σ.

No assertion of minimality is needed to verify this positive certificate. Factor X^N−f over K, take any irreducible factor, and let a be its root. Differentiating a^N=f gives dlog a=ω. The coordinate functions z=aA and w=a⁻¹B then reconstruct the required source by Section 5. The source field is K(a), even if N was not minimal. A certified minimal exponent gives its degree immediately; otherwise it is the degree of the selected irreducible factor. This is a finite explicit reconstruction rather than an existential choice of a cover or source coordinates.

If n>1 is minimal, the base equations have at most one solution each. A difference of two A-solutions would give a nonzero homogeneous solution H with d(aH)=0, forcing a∈K, a contradiction; the B-equation is identical. For n=1 the homogeneous freedom is exactly translation of z or w.

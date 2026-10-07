# Independent reconstruction of the level-prime trace interface

Checkpoint: 2026-10-07 05:53 UTC. Completion of the specifically assigned
level/module/split-mod8 audit: 100%. This closes the local representation
dependency left conditional in the earlier coefficient report. No source or
Git changes; no external communication. The pinned coefficients.tex and
pointwise.tex hashes are respectively
6e2266b43cdada2d63df5c0d5bba8b42e6dd24ea6cc9b230e3d52e9dbc5f213d and
66717dc63cf7821281f988386a24a99f65113cfa1fa97419f8ebd752a78056d3.

## Exact claim and the necessary level hypothesis

The claim needed at pointwise.tex 651–700 is a characteristic-zero identity
on the ramified conductor-one constituents, followed by a coefficient identity
on the entire divided vector. It is **not** an identity on arbitrary oldforms:
on an unramified old multiplicity space U_p need not be scalar.

Let g have half-integral weight 3/2 and level M, with p odd and p∤M.
Here M includes all fixed support sieves. Put
B=(U_p−η(p)V_p)g/2, C_0=θ B[1]Θ_empty, C_p=θ B[p]Θ_p,
R=θ B, and f=(R−C_0−C_p)/2=θ H_{p}.
The actual coefficient definitions are U_p a[n]=a[pn] and
V_p a[n]=a[n/p], with the latter zero unless p|n.

[James–Ono, Proposition 3, p.4](https://uva.theopenscholar.com/files/ken-ono/files/043.pdf)
states with these exact definitions that both operators carry weight k+1/2,
level M, character ψ forms to level Mp and character ψ(4p/·). It requires
4|M and k a nonnegative integer, both satisfied. For odd units (4p/·)=(p/·).
The level exponent is one, not two. Independently, V_p is obtained by
conjugating Γ_0(Mp) into Γ_0(M); the half-weight multiplier quotient supplies
(p/d). Further U_p=U(p²)V_p directly on expansions. At p|Mp the square-index
Hecke operator U(p²) preserves that space and extracts a[p²n], as explicitly
shown in [Purkait, Lemma 4.1 and its proof, p.7](https://arxiv.org/pdf/1208.4326).
This checks both the metaplectic character and exponent.

Multiplication by θ changes weight 3/2 to weight 2 without a further
Dirichlet character: the fourth power of its multiplier is (cz+d)².
The character of Θ_J in this case is η(−J/·), and ψ=ηχ_{−4}.
Consequently R and C_p have ordinary character ψ(p/·) at level Mp,
primitive ramified quadratic character at p, whereas C_0 has character ψ
and level M. Constants B[1],B[p] and division by 2 do not change these
characteristic-zero level statements. This separates the two local types
without a conjectural decomposition or a q-expansion identity inferred from
the desired conclusion.

## What the primary local theorem actually supplies

[Carayol, Theorem (A), §§0.3–0.7, pp.409–411](https://www.numdam.org/article/ASENS_1986_4_19_3_409_0.pdf)
applies to holomorphic cuspidal GL_2 forms over a totally real field, with
archimedean weights at least two and the stipulated common parity. Its
additional finite discrete-series assumption applies only when the field
degree is even. Thus F=Q, weight two satisfies it without that additional
condition. The theorem identifies the local Weil representation at every
finite p for every auxiliary coefficient place of residual characteristic
different from p; here the latter is 2 and p is odd. This is full local
compatibility, not a statement only at good primes.

Carayol uses geometric Frobenius and a Hecke correspondence with a dual and
an absolute-value twist. Fix the corresponding arithmetic convention by
tr(ρ(Frob_q))=a_q and det(ρ(Frob_q))=qχ(q) at good q. In that convention
the local L-factor is det(1−ρ(φ_p)p^{−s}|V^{I_p})^{-1}.
For a normalized weight-two newform at p|level, the q-expansion U_p relation
gives a[pn]=a_p a[n], hence its local Euler factor is
(1−a_p p^{−s})^{-1}. Local compatibility therefore gives λ=a_p on the
unramified invariant line. This explicitly fixes the possible inverse and
power-of-p ambiguities. Changing from Carayol's convention without the
corresponding dual would be incorrect.

For any constituent of R or C_p, the ambient level bounds its conductor
exponent by one; the ramified determinant bounds it below by one. A
nonzero monodromy operator would give a special representation: with
unramified twisting its determinant is unramified, and with ramified
twisting its conductor is at least two. It is therefore excluded.
With monodromy zero, the conductor formula gives dim V^{I_p}=1 and Swan=0.
The complementary inertia character is precisely the ramified quadratic
determinant. The distinct inertia characters are preserved by Frobenius
(the quadratic character is invariant under conjugation), so the local
representation splits into an unramified line and a ramified quadratic
line after adjoining coefficients. In a suitable basis,

    ρ(τ_p)=diag(1,−1),  ρ(φ_p)=diag(λ,μ),  U_p=λ.

No irreducible supercuspidal representation has this one-dimensional inertia
invariant space. The Eisenstein constituents are sums of their defining
characters; exponent one makes exactly one character unramified. Their
U_p eigenvalue is its Frobenius value, also directly from the Eisenstein
q-expansion Euler factor. At the prime p there is no old multiplicity for
these conductor-one constituents. Multiplicity from other level primes
is retained and U_p acts by the same scalar on it.

It follows, as an operator on these constituents, that

    U_p² t(φ_p)=U_p³+d(φ_p)U_p,

because λ²(λ+μ)=λ³+(λμ)λ. Likewise for an arbitrary g, writing z for its
lower-right matrix entry, the two differences in co:inertia are −2zμ and
−2z; multiplication by U_p=λ and d(φ_p)=λμ gives the identical value
−2zλμ. These are deductions from the checked local type and compatibility,
not merely substitutions conditional on an unverified principal-series
assertion.

## Integral divided module and the unraised term

The argument in co:traces 789–849 works without saturation. All diamond
translates of f are integral: on the original H_U each apparent denominator
is (ψ_U(u)−η(u)χ_{−4}(u)^i(−J/u))/2, which is zero or a unit since
the quotient is quadratic. Good Hecke q-expansion operators preserve
integrality and commute with diamonds. The O-module generated by f and
the undivided unary terms under these operators embeds, through finitely
many injective coefficients, into O^r. It is a finite closed module.
On finitely many characteristic-zero systems, simultaneous Chebotarev
approximation makes T_q tend to t(u) and q⟨q⟩ tend to d(u); scalar actions
are extended by the identity on all old multiplicity spaces. The closed
module is consequently preserved. Approximating eigenvalues sufficiently
closely also approximates the operator on this fixed lattice, even if the
chosen spectral projections have bounded denominators.

C_0 is unramified at p. Its ordinary good-prime coefficient formula gives

    (t(φ_p)C_0)[p²]=C_0[p³]+(d(φ_p)C_0)[p].

R and C_p give the same coefficient identity using the ramified operator
identity. Linear combination and division by 2 now prove

    (t(φ_p)f)[p²]=f[p³]+(d(φ_p)f)[p]

in characteristic zero, with integral terms by module stability. This
does not incorrectly apply the ramified operator identity to C_0.

The determinant cancellation needs an extra check after division. Let
δ_p be d(φ_p) on R,C_p and δ_0 its value on C_0. They share the same
cyclotomic factor and differ only by a quadratic character, so
(δ_p−δ_0)/2 is integral. Exactly,

    d(φ_p)f=δ_p f+(δ_p−δ_0)C_0/2.

Since θ≡1 mod 2 and H_p[p]=0 by its subtraction, f[p]=0 mod 2.
Moreover Θ_empty[p]=0 because p is not a square, and

    (θΘ_empty)[p]=2 Σ_{r²+m²=p} η(m)m

with r,m positive and the retained sieves. Thus C_0[p] is even. Both
terms of (d(φ_p)f)[p] vanish modulo 2, including the correction divided
by 2. An arbitrary ramified Frobenius lift can give either sign for the
new quadratic determinant; this calculation handles both signs. It
does not rely on assigning a Dirichlet value at a ramified prime.

## Fresh prime, allowed support, and the mod-8 conclusion

Choose a new prime p′ avoiding p,M and the tested index, whose image in a
finite quotient approximates φ_p on all representations to the required
lattice precision. Include K and every rational quadratic character used
by the S_0 support tests in that finite quotient. Since p splits in K,
φ_p∈G_K and hence p′ also splits. Those rational characters are unramified
at p, so their values on φ_p are their values at p. Their matched values
at p′ show pp′ is a square unit at all places of S_0, including 2.
Therefore pp′ is an allowed all-K-split squarefree index even when p
itself is not on the total filter. Chebotarev supplies infinitely many
such fresh primes; requiring extra precision does not change this.

The good-prime coefficient formula at p² has no second term for p′,
so the left side tests f[p²p′]. Modulo 2 it is H_p[p²p′]. Its underlying
squarefree coefficient is a(pp′); the assumed extra depth is at least
3, so it vanishes after B's division by 2 and H's further division by 2.
The unary subtractions cannot contribute at p²p′. This gives f[p³]=0
mod 2 by the determinant calculation above.

Finally f[p³]≡H_p[p³] mod 2, and the square-index recurrence, independently
fixed by the Shimura eigenvalue relation, gives 1,a−1,a(a−1)−p at
1,p²,p⁴, after the stated phase normalization. The p-unary contribution
has coefficient η(p)p at p³ and the empty unary has zero coefficient.
The result is a unit times (a−1)(a−p−1)/4. Full rational two-torsion
implies a even: at this odd good prime #E(F_p)=p+1−a is divisible by 4.
Thus a−1 is odd and the integral coefficient being zero mod 2 forces
a≡p+1 mod 8. This verifies the exact pw:split-mod8 interface.

## Scoped verdict

No mathematical gap remains in the assigned level-change, local module
identity, unraised unary correction, finite-precision matching, or mod-8
deduction. The earlier conditional trace arithmetic has been upgraded to
a reconstruction of its actual representation and integral-module inputs.
The companion analytic audit, including its explicit sieve replacement and
height comparison, is in nonvanishing_audit.md. These reports do not by
themselves certify deductions elsewhere in the entire upstream program;
they identify no unresolved dependency within the scope assigned here.

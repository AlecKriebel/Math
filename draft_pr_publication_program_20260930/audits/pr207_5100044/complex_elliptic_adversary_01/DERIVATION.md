# Independent reconstruction of the analytic mechanism

This is an independent reconstruction for the elliptic-caustic, least-period,
signed straight-chord problem. It does not use the submitted checker, old
review, neighboring proofs, or another current reviewer's assessment. The
original proof is the claim under examination. All computations below are
deductions from the displayed standard Jacobi identities and real geometry.

## 1. The canonical coordinates cover the stated geometry

Let the caustic semiaxes be alpha>beta>0, c²=alpha²-beta²>0,
k=c/alpha, k'=beta/alpha. Set K=K(k), K'=K(k'), p=iK'. For any
strictly exterior confocal ellipse (a,b), there is a unique real v in (0,K)
with cn(v)=beta/b. Confocality and the identities sn²+cn²=1,
dn²=1-k²sn² give

    a=alpha dn(v)/cn(v), b=beta/cn(v).

There is no modulus-versus-parameter ambiguity here: k is the modulus;
mpmath's parameter in the diagnostic script is k².

The boundary parametrization P(w)=(-a sn(w),b cn(w)) is one-to-one modulo
4K on the real boundary. Addition formulas show that the chord with endpoints
P(u-v), P(u+v) has equation

    -sn(u) dn(v) x/a + cn(u) y/b = cn(v),

equivalently -sn(u)x/alpha+cn(u)y/beta=1. This is the caustic tangent at
(-alpha sn(u),beta cn(u)). Thus the shift is exactly delta=2v, with no
quarter-period or caustic-normalization ambiguity. The published canonical
billiard input and its converse are Stachel's Theorem 4.3 / (4.9), independently
checked in the publisher HTML: [primary source](https://link.springer.com/article/10.1007/s40879-021-00524-2).

Closure and least period imply N delta=4K tau with gcd(N,tau)=1. Orientation
can be chosen to make 0<tau<N/2; the opposite orientation is obtained by
reversal. Conversely these coprime shifts have least period N because P is
injective modulo 4K. This covers the stars without treating their signed areas
as unsigned union areas.

## 2. Original signed area

Write h=sn(v), q=cn²(v), d_v=dn(v), t=h², D=1-k²t sn²(u). Direct addition
gives

    (1/2) det(P(u-v),P(u+v))=ab h cn(v) dn(u)/D,
    dn(u-v)+dn(u+v)=2 dn(u) d_v/D.

For C_A=ab h cn(v)/d_v, summing gives A=C_A sum_(j=0)^(N-1)
dn(w+j delta). Now let N=4n, m=N/2=2n, ell=2K/m. Since tau is odd,
m delta=2K tau, so this becomes

    A(w)=2 C_A S(w), S(w)=sum_(j=0)^(m-1) dn(w+j delta).

All summands are positive for real w. This verifies the normalization and the
sign even for self-intersecting stars.

## 3. Exact divisor of S

The standard Jacobi facts used here are the dn period pair (2K,4p), the
anti-period 2p, evenness, and the local shift dn(p+z)=-i cn(z)/sn(z).
Their primary table references are [DLMF 22.4](https://dlmf.nist.gov/22.4);
the additions are [DLMF 22.8](https://dlmf.nist.gov/22.8). In particular the
dn residue at p is -i, not an unspecified possibly canceling quantity.

Because gcd(tau,m)=1, S has period ell: its periods 2K=m ell and
delta=tau ell generate ell. On X=C/(ell Z+4p Z), the only possible poles
are p and 3p. At the literal lift w=p, exactly j=0 is singular: a second
singular summand would require j tau=0 mod m with 0<j<m. Thus the residue
of S at p on X is exactly -i. The residue at 3p is +i. Reducing the real
lattice identifies different pole locations; it does not multiply residues.

Evenness follows by replacing j with -j modulo m. Put z=p+ell/2. This point
is finite, since it is not a pole. The relations -z=z-ell-2p,
S(-z)=S(z), S(z-2p)=-S(z) force S(z)=0; likewise at 3p+ell/2. They are
two distinct points. A nonconstant meromorphic function on a torus has equal
total zero and pole orders, so these are exactly its two zeros, both simple.
Consequently S(w)S(w+ell/2) has no poles or zeros, is constant by compactness,
and is positive by its real restriction. This argument uses the complete
divisor, rather than sampled values or a presumed cyclic identity.

## 4. Focal inversion algebra

For f=(c,0), real Euclidean distance to P(w) is a+c sn(w)>0. This follows by
squaring and choosing the positive branch, whose lower bound is a-c>0.
The translated inverted vertex is (P(w)-f)/(a+c sn(w))². Translation of a
closed polygon does not affect its signed shoelace area.

Set

    U=1-2k²t+k²t², V=1-2t+k²t², W=1-k²t²,
    C=b h d_v q²/alpha³.

Expanding the endpoint distance product, with s=sn(u), yields

    qD d(u-v)d(u+v)/alpha²
      =d_v² D+2ks q d_v²+k²q(s²-t)
      =(1+ks)(U+kVs).

The translated endpoint determinant is

    det(P(u-v)-f,P(u+v)-f)=2alpha b h d_v dn(u)(1+ks)/D.

Dividing half this determinant by the square of the distance product gives

    E(u)=C dn(u) D / [(1+ks)(U+kVs)²].

This is an ordinary rational meromorphic continuation of a real formula;
it contains no complex conjugation. Real denominators cannot vanish: U>0,
U²-k²V²=k'²W²>0, |s|<=1, and k<1. Pairing the antipodal sides gives

    B(u)=E(u)+E(u+2K)
        =2C D [U²+k² V(V+2U) sn²(u)]
          /[dn(u)(U²-k²V² sn²(u))²],
    A_f^dagger(w)=R(w+v), R(u)=sum_(j=0)^(m-1) B(u+j delta).

In particular E, B, R are strictly positive on the real line with the chosen
forward orientation. No zero-area denominator or unmentioned sign choice is
hidden in proportionality below.

## 5. Complete generic pole accounting

Assume V is nonzero and put r=K+p, H(u)=U²-k²V² sn²(u). On the smaller
sn² torus with periods (2K,2p), H has one double pole at p. Doubling gives
cn(delta)=V/W, dn(delta)=U/W. The quarter shift

    sn(r+z)=dn(z)/(k cn(z))

then makes the two H zeros r+delta and r-delta. They are distinct: equality
modulo (2K,2p) would force delta=K because 0<delta<2K, equivalent to V=0.
They are different from p and r. Their simplicity can also be checked without
divisor counting:

    H(r+z)=W² k'² [sn²(delta)-sn²(z)]/cn²(z),
    H'(r+delta)=-2 W² k'² sn(delta)dn(delta)/cn(delta) != 0.

This exhausts the zero divisor. In the full B torus (2K,4p), its possible
double poles are these two points and their 2p translates. At r and r+2p,
dn has a simple zero but H=U²-V² is nonzero, since

    U-V=2t k'²>0, U+V=2q d_v²>0.

Thus these are at most simple poles. At each common sn,cn,dn pole p or 3p,
the numerator of B has order at most four while the denominator has order
five (because V!=0). Hence B has a removable zero there. These alternatives
exhaust all points of the compact torus. In particular no affine "infinity"
has been silently discarded.

The standard shifts and parity give

    sn(2r-u)=sn(u), dn(2r-u)=-dn(u), B(2r-u)=-B(u).

If the Laurent coefficients at r+delta are a_-2,a_-1, then those at
r-delta are -a_-2,a_-1. This assertion also permits a_-2=0.

## 6. Cyclic multiplicities and the exceptional four-period case

For V!=0 and N divisible by four, m>=4. At the literal lift u=r, the terms
which can be singular in R are exactly j=0, j=1, j=m-1. They come from
r, r+delta, r-delta respectively. The indices are distinct; the last two
double coefficients cancel. All other poles of R are translates of this
calculation, since j delta runs through the m distinct real residue classes
modulo 2K. Therefore after reducing to X, R has at most simple poles at r
and r+2p. There is no multiplicity factor depending on the turning number.
The N=8 shifts delta=K/2 and 3K/2 still have distinct indices 0,1,3, so the
smallest generic order is covered.

If V=0, cn(delta)=0 entails delta=K, hence tau/N=1/4. Coprimality forces
N=4,tau=1. Here

    B(u)=(2C/U²)[q/dn(u)+t dn(u)].

The base poles at p and r (and their 2p translates) are all simple. Now ell=K
and R=B(u)+B(u+K), so p and r are the same real class in X. Sums of simple
poles remain at most simple, even when they coalesce after lattice reduction.
The generic removable-pole argument at p is correctly not used in this case.

## 7. Residues, compactness, and conclusion

Both R and S(u+K) are ell-periodic and change sign under 2p. The latter
has exactly the two possible simple pole locations of R and residue -i at r.
Subtracting the unique multiple that matches the residue at r matches the
other residue by anti-periodicity. The remainder is holomorphic on X and
therefore constant; its anti-period makes that constant zero. Hence

    R(u)=C_R S(u+K), C_R>0.

The positivity follows from the real restriction. Thus

    A(w) A_f^dagger(w)=2 C_A C_R S(w)S(w+K+v).

Here (K+v)/ell=(m+tau)/2 is a half-integer, because m is even and tau odd.
The product is constant by Section 3. Notice K=(m/2)ell, so S(u+K)=S(u)
in the case at issue; retaining K is harmless and tracks the pole location.

For the other focus, -f, the inverted translated point satisfies
I_-f(P)=-I_f(-P). Since -P(w+j delta)=P(w+(j+m)delta), its ordered vertex
list is a cyclic shift followed by central reflection, both of which preserve
signed area. Reversal changes the sign of each of the two areas, preserving
their product. These are exact operations, so both foci and both traversal
orientations are covered.

## 8. Boundaries and falsification controls

The proof uses 0<k<1 and 0<v<K. Degenerate/hyperbolic caustics, coincident
outer and inner ellipses, and zero-length or diametral sides are excluded by
these hypotheses. Limits toward them cannot be inserted into the torus proof
without a new limiting argument. No such extension is claimed.

For k=0, focal inversion is centered at the circle center. A regular star's
area is (N/2)a² sin(2pi tau/N), and its inverse area is the same expression
with a² replaced by a^-2. The product is N² sin²(2pi tau/N)/4, constant
under rotation, including reversal. For N=4 this gives four.

The real N=4 axial quadrilateral has area 2ab; direct Euclidean inversion
gives its inverse area 2/(ab), so the constant is four. This calculation is
consistent with the separate exceptional-divisor proof, and does not justify
claiming novelty for this known special case.

As an analytic negative control, the same generic mechanism applies for
primitive N=4n+2>=6, but now m and tau are odd, so (K+v)/ell is an integer.
It gives A A_f^dagger=2 C_A C_R S(w)². S is nonconstant because it has
poles, and it is strictly positive on the real line, so this product cannot
be constant on the real line (otherwise the identity theorem would make
S² constant meromorphically). A twice-traversed primitive period-six orbit
displayed with twelve vertices likewise has a varying product, scaled by
four. This explains why least period and the parity hypothesis are necessary.

## Assessment

I find no mathematical gap in the submitted elliptic-function mechanism under
the exact hypotheses audited here. The strongest verified statement is the
full primitive N divisible-by-four, nondegenerate nested confocal-ellipse
theorem for signed straight-chord focal-inverse areas, either focus and either
orientation. The proof does not rest on a finite numerical test. This is a
mathematical validation only; no general novelty, historical priority, broader
caustic theorem, publication clearance, or external human review is asserted.

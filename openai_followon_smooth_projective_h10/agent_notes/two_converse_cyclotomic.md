# Cyclotomic arithmetic audit at the pinned 2-converse

Closing checkpoint: 2026-10-06 22:37 PDT / 2026-10-07 05:37 UTC.
**Assigned non-CM arithmetic audit complete (100%).** The closing supplement
below reconstructs the preceding perfection/residual interface, checks the
actual prime-2 real duality sequence, and makes all convention corrections
explicit. No genuinely unsupported claim or counterexample remains in this
assigned slice, using the established external theorems whose hypotheses
are identified here. This verdict does not certify the separate coefficient,
ring-class, or full pointwise assembly mechanisms.

Checkpoint: 2026-10-06 22:27 PDT / 2026-10-07 05:27 UTC.
Scope: `build/sections/cyclotomic.tex:315–748`, especially uniform fixed-form
integrality, unsmoothing, rational divisibility, local Euler corrections,
and the central determinant formula. Best-guess completion of this assigned
arithmetic slice: **85%**. Estimated completion of my own independent audit
of the whole companion: **45%**. Neither percentage estimates the probability
of the theorem. Other agents own the preceding perfection/residual lemma and
the ring-class, coefficient, and assembly obligations.

Read-only source checkout:
`/Users/alec/Desktop/math/preprints/A-pointwise-2-converse-for-elliptic-curves-with-rational-two-torsion-September-24-2026`,
HEAD `adc7f1241b42e322a6451854ab7e4b4c146bf78a` (previously verified).
No companion edits or git mutations were made. No outside communication was
initiated. Primary PDFs were inspected through web or memory-only extraction;
no large PDF was saved to disk.

## Result and scope of validation

I found **no falsification of the assigned arithmetic slice**. The previously
unread Kato references have now been inspected in the original, including
the actual constructions and proof hypotheses. They support the fixed-form
trace at coefficient prime 2 and the rational, rather than residual-image
integral, divisibility used here. The local and determinant length calculation
can be reconstructed without a growing-prime error. This materially closes
the source-access concern in `two_converse_dependency.md`.

The strongest result established here is conditional on the preceding
perfect-complex/base-change and residual-concentration assertions: **the
arithmetical steps 315–748 do produce the claimed uniform denominator and
central valuation formula, given those interfaces and the stated standard
global/local duality results**. This is not a certification of Theorem 1.1,
nor an independent reproof of Kato's Euler-system theorem, the full Nekovar
duality formalism, or the ring-class proof. The exact remaining scope is at
the end of this note. There is also a harmless Euler-convention clarification
whose explicit repair is supplied below.

## Original sources actually inspected

1. K. Kato, *p-adic Hodge theory and values of zeta functions of modular
   forms*, Asterisque 295 (2004), pp. 117–290. Primary source:
   <https://www.numdam.org/article/AST_2004__295__117_0.pdf>.
   The 175-page PDF was fetched into memory and the following printed pages
   were extracted and read: 143–145, 153–163, 180–186, 189, 212–234,
   236–243. In particular the relevant hypotheses were read rather than
   inferred from a theorem title. PDF extraction sometimes mangles formulas;
   the accompanying prose and the unmangled occurrences of the same formula
   were compared. The key theorem numbers and prime restrictions below are
   clear in the original.
2. A. Burungale and Y. Tian, *A rank zero p-converse to a theorem of
   Gross–Zagier, Kolyvagin and Rubin*, arXiv:2506.03465v1, primary text:
   <https://arxiv.org/pdf/2506.03465v1> (the version specified in the
   companion bibliography). Theorem 2.6 and Remark 2.7 on p. 5, and their
   dependency on Theorem 2.1, were inspected. The rational main-conjecture
   statement is for every prime, including 2. Its proof invokes the
   rational equivariant main conjecture and Kato's Section 15 link with
   elliptic units; that full downstream proof was not reconstructed here.
3. Nekovar, *Selmer complexes*, original book metadata and the actual
   searchable text of Section 6.9.1 were inspected:
   <https://www.numdam.org/item/AST_2006__310__R1_0/>.
   The full 43 MB book exceeds the web fetch limit and was not downloaded.
   Thus my check of the integral length sequence is a direct duality
   reconstruction below, with the book's complete chain-level theorem
   remaining an explicitly external standard input. Kato pp. 239–240
   independently states the global/local Poitou–Tate sequences, their
   finite-condition quotients, and the real-prime correction at p=2.

## Fixed-form class and the uniform denominator

### Hypotheses and integral trace, lines 315–361

Kato Chapter II fixes an arbitrary coefficient prime p. Section 8.1.2
constructs the integral smoothed class with coefficients in the integral
cohomology of Y_1(N). Section 8.1.3 is its image in the lattice of the
**fixed normalized newform f**; Section 8.3 defines this lattice as the
image of integral modular cohomology. It is free of rank 2 over the
coefficient valuation ring. None of these statements excludes p=2.

For a symbol xi in SL_2(Z), Section 8.9 chooses an auxiliary L with
m|L, N|L and prime(L)=S. Its trace to Y_1(N) over Q(mu_m) lands in the
lattice identified with

    Z_p[Gal(Q(mu_m)/Q)] tensor V_{k,Z_p}(Y_1(N)).

The trace is integral and independent of L. Section 8.11 projects this
class to the lattice of f. The growing L therefore does not produce a
new lattice or a new form at level L. This is the decisive distinction
from an unsupported claim that every varying twisted form has uniformly
comparable integral modular lattices.

The parameters at weight 2 are k=2, r=r'=1, admissible in Sections 8.1
and 9.7. The requirements include prime(cd) disjoint from S, (cd,6)=1,
and (d,N)=1. The companion's c,d prime to 6Nm, together with fixed omitted
support, can meet these conditions. Auxiliary fixed support should also be
included in the CRT modulus if it contains primes not already in 3Nm;
this changes only a fixed modulus. The actual presentation takes S as
2N, h_0, and Q, so there is no extra varying requirement.

Sections 13.6–13.9 provide fixed SL_2(Z) symbols having nonzero projections
on the two period lines. At weight 2 the symbol index j is 1. Thus the
fixed modular lattice can be embedded into T_2E after multiplying by a
single power 2^{c_E}; a fixed combination of the two sign symbols costs
only a fixed additional denominator. The sign is fixed in each cube.

The map from the cyclotomic group ring to Z_2[Gamma_n x G] is an actual
integral quotient/twist of coefficient modules. Shapiro and restriction to
the open global support carry an actual cohomology class through this
map. The map is not a Fourier idempotent and never divides by |G|. Taking
the real cyclotomic quotient likewise uses a group-ring homomorphism, not
an integral decomposition into the two complex-conjugation idempotents.

Kato Proposition 8.12 has its Euler product only for primes in S'\S.
When m2^n grows while S is fixed and already contains 2, this product is
empty. Exact norm compatibility therefore gives the asserted inverse
limit. No separate cohomological-surjectivity premise was used here.

### Unsmoothing, lines 363–389

Kato (4.2.4) gives (u,v)=(r+2-k,r) when r'=k-1. Hence weight 2 and
r=r'=1 give u=v=1. Theorem 6.6 for xi in SL_2(Z) and c=d=1 mod N uses
the factors

    (c^2-c chi(c))(d^2-d chi(d)).

Thus the corresponding universal factors c^2-c sigma_c and d^2-d sigma_d
in the companion have the correct exponents. Here the discriminants are
odd products of signed odd primes, so their quadratic characters have odd
conductor. Choosing c,d=1 mod m makes their tame actions, including chi_h0,
trivial. If this section were generalized to discriminants with 2-primary
conductor, e should additionally cover that fixed conductor; that extension
is unnecessary in its stated scope.

Fix e >= max(2,v_2(N)); the CRT imposes c,d=1 mod 3N_odd m and
c,d=1+2^e mod 2^{e+1}. Such positive integers exist without invoking primes
in arithmetic progressions. They are prime to all required support. In
Gamma=1+4Z_2, the exponent kappa(c) relative to a topological generator
satisfies v_2(kappa(c))=e-2. It is nonzero.

Modulo the maximal ideal (2,I_G) of O[G], the factor is
1-(1+t)^{kappa(c)} in F_2((t)), and is nonzero. Indeed if kappa(c)=2^j u
with u odd, the coefficient of t^{2^j} is 1. It is therefore a unit of
O[G]. At t=0 it is c(c-1), whose valuation is precisely e. The same holds
for d and inverse actions. Only **two** smoothing factors occur, regardless
of the number of tame primes. Their inverse creates no denominator at
(2), and their central denominator is 2e, independent of m, h_0, or b.

This argument does not provide uniform Laurent support for their inverses
modulo 2^M; it does not need to. The cyclotomic Fourier-intersection step
only asks for O[G] integrality and characterwise bounded-denominator power
series, unlike the more delicate ring-class outer-limit argument.

## Reciprocity and rational divisibility

### Reciprocity, lines 391–421

Kato Theorem 9.7 sends the smoothed p-adic class under the dual exponential
to the modular zeta element. Theorem 6.6 gives its character sum for every
character of (Z/m)^x, including an imprimitive character whose conductor
is a proper divisor of m. It uses the same fixed symbol vector delta.
Consequently a superfluous tame prime in m does **not** introduce a factor
phi(m), a normalized character average, or a new modular-period vector.
It contributes exactly the omitted local L-polynomial.

The factors from a tame quadratic Gauss sum and the odd conductor are
2-adic units. Depending on the chosen de Rham twist basis, the Gauss factor
may be placed on the basis rather than on the scalar. This convention
does not affect the valuation being claimed. The only possible 2-adic
period/differential discrepancies come from the fixed symbol and one of
finitely many local twists at 2. Their valuations are bounded independently
of the prime support. Fixed sign-line projection contributes at worst one
fixed factor 2.

For q in Q that is good and unused at h, the omitted polynomial at the
center is exactly

    1-a_q(E) chi_h(Frob_q)/q + 1/q = #E^h(F_q)/q.

Since q is odd, its valuation is v_2(#E^h(F_q)). For a good ramified
quadratic twist the invariant rational representation is zero and its
local L-factor is 1. This also applies to every prime of h_0; their number
can grow without producing an extra reciprocal error. The two smoothing
factors and the fixed omitted support account for bounded terms only.

### Actual prime-2 hypotheses, lines 428–438

Kato Theorem 12.5(3), printed p. 222, is a height-one statement at primes
not containing the coefficient prime. It allows a local H^2_Iw correction.
The stronger integral Theorem 12.5(4) explicitly assumes p != 2 and a
large integral image. The companion correctly does not use 12.5(4).

Theorem 13.4, printed p. 226, separates the two assertions in the same
way: its rational assertion (2) has no odd-prime or residual-irreducibility
condition. It requires nonzero Euler-system constituents, equal +/- ranks,
purity, rational irreducibility, and a sigma in Gal(Q/Q(mu_p^infty)) whose
1-eigenspace is one-dimensional. For non-CM elliptic curves these last
conditions follow from an open SL_2 image; an element [1,2^M;0,1] of a
sufficiently small congruence subgroup has exactly that 1-eigenspace.
Kato Remark 12.8.2 and Section 13.13 use this open-image version. Full
rational 2-torsion changes the residual image but does not violate it.
Sections 13.5–13.7 give the nonvanishing of the fixed-symbol zeta line
using cyclotomic finite-order twists. Section 13.1 fixes a prime p without
an oddness restriction; no hidden standing p != 2 assumption was found.

For CM curves, Burungale–Tian Theorem 2.6 in the actual cited v1 asserts
the rational equality for every prime. Remark 2.7 explicitly distinguishes
the as-yet finer integral versions. This matches the companion's usage.
For Family004, E:y^2=x(x-1)(x+3) has j=35152/9, so it is non-CM: a
rational CM j-invariant is an integer. Thus Family004's cyclotomic input
does not require the CM replacement theorem.

### Full global cohomology and fixed multipliers, lines 440–572

The cone between j_* cohomology and full global cohomology is governed by
W_q=H^1(I_q,V_h), not blindly by V_h^{I_q}(-1). The resulting two-term
local complex has differential 1-gamma_q Frob_W and is injective over A.
The cyclotomic exponent of an odd positive prime q is nonzero: its image
in 1+4Z_2 cannot be 1, since q is not +/-1. Therefore its determinant is
not the zero power series. Localization at a divisor of the determinant
does not make that map zero; it remains injective.

At good unused primes, W_q=V_h(-1), so the determinant is
P_q(Z)=1-(a_q/q)Z+(1/q)Z^2. At active good primes, inertia is -1 and
W_q=0 rationally. At split multiplicative primes the Tate extension gives
W_q=Q_2(-1), hence D_q=1-gamma_q/q. The example in the source correctly
avoids the spurious central zero obtained from V_h^{I_q}(-1)=Q_2.
For every reduction type D_q(0) != 0 follows from local duality and
V_h(Q_q)=0, since local elliptic torsion is finite.

The long exact sequence bounds the extra H^2 length by the sum of
v_p(D_q). The class acquires the exact same varying unused Euler factors,
so they pay for this increase in the zeta index. The fixed bad-prime
determinants and the fixed omitted L-polynomials can differ, but their
finite collection has nonzero central value and can be covered by one
fixed multiplier. At 2, derived local control gives

    H^2_Iw(Q_2,T_h)_Gamma tensor Q_2 = H^2(Q_2,V_h) = 0.

There is no higher local cohomology obstructing this H^2 coinvariant
identity. Thus the local characteristic polynomial has no factor t;
a common F_2 for the finitely many local twists can have F_2(0) != 0.
This excludes a correction that would force every central value to zero.

The rational comparison can be reconstructed from rank-one H^1 and the
same reciprocity formula for infinitely many finite-order characters.
Coprime Gauss-sum factorization produces a fixed scalar for each h and a
group-like cyclotomic unit; chi_h(2)^n is constant after fixing the parity
of n. The scalar may have large 2-valuation and is used **only over A**.
After clearing the scalar ratio and smoothing denominators, both sides
are bounded-denominator power series. An infinite set of nonzero tests
then forces equality by Weierstrass preparation. This argument would fail
for arbitrary Q_2[[t]] series with unbounded coefficient denominators; the
actual smoothed classes and finite denominator clearing avoid that issue.

### Explicit repair of the inverse-Frobenius convention, lines 574–595

The ratio in the source compares P_q(Z) to Z^2 P_q(Z^{-1}). If one starts
instead with P_q(Z^{-1}), first multiply the whole universal class by
Z^2=gamma_q^2. The quadratic factors square to 1. This is an integral
group-like unit of Lambda[G], with central value 1 at every character.
At active characters it leaves an extra group-like factor, harmless to
height-one lengths over A and to central valuations.

Now

    P_q(Z)-Z^2 P_q(Z^{-1}) = ((q-1)/q)(1-Z^2).

Both polynomials are units over O[G], so their ratio r_q is 1 mod 2.
Consequently U_q=1+((r_q-1)/2)(1+g_q) is integral and a unit: modulo
(2,I_G), its second summand is zero. It evaluates to r_q on unused
characters and 1 on active characters. Its unused central value is 1
because Z=+/-1. Products of these corrections introduce no growing
2-denominator and no central valuation. The source omits the explicit
preliminary global Z^2 translation, but it is available integrally and
does not change the asserted conclusions; this is a repairable convention
clarification, not a counterexample.

## Independent central length calculation, lines 629–748

Assume s_2(E^h)=0. Then Mordell–Weil rank and divisible Sha corank are
both zero, so Sha[2^infty] is finite and the discrete finite Selmer group
has length s(h). This assumption supplies finiteness before analytic
nonvanishing; no use of the desired converse is needed.

Let K_v be the integral Kummer subgroup of H^1(Q_v,T_h). For odd v,
local duality identifies H^1(Q_v,E)[2^infty] with the dual of the finite
2-completion of E(Q_v). Its Tate module is zero, so the inverse-limit
Kummer sequence gives K_v=H^1(Q_v,T_h), including bad places. At 2 the
same argument gives

    L_2 = H^1(Q_2,T_h)/K_2 = Z_2 (noncanonically).

Its identification under exp^* with a de Rham line has an index depending
only on the local curve and differential. A fixed sufficiently small
formal subgroup has elliptic logarithm an isomorphism; exp^* is its
adjoint for local duality. There are finitely many local twists at 2,
so these indices are bounded even for additive or supersingular reduction.

In rational global duality, the finite Selmer group is zero and the
local singular line is one-dimensional. The global ordinary H^1 maps
isomorphically to it and ordinary H^2 is zero. At odd finite places the
rational local H^1 is zero (the integral Kummer group there is finite).
The positive modification adds just the rational real invariant line.
Hence the rational positive specialization has H^1 of dimension 2 and
no other cohomology, agreeing with the generic determinant rank.

Let J be the image of global H^1 modulo torsion in L_2 and
i=length(L_2/J). Compact/discrete duality for the orthogonal Kummer
conditions gives, with bounded real terms inserted,

    0 -> L_2/J -> Sel_{2^infty}(E^h)^vee -> H^2_global(T_h)
      -> direct_sum_{q in S} H^2(Q_q,T_h)
      -> H^0(Q,A_h)^vee -> 0.

This follows by taking the local singular quotient in the global
Poitou–Tate sequence: at odd primes the compact finite condition is all
H^1(T_h), and its orthogonal discrete condition is zero, exactly the
local Kummer condition for A_h. At 2 they are dual finite conditions.
The global compact finite subgroup is torsion, so its image in L_2 is
zero. This explains why only J occurs in the displayed initial quotient.
One must use the exact real-modified sequence, not infer a uniform size
bound merely from Kato's wording “exact up to multiplication by 2.” The
errors here are the actual real cohomology groups of a rank-2 lattice,
whose relevant degrees have bounded F_2 dimension.

Writing tau_q=length H^0(Q_q,A_h), the exact length identity is therefore

    length H^2_global(T_h) = s(h) - i + sum_{q in S} tau_q + O_E(1).

Global torsion injects into E^h(Q_2)[2^infty]; at 2 and fixed bad primes,
local torsion also lies in a finite collection of local curves. These
are genuinely bounded terms, not terms repeated once for each prime.
The positive real modification changes only bounded torsion and one
real-line index. An integral determinant basis specializes to an integral
basis, so it introduces no additional h-dependent normalization.

If exp^*(z_h) is nonzero, its coordinate on the global free line has
valuation v_2(exp^*z_h)-i+O_E(1). For inverse determinant, degree-2
torsion subtracts its length and degree-1 torsion adds its bounded
length. This sign follows already from [Z_2 --2^a--> Z_2] in degrees
1,2, whose inverse determinant lattice is 2^a Z_2. Thus

    v_2(u_h(0))
      = v_2(exp^*z_h) - i - length H^2_global(T_h) + O_E(1)
      = v_2(exp^*z_h) - s(h) - sum_{q in S} tau_q + O_E(1).

The two i terms cancel exactly. There is no need to bound the global
localization index i, which can be large.

At a good unused q, reduction is an isomorphism on 2-primary torsion
because its kernel is pro-q. Hence tau_q=v_2(#E^h(F_q)), exactly cancelling
the omitted Euler term in reciprocity. At an active good q, inertia is
-1 on T_h, so A_h^{I_q}=A_h[2]=E[2]. Frobenius then has invariants of
length t_q. This includes all primes dividing h_0. Their sum is exactly
2w(h). Therefore

    v_2(u_h(0)) = v_2(mathcal L(h)) - s(h) - 2w(h) + O_E(1).

All remaining terms come from a fixed form, two fixed smoothing factors,
one fixed multiplier, fixed real sign, and finitely many local twists
at fixed places. This proves the claimed uniform error ledger.

If L(E^h,1)=0, reciprocity makes exp^* zero. The specialization then
belongs to rational finite Selmer, which is zero under the corank-zero
assumption; its ordinary class and wedge with the real line are zero.
Unsmoothing is regular at t=0 because c(c-1)d(d-1) is nonzero; inverse
Euler corrections are also regular there because #E^h(F_q) is nonzero.
Thus determinant base change gives u_h(0)=0 legitimately. Conversely a
nonzero L-value has nonzero exp^*, so the wedge is nonzero.

## Exact remaining interfaces and promotion boundary

* Perfection and derived coefficient/central base change of C_S^+,
  `cyclotomic.tex:196–244`, are prerequisites. They were read, but their
  infinite-cochain/minimal-model argument is owned by the limits audit.
* Residual concentration over O[G], `cyclotomic.tex:245–312`, is the
  crucial input that converts the actual integral class into uniform
  determinant-coordinate integrality. In the present slice, once this
  is granted, no further index arises from a free degree-1 complex.
  If this premise fails, the denominator conclusion does not follow.
* The exact real-modified integral Poitou–Tate theorem is a standard
  external input. I reconstructed the required quotient and all length
  cancellations, but did not inspect the full chain-level proof in
  Nekovar's 567-page book. The limited “exact up to x2” statement by
  itself is weaker than the uniformly bounded-error claim; the proof
  needs the explicit fixed-dimensional real terms, as stated here.
* Kato Theorem 12.5(3) is used as an established external theorem whose
  hypotheses and local correction were checked. The original Euler-system
  descent proof was not reproved. The CM replacement has the same status.
* This slice does not establish the ring-class missing-vertex theorem,
  outer DVR limit, integral coefficient trace identities, or final
  corank-one assembly. Consequently it cannot alone exclude Family004's
  remaining divisible-Sha alternative identified in the initial note.

No central claim was transferred to an equivalent unsupported uniform
denominator statement within the assigned slice: the fixed-form trace and
O[G] unsmoothing give its arithmetic part concretely. The remaining
residual/perfection interface must still be established by its own proof.
This distinction is essential before promoting the companion theorem or
the proposed downstream H10 implication.

## Closing supplement: the remaining interfaces reconstructed

### Perfection and residual concentration

I cross-checked `cyclotomic.tex:196–312` against the actual perturbation
proof in `ring-limits.tex:121–185` and the independent
`agent_notes/two_converse_limits.md` audit. The needed contraction is
explicit: over an Artin coefficient quotient, split the residual cochains
into finite cohomology plus disks, lift the graded bases, write d=d_0+epsilon,
and use the finite geometric inverse of 1+h_0 epsilon. Nilpotence makes
the contraction formulas finite even with infinitely many disks. Continuous
cochains reduce exactly and are flat because they are filtered unions of
finite partition-function modules. The real cone has finite bounded
residual cohomology, using the high-degree restriction isomorphism in
Nekovar 5.7.1.7. Minimal finite free models reduce compatibly along the
coefficient quotients: a quasi-isomorphism between the two reduced minimal
models is a graded isomorphism, which lifts to an invertible change of basis.
Equivalently the fixed residual splitting can be lifted compatibly before
applying the nilpotent perturbation formulas. The inverse limit computes
the completed cochains and their derived specializations. Thus this
interface uses actual cochains and maps, not just finite cohomology counts.

For the trivial residual constituent in the real layer K_n of degree d=2^n,
the signature vector of epsilon=1+zeta+zeta^{-1} has odd augmentation,
because its norm is -1. The recurrence f_{n+1}(X)=f_n(X^2-2) proves
f_n(-1)=-1 by induction. It also proves epsilon is a unit. Its translates
span the regular F_2[C_d] signature module, since this group algebra is
local and odd augmentation means a unit. Hence H^1_global -> H^1_real
is surjective. The Brauer sum relation and the presence of a place at 2
give surjectivity in H^2 as well. The degree-zero map is the injective
diagonal F_2 -> F_2^d. Therefore H^1 of the positive cone has dimension
d+O_S(1), while every other degree has bounded dimension and higher
degrees vanish. This accounts for the real H^0 cokernel of dimension d-1;
it must not be omitted from the dimension count.

The class-group bound can also be established without any subtle
Iwasawa-control error: the real 2-power cyclotomic layers have odd class
number. At a quadratic step K_{n+1}/K_n only the unique prime at 2 ramifies,
and no real place becomes complex. The ambiguous-class formula gives

    |Cl(K_{n+1})^{C_2}| = h(K_n) / [U(K_n):U(K_n) intersect Norm(K_{n+1}^x)].

The denominator is a power of 2. Starting with h(Q)=1, induction makes
the fixed class group odd. Any nontrivial finite 2-group with an involution
has a nonidentity fixed element, by orbit counting. Thus the full class
group has no 2-primary part. The S-class group is a quotient and also has
zero 2-rank. This is the classical one-ramified-prime argument; the precise
theorem and its class-number formulas can be checked in H. Yokoi,
*On the class number of a relatively cyclic number field*, Nagoya Math. J.
29 (1967), pp. 31–44, pp. 31–32 and Lemmas 4–5:
<https://doi.org/10.1017/S0027763000024119>.
The primary PDF was read through the web, without a disk file.

For a perfect complex over F_2[[t]], derived reduction modulo t^d has
dimension d times the cohomology rank plus bounded torsion contributions.
The preceding dimensions force precisely one rank in degree 1 for the
trivial constituent after inverting t, and zero ranks elsewhere. Two
trivial constituents give dimension 2 in degree 1 for E[2]. In Family004
they are a direct sum because all of E_l[2] is rational. A minimal finite
free complex over the local ring O[G] then has exactly one nonzero term,
O[G]^2 in degree 1. This proves the denominator-free residual interface
used at lines 616–626, including its asserted independence of |G|.

### Exact real-place error, rather than “exact up to x2”

The original primary searchable PDF now gives Nekovar **5.7.1.6 on
printed p. 131** explicitly: the finite-coefficient Poitou–Tate sequence
is exact, and its real local summands use complete Tate cohomology.
Section 5.7.1.7 supplies the high-degree global-to-real isomorphism.
Section **6.9.1 on p. 154** extends the Selmer-complex construction to
these Tate real cochains for bounded coefficients. Thus the earlier source
access limitation no longer leaves the real-error theorem unexamined.
The independent limits audit also checked the hypotheses of Theorem
6.3.4: finite bounded coefficient complexes, perfect pairing, and exactly
orthogonal local conditions. The finite Kummer conditions meet them.

For completeness, the size bound is explicit. For a rank-2 Z_2 lattice T
with involution c, the Tate complex alternates c-1 and c+1. Its compact
Tate groups are killed by 2 and have F_2 dimension at most 2. For T/2^n,
the reduction sequence bounds each relevant Tate group by the two adjacent
compact Tate groups, so its dimension is at most 4, uniformly in n.
Only the single real place of Q occurs. Taking the finite Kummer quotients
in the exact sequence, and then compact/discrete limits, changes the
central displayed sequence only through subquotients of a fixed finite
number of these bounded real groups. Finite-level inverse systems satisfy
the required Mittag–Leffler condition, and direct limits are exact. This
gives a constant bound independent of S, h_0 and b. Ordinary real H^0 has
the rank-one contribution already isolated by the positive real-place
class a; the higher real defect groups remain finite. There is no growing
unidentified x2-killed global error. This closes the last integral-PT
obligation in the central calculation.

### One formula correcting all varying factors

Write gamma_c for the cyclotomic action of a smoothing integer c, and put
A_c^+=c^2-c gamma_c, A_c^-=c^2-c gamma_c^{-1}. Its tame action is trivial
by the stated CRT. Define B_c=gamma_c A_c^-. Then

    A_c^+ - B_c = c(c+1)(1-gamma_c),
    R_c = A_c^+/B_c in O^x,   R_c = 1 mod 2,   R_c(0)=1.

Both B_c and A_c^+ are O-units with the same central valuation e. The
identical construction applies to d. Inversion of a smoothing convention
therefore has no loss at (2), and no changed central valuation. The ratios
are taken in the genuine rational function field before the O extension;
their regular central evaluations exist because c(c-1) is nonzero.

For each varying good q let Z_q=theta_q gamma_q, with theta_q^2=1, and

    r_q=P_q(Z_q)/(Z_q^2 P_q(Z_q^{-1})),
    U_q=1+((r_q-1)/2)(1+g_q),
    V_Q=product_{q in Q} gamma_q^2.

Starting from an inverse-convention smoothed class z_raw^-, first multiply
it universally by

    gamma_c gamma_d V_Q (product_q U_q) R_c R_d,

and then divide by A_c^+ A_d^+. The resulting class is exactly

    z_new = V_Q (product_q U_q) z_raw^- / (A_c^- A_d^-).

Every multiplier preceding the division is an integral O[G] unit. The
two smoothing divisors are O[G] units; their combined central valuation
is 2e, independent of the support. At an unused character q, V_Q changes
P_q(Z_q^{-1}) to Z_q^2 P_q(Z_q^{-1}), and U_q changes this to P_q(Z_q).
At an active character it contributes just gamma_q^2, an A-unit with
central value 1. Consequently the displayed rational comparison and
divisibility hold with an extra group-like factor
product_{q active} gamma_q^2, absorbed in epsilon_h(t). All convention
units have central value 1. The fixed bad-support factors need only a fixed
finite set of analogous translations and the previously constructed F_E.
This supplies a formal universal repair for all smoothing and unused-Euler
factors, before character evaluation; it does not divide by 2 once per
prime, does not normalize by a character idempotent, and changes neither
C_int nor the central error constant.

### Family004's fixed support is legitimate

Family004's positive squarefree l satisfies l=3 mod 4. Hence l itself
has quadratic discriminant 4l and cannot simply be substituted as an
allowed odd discriminant h of the cyclotomic section with fixed E_1.
The actual application of Theorem 1.1 fixes **E=E_l first**, exactly as
`pointwise.tex:3` and its base h=1 assembly specify. This fixes N and all
its bad places before an internal binary cube grows. Internal h,h_0 are
then odd signed-prime discriminants supported outside 2N, or h=1. Thus
their characters have odd conductor and the CRT/unsmoothing argument
above applies. The primes of l are part of the fixed curve's bad support;
their constants may depend on E_l. The proof of a rational point for every
individual l requires no common constant across all Family004 l.

The integral model of E_1 has discriminant 2^8*3^2, so E_l has bad primes
only among 2,3 and the support of l; any further fixed auxiliary support
can be incorporated before the cube. Local squareclasses at these fixed
places and the real sign are fixed by the internal filter. All newly
varying primes are good and odd. E_l has j=35152/9 and full rational
two-torsion for every nonzero l, so the non-CM Kato rational hypotheses
and the split residual calculation both apply.

**Closing verdict:** the relevant non-CM cyclotomic construction, its
uniform fixed-form denominator, and its central formula are fully
reconstructed in the assigned use, with the explicit harmless convention
repair above. The external inputs are established fixed-form Kato rational
divisibility, cyclotomic nonvanishing, standard class-number/duality results,
and local exponential compatibility; their hypotheses were checked. No
equivalent unsupported uniformity claim replaces the conclusion. Separate
coefficient/ring-class/pointwise assembly validation remains outside this
agent's assigned result.

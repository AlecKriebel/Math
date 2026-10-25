# Independent source/scope derivation: 23395703

The literal theorem concerns every characteristic-zero field K, the four ambient partials of
Q=xy(x−y)(x−2y)zw(x+z+w), and degree reverse lexicographic gin B in the order x1>x2>x3>x4.
It asserts p=min{d:x2^d∈B}=8 and a degree-seven minimal generator in the first three variables divisible by x3.
This verifies the whole published conclusion; no complete gin or particular exponent vector is inferred.

For an injective binary or ternary restriction, write X,Y,Z,W for restricted coordinates, Li for the seven restricted factors,
ai for their ambient normal rows and fj for the restrictions of the four ambient partials. Require X,Y independent,
all Li nonzero and pairwise nonproportional, and, in the ternary case, X,Z,W independent.
If a tuple of homogeneous linear forms u satisfies Σujfj=0, reduction modulo Li leaves
(ai·u)∏h≠i Lh=0 in the integral domain R/(Li). All other factors have nonzero images, so ai·u=λiLi for a scalar λi.
Conversely those proportionalities give Σujfj=(Σλi)∏Li. Thus the relation space is exactly this scalar system with Σλi=0.
For a constant tuple the same divisibility forces every ai·u=0, and the coordinate-factor rows force u=0.
The four restricted degree-six polars are consequently linearly independent and minimal.

The factors X,Y,X−Y,X−2Y force ux=aX and uy=aY with the same a; put uz=bZ and uw=cW.
The last factor and trace condition become
(a−d)X+(b−d)Z+(c−d)W=0 and 4a+b+c+d=0.
Ternary independence forces a=b=c=d, hence 7a=0 and u=0 in characteristic zero.
It follows that H3(5)=21, H3(6)=28−4=24 and H3(7)=36−12=24.
In two variables the relation space among X,Z,W has dimension one since X,Z are nonproportional.
For a nonzero relation vector ρ, write a=d+tρx, b=d+tρz, c=d+tρw.
The trace is 7d+t(4ρx+ρz+ρw)=0, exactly one constraint even when the coefficient of t vanishes.
The map (d,t)↦u is injective: u=0 forces a=b=c=0, and then d(X+Z+W)=0 forces d=0 and t=0.
Thus there is exactly one binary linear syzygy, with no omitted exceptional trace subcase.

The binary ideal has no projective common zero over an algebraic closure. Restricted Euler gives Q=0 at such a point;
exactly one Li then vanishes because binary factors are distinct. The ambient gradient is ai∏h≠i Lh there and is nonzero,
a contradiction. Height two and finite length descend to K. The standard graded Hilbert–Burch theorem gives three minimal
syzygy coefficient degrees ej≥1 for four degree-six minimal generators. The Hilbert numerator is
N(t)=1−4t^6+Σt^(6+ej); finite length implies a double zero at1. The derivative condition gives Σej=6.
Exactly one degree-one syzygy and the other degrees at least two force {ej}={1,2,3}.
Therefore HS=(1−4t^6+t^7+t^8+t^9)/(1−t)^2 and (H2(6),H2(7),H2(8))=(3,1,0).
This is an application of a standard theorem, not a claim to have independently reread Burch's original complete proof.

Genericity is an analytic-algebraic proof step, not a property established by the finite replay.
The compatible ternary section (x,y,z,w)=(s,t,u,s+2t+3u), binary u=2s+3t, has factor rows
(1,0),(0,1),(1,−1),(1,−2),(2,3),(7,11),(10,14).
All 21 pair determinants are nonzero in characteristic zero. The triangular full basis
[[1,0,0,0],[0,1,0,0],[2,3,1,0],[7,11,3,1]] has determinant1 and its first two/three column spans give this flag.
The preceding arguments hold throughout the open set defined by these rank conditions.
Its nonempty lift to GL4 intersects the generic-initial open set by irreducibility; over infinite K the nonempty opens defined over K have K-points.
Thus these dimensions are generic over every field in scope. Galligo's standard theorem is credited; its relevant char0 interface was read in actual BPT Theorem4.4.

Conca Lemma1.2, whose full short proof was read, and BPT Theorem6.2 identify these functions with
Hilbert functions of K[x1,…,xr]/Br, Br=B∩K[x1,…,xr]. Strong stability of B implies that x2^7∈B would kill every binary degree-seven monomial,
contradicting H2(7)=1. H2(8)=0 gives x2^8∈B, and ideal closure excludes earlier powers, so p=8.
On A3=K[x1,x2,x3]/B3 the multiplication-by-x3 kernel at degree k has dimension H3(k−1)−H3(k)+H2(k).
This is zero at k6 and one at k7. There are no B elements below degree six.
The zero first kernel excludes any degree-six minimal generator of B3 involving x3.
A degree-six standard monomial m killed by x3 in the second kernel has a minimal generator v dividing x3m.
If v lacks x3 then it divides m, impossible. Its degree is therefore seven. A divisor of a first-three-variable monomial cannot involve x4,
so this v is minimal in full B as well. The proof uses the triangle calculation inside B3 and does not infer arbitrary later-variable generators from its row.

The exact package replay independently recomputes five matrix ranks 4,12,4,7,9 with exact nonzero minors and complete left kernels.
It also checks the displayed binary relation with scalar tuple (11,−73,25,4), whose trace is44−73+25+4=0,
and all signed maximal minors of the constructive Hilbert–Burch matrix. The unchanged orthogonal replay includes 21 binary Buchberger pairs,
specified-coordinate initial ideals and characteristic-seven/excluded-flag controls. These finite checks support the equations; the open-set argument supplies their generic meaning.

The original conjecture is exact: actual BPT Conjecture5.7 uses d0=min{d:x2^(d+1)∈B} and bound d0+1,
while actual OWR Conjecture7 uses the pure exponent p itself. Thus p8 with degree7 is a counterexample in both conventions.
The valid MPT three-variable theorem addresses the three derivatives of an arrangement in K3.
Our ternary section still has four ambient partials and is outside that theorem's hypotheses.
The arrangement is the classical parallel connection U2,4 and U3,4 along x (rank2+3−1=4), not a new arrangement.
The scalar mechanism is classical logarithmic derivation theory, with Tohaneanu's explicit Orlik–Terao credit preserved.

A fresh independent rational check of all35 triples of the seven normal rows finds only the four triples within the first pencil to have rank two;
all other triples have rank three. Hence exactly one multiplicity-four rank-two flat exists, and no hyperplane contains two high-multiplicity flats.
Actual Migliore–Nagel Section8.2 therefore applies with d7, one such flat, s3 and t4.
Its Corollary8.12 gives 0→S(−7)^3⊕S(−9)→S(−6)^5→Jtop→0.
This is substantive prior family information; Jtop has five minimal generators, whereas J has four. It cannot simply replace the J-section calculation.

No central gap was detected in the literal characteristic-zero theorem. No historical-firstness conclusion follows:
Ilardi2018's full body was not accessible, and original Galligo/Burch/Orlik–Terao bodies were not all read.
The manuscript itself disclaims historical novelty, independent discovery, a new construction, a full gin, a smallest count and positive-characteristic extension.
Those limits remain part of this review outcome.

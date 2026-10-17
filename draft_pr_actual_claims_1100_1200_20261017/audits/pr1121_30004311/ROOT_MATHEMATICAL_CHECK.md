# Parent mathematical assessment: PR1121 / problem 30004311

2026-10-17. In progress pending independent final reports and unchanged-code replays.
Original head: `f86b108ac1bc024302648eee9f47f74e26c810ec`.
Original proof SHA-256:
`68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75`.

## Exact target and source inspection

The parent read the entire frozen proof and substantive audit. The original
OWR51/2019 contribution was freshly retrieved from
<https://ems.press/content/serial-article-files/46831>. Its Problem 9 was visually
inspected on physical page 22, printed page 3228. The question concerns finite,
nontrivial, simple left braces whose multiplicative group is metabelian and has
abelian Sylow subgroups, and asks for an asymmetric product of two trivial braces.
The proposed example retains every condition. No queue entry is used as evidence
of its outcome or correctness.

The parent freshly retrieved and read the general normalized symmetric-cocycle
definition and lambda formula in arXiv:2001.08905v1, Theorem 2.2, and cross-checked
arXiv:1705.08493, Theorem 3.1. The former's physical page 3 was visually inspected.
Source bodies, extractions and renderings remain in ignored `sources/private/`;
only retrieval fingerprints are distributed. This is a mathematical definition
check, not the later current-priority audit.

## Universal construction checks

Work in the ideal R=x F5[x]/(x^5). Total degrees at least five vanish after any
substitution of elements of R. Truncated logarithm and exponential identities
through degree four have invertible denominators in characteristic five. The
parent independently encoded the polynomial identities over
F5[X,Y]/(all monomials of total degree at least five), rather than sampling ring
values. Both inverse identities, the circle-to-additive identity, and the
exponential product identity hold. The fourth logarithm coefficient has precisely
the stated coefficients. Normal and optimized runs agree; see
`root_reproduction/SYMBOLIC_RESULTS.json`. This does not replace the remaining
group, simplicity or exclusion arguments.

For the even-weight subspace V of F2^5, the dot form's radical is the intersection
with the constant-vector space, which is zero. The weight-half quadratic form
polarizes to that dot form. Rotation preserves both; its only fixed vector in V
is zero, so M-id is invertible. The independent parent bitmask control checks all
16 vectors and 256 ordered pairs, as well as bijectivity of M-id.

In logarithmic coordinates the circle law is exactly
((k,e),(v,s)) ((h,f),(w,t)) =
((k+tau^e h,e+f),(v+M^s w,s+t)). The fourth logarithm coefficient is fixed by
reflection. The quadratic correction to e cancels the binary bilinear term.
This proves associativity by a bijection with two genuine semidirect products;
no associativity inference is drawn from generator tests alone.

The lambda formula is an invertible F5-linear ring block and an invertible
F2-linear triangular block. Consequently the independently established circle
group and componentwise abelian addition satisfy the left-brace identity on all
inputs. The group is metabelian, with derived image ranks two and four, and hence
derived order 5^2*2^4=400. Explicit Sylow groups have orders 625 and 32 and are
abelian; conjugacy covers all Sylow groups without assuming normality.

## All-ideal argument

For a genuine ideal I, lambda_a(i)-i and i*a belong to I. The second inference is
justified in the quotient brace, rather than being assumed for arbitrary left
ideals. An additive multiple isolates a nonzero primary component of any nonzero
seed. A ring seed's lowest coefficient produces x^4 by multiplication by an
appropriate monomial, then nonzero scalar rescaling. A nonzero binary vector
produces the last-coordinate bit through nondegeneracy; a pure nonzero bit is
already that bit. This treats mixed seeds and does not assume a coordinate ideal.

The bit stars x to 3x. The element x^4 stars binary vectors onto (M-id)V=V.
Thus either primary seed gives both primary generators. Multiplication by x
then produces every remaining ring monomial. The resulting nine additive basis
vectors generate all of B. Every inference is legitimate ideal closure, so every
nonzero ideal equals B. Nontriviality follows from x*x=x^2.

## Universal two-trivial-factor obstruction

Start with an arbitrary admissible normalized symmetric 2-cocycle, without
assuming bilinearity. For trivial factors,
lambda_(t,0)(w,z)=(w,z-b(w,t)). Multiplicative lambda composition at (t,0),(u,0)
forces b(w,t+u)=b(w,t)+b(w,u); symmetry gives biadditivity. This is a necessary
brace-law consequence, so it covers the entire inspected source definition.

Mixed-primary bilinear values vanish and p-primary values stay p-primary.
The set T_p x S_p is therefore both the additive Sylow group (possibly with
twisted addition and increased exponent) and a multiplicative Sylow group. Its
assumed multiplicative commutativity forces alpha_(S_p) to fix T_p pointwise.
Careful twisted subtraction gives a*b=(0,-b(u,t)) inside this primary subbrace.
Every such output has identity lambda action on the same subbrace. Hence all
(a*b)*c vanish there. This uses no simplicity and no classification of factor
orders. Brace isomorphisms preserve the primary subgroups and both stars.

In the proposed example P5 is precisely the radical-ring brace; (x*x)*x=x^3
is nonzero. Thus every two-trivial-factor presentation is excluded, not merely
one known family or one coordinate choice.

## Redundant intrinsic checks

The direct group decomposition gives center order five and abelianization
order fifty. The global lambda-fixed set is F5 x^4 x {0} x F2, of order ten.
The stated explicit commutator has logarithm x, and multiplying its exponential
by x and then by x gives the displayed nonzero polynomial.

The separate comparison with simple two-trivial-factor products is sound:
rad(b) x {0} is a proper ideal, so simplicity kills the radical. If H is generated
by alpha_s(t)-t, then H x S is a nonzero ideal, forcing H=T. Thus the derived
group is T x {0}, while the lambda-fixed group is {0} x S, giving a complement.
The ideal {0} x ker(alpha) forces faithfulness. A central element then has zero
S-coordinate and an invariant T-coordinate; orthogonality annihilates its
pairings with H=T, forcing it into the zero radical. These arguments concern
this construction class only, rather than arbitrary simple braces.

## Outstanding gate

No mathematical defect identified by the parent. Independent final family
reports and fingerprinted unchanged-program replays remain required before
promoting this to mathematical acceptance. Current historical novelty is not
asserted and has not yet passed the fresh extensive priority gate.

# Additive boundary checks after first seal

2026-10-12 UTC. The first assessment and first inventory remain unchanged.
Family completion estimate: 95%. No original verifier or other scientific
family report has been read. ROOT requested these two additional boundary
checks after personally reading the sealed first assessment.

## Integer-valued finite-type ring

Let V_Z be the unital ring of integer-valued finite-type invariants, with the
usual Z-linear singular extension. For v in V_Z of order at most d, all values
a_n=v(L_n) and differences Delta^r a_0 are integers. The same singular immersion
therefore gives Delta^(d+1)a_n=0. Its Newton polynomial is

    P_v(t)=sum_(r=0)^d Delta^r a_0 * t(t-1)...(t-r+1)/r!.

The coefficients are rational; they need not be integers. P_v is nevertheless
in Q[t], and agrees with a_n at every n>=0. In particular integer-valued basis
functions C(n,r) have rational polynomials C(t,r). Larger admissible orders give
the same polynomial because uniqueness holds over Q. Additivity, unitality,
and multiplicativity again follow from equality at infinitely many integers;
the product lies in V_Z because its values are integers and its order is at
most the sum of the factors' orders. Thus P:V_Z -> Q[t] is a ring homomorphism,
and chi(v)=P_v(1/2) is a unital ring homomorphism V_Z -> Q. It is not asserted
to have values in Z; for example the linking number maps to 1/2 in the
two-component coherently oriented setting.

The invariant g is integer-valued and order at most two; f=4g^2-g is likewise
integer-valued and finite type. Suppose g belongs to radical(f V_Z). By the
definition of radical, for some N>=1 and h in V_Z, g^N=fh. Mapping this equality
to Q gives (1/4)^N=0*chi(h)=0, impossible because Q is an integral domain of
characteristic zero. A homomorphism to Q suffices; the coefficient ring of
the domain need not equal the target ring. Equivalently ker(chi) is a prime
ideal containing fV_Z, hence contains its radical, but it does not contain g.
There is no denominator-clearing requirement in the domain and no extension
of ideal membership from V_Z to a larger ring is being assumed.

The auxiliary integer-valued claim is therefore valid under the same ordinary
finite-order model. On an unoriented/unnamed link domain g and f still descend;
their nonzero/zero character values prove the radical statement even when an
individual named oriented linking number is not an element of that domain.

## All component counts and order-zero idempotents

For each allowed component count k, let e_k(L) be 1 when L has k components
and 0 otherwise. Crossing changes preserve the immersed domain circles, so
e_k is order zero. It satisfies e_k^2=e_k and e_k e_l=0 for k!=l. More generally
any function H of the component count is an order-zero invariant, with no
polynomial restriction on H itself.

The family used to construct the character stays in one component count m:
m=2 on the all-link domain, or the prescribed m on a fixed-count domain.
Restriction to that count is a unital algebra homomorphism, followed by the
polynomial restriction map already proved. Thus

    P_(e_k)(t)=1 if k=m, and 0 otherwise;
    chi(e_k)=delta_(k,m);   chi(H(component count))=H(m).

These values respect both idempotency and orthogonality. The map kills every
invariant supported only at counts other than m, even if that invariant has a
large finite order; this is legitimate projection onto the m-component sector.
For an arbitrary v of global finite order d, restricting v to this sector
preserves the same upper bound d, so Newton interpolation still works. No
single order bound for all v is required. The previously proved uniform bounds
for g and f ensure that they themselves belong to the global algebra.

Although pointwise one can describe 1 as the sum over all e_k, this is an
infinite pointwise sum. The algebra operations used here are finite addition
and multiplication; an algebra homomorphism is not required to preserve
arbitrary infinite sums. More directly, the explicit evaluation-at-m rule
already maps the constant function 1 to 1 and all products correctly. There is
no topological completion or infinite-series argument involved. Component-count
idempotents therefore create no obstruction to the whole-algebra character.

## Explicit source and historical qualifications

The complete rendered/extracted printed p.398 is about **oriented knots**.
Applying its identical local positive-minus-negative rule to an immersion of a
finite disjoint union of oriented circles is the ordinary link convention
adopted for this proof. Printed p.422 explicitly asks about finite-type
invariants of links. This distinction should remain explicit in publication.

The complete one-page author question displays a June 2001 posting label and
a July 2011 notebook date. Its body agrees with the printed arbitrary-ideal
question and separately presents the linking-number-generator example. These
facts establish source formulation only. They establish neither novelty nor a
current literature status, and this audit did not read the referenced paper
bodies. No completion/framing variant has been audited here.

## Additional executable falsification

For the geometric crossing units in the first assessment, their y-displacement
may be replaced by a bump supported in an arbitrarily small neighborhood of
t=1/2. The x-coordinates coincide only at t=1/2, so this replacement is an
isotopy of each resolved pair relative to endpoints and causes no additional
intersection. Thus the two opposite e-values represent genuinely local
resolutions of the unique double point, as required by the finite-type rule.

The independently authored `adversarial_mutation_harness.py` replays actual
changed braid compilation mechanisms against endpoint, closure, RII, linking,
and self-writhe acceptance checks. Its baseline passes 90 diagram cases. Five
mechanism mutants are rejected with explicit first failing diagrams: deleted
companion, smoothing a negative branch, odd prefix, mistranscribed resolution
sign, and a single shared physical singular site. This adds executable mutant
replays to the direct false-claim witnesses retained in the first seal.

Both normal Python and Python -O produce the same outcomes. A separate exact
product check covers all 1,024 pairs of Boolean monomials on a five-site cube
and a non-monomial rational example, including overlap reduction x_a^2=x_a.
The fourth forward difference of f(L_n)=4n^4-n^2 is exactly 96, so the controls
would detect an erroneous order-at-most-three assertion along this family.

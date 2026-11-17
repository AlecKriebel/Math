# Exact imported EGH mechanism: independent written audit

This is a written proof review of a recent, unrefereed new claim. It supplies
no formal or conventional human-refereeing certificate. No source program,
scientific test, finite certificate or historical AI audit was used as proof.
All cited local EGH files are genuine complete GitHub-connector responses at
adc7f1241b42e322a6451854ab7e4b4c146bf78a. Their full saved bodies were read.
PRIMARY_PROVENANCE.json supplies exact URLs, Git blob IDs and SHA256 values.
The actual entrypoint and nine sections total3219lines/141816bytes; bibliography
was retrieved and read separately. No large upstream PDF was downloaded.

## 1. Imported statement and exact minimal scope

01-introduction.tex:33,65,93 contains respectively Theorem1.1, Corollary1.2 and
Corollary1.3. The construction is for a FULL complex regular sequence, n>=1,
sorted degrees>=2. It produces a finite-dimensional CENTRAL DIVISION algebra
Delta over a finitely generated extension k/C and pairwise commuting linear
forms t_i, with full ordered left-Delta basis before quotienting, and rows

    t_i^a_i = c_i f_i + sum_(l<i) B_il f_l + sum_(d>i) C_id t_d,
    c_i !=0, deg B_il=a_i-a_l, deg C_id=a_i-1.

Corollary1.2 gives ONE monomial ideal containing every corresponding pure power,
matching every quotient Hilbert dimension for EVERY homogeneous containing
ideal. Its further generators are unrestricted. That is precisely the premise
needed for each preimage of AV. The native note can use this full-length complex
case and its own coefficient-field descent; it need not rely on the stronger
arbitrary-length reduction or companion Betti inequalities. Corollary1.3 has
the claimed characteristic-zero quantifiers, but is not a substitute for its
construction proof. Degree1 and n=0 are outside that construction and handled
directly in the native note.

## 2. Ordered basis and ONE monomial ideal (02-reduction.tex)

Let N=Delta[x] as a right module over the commutative algebra A of the forms.
It is free over central k[x], and A is a k[x]-submodule of this finite module,
so A is finite over k[x]. The triangular rows imply A/(t_1,...,t_n) has dimension
zero: read rows in increasing i when all t vanish to force all f, hence all x,
to vanish. Positive grading and finiteness exclude another projective fiber.

At A_+, the central x_i are an N-regular sequence of length n with nonzero
quotient Delta. Thus N has depth/support dimension n there. The actual CM
system-of-parameters assertion applies to the t_i; Stacks00N6 was read at its
primary page, including its dimension-drop hypothesis and proof. Homogeneous
kernels survive localization because a multiplier with nonzero constant term
cannot kill their lowest component. Therefore the t_i are globally regular on
the graded module. Their degrees are1; Hilbert series now makes N/(Nt_i) purely
degree0, equal to Delta. Degree induction gives spanning by t^alpha, and the
degree-d count binomial(n+d-1,n-1) gives independence.

For a homogeneous I, Delta I is two-sided because its original coefficients
and variables are central. Within each FINITE homogeneous piece, division-
algebra elimination counts least exponents in the reversed coordinate order
alpha_n,...,alpha_1. Right multiplication by t_j translates all exponents,
so their collection E is upward closed. A row places a_i e_i in E because
every C_id t_d term has a positive coordinate of index greater than i. Thus
E defines one ordinary monomial ideal containing all pure powers. The quotient
left-Delta dimension is dim_C(S/I)_d by scalar extension. No equality of ideal
generator counts and no coefficientwise commutation with Delta is presumed.

## 3. Low-degree relations and generic initial division data (03)

The induction retains ALL old rows as consequences of an ideal Q generated in
degrees1,2. This matters when a later row has lower degree. The stage ideal
j=(Q,f_l for l<=i,t_d for d>i) has a base-point-free degree-b part: all named
generator degrees are<=b, and the old rows force the remaining f to vanish at
a purported common zero. Its annihilator W is a space of degree-b functions
on formal forms U, through w_lambda(ell)=lambda(ell^b).

The simple-factor lemma addresses EVERY nonzero geometric member of W, not
just a basis. Annihilation of Q_b gives q(partial)w=0. For a repeated irreducible
factor p^r, its lowest p-adic derivative terms put the projective gradient of p
in V_+(Q). A nonconstant gradient, restricted to a suitable plane-section
curve, produces an image curve of degree<=deg(p)(deg(p)-1). The prescribed
no-small-curve condition excludes this, so repeated factors must be linear.
If all factors were repeated, logarithmic differentiation instead puts the
AMBIENT gradient of w in V_+(Q). Restriction to a varying line produces another
forbidden curve. A constant gradient makes w a pure power, contradicting the
base-point-free stage ideal. Characteristic zero is used in derivatives and
pure-power spanning; the proof never silently extends this to positive char.

Initial data use rows of anticommuting Laurent variables, with distinct rows
commuting. Ordered Laurent leading terms give a domain; adjoining central
squares gives a finite-dimensional domain over its center, hence division.
Even row length makes the only central parity vector zero. Generic square
relations s_rho^2=q_rho(x) yield a finite formal cover. The Chow-form coefficient
bound limits the field-of-definition transcendence degree of any bounded-degree
curve. Retaining whole coefficient blocks loses at most that many blocks.
Their generic quadric divisors on the curve are reduced, disjoint and nonempty;
odd valuations give independent squareclasses. A degree<=D cover cannot contain
2^(m-d_*) such independent roots when m was chosen larger. This proves the
no-small-curve condition; finite graded enlargement preserves it by the degree
formula for finite maps of projective curves. No genericity of the ORIGINAL
regular sequence was imposed, only of auxiliary square parameters.

## 4. Parameter geometry, homology and homotopy (04)

One simple factor makes w^(-1)(1) connected by cyclic-cover meridian monodromy.
The two-half-plane open cover of f+g=1 gives a homotopy pushout of the two
projections of f^(-1)(1) times g^(-1)(1), hence a join. The half-plane factors
contract by positive radial scaling; their intersection is a strip where both
roots are continuous. Thus M blocks have integral reduced homology zero through
2M-2. This is not an isolated-singularity assumption.

For s=dim W,r=dim U,N=Mr, defective Jacobian rank has dimension<=N-M+s-1.
Every component of Y has dimension>=N-s, and M>2s-1 forces a generically full
Jacobian on each component. Height s, CM and generic smoothness give a reduced
complete intersection. The omitted singular cone has complex codimension
c=M-2s+1. The construction then proves connectedness, rather than assuming it.

The complement incidence H over C^N minus Y has affine-space fibers of rank
s-1. Its map to O_(P(W))(1)^times has fibers the nonzero levels above. This
map is NOT assumed proper or locally trivial. Proper-support stalks, compact-
support duality and the complex orientation give a constant top direct image
in degree q=2N-2 and a2M-2 gap below it. Base real dimension2s and2M>2s make
the compact-support Leray comparison H_j(H)=H_j(S^(2s-1)) valid in the required
range. The closed/open sequence transfers this to high compact-support degrees
on Y. Removing its singular part is allowed because

    kappa=M+2h <=2c-2=2M-4s,
    2s+kappa-1 <=2M-2,

both ensured by M>=2h+4s+10. Duality on Y^o gives integral homology vanishing
through kappa. The separate fundamental-group step is necessary.

The actual Hamm-Le1985 Theorem1.1.3(ii), printedp126, was checked in the
primary Numdam text. It applies to projective X with deleted algebraic Z when
X minus Z is smooth, and sufficiently general hyperplanes. Here Z=Sing X.
Iterating its cell attachment statement reaches a surface avoiding Z because
codim Z>h>=2. A smooth complete-intersection surface is simply connected by
projective Lefschetz. Thus pi_1(X_sm)=0. The circle bundle for O(-1) makes
pi_1(Y^o) abelian, and H_1=0 kills it. Hurewicz then upgrades the homology
vanishing to kappa-connectivity. This checks the exact smooth-open interface,
rather than applying a smooth-projective theorem directly to singular X.

## 5. Binary curves and Picard inputs (05)

The Kummer cover of the s-line has independent valuation-one classes, including
composite b. Its cyclic extension to t=s^b gives G of order e=b^b, with only
0,1,infinity branched of index b. The auxiliary degree-b cover, additionally
branched at2, is linearly disjoint: every nontrivial common intermediate of
that cyclic cover would ramify at2. After normalization, tame local roots
cancel ramification at the first three points, giving an etale G-cover C/T0.
Riemann-Hurwitz gives g_T=b-1 and g_C-1=e(g_T-1).

L is genuinely G-linearized in degree b because the diagonal scalar subgroup
acts trivially there. Its degree is e. The displayed monomial sections give
z^b=u^b+v^b and a base-point-free pencil u,v. Generic A in Pic^0 makes
A L^(g_T-1) noneffective of degree g_C-1. Its H^0,H^1 both vanish. Therefore
pi_*(A L^g_T)(-1) has no cohomology and its untwisted evaluation at every point
is an isomorphism: pi_*(A L^g_T) is a TRIVIAL rank-e bundle. Multiplication
then produces commuting linear matrix polynomials, not commuting individual
coefficient matrices. Scalar ambiguity cancels on endomorphisms.

Pic^1 is free under G: a fixed degree-one line for a cyclic subgroup can be
linearized after rescaling, would descend along its etale quotient, and would
have degree divisible by that subgroup order. Character maps Pic^1 to S^1 are
constructed by lifting the character class to integral H^1(T0), dividing its
pullback by b on C, and extending the resulting integral harmonic class via
the Abel/Jacobian integral H^1 identification. Thus both freeness and the
characters used below have actual proofs, not a Picard-variety headline.

## 6. Coherent descent and the old division algebra (06)

With B=product Pic^0, H=G^(M-1), K=k(B times X times faithful R), F=K^H,
the action is faithful and K/F is Galois. End(E) descends as an algebra by
actual semilinear group transport; Stacks0CDR states the exact cocycle descent
interface. Central simplicity is NOT confused with division.

An arbitrary right Delta-module of reduced rank r becomes a twisted coherent
Delta0-module of generic dimension e0*r. A finite orbit-sum inside rational
sections extends it across the parameter scheme with the required Hom-line
transport. Adding Pic^1 factors P permits the determinant correction D. Its
weights in the universal degree-zero/degree-one lines are(-1,0), so it cancels
the scalar cocycle genuinely. Derived restriction to R=0 preserves a coherent
class beta and its generic rank; no flatness over R is assumed.

After a complex embedding, old Delta0 splits, and a primitive fixed matrix
idempotent reduces beta to beta'. It divides every rank by e0 and preserves
H-equivariance because H fixes Delta0 pointwise. Normalized universal classes
give c1(D) purely mixed between B and P, with UNIMODULAR integral matrix from
the curve intersection pairing. Its top exponential integrates to plus/minus1.
Any positive-degree ch(gamma) from B then has too much B-degree, so the fiber
Euler integral is exactly plus/minus r, not an unnoticed polarisation multiple.

Before this base change, freeness on P makes the full quotient a projective
finite-etale H-torsor. Its descended cohomology carries the division algebra
Delta0, hence dimensions divisible by e0^2. The torsor Euler lemma is valid
even for singular X: the virtual rank-zero bundle d=[delta_*O]-|H| lowers
support dimension on G0, so is nilpotent as an operator; projection formula
gives(|H|+d)d=0. Rational inversion kills d, and integral Euler characteristic
kills torsion. Thus every twist chi(beta(l))/e0 is divisible by e0*e1.
Division of Delta0 is not inferred from its complex specialization.

## 7. Integral K-theory and noncircular division proof (07)

The unit cone is(M+2h)-connected. Cell-by-cell section extension over
(T/H') times P^h, of real dimension M+2h, gives the needed H' times S^1
equivariant lift. The homotopy between this lift and a constant-T lift uses
one higher cell dimension but only pi_(M+2h), which also vanishes. Pic^1
character maps supply P to T. Thus beta' pulls to an equivariant class on
Z times P^h that descends to V=Z/H times P^h.

Integral topological pushforward has values in K^0(P^h)=Z[u]/u^(h+1),
u=1-[O(-1)]. The primary Hatcher2.24 and2.25 statements were checked, including
the compactness/freeness hypotheses; the products used here are smooth
projective/compact with projective-space even-cell fibers. The explicit normal
Thom convention in the new proof has Chern character td(normal)^(-1), so the
pushforward is genuinely integral, not merely a rational RR formula. Etale
degree e1 makes every coefficient q_j divisible by e1, and q_0=plus/minus r.

A smooth h-dimensional linear section D0 avoids Sing X. Its inclusion and
the projective test map have homotopic circle lifts with the SAME tautological
line; this retains the q_j after restriction. The hyperplane Koszul complex
expresses every Euler twist on D0 as an integral finite difference of the
original twists on X. Hence sum q_j*chi_D0(u^j O(l)) is divisible by e0*e1.

Write Q_*(u)=sum(q_j/e1)u^j. The Hilbert series of D0 converts these integer
twist divisibilities into

    A_b(u)^s Q_*(u)=0 mod(e0,u^(h+1)),
    A_b(u)=(1-(1-u)^b)/u.

For p^v exactly dividing e0, the order of A_b^s mod p is
nu=s(p^(v_p(b))-1). The proved truncation lemma successively divides the
low-degree part of Q_* by p, losing at most nu degrees each time. h>=v*nu
therefore forces p^v|Q_*(0). It includes nu=0, composite b, and s=0.
All primes give e0*e1|r, excluding a nonzero proper right ideal and proving
division. h depends on OLD e0,s,b, then M is chosen, then e1 grows with M.
There is no self-referential requirement that h dominate the NEW e1.

## 8. Invariant assembly and preservation (08)

The generic O_X(1) line has a NONZERO invariant generator tau by Galois
descent. Dividing coordinate sections by tau turns the inverse point phase
into the desired coefficient character; its sign is checked against the
matrix-transport equation. The recursive lambda/eta weights make the final
output invariant. Old forms and Delta0 remain fixed.

For each binary link, new coefficient matrices centralize the old algebra
and earlier tensor factors. Inputs commute as WHOLE forms, giving a valid
substitution homomorphism and commutation of all outputs, without demanding
individual coefficient commutativity within a link. Degree-b monomial symbols
satisfy the Veronese pair exchanges and linear diagonal/input relations.
Unit-exchange proves T_alpha^b=product D_j^alpha_j; z is integral by
z^b=u^b+v^b, so the new relation algebra is finite and still defined in
degrees1,2. Telescoping gives t_i^b=sum ell_m^b.

The f_i coefficient is generically NONZERO: if it is not absorbable into the
other stage terms, pure-power spanning produces a cone point whose sum is
exactly f_i, using M>=dim Sym^b U. Integrality of X makes this coefficient
nonzero generically. Invariant linear algebra descends the coefficients.
Semilinear descent of the full degree1,2 pieces recovers the whole stable ideal,
and faithful flatness descends finiteness. Finite projection preserves the
no-small-curve condition. This closes the induction in n,n-1,...,1, retaining
earlier higher-degree rows. Section02 then extracts the exact Artinian EGH
premise. The full-length field passage in09 is the finite coefficient-field
argument independently checked in the sealed INITIAL.

## 9. Written-review conclusion and limits

The central imported proof was examined substantively through all these
interfaces. No unsupported central inference or in-scope counterexample was
established. The exact Artinian EGH input is accepted for this written review;
it is not independently certified by finite examples, a formal build, an old
AI audit, a release announcement or conventional refereeing. The target note
is an attributed consequence of this recent input and the known reduction.
No companion Betti, unrelated EGH consequence, novelty or Lefschetz claim is
inferred. No native reproduction was run because it would only illustrate
Hilbert coefficients, not test this universal proof.

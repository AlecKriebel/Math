# Independent INITIAL reconstruction: original controlling manuscript only

Recorded 2026-11-17 UTC. Lane: scope-sol. Inventory row 188; native record
23203270. This is an initial scientific work product, not a final disposition.
The target conclusion is a hypothesis under examination. No packaged audit,
certificate result, supplementary mathematical body, native scientific program,
or other review family's findings was read before this record was frozen.

## Source identity and exact reading boundary

The controlling published outer asset is `sources/zenodo-files/paper.pdf`,
74,424 bytes, SHA256
`c579ec3442f4bcdf68ed737ad8bc65328682158845ed2e14e6636b2b119f52c6`.
It has six pages. All extracted text, including references and disclosures,
was read; all six fresh 110 dpi Poppler page images were personally viewed.
The complete corresponding `main.tex` was read: 362 lines, 16,724 bytes,
SHA256 `0950f3488e6b59b3ca68e066468fc49b99838be42f1ff8ff5fd6afef9fd04d6b`.
No TeX compilation or scientific execution was performed.

The original namespace was authenticated independently by reading and hashing
its bytes and topology, including hidden entries and modes. It has 97 files
and 12 child directories. The source manifest accounts for 95 payload files
and 13 directories including its root; its only excluded controls are itself
and SOURCE_FINAL.json. All original payload records match the actual objects.
All 87 native ZIP members match their extracted file bytes. There are no
embedded PDFs. The original sources were not modified.

Full native API metadata and the captured native record page text were read,
including the entire Description. The native publication date is 2026-10-06;
creation 2026-10-07T04:54:17.591002+00:00; modification
2026-10-10T21:27:07.249789+00:00. The API metadata has **no `version` field**.
The captured HTML page displays `Version v1`, and the API relation has a
version index 0; neither is silently substituted for a supplied native version
field. DOI 10.5281/zenodo.23203270, concept DOI 10.5281/zenodo.23203269.
Creator Alec Kriebel, ORCID 0009-0001-9320-500X; open preprint, English,
CC BY 4.0. Native asset order: source-and-verification.zip, paper.pdf.
The Description asserts the explicit split maps and nonpolynomial image,
attributes the cancellation/nonpolynomiality inputs to OpenAI, leaves the
four-variable question unsettled, and expressly disclaims a reproduced full
kernel build and formal verification of the follow-on theorem. Those are
metadata assertions to check, not independent evidence of correctness.

Custody checks are documented in SOURCE_AUTHENTICATION.json. The root
source-only adoption was used only for the supplied custody pin; its status
does not supply a scientific finding.

## Exact target claims and success criteria

Work over the field k = C, with all maps unital k-algebra homomorphisms. Let

    P = k[p,s,u,F,J],  x = s^2+u^3+p^2 F,
    H = x^2 F-(1+2sx)J-p^2 J^2-pu,  A = P/(H),
    B = k[p,s,u,m,e].

The full target is the conjunction of the following claims, with the displayed
H, variable names, and base field fixed:

1. A is a smooth integral finitely generated complex algebra with
   transcendence degree four.
2. The manuscript's denominator-free polynomials actually specify maps
   i:A -> B and r:B -> A with r composed with i equal to identity on A.
3. The five specified component polynomials are the images of B's generators
   under rho = i composed with r. Thus rho is an idempotent k-algebra
   endomorphism, and its image algebra is i(A).
4. A is not isomorphic as a complex algebra to k[t1,t2,t3,t4]. With claim 1,
   this excludes a polynomial algebra in any finite number of variables.
5. Contravariantly, the same component tuple gives an idempotent morphism
   of affine five-space with closed scheme-theoretic image isomorphic to
   Spec A.

Claims 1-3 and 5 are susceptible to explicit algebraic proof using the original
formulas alone. Claim 4 is an essential external mathematical input; it does
not follow from finding a split map, checking identities, smoothness, or
dimension. A final disposition requires checking that input at the exact
presentation and its assumptions. Verifying only a conditional transport is
not a substitute for the target conclusion. Historical/priority statements,
formal-verification statements, and four-variable limits are separate claims
whose evidentiary requirements are listed below.

## Reconstruction I: the domain, dimension, and smoothness arguments

This argument avoids dependence on cancellation or nonpolynomiality.
Localize P at p. Introduce

    y = s+x(x-u^3),  z = sx+p^2 J.

The inverse coordinate formulas are

    s = y-x(x-u^3),
    F = p^(-2)(x-s^2-u^3),
    J = p^(-2)(z-sx).

Therefore P[p^(-1)] is the polynomial ring
k[p,p^(-1),x,y,z,u]. Expanding without using H gives

    xy-z(z+1) = p^2[x^2 F-(1+2sx)J-p^2 J^2],
    H = p^(-2)[xy-z(z+1)]-pu.

The coefficient -p of u is a unit in the localized coefficient ring.
Consequently the localized quotient is
k[p,p^(-1),x,y,z], and H is prime and irreducible after localization.
In the UFD P, an element that becomes a unit upon inverting p is a
constant times a nonnegative power of p. But H modulo p is the nonzero
polynomial

    L = (s^2+u^3)^2 F-[1+2s(s^2+u^3)]J.

Thus p does not divide H. Any nontrivial factorization of H in P would
remain nontrivial after localization, a contradiction. H is irreducible
and prime in P, so A is a domain. Also the image of p in A is nonzero:
H cannot divide p in this UFD. Its localization embeds in the same fraction
field as A, giving transcendence degree four. This justifies the later
p-cancellation step without assuming the cylinder inverse or an external
nonpolynomiality theorem.

For smoothness, the open subset p != 0 is the Laurent polynomial
presentation above. On p = 0 put x0=s^2+u^3. The partial derivatives of
H with respect to F and J become x0^2 and -(1+2sx0). The polynomial
identity

    4s^2*x0^2 + (1-2sx0)(1+2sx0) = 1

shows those two derivatives generate the unit ideal there. This covers all
points of the remaining fiber. The characteristic-zero hypersurface
Jacobian criterion gives smoothness. No restriction x0 != 0 or s != 0 is
being inserted.

## Reconstruction II: the polynomial shear and quotient direction

Define a derivation Delta on P by

    Delta(p)=0, Delta(u)=-p^2, Delta(s)=-3p^2*x*u^2,
    Delta(F)=(6sx+3)u^2, Delta(J)=3x^2*u^2.

In the localized coordinates just established, this is -p^2 partial_u
with p,x,y,z fixed. Computing from the inverse formulas recovers exactly
the displayed values, so it preserves P. Each polynomial is killed by a
sufficiently high power in the localization; injectivity P -> P[p^(-1)]
then gives local nilpotence on P. This is a valid way to descend local
nilpotence; merely knowing a derivation preserves a subring would not
alone suffice without nilpotence in the localization.

Since H = p^(-2)[xy-z(z+1)]-pu, Delta(H)=p^3 and Delta^2(H)=0.
Extend Delta by Delta(w)=0. The finite exponential Phi=exp(w Delta)
is an automorphism of P[w] with inverse exp(-w Delta). From the fixed x
and the shift u -> u-p^2 w, let

    D_w = [(u-p^2 w)^3-u^3]/p^2
        = -3u^2 w+3p^2 u w^2-p^4 w^3.

Here the first notation is an identity used to derive the polynomial;
the second is its actual definition at p=0. The fixed y,z and x imply

    Phi(s) = s+p^2 x D_w,
    Phi(F) = F-(1+2sx)D_w-p^2 x^2 D_w^2,
    Phi(J) = J-x^2 D_w.

For example, the F formula follows by expanding
x = Phi(s)^2+Phi(u)^3+p^2 Phi(F); its apparent division cancels
term by term as a polynomial identity in P[w]. Thus Phi(H)=H+p^3 w.
This direction matters: Phi sends the ideal (H) to (H+p^3 w), so it
induces an isomorphism

    barPhi: A[w] -> T=P[w]/(H+p^3 w),

not an unqualified endomorphism of A[w] fixing its defining equation.
The earlier domain proof makes T a domain via this isomorphism, before
any appeal to g or q below. Its element p is nonzero.

## Reconstruction III: a denominator-free coordinate e0

Set x0=s^2+u^3, and use the original L and

    M = (1-2sx0)F+4s^2 J.

The determinant of the map (F,J) -> (L,M) is
4s^2*x0^2+(1+2sx0)(1-2sx0)=1. Hence this is an automorphism over
k[p,s,u], with inverse

    f(L) = a0 L+b0 M,  j(L)=c0 L+d0 M,
    a0=4s^2, b0=1+2sx0, c0=2sx0-1, d0=x0^2.

Define Q(L)=2x0 f(L)^2-2s f(L)j(L)-j(L)^2. Expanding its three
coefficients gives

    C = Q(0)=M^2(2x0+6s*x0^2+4s^2*x0^3-x0^4),
    q1=M[4x0*a0*b0-2s(a0*d0+b0*c0)-2c0*d0],
    q2=2x0*a0^2-2s*a0*c0-c0^2,
    Q1(L)=q1+q2 L,  Q(L)=C+L Q1(L).

This checks the Q1 specification without dividing by L or M.
Expanding x=x0+p^2 F in H yields

    H(L) = L-pu+p^2 Q(L)+p^4 f(L)^3.

Write t=H(L)+p^3 w and

    Lstar=pu-p^2 C,
    h=u-p Q(L)-p^3 f(L)^3-p^2 w,
    e0=-w-p f(L)^3-Q1(L)h.

Two short derivations are useful instead of assuming supplied
certificates. First t=L-ph, directly from the definition of h. Next

    t=(L-Lstar)+p^2 L Q1(L)+p^4 f(L)^3+p^3 w.

Therefore

    p^3 e0-(L-Lstar)
      =-t+p^2 Q1(L)(L-ph)
      =(p^2 Q1(L)-1)t.

In T this proves L=Lstar+p^3 e0 with no localization. Substitution
L=Lstar into H also gives

    H(Lstar)=p^3[(u-pC)Q1(Lstar)+p f(Lstar)^3],

because Lstar=p(u-pC). This proves the root divisibility identity
independently and identifies why p^3, rather than only p^2, appears.

## Reconstruction IV: both inverse compositions

In B replace M by m, then define

    ell=pu-p^2 C+p^3 e = p(u-pC+p^2 e),
    f=f(ell), j=j(ell),
    W=-e-(u-pC+p^2 e)Q1(ell)-p f^3.

The expansion of t above gives t(ell,W)=0 term by term, so the proposed
g:T -> B is well defined on the quotient when it sends
(p,s,u,F,J,w) to (p,s,u,f,j,W). The map q:B -> T is the free polynomial
algebra map sending (p,s,u,m,e) to (p,s,u,M,e0).

For gq, the determinant-one inverse recovers m from f,j. Set
v0=u-pC+p^2 e. Directly substituting ell=pv0 and W into h gives

    h(ell,W)
      =u-pC-p*ell*Q1(ell)-p^3 f^3-p^2 W
      =u-pC+p^2 e = v0.

The terms -p*ell*Q1(ell) and p^2*v0*Q1(ell) cancel. Hence
e0(ell,W)=-W-p f^3-Q1(ell)v0=e. The other generators are fixed,
so gq=identity_B without invoking a generic-fiber argument.

For qg, p,s,u,M are fixed. The certificate gives q(ell)=L, so L
is fixed too. The invertible linear change then shows F,J are fixed.
Since qg preserves the quotient relation H+p^3 w=0 and H is fixed,

    p^3(qg(w)-w)=0 in T.

The independently established domain property and nonzero p allow
cancellation, yielding qg(w)=w. Thus qg=identity_T. The dependency
order is domain -> shear isomorphism -> T domain -> final inverse
composition; it does not use the desired cylinder inverse to assume its
own missing injectivity.

This reconstructs a concrete cylinder isomorphism theta=g barPhi:
A[w] -> B using only the outer manuscript's displayed formulas.

## Reconstruction V: split maps, component tuple, and scheme image

Let jmath:A -> A[w] be coefficient inclusion and epsilon:A[w] -> A
the evaluation w=0. Define

    i=theta jmath,
    r=epsilon theta^(-1)=epsilon barPhi^(-1) q.

Both maps are complex algebra maps. All corrections in Phi^(-1) contain
w, so evaluation at w=0 removes them. Consequently

    r(p)=p, r(s)=s, r(u)=u, r(m)=M,
    r(e)=-p F^3-Q1(L)[u-p Q(L)-p^3 F^3]=E_A.

For i, putting x=X=s^2+u^3+p^2 f and w=W in Phi gives

    D=-3u^2 W+3p^2 u W^2-p^4 W^3,
    S=s+p^2 XD, U=u-p^2 W,
    Fcal=f-(1+2sX)D-p^2 X^2 D^2,
    Jcal=j-X^2 D.

Thus i(p,s,u,F,J)=(p,S,U,Fcal,Jcal). The equation H maps to zero
because barPhi was induced from a quotient and g is well defined;
there is no need to infer this from sample evaluations.

Writing Mcal and Ecal for the polynomials defining M and E_A, with
their arguments supplied explicitly, the composite rho=i r sends
B's generators to

    (p,S,U,Mcal(S,U,Fcal,Jcal),Ecal(p,S,U,Fcal,Jcal)).

This is exactly the five displayed components, with no denominator
and with all nested substitutions determined. The formal equations

    r i=epsilon theta^(-1) theta jmath=identity_A,
    rho^2=i(r i)r=i r=rho

now follow from the proved inverse maps. i is injective and r is
surjective. The image of rho is i(A) because r is onto; its kernel
is ker r because i is injective. In particular it has transcendence
degree four by the independent domain computation.

Contravariantly pi=Spec i:A^5 -> Spec A and
sigma=Spec r:Spec A -> A^5 satisfy pi sigma=identity. Since r is
surjective, sigma is a closed immersion. Spec rho=sigma pi, its
scheme-theoretic image has coordinate ring B/ker rho=B/ker r=A,
and its point image equals sigma(Spec A) since pi has the section
sigma. One can additionally check the fixed scheme: the ideal
generated by b-rho(b) is exactly ker rho for an idempotent, so it is
the same closed image, not merely a set of fixed closed points.

## Boundary cases and independent zero-fiber derivation

The formulas must work at p=0; an isomorphism after inverting p is
insufficient. Let kappa be the bracket polynomial in q1, so q1=kappa*m;
kappa does not involve m. This defines kappa at m=0 too.
At p=0, ell=0, f=b0*m, j=d0*m, and W=-e-u*kappa*m. Also S=s,
U=u, D=-3u^2 W. Thus

    Fcal=b0*(m+3u^2 W), Jcal=d0*(m+3u^2 W).

The determinant identity gives m'=m+3u^2 W, while the reconstructed
L is zero. Therefore e'=-u*kappa*m' and

    rho(0,s,u,m,e)=(0,s,u,m',-u*kappa*m').

Evaluating W again yields W'=-e'-u*kappa*m'=0, proving that a
second application fixes every component of this fiber. At u=0 this
reduces to (0,s,0,m,0); at m=0 it remains defined and gives
m'=-3u^2 e. No division by p, L, m, x0, 1+2sx0, or a Jacobian
minor has been introduced into the global formulas. On the zero
fiber A/(p) the (L,M) coordinate change gives k[s,u,M] after setting
L=0, which is also consistent with its dimension and smoothness.

The exponential derivation uses characteristic zero; no claim here
extends this argument to arbitrary characteristic. The image is a
complex algebra retract, and nonpolynomiality must be as a complex
algebra, not just absence of a particular coordinate choice. No
four-variable nonpolynomial retract is constructed by this transport.

## Needed primary interfaces and exact remaining gaps

The following is a plan of interfaces to check after the initial gate,
not a report of imported primary-source verification.

* Essential nonpolynomiality interface: OpenAI's written Theorem 1.1
  at commit adc7f1241b42e322a6451854ab7e4b4c146bf78a, manuscript
  dated September 23, 2026, for exactly the displayed A over C. The
  needed statement is A not isomorphic to C^[4]. Its stabilization
  statement is independently reconstructed above, but this does not
  verify its nonpolynomiality. Exact presentation matching, quantifiers,
  characteristic, and use of ring versus scheme isomorphism must be
  checked from the source body. A theorem label or packaged audit is
  not enough.
* Nonpolynomiality proof interfaces advertised in the outer manuscript:
  exact filtered/valuation degeneration G=R[tau,I/tau^2]; transfer
  from polynomiality to a nonzero homogeneous LND with a positive-degree
  invariant; principalization on the determinant torus bundle; existence
  and normalization of the additive lift; production of an LND E of
  nonpositive shift with E^2(v)=0; compatibility of the auxiliary
  highest part and the equation E'^2(d^2+a^2u^3)=0; orbit-polynomial
  coprimality and applicability of Mason--Stothers; the precise field
  in which -u^3 is nonsquare; and regularity across both determinant
  charts forcing the incompatible shift sign. None has yet been read
  in its imported proof body. Potential logical losses to test include
  a lift becoming zero, invariants losing their positive degree, an
  associated highest part losing local nilpotence or the squared
  relation, dividing by an invariant that vanishes on a chart, and a
  sign inference valid only generically. These are falsifiable review
  targets, not claimed defects.
* General-reduction attribution: Nagamine Proposition 1.4 at
  arXiv:1811.04153v2. The formal transport above is independently
  proved and does not need this citation for truth; the source is
  needed for the manuscript's attribution and precise hypothesis
  comparison. Costa's 1977 question supplies historical context.
* Scope/history interfaces: Nagamine's ambient-three theorem;
  Chakraborty--Dasgupta--Dutta--Gupta Theorem 5.8 at
  arXiv:1910.11023v1 for transcendence degree two; the stated August
  2026 version of Chakraborty--Pal arXiv:2504.14382v2 for its open
  problem formulation; Epstein--Nguyen arXiv:1301.3967v1 for the
  polynomial-extension relation. The original bibliography supplies
  locators, not independent validation.
* Formal-scope interface: the actual Lean declaration claimed as
  OAI.ComplexCancellation.main in
  OAI/Algebra/AffineCancellation/Main.lean, its imported dependencies,
  theorem statement, axioms, and distinction from the comparator's
  challenge statement. The manuscript disclaims a reproduced full
  kernel build and a formalized retract theorem. No native source has
  been inspected or executed here; no formal proof credit is assigned.
* Computational-scope interface: later read actual native symbolic
  programs and certificates to see whether they check the same
  simultaneous substitutions, quotient identities, and boundary
  cases. A success receipt, rational examples, or checking only one
  inverse cannot establish the global theorem. They are not needed
  for the hand derivations above and cannot establish nonpolynomiality.
* Priority/publication interface: distinguish manuscript date, supplied
  commit, publication date, and demonstrable public disclosure. No
  earlier explicit transport in a bounded search is not a proof of
  priority. A new explicit presentation is distinct from a new general
  cylinder-to-retract implication or a new cancellation example.

## Falsifiable checks to perform on any resumed phase

1. Expand the localized xy-z(z+1) identity and check both inverse
   coordinate substitutions. Confirm H modulo p is nonzero and that
   domain proof has no dependence on qg.
2. Verify Phi fixes x,y,z,p,w and shifts H by +p^3 w; check both
   simultaneous compositions with w replaced by -w. Confusing
   sequential substitutions with simultaneous ones can give false
   certificates.
3. Check the determinant, all three coefficients of Q, H(L),
   t=L-ph, and the full ideal-membership certificate in the polynomial
   ring before quotienting. A mismatch of L/M or original versus
   transported s,u is fatal to the displayed maps.
4. Check t(ell,W)=0, gq(e)=e, qg(L)=L, and the exact p-cancellation
   argument for qg(w). A failure on p=0 would invalidate the asserted
   global stabilization even if every p != 0 sample passed.
5. Match i and r generator images to the actual declared composition
   order; test the full five-component tuple including its e component.
   Check p=0, m=0, u=0, x0=0, and the complementary Jacobian chart.
6. Independently test the external theorem's exact assumptions and
   every essential nonpolynomiality interface before giving the
   nonpolynomial-image conclusion. Exhibiting A=C^[4] would refute
   that conclusion despite the split-map identities. Merely failing
   to find such coordinates would not prove it.

## Initial status

Original-only reconstruction and boundary-case analysis are complete for
the authorized INITIAL phase. The hand reconstruction is checkable algebra,
not an execution result and not a final verification of the full published
target. The essential imported nonpolynomiality proof remains unread at the
required gate. Best-guess completion: INITIAL phase 100%; full scientific
review 35%, with substantial uncertainty concentrated in the essential
external input and associated scope claims. No route is promoted to a final
PASS; no weaker conditional claim is substituted for the target. This lane
must stop after finite sealing pending the root checkpoint and explicit
RESUME.

# Full original scientific review: scope-sol continuation

Record 23203270, inventory row 188. Author: Alec Kriebel,
ORCID 0009-0001-9320-500X. Review date: 2026-11-17 UTC.

This continuation was authorized after the root independently checkpointed
the original-only INITIAL phase. It leaves the 17-file, one-child-directory
INITIAL namespace byte-, mode-, and topology-exact. The pre-support
independent claim analysis and constructive reconstruction remain in the
separately sealed INITIAL folder. This report follows that reconstruction;
the package's favorable audits are not premises of the argument below.

## Result and exact scope

The full original mathematical claim is supported by the independently
reconstructed explicit maps and the actual pinned written primary proof.
No substantive mathematical defect or unresolved central proof gap was
identified. This finding covers the smooth integral complex algebra

    A=C[p,s,u,F,J]/(H),
    x=s^2+u^3+p^2 F,
    H=x^2 F-(1+2sx)J-p^2 J^2-pu,

its transcendence degree four, its specified denominator-free split maps
with the polynomial ring B=C[p,s,u,m,e], the actual five-component
idempotent, and its image being isomorphic to the nonpolynomial algebra A.
It is not a finding only about a conditional cylinder-to-retract lemma.
The crucial nonpolynomiality input was checked in its actual primary proof
body, not accepted from a theorem declaration or an author audit.

The single authorized native computation did **not** reproduce the reported
symbolic run: the existing Python environment lacks SymPy. It exited at
the import before any identity check. No dependency was installed, no
interpreter changed, and no native route retried. The written proof and
independent algebraic reconstruction, rather than a claimed fresh PASS
transcript, support the mathematical finding. No formal kernel build was
attempted or certified. The published manuscript itself expressly
disclaims a reproduced full kernel build and a formalization of the
retract theorem, so those absences do not negate a formal claim it made.

This review does not establish first priority or an exhaustive literature
absence claim. The manuscript's explicit attribution to OpenAI for the
cancellation example and nonpolynomiality, and to the classical reduction
for the abstract retract consequence, is appropriate. It does not resolve
the four-variable retract question.

## Authentic primary evidence and reading coverage

The native controlling manuscript is the six-page outer Zenodo paper,
74,424 bytes, SHA256
`c579ec3442f4bcdf68ed737ad8bc65328682158845ed2e14e6636b2b119f52c6`.
The INITIAL records its complete TeX/text reading and personal viewing of
all six fresh renders. Its exact target and zero-fiber analysis were frozen
before support was opened.

The essential primary source is OpenAI, *An explicit failure of complex
affine-space cancellation*, pinned commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The obsolete local clone path
listed in the original provenance is absent; instead, 16 exact files were
retrieved by ordinary public GET at that commit. Every retrieved byte
length and SHA256 matches the published provenance. These are captured
under `primary-pinned/`, with request metadata in PRIMARY_ACQUISITION.json.
The complete actual TeX entrypoint, preamble, seven sections, and reference
list were read. The central proof bodies are the following:

| Source section | Exact interface read in actual proof | Source SHA256 |
|---|---|---|
| 02-construction.tex | domain and polynomial cylinder | fd10c0e2eb35a5572f43263ba88ea893551415c1807f6f6c8ad6158e64caa882 |
| 03-degeneration.tex | exact valuation, graded presentation, induced LND, positive invariant | 01c8fba41829052c46ae2e1c34ace91283808c3bcd5a6adcfa58cdca1ad7424c |
| 04-bundle.tex | principalization, normalized linearization, homogeneous lift | 37097f3689e0d41315a623c7d94e362141526f642ca8515682751f47a0ea5ae7 |
| 05-reduction.tex | sign-sensitive extraction of a nonzero LND | 8c6e5470bfc09d98f6cca44b461d3894034cc7b90f2bd379e47990753192f6b2 |
| 06-rigidity.tex | polynomial abc proof, orbit rigidity, coefficient intersection | a15737c05af4fe6ec7f4af2552250bb9366c19f7c47dea3e13f492529fd50bf8 |

The source's field macro is C. Its Theorem 1.1 uses precisely the same
H and A; there is no auxiliary coefficient-preservation or equivariance
hypothesis imposed on a hypothetical polynomial algebra equivalence.
The pinned primary PDF is separately captured with its provenance hash
`91a1a2f28c960cba25dd268e0f5515f0cff31463e4342098bbd89f857dd82023`.
The proof audit here uses the complete pinned TeX bodies; it does not
claim a personal page-by-page viewing of the separate upstream PDF.

Full supporting stabilization, nonpolynomiality, bundle, formal-scope,
priority audits, theorem/dependency ledgers, provenance, computational
results, and formal build logs were read after the gate. They do not
replace the primary proof checks. The 55 bundled formal modules match
the recorded byte hashes, contain 5,573 lines, and their imports close
within those modules plus Mathlib. Nine relevant formal modules were
personally read completely: Model, Main, Dimension, EquivariantLift,
PositiveObstruction, Determinant, Bundle, OrbitRigidity, HighestWeight.
This is explicitly not a line-by-line audit of all 55 formal proof bodies.

## Explicit construction and its dependence order

The original-only derivation in INITIAL already proves the local-coordinate
identity

    xy-z(z+1)=p^2(H+pu),
    y=s+x(x-u^3), z=sx+p^2 J,

and the localized polynomial presentation
A[p^-1]=C[p,p^-1,x,y,z]. Since H is irreducible after inverting p and
H modulo p is the nonzero polynomial L, the UFD descent proves A is a
domain before any cylinder inverse is used. The fraction field gives
transcendence degree four. This closes the possible circularity in
canceling p^3 later.

The localized derivation -p^2 partial_u, with p,x,y,z fixed, restricts
to P and remains locally nilpotent by injectivity into its localization.
Its finite exponential Phi fixes x and sends H to H+p^3 w. It induces
barPhi:A[w] -> T=P[w]/(H+p^3 w), with the quotient direction correct.
Thus T is a domain with nonzero p independently of qg.

The determinant-one change from (F,J) to (L,M), over C[p,s,u], has
inverse f(L),j(L). Put Q=C+LQ1, Lstar=pu-p^2 C, and

    h=u-pQ-p^3 f^3-p^2 w,
    e0=-w-p f^3-Q1 h,
    t=H+p^3 w=L-ph.

Direct expansion, with no computation receipt as a premise, gives

    p^3 e0-(L-Lstar)=(p^2 Q1-1)t.

In B set ell=Lstar+p^3 e, v0=u-pC+p^2 e, and
W=-e-v0 Q1(ell)-p f(ell)^3. Then ell=pv0 and
t(ell,W)=0. Substitution gives h(ell,W)=v0 and e0(ell,W)=e.
Consequently gq fixes all five free generators. For qg the certificate
fixes L, while the linear inverse fixes F,J; the relation gives
p^3(qg(w)-w)=0. The independently proved domain property supplies
legitimate cancellation. Both maps are actual global isomorphisms.

With theta=g barPhi, coefficient inclusion jmath, and evaluation
epsilon at w=0, i=theta jmath and r=epsilon theta^-1 satisfy ri=1.
The manuscript's r(e) follows because all exponential corrections
vanish at w=0. Its S,U,Fcal,Jcal are the transported generator images.
Applying i to r(m) and r(e) yields exactly the last two specified
components. Hence the displayed rho is ir, and rho^2=rho. Its image
is i(A), not merely a ring with the same dimension.

Smoothness follows from the Laurent chart and the complementary F,J
partials at p=0. Their Bezout identity is one, so no singular points
are hidden on the parameter-zero fiber. Every expression is polynomial
at p=0, m=0, L=0, and x0=0. In particular kappa is a specified bracket
polynomial, not a quotient operation at m=0. The independently derived
zero-fiber map has m'=m+3u^2 W and e'=-u*kappa*m'; its next W is zero.
Thus no localization-only verification is being promoted globally.

On spectra, Spec r is the closed embedding and Spec i its left
inverse. The affine-five-space map is their composite in that order.
The scheme-theoretic image algebra is B/ker r=A, since
ker(ir)=ker r. These facts also verify the contravariance and closed
image assertions, rather than only an equality on complex sample points.

## Essential nonpolynomiality input: independent proof checks

The following checks address the interfaces identified before reading
the package. They use the actual pinned proof bodies and the indicated
algebraic deductions. They are not deductions from the packaged audits'
favorable conclusions.

### Exact degeneration and polynomiality-to-action step

In 03-degeneration.tex, the auxiliary domain

    S=C[p,x,y,z,u]/(xy-z(z+1)-p^3 u)

injects into A because it becomes an isomorphism after inverting p
and has no p-torsion. The residue R=S/pS is the smooth domain
C[x,y,z,u]/(xy-z(z+1)). At the prime pS the maximal ideal is generated
by p. Repeated divisibility terminates by the ascending-chain condition,
so the local ring gives a discrete valuation. Primality of pS descends
positive divisibility from that localization back to S, and then gives
all orders by iteration. This is the missing justification one would
need if initial coefficients were only known to lie in Frac R.

For weights (-1,0,0,2,2), the leading relation is
Htop=x^2 F-(1+2sx)J-p^2 J^2. The initial map to R[tau,tau^-1] has
kernel exactly (Htop): inverting p identifies its kernel with the
quadric equation, and UFD irreducibility plus p-nondivisibility permits
contraction. This is stronger than checking only that Htop vanishes.
If the top weight of a representative exceeds its actual valuation
degree, subtract H times the corresponding homogeneous quotient of its
top part by Htop. The maximum weight decreases, and its fixed valuation
degree bounds it below. Negative generator weights do not prevent this
finite descent. Thus the associated graded ring is exactly
G=R[tau,I/tau^2], with the specified copy of R, and every element has
an exact-weight representative.

That representative property bounds a derivation's shift globally
from its five generator images. A generator attaining the bound makes
the induced top derivation nonzero. The iterate formula in the graded
pieces descends local nilpotence without requiring a nonnegative shift.
If A were polynomial, some coordinate would have positive valuation
degree because F has degree two and the nonpositive-degree subalgebra
is proper. Differentiation in another coordinate is nonzero and fixes
that coordinate. Therefore a nonzero homogeneous LND of G with a
nonzero positive-degree homogeneous invariant is produced. No
preservation of R by this additive derivation is assumed.

### Principalization and normalized lift

In 04-bundle.tex the charts over z+1 and z cover the base and make
Rt=C[a,d,b,c,u]/(ac-bd-1) a Laurent-line bundle over R. The transition
between the parameters a and d is a base unit. This proves faithful
flatness; it is not inferred merely from a suggestive torus action.
Writing v=a^3 b-a^2 u^3-d^2 and h=ab-u^3, direct determinant-ring
calculation gives the two center generators as C1*v and b^2*v, where
C1=c^2-b^2 h. The displayed alpha,beta satisfy
alpha*C1+beta*b^2=1, so the ideal is exactly (v), including both
containments. Flat base change identifies the actual pullback with
Rt[tau,v/tau^2]. The proof of tau-saturation of
(tau^2 V-v) establishes its full presentation and domain property.

The lift is over Spec G itself, not over Spec R. G was proved smooth
on its Laurent chart and by the same complementary Jacobian minors at
tau=0. For a smooth integral affine base C, the source proves
Pic(C)=Pic(C[t]): subtract a generic principal divisor to remove
horizontal components, then show each remaining height-one prime is
q[t] for a height-one q of C with multiplicity one. Restriction at
t=0 supplies the inverse. The ordinary standard interfaces used here
are smooth implies regular, regular local rings are UFDs, and locally
factorial normal schemes have Picard group equal to divisor class
group. The actual Stacks proofs at tags 056S, 0AG0, and 0BE9 were read
and captured; their hypotheses hold for this smooth integral
finite-type complex base. This does not transfer the cancellation
claim to an unsupported theorem of comparable difficulty.

Picard invariance supplies an isomorphism of the two pulled-back line
bundles; normalize it at the identity. Its ambiguity is a unit of
C[t], which is a unit of C because C is a domain. The ratio of the
cocycle expressions is a unit of C[s,t] and is one at s=0, so it is
identically one. Hence the normalized action exists and is unique,
linear on fibers, and preserves the nonzero-vector locus. In
characteristic zero its polynomial coaction gives an LND. None of
this requires C to have only constant ground-field units.

For homogeneity, the valuation torus fixes the actual coefficient R,
so its pullback action extends linearly to the total line bundle.
Conjugating the lift and rescaling the additive parameter give two
normalized linear lifts of the same action. Uniqueness identifies
them, proving the exact original shift and fiber weight zero. This
argument avoids assuming that the additive action preserves R or Rt.

### Extraction with a moving parameter

In 05-reduction.tex the exact homogeneous pieces of the pullback are
tau^-e Rt for e<0, V^l Rt for e=2l>=0, and
tau V^(l+1) Rt for e=2l+1>0. Coefficients are unique because the ring
is a domain. Every positive-degree invariant is divisible by V.
Product-additivity of LND order in characteristic zero gives factorial
closure of the kernel, and therefore the lifted derivation fixes V.

If tau is fixed, localization at tau preserves local nilpotence. The
degree-j value on Rt is tau^-j E(r), where E maps Rt into itself.
Since the multiplier is invariant, iterates prove that E is a nonzero
LND of fiber shift zero fixing v.

If tau moves, an LND cannot send a nonzero element into its own
principal ideal unless the value is zero. The exact pieces therefore
force j=2l+1 with l>=0, and the value on Rt is
tau V^(l+1) E(r). Cancellation gives a derivation with values already
in Rt and fiber shift -2(l+1). The proof does not localize at the
moving tau to infer nilpotence. If m is the LND order of tau, then
whenever E(r) is nonzero its lifted LND order equals
nu(r)-m-1. Successive iterates decrease a nonnegative integer, proving
local nilpotence of E. Since nu(v)=2m, E(v) has order m-1, and a
nonzero E^2(v) would have order -2. Thus E^2(v)=0 and E is nonzero.
This independently checks the sign and the delicate multiplier step.

### Rigidity, nonsquareness, and boundary regularity

In 06-rigidity.tex the auxiliary weights (0,3,-3,0,2) define a genuine
grading commuting with the fiber grading. A derivation has only
finitely many shifts, as seen on the five generators. Its highest
nonzero auxiliary component E' is an LND: in an iterate on a
homogeneous input, only choosing the highest shift every time can
contribute to the highest possible degree. This reasoning works for
negative highest shift as well. It preserves the fiber shift.

The two parts of v have auxiliary degrees -3 and 6, so projecting
E^2(v)=0 to degree 6+2lambda gives E'^2(N)=0 for
N=d^2+a^2 u^3. Over the original field
K=Frac Rt=C(a,d,b)(u), the nonzero orbit polynomials obey
D(q)^2+A(q)^2 U(q)^3=N+q E'(N). A common root of the two summands
would have multiplicity at least two in their nonzero sum, which has
degree at most one. Thus the abc coprimality hypothesis holds.

The source supplies and proves the polynomial abc inequality by a
Wronskian. Applying it to these summands gives, in the nonconstant
case, 2Dd=2Da+3Du and Dd<=Da+Du. Thus Du=0 and Dd=Da>0.
Highest-term cancellation would make -u^3 a square in K, impossible
because its u-order is odd. The algebraic closure was used only for
root counting; the leading coefficients stayed in K. Consequently
E' fixes a,d,u.

The determinant relation now gives E'(b)=a h and E'(c)=d h with
h=c E'(b)-b E'(c) an element of Rt. Localizing at the invariant
nonzero elements of C[a,d,u] preserves nilpotence and makes the ring
Q[b], Q=C(a,d,u). The one-variable LND argument forces h into Q.
The separate a and d charts then place it in
C[a,d,u][a^-1] intersect C[a,d,u][d^-1]=C[a,d,u]. Since a,d are
coprime in that polynomial UFD, there is no hidden denominator.
But h is nonzero of fiber weight e-2<0, whereas C[a,d,u] has only
nonnegative fiber weights. This is the contradiction. It completes
the nonpolynomiality input for the exact A, not an analogue or a
restricted class of actions.

## Adversarial checks and exact limitations

The proof dependency order was checked for circularity: domain precedes
the inverse cancellation; the exact graded ring precedes degree bounds;
smoothness of G precedes lifting; the invariant fixes V before order
extraction; the original fraction field precedes nonsquareness; both
charts precede elimination of denominators. These are essential steps
and all are supplied in the primary bodies.

Potential counterexamples outside the assumptions do not refute the
application. Positive fiber shift genuinely admits the root derivation
b->a, c->d with E(v)=a^4; therefore the sign condition cannot be
dropped. The opposite root derivation has nonzero second value on v.
Characteristic zero is essential to exponential identities, LND order
additivity, and abc. Replacing u^3 by an even exponent would destroy
the stated parity obstruction. Nonreduced bases can have polynomial
units depending on the parameter, so the normalized-lift uniqueness
must not be extended to them; the actual base is smooth and integral.
None of these assumption changes is made in the manuscript.

The two native Python programs and every function they call within
those files were read completely before executing the selected route.
Their exact certificate roles were checked against the equations.
The stabilization program does not itself prove the domain or
nonpolynomiality; its last inverse uses the written domain argument.
Its seven rational regression points cannot prove idempotence. The
other program verifies principalization identities modulo the
determinant equation and two sample root derivations; it cannot
exclude all LNDs. Its output file side effect was inspected, and that
second program was not executed in this lane.

The unmodified stabilization file was copied into a fresh isolated
directory and invoked once with the existing python3. Exact receipt:
start 2026-11-17T06:37:48.791669+00:00; finish
2026-11-17T06:37:48.839307+00:00; elapsed 0.04741466599807609 seconds;
exit 1; stdout empty; stderr reports ModuleNotFoundError for sympy
at line 15. The source and copied SHA256 both equal
`bdac2f5d79284a125f0c63b970b06ca67060ff0d0f8ed60cfb0644f0a005a6ff`.
Original sources and INITIAL guards match before and after. The
published 32-symbolic-check/seven-point PASS receipt was read as
historical package evidence and was not relabeled as this run's result.
No separate analytic computation was needed; the independent controls
are the written algebraic deductions above and the INITIAL notes.

For formal scope, Model's exact definitions match the actual pinned
comparator definitions. The comparator's `sorry` is in its challenge,
not the Main solution. The actual Main proves a statement about the
finite-type complex quotient, domain, Krull dimension four, polynomial
cylinder, and nonpolynomiality. It does not state smoothness, retract
maps, five components, or priority. EquivariantLift visibly uses a
nonzero invariant replica and subsequent highest-component extraction,
not the printed normalized Picard lift. The inspected highest-weight
lemma also supplies a different formal rigidity mechanism. Neither
formal-source presence nor a lexical scan certifies kernel checking.
The retained logs really show missing Mathlib/OAI modules, consistent
with the manuscript's explicit non-reproduction disclosure. This
review relies on the audited written proof, not a claimed successful
Lean build or an uninspected formal closure.

## Literature, attribution, and version boundaries

The actual primary Nagamine v2 Question 1.3 and entire Proposition 1.4
proof were read. Coefficient inclusion/evaluation supplies precisely
the classical implication used here. Its Theorem 2.5 and proof state
the ambient-three characteristic-zero result. The actual
Chakraborty--Dasgupta--Dutta--Gupta v1 Theorem 5.8 and proof do state
the stronger arbitrary-ambient result for transcendence-degree-two
images. Its introductory ambient-three summary alone would not have
sufficed to check that stronger assertion. The actual
Chakraborty--Pal v2 introduction is dated August 20, 2026 and makes
the stated then-open characteristic-zero n>=4 assertion.
Epstein--Nguyen v1's actual introduction records polynomial-extension
retracts and the stronger-than-cancellation relationship. The three
captured arXiv PDFs match the original provenance hashes. Full
HTML/PDF captures and ordinary-GET receipts are in primary-context/
and CONTEXT_ACQUISITION.json.

Those contextual theorem statements agree with the manuscript's
scope, and none is being used as a new theorem of this consequence
note. This review has not performed an exhaustive new priority
search. The package appropriately limits its claimed new contribution
to the explicit transport and verification presentation and says
failed searches do not prove priority. Original Costa full-text
reading is not claimed; the question formulation is reproduced in
the inspected primary articles. Manuscript dates and actual public
disclosure dates must remain distinct.

The native API has no version field, as authenticated in INITIAL and
preserved by all guards. The native HTML's `v1` display and the
primary sources' explicit arXiv versions do not supply such a field.
The published date remains October 6, 2026. No metadata, manuscript,
source, website, Sheet, deployment, release, or Zenodo record was
changed.

## Closure

The full original mathematical target is supported at the level of
independent written-proof review. The exact remaining reproduction
limits are the unavailable SymPy run and the unattempted formal
kernel build; neither is asserted to have passed. No central
mathematical gap requiring a DEFER was identified in this lane.
There is no proposed repair, narrowed promotional replacement, or
follow-up project. Final publication/disposition belongs to root
after its independent original-reading gate. Best-guess completion
of this bounded scientific review: 100% at the terminal seal.

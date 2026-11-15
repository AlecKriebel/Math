# Independent paper-only analytic reconstruction

This initial is written after personally reading the entire actual published four-page PDF, all 263 lines / 11910 bytes of the controlling TeX and all four fresh individual page rasters. It precedes reading foreign scientific bodies, native scientific source code/results, archived/current scientific review/opinion or inventory triage. My earlier acquisition exposure was native metadata, identity columns, file names and opaque complete-byte/CRC/hash/extraction custody only. No manuscript text, TeX preamble or scientific body was read in that acquisition. This is not a new blind context, and no inherited custody reading is represented as personal prior scientific reading. One analytic reviewer uses the distinct mechanisms below; these are not counted as separate reviewers.

## Exact original hypothesis and success criterion

For **every field k**, every alpha in k and every beta in k satisfying beta^2 != 1, let R be the connected graded four-generator free-algebra quotient by the six quadratic relations f1,...,f6 displayed on target page1. All generators have degree1, and the ideal I=(x3-x1,x4-x2) is the two-sided homogeneous ideal in R. The theorem asserts the exact graded k-algebra isomorphisms

R/I = k<X,Y>/(Q) = B(P^1_k,O(1),sigma),

where Q=beta X^2-XY+YX-beta Y^2 and sigma[s:t]=[s+beta t:beta s+t]. The specified map sends x1,x3 to s and x2,x4 to t, and its kernel is **exactly I**. It further asserts 0 != I strictly contained in R_+, complete primality (hence ordinary and graded primality), Hilbert series (1-z)^(-2) and GK dimension2. This is an infinite-dimensional positive-curve image, not an augmentation image. It claims to refute two **actual printed** Rogalski–Sierra assertions in their algebraically independent parameter regime: unique nontrivial graded prime and absence of nontrivial maps to any twisted homogeneous coordinate ring.

The algebraic theorem applies to the displayed presentation in all characteristics. It does not identify every characteristic2 independent-parameter presentation with the journal's geometrically defined family, and does not transfer source noetherianity/GK dimension to all fields/parameters. It does not classify all primes, claim equality of birational graded quotient rings, certify firstness or worldwide current openness, or propose a research follow-up. Full success requires both the exact quotient theorem and faithful primary-source identification/interpretation. A calculation for a miscopied presentation or a map to a different class of ring would not establish the source-specific negative answers.

## 1. Universal quotient and relation matching

Write T4=k<x1,x2,x3,x4>, L=(x3-x1,x4-x2) in T4, and let phi:T4 -> T2=k<X,Y> send the generators in order to X,Y,X,Y. The free-algebra universal property gives T4/L=T2. Consequently

R/I = T4/(L+(f1,...,f6)) = T2/(phi(f1),...,phi(f6)).

This is exact: the quotient ideal cannot acquire an additional unknown generator by substitution. Direct noncommutative substitution, without commuting X and Y, gives:

- phi(f1)=X(alpha X-X)+X(X-alpha X)=0;
- phi(f2)=X(alpha Y-Y)+X(Y-alpha Y)=0;
- phi(f3)=Y(alpha X-X)+Y(X-alpha X)=0;
- phi(f4)=Y(alpha Y-Y)+Y(Y-alpha Y)=0;
- phi(f5)=X(beta X-Y)+Y(X-beta Y)=Q;
- phi(f6)=X(beta X-Y)+Y(X-beta Y)=Q.

Thus the six images generate exactly (Q). Alpha drops out identically, so no genericity or algebraic independence is needed for this step. One must not assume commutativity before computing these images. The two-sided ideal convention and the fact that x4 is the relevant left factor in the target's last summands are important. Actual primary relation lists and their parameter convention remain **unverified at this initial seal**; the target's assertion that they match is a hypothesis to test, not evidence in its own favor.

## 2. Graded automorphism twist, all fields and arbitrary elements

Let S=k[s,t], theta(s)=s+beta t and theta(t)=beta s+t. Its degree-one matrix M has determinant 1-beta^2, nonzero by hypothesis, so theta is a graded k-algebra automorphism over every field. For homogeneous f of degree m set f star g=f theta^m(g). If g has degree n, then

(f star g) star h = f theta^m(g) theta^(m+n)(h)
= f theta^m(g theta^n(h)) = f star (g star h).

The degree-zero scalar unit is unchanged. A product of nonzero homogeneous f,g is nonzero because S is a domain and theta is injective. If a,b are arbitrary nonzero finite graded sums, their highest nonzero components a_m,b_n contribute the unique highest total degree m+n component a_m theta^m(b_n), which is nonzero. Therefore the entire twisted algebra is a domain; no homogeneous-only definition of domain is being silently used.

It is generated in degree1. Inductively the span of star products of degree n sections and degree1 sections is S_n theta^n(S_1)=S_n S_1=S_(n+1), since theta^n acts bijectively on S_1. The notation denotes product **spans**, not a claim that every polynomial is a single product of two chosen forms. Its vector-space Hilbert function is dim S_n=n+1.

## 3. Projective-line geometry and positive-pullback convention

The invertible matrix M induces the projective k-automorphism sigma[s:t]=[s+beta t:beta s+t]. Pullback of the coordinate sections gives sigma^*(s)=s+beta t and sigma^*(t)=beta s+t under the linear lift's identification sigma^*O(1)=O(1). The iterated tensor identifications give L_n=O(n); using the compatible linear lifts at all stages makes section multiplication f tensor (sigma^m)^*g exactly f theta^m(g).

Thus the constructed algebra is the actual THCR under the explicitly stated positive-pullback convention, not merely a vector-space lookalike or an unspecified inverse twist. In particular H^0(P^1_k,O(n))=S_n, including n=0, over arbitrary k; algebraic closure is unnecessary. The sheaf O(1) is sigma-ample because L_n=O(n) and Serre vanishing applies to every coherent sheaf tensor O(n). If a cited primary uses an inverse convention, that convention must be distinguished rather than silently swapped. The projective image has dimension1; its ring has GK dimension2. These are different dimensions.

Directly,

s star s=s^2+beta st,
s star t=beta s^2+st,
t star s=st+beta t^2,
t star t=beta st+t^2.

The coefficients of s^2,st,t^2 in beta(s star s)-(s star t)+(t star s)-beta(t star t) all cancel, proving Q=0 in this algebra. Since s,t generate, there is a graded **surjection** A=T2/(Q) -> B. The exact-kernel issue requires an independent dimension argument; satisfying relations alone would not suffice.

## 4. Termination, spanning and equality without a confluence assumption

Use the triangular change U=X-Y,V=Y, whose inverse is X=U+V,Y=V and whose determinant is1 in every characteristic. Substitution gives

Q=beta U^2+(beta-1)UV+(beta+1)VU.

Since beta+1 !=0, rewrite

VU = q UV + r U^2,
q=(1-beta)/(1+beta), r=-beta/(1+beta).

For words of a fixed length n, lexicographic order with V>U is finite. Replacing a selected VU by either UV or UU changes its first differing letter from V to U, leaving the prefix unchanged; it strictly decreases that finite order. Hence reductions terminate, including linear combinations after distributing coefficients. A word without VU is precisely U^i V^(n-i), 0<=i<=n. These n+1 words therefore span A_n. There is no claim that this observation alone establishes their linear independence, and no confluence claim is needed.

The graded surjection A -> B gives dim A_n >= dim B_n=n+1, while the spanning argument gives the reverse inequality. Equality follows degree by degree, and the surjection is injective in each degree. This closes the exact quotient/kernel statement for the whole graded algebra, not just bounded degrees. Infinite-field arguments, numerical rank guesses and sampled parameter values play no role.

## 5. Fresh secondary Ore/diagonal/Jordan mechanism

The same relation suggests an independently checkable secondary construction. Let C=k[U], tau(U)=qU, and delta(U)=rU^2. Here q !=0 because beta !=1 and beta !=-1. The tau-derivation is determined on powers by

delta(U^n)=r(1+q+...+q^(n-1)) U^(n+1),

which follows by induction from delta(ab)=tau(a)delta(b)+delta(a)b. The Ore extension C[V;tau,delta] has relation VU=qUV+rU^2 and the polynomial basis U^iV^j. Establishing its construction/basis directly or by a checked classical interface would give another quotient-domain route. This is not used to replace a gap in mechanism4: the target's spanning-plus-surjection proof already handles the full theorem. It offers a distinct algebraic falsification mechanism and predicts characteristic-dependent normal forms before any native code is read.

In characteristic !=2, put W=X+Y=U+2V. The relation becomes

Q=((beta-1)UW+(beta+1)WU)/2,

so WU=qUW. The eigenforms s-t and s+t for theta have eigenvalues 1-beta and1+beta, respectively, matching that quantum-plane parameter. At beta=0, q=1,r=0 and the quotient is the ordinary polynomial plane. There is no division by beta in this statement.

In characteristic2, q=1 for every permitted beta and r=beta/(1+beta), so the relation is VU=UV+rU^2. For beta!=0,1 this is a Jordan-plane form after scaling; beta=0 is again commutative. This makes clear why using X+Y and X-Y as an invertible basis in characteristic2 would be wrong. A meaningful finite diagnostic should include a nonzero allowed beta over F4 (F2 itself has only the allowed value beta=0), or an exact rational-function field in characteristic2, rather than pretending F2's beta=0 probes the generic characteristic2 situation.

## 6. Complete prime, degree-one nonvanishing and growth

All defining relations in R have degree2. Their homogeneous two-sided ideal in T4 has no degree1 component; hence x1,x2,x3,x4 remain linearly independent for **all** alpha,beta, including specializations. Thus x3-x1 is a nonzero member of I, even when minus equals plus in characteristic2. I is homogeneous and lies in R_+ because it is generated in positive degree. The map sends x1 to nonzero s, so x1 is not in I and I is strictly below R_+. The domain quotient makes I completely prime, which implies ordinary and graded primality by the two-sided ideal-product criterion. R/R_+=k is the augmentation quotient, and the new I is distinct from both0 and R_+.

The Hilbert function n+1 yields sum_(n>=0)(n+1)z^n=(1-z)^(-2). Since the ring is generated by its finite degree1 space, the cumulative word-length filtration has exact dimension sum_(j=0)^n(j+1)=(n+1)(n+2)/2, giving GK dimension2. This calculation does not establish the source R's GK dimension for all parameters and is not presented as a Krull-dimension classification.

## 7. Singular parameters, base fields and independence boundaries

The excluded values are necessary for this automorphism/domain description. At beta=1,

Q=(X+Y)(X-Y),

and at beta=-1,

Q=-(X-Y)(X+Y).

The displayed linear factors are nonzero in the quadratic quotient, since its defining ideal has no degree1 elements. They are zero divisors; in characteristic2 they coincide and give a nonzero square-zero linear element. Thus dropping beta^2!=1 would produce a false domain statement and a singular projective matrix. Beta=0 is a genuine allowed specialization, and alpha is arbitrary because it cancelled in mechanism1.

Algebraic independence over the prime subfield implies beta is not a root of z^2-1, so the prescribed independent-parameter regime satisfies the theorem's hypothesis. No countability argument is needed. For the journal's stated substitutions c=(vartheta-1)/(vartheta+1), d=(rho-1)/(rho+1), their inverse fractions in characteristic !=2 give a birational parameter change and preserve independence when defined. In characteristic2 these fractions equal1 where defined. The target correctly separates the all-field presentation theorem from a claim to identify that independent-parameter characteristic2 presentation with the geometric source family. The actual journal hypotheses and parameter formulas remain a pending primary check.

## 8. Printed problem/category interpretation remains an exact external check

The target says the OWR2010 report printed1361–1362 and the 2012 journal printed1198 contain both contrary assertions, and the journal Theorem3.5(2) printed1202 has these six relations using c,d. This must be verified from the actual primary bodies and legible page images. In particular:

1. The same six relations, factor positions and signs must appear under the claimed parameter convention.
2. The phrase nontrivial homomorphism must not be restricted to an injective, birational, dimension-at-least2-image or same-graded-quotient-ring class that would exclude the constructed curve quotient.
3. Nontrivial graded prime must permit the nonzero ideal I strictly below R_+, as ordinarily understood.
4. The printed source's geometric/base-field hypotheses must match the claimed generic parameter consequence; a presentation-only all-field result must not be overextended to a degenerate geometric family.

At this initial seal none of these primary statements has been independently read. If a substantive mismatch is found, the source-specific negative-answer claim is not rescued by narrowing the promotion or rewriting the presentation; the exact defect must be documented and the route deferred. No such mismatch has yet been established merely by reading the target.

## 9. Classical credit and priority/category limits

The target credits THCR/polynomial-twist machinery to Artin–Van den Bergh and Rogalski–Zhang and does not claim that the elementary two-generator classification is new. Its specific proposed contribution is this source's linear substitution and exact projective-line quotient. The alleged later Nevins–Sierra repetitions, their Theorem1.2 moduli/dimension conditions, universal-factor Theorem4.10, strong-noetherian hypotheses in Rogalski–Zhang, generic source failure of strong noetherianity and Campbell-thesis distinctions all remain **unverified primary assertions at this stage**. Earlier AI audits inside the source package are not scientific evidence for my reconstruction and have not been read.

Even if those inspected passages contain no matching predecessor, that would not certify historical firstness or worldwide current openness. The target itself acknowledges unread journal versions, older/unindexed work and citation-coverage gaps. A priori, other classical quotient descriptions may duplicate this one. No follow-up is justified from a failed search; default follow_up remains null.

## Mechanism / evidence / status / exact gap

| Mechanism | Paper-only evidence reconstructed here | Initial status | Exact remaining check |
|---|---|---|---|
| Universal free quotient | All six noncommutative substitutions and exact ideal universal property | Internally supported | Compare actual primary presentation and parameters |
| Polynomial graded twist | Associativity, degree-one generation, domain for arbitrary finite sums | Internally supported | Primary conventional identification/credit |
| Projective geometry | Matrix determinant, pullback lift, L_n=O(n), sigma-ampleness | Internally supported | Check actual THCR convention/interfaces |
| Termination and dimension | Fixed-length lex order, n+1 spanning words, lower-bound surjection | Internally supported | Meaningful exact bounded implementation check, not empirical proof |
| Secondary Ore/quantum/Jordan | Explicit tau, delta, q/r and characteristic-dependent basis change | Independent prediction before native code | Derive/check basis interface if used; avoid dividing by2 in characteristic2 |
| Prime and growth | No degree1 relations, strict ideal inclusion, domain quotient, exact cumulative count | Internally supported | No additional central internal gap found |
| Boundaries and field scope | Beta=0, beta=+-1 factors, characteristic2 collision, independent-parameter implication | Internally supported | Nontrivial characteristic2 diagnostic; actual geometric parameter scope |
| Printed negative answers | Exact source locators and interpretive requirements isolated | Unverified external input | Read actual OWR/journal relations and literal assertions |
| Credit/history | Specific asserted predecessor categories distinguished | Unverified external comparison | Actual RZ/NS/thesis passages; no exhaustive priority claim |

Initial assessment: the displayed-presentation quotient theorem has a coherent internally reconstructed proof in its full all-field/beta range, with no paper-only counterexample found. The source-specific claim to contradict actual printed assertions and the historical-context statements remain open primary verification tasks. This is a provisional initial, not a passing verdict. Root's science gate is closed; no mathematical finding or opinion has been sent. Subsequent independent work may inspect actual primaries and source programmes after this seal, without sibling opinions, and must stop extended repair if a substantive defect emerges.

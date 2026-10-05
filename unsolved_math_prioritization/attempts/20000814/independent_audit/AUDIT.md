# Independent adversarial audit: Problem 20000814

Date: 2026-10-05 UTC  
Catalog rank: 759  
Target: AIM *Components of Hilbert Schemes*, Problem 13  
Verdict: **PASS, scoped to the stated partial results and verification packet**  
Required mathematical corrections: **none found**  
Original problem solved: **no**  
Research disposition: **partial progress; five approaches completed**

This is an independent mathematical and computational review of the frozen
author packet, not a human peer-review certificate or a formal proof-assistant
verification. The entire authored report, proof document, source metadata,
control program, replay record, README, and manifest were inspected. The
upstream report was also read in full. The scope of each external-source check
is recorded in SOURCE_AUDIT.json. The author files and archive were preserved.

## 1. Accepted conclusions

Under the packet's precise assumptions, the following claims pass review:

1. An embedded flat family in fixed projective three-space, with smooth
   complete-intersection geometric generic fiber of type (a,b) and smooth
   special fiber, preserves degree, genus, and the specified canonical bundle.
2. The special curve is a complete intersection if and only if its Rao module
   vanishes. Subcanonicity is essential to the reverse implication here.
3. An integral degree-a containing surface suffices, even if it is singular or
   nonnormal. Smoothness of the containing surface is unnecessary.
4. A non-complete-intersection special curve must have minimal containing
   degree 3 <= c < a. Thus every a <= 3 case is affirmative.
5. The auxiliary rank-two section has a nonempty lci zero curve Z of degree
   (a-c)(b-c), with canonical twist 2c-a-b-4. Z must be nonreduced and cannot
   have degree one. In particular, type (4,4) is affirmative.
6. Every equation through the special curve of degree at most b is a multiple
   of its unique minimal degree-c equation, with the stated dimension jump.
7. The explicit plane-cubic-plus-line family is a valid singular-special-fiber
   negative control. The characteristic-two polynomial comparison is also
   valid, and neither is a counterexample to the characteristic-zero target.

No conclusion about a full resolution, existence of a remaining candidate, or
membership of such a candidate in the complete-intersection component follows.
The packet consistently retains these limitations and makes no novelty claim.

## 2. Specialization, connectedness, and canonical bundles

The trait formulation correctly fixes the embedding, the Hilbert polynomial,
and geometric smoothness of both fibers. In a Hilbert-scheme specialization
question, curve selection followed by normalization and completion supplies
the indicated trait after the usual field extensions. This does not convert
an abstract-curve degeneration into an embedded one.

Flat finite presentation and geometrically smooth fibers make the morphism
smooth. A smooth proper family has locally constant geometric connectedness;
the complete-intersection fiber is connected. The special smooth connected
curve is therefore integral. Regularity of the total space and flatness also
exclude an extra purely vertical component.

The generic trivialization of omega(relative)(-a-b+4) is a rational section on
this regular integral surface. Its divisor has no horizontal components. The
special fiber is the sole vertical prime divisor and occurs with multiplicity
one in div(t), so any resulting vertical Cartier divisor is principal. This
proves specialization of the actual line-bundle isomorphism, not merely its
degree or numerical class. The argument would fail without the integral
special-fiber hypothesis, which is established before it is used.

The descent sentence is sound: cohomology commutes with field extension on a
proper curve, so a degree-zero line bundle that becomes trivial has a nonzero
section over the original field; degree zero forces that section to have no
zeros. No claim about a torsion-free relative Picard group is needed.

The ideal sheaf is flat over the trait by the displayed short exact sequence.
Upper semicontinuity gives the correct inequality h0(special) >= h0(generic),
and hence a degree-a equation. The same principle permits, rather than rules
out, special Rao cohomology. The audit found no reversed semicontinuity step.

## 3. Rao criterion and the precise Serre construction

For the saturated curve ring of dimension two, vanishing of the stated Rao
module is equivalent to depth two. In the ACM case both the ring and its
canonical module are recovered as graded sections of their associated
sheaves. Subcanonicity therefore identifies the canonical module with a shift
of the ring. A codimension-two Gorenstein ideal has a Hilbert–Burch resolution
of type one and hence two generators. Its height makes those generators a
regular sequence. Conversely, the Koszul resolution gives Rao vanishing.

The Serre construction is performed **on the special P3 only**. It is not a
claim that an entire family of bundles has been constructed or that splitting
specializes. The extension class corresponding to the nowhere-vanishing
section 1 of omega_C(4-a-b) makes the middle term locally free at every point
of C. Away from C local freeness is immediate. The necessary intermediate
cohomology of O_P3(-a-b) vanishes, as stated.

Twisting the extension proves both the lifting of every equation and
H0(E(-a-b))=0: the adjacent groups are H0(O(-a-b))=0 and H0(I_C)=0. There is no
unproved relative Serre or bundle-specialization shortcut in this argument.

## 4. Integral containing surfaces and zero schemes

The nonzero section lifting an irreducible degree-a equation F cannot have a
divisorial zero. Such a divisor would give a positive-degree homogeneous
factor G of F. Since F is irreducible, G must be the full F, and division
would leave a section of E(-a-b), which has no nonzero sections. Division is
legitimate: the common codimension-one vanishing can be removed from a
locally free sheaf on the smooth, factorial ambient space; regularity across
codimension two follows from normality/reflexivity.

There is no hidden isolated-point exception. Locally a nonempty zero scheme
of this section is generated by two functions. With codimension-one zeros
excluded, a minimal prime has height exactly two, and the functions form a
regular sequence. The resulting lci scheme is pure of dimension one, with
no embedded isolated point. Its effective one-cycle has positive degree.

The rank-two twist formula gives c2(E(-b))=0, so this zero scheme is empty.
Only at that point may one form the everywhere exact line-bundle extension;
H1(O(b-a))=0 then splits it. The original section of E supplies two global
forms cutting C scheme-theoretically. This proves the claimed CI type.

The argument uses no smoothness, normality, or Cartier-divisor property of C
on the containing surface. DGF Lemma 2 independently confirms the same
equality case with T=P3, t=1, s=a, d=ab, and canonical exponent -4. It is
important to cite that lemma rather than incorrectly demand minimality in
the integral-surface proposition.

Primality of I_C makes every minimal-degree equation irreducible. Combined
with existence of a degree-a equation, the preceding proposition proves
c<a for a non-CI candidate.

## 5. Quadric classification, including the vertex

The reducible and double-plane cases reduce scheme-theoretically to a plane
because I_C is prime. A smooth integral plane curve is a complete intersection.

On a smooth quadric the diagonal H1 vanishing holds for every integer. For
u,v>0, the lifted trivialization is nonzero on all of C, so its effective zero
divisor is disjoint from C. Every nonzero effective divisor has positive
intersection with C; hence the divisor is zero and u=v. The cases with one
bidegree zero are single ruling lines. Thus no divisor class is omitted.

On the quadric cone, the resolution is the blowup of the vertex and the
pullback of its maximal ideal is O(-E). If C passes through the vertex, the
restriction of that ideal to the smooth curve is its full point ideal, not a
higher power. The blowup of a smooth curve at that invertible ideal is the
curve itself. Consequently the strict transform is isomorphic to C and
meets E with total intersection multiplicity one. If C avoids the vertex,
the intersection is zero. This justifies delta in {0,1}; it is not an
unjustified transversality assumption.

The intersection form on F2 gives the displayed genus formula. In the
vertex case, n=2r+1 and the integer subcanonical exponent forces n to divide
2g-2. Twice that expression is n^2-4n-1, so n=1. In the avoidance case,
n=2r gives class rH on the cone. In its divisor class group this is a Cartier
class, and the effective curve is a Cartier divisor linearly equivalent to
rH; its section lifts from the quadric. The exceptional curve itself cannot
be a strict transform of a positive-degree curve. Together with the ruling
case, this covers the relevant smooth integral curve classes.

The Chiodera–Ellia statement on printed page 419 expressly corroborates this
quadric fact. The author's independent proof addresses the singular-cone
detail that the short literature statement does not spell out.

## 6. Residual lci curve and fixed factors

The lift of a minimal degree-c equation has no divisorial zeros by exactly
the preceding irreducibility argument. Its top Chern class is positive, so
it cannot be nowhere zero. It has a pure lci curve as zero scheme, and
adjunction applies to this possibly nonreduced scheme. The degree and
canonical twist in the packet are correct.

For a reduced proper curve, global functions are constants independently
on its connected components. There are at most D components when the degree
is D, giving arithmetic genus at least 1-D. The required canonical degree
instead gives genus at most 1-3D, a contradiction. The argument does not
extend that lower bound to a nonreduced curve, and the packet does not do so.

For D=1 the degree formula forces a single degree-one generic component of
multiplicity one. Its support is a line. Any nilpotent excess would then be
supported in dimension zero, but a pure locally Cohen–Macaulay curve has no
such finite-length subsheaf. Thus Z would be the reduced line. This proves
the degree-one exclusion and the (4,4) consequence without assuming Z smooth,
connected, or reduced in advance.

For every m<=b, an equation not divisible by F_c meets the integral surface
properly in a complete-intersection curve of degree cm. Containment of C
then implies ab<=cm, contrary to c<a and m<=b. Zero equations and m<c are
harmless under the S_j=0 convention. This proves the full fixed-factor
identity, uniqueness in degree c, and the displayed degree-a dimension.

## 7. Flatness and singular-limit control

The matrix minors, signs, syzygies, and degree shifts are correct. The first
quadric is primitive and irreducible as a polynomial linear in x, and does
not divide the second. The ideal of maximal minors therefore has height two
and is perfect by Hilbert–Burch. The special ideal also has height two, so
t avoids the associated primes of the total Cohen–Macaulay quotient.
Torsion-freeness over the local DVR proves flatness near zero; no appeal to
constant Hilbert polynomial alone is made to infer it.

The central ideal really is the intersection of the plane cubic ideal and
the line ideal. The cubic is smooth, meets the line only at the stated point,
and has a distinct tangent direction there. The union is singular and its
cubic generator is essential. Its Cohen–Macaulay coordinate ring is saturated.
The generic CI is smooth because a t=1 smooth witness gives smoothness at
the generic parameter. Relative Jacobian smoothness supplies the needed open
neighborhood even without invoking flatness at an arbitrary parameter.

Additional independent exact computations verified:

- Saturating (q1,q2) by t gives precisely J.
- Saturating J by t leaves J unchanged.
- Eliminating an auxiliary variable from the two component ideals gives
  exactly the claimed special ideal.
- The t=1 symmetric quadric pencil has determinant
  -3u^4/16 + 3u^2/4 - u/4 and discriminant 1053/65536.
- Its determinant at infinity is nonzero. A singular point of the base
  intersection would force a repeated root of this determinant: at a rank
  three pencil matrix the derivative is a nonzero scalar times the second
  quadric on its kernel, while rank at most two makes the derivative zero.
  Thus the nonzero discriminant supplies a separate smoothness certificate.
- The plane cubic has unit Jacobian ideals on all projective charts over
  both F5 and F7. Properness of the projective singularity locus makes either
  good-reduction certificate sufficient for characteristic-zero smoothness.
- A genuinely singular reduction modulo 11 was detected as an expected
  negative control. No conclusion of smoothness in every characteristic is made.
- Standard-monomial counts give Hilbert function 1,4,8,...,48 through degree
  twelve, consistent with the all-degree Hilbert–Burch proof.

The KPR algebraic identity and its discrepancy in characteristic zero are
correct. Its role is only a warning against interchanging characteristic
change and flat specialization; it is not used to claim a lifting theorem.

## 8. Computation, sources, and reproducibility

The author program was replayed from a temporary unrelated working directory
in normal and optimized Python. Both outputs are byte-identical to the
frozen 43,052-check result. The independently written verifier adds 183,459
explicit checks in the full-input run, including 4,725 CI numerical types,
10,001 odd cone classes, 40,984 residual triples, the elimination checks,
the distinct smoothness certificates, and integrity/source checks. These
counts are arithmetic regressions, not proofs of the geometric statements.

Full local public corpus hashes and byte counts agree with the author
metadata and the immutable repository manifest. The selected problem is
unique, and the normalized upstream report hash matches. The entire local
DGF PDF hash and byte count match; its relevant lemma page was also visually
inspected. The AIM Problem 13 text was independently read via the primary
web source. The author-reported unsuccessful AIM byte retrieval remains a
limit; this audit neither claims possession of those bytes nor invents a
hash or a successful primary-page image inspection.

The full Ellia–Hartshorne 1999 chapter was not obtained or inspected. Its
bibliographic existence is supported by the AIM reference and book record.
No theorem or priority claim is attributed to uninspected chapter contents.
The other source uses were checked at their cited passages or abstracts,
without pretending to audit unrelated results in those works.

The matching repository queue entry and absent attempt directory were
independently checked at the recorded commit. Exact-ID branch/PR searches
and the selected code searches again returned no matches. Such searches
remain bounded observations; they do not prove absence of unindexed work.
Likewise, this audit is not an exhaustive current-literature status search.

## 9. Corrections, limitations, and publication boundary

No mandatory correction was identified. Two precision points should remain
explicit in any shortened presentation: the Serre bundle is an absolute
construction on the special P3, and the degree-one argument requires the
purity supplied by the lci zero-section construction. Both requirements
are already met in the full proof.

The remaining problem is to exclude or realize a smooth subcanonical
non-CI curve with 3<=c<a, together with an actual embedded smoothing to
CI(a,b). This audit provides no such exclusion or realization. Negative
arithmetic genus of a nonreduced auxiliary curve is not a contradiction.

The verdict approves the original frozen packet only at its declared
partial-progress scope. It must not be presented as solving AIM Problem 13,
certifying global novelty, or certifying that no solution exists elsewhere.
No remote mutation was performed. No scholarly PDF, extracted source text,
raw dataset, selected record, or private coordination file is included in
the independent audit deliverables.

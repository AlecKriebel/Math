# Independent CM/Hodge verification of PR 799 / problem 30002364

Audit date: 2026-10-16 UTC. Authenticated candidate head:
`cc45ec9dc93515593c3b2a228def86c3a562e13f`.

## Finding and scope

Within this mathematical family, the corrected forward construction passes.
It supplies a simple CM eightfold A over Qbar with divisor-generated Hodge
classes on every power, and a geometrically simple reduction A0 in
characteristic 5 with non-Lefschetz Tate classes in H4(A0,Q_l(2)), for every
l different from 5. The verified dimensions in that degree are 32 for Tate
classes and 28 for divisor products. I found no missing central hypothesis
in the CM realization, all-powers Hodge argument, or reduction endomorphism
argument. This is verification of the completed candidate, not a sixth
proof search, a formalized proof, a priority determination, or human review.

The corrected converse gives a class of varieties uniformly at every prime:
CM elliptic curves. Its conclusion already holds for every member of the
class, independently of the reduction. That is a logically valid, elementary
answer to the existential question; it is not a new nontrivial comparison
theorem. The separately attributed splitting result is a theorem about
specified pairs (A, prime). The original proof did not make this distinction
as clearly; the corrected proof does.

The target-only strategy was written before candidate or historical-review
material was read. Source bodies are excluded scratch. The reading ledger
states exactly which passages were inspected. In particular this audit did
not inspect final CCO Proposition 2.1.4.2 or Dodson's original rank definition.
The direct proof below does not depend on either passage.

## 1. Actual CM realization and reduction

Write K=Q(sqrt(6)). Eisenstein gives [Q(a):Q]=4 for
a=sqrt(3+sqrt(6)). If sqrt(3) were in Q(a), then Q(a)=K(sqrt(3)).
Writing a=u+v sqrt(3) over K forces uv=0. The two resulting possible squares
in K have norms 3 and 1/3, respectively. Neither is a rational square,
contradicting multiplicativity of the norm of a square. Since ab=sqrt(3),
adjoining b doubles the degree. Thus L=Q(a,b) is totally real Galois of
degree 8 with the displayed D4 root action. Consequently E=L(i) is a
degree-16 CM Galois field, with central conjugation c fixing L.

Every one-per-conjugate-pair subset Phi is a realizable polarized CM type.
For completeness, take the lattice O_E in E. Weak approximation in L
provides t with prescribed signs at its eight real embeddings. For the
displayed Phi choose those signs so that alpha=i*t has positive imaginary
part at each selected embedding. The alternating trace form
Tr_{E/Q}(alpha*x*c(y)), with its sign fixed by the complex-structure
convention, is a rational Riemann form; multiply by a positive integer to
make it integral on O_E. The complex torus C^Phi/Phi(O_E) is therefore an
abelian variety with O_E action. This is also Milne CM, Example 2.11 and
Proposition 3.12. Proposition 7.9 gives descent to Qbar, hence a number field
for the variety and its finitely many chosen endomorphism generators.

At 5 the specified simple root a=2 and i=2 lift by Hensel's lemma into Q_5.
The element b lies in its unramified quadratic extension because its residue
square is 2. The residue Frobenius fixes a and i and sends b to -b, so the
chosen prime of E has decomposition group {1,s}. The polynomial
discriminant excludes ramification at 5. This describes a place of E,
not a pre-existing good-reduction model. Milne CM Proposition 7.12 permits
a finite extension of a field of definition to obtain good reduction above
this place. The E-action extends to the abelian scheme and specializes
faithfully. All conjugates of E are contained in the coefficient field
because E is Galois; O_E already acts. Milne CM Theorem 8.1 therefore
applies and supplies an actual Frobenius pi in O_E. Normalized slopes are
unchanged by further finite base extension, as also checked in Conrad
Theorem 2.1 and Remark 2.2. The Weil property gives pi*c(pi)=q.

## 2. All powers and the characteristic-zero endomorphism field

For each h in H=D4, write d_h=m_h-m_ch for the multiplicity difference
in a split exterior monomial of H^{2r}(A^n)(r). The smallest rational torus
containing the Hodge cocharacter contains all its Galois conjugates.
Conversely their span determines that torus. Centering removes the weight
direction, so its invariance equations are precisely M*d=0. The independent
finite calculation obtains det(M)=256 and centered/full ranks 8/9. The
Mumford-Tate torus is therefore

    T={x in Res_{E/Q} G_m: x*c(x) is a rational scalar}.

Its sixteen coordinate characters are distinct. Its commutant on H1 is
the diagonal algebra after splitting coefficients, of rational dimension
16; it contains E, hence equals E. A rational map of H1 preserving the
Hodge structure becomes a map of the integral lattice after clearing
denominators. It is complex linear on the universal covering torus and
therefore a holomorphic homomorphism of complex tori; for abelian varieties
this is algebraic. Thus End0(A)=E. A nontrivial isogeny decomposition would
give a nontrivial idempotent in E, impossible in a field. Simplicity and
primitivity are conclusions, not assumptions used to realize Phi.

For every n and r, invertibility of M gives d_h=0 at every h. In a balanced
exterior basis monomial, pair each occurrence of h with an occurrence of ch.
Their wedge pairs are degree-two invariant monomials, including pairs from
different factors of A^n. Their product recovers the original monomial up
to a nonzero sign. Thus the entire invariant algebra is generated in
degree two for every power. The rational degree-two Hodge subspace is the
divisor subspace by Lefschetz (1,1). The invariant subspace and the image
of the multiplication map are rational subspaces, and scalar extension
commutes with kernels and images. Equality over the splitting field
therefore descends to Q. No unjustified assertion that an individual
split eigenline is rational is needed.

## 3. Frobenius torus and the changed-Lefschetz-group trap

Milne 2001 Appendix A.8 defines Phi through H^{1,0} and the local fiber
by sigma^{-1}P=v. At v=tP, evaluating h(pi) means evaluating pi at
h^{-1}tP. The embeddings in that fiber form D*t^{-1}*h, so the slope is

    #(Phi intersect D*t^{-1}*h)/|D|.

This establishes the left/right convention before comparing ranks. My
checker computes the fibers as actual right cosets, independently of the
submitted averaging function. It gives centered/full slope ranks 4/5,
sixteen distinct centered embedding columns, and Newton multiplicities
0^6,(1/2)^4,1^6. Local degree is two, so its product with every slope is
integral; there is no division-algebra invariant obstruction to End0=E.

Distinct columns prove more than distinct Frobenius eigenvalues: if
h(pi)^m=k(pi)^m for any m>0, their quotient is a root of unity and all
valuations agree, forcing h=k. Thus Q(pi^m)=E for every m. Base change
identifies H1(A0,Q_l) as a rank-one E tensor Q_l module. The commutant of
pi^m has dimension 16 and is exactly E tensor Q_l. Tate's original 1966
Main Theorem identifies it with End0 over F_{q^m} tensor Q_l. Every
geometric endomorphism is defined over a finite extension, so geometric
End0(A0)=E. A0 is geometrically simple.

This step is indispensable. In general the reduction has more endomorphisms,
so its Lefschetz group may be smaller. Merely comparing characteristic-zero
CM rank to slope rank would not establish the target conclusion. Here
both centers and both Lefschetz norm-similitude tori are E and T, whereas
the Mumford-Tate and Frobenius dimensions are 9 and 5. The direct divisor
analysis in the next section makes the conclusion independent of using a
general all-powers torus-equivalence theorem.

## 4. An actual Tate class outside divisor products

For a normalized Frobenius product of weight zero, vanishing valuations
at every place over 5 are equivalent to its being a root of unity. In
the nontrivial direction, pi and q/pi are integral, hence units away from
5. The normalized product is a global algebraic unit with all archimedean
absolute values one, so Kronecker applies. This also verifies the source's
finite-extension definition of Tate classes; eigenvalue one in the original
field of definition is not required.

The displayed e=(0,1,0,1,0,-1,0,-1) lies in the slope kernel. Therefore
R=r(pi)*r^3(pi)/((rs)(pi)*(r^3s)(pi)) is a root of unity. The four
distinct split eigenlines r,r^3,crs,cr^3s have nonzero exterior product
in H4(2), with eigenvalue R. It becomes fixed over a finite extension.

A degree-two wedge is Tate exactly when its two centered columns add
to zero. The exact enumeration gives only the eight conjugate pairs.
These have normalized eigenvalue exactly one. They span the whole degree-two
Tate space and, by Tate for divisors, the divisor space. Products of two
divisors are the 28 distinct exterior basis lines consisting of two
conjugate pairs. The four labels of the witness contain no conjugate pair,
so its basis line is outside this image. Enumerating all 1,820 quartics
finds 32 Tate lines, with four exceptional lines:

    (0,2,12,14), (1,3,13,15), (4,6,8,10), (5,7,9,11).

Here labels 0..7 are H and 8..15 are cH. The exceptional family is
Galois stable. For a fixed cohomological degree there are finitely many
root-of-unity eigenvalues, so one finite extension kills all their orders.
The fixed kernel and divisor-product image are Q_l subspaces whose scalar
extensions are the spaces just calculated. Strict containment descends to
Q_l for every l different from 5. The argument concerns cohomology; it
does not claim a nonalgebraic cycle or a failure of the Tate conjecture.

## 5. Target quantifiers, boundary checks, and literature conflict

One valid good reduction violating the conclusion disproves the unrestricted
forward question. Failure on A0 itself implies failure of the property
on all its powers. A is CM type over Qbar, and potential good reduction
followed by finite extension is legitimate in this formulation. The
nonabelian E and nontrivial decomposition group do not satisfy Sugiyama's
abelian-field or complete-splitting hypotheses.

For every CM elliptic B, the split Hodge representation has two conjugate
characters. On B^n an invariant monomial uses them equally often and
factors into degree-two invariants, so every power is Hodge-Lefschetz.
For every B in that nonempty class and every reduction B0, the converse
implication therefore holds. The premise contributes no information in
this example. Sugiyama Theorem 0.1(2)(b), inspected in the preprint,
instead supplies an informative bidirectional comparison when the chosen
prime is unramified of absolute degree one in the Galois closure of
End0(A). For this Galois closure that means complete splitting. The OWR
reflex-field wording was independently read but is not silently substituted
for the preprint's hypothesis.

Meaningful controls reproduce centered rank 8 at a trivial decomposition
group. A decomposition group containing c gives rank zero and coincident
columns, exactly where the same-End0 argument must fail. A supersingular
CM elliptic reduction is the conceptual boundary example: its new
quaternionic endomorphisms prevent using its characteristic-zero CM
Lefschetz torus unchanged. Repeated eigenlines and nonsimple products are
not covered by the distinct-column lemma; the actual candidate avoids
both cases. Characteristic 2, bad models before field extension, and
l=p are not claims of this construction.

Angle ranks Remark 3.5 was read in the primary v3 PDF, together with its
absolute-simplicity setup and exclusion of supersingularity. No ordinary
or canonical-lift restriction was found in those passages. The candidate
satisfies the stated setup; its Frobenius field and its Galois closure
are both E. The source's unqualified equality of lift rank and slope
rank conflicts with the directly verified 8 versus 4 centered orbit
dimensions. Adding the weight direction gives 9 versus 5 and does not
repair the concluding equivalence. The averaging formula itself is
supported by independently inspected Milne and Conrad passages. The
unsupported inference is that averaging preserves the orbit-span rank.

No central gap remains in this family's mathematical check. Priority,
the exact final CCO and Dodson passages, and the full current erratum
history remain separate review needs. This report does not call the
construction new or the literature correction author-approved, and it
does not infer anything about the rest of the Angle ranks paper.

## Reproducibility and trust boundary

The finite checker uses signed two-by-two integer matrices and direct
embedding fibers. It imports none of the submitted code. It certifies
finite group, matrix, exterior-basis, and boundary calculations. The
geometric steps above remain ordinary mathematical deductions using the
identified standard theorems. The sealed bundle is closed by its manifest
and an externally supplied SHA256 for both manifest and launcher. Verify
the launcher's bytes before executing it; self-hashing cannot authenticate
untrusted code before its first instruction. The control receipt covers
normal and optimized execution, relocation, hostile import environment,
and rejection of tampered files/manifests and symlinks. This assumes a
trusted interpreter/standard library and no concurrent filesystem races.

# Independent source review: 30002709

**Verdict: PASS_COMPLETE_CREDITED_CHARACTERIZATION.**
The proposed **already_solved, 0/5** disposition is supported. No mandatory
correction is required. Datta's theorem gives the full characterization requested
by the original source, with the local defect convention made explicit.

This verdict binds:
- KNOWN_RESULT.md SHA256
  `0731e16b135ec29c05e84811dc07462bf17fd7a2799b867fd6c3909fcf7b63d9`
- FROZEN_MANIFEST.json SHA256
  `7cc8aad30432a9fc0ca405fbd0be3c4c7f19a94b47a9fa066267ee6610348834`

The reviewer did not contribute to the author's source route. All thirteen
bound author files and four full primary PDFs match their hashes. The author
receipt replays byte-for-byte with 7,173 controls. A separately authored checker
passes 32,010 exact convention controls. The result is an established theorem;
finite checks do not prove the general valuation-ring classification.

## 1. Exact original question

I read the full Novacoski contribution in OWR49/2014, printed pp.2798–2800,
and visually inspected the question and invariant display. Its second question
explicitly removes the preceding finite-inertial hypothesis. It asks when the
chosen valuation ring in a finite extension can be written as a finitely
generated algebra localized at its contracted maximal ideal. The subsequent
necessary condition and special-case sufficiency make the characterization
purpose clear.

The bare extracted sentence, if interpreted as an assertion for all finite
valued-field extensions, is not universally true. The author's classification
answers the richer original question and explains that negative reading as
well. It does not replace the target by an inertial, separable, characteristic-zero,
rank-one or function-field special case.

## 2. The exact theorem and its scope

Datta's Theorem1.2 in the complete arXiv2101.08337v2 manuscript, pp.2 and11,
starts with an arbitrary finite field extension and a chosen valuation of the
upper field restricted to the lower one. These give precisely the local
valuation-ring inclusion in the OWR question. Local rings are explicitly allowed
to be non-Noetherian. No extra separability or residue-field restriction is
present.

Writing V for the base and W for the selected extension, the theorem gives

    W essentially finite type over V
    iff W essentially finite presentation over V
    iff [Frac(W^h):Frac(V^h)] = e*f and epsilon=e
    iff W^h finite over V^h.

The manuscript also includes an equivalent essentially-finite-type henselian
condition and proves the stronger finite-subalgebra localization conclusion
used by the author. The notation conversion from Datta's L/K to the report's
F/L is consistent throughout.

The publisher verifies Math. Nachr.296 (2023),1041–1055 and first publication
5January2023. The independently inspected arXiv metadata identifies the
24September2024 v2 as updated to match the journal. The actual proof access
was the complete revised author manuscript; no typeset journal PDF is falsely
claimed to have been read.

## 3. Local defect, splitting and the initial segment

The OWR image really prints the total field degree in each branch's displayed
defect, while simultaneously allowing multiple extensions. That cannot serve
as the general local defect. Datta Definition4.8 and the earlier
Cutkosky–Novacoski definitions use compatible ordinary henselizations and
isolate the chosen field factor. The correction is necessary and clearly
identified, not silently inserted.

For a unique extending valuation the tensor product with the henselian base
has a single field factor, so its degree equals the total field degree; otherwise
one must not substitute the total degree for that selected factor's degree.
Henselization preserves the residue fields and ordered value groups here.
Completion and strict henselization are different operations and are not used.
The residue degree includes its inseparable part.

The initial index counts nonnegative upper values strictly below *every*
positive base value. Those values represent distinct quotient classes, giving
epsilon<=e. Merely selecting a nonnegative representative of each coset is
much weaker. For example, in lexicographic Z^2 over mZ x nZ the index is mn
but the initial segment has n elements. The author avoids the overly loose
introductory shorthand found in one sentence of the preprint and uses the
precise definition. Dense rank-one base groups similarly can have epsilon=1
while e>1.

Trivial valuations are included: finite algebraic extensions have trivial
extended value group, e=epsilon=1, and residue degree equal to field degree.
There is no excluded boundary case hidden in the criterion.

## 4. The full sufficiency proof was checked

I read Datta's complete Sections3–5, not just the theorem or abstract.
The key points in the author's proof map are valid:

1. Start with the integral closure A of V in the finite upper field. It need
   not be finite over V, but it has finitely many maximal ideals.
2. After tensoring with V^h, Proposition3.6 decomposes A into the henselized
   local branches. Normality, the finite set of minimal primes, and the
   maximal/minimal-prime pairing supply actual domain factors.
3. Corollary3.7 chooses finite V-subalgebras B with the full upper fraction
   field and separating the finitely many maximal ideals. This family is
   filtered and exhausts A. The separating condition is important: it
   identifies the matching local factors and ensures that their maps are
   injective. One cannot simply assume every localized tensor map is injective.
4. For the selected factor, W^h is the filtered union of these injected local
   base changes. If W^h is finite over V^h, its finitely many module generators
   all lie in one stage. That stage already contains V^h and consequently
   equals W^h. No Noetherian stabilization of an arbitrary ascending chain is
   invoked.
5. The henselization of B at the contracted maximal ideal is this valuation
   ring. Faithful flatness and the cyclic-purity criterion of Lemma4.6
   descend the valuation-ring property. Its fraction field is the full
   upper field. W dominates it, so maximality of valuation rings under
   domination makes the two local rings equal.
6. Thus W is the required localization of a finite V-algebra B. Such B is
   torsion-free and flat over V; the cited finite-presentation result applies.
   The proof uses flatness, not the false assertion that every arbitrary
   torsion-free valuation-ring module is free. Finite torsion-free modules
   are free, and the final finite B also has that stronger property.

For the other implications, Knaf's necessary condition was checked in
Cutkosky–Novacoski Theorem4.1, including the contracted-prime localization
and henselian compositum step. Their classical unique-extension criterion
(Corollary2.2) supplies the finite henselian extension when the two numerical
conditions hold. The author attributes these inputs correctly. This is a
full applicability/proof audit of a published theorem, not a claim to have
reproved the entire cited commutative-algebra literature from first principles.

## 5. The precise localization and global distinction

If W=S^{-1}V[a_1,...,a_r] inside the chosen valued field and
p=V[a_1,...,a_r] intersect m_W, S avoids p. Conversely, every element outside
p is a unit in W. The two universal localization inclusions therefore give
W=V[a_1,...,a_r]_p, exactly the expression asked for in OWR.

The finite B in the theorem is not asserted equal to W as an unlocalized
module. Conditions at all valuation extensions characterize finiteness of the
whole integral closure. Conditions at the one selected branch characterize
this local essential-finite-generation problem. The author does not interchange
these quantifiers. The earlier Kuhlmann–Novacoski finite-inertial result already
allows essential generation despite examples failing finite algebra generation;
Theorems1.3 and1.5 confirm that distinction.

## 6. Diagnostics and the negative reading

For the split-prime diagnostic, X^2-6 has two simple roots modulo5.
Hensel's lemma over the ordinary henselian base lifts the chosen root. Its local
field degree is one, even though Q(sqrt6)/Q has total degree two. At the branch
sqrt6=1 mod5, sqrt6+1 is a unit and

    (sqrt6-1)(sqrt6+1)=5.

The selected localization of Z_(5)[sqrt6] has principal maximal ideal (5),
is one-dimensional and Noetherian, and is a DVR. Thus it is the valuation
ring for that branch and is essentially finite type. Its e=f=epsilon=d=1
uses the local degree. The total-degree quotient would incorrectly equal two.

As an additional check of the same diagnostic, 1/(sqrt6+1)=(sqrt6-1)/5
lies in that selected local ring but has trace -2/5 and norm -1/5, so it is
not integral over Z_(5). This confirms why the local ring need not be a finite
module over the base despite being a localization of a finite algebra.

The cited Cutkosky–Novacoski Example2.5 distinguishes a branch with e=2,
epsilon=1,d=1 from one with e=epsilon=d=1. Knaf's necessity excludes essential
finite generation for the former. The author's careful wording is important:
it cites the stated extension and does not assert irreducibility of the
example's cubic for every base field with the same value group. Nothing in
this review promotes that overstrong version.

## 7. Disposition and reproducibility

The exact characterization is known, so the dated imported partial-progress
assessment is obsolete. `already_solved0/5` is supported, with Datta, Knaf,
Cutkosky–Novacoski and Kuhlmann–Novacoski retaining their credits. No new
mathematical discovery, local-uniformization solution, or historical priority
claim is justified or made.

The separate checker uses exact rational ordered-group calculations, an
independent Newton-correction implementation for both split roots, the
quadratic-field inverse trace/norm, and local-versus-total-degree controls.
All 32,010 assertions pass. The author's 7,173-control receipt was reproduced
from a separate copy. These are elementary convention diagnostics; the full
classification rests on the verified written theorem and proof.

The frozen author files are unchanged. Seven portable review files accompany
this report; reading inputs, PDFs and page images are excluded. The parent
retains the publication gate.

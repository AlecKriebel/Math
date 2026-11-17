# Independent original-only initial reconstruction

UTC: 2026-11-17T13:42:00Z (draft checkpoint; see log and seal for terminal time).
Status: INITIAL ONLY. This is neither a scientific clearance nor a final verdict.
Initial-gate work: 100% upon sealing. Estimated complete scientific review: 20%.

## Exact target and evidence boundary

The controlling manuscript is the 95-line, 12344-byte original `main.tex` in
`archives/02-thompson-cstar-source.zip.extracted`, together with the native outer
four-page `paper.pdf`. I personally read the entire TeX, the fresh complete PDF
text, and each of four freshly rendered pages individually. The title, abstract,
theorems, proofs, disclosure and bibliography agree in mathematical scope across
these presentations. No supplementary proof, audit, code or primary source has
been read in this gate. Original author descriptions of audits and formalization
are recorded exposures, not evidence that their conclusions are correct.

Write N for the assertion that the particular standard dyadic PL group F is
nonamenable. The manuscript's target is the following consequence of N:

1. For each discrete H in {F, T, full Aut(F), full abstract Comm(F)}, C*_r(H)
   is simple and has one tracial state, the coefficient-at-identity trace.
2. For every countable subgroup G of Homeo(S^1) containing the specified
   standard circle action of F, the same conclusion holds for C*_r(G).

The paper also asserts conditional equivalences and inherited facts: N is
equivalent to the simplicity assertions in its Theorem 1; T already has unique
trace without N; the used reductions are old; the new nonamenability input is
attributed to OpenAI. These subsidiary attribution and theorem-scope claims
remain to be checked against actual primary proofs after authorization.

Its new-input dependency is explicit in the abstract, Corollaries 3 and 4, and
disclosure. In an original-only gate N is an unverified premise, not a proven
fact. A bibliographic pin, statement, manual-audit assertion or source inventory
does not discharge N. There is no independent nonamenability proof in these four
pages. The finite deductions below do not transfer the truth of N into this gate.

Success requires (a) the exact standard F identification for the actual pinned
nonamenability proof; (b) actual validity of that proof; (c) the stated full-group
and countable-action simplicity reductions with all their hypotheses; (d) the
discrete reduced-group-algebra trace theorem; and (e) the elementary countability
and norm-density interfaces. Failure of any needed premise leaves the dependent
claim unverified. No finite numerical experiment would settle (a)-(d).

## Hand reconstruction: countability without changing the groups

Dyadic rationals and integer powers of two are countable. A PL element of F or T
is encoded by a finite list of breakpoints and finite dyadic linear data. The
union over all finite lengths is countable. This proves countability directly
from the definitions, without assuming nonamenability.

For the next statements, retain the explicitly exposed premise that F has a
finite generating set S of size r (the original cites a two-generator fact; its
primary proof is not read here). An automorphism is determined by the r images
of S, so Aut(F) injects into F^r and is countable. This argument concerns the
full abstract automorphism group; it does not discard orientation reversal.

For a finitely generated countable group K and a fixed index n, every subgroup
of index n occurs as the stabilizer of a point in some labelled transitive action
K -> S_n. There are at most (n!)^r homomorphisms specified by generator images
and n point stabilizers per action, hence at most n(n!)^r such subgroups. This
crude finite bound suffices; duplicates do not matter. The union over n >= 1 is
countable. Index 1 is included rather than silently omitted.

For each finite-index subgroup H, choose right-coset representatives t for H\K.
For x in S union S^{-1}, the elements t x (overline{t x})^{-1} lie in H and
generate it: rewriting a word one letter at a time telescopes the chosen coset
representatives. Thus H is finitely generated with at most 2rn listed generators.
For every ordered pair H,J, a homomorphism H -> J is determined by finitely many
images in countable J, so there are at most countably many such homomorphisms.
Isomorphisms form a subset. Taking a countable union over ordered pairs and then
quotienting by the commensurator equivalence relation preserves countability.
This validates that interface conditional on finite generation, independently
of any asserted faithful line realization. It does not prove that the full
abstract commensurator is the precise group in the cited simplicity corollary.

## Hand reconstruction: trace and the sole density passage

For finite sums a=sum a_g lambda_g, the coefficient at e gives
tau(a^*a)=sum |a_g|^2 >= 0, tau(1)=1, and tau(ab)=tau(ba), since gh=e iff hg=e.
Equivalently tau(a)=<a delta_e,delta_e> is a norm-one positive functional on
C*_r(G); positivity follows directly from tau(a^*a)=||a delta_e||^2 for arbitrary
a. The trace identity extends by norm continuity from the finite group algebra.

Assume exactly the imported BKKO vanishing statement: every tracial state phi
satisfies phi(lambda_g)=0 for g outside the amenable radical. If that radical is
{e}, then phi(lambda_e)=1 and phi(lambda_g)=0 for g != e, hence phi(b)=tau(b)
on every finite sum b. Given arbitrary a and epsilon>0, norm-density supplies
b with ||a-b||<epsilon. Since both functionals have norm one,
|phi(a)-tau(a)| <= |phi(a-b)|+|tau(b-a)| <= 2 epsilon.
Therefore phi=tau. No exchange of differentiation, integration, pointwise limit
or nonuniform infinite sum is needed in this final density step. The imported
vanishing theorem and C*-simplicity-implies-trivial-radical theorem themselves
are not proved by this estimate and remain separate interfaces.

The logical dependency graph is N -> the four simplicity assertions via the
two asserted Le Boudec--Matte Bon equivalences -> trivial radicals -> unique
traces via the asserted BKKO statements. For the circle package it is N plus
standard faithful action plus countability -> imported action criterion -> the
same trace chain. No step may be replaced by 'every nonamenable group is
C*-simple' or 'every C*-algebra that is simple has a unique trace'. Neither is
the premise asserted or established here.

## Own attempts to break scope and boundary assumptions

**Abstract overgroup trap.** For any nonamenable H, the abstract overgroup
H x C_2 contains H. In its reduced algebra, with z the nonidentity central
involution, p=(1+lambda_z)/2 is a central projection: p^2=p, p^*=p, and both
p and 1-p are nonzero by applying them to delta_e. The ideal p C*_r(H x C_2)
is nonzero and proper, since multiplication by 1-p annihilates it. Thus
nonamenability of a subgroup alone cannot imply C*-simplicity of all abstract
overgroups. This is a concrete falsification of an overbroad transfer rule,
not a counterexample to the manuscript's specified circle-action claim.

**Why that trap does not immediately refute the actual action claim.** A useful
local element of standard F is
f(t)=t/2 for 0<=t<=1/2; f(t)=t-1/4 for 1/2<=t<=3/4; and f(t)=2t-1 for
3/4<=t<=1. It is continuous, increasing, fixes the endpoints, has allowed slopes
and dyadic breakpoints, and moves every point of (0,1). For any interval
I=[a,a+2^{-k}] inside (0,1), with dyadic a, its affine conjugate on I, extended
by identity off I, is again in F. The factors 2^k and 2^{-k} cancel in the
slopes; every transformed breakpoint remains dyadic. Consequently every circle
arc contains a nontrivial such local element, even when the arc crosses the
identified endpoint (choose a smaller interval avoiding that point).

In fact the centralizer of this standard F in Homeo(S^1) is trivial. If h moves
some point, choose a small open U with U disjoint from h(U), then choose the
above nontrivial local f supported inside U. If h commuted with all of F, then
h f h^{-1}=f, but their moved sets lie in the disjoint sets h(U) and U, which
is impossible for nontrivial f. Thus H x C_2 with H acting as the standard F
cannot supply a faithful standard-action counterexample: the extra central
involution would have to act trivially. This does not prove the general action
criterion, which is an explicitly unresolved imported theorem.

**Local nonamenability interface.** If N is granted, the affine construction
embeds a copy of F in every nonempty open arc's rigid stabilizer. An amenable
group cannot contain a nonamenable subgroup: an invariant mean restricts by
choosing coset representatives and extending bounded subgroup functions
equivariantly. Thus these stabilizers are nonamenable conditional on N. The
existence of an embedded subgroup is not itself the C*-simplicity criterion.
The actual hypotheses and proof of the cited Theorem 3.7 must be inspected;
faithfulness, countability, topological hypotheses and possible extra dynamical
conditions may not be supplied by a headline citation.

**Finite, trivial, and full-algebra controls.** The trivial group has algebra C,
so the manuscript's warning about full group algebras must retain 'nontrivial'.
For any nontrivial G, let u_g be the universal unitary and epsilon its
augmentation character. u_g-1 (g!=e) is a nonzero element of ker epsilon:
its regular image sends delta_e to delta_g-delta_e, of norm sqrt(2).
The kernel is proper because epsilon(1)=1. Hence the full algebra is not simple.
Moreover epsilon(u_g)=1 and (tau_r composed with the regular quotient)(u_g)=0,
so it has two distinct tracial states. For C_2 the reduced algebra already has
the above nontrivial central projection; N cannot be casually deleted from a
general simplicity inference. All target groups are nontrivial.

**Abstract simplicity is a separate property.** In F the endpoint slope map
f -> (log_2 f'(0+), log_2 f'(1-)) is a homomorphism to Z^2: the one-sided chain
rule multiplies endpoint slopes, and logarithms add. The displayed f has image
(-1,1), while every nontrivial local element strictly inside (0,1) has image
(0,0). The kernel is therefore a nontrivial proper normal subgroup. This is an
independent elementary control on the distinction the original states.

**Orientation, topology and quantifier tests.** The targets use full Aut(F) and
full Comm(F), not their orientation-preserving index-two parts. Countability
survives taking the full groups, but a theorem about only a subgroup would not
establish their simplicity. The exact cited full-group identification must be
checked. Homeo(S^1) permits orientation reversal; its intended convention and
the source theorem's convention must coincide. The algebra uses the discrete
topology regardless of any homeomorphism topology. Replacing it by a
topological-group reduced algebra would change the question. The circle claim
includes G=F and G=T, every countable faithful standard-action overgroup, and
finite extensions meeting these conditions; an arbitrary abstract embedding
and an uncountable overgroup are outside the stated quantifier. A finite
quotient of G by itself does not create a reduced-algebra augmentation; the
abstract-overgroup counterexample above uses an actual central finite normal
factor and a displayed ideal.

**Prior T trace.** Given the separately asserted facts that T is abstractly
simple and nonamenable, its amenable radical, being normal, is either {e} or T;
the latter contradicts nonamenability. The imported trace theorem would then
give unique trace without N. This is a valid conditional reconstruction, not
verification of the assertions about T or the historical attribution.

## Exact remaining interfaces and stopping boundary

I have not read or checked the actual pinned OpenAI nonamenability proof,
formal source, its dependencies or proof-to-standard-F identification. I have
not read the actual Le Boudec--Matte Bon proof bodies for Theorems 3.7, 4.1,
4.3 and Corollaries 4.2/4.4, including their countability, orientation and
full-group hypotheses. I have not checked BKKO's actual proofs or numbered
theorems, the finite-generation reference, the faithful line realizations, or
the original prior-status proofs and publication/edition numbering. These are
scientific interfaces, not merely bibliographic tasks. No claim that the
imported central difficulty has been solved follows from the local arguments.

The strongest artifact in this gate is the explicit conditional reconstruction
and finite hand controls above. They isolate where the author's conclusion
would follow and where actual primary proof verification remains essential.
This gate makes no final scientific verdict, promotion decision, priority claim,
recommendation for a weaker publication, or follow-up assignment. Stop after
freezing. Any further work requires root checkpoint and explicit RESUME in a
new sibling namespace; this INITIAL namespace will remain immutable.

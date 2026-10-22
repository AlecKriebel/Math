# Independent audit of Dini space realization partial results

Problem 30002395 / OWR-12591-005. Audit date: 2026-10-07 UTC.

Verdict: ACCEPT the five scoped partial results after the supplied one-sentence correction, applied in both PROOF.md and TURN_2.md. The universal realization problem remains UNSOLVED, with 5/5 substantive approaches completed. The original packet is preserved. This is an independent mathematical and computational review by an AI reviewer, not human peer review or proof-assistant certification.

Frozen input manifest SHA-256: 5d4700cf4699eea9443dbd40b268839f77404cb701bb15976efdb02bb1861c3a.

Frozen input PROOF.md SHA-256: 3f9686c459bfdcfe0ede72ef21c102d74c9f3c6fd5f019ab263aca762cdcedb4.

The review covered the complete authored proof, all five turn files, source metadata, both author programs, and the recovered independent checker. Every turn file was verified to occur verbatim in the original full proof. Required primary statements were checked against locally available PDFs and the current public source pages. Source inspection boundaries are stated below and in SOURCE_AUDIT.json.

## 1. Target and acceptance boundary

The intended question concerns sober, second-countable, locally quasicompact T0 spaces and primitive ideal spaces of separable amenable complex C*-algebras. Amenability is used in its C*-algebra sense, equivalently nuclearity. The zero algebra handles the empty space. Sobriety cannot be omitted: the countable infinite cofinite space is T1, second countable and locally quasicompact, but its whole space is irreducible closed without a generic point. The manuscript correctly excludes that artificial negative answer.

Acceptance covers the five stated sufficient conditions, worked realization, reductions and construction obstructions. It does not establish that every Dini space is realizable, that some Dini space is nonrealizable, or that these consequences are new. Harnisch–Kirchberg's realization characterization is an explicitly credited external theorem. Its complete operator-algebraic proof and the general amenability/nuclearity equivalence were not re-proved here.

The partial results survive the correction. The only false standalone statement found in the original authored proof is the unqualified ambient-openness sentence identified next. Its following argument already uses the correct relative-image topology, and the Baire-space application separately supplies surjectivity.

## 2. Required correction and non-surjective countercontrol

Location: Turn 2, paragraph beginning with the T1 target assertion, in both PROOF.md and TURN_2.md.

The corrected statement is: a continuous pseudo-open map into a T1 space is open onto its image; surjectivity makes it open into the whole target. CORRECTION.patch makes exactly this change. The corrected directory contains the full author packet with only these two mathematical text changes and a regenerated manifest. The other eleven author files are byte-identical.

Proof of the corrected assertion: for f:Q->P with P T1, its pseudo-graph is R={(q,r):f(q)=f(r)}. If V is open in Q, the set R intersect (Q times V) is open in R. Its first projection is f^{-1}(f(V)), so pseudo-openness makes that saturation open. It is R-invariant. The invariant-image requirement says its image f(V) is open in f(Q). When f is onto, f(Q)=P. A pseudo-epimorphism into a T1 target is onto, because its image must have dense intersection with each closed singleton.

A complete counterexample to the unqualified sentence is Q={q}, P=R with the usual topology, f(q)=0. The map is continuous. Its pseudo-graph is the singleton {(q,q)}, whose first projection is open. Its only invariant open sets are empty and Q, with images empty and {0}, both open in the image subspace {0}. Therefore f is pseudo-open. But the image of the open set Q is {0}, which is not open in R: for every real r>0, r/2 lies in (-r,r) and differs from zero. The map is not pseudo-epimorphic, since it misses the closed singleton {1}.

The written all-radii argument is the negative proof. The extra checker exhausts the singleton domain conditions and checks 128 exact rational instances of the displayed neighborhood witness. Those finite instances are regressions, not certification of the entire real-line topology.

The main Turn 2 obstruction is valid after this correction. A continuous open surjection from locally quasicompact Q onto Hausdorff P sends a quasicompact neighborhood to a compact neighborhood: the image contains an open neighborhood and is compact, hence closed in P. The construction can be made inside any prescribed open neighborhood by taking its preimage first. Every basic cylinder in N^N is closed and has an open cover by its infinitely many next-coordinate cylinders without a finite subcover. Any compact neighborhood would contain such a closed cylinder, a contradiction. Thus N^N has no continuous pseudo-open pseudo-epimorphic presentation from a locally quasicompact space. This disproves the proposed universal auxiliary repair, while N^N itself is correctly excluded from Dini inputs.

## 3. Turn 1 and Alexandrov realization

All hypotheses of the realization criterion are met for a countable sober Alexandrov T0 space X. The discrete space on the same set is locally compact and Polish. Its identity map induces an injective top/bottom preserving map on open sets. Arbitrary unions and arbitrary lattice infima are preserved because arbitrary intersections are open in both spaces.

The countability point is correct: in a second-countable Alexandrov T0 space, the minimal open neighborhood U_x of x must be a basis element. Distinct points have distinct U_x, so the space is countable. Each U_x is quasicompact because a member of any cover containing x contains all of U_x. Every finite T0 space is sober: an irreducible closed set cannot be a finite union of proper point closures. T0 gives uniqueness of its generic point.

The limitation is exact. If a discrete-domain surjection preserves arbitrary open-lattice infima, surjectivity forces every intersection of target opens to equal its interior. Conversely that Alexandrov condition is enough. The convergent-sequence example correctly distinguishes ordinary intersection from lattice infimum. Its shrinking open tails have intersection {0}, with empty interior, although the corresponding intersection is open in the discrete domain. This is a failed proposed presentation of an already realizable space, not nonrealizability of the space.

## 4. Turn 3 and the doubled-limit AF example

The topology on N together with a and b is correctly specified. Cofinite tails with one chosen endpoint give a countable neighborhood base and quasicompact neighborhoods inside arbitrary open neighborhoods. The space is T1. Its sobriety argument is valid: an irreducible closed set meeting N can be split by the clopen singleton of an isolated point unless it is a singleton; a closed set contained in {a,b} is a finite T1 set and is irreducible only when a singleton.

The two open compact sets K_a=N union {a} and K_b=N union {b} are also G_delta sets by repeating the same open set. Their intersection N is discrete and noncompact. Thus the stated coherence condition fails.

The matrix-sequence algebra is closed in the supremum norm: a uniform limit of sequences with diagonal limits again has a diagonal limit, as the diagonal-limit map is contractive. The finite-stage description M_2(C)^m direct-sum C direct-sum C, diagonal insertion maps, and density of the union are correct. The maps retaining the first m entries and then using the limiting diagonal are contractive *-homomorphisms and retract onto these finite stages. Their errors tend to zero in norm for every element, giving the stated finite-dimensional completely positive contractive factorizations and nuclearity. A countable union of separable finite stages has separable closure.

The classification of primitive ideals is complete. The c_0 matrix ideal has quotient C direct-sum C. If an irreducible representation does not kill that ideal, one central coordinate projection has nonzero image; otherwise it kills a dense union of finite-support elements. A nonzero central projection acts as identity in an irreducible nonzero representation. The representation therefore factors through exactly that coordinate M_2(C). The other two possibilities factor through the quotient characters. Distinct coordinate and endpoint kernels are distinguished by the displayed elements.

The open supports have the asserted topology. A nonzero diagonal limit forces nonzero entries eventually. Conversely an arbitrary subset of N is realized by a decaying scalar sequence on precisely that subset, and a cofinite set with specified endpoints is realized by the matching diagonal limit with the finitely omitted entries set to zero. These supports form the standard hull-kernel open basis, proving the homeomorphism rather than merely a bijection.

For f=1_{K_a} and g=1_{K_b}, lower semicontinuity follows from openness. The finite intersection property in each compact K proves the Dini identity for decreasing closed sets, without requiring those K to be closed in X. The sets F_m={a,b} union {n:n>=m} are closed and decrease to {a,b}. Their h=fg=min(f,g)=1_N suprema stay at 1 but become 0 at the intersection; the f+g suprema similarly drop from 2 to 1. These are valid failures of product, minimum and addition closure. Both the 2013 contribution and Kirchberg's 2006 paper already give the underlying algebra; the packet credits this correctly.

## 5. Turn 4 and the missing binary join

The map from the four-element Boolean open lattice to subsets of {u,v,w}, with singleton images {u} and {v}, has four distinct values, preserves top and bottom, and preserves every meet, including the empty-family meet. Every nonempty directed family in a finite partially ordered set has a largest member when it is closed under finding upper bounds within the family. Consequently the map preserves all nonempty directed suprema. Nonetheless its binary join omits w. Its range enlarged by that missing union has five elements, so this closure operation cannot retain an isomorphic four-element open lattice. No function to the two-point target can induce these preimages because w would have to choose one of the two target values.

The upgrade lemma is also valid. A union of open subsets of a second-countable space has a countable subfamily with the same union. Binary-join preservation implies monotonicity, and successive finite unions of that subfamily form an increasing sequence. Preservation of those increasing unions gives the whole union. If the union is empty, a nonempty family consists only of empty opens and the identity is automatic; preservation of the empty family requires the stated bottom condition. Thus binary joins are sufficient in addition to the existing increasing-union property. This is a conditional upgrade, not construction of the missing property for every Dini space.

The source's directed-union condition is at least as strong as the increasing-sequence condition used here. The finite countermodel satisfies even the full directed-family condition, so it legitimately refutes automatic binary-join preservation from the weaker list. The finite space in that countermodel remains realizable by a commutative algebra.

## 6. Turn 5 and open-cover permanence

The open-cover construction is correct. Each local realization supplies a locally compact Polish witness and a complete-lattice embedding by the credited criterion. A countable topological disjoint union of those witnesses is locally compact and Polish: truncate each complete component metric at 1 and put distance 2 between distinct components. A Cauchy sequence eventually lies in one component; countable dense sets unite to a countable dense set. Empty components cause no exception.

Restriction V -> V intersect U_n preserves top, bottom and unions. The cover and local injectivity give global injectivity. For an arbitrary subset S of X and an open U, the equality

U intersect int_X(S) = int_U(U intersect S)

holds because a relatively open subset of an open U is open in X. Apply it to S=intersection_i V_i, then use each local embedding and the componentwise interior operation on the disjoint union. This proves preservation of arbitrary lattice infima, including empty-family infima, and completes the application of the criterion.

Openness is essential, not cosmetic. Let X=R, U={0}, and V_n=(-1/n,1/n). Then U is closed, intersection_n V_n={0}, and the left side is empty while the right side is {0}. This is an analytical countercontrol against replacing open charts by arbitrary closed charts. The rational prefix tests only check the concrete formulas; they do not prove the infinite intersection identity.

The converse correctly uses the ideal/open-subspace correspondence and nuclearity and separability of ideals. Second countability gives a countable subcover of any open cover. An open Hausdorff subspace of a Dini space inherits the local quasicompact neighborhoods inside each of its opens, and these are compact in its Hausdorff topology. It is therefore second-countable locally compact Hausdorff, with a separable nuclear C_0 realization. The locally Hausdorff subclass follows. Nothing in this argument establishes the needed local witnesses for arbitrary Dini spaces.

## 7. Definitions and source verification

The required complete-lattice operation is inf_i U_i=int(intersection_i U_i). This is explicit in HK Definition 1.1 and in the full 2013 contribution. The manuscript consistently uses this operation in the discrete-cover failure and the gluing proof; finite intersections or finite-poset checks cannot replace that infinite condition.

K06 Definition 1.1 explicitly states the sufficiency of decreasing sequences in a second-countable space. There is also a direct verification. For a nonempty downward-directed family G of closed sets, use second countability to choose a countable subfamily with the same intersection, by applying the countable-subcover property to the union of the open complements. Recursively choose H_n in G with H_n contained in H_{n-1} and the n-th selected member. Then H_n decreases and its intersection equals intersection G. The sequence identity gives sup f(intersection G)=inf_n sup f(H_n). This is at least inf_{F in G} sup f(F), while inclusion in every F gives the reverse inequality. The directed identity follows. No implicit countability of the point set is needed.

Source inspection:

- [OWR](https://ems.press/journals/owr/articles/12591): the complete contribution at printed page 2456 was inspected as extracted text and a rendered page. The publisher gives publication on 2014-06-01 for the 2013 report. Its abbreviated definition is reconciled with the rigorous sober definition.
- [HK](https://arxiv.org/abs/2401.05917v1): the title page is dated 2005-07-10; arXiv gives upload on 2024-01-11. Definitions 1.1 and 1.3, Theorem 1.4, Corollary 1.5, the directed-join warning on page 6, Section 6 and Proposition A.11 were checked. The complete 67-page operator-algebraic construction remains an external dependency.
- [K06](https://jot.theta.ro/jot/archive/2006-055-002/2006-055-002-002.pdf): definitions and context on printed pages 239-242 and the relevant characterization discussion on pages 249-250 were checked. These substantiate sobriety, local quasicompactness, the sequence convention and the prior matrix-sequence example.
- [STW](https://arxiv.org/abs/2506.10902v2): all of Section 20 on printed pages 64-65 was inspected, with rendered page 64 and current HTML cross-checks. Problem LXXI(1) still poses the universal nuclear question. The PDF prints 2026-05-11 and arXiv records revision 2026-05-08; the experimental HTML instead displays 2026-08-24. This mismatch is disclosed, not harmonized or treated as an additional version.

All four local PDF hashes, byte counts and page counts match the author metadata. This audit reused the existing PDF bytes; it does not claim fresh PDF downloads. Current primary web pages were read. Targeted searches supplied no new useful solution source; absence from those searches does not prove exhaustive absence of a later solution. SOURCE_AUDIT.json records the exact inspection boundaries and public metadata without redistributing source documents or extracted source text.

## 8. Computational checks and falsification

The author checker was read and replayed: PASS, 1,029,251 elementary assertions. Its manifest verifier also passes all 13 files. That verifier alone checks listed members, so the independent validator adds an externally fixed manifest digest and exact inventory equality.

The recovered independent checker was inspected and rerun: PASS, 2,315,828 checks. It enumerates labeled partial orders on zero through five points, with counts 1, 1, 3, 19, 219 and 4,231. Its three-state-per-unordered-pair enumerator is independently compared with the naive directed-edge enumerator through four points. It checks finite sobriety using intersecting opens, minimum neighborhoods, lattice operations, open-chart interior identities for every subset, and two-chart injectivity.

It also inspects 10,862 finite set maps, of which 4,842 are continuous, for the pseudo-map/lattice correspondence and finite pseudo-epimorphic surjectivity. It includes a pseudo-open surjection onto a non-T1 finite space that is not a quotient, guarding against conflating the pseudo condition with ordinary open or quotient behavior. The weak-map search confirms the smallest tested discrete codomain size admitting the binary-join failure is three.

The independent AF checks use small Gaussian integers, represented exactly at these magnitudes, to test multiplication, addition, adjoints, injectivity via a left inverse, and retraction after later stages. Deliberately replacing the diagonal insertion by a nondiagonal insertion is rejected by multiplication and adjoint controls. Snapshot controls reject altered proof bytes, missing members, unlisted members and a changed manifest, then reread the untouched original packet.

The added scope checker passes 412 checks, including actual unified-patch application to temporary copies, byte comparison with the corrected packet, unchanged-file checks, complete-proof/turn consistency, singleton pseudo-open conditions and exact rational regressions for the two analytical countercontrols. The written proofs establish infinite compactness, sobriety, completeness, the complete primitive-ideal list and infinite intersections. The checker counts do not establish those claims or the external realization theorem.

The independent audit verifier checks recursive inventory, path safety, byte lengths, SHA-256 values and an optional externally supplied manifest digest. Its self-tests deliberately corrupt synthetic snapshots and require rejection. Final verification was run with the actual frozen audit-manifest digest supplied separately.

## 9. Disposition and deliverables

ACCEPTED AFTER CORRECTION: Alexandrov realization; the Baire auxiliary-cover obstruction; the doubled-limit AF realization and Dini-function failures; the binary-join countermodel and upgrade lemma; and open-cover permanence with the locally Hausdorff subclass.

UNRESOLVED: the universal Dini realization question. A general Dini space still needs a suitable complete-lattice embedding into the opens of some locally compact Polish space, or an explicit obstruction ruling out every such embedding. None of the five approaches supplies either universal conclusion.

Deliverables are CORRECTION.patch, the corrected author packet, the present report, public source-verification metadata, independently reviewed checker programs and replay receipts, and the audit manifest. No primary PDF, copied primary-source text, dataset contents, private source, or private coordination file is included. No remote publication, commit or push was performed by this audit.

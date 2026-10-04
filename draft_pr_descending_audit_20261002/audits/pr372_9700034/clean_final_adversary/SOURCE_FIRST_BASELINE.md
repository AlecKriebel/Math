# Independent source-first baseline

This file was written before opening the candidate TURN proofs, programs, generated results, receipts, earlier review, root analyses, or sibling analyses. Only the candidate SOURCE_MANIFEST locators were used to locate sources; its alleged hashes were treated as data and freshly recomputed. Independence does not mean independence from the standard mathematical literature.

## Exact question and boundaries

Aldous's long 2012 paper, Open Problem 34, physical PDF page 50, asks which extra assumptions, if any, imply finite expectation of the supremum of Euclidean route lengths from 0 to infinitely many independent uniform destinations in the closed unit disc. The published 2014 paper repeats the same question as Open Problem 8, physical PDF page 38. Destinations must be independent of the SIRSN realization. The target concerns a single common random network; it is not independent resampling of the network for each destination. Closed versus open disc and the singleton origin do not affect uniform sampling. A theorem about an uncountable pointwise supremum would require additional version/regularity hypotheses.

The published definition, physical PDF pages 6--8, requires rectifiable non-self-intersecting routes, reversal symmetry, pairwise compatibility, consistent measurable finite-dimensional network laws, invariance under Euclidean similarities, finite fixed-distance mean route length, and finite trimmed-network edge intensity p(1). The source does not require a pre-existing minimum-cost metric. Finite intensity bounds expected union length in a deterministic bounded region. It alone does not bound lengths of routes which leave that region or the collection of endpoint pieces over all densely sampled destinations.

## Independently derived universal measure baseline

Let D be the unit disc with normalized area measure nu. For a jointly measurable route-length field L(omega,y), let q_t(omega)=nu{y:L(omega,y)>t} and M(omega)=esssup_nu L(omega,y). Condition on omega. Independence of destinations gives

P(max_{1<=i<=n} L(omega,U_i)<=t | omega)=(1-q_t(omega))^n.

Taking n to infinity shows P(sup_i L(omega,U_i)>t | omega)=1_{q_t(omega)>0}. Use rational t and Fubini/conditional product law to obtain sup_i L(omega,U_i)=M(omega) almost surely, including M=infinity. Consequently

E sup_i L(omega,U_i)=integral_0^infinity P(q_t>0) dt.

This is an exact equivalence, not a solution: replacing the target by this integral is blocked unless the axioms or genuinely weaker checkable conditions control its integrand. The averaged marginal tail is E q_t=P(L(omega,U)>t); its integral equals E L(omega,U), a different quantity. Similarity invariance gives E L(omega,U)=(2/3) E D_1. Thus the defining first moment proves a one-destination baseline but leaves the maximum question open.

For any deterministic positive h(t), the property q_t=0 or q_t>=h(t), almost surely for almost every t, yields P(q_t>0)<=E q_t/h(t). Integrability of the right hand side is sufficient. One must prove h from geometric/regularity structure; simply postulating the integrability is an equivalent reformulation, not independent progress.

## Independent falsification controls

Choose pairwise disjoint deterministic measurable cells A_k within D, each with positive measure a_k, sum a_k<=1, and assign L=k on A_k and 0 elsewhere. With a_k proportional to 2^{-k}, E L(U)<infinity, and every finite moment of L(U) is finite, yet M=infinity deterministically. Every cell is eventually sampled almost surely. This is a measurable-field negative control, not a SIRSN, and cannot refute the axioms. Random rotation of a tiny hot cell preserves rotational symmetry while retaining the same defect; neither rotational invariance nor one-point marginal moments settles the target.

A positive control is L(omega,y)<=B(omega) for nu-almost every y with E B<infinity. Another is an explicit spatial regularity mechanism which bounds local hot-cell size from its height together with an integrable averaged tail. An a.s. finite B with infinite mean is insufficient. Altering lengths on an area-zero set changes pointwise supremum but not the iid target.

A geometric approach needs two logically separate estimates: control of the length accumulated inside a common deterministic or random bounded region, and control of escaping/endpoint pieces. A finite-intensity union estimate only resolves the first after containment is established. A random containment radius needs a joint bound; a product of dependent quantities cannot be factored without evidence.

## Independent Poisson-line model control

Kahn v3 (fresh arXiv primary), physical PDF page 10, Theorem 3.1 supplies a common travel-time diameter with stretched-exponential upper tail for bounded sets. Physical pages 25--27 use speed maxima at dyadic radii and independent newly intersecting line sets to control a single geodesic's Euclidean length. The common-diameter estimate suggests a simultaneous extension: on {common time<=T_n}, any route of length>r_m must trigger the same speed events at every smaller radius, regardless of destination. A union bound on those speed events can then be performed once, without unioning over destinations. If the line process parameter is gamma>d>=2, moments below gamma-1 can plausibly control the maximal length; this mechanism is model-specific and does not prove the abstract SIRSN question.

A technical hazard in the primary is its displayed conditional bound: probability of a speed event after conditioning on the time event is not automatically bounded by its unconditional probability. Use the unconditional intersection P(length>r_m, common time<=T_n) and add P(common time>T_n). No independence between the time and speed events is required then. The independent increments used for dyadic speed records concern disjoint line sets, not iid speed maxima themselves. Kahn's formula (2) also visually contains a time/length conversion typo; dimensions require time contribution L/v, not v L. No candidate proof should rely on that typo.

## Evidence and scope

All four primary bytes were fetched afresh with UTC receipts. All match locator hashes. Text extraction succeeded. Critical statement, definition, and Kahn dyadic argument pages were independently rendered and visually inspected. This baseline does not certify novelty, the entire literature, or the original universal question. The strongest baseline is the exact conditional essential-supremum identity and the explicit distinction between averaged tails and positive-volume-event tails.

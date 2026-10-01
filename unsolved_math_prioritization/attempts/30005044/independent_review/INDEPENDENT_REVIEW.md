# Independent full review: contact-process explosion, 30005044

## Binding verdict

**PASS_COMPLETE_EXISTENTIAL_SOURCE_TARGET. No mandatory correction.**

The unchanged candidate gives an admissible almost-surely finite offspring law with infinite mean and proves infinitely many **simultaneous** infections at a deterministic finite time with positive probability. It answers the source's existential explosion question, with the stronger stated quenched possibility result. It does not classify all infinite-mean offspring laws.

Binding author hashes:

- `PROOF.md`: `8f2010e4aa303e260546faf72c507d53c30b43025be7ad2e99019631eac7b2bd`
- `FROZEN_MANIFEST.json`: `55130936f058befa5657d05adb4677764fc26f174d8cf2dfce104187186c0b29`, covering ten author files

All ten author files and all three pinned primary PDFs hash-match. The 17,228-assertion author receipt replays byte-for-byte. The reviewer did not contribute to this candidate or its ray/recovery construction; the shared OWR source location was supplied as source-only assistance. This is independent adversarial AI review, not human peer review or novelty certification.

## 1. Original source and later-literature scope

I read the complete OWR contribution, printedpp618–620, and visually inspected the exact question onp619. The general model has iid finite fitnesses in [1,infinity), infection rate lambda times the two endpoint fitnesses, recovery rate1, and initially only the root infected. Constant fitness1 is an admissible degenerate iid choice. The unbounded-support condition appearing earlier onp619 belongs to a different survival theorem and is not a general model restriction. The neighboring moment-gap and bounded-offspring questions are correctly kept separate. [Official OWR report](https://ems.press/content/serial-article-files/46949).

The latest full author manuscript, [Cardona–Tobón–Ortgiese, arXiv2110.14537v4](https://arxiv.org/abs/2110.14537), was checked for Definition2.1, the graphical setup and Theorem3.2, with the latter page visually inspected. It allows a broader positive-fitness model, but its nonexplosion theorem expressly assumes finite offspring mean. The present example therefore does not contradict that theorem. The full inspected mathematical version is the41-page July2026 author manuscript; the publisher's37-page typesetting is not silently identified byte-for-byte with it.

The full publisher PDF of [Bartha–Komjáthy–Valesin, Degree-penalized contact processes](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0C2D174326F5BB7EFDC7DADE9E768D56/S2050509425101448a.pdf/degreepenalized_contact_processes.pdf), *Forum of Mathematics, Sigma*14(2026),e6, was checked. Definition3.1 and equation(19), p17, use finite infection paths and explicitly allow finite-time explosion. Definition6.1 and Proposition6.2, pp46–48, use downward growing-degree infection rays for global survival. The author correctly credits that mechanism without citing the proposition as an already stated simultaneous-infection explosion theorem. No exhaustive priority claim is made.

## 2. Offspring law and graphical construction

The tail m^(-1/4) decreases from1 to0. Its successive differences are a positive normalized mass function on finite positive integers. The tail limit rules out an infinite offspring value; its divergent sum gives infinite mean. Every finite generation and ball are finite almost surely, by induction. Because every vertex has at least one child, the tree is infinite almost surely.

On this countable locally finite tree, independent directed edge-arrow processes and independent recovery processes can be assigned on a countable Ulam indexing before revealing the tree. Each edge rate is finite. The event that a fixed vertex is infected at a fixed time is determined by the existence of a **finite** infection path. This agrees with the increasing union of finite-ball contact processes: every finite path is contained in some finite ball, and adding graph edges preserves such paths.

The candidate therefore does not rely on a process started at infinity, on an infinite-jump continuation, or on a finite-total-rate pure-jump chain after explosion. It works in the explicit minimal graphical interpretation used by the source literature. Suppressing upward arrows only restricts infection paths.

## 3. Adaptive exploration and the quantitative ray event

The stage thresholds and deterministic time lengths are

`D_n=2^(4n+8)`, `ell_n=2^(-n-2)/lambda`, `s_n=(1-2^(-n))/(2lambda)`.

The root-threshold probability is exactly1/4. At stage n, the selected vertex's own degree is already exposed and biased; the proof never treats that degree as a fresh unconditioned sample. Its first D_n children exist, and their own offspring counts and the outgoing directed arrow processes have not been inspected before. Selection at the preceding stage used only this vertex's own degree and an incoming arrow. Distinct Ulam offspring coordinates and distinct directed edge processes remain independent with their original laws conditional on that exploration history.

Consequently each child qualifies with the displayed probability

`p_n=2^(-n-3)(1-exp(-2^(-n-2)))`.

The bound `1-exp(-x)≥x/2` for0≤x≤1 gives `D_n p_n≥4^(n+1)`. The probability of no eligible child is at most `exp(-4^(n+1))≤16^(-(n+1))`. I checked both exponent inequalities and their endpoint cases. Summing the probabilities of the disjoint first-failure events requires only these conditional bounds, not independence of stage successes. The total failure majorant is1/15, yielding ray probability at least7/30 after the root event.

The exploration is measurable and uses only the tree and arrows. In particular it does not inspect any recovery mark. This is crucial for the next step.

## 4. Recovery windows and simultaneous infections

Condition on the entire tree and arrow field. On the infinite-ray event the selected vertices become a fixed sequence of distinct labels, and their recovery processes are still independent rate-one Poisson processes. The forbidden recovery intervals are [0,tau] at the root and [s_(n-1),tau] at vertex n≥1, where tau=1/(2lambda).

Their total length is

`tau + sum_(n>=1)(tau-s_(n-1)) = 3tau`.

Thus the conditional probability of avoiding every recovery window is exactly exp(-3tau), by continuity from above of the finite collections. The overlap of these time intervals does not create dependence: they refer to different vertices. The root and first child each incur a full interval of length tau; the remaining lengths form the geometric tail. This explains the factor3 rather than2. Poisson endpoint coincidences do not change the probability or the argument.

The induction is valid with the precise stage alignment. Vertex n is infected by s_n. The selected arrow during [s_n,s_(n+1)) reaches vertex n+1 after its no-recovery window has begun and before s_(n+1). Each reached vertex remains infected until the common time tau. For every fixed n the path to vertex n uses finitely many arrows and is contained in the radius-n ball. Therefore the minimal graphical configuration at tau contains all distinct ray vertices.

Combining the two independent-field arguments proves exactly

`P(|X_(1/(2lambda))|=infinity) >= (7/30) exp(-3/(2lambda)) > 0`.

This is an annealed bound. The argument is stronger than an arbitrarily deep infection reached before tau, a finite-total-time first-passage ray, or ordinary survival. A fast ray without the recovery windows would not suffice; the separate negative control illustrates that distinction.

## 5. Quenched enhancement

For a fixed rate, goodness is defined through the countable deterministic times tau+m. It is measurable in the rooted tree, because fixed-time infection events are generated by countably many finite paths. The positive annealed bound implies that good trees have positive probability.

If a child subtree is good, it can be reached and kept infected until time1 by a finite positive-probability event: no recoveries at the two endpoints during[0,1] and an arrow during[0,1/2]. The stated lower bound `(1-exp(-lambda/2)) exp(-2)` is correct. Future Poisson marks after time1 are independent, and concatenating finite paths with the child's future paths gives the original infection at a time in the same countable family shifted by one. If the child has positive probability for the countable union, one particular time has positive probability.

Thus a bad tree must have only bad child subtrees. Independence of the Galton–Watson subtrees gives `1-q≤E[(1-q)^xi]`. For0<q<1, positivity of xi and positive mass above1 make the right side strictly smaller than1-q. Hence q=1. No finite offspring moment is used in this bounded generating-function expectation.

Intersecting over positive rational rates and then using monotonicity proves: for almost every tree, every positive real rate has positive conditional probability of explosion at some finite time. The statement appropriately does not claim a common quenched lower bound, a tree-independent time, or probability-one explosion for the dynamics.

## 6. Fitness extension

For a fixed finite fitness environment bounded below by1, superpose independent extra arrows of rate `lambda(F_u F_v-1)` on each directed edge. The constant-fitness infection paths remain present and recoveries are unchanged. All per-edge rates remain finite. This proves both the annealed lower bound and the stated quenched possibility for the original iid fitness model, including finite unbounded-support laws if desired. No extension to fitness values approaching zero is certified.

## 7. Independent controls and disposition

The author checker was inspected before execution; its output is reproduced exactly. Fresh `independent_checks.py` passes **7,136 exact assertions**, including:

- threshold/tail identities and divergent truncated-mean lower bounds
- geometric failure sums with exact infinite remainders
-69,904 finite exploration cylinders, grouped by all the data used to select the first eligible child, checking fresh outgoing/recovery marks despite the selected-degree bias
- exact common-horizon guard coverage and finite-path ordering at several rates
- a deterministic fast-ray negative control whose vertices recover before the limiting horizon
- the strict bad-probability inequality for the hereditary quenched argument

These are finite controls, not simulations and not computational substitutes for the infinite-event probability reasoning. The written proof supplies the countable conditioning, limiting and graphical-measurability steps.

The exact existential source target is fully proved after one substantive author turn. No correction is required. The packet is suitable for a reviewed draft result, retaining classical-method credit, the annealed/quenched distinction, the simultaneous-infection meaning of explosion and the explicit absence of a universal infinite-mean criterion. Publication remains subject to the parent campaign's authorization gate.

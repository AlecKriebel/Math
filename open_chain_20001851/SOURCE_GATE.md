# Source and prior-attempt gate

Checked 3 October 2026. Problem 20001851, AIM-GEOMETRY-0189, rank 459.

## Actual problem and conventions

The AIM workshop list, Item 2 attributed to Ileana Streinu, asks whether the
non-self-intersecting configuration space of an open equilateral polygonal arm
in three dimensions is connected. The original notation is
`ell_1 = ... = ell_n`; the catalogue's backticks are extraction damage.
The accompanying workshop report, page 3, Working Group 2, explicitly identifies
the question with straightening every unit-bar open chain by noncrossing motion.

We use positive unit lengths, labelled vertices `p_0,...,p_n`, freely moving
endpoints, universal joints, zero-thickness rigid segments, and continuous
length-preserving motions. The polygonal map is injective: nonadjacent closed
segments are disjoint, and adjacent ones meet only at their common endpoint.
Collinear straight joints are allowed; backtracking overlap is not. Fixed bond
angles, positive thickness, and permission for self-contact define different
problems. The terse AIM source does not separately specify contact conventions;
the strict embedding model here agrees with the cited straightening literature.
No endpoint is pinned except when a harmless translation fixes a frame.

The imported title, "A one-coordinate unlockability certificate for open chains
in three-space," describes a previous machine-generated sufficient condition.
It is not the original research question. Failure of that sufficient condition
does not establish locking.

## Sources and current-literature check

- Exact catalogue URL: <https://www.unsolvedmath.com/problems/20001851>.
  Web retrieval failed and a direct cloud-browser inspection displayed HTTP
  403, "This request was blocked." No successful live rendering is claimed.
- Original [AIM problem list](https://aimath.org/pastworkshops/linkagesproblems.pdf),
  page 1, Item 2; [workshop report](https://aimath.org/pastworkshops/linkagesrep.pdf),
  page 3, Working Group 2. Both original documents were read.
- Biedl et al., *Locked and Unlocked Polygonal Chains in Three Dimensions*,
  Discrete & Computational Geometry 26 (2001), 269–281,
  <https://doi.org/10.1007/s00454-001-0038-7>;
  [author preprint](https://arxiv.org/abs/cs/9910009).
  Theorem 2.1 proves straightening when a simple orthogonal projection exists.
  Section 6, Question 5, states the equilateral question and credits
  Cantarella–Johnston with the affirmative result for at most five bars.
  Its five-bar locked construction has deliberately unequal lengths.
- Cantarella–Johnston, *Nontrivial embeddings of polygonal intervals and
  unknots in 3-space*, J. Knot Theory Ramifications 7 (1998), 1027–1039,
  <https://doi.org/10.1142/S0218216598000553>. Its five-segment classification
  is used only through the explicit bound reported in Biedl et al.; no new
  proof of that classification is claimed here.
- Demaine, Demaine, Langerman and Vervier, *Locked Thick Chains*, EuroCG 2009,
  [author page](https://erikdemaine.org/papers/ThickChain_EuroCG2009/).
  Thick-chain results must not be substituted for the zero-thickness question.
- Connelly–Demaine, *Geometry and topology of polygonal linkages*, 2017
  [author handbook chapter](https://www.csun.edu/~ctoth/Handbook/chap9.pdf),
  Problem 9.7.1, also lists the equilateral-arc question.
- Lummerzheim, *On 3D fixed-angle chains that are locked, equilateral,
  equiangular, and obtuse* (2022), <https://doi.org/10.57683/EPUB-1952>.
  This is about fixed-angle chains, not the present universal-joint model.

Targeted searches through the check date for equilateral/unit-length locking,
universal joints, and recent Carpenter's Rule developments located no primary
resolution of the arbitrary-bar-count question. This bounded search supports
retaining open status; it is not a completeness or novelty certificate.

## Genuine prior-attempt gate

The live default-branch queue row is `queued`, `0/5`. Exact-ID/code PR searches,
an exact-ID issue search, an exact-ID commit search, and relevant branch-name
searches found no prior campaign attempt. A broader PR search for "equilateral"
returned an unrelated polygon-space syzygy problem, not this linkage question.

The hash-verified supplied catalogue contains one explicitly partial AI attempt:
strictly disjoint scalar projection intervals for nonadjacent bars imply a
simple planar projection, hence unlockability by Biedl et al. That report
expressly leaves arbitrary equilateral chains open and labels novelty confidence
low. It is useful background, not a prior campaign resolution or peer-reviewed
literature. Five fresh substantive proof attempts are available. Source retrieval,
review and packaging do not consume a proof-attempt turn.

No solved-status or priority claim is authorized by this gate.

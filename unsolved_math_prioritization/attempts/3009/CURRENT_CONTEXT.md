# PR37: credited low-dimensional consequence; complete KP-5.2 unsolved

The complete flat source asks about one common full-orbit diameter bound and
compact-open recurrence on R^n, plus the boundary-fixed closed-ball question.
It also discusses informal local/manifold variants and stronger smooth
recurrence. The original proof verifies the line and plane homeomorphism
cases and boundary-fixed interval/disk cases. Diffeomorphisms in dimensions
one and two follow after forgetting smoothness. Dimensions at least three,
general local/manifold claims and stronger smooth recurrence there remain
unresolved. No full resolution, counterexample or novelty is claimed.

The disk corollary was directly read in the accessible arXiv v3, revised 2 March 2009, of the paper first published in 1998. The printed 1998 disk passage remains unverified. Brown1977 remains inaccessible and is not claimed as read.
Hamilton1954's complete proof, printed pp522–524, was directly read by root;
the closed planar family preserves its primary proof ledger. Cartwright–
Littlewood and Kolev–Pérouème are established theorem imports. Finite controls
do not certify their global topological content or the cited proof texts.

Original substantive budget1/5; new substantive attempts0; audit attempts0.
Three closed first-party families and finalized actual root reproduction are
bound. Original complete31/8462 generated receipts were BYTE/fullJSON equal;
the independent program's stdout is metadata only and was checked against its
specified metadata serialization. Current model/reasoning are not independently
exposed; no current deadline is inferred. Original dated metadata is archival.
A NEW whole-current-packet source-first adversarial gate is PENDING; no old
verdict transfers. No paper, new DOI, tracker, release, or external human review
is claimed. No outside individual was contacted.

The exact complete statement follows without editing:

(Doubly-Small Morphisms of Manifolds).

- Suppose that $h: \R^{n} \to \R^{n}$ is a homeomorphism (or diffeomorphism) which satisfies two smallness hypotheses:

- every orbit of $h$ (of any $x\in \R^{n}$, under all powers of $h$) is uniformly bounded in diameter (by 1 say), and

- some subsequence of powers of $h$ converges to $\mathrm{Id}_{\R^{n}}$ in (say) the compact-open topology.

Then must $h$ be the identity map?

- A special case of this question is: let $h$ be a homeomorphism of $B^{n}$ that is the identity on $\partial B^{n}$. If there is a subsequence of powers of $h$ which converge to the identity, must $h$ itself be the identity?

The exact complete background and dated literature triage follow without editing:

Source: Kirby's Problems in Low-Dimensional Topology notes. Original problem number: KP-5.2.

Literature notes:
- The case $n=1$ is trivial, $n=2$ seems likely to be true, as a consequence of results of Brouwer and Cartwright-Littlewood (nicely and succinctly reproved in [Bro84] and [Bro77]), and $n\geq 3$ is open.

- The question is meant to be local in nature, i.e. the question can be adapted to any open subset of $\R^{n}$. It also applies to any manifold, where in Condition (i) one would assume that every orbit of $h$ has diameter less than some $\epsilon$ in the compact-open topology.

- The answer is `yes' if $h$ is periodic. This is Newman's Theorem, with an excellent exposition in [Dre69].

- For $h$ a diffeomorphism, and using $C^{\infty}$ convergence, the answer seems likely to be yes.

- Since a homeomorphism $h: \R^{n}\to \R^{n}$ generates a homomorphism $\varphi: \Z \to \Homeo(\R^{n})$ (and vice-versa) by $m\mapsto h^{m}$, the Question can be rephrased in terms of such a $\varphi$. Condition (i) becomes: Assume that $\image(\varphi)$ lies in a suitably small neighborhood of $\mathrm{Id}_{\R^{n}}$, and Condition (ii) becomes: Assume that $\varphi$ accumulates at $\mathrm{Id}_{\R^{n}}$. And the Question becomes: Must $\varphi$ be the trivial homomorphism?

- The question is `stronger' than the Hilbert--Smith Conjecture, discussed in Problem 5.3 below. That is, an affirmative answer to it would imply the Hilbert--Smith Conjecture. The Hilbert--Smith Conjecture (in its Question form) is equivalent to the Question above if in addition one assumes that the closure of the union of the powers of $h$ in $\Homeo(\R^{n})$ is compact.

References cited:
- [Bro84] Morton Brown. A new proof of Brouwer’s lemma on translation arcs. Houston J. Math., 10(1):35–41, 1984.
- [Bro77] Morton Brown. A short short proof of the Cartwright-Littlewood theorem. Proc. Amer. Math. Soc., 65(2):372, 1977. doi:10.2307/2041926.
- [Dre69] Andreas Dress. Newman’s theorems on transformation groups. Topology, 8:203–207, 1969. doi:10.1016/0040-9383(69)90010-X.

<!-- LITERATURE-TRIAGE:BEGIN -->
## Literature review (checked 2026-08-17)

**Status:** partially_solved  
**Classification:** PARTIAL-PROGRESS

**Current literature assessment.** The doubly-small question is elementary in dimension 1 and affirmative for periodic transformations under Newman's theorem, but remains open in dimensions at least 3; the planar discussion remains nonterminal.

**Verified partial progress.**

- The dimension-one case is elementary.
- Newman's theorem gives an affirmative answer when h is periodic.
- With compact closure of the cyclic subgroup generated by h, the question becomes the Hilbert--Smith setting; without that compactness it is strictly stronger.

**Full solution or refutation.**

No general proof or counterexample was found for the stated homeomorphism or diffeomorphism conditions in dimensions at least 3.

**What remains.**

Settle the compact-open recurrence plus uniformly small-orbit problem in dimensions at least 3, and make the expected two-dimensional consequence fully explicit if possible.

**Sources checked.**

- Andreas Dress, Newman's theorems on transformation groups, Topology 8 (1969), 203--207. (primary): https://doi.org/10.1016/0040-9383(69)90010-X
  Evidence used: Provides the periodic small-action theorem used for the periodic special case.
- R. I. Baykur, R. C. Kirby, and D. Ruberman (eds.), K3, AMS 295 (2026), Problem 5.2. (authoritative_secondary): https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
  Evidence used: Current dimensional status and precise connection with Hilbert--Smith.

**Review notes.** The background's phrase 'diameter less than epsilon in the compact-open topology' is not literally a well-typed metric assertion and was treated as informal rather than repaired.

This is a dated literature triage; an open classification is not proof that no later or unindexed result exists.
<!-- LITERATURE-TRIAGE:END -->

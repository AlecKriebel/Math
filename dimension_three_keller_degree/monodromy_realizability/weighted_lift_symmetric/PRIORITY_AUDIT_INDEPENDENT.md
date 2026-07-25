# Independent priority audit: weighted-lift symmetric monodromy

**Sweep completed (UTC):** 2026-07-25T19:52:10Z
**No person was contacted.**

This is source-specific evidence, not a guarantee of worldwide priority.
The public record is changing rapidly.

## Claim separated into its components

The candidate statement is:

> For every \(d\ge3\), some dimension-three Keller counterexample of
> generic degree \(d\) has geometric monodromy \(S_d\).

It combines three logically distinct ingredients:

1. Gallagher's all-degree weighted-lift construction;
2. the classical theorem that a polynomial with arbitrary fixed higher
   coefficients and independent linear and constant coefficients has full
   symmetric Galois group; and
3. the observation that Gallagher's inverse pencil has exactly that form:
   \[
   \Phi(T)-PT+cQ
   \]
   with \(P,Q\) algebraically independent and with exact recovery of the
   Keller function field.

No novelty can be claimed for items 1 or 2.

## Decisive classical source: Brink 2004

David Brink,
[*On alternating and symmetric groups as Galois groups*](https://doi.org/10.1007/BF02771527),
Israel J. Math. **142** (2004), 47--60, Theorem 13, proves:
\[
X^d+a_{d-1}X^{d-1}+\cdots+a_2X^2+SX+R
\]
has Galois group \(S_d\) over \(K(S,R)\) whenever
\(\operatorname{char}K\nmid d(d-1)\).

For any fixed Gallagher-admissible seed \(p\) of degree \(d-1\), set
\(\Phi(T)=\int_0^T p(t)\,dt\).  Gallagher's inverse equation is
\[
\Phi(T)-PT+cQ=0.
\]
After division by its nonzero leading coefficient, this is precisely
Brink's polynomial, with independent variables \(S=-P/\operatorname{lc}
(\Phi)\) and \(R=cQ/\operatorname{lc}(\Phi)\).  The Keller condition makes
the target coordinates algebraically independent, and
\((A,B,C)\leftrightarrow(P,Q,C)=(BC,AC^2,C)\) is birational.  The recovery
\(\gamma=(P-p(T))/c\) and
\[
\frac{d}{dT}\bigl(\Phi(T)-PT+cQ\bigr)=p(T)-P=-c\gamma
\]
remove any extraneous generic root.

Thus Brink implies the stronger family-wide statement:

> Every Gallagher-admissible weighted lift of generic degree \(d\) has
> geometric monodromy \(S_d\).

The exact compact family \(T^d-T^2+UT+V\) is only one special case.
Accordingly, the Galois calculation itself is classical prior art, not a
new all-\(d\) theorem.  What may be new in the live 2026 record is noticing
and recording the Brink--Gallagher corollary.

## Material direct predecessor omitted from the first audit

The MathOverflow answer
[Geometric degrees of counterexamples to the Jacobian conjecture in
dimension three](https://mathoverflow.net/questions/513440/geometric-degrees-of-counterexamples-to-the-jacobian-conjecture-in-dimension-thr/513470)
states that Gallagher's canonical seed tower has
\[
\operatorname{Gal}(h_e/\mathbb C(s,r))=S_{e+1}
\quad\text{for }2\le e\le12,
\]
equivalently \(S_n\) for generic degrees \(3\le n\le13\).  It cites three
exact certificates and links the public repository
[dasjoms/jacobian-conjecture-counterexample-exploration](https://github.com/dasjoms/jacobian-conjecture-counterexample-exploration).

The repository's
[Note 19, “The Pin's Transposition”](https://github.com/dasjoms/jacobian-conjecture-counterexample-exploration/blob/main/jacobian_pin_transposition.md)
states and proves this finite-range theorem.  GitHub's public commit record
shows that the note was already present in commit `ad47e9cea792` at
**2026-07-21T19:47:33Z**, four days before the present draft.  The
repository also reports symbolic checks of its three certificates through
seed degree \(30\), while expressly leaving the all-degree transposition
step open.

This is direct prior overlap and must appear prominently in the main
priority audit.  The statement currently in `PRIORITY_AUDIT.md` that no
Gallagher monodromy calculation was found is true only for Gallagher's
own `jacobianfun` record; it is incomplete as a survey of the public
Gallagher-family record.

The predecessor does **not** prove the present theorem:

- it proves only \(3\le n\le13\), not all \(n\);
- it uses Gallagher's canonical all-degree seed, whereas the present
  compact seed agrees only in the cubic row and is otherwise different;
- its note explicitly calls an all-degree proof a remaining “corridor.”

Accordingly, the predecessor narrows the candidate novelty to the uniform
all-degree completion and the particularly simple compact seed.  It does
not erase that candidate novelty.

## Classical Morse theorem

Jean-Pierre Serre, *Topics in Galois Theory*, Theorem 4.4.5, states that
if \(f\) is a Morse polynomial over a characteristic-zero field, then
\(\operatorname{Gal}(f(X)-T)=S_{\deg f}\).  Proposition 4.4.6 supplies
the finite-inertia generation step used in the proof.

This precisely covers the branch-cycle portion of the candidate note once
\(T^d-T^2+UT\) is shown to be Morse.  The main artifact should cite Serre
and should describe the classical theorem as prior art, not as a new
monodromy mechanism.

## Gallagher sources

The following were checked:

- Alexis Gallagher,
  [*An infinite family of counterexamples to the Jacobian Conjecture in
  dimension three: every generic fiber degree \(n\ge3\) occurs*](https://doi.org/10.5281/zenodo.21479195).
  This proves the uniform weighted-lift construction and generic degree,
  but does not compute monodromy groups.
- Gallagher's
  [`RESEARCH.md`](https://github.com/algal/jacobianfun/blob/main/RESEARCH.md).
  Exact searches of the current full text found no occurrence of
  “monodromy” or “Galois.”
- Gallagher's
  [public explainer](https://jacobianfun.org/jacobian-explained) and
  [counterexample atlas](https://jacobianfun.org/counterexamples).
  They state generic degrees and exact fibres, but not the monodromy
  groups of the all-degree tower.

Gallagher therefore has priority for the maps, seed framework, recovery
mechanism, and all-degree generic-fibre theorem.

## Current Jacobian-counterexample discussions

The following live sources were checked:

- The MathOverflow question
  [Galois structure of the new counterexample](https://mathoverflow.net/questions/513387/galois-structure-of-the-new-counterexample-to-the-jacobian-conjecture-an-explic)
  computes \(S_3\) for the announced cubic map only.
- Terence Tao's
  [digestion post and comments](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/)
  include a different odd-degree family whose monodromy is
  \(S_{2m-1}\) for even \(m\) and \(A_{2m-1}\) for odd \(m\).  This is not
  an all-degree symmetric realization.
- The
  [Secret Blogging Seminar thread](https://sbseminar.wordpress.com/2026/07/20/the-new-counterexample-to-the-jacobian-conjecture/)
  discusses Gallagher's tangent-sweep construction and links the
  finite-range exploration repository.  It does not supply an all-degree
  symmetric-monodromy proof.
- arXiv:2607.20210,
  [*Graded Keller maps and the Jacobian Conjecture*](https://arxiv.org/abs/2607.20210),
  records \(S_3\) for the announced example, not the present theorem.
- arXiv:2607.21572,
  [*Generic degrees of real polynomial Keller maps with non-dense
  image*](https://arxiv.org/abs/2607.21572),
  concerns real generic degrees and does not state this monodromy result.

## Exact and broad searches

At the timestamp above, searches were run for:

- `"T^d-T^2+UT+V"` with `Galois`, `monodromy`, and `symmetric`;
- `"w^d-w^2"` and `"w^n-w^2"` with `Galois` and `monodromy`;
- `weighted lift`, `Gallagher`, `Keller counterexample`, `S_d`, and
  `symmetric monodromy`;
- July 2026 arXiv combinations of `Jacobian`, `Keller`, `generic degree`,
  `monodromy`, `Galois`, and `symmetric group`;
- MathOverflow, Tao's blog, Secret Blogging Seminar, and publicly indexed
  X/Twitter pages.

The exact compact polynomial did not return a prior monodromy computation.
The only direct Gallagher-tower hit was the finite-range MathOverflow and
GitHub result described above.  X/Twitter indexing returned no relevant
matching claim; this is weak negative evidence because X indexing is
incomplete.

General searches also returned the classical Morse-polynomial theorem and
Brink's two-free-coefficient theorem.  Brink does not mention Keller maps
or Gallagher, but his Theorem 13 applies verbatim to Gallagher's inverse
pencil.

## Independent priority verdict

The original broad wording “the addition here is the monodromy
calculation” is not priority-safe.  The group computation is an immediate
instance of Brink's 2004 theorem, and a finite range of the Gallagher tower
was already computed publicly in July 2026.  A safe formulation is:

> Gallagher constructed the all-degree weighted-lift family.  Full
> symmetric monodromy was already proved publicly for generic degrees
> \(3\) through \(13\) in Gallagher's canonical tower.  Brink's classical
> two-free-coefficient theorem implies uniformly that every
> Gallagher-admissible weighted lift of generic degree \(d\) has geometric
> monodromy \(S_d\).  The compact seed gives a self-contained instance.

I found no pre-audit public source that explicitly states the
family-wide Brink--Gallagher corollary.  That application may be a new
observation in the current event record, but it is not a new Galois
theorem and should be published as an attributed classical corollary.
Absence of a search hit is not proof of novelty or worldwide priority.

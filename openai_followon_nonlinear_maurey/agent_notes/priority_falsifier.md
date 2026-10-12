# Independent priority falsification of the original nonlinear Maurey target

Audit completed 2026-10-06 at approximately 22:17 America/Los_Angeles
(2026-10-07 approximately 05:17 UTC). Investigator: an independent AI
subagent assigned the original request and primary references. No external
individual was contacted. No Git operations were performed.

## Verdict

**No substantive new theorem within the requested scope has been identified.**
The advertised cotype input was publicly announced by Mendel and Naor before
the October OpenAI source. Once that input is accepted, the entire requested
all-Markov-type-two/all-real-L1/all-subset theorem is an elementary consequence
of published Mendel--Naor extension machinery, classical L-embeddedness, and
the finite cut reduction already used in the supplied source. The extra
quantifiers are mathematically necessary to verify, but do not by themselves
constitute a new resolution of an open problem.

This is **not** a claim that I located a complete public proof of the announced
Mendel--Naor 2026 cotype theorem. I did not. Public announcement, available
proof, and immediate consequence must remain separate in the project records.
An honestly attributed, substantively different proof of an announced theorem
could still have research value. The proposed adaptation of the supplied cut
proof does not yet demonstrate such a contribution.

Best-guess completion of this assigned priority audit: 95%. The unresolved 5%
is whether the forthcoming full manuscript is publicly hosted somewhere not
found by the documented searches. Mathematical validation of the supplied
cotype proof and publication-package completion are separate tasks and are
not certified by this note.

## Primary disclosures and their exact status

1. [Naor, De-Höldering factorization, arXiv:2609.07564v1](https://arxiv.org/abs/2609.07564v1)
   was submitted 7 September 2026 at 14:43:48 UTC. Its full public manuscript
   proves extension from Hilbert space to standard real Lebesgue L1. Its
   Corollary 8 proves the bound O(sqrt(q log q)) for standard Lq-to-L1 when
   q is at least 2. This is a complete available proof for those claims.
   Submission metadata gives a verified chronology marker; it does not by
   itself identify the minute at which the manuscript became public.

2. [Version 2](https://arxiv.org/abs/2609.07564v2) was submitted 10 September
   2026 at 15:15:29 UTC. Its
   [Added in proof](https://arxiv.org/html/2609.07564v2#S4)
   announces that forthcoming joint work with Manor Mendel proves metric
   Markov cotype 2 for L1 and the bound e(Lq;L1) = O(sqrt(q)) for q at least 2.
   The reference is Mendel--Naor, *Metric invariants from de-Höldering
   factorization*, 2026, preprint. The announcement contains no cotype proof.
   The paper's first footnote defines Lp as Lebesgue Lp on [0,1], so the
   literally announced L1 target is that standard space.

3. [Mendel--Naor, Spectral calculus and Lipschitz extension for barycentric
   metric spaces](https://web.math.princeton.edu/~naor/homepage%20files/cat0-extension.pdf),
   Theorem 1.11 and pp. 9--10, provide a complete published proof of the
   extension reduction, including the quantitative dependence on the Markov
   type constant and the discussion of extension into a bidual followed by a
   Lipschitz retraction. The theorem is not restricted to Hilbert sources.

4. [Harmand--Werner--Werner, Chapter IV](https://page.mi.fu-berlin.de/werner99/mbuch/buch4.pdf),
   Example IV.1.1(a), p. 158, proves L-embeddedness of L1(mu) through its
   projection-band/AL-space structure. This is the appropriate classical
   target compactness ingredient; it does not assert that all L1 spaces are
   dual Banach spaces.

5. The local OpenAI manuscript *Metric Markov Cotype Two of ell1*, dated
   October 5, 2026, states N2(ell1) <= 12 sqrt(21) and supplies a finite-cut
   argument. Its supplied source attributes the standard finite cut
   representation to Deza--Laurent, Chapter 4. I read its introductory claims
   and finite-cut/reconstruction section; I did not independently certify its
   complete martingale proof in this priority task. The parent project has a
   separate mathematical audit. Its manuscript date alone is not evidence
   of the first public release date.

The relevant primary PDF hashes, computed from the project's downloaded
copies, are:

| File | SHA256 |
| --- | --- |
| naor_deholder_v1.pdf | 1c0ff70969b593f4dd4421d264add7bb3be3903622c1bc2e6f5758ae6941a9e9 |
| naor_deholder_v2.pdf | 176e89d6df829642fd8555586c9e5ff553113a99ff190b0f1de142633267f2b7 |
| mendel_naor.pdf | caf077bec643c224e4db3ef3fd0da18daf11f595933ed0ee4b966fb1dd905dd2 |
| hww_iv.pdf | e71ba24e82eddb51f0e842b3dd43efc0889cf5670bfddc34afdf2f561f38dce3 |

## Search for the complete forthcoming manuscript

Independently inspected on the audit date:

- General exact-title and author searches for the forthcoming title,
  Mendel plus de-Höldering, and Markov cotype plus Naor plus 2026.
- [The arXiv exact-title search](https://arxiv.org/search/?query=Metric+invariants+from+de-H%C3%B6ldering+factorization&searchtype=all&abstracts=show&order=-announced_date_first&size=50),
  which returned no results.
- [Manor Mendel's arXiv author search](https://arxiv.org/search/?query=Mendel%2C+Manor&searchtype=author&abstracts=show&order=-announced_date_first&size=50),
  which displayed 40 results, the latest originally announced in July 2026;
  no forthcoming factorization/cotype manuscript was listed.
- Broader arXiv title searches for metric invariants and de-Holdering.
- [Naor's primary homepage](https://web.math.princeton.edu/~naor/) and its
  publicly indexed manuscript directory.
- [Mendel's primary research list](https://sites.google.com/site/mendelma/Home/research).
- The v2 HTML and PDF reference entries, which name the forthcoming preprint
  but supply neither a manuscript URL nor an arXiv identifier.

No complete copy was found. The export.arxiv API endpoint returned an error;
the public author-search page worked. Some broader unaccented search queries
gave unrelated results, so they are weak negative evidence. The appropriate
statement is 'not located in these searches', never 'no public proof exists'.
Outside input might clarify availability, but the project policy forbids
outreach and none was initiated or prepared.

## Checkable deduction covering every original quantifier

Let Y0 = L1([0,1]; R). Assume the announced result N2(Y0) <= N < infinity.
The next reductions require no new cotype mechanism.

### From standard L1 to every weighted finite ell1

For m positive weights w_r, partition [0,1] into m equal intervals I_r.
Embed the weighted normed space E with norm sum_r w_r |u_r| by

    J(u) = sum_r m w_r u_r 1_{I_r}.

This is an isometry. The map

    P(g) = sum_r m (integral_{I_r} g) 1_{I_r}

is a norm-one projection onto J(E). Apply the announced cotype inequality
in Y0 to J(z_i), and project its witnesses with P. All witness costs and
one-step distances decrease; the original pair distances are unchanged.
Consequently N2(E) <= N. This uses complemented copies, not the false claim
that cotype passes to all subspaces.

### Exact transfer to arbitrary measure spaces

Take finitely many real x_i in L1(mu), where mu is any nonnegative
countably additive measure on any sigma algebra. Choose measurable,
finite-almost-everywhere representatives and alter a common measurable
null set if necessary. Define

    v = min_i x_i,
    b_B = (min_{i in B} x_i - max_{i outside B} x_i)_+,
    w_B = integral b_B,

for the nonempty proper subsets B of [n]. These are measurable and
integrable: their absolute values are bounded by twice sum_i |x_i|.
Discard zero weights. With z_i(B) = 1_{i in B}, define

    T(u) = v + sum_B u_B b_B.

At each point, order the real numbers x_i, grouping ties. The positive b_B
are precisely the successive upper-level gaps. Telescoping yields

    T(z_i) = x_i,
    ||x_i - x_j||_1 = sum_B w_B |z_i(B) - z_j(B)|,
    ||T(u) - T(u')||_1 <= sum_B w_B |u_B - u'_B|.

Thus apply the cotype inequality in E to z_i and reconstruct its witnesses
using T. Every left-side distance contracts, while every right-side original
distance is exact. This proves N2(L1(mu;R)) <= N with no loss of constant.
If there are no positive weights, all x_i coincide and the cotype assertion
is trivial. Nothing uses sigma-finiteness, atomlessness, separability, or
completeness of the measure space.

The transfer is short, exact, and valid. Its validity does not make the
standard cut decomposition a new theorem.

### From cotype to all Markov-type-two sources

For a Banach space, the ordinary barycenter of finitely supported
probability measures satisfies

    ||B(nu) - B(eta)|| <= W1(nu,eta) <= W2(nu,eta).

The first inequality follows from any coupling and the triangle inequality;
the second follows from Cauchy--Schwarz with total mass one. Therefore the
Wp barycentric constant required by Mendel--Naor is Gamma = 1 for p = 2.
The stronger '2-barycentric' uniform-convexity condition is not needed.
Their Theorem 1.11 now gives, on every finite subset D of any Markov-type-2
space X, an extension agreeing with f on D intersect S and having Lipschitz
constant at most

    K = c_MN M2(X) N Lip(f).

This exact dependence on M2(X) is inherited from that theorem.

### Infinite subsets and nonseparable spaces

For completeness, normalize at an anchor s0 in S by subtracting f(s0).
Require every finite D to contain s0. Its extension values obey

    ||F_D(x)|| <= K d(x,s0).

In Y** form the product, over x in X, of the corresponding weak-star compact
closed balls. Prescribed values at points of S and constraints

    ||F(x)-F(y)|| <= K d(x,y)

are closed. Every finite list of constraints is realized by a finite
extension. Product compactness therefore gives a map X -> Y** satisfying all
constraints, for arbitrarily large X and S. Compose with the norm-one
projection Y** -> Y given by HWW's L-embeddedness. This fixes Y, so the
result extends the entire f with the same K. Empty S has the zero extension.

This is the usual bidual compactness passage already indicated by
Mendel--Naor; no countability assumption and no identification of Y* with
the original measure space's L-infinity are used.

Combining the four steps gives the exact original theorem, conditionally
on the announced cotype input. When that input is replaced by an audited
proof of the supplied ell1 theorem, the same reductions give an
independently checkable unconditional proof; this does not change the
chronology of the previously announced result.

## What is and is not new

The best defensible description of the proposed package is an explicit
quantifier-complete consequence of a previously announced cotype theorem,
with an adaptation of an available cut proof. It does not add a substantive
previously unresolved statement beyond the cotype input. O(sqrt(p)) for
standard Lp sources was itself expressly announced in September; standard
Markov-type estimates and the preceding transfer give the wider measure
scope immediately.

Naor v1 alone must not be said to prove the full sharp M2(X) target:
factorization through Hilbert space together with known Hilbert-target
extension gives a quadratic dependence on M2(X), rather than the linear
dependence requested here. The September cotype announcement is the
additional ingredient that makes the linear bound an immediate consequence.

No proposed rescue has demonstrated substantial novelty:

- Nonseparable spaces, arbitrary measures, complex realification, norm-one
  complemented targets, and Banach-isomorphic target variants are routine
  consequences, not an identified new research result.
- General target subspaces cannot be asserted: the required cotype is not
  hereditary, and known counterexamples explicitly obstruct that inference.
- Noncommutative L1 targets do not admit this pointwise min/max argument and
  are excluded by the original mandatory boundary.
- Merely supplying an explicit but unoptimized universal constant does not
  establish a new endpoint theorem.
- A genuinely different cotype construction, sharp optimal constant, or
  substantial new extension phenomenon could have research value, but none
  has been established by this task and these possibilities are not novelty
  claims.

Recommendation: preserve the verified deduction and priority evidence in
research notes, and withhold a preprint advertised as a new solution of this
core target. Do not claim the full forthcoming proof was found, do not
ascribe its cotype breakthrough to this follow-on project, and do not label
an elementary scope reduction a new resolution merely to satisfy the
publication objective.

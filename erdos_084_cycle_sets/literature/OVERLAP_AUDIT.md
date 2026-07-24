# Literature and overlap audit

Last checked: 2026-07-24.

## Confirmed public status

- [Erdős Problem 84](https://www.erdosproblems.com/latex/84) still lists
  \[
  f(n)/2^{n/2}\to\infty
  \]
  as open. It attributes the \(2^{n/2}\)-scale lower bound to Erdős and
  Faudree.
- [Rajko Nenadov, *Improved bound on the number of cycle sets*
  (2026)](https://escholarship.org/uc/item/4k75b3z7) proves the current upper
  bound
  \[
  f(n)\le2^{n-\Omega(\sqrt n/\log^{3/2}n)}.
  \]
  Page 2 of the published article explicitly says that the best known lower
  bound remains Faudree's \(2^{n/2}\) construction and that even an
  improvement to \(2^{(1+c)n/2}\) would be interesting. Its new machinery is
  for upper bounds via Hamiltonian-chord fingerprints and containers, not the
  protected lower-bound construction developed here.
- [Alvin Dunås, *The number of sets of cycle lengths for graphs on \(n\)
  vertices* (2026)](https://uu.diva-portal.org/smash/get/diva2%3A2077189/FULLTEXT01.pdf)
  is directly relevant. The
  [Uppsala listing](https://www.uu.se/institution/matematiska/utbildning/examensarbete)
  and indexed abstract say that it lower-bounds the cycle-set count by a
  computationally amenable function and obtains numerical evidence for the
  same open limit.

## Access audit

The Dunås thesis remains the principal novelty risk. The full text could not
be read during either checkpoint. Direct PDF downloads timed out; direct web
fetches failed; Chrome reached either a connection timeout or the host's
Anubis gate; Jina returned HTTP 401; and AllOrigins returned HTTP 520. The
record and abstract were accessible through indexing, but there is no honest
page-level comparison of the mathematical body.

Primary record locations:

- [DiVA record](https://uu.diva-portal.org/smash/record.jsf?pid=diva2%3A2077189);
- [full-text endpoint](https://uu.diva-portal.org/smash/get/diva2%3A2077189/FULLTEXT01.pdf);
- [persistent URN](https://urn.kb.se/resolve?urn=urn%3Anbn%3Ase%3Auu%3Adiva-591570).

## Component-level novelty verdict

Until the thesis is obtained and compared line by line, none of the following
may be claimed as literature-cleared original:

1. the reduction to one-dimensional difference supports;
2. the exact protected signature family \(\mathcal F_m(P)\);
3. the protected geometric realization;
4. the sequence \(S_m\);
5. the eight-way recurrence;
6. the union-shadow excess \(E_m\);
7. the associated finite diagnostics.

The twin-boundary identity

\[
g_m(P)=2|\mathcal B_P|
 -\bigl(|\mathcal A_P|-|\mathcal A_P\vee V(P)|\bigr)
\]

and the join-commuting embedding \(A\mapsto A\cup\{m\}\) are plausible
original developments in the notation of this program, but they are
elementary, have no independent asymptotic consequence, and have not been
cleared against Dunås. The universal Boolean down-set inequality and all-\(m\)
Hamming-two Hall assertion remain conjectural; the exact matching
computations through \(m=7\) are finite evidence only.

The defensible publication boundary is therefore a public research report
that says the problem is open, no asymptotic bound was improved, and novelty
is not cleared against Dunås. A paper or preprint claiming new mathematics is
not justified at this checkpoint.

## External input

No outside researcher was contacted. If source access remains blocked, the
human researcher may wish to obtain the thesis independently and place a copy
in this project for audit. Under the independent-research policy, no outreach
draft has been prepared and no communication has been initiated.

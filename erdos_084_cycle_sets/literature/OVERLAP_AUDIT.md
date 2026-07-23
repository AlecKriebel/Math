# Literature and overlap audit

Last checked: 2026-07-23.

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
  f(n)\le2^{n-n^{1/2-o(1)}}.
  \]
  Its abstract and stated method concern upper bounds via containers, not the
  protected lower-bound construction developed here.
- [Alvin Dunås, *The number of sets of cycle lengths for graphs on \(n\)
  vertices* (2026)](https://uu.diva-portal.org/smash/get/diva2%3A2077189/FULLTEXT01.pdf)
  is directly relevant. The indexed abstract says that it lower-bounds
  \(f(n)\) by a more computable function and obtains numerical evidence for
  the same open limit.

## Unresolved overlap risk

The Dunås thesis is the principal novelty risk. Its full PDF could not be
retrieved during this checkpoint because the source repeatedly timed out,
although the record and abstract were accessible through indexing. Therefore
none of the following may yet be claimed as original:

1. the reduction to one-dimensional difference supports;
2. the exact protected signature family \(\mathcal F_m(P)\);
3. the sequence \(S_m\);
4. the eight-way recurrence;
5. the union-shadow excess \(E_m\).

The new diagnostics in this folder - the exact \(m=8,9,10\) shadow totals,
the failed collision and rank conjectures, the Boolean down-set conjecture,
and the alternating-defect orbit reduction - must also be compared line by
line once the thesis is available.

## External input

No outside researcher was contacted. If source access remains blocked, the
human researcher may wish to obtain the thesis independently and place a copy
in this project for audit. Under the independent-research policy, no outreach
draft has been prepared and no communication has been initiated.

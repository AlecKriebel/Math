# Hostile review: order-12 parameter-four DoubleLex reduction

Status: **ACCEPT EQUISATISFIABLE DOUBLELEX STRENGTHENING**

This review covers:

- `math/lemmas/order12_k4_doublelex.md` at SHA-256
  `d5be9b6373d7aa7c49dec32c18c6202698b35fe05a1f58b2b97dcc98d9114a76`;
- `src/search/k4_doublelex.py` at SHA-256
  `e5aeb23eb3938631c62a29df45a880839fa9c8384121e0ec310d9740936baba1`;
- `tests/test_k4_doublelex.py` at SHA-256
  `36282f747f971cf5a57c90e1b645fbe2cd76ab51c3413b7b2268547144322469`.

I found no counterexample or blocking gap.

## Mathematical verdict

Let \(F_0\) be the accepted anchored formula before the existing outer-row
sort. The proposed \(S_8\times S_4\) action is valid:

- edges \(e_{uv}\) map to \(e_{\pi(u)\pi(v)}\);
- common-neighbor witnesses \(w_{T,x}\) map to
  \(w_{\pi(T),\pi(x)}\);
- family states \(f_D\) map to \(f_{\pi(D)}\); and
- move variables \(m_{D,r,u}\) map to
  \(m_{\pi(D),\pi(r),\pi(u)}\).

The no-\(K_5\), triple-witness, domination, eternal-response, and
independent-state clauses are set-indexed and covariant. Anchor-clique units
are preserved by \(S_4\). Although connected-cut generation selects the
side containing vertex 0, moving vertex 0 merely selects the complementary
side of the same cut and therefore the same crossing-edge clause.

For the complete coloring bank, push old anchor \(i\) to \(\pi(i)\) and
rename old color \(c\) to \(\pi(c)\). The new color at anchor \(\pi(i)\) is
\(\pi(i)\), so anchor normalization is restored. Since all \(4^8\) outer
color rows are present, the bank is permuted as a set.

The hostile probe reconstructed all 18,381 semantic variable actions and
checked the complete 114,637-clause, 1,179,330-literal \(F_0\) clause
multiset under all ten adjacent-transposition generators: three generators
of anchor \(S_4\) and seven generators of outer \(S_8\). Every image matched
exactly. It also verified that these clauses are the exact prefix of the
frozen parent, before the accepted 105-clause row-order suffix.

Now choose a row-major lexicographically least image of a model's finite
\(S_8\times S_4\) orbit. An inverted pair of rows can be swapped to decrease
the word, so rows are nondecreasing. If adjacent columns are inverted, they
agree in every earlier row and have \(1,0\) at their first difference.
Swapping those columns leaves the earlier row-major positions unchanged
and changes the first affected position from 1 to 0, again decreasing the
word. Thus the same least image has both nondecreasing rows and
nondecreasing columns.

This proves
\[
F_0\text{ SAT}\iff F_0\land R\land C\text{ SAT}.
\]
Together with the already accepted row breaker
\(F=F_0\land R\), it proves
\[
F\text{ SAT}\iff F\land C\text{ SAT}.
\]
The reverse implications are literal formula weakening. No assertion that
every labeled model satisfies \(C\) is needed or made.

As a regression independent of the proof, the probe exhausted all 512
binary \(3\times3\) matrices and all their row/column images; every
row-major least orbit image had both rows and columns nondecreasing.

## Comparator and implementation audit

For adjacent columns \(a,b\), each emitted clause fixes a common prefix and
forbids the unique first difference \(a_t=1,b_t=0\). An independent
generator, using a closed-form edge-variable allocation rather than the
implementation's edge map, reproduced the suffix byte for byte.

An exhaustive evaluation of all \(2^{16}=65,536\) assignments to one
eight-bit comparator accepted exactly \(a\le_{\mathrm{lex}}b\). The
independent census is:

- 255 clauses and 3,586 literals per comparator;
- 765 clauses and 10,758 literals for three adjacent comparators;
- 37,710 suffix bytes;
- suffix SHA-256
  `328eeeaadc688bbce63fd3ffd952f86a4eb9209e6d0abf5542979fe54ebdbbe0`.

Appending that exact suffix to the exact frozen parent
`adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac`
produces:

- 18,381 variables;
- 115,507 clauses;
- 1,190,774 literals;
- 4,030,657 bytes;
- SHA-256
  `14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7`.

The implementation refuses a parent with any different size or SHA-256,
parses the exact DIMACS census, adds no variables, checks the suffix census,
and uses create-new publication rather than replacing an existing output.
Its four tests passed, including the full 65,536-row truth table, exact
output hash, parent mutations, and forbidden-import audit.

## First-row consequence and claim boundary

Ordered columns force the first row to be nondecreasing, so it is one of
`0000`, `0001`, `0011`, `0111`, or `1111`. The last would join the anchored
\(H\)-\(K_4\) to an \(H\)-\(K_5\), which the exact target forbids. Hence the
four remaining first-row cubes cover all orbits of the strengthened
formula.

This review proves only an equisatisfiable symmetry strengthening and binds
its exact generated CNF. It does not prove the strengthened CNF UNSAT,
exclude the \((12,4)\) slice, alter the immutable 16-cube production run,
or resolve the γ–θ conjecture.

Executable evidence is in
`reviews/order12_k4_doublelex_hostile_probe.py`; its canonical recorded
output is in `reviews/order12_k4_doublelex_hostile_probe.json`.

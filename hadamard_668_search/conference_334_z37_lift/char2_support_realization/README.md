# Exact characteristic-two support realization for both `C37` quotient types

## Result

This checkpoint closes the **support-realizability question in
characteristic two** for one integral quotient representing each of the
two binary quotient types (up to fiber permutation and complement).

For each target, it constructs 45 binary cyclic blocks of length 37 such
that:

- every block has its prescribed exact integer margin;
- diagonal blocks have zero identity coefficient and are inverse-symmetric;
- lower blocks are the cyclic reversals of upper blocks;
- every nonzero quadratic-residue lag occurs in six diagonal blocks and
  every nonresidue lag occurs in three;
- all 2,997 coefficients of

  \[
  A(x)^2+A(x)=\delta I+
  (1+x+\cdots+x^{36})J
  \quad\text{in }\mathbf F_2[C_{37}]
  \]

  hold exactly.

The two frozen exact witnesses are:

| target | text SHA-256 | JSON semantic SHA-256 |
|---|---|---|
| type 1 | `3f77fc3d39fc6b8dfd33efbba846e61ca835581d15f9ae4c12d8f57a3249e697` | `fc5b7f7bd19250731d148bdbae1200cb64b08851bd8e28d5f0047d5983273dc4` |
| type 2 | `2e5087308dceb18398daaba4b1ca5868d755cecb41ae7892f988ae8083c03c22` | `2f03cbaaf514b4a90bd4aa7ad7f533b8abd9e0b1fddb724aeb40d718db51465c` |

The JSON files contain full `9 x 9` hexadecimal word matrices and can be
loaded directly as hints by the adjacent mod-four search.

Keeping the type-1 diagonal projection fixed and varying only exact-margin
unit-circle phases reduced its independent mod-four carry defects from
`722/1503` to `672/1503`:

```text
TYPE1_SUPPORT_WITNESS_CARRY672.txt SHA-256
bb6d7431ace29949e0af8077afdd7377b7dd3c615832e197562018fe18eee060

TYPE1_SUPPORT_WITNESS_CARRY672.json semantic SHA-256
7d6e7d1827a4129fc12916c3007772511e40bd011f6b5193349029de3522aaae
```

The frozen optimized seed has 72 diagonal and 600 off-diagonal defects,
versus 72 and 650 in the first type-1 witness.  It remains an exact
mod-two witness, not a mod-four solution.

## Strict scope

This is **not** a conference graph, conference matrix, or Hadamard matrix.
It proves the adjacency equation only modulo two, equivalently the sign
conference-core equation modulo eight.  It does not prove the adjacency
equation modulo four or over the integers.

Thus the result says something strategically important but negative:
neither binary quotient type is obstructed by characteristic two, even
after imposing exact block margins and the full `6/3` diagonal trace law.
The next genuine gate is the carry/mod-four layer.

## Field model and CRT

Because `ord_37(2)=36`,

\[
\mathbf F_2[C_{37}]
\cong \mathbf F_2\times K,\qquad
K=\mathbf F_2[x]/(1+x+\cdots+x^{36})
=\mathbf F_{2^{36}}.
\]

Inversion is the unitary involution
\(\bar z=z^{2^{18}}\), with fixed field
\(L=\mathbf F_{2^{18}}\).

If `d` is represented by a polynomial of degree below 36 and `q` is its
prescribed trivial-factor bit, the unique 37-bit CRT inverse is

\[
f=d+c\Phi_{37},\qquad
c=q+d(1).
\]

This identity makes Hamming support extraction exact and cheap.  It also
shows why the parity quotient and nontrivial unitary factor are algebraically
independent before Hamming margins are imposed.

Let \(\eta\) be the nonresidue quadratic period, so
\(\eta^2+\eta=1\).  At the nontrivial factor,

\[
D^2+D=I,\qquad E=D+\eta I,\qquad E^2=E.
\]

The trace orientation makes \(E\) a rank-four Hermitian projection.

## Constructive diagonal prescription

For either binary quotient `Q`, the dense central projection

\[
E_0=Q+\eta(I+J)
\]

is Hermitian and idempotent.  A max-flow first chooses a `9 x 18`
inverse-pair incidence table having:

- the nine prescribed diagonal margins; and
- column sums six on quadratic residues and three on nonresidues.

After shifting those target words by \(\eta\), their field sum is zero,
as required for the diagonal of a rank-four projection.

The search then uses exact two-coordinate unitary rotations

\[
U(c,u)=
\begin{pmatrix}
c&u(1+c)\\
\bar u(1+c)&c
\end{pmatrix},
\qquad c\in L,\quad u\bar u=1.
\]

Here \(U^*=U\) and \(U^2=I\).  If the current principal block is
\(\left(\begin{smallmatrix}a&b\\\bar b&d\end{smallmatrix}\right)\),
the new first diagonal entry is

\[
c^2a+(1+c)^2d+
c(1+c)(\bar u b+u\bar b).
\]

The program enumerates the exact trace image of the unit circle and solves
this equation without floating point.  It prescribes eight diagonal
entries sequentially; the ninth is forced by trace.  For both target
quotients the resulting projection is checked again from scratch for
Hermitian symmetry and idempotence.

This is a constructive theorem for the two recorded target incidence
tables.  The code exposes the more general rotation equation, but this
checkpoint does not claim that every possible trace-law table is reachable.

## The norm-support trace law

Let \(f\) be any binary word of length 37 and weight \(k\), evaluated at a
nontrivial 37th root \(\zeta\).  Then

\[
\boxed{
\operatorname{Tr}_{L/\mathbf F_2}
\bigl(f(\zeta)f(\zeta^{-1})\bigr)
=\binom{k}{2}\pmod2.}
\]

Proof: write the norm using the parity autocorrelations
\(c_t=|S\cap(S-t)|\pmod2\).  The 18 inverse-pair terms satisfy

\[
\operatorname{Tr}_{L/\mathbf F_2}
(\zeta^t+\zeta^{-t})=1,
\]

because `2` is primitive modulo 37.  Summing the 18 autocorrelations
counts each unordered pair of support points once.

For a Hermitian projection, its diagonal equation gives

\[
\sum_{j\ne i}E_{ij}\bar E_{ij}=E_{ii}+E_{ii}^2.
\]

Taking the absolute trace shows that the graph whose edge `ij` is labeled
\(\binom{k_{ij}}2\bmod2\) must be Eulerian.  The independent census audit
checks that all 625 integral quotient classes obey this condition.  In
fact it follows from the diagonal quotient equation modulo four, so it
does not eliminate a quotient; it is nevertheless the exact compatibility
gate for off-diagonal norm fibers.

## Fixed-diagonal phase CSP

After the diagonal is fixed, conjugation by
`diag(p_0,...,p_8)` with \(p_i\bar p_i=1\) preserves it and changes

\[
E_{ij}\longmapsto p_iE_{ij}\bar p_j.
\]

The unit circle is cyclic of order

\[
2^{18}+1=262145.
\]

For every edge the program exhausts all 262,145 phase differences and
records those producing the requested Hamming weight.  Once the norm-trace
labels match, every edge domain in both runs is nonempty.  The remaining
problem is a nine-vertex cyclic difference CSP.  Fixing `p_0=1`, both
recorded runs found a complete assignment in nine search nodes.

The product-of-marginals heuristic gives about \(2^{87.52}\) phase
assignments for type 1 and \(2^{89.50}\) for type 2 if edge constraints
were independent.  These are heuristics, not exact counts, but they explain
why the final phase CSP is easy once the norm gate is satisfied.

As a secondary objective, a deterministic single-coordinate conditional
phase walk sampled 200,000 further exact-margin assignments.  Every move
stayed inside the phase CSP.  Independent integer convolution replay
reduced the type-1 carry defect count from 722 to 672.  This is an attained
upper bound inside one fixed-diagonal phase fiber, not a certified minimum.

## Reproduction

Build and regenerate either witness:

```text
clang++ -O3 -std=c++20 \
  hadamard_668_search/conference_334_z37_lift/char2_support_realization/search_char2_support.cpp \
  -o /tmp/search_char2_support

/tmp/search_char2_support 1
/tmp/search_char2_support 2

# Reproduce the frozen 200,000-step type-1 carry optimization.
/tmp/search_char2_support 1 200000
```

Wall-clock timing is written to standard error, so the certificate text on
standard output is byte-reproducible.

Replay both frozen JSON artifacts independently, using only bit-level
cyclic convolution:

```text
python3 \
  hadamard_668_search/conference_334_z37_lift/char2_support_realization/verify_all_char2_support.py
```

Audit the norm-trace condition on the frozen 625-class quotient dump:

```text
python3 \
  hadamard_668_search/conference_334_z37_lift/char2_support_realization/audit_norm_trace_quotients.py \
  /tmp/z37_625_canonical_final.txt
```

On the project machine, deterministic witness generation took about
6.4 seconds for type 1 and 9.8 seconds for type 2, with peak RSS below
49 MB.  Aggregate independent replay took under 0.2 seconds.

# Erdős Problem 84: cycle sets via difference supports

This folder is the paused checkpoint of a provisional, AI-assisted research
program on the open lower-bound half of Erdős Problem 84.

> **Paused 24 July 2026.** The problem remains open, and this work does not
> improve the published asymptotic bounds. See [`STATUS.md`](STATUS.md) for
> the scoped record and [`RESUME.md`](RESUME.md) for the only conditions under
> which this program should restart. The public, non-paper checkpoint is at
> <https://aleckriebel.github.io/Math/research/erdos-problem-84/>.

For an \(n\)-vertex graph \(G\), let \(\mathcal C(G)\) be the set of lengths of
cycles in \(G\), and let \(f(n)\) count the possible sets \(\mathcal C(G)\).
The target is

\[
\frac{f(n)}{2^{n/2}}\longrightarrow\infty.
\]

The current route uses fan graphs to reduce the problem to counting positive
difference supports

\[
\Delta(X)=\{|x-y|:x,y\in X,\ x\ne y\}.
\]

A protected central construction then produces finite signature families
\(\mathcal F_k(P)\). The proved reduction shows that unboundedness of

\[
T_k=\frac{S_k}{8^k},
\qquad
S_k=\sum_{P\subseteq[2k]}|\mathcal F_k(P)|,
\]

would solve the problem.

## Status at pause

The exact signature definition and the elementary recurrence
\(S_{k+1}\ge 8S_k\) have been reconstructed. A sharper recurrence

\[
S_{m+1}\ge 8S_m+2E_m
\]

has also been recovered. The unresolved step is to prove a nonsummable
normalized gain, for example \(E_m\gg 8^m/m\). Exact enumeration through
\(m=10\) supports the stronger global inequality \(mE_m\ge S_m\). A
Boolean down-set charging conjecture, exactly verified through \(m=10\), is
the strongest surviving restart target. An all-\(m\) identity collapses its
two positive unsafe-boundary families to two typed copies of one family.
A bounded representation-aware Hall graph succeeds through \(m=7\) only
at full row-selection Hamming radius two; no all-\(m\) matching rule is yet
known.
A defect-sensitive cyclic-orbit route is
now secondary because explicit four-run words suggest its required constant
may decay like \(1/m\).

The bounded Hall experiment was then stopped at its prescribed \(m=6,7\)
gates. It proved the all-\(m\) twin-boundary identity

\[
g_m(P)=2|\mathcal B_P|
 -\bigl(|\mathcal A_P|-|\mathcal A_P\vee V(P)|\bigr),
\]

falsified the one-local-edit matching rule, and exactly verified the
representation-aware Hamming-two matching through \(m=7\). The repairs grew
less canonical in the larger case, and no uniform matching theorem emerged.
Even such a theorem would leave the separate trace lower bound unproved.

Nothing in this folder should be described as a solution unless
[`STATUS.md`](STATUS.md) explicitly records a completed and audited proof.

## Reproduction

The reference implementation uses only the Python standard library:

```sh
python3 src/signature_counts.py --max-k 4
python3 -m unittest discover -s tests -v
c++ -O3 -std=c++17 src/full_signature_counts.cpp -o /tmp/full_counts
/tmp/full_counts --max-m 8
c++ -O3 -std=c++17 src/orbit_diagnostics.cpp -o /tmp/orbit_diagnostics
/tmp/orbit_diagnostics --m 8
c++ -O3 -std=c++17 src/targeted_orbit.cpp -o /tmp/targeted_orbit
/tmp/targeted_orbit --word 00000001111100011111
c++ -O3 -std=c++17 -pthread src/downset_diagnostics.cpp -o /tmp/downset
/tmp/downset --m 8 --threads 4
```

Larger exact cases are expensive because both \(P\) and the union-closure vary
exponentially. Discovery code and independent verification code will be kept
separate as the project grows.

## Sources and overlap risk

- [Erdős Problem 84](https://www.erdosproblems.com/84)
- [R. Nenadov, *Improved bound on the number of cycle sets* (2026)](https://escholarship.org/uc/item/4k75b3z7)
- [OEIS A067247: difference supports of subsets of an interval](https://oeis.org/A067247)
- [Alvin Dunås, *The number of sets of cycle lengths for graphs on n vertices* (2026)](https://urn.kb.se/resolve?urn=urn%3Anbn%3Ase%3Auu%3Adiva-591570)

The recent Dunås thesis studies the same one-dimensional distance-set route.
A complete overlap audit is required before making any novelty claim; current
source-access status is recorded in
[`literature/OVERLAP_AUDIT.md`](literature/OVERLAP_AUDIT.md).

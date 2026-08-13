# Independent exact-byte audit of the final 46,872-pair theorem

**Independent hostile proof-first audit, 2026-08-12 PDT.**  The immutable
target is

~~~text
research_notes/proof_first_two_linkage_46872_final_theorem.md
SHA-256 dae2a58f170836427ffc053ff931c1909d64ac591d77b971591b0d5814526cde
206 lines / 7,865 bytes
~~~

The verdict is **STRICT PASS** at these exact bytes.  The theorem is a
disjoint union of completed fixed-support-pair theorems.  No finite
certificate supplies a stochastic implication, and no trajectory switches
between branch potentials.

## 1. Exact universe and certificate replay

For ten binary complexes, assign each complex to the first support, the
second support, or neither.  Inclusion--exclusion for two ordered supports
of size at least two gives

\[
 3^{10}-2(2^{10}+10\,2^9)+(1+10+10+90)=46{,}872. \tag{1.1}
\]

The target's final certificate and test rehash as

~~~text
certificate 5b249ded4b54801f7eb5ab9ced943ed566216e1228c0e07f3e205b1eef319288
test        dd51ce074aa43bb4722d176ef4c85face956c924150681d5cae32f3b615c5e76
~~~

All four certificate dependencies rehash to the values asserted in its
source.  Its five focused tests were rerun independently and all passed.
The literal branch manifest is

\[
\begin{array}{l|r|l}
\text{branch}&\text{pairs}&\text{pair fingerprint}\\ \hline
\text{completed mixed orbit}&27{,}462&\texttt{1bf337cf143c6eb4}\ldots\\
\text{active-invariant orbit gap}&432&\texttt{5516d6071b2b9d07}\ldots\\
\text{strict positive invariant}&146&\texttt{d1fc7112f8a08605}\ldots\\
\text{level-set residual}&336&\texttt{ea3d7b08d39c6f9c}\ldots\\
\text{outside-mixed remainder}&18{,}496&\texttt{eb7db151e42eb956}\ldots
\end{array} \tag{1.2}
\]

The five sets are pairwise disjoint and their union is the complete ordered
support universe.  The full-universe and branch-manifest fingerprints are

~~~text
00446e17dca5ce6b75e86cdc755b5660d7c94b68fa4f3e6f028efa40d02c6c60
bd6ae54bff3aed8fc4fedb9255fe0b7377a28dc67404d6a5bea41c6aa4ac1bba
~~~

respectively.  The certificate explicitly records
`recurrence_claim=False` and performs no orientation, rate, population,
history, or class enumeration.

## 2. Analytic scope of every branch

The four cited pair-theorem targets and their cited audits were rehashed:

~~~text
completed mixed orbit
target a91e8c31f35312ef4b9063e8f5a48af534861145db2236e662ea6cc1eff8e30e
audit  32eec768b2d8d701664f3ace2b1a7c04fd3790a4811eba5e05d56a8fa903e73b

active-invariant orbit gap
target 7edab78daabbf7e492851efe5326ccc228adfcb57f02cd5ff55eaa7056e034c8
audit  1110efc0760ed8714fc4bf203739152820f6f9a18cbdc0e92716638a707140fd

level-set residual
target 6e9ddcaccd03fe64b1c6a57cbaef052e984eaf7b7e2e87c4df52ca1240787a6c
audit  35b18c365ce954594397b4c48ed55f7d11c847af37594f0fb354517434f76d72

outside-mixed remainder
target e7b08be8b6ca3ff604f3975bdae18b526db532ea1168f25bf21170d8248b5106
audit  192dfc3d79401c57416b582b45aeb0140f0c1ad3e0f90ab80acaae48e3b9a090
~~~

Each target literally concludes nonexplosion and positive recurrence on
every closed irreducible class for arbitrary strongly connected labelled
orientations and positive labelled rates on its fixed pair scope.  In
particular:

1. the 27,462 theorem removes the invalid active-only invariant seeds before
   orbit closure and transfers completed seed theorems by exact generator
   conjugacy;
2. the 432 theorem replaces the failed chart-exit composition by a global
   population-Foster proof, including its 24 exceptional service pairs;
3. the 336 theorem is global across the homogeneous and anisotropic boundary
   faces and uses physical-time Foster estimates; and
4. the 18,496 theorem is itself the disjoint union of the 11,842 statewise
   population-Foster pairs and the 6,654 common-marked pairs.

For the remaining 146 pairs, a vector $h>0$ annihilates every reaction
vector.  Hence $h\cdot x$ is fixed on a population class, and its
nonnegative integer level set is finite.  This is a complete classwise
recurrence proof, not the invalid use of an invariant vanishing on one
coordinate.

## 3. No cross-potential seam

A physical network has one immutable ordered support pair $P$.  The exact
certificate assigns $P$ to one branch before the chain starts.  Therefore
the population, marked, workload, and finite-invariant arguments appearing
in different branches are never compared along one trajectory.  The same
fixed-pair observation closes the internal 11,842/6,654 split of the final
branch.  The proof is a union of theorems, not a state-dependent menu of
branch potentials or a terminal-SCC circulation.

The standard reaction convention excludes distinct linkage classes sharing
a complex; deleting a zero-displacement label leaves the generator
unchanged.  Weak reversibility makes each nontrivial linkage orientation
strongly connected.  Networks with fewer than three species embed by
adjoining unused coordinates, so the stated at-most-three-species scope is
contained in the certified universe.

## 4. Nonexplosion

Let $N(x)=1+|x|_1$.  A degree-two source cannot increase total population,
because every target is binary.  All population-increasing reactions have
degree-zero or degree-one source, bounded jump size, and combined positive
population drift bounded by $C N(x)$.  Localization at
$\tau_R=\inf\{t:N(X_t)\ge R\}$, Dynkin's formula, and Gronwall give

\[
 \mathbb E_x N(X_{t\wedge\tau_R})\le N(x)e^{Ct}. \tag{4.1}
\]

Letting $R\to\infty$ rules out finite-time population escape.  On each
bounded-population set there are finitely many states and the full hazard is
bounded, so population-neutral quadratic clocks cannot accumulate there.
This proves nonexplosion of the minimal chain and matches every branch
theorem's scope.

## 5. Publication checks

The exact target was independently converted with Pandoc's single-backslash
TeX-math reader and compiled with Tectonic.  The result is a four-page
letter-size PDF with zero compiler or layout
diagnostics.  Every page was inspected visually; equations (2.1)--(2.4),
the branch hashes, Theorem 1.1, and the final nonexplosion displays are
unclipped and legible.  A text and hidden-byte scan found no placeholder,
corrupt control sequence, or non-ASCII control byte.

Therefore the final theorem at the exact SHA above receives **STRICT PASS**.

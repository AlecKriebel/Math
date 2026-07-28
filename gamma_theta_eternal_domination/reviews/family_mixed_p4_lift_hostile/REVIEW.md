# Hostile review: the family-list mixed \(P_4\) lift

## Revision confirmation: manifest v2

**PASS.**

The revised candidate is confirmed at seven-file tree SHA-256

`33a7dfb07261dff1d3ec4442269600c09e3e2b4566254710d4cc1dbab7c6897d`.

The two nonblocking metadata findings from the original review were
resolved exactly:

1. `OBSERVED_RESULTS.json` now says “an arbitrary (possibly proper)
   eternal triple-family”; and
2. `NOTE.md` no longer claims that literal commands are stored in the
   observed JSON.  It accurately names the variable counts, clause
   counts, times, memory, and relevant generator and solver hashes that
   are present there.

This was checked byte-specifically, not merely by reading the new prose.
Replacing the single revised paragraph in `NOTE.md` by the original
paragraph reconstructs the original note hash
`3f03a3bbcdb6b81cc1ff286c3b1c40eedf4219c87dab0b8a6ffc34b2eb186c07`.
Replacing the single revised scope phrase in `OBSERVED_RESULTS.json`
reconstructs its original hash
`272611aa8642cdf656140d311cf44edd4b173299ebedc7d2e08b8f4cf89fc4cf`.
Reversing only the manifest schema, two classification labels, and those
two bound artifact hashes reconstructs the original manifest hash
`7cd259df8d4a408526715c86d0710eea474ca333d2459d73cb5979f7ba7ff33e`.

The four substantive artifacts are byte-identical to those already
audited:

| unchanged artifact | SHA-256 |
|---|---|
| `RESEARCH_LOG.md` | `be8fecde21819ab7309fbfcc25e597943506fe6c7ba51db0cd7a48e2ca11400a` |
| `cegar_dominating_pairs.py` | `c8fe9ddb9ae7fe1f333eac0da7492cfe951937c660174e61870b58e05b198e2b` |
| `minimize_gamma_pairs.py` | `0968db1d4f5910c7ce763df051a62cfb44e38d07127330af8224caeee40f6c48` |
| `synthesize.py` | `3b822ffcd544e8a5585ac9f9063b2fd6ca92b8cc247a8c1c78b74c46db78dcfb` |

The revised manifest binds all six non-manifest artifacts, all three
accepted dependencies, and the pinned solver correctly.  No theorem,
proof, encoding, run row, dependency, or source-code byte changed.
Therefore every substantive conclusion of the original hostile audit
transfers unchanged, and its two editorial qualifications are now
discharged.

The original v1 audit is preserved below as an immutable historical
record.

## Original v1 verdict

**PASS.**

At the frozen candidate tree hash

`1e4a808e1eb45d9f03f8f74ed199e30cd20c51bd3d7c566fea4d73869329fae4`,

Theorem 1 is a valid weakening of the accepted C-148 input, Theorem 2 is
the exact synchronous greatest-kernel dichotomy, and the discovery SAT
material is correctly kept at **OBSERVED_DISCOVERY_ONLY** status.  No
argument or clause turns an omitted family response into a graph nonedge.

The result proved here is only that both omitted endpoint \(c\)-swaps
dominate, together with the survivor-or-positive-finite-rank normal form.
It does not exclude the family-list mixed \(P_4\), prove the complete
\(k=3\) case, or resolve the gamma--theta conjecture.

## Frozen bytes

The tree hash above is SHA-256 of the following seven lines, in
lexicographic basename order, each terminated by `\n`:

| candidate artifact | SHA-256 |
|---|---|
| `MANIFEST.json` | `7cd259df8d4a408526715c86d0710eea474ca333d2459d73cb5979f7ba7ff33e` |
| `NOTE.md` | `3f03a3bbcdb6b81cc1ff286c3b1c40eedf4219c87dab0b8a6ffc34b2eb186c07` |
| `OBSERVED_RESULTS.json` | `272611aa8642cdf656140d311cf44edd4b173299ebedc7d2e08b8f4cf89fc4cf` |
| `RESEARCH_LOG.md` | `be8fecde21819ab7309fbfcc25e597943506fe6c7ba51db0cd7a48e2ca11400a` |
| `cegar_dominating_pairs.py` | `c8fe9ddb9ae7fe1f333eac0da7492cfe951937c660174e61870b58e05b198e2b` |
| `minimize_gamma_pairs.py` | `0968db1d4f5910c7ce763df051a62cfb44e38d07127330af8224caeee40f6c48` |
| `synthesize.py` | `3b822ffcd544e8a5585ac9f9063b2fd6ca92b8cc247a8c1c78b74c46db78dcfb` |

All candidate artifact hashes and all three accepted-dependency hashes
match `MANIFEST.json`:

| accepted dependency | SHA-256 |
|---|---|
| accepted C-148 note | `c58271538d6253ec4ac56d8df7edb7a067d67453dcf8393352a5bf394ed71d34` |
| accepted C-070 source | `079c3ee0e880eb211f7e7460193e9c4c8212d70350965e668eb462f4f0a4db04` |
| accepted C-148 hostile review | `8f9680d99797cb43b23383a573d17e71797f15ff6420e70d7d747e00409ca25c` |

The candidate directory was read only.  This review writes only under
`reviews/family_mixed_p4_lift_hostile/`.

## 1. Theorem 1: one genuine endpoint defect is enough

Assume first that

\[
Q_0=\{a,b,x_0\}
\]

does not dominate.  A missed vertex \(d\) satisfies

\[
da,db,dx_0\notin E(G).
\tag{1.1}
\]

The candidate's collision audit is complete:

- \(d\notin\{a,b,x_0\}\), since occupied vertices are dominated;
- \(d\ne c\), since accepted C-070 gives \(cx_0\in E(G)\);
- \(d\ne x_1\), since the positive \(a\)-role gives
  \(ax_1\in E(G)\);
- \(d\ne x_2\), since the positive \(b\)-role gives
  \(bx_2\in E(G)\); and
- \(d\ne x_3\), since the positive \(b\)-role gives
  \(bx_3\in E(G)\).

Thus \(d\) is a genuine eighth vertex.  Since the retained root
\(S=\{a,b,c\}\) dominates \(d\), (1.1) forces \(cd\in E(G)\).
The triple \(\{a,b,d\}\) is independent.  It belongs to every eternal
three-family: attack its unoccupied vertices successively; a guard
already installed on this independent triple cannot answer another such
attack, so each response increases the number of installed vertices.
Consequently it is the retained direct \(c\)-replacement of \(S\).
The nonedges \(ad,bd\) exclude the other two direct roles, and hence

\[
L_S^{\mathcal F}(d)=\{c\}.
\tag{1.2}
\]

The positive \(c\)-roles at \(x_1,x_2\) retain
\(\{a,b,x_1\}\) and \(\{a,b,x_2\}\).  Those two states must dominate
\(d\); because \(a,b\) miss \(d\), this forces

\[
dx_1,dx_2\in E(G).
\tag{1.3}
\]

Equations (1.1)--(1.3), the exact family lists, endpoint saturation, and
the induced complement path give exactly the accepted C-148 ledger:

\[
14\text{ fixed edges}+9\text{ fixed nonedges}
+5\text{ optional pairs}=\binom82.
\]

The optional pairs are precisely

\[
bx_0,\quad bx_1,\quad ax_2,\quad ax_3,\quad dx_3.
\]

No negative static role is used.  In particular, a missing family role
only excludes its direct family state.  In the local overapproximation,
the accepted restoration condition excludes that direct state because
the omitted anchor is not supplied by the exact family list; it does not
exclude the corresponding graph edge.

For each of the \(2^5=32\) graph completions, accepted C-148 starts with
all core-dominating, restoration-compatible core triples and applies
literal synchronous one-guard deletion.  I replayed both the packed
checker and the clean-room hostile checker.  Both returned all 32
terminal kernels empty; the clean-room pair partition was
\((14,9,5,28)\).

The external-vertex argument is sound.  If a global family state is a
triple inside the eight-vertex core and the attacked vertex is also in
the core, every one-guard successor remains a core triple.  Thus the
global family's core portion is contained in every local deletion
horizon.  External states and external attacks can only add obligations;
they cannot repair a displayed attack from a displayed source.

Finally, the relabeling

\[
a\leftrightarrow b,\qquad
x_0\leftrightarrow x_3,\qquad
x_1\leftrightarrow x_2,\qquad c\mapsto c
\]

preserves the exact list pattern and the induced-path incidences and maps
\(Q_0\) to \(Q_3\).  It also maps the complete collision and optional-pair
ledger to itself.  It is only a proof relabeling; no graph automorphism is
assumed.  The argument therefore proves domination of both endpoint
states.

## 2. Theorem 2: exact synchronous ranks

Let \(\mathcal K_0\) be all dominating triples and obtain
\(\mathcal K_r\) by simultaneously deleting from
\(\mathcal K_{r-1}\) every state with an unoccupied attack having no
one-edge successor in \(\mathcal K_{r-1}\).  The stable set is the
literal greatest eternal triple-family.

Theorem 1 rules out rank zero for \(Q_0,Q_3\).  On a finite graph, every
dominating triple either survives the stable kernel or is deleted in a
unique positive finite round, so the stated alternatives are exhaustive
and disjoint.

If \(Q_i\) is deleted in round \(r\), the deletion definition supplies
an unoccupied attack \(t_i\) for which no adjacency-eligible successor
lies in \(\mathcal K_{r-1}\).  Therefore every swap

\[
Q_i-u+t_i,\qquad u\in Q_i,\quad ut_i\in E(G),
\]

has rank below \(r\).  Nondominating successors have rank zero.
A successor deleted in round \(r\) would still lie in
\(\mathcal K_{r-1}\), which is why the synchronous convention yields a
strict inequality rather than a weak one.  No successor class is omitted.

If the exact lists occur in the greatest family itself, absence of the
\(c\)-roles means exactly that the direct states \(Q_0,Q_3\) are absent
from that family.  Together with their domination, this makes both ranks
positive and finite.  For a merely specified family, its omission of a
state says nothing about survival in the unrestricted greatest family;
the candidate keeps this distinction throughout.

## 3. No family omission is converted to graph nonadjacency

The proof and code pass this audit:

- The only anchor--path graph edges inferred from the family lists are
  the six **positive** roles.
- The six negative roles leave their graph pairs undecided unless some
  separate argument fixes them.
- The only new graph nonedges in Theorem 1 are the three genuine
  missed-vertex incidences \(da,db,dx_0\).
- The C-148 optional ledger retains all four negative-role
  anchor--path pairs as optional.
- In `synthesize.py`, a positive role adds a family-state unit and an
  edge unit; a negative role adds only `-family(state)`, never
  `-edge(role,target)`.
- The candidate explicitly allows an endpoint state omitted from the
  specified family to survive the unrestricted greatest kernel.

## 4. SAT encoding, scope, and observed status

The frozen generator encodes the advertised one-guard model:

1. unordered variables encode a simple graph;
2. the seven named vertices are distinct, the root is independent, and
   the four path vertices induce \(P_4\) in the complement;
3. the six positive direct states are retained and the six negative
   direct states are forbidden;
4. every retained triple dominates every unoccupied vertex;
5. for every retained state and unoccupied attack, at least one response
   witness moves one occupied guard along one \(G\)-edge and retains the
   resulting triple;
6. every four-set spans a \(G\)-edge, encoding \(\alpha\le3\); and
7. every vertex pair has an outside vertex missed by both guards,
   encoding the absence of a dominating pair.

The retained independent root gives \(\alpha\ge3\); the explicit eternal
three-family gives \(\gamma^\infty\le3\); and
\(\alpha\le\gamma^\infty\) gives equality.  Root domination and the
pair constraints similarly give \(\gamma=3\).

An independent count from the clause families gives

\[
\begin{aligned}
V(n)&=\binom n2+\binom n3
      +3(n-3)\binom n3+(n-2)\binom n2,\\
C(n)&=28+8(n-3)\binom n3+\binom n4
      +(2n-3)\binom n2.
\end{aligned}
\]

These formulas match every reported variable and clause count for
\(12\le n\le22\).  A fresh replay with the pinned CaDiCaL 3.0.1 binary
(SHA-256
`51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6`)
returned code 20 and `UNSAT` at all eleven orders, with the same formula
sizes.

This replay does not promote the table.  There is still no included
DRAT/LRAT proof, independently reconstructed CNF, proof checker, or
coverage theorem, and the recorded historical time and memory figures
were not independently authenticated.  The candidate repeatedly says
that these runs are observed discovery evidence and prove neither the
bounded UNSAT statements nor a universal exclusion.  That labeling is
honest.

## Nonblocking metadata precision

This section records the two original v1 findings.  Both are resolved
exactly in manifest v2, as confirmed above.

Two literal wording changes would make the discovery metadata exact, but
neither affects a theorem or the PASS verdict:

1. `OBSERVED_RESULTS.json` calls the encoded family “an arbitrary proper
   eternal triple-family.”  The formula actually permits any specified
   eternal triple-family, including one equal to the greatest family.
   Replace this with “an arbitrary (possibly proper) eternal
   triple-family,” matching `NOTE.md`.
2. `NOTE.md` says exact “commands” are in `OBSERVED_RESULTS.json`, but
   that JSON contains the solver/generator identities and run parameters,
   not literal command strings.  Either remove “commands” from that
   sentence or add a command field per run.

## Final scope

| item | result |
|---|---|
| Theorem 1 endpoint domination | **PROVED**, using accepted C-070 and C-148 |
| named-vertex distinctions | **COMPLETE** |
| reflected endpoint | **VALID RELABELING** |
| Theorem 2 survivor/rank dichotomy | **PROVED** |
| strict lower-rank successor row | **EXACT** |
| omitted response treated as nonedge | **NO** |
| SAT model | **MATCHES STATED ONE-GUARD EQUALITY SCOPE** |
| orders \(12\) through \(22\) | **OBSERVED ONLY; REPLAYED, NOT CERTIFIED** |
| family-list mixed \(P_4\) exclusion | **OPEN** |
| complete \(k=3\) theorem | **OPEN** |
| universal gamma--theta conjecture | **OPEN** |

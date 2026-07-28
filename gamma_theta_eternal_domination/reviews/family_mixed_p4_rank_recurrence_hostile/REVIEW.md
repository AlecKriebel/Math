# Hostile review: family mixed-\(P_4\) rank recurrence

Review date: 2026-07-28 PDT

Frozen candidate commit:
`0017e89b00d7d8314cec5d4f3e5cd6358ea6f4a4`

## Verdict

**FAIL PENDING NONSUBSTANTIVE PROOF-BINDING CORRECTIONS.**

I found no substantive mathematical counterexample to the claimed partial
recurrence.  The single-hit rank descent, named-target audit, eight-cell
multi-hit table, all three uses of C-145, and the
dominating-pair/completion-clique alternative are correct at their stated
scope.

The frozen package is nevertheless not ready for promotion because two
accepted dependencies used in the proof are neither identified nor bound,
and one of those omissions leaves a literal logical step unstated:

1. Lemma 2.1 needs accepted C-064 ridge response-covariance, or its missing
   opposite-vertex domination argument.  The identity of two successor
   sets alone does not imply equality of response roles, because a response
   role also requires a move edge.
2. Theorem 4.2 uses accepted arbitrary-state restoration without naming or
   binding C-058.
3. The rank-one terminal at lines 218--222 should identify accepted C-151
   Lemma 1.1, the exact family-list one-defect form of C-148, rather than
   leave the scope to be inferred from the static statement of C-148.

These are repairable citation/proof-binding defects, not evidence against
the mathematics.  Candidate files were not modified during this review.
After the exact corrections below, a short revised-byte re-audit should be
sufficient.

The desired full eight-cell recurrence remains **OPEN**, exactly as the
candidate says.  Nothing reviewed here proves the family-list mixed path
impossible, proves the complete \(k=3\) case, or resolves the
\(\gamma\)--\(\theta\) conjecture.

## Frozen candidate bytes

| Artifact | SHA-256 |
|---|---|
| `math/working/family_mixed_p4_rank_recurrence/NOTE.md` | `cf01ad09c7ec684dc25d47db57c2dd47e7878eb0dbd1be7a128a4d5ec8c0698b` |
| `math/working/family_mixed_p4_rank_recurrence/OBSERVED_RESULTS.json` | `d0d54d2cd8d6b84e668fcf2d4f6965fc593fb657b305dd6036e4e66ae46f6658` |
| `math/working/family_mixed_p4_rank_recurrence/RESEARCH_LOG.md` | `e3a449a49b4765e204d3c7e92d71388e52289cd032df1a769892fbb181295e8a` |
| `math/working/family_mixed_p4_rank_recurrence/MANIFEST.json` | `5d7e2d0faf09db50f29801bcb19d1549c7da80ef35fe6763722d722ad1c0e3d1` |

The first three hashes agree with the frozen manifest.  The manifest does
not hash itself, as expected.

## Required exact corrections

### R1. Bind and correctly invoke C-064 in Lemma 2.1

Candidate lines 94--103 currently argue

> the two possible direct successors are literally the same triple;
> therefore the exchanged roles occur together.

The conclusion is true, but the displayed reason omits the move-edge
condition in the definition of a family response.  Equality of the
successor three-set proves equal family membership, not by itself equal
graph adjacency.

Replace that step by either of the following equivalent repairs:

1. cite accepted C-064 Theorem 3.1 directly, since \(S,S'\) are retained
   independent ridge states, \(x_j\notin S\cup S'\), and the ridge
   transposition \(g\leftrightarrow r\) fixes \(x_j\); or
2. after (2.2), add the missing two-way domination argument.  If
   \(S-g+x_j=(S\cap S')\cup\{x_j\}\) is retained, it must dominate \(r\).
   Every shared root vertex misses \(r\) because \(S'\) is independent, so
   \(rx_j\in E(G)\), making \(r\) a response at \(S'\).  Conversely,
   retained membership at \(S'\) forces \(gx_j\in E(G)\) by domination of
   \(g\).

The preferred publication wording is to cite C-064 and retain the
one-sentence domination explanation, because it makes clear why no omitted
response is converted into a graph nonedge.

Add these exact dependency bindings:

| Dependency | Path | SHA-256 |
|---|---|---|
| C-064 source | `math/working/cross_state_response_exchange.md` | `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7` |
| C-064 hostile review | `reviews/cross_state_exchange_hostile/REVIEW.md` | `bc5011d85d333fb66fce3ea563e4cc80cf016090cc3427e44187b2e40fb5f9f8` |

### R2. Name and bind C-058 at Theorem 4.2

Candidate line 345 invokes “accepted arbitrary-state restoration” but the
manifest has no restoration dependency.  The use is valid:

\[
D=\{c,x_0,x_1\},\quad
S-D=\{a,b\},\quad
D-S=\{x_0,x_1\},
\]

while

\[
L_S(x_0)\cup L_S(x_1)=\{a,c\}
\]

does not restore \(b\).  Therefore \(D\notin\mathcal K\).

Identify this as C-058, arbitrary-state restoration, and add:

| Dependency | Path | SHA-256 |
|---|---|---|
| C-058 source | `math/working/universal_transition_private_neighborhood_attack.md` | `71384d66373ab4cbffa7ced60973971cf39b72a0315eac31ad522abd1afa2f47` |
| C-058 hostile review | `reviews/universal_transition_hall_hostile_review/REVIEW.md` | `4369b3b85912e3e9a534ea2a63c9cc12ab06cb701cd2227ea77c912665c51d45` |

C-058 states the restoration theorem using viable lists; its proof
actually constructs \(S-u+x\) inside the specified family and therefore
supplies the family-response form used here.  The exact family-list form is
also written explicitly as Lemma 1 in the accepted frozen-color-projection
lane, but no extra theorem is needed once the C-058 proof is cited
accurately.

### R3. Bind the rank-zero terminal to C-151 Lemma 1.1

At candidate lines 218--222, replace

> These are exactly the one-defect hypotheses isolated from C-148.

by wording such as

> These are exactly the hypotheses of accepted C-151 Lemma 1.1, the
> family-response-list one-defect form of the C-148 local kernel.

This removes a scope ambiguity.  The headline C-148 theorem assumes exact
static lists, whereas the recurrence transports exact family lists.
Accepted C-151 already proves that the one genuine endpoint domination
defect plus those family lists and C-070 endpoint saturation is sufficient.
The candidate manifest already binds C-151 correctly.

### R4. Update manifest and research log

In `MANIFEST.json`:

- add the C-064 and C-058 source hashes above under
  `accepted_dependencies`;
- add their hostile-review hashes under `hostile_reviews_read`;
- update the bound `NOTE.md` and `RESEARCH_LOG.md` hashes after revision.

In `RESEARCH_LOG.md`, record the two explicit dependencies and the
domination step for exchanged roles.  No theorem statement needs to be
weakened.

## Proof reconstruction

### Model and equality consequences

All proof branches use the standard one-guard model:

- attacks are at unoccupied vertices;
- one occupied guard moves along one graph edge;
- a retained successor is a dominating triple; and
- \(\mathcal K\) is the literal greatest fixed point obtained by
  synchronous deletion from all dominating triples.

From

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\]

and the parameter chain, every maximal independent set has size three.
Every independent triple belongs to every eternal triple-family, hence to
\(\mathcal K\).  No proof branch uses all-guards movement or treats a
missing family response as a graph nonedge.

### Rank convention and the \(h=1\) boundary

The convention is internally consistent:

\[
\rho(D)=0\iff D\notin\mathcal K_0,
\]

\[
\rho(D)=h\iff
D\in\mathcal K_{h-1}\setminus\mathcal K_h
\quad(h\ge1).
\]

Thus a deleting attack for a rank-\(h\) state has every
adjacency-eligible successor at rank below \(h\).  C-146 applies to

\[
Q=S-c+x_i,\qquad Q'=S'-c+x_i
\]

with independent sources \(S,S'\), shared fixed responder \(c\), fixed
target \(x_i\), and ridge distance one.  Both ranks are finite: \(Q\) is
positive finite by C-151 and the exact greatest-family list, while exact
ridge transport keeps the \(c\)-role absent at \(Q'\).  Hence

\[
|\rho(Q)-\rho(Q')|\le1.
\]

Deletion gives \(\rho(Q')<h=\rho(Q)\), so integer arithmetic forces

\[
\rho(Q')=h-1,
\]

including \(\rho(Q')=0\) when \(h=1\).  C-151 Lemma 1.1 excludes that
rank-zero domination defect.  There is no off-by-one error.

### Single-hit collision audit

Every path target has at least two graph neighbors in the independent
root:

- \(x_1,x_2\) have their two positive list roles;
- \(x_0,x_3\) have their positive endpoint roles plus the C-070
  \(c\)-edge.

Therefore a single-hit deleting target cannot be a named path vertex.  It
cannot be \(a\) or \(b\), which are occupied in \(Q_i\), and it cannot be
\(c\), whose attack has the retained move \(x_i\to c\) back to \(S\).

If the unique root neighbor were \(c\), domination by
\(Q_i=\{a,b,x_i\}\) would force \(x_ir\in E(G)\).  The move
\(x_i\to r\) reaches the independent triple \(\{a,b,r\}\), which is
retained, contradicting deletion.  Thus the unique root neighbor is
\(g\in\{a,b\}\), and \(S'=S-g+r\) is an independent ridge neighbor.
The successor \(Q-g+r\) is exactly the transported endpoint row.  This
proves the single-hit theorem once R1 is inserted.

Finite iteration is sound: each single-hit step lowers a positive integer
rank by exactly one and preserves the complete exact list pattern.
The rank-one terminal is impossible by C-151, so a genuine realization
must meet a multi-hit deleting row.

### Named-target audit

For \(Q_0=\{a,b,x_0\}\):

- At \(x_2\), inducedness of the complement path gives
  \(x_0x_2\in E(G)\), and the \(c\)-role at \(x_2\) retains
  \(\{a,b,x_2\}\).  Hence \(x_2\) cannot delete.
- At \(x_1\), start from retained \(A_0=\{b,c,x_0\}\).  The guard \(x_0\)
  has no move edge.  If \(bx_1\) is absent, \(c\to x_1\) is the unique
  possible response.  If it is present, the competing successor
  \(\{c,x_0,x_1\}\) is excluded by C-058 restoration because \(b\) is
  not restored.  Closure therefore retains
  \(\{b,x_0,x_1\}\), which is also the legal \(a\)-successor from
  \(Q_0\).  Hence \(x_1\) cannot delete.
- At \(x_3\), inducedness gives \(x_0x_3\in E(G)\), and the corresponding
  successor is \(Q_3\).  If the attack deletes \(Q_0\), then
  \(\rho(Q_3)<\rho(Q_0)\).

The displayed reflection proves the \(Q_3\) rows.  Root vertices were
already excluded.  Therefore every unresolved deleting target is fresh.

### Eight-cell table

For

\[
S=\{c,\ell,m\},\qquad Q=\{u,\ell,m\},
\]

a fresh multi-hit root neighborhood is exactly one of

\[
\{c,\ell\},\quad\{c,m\},\quad\{\ell,m\},\quad S.
\]

Splitting on \(ur\) gives eight cells.  Direct intersection with \(Q\)
reproduces all eight mover sets in the candidate.

The conclusions are correct:

1. In the \(\{c,\ell\}\), \(ur=0\) cell, \(Q\) has only the
   \(\ell\)-successor \(C_\ell\), which is omitted.  The retained positive
   \(\ell\)-response state \(D=\{c,m,u\}\) then has only \(c\) adjacent to
   \(r\), and its \(c\)-successor is the same omitted \(C_\ell\).  This
   contradicts closure.
2. In the \(\{c,m\}\), \(ur=0\) cell, \(C_m\) is the unique successor.
   Survival of \(Q\) through horizon \(h-1\) and deletion at \(h\) give
   \(\rho(C_m)=h-1\), including zero at \(h=1\).
3. In either \(\{c,g\}\), \(ur=1\) cell, the deleting row excludes
   \(C_u=S-c+r\), so the \(c\)-role at \(r\) is absent.  The other outer
   guard misses \(r\), and closure forces the singleton list \(\{g\}\).
4. In either \(\{\ell,m\}\) cell, graph adjacency excludes \(c\) and
   closure leaves a nonempty subset of \(\{\ell,m\}\).
5. In the all-root, \(ur=1\) cell, deletion again excludes \(C_u\), so
   the \(c\)-role is absent.  In the \(ur=0\) cell no such exclusion is
   available, exactly as the table records.

The table makes no recurrence claim beyond these consequences.

### C-145 direction audit

All three invocations have the correct orientation and a genuine common
nonneighbor:

| Cell | Forward active edge | Hypothetical missing reverse | Common nonneighbor | C-145 retained ridge |
|---|---|---|---|---|
| \(\{c,m\},ur=0\) | \(\ell\triangleright u\) | \(u\not\triangleright\ell\) | \(r\) | \(\{\ell,u,r\}=C_m\) |
| \(\{c,g\},ur=1\) | \(g\triangleright r\) | \(r\not\triangleright g\) | other outer \(q\) | \(\{g,r,q\}=C_u\) |
| \(\{\ell,m\}\), singleton \(\{g\}\) | \(g\triangleright r\) | \(r\not\triangleright g\) | \(c\) | \(\{g,r,c\}\), the omitted other-outer response |

Each C-145 ridge is exactly the state already excluded by the relevant
deleting row or singleton list.  Hence the stated reciprocal edge follows.
No C-145 direction is reversed.

### Completion-clique alternative

In the outer collision, \(cr\notin E(G)\).  The set

\[
W_{cr}=N_{\overline G}(c)\cap N_{\overline G}(r)
\]

is empty exactly when \(\{c,r\}\) dominates.  If nonempty, two nonadjacent
members of \(W_{cr}\), together with \(c,r\), would make an independent
four-set, so \(W_{cr}\) is a \(G\)-clique.  A completion vertex missing both
\(\ell,m\) would make \(S\cup\{w\}\) independent of size four, so every
completion hits at least one outer anchor.

If \(w\ell\notin E(G)\), the independent triples

\[
\{c,\ell,w\},\qquad\{c,r,w\}
\]

share a ridge and are both retained.  Since \(\ell r\in E(G)\), both
one-guard exchanges survive, giving \(r\leftrightarrow\ell\); the
\(m\)-statement is symmetric.  Finally \(\gamma(G)=3\) excludes the empty
completion set.  The theorem is correct.

## Independent bookkeeping audit

`audit.py` is a clean-room symbolic checker.  It imports no candidate code
or campaign evaluator.  It independently verifies:

- every path vertex has exactly the two required root neighbors used in the
  single-hit collision audit;
- the missing domination step in exchanged ridge transport;
- rank arithmetic for \(1\le h\le32\), including \(h=1\);
- the three named \(Q_0\) target rows and the reflection involution;
- all eight mover and successor rows;
- exact identity of every C-145 retained ridge with the excluded successor;
  and
- the set identities in the completion-clique alternative.

It deliberately encodes only positive family roles as graph edges.  No
negative role is entered as a nonedge.

Command:

```text
python3 -I -B -W error \
  reviews/family_mixed_p4_rank_recurrence_hostile/audit.py
```

Result: `PASS_BOOKKEEPING_ONLY`.

| Item | SHA-256 |
|---|---|
| `audit.py` | `84a0c2c158d0517563914535948669ea914516fcd5e329f2eac4206437f5160b` |
| canonical stdout | `af2e63e9decaf222f78f075546693a8036425e1b672c45e633eb9b0e2e4c9a62` |

This finite audit corroborates bookkeeping; the universal implications are
accepted or rejected on the proofs above.

## Replays

### C-148 one-defect kernel

The following four independent or cross-checking commands all completed:

```text
python3 -I -B -W error math/working/mixed_p4_infinite_descent/verify.py
python3 -I -B -W error math/working/mixed_p4_infinite_descent/verify_bitset.py
python3 -I -B -W error reviews/mixed_p4_infinite_descent_hostile/independent_check.py
python3 -I -B -W error math/working/reverse_rank_descent/verify_controls.py
```

The three C-148 implementations each returned 32 empty terminal kernels.
The rank-control replay reproduced the sharp unit and distance-two
star-Lipschitz examples, exact rank-two-to-rank-one single-hit descent, and
the rank-one multi-hit boundary.

### Discovery-only orders \(7\) through \(11\)

Using the frozen C-151 generator and pinned CaDiCaL 3.0.1, a fresh replay
returned:

| \(n\) | variables | clauses | status |
|---:|---:|---:|---|
| 7 | 581 | 1,414 | `UNSAT` |
| 8 | 1,092 | 2,702 | `UNSAT` |
| 9 | 1,884 | 4,726 | `UNSAT` |
| 10 | 3,045 | 7,723 | `UNSAT` |
| 11 | 4,675 | 11,963 | `UNSAT` |

These remain **OBSERVED_DISCOVERY_ONLY**.  No DRAT/LRAT proof, independent
formula constructor, or proof-checker package was created here.

## Exact status table

| Item | Verdict on frozen mathematics |
|---|---|
| exact ridge list transport | **TRUE, but frozen proof/dependency binding incomplete** |
| single-hit rank descent | **PROVED after R1 binding** |
| rank-one C-151 terminal | **PROVED; citation must be made exact** |
| finite descent to a multi-hit row | **PROVED after R1 binding** |
| named path target audit | **PROVED; C-058 binding missing** |
| eight-cell mover/list reduction | **PROVED** |
| three C-145 reciprocity consequences | **PROVED** |
| completion-clique alternative | **PROVED** |
| full eight-cell recurrence | **OPEN** |
| family mixed-\(P_4\) exclusion | **OPEN** |
| complete \(k=3\) theorem | **OPEN** |
| universal conjecture | **OPEN** |

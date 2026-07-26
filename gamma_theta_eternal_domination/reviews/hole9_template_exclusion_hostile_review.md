# Hostile review of the `hole9` graph-theoretic exclusion

## Verdict and binding

**ACCEPT without reservation.**

This review binds the exact bytes of
`math/lemmas/hole9_template_exclusion.md` with SHA-256
`4305dcfc170f665d0c97b5d4601c3dd226099b61e11a2ad28a15fc66ee36c1f2`.
The review was performed on 2026-07-25 after the note was amended to specify
the values of unused witness and move variables explicitly.

The theorem in the reviewed note is a sound graph-theoretic consequence of
the exact recovered CNF and its accepted addition-only RUP certificate.  No
quantifier error, complement reversal, one-guard-model error, relabeling gap,
or enlargement of the certified universe was found.

## Exact evidence checked

The following decisive artifacts were read and compared with the reviewed
argument.

| Artifact | SHA-256 |
|---|---|
| Reviewed exclusion note | `4305dcfc170f665d0c97b5d4601c3dd226099b61e11a2ad28a15fc66ee36c1f2` |
| Core reductions | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` |
| Maximum-independent-state theorem | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |
| Complement-side \(k=3\) dictionary | `54d7cafdc7047d75ed58739f6a773344a2f780aaecd0eafde8ed01a0692c6256` |
| C-014 structural note | `00d6fb851a3cb50ed907a593b0379376571251f8604974b5b67e05e2b0705d6e` |
| C-017 antihole-elimination note | `9e572203c09e082c3cbdfc0cdae8e4166007af3f909b73f7d8d2e196f04ddc4f` |
| Recovery acceptance record | `ebede11b90e6e0b73d75f57c7706ba2e62e699281fcd8c15a208886dd53db291` |
| Recovery hostile review | `4a8bba44ea71090652a5cfbc2b54565594fdb945dfe109193e9921157ffd563c` |
| Exact base-plus-170-cut CNF | `2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d` |
| Addition-only RUP proof | `24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab` |

The acceptance record changed after the mathematical review solely by
appending `root_replay.full_suite_clean_replay`, which reports a successful
238/238 clean test-suite replay after disk space became available.  Removing
that one 540-byte appended member reconstructs byte-for-byte the previously
reviewed acceptance record with SHA-256
`63d9ec3076049114093c70425f51ca215695fa0981d647eb09dd55b6e4624e93`.
The earlier 227-pass/11-preflight-refusal resource event remains present and
unchanged.  No mathematical claim, formula field, proof field, certificate
binding, erratum, or hostile-review field changed.  The update is therefore
claim- and proof-neutral; this review binds the current acceptance-record
hash shown in the table.

The recovery hostile review independently reconstructed the formula, checked
all 170 cut records, replayed all 4,705 RUP additions with a standalone
implementation, and confirmed that the last addition is the empty clause.
This review does not substitute a new SAT checker for that accepted audit;
it checks the mathematical implication from the intended graph universe to
the already certified-unsatisfiable formula.

## Line-by-line implication audit

### Lines 5--11: universe and notation

The note fixes a finite simple graph on exactly 12 vertices and sets
\(H=\overline G\).  It explicitly separates the recovered certificate from
the nonterminal source CEGAR run and from the `hole5` and `hole7` branches.
Those are the correct universe and exclusions.

### Lines 15--22: theorem quantifiers

The quantified graph class exactly matches the mathematical claim in the
recovery acceptance record:
\[
  G\text{ connected},\quad |V(G)|=12,\quad
  \gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G),
\]
with a hub-free induced \(C_9\) in \(H\).  “Hub-free” is correctly quantified
over every vertex outside the chosen induced cycle.  The theorem neither
omits a target condition used by the CNF nor adds a conclusion about another
template.

### Lines 26--39: contradiction setup and sound relabeling

From \(\gamma(G)=3\), no two-set dominates \(G\).  For each pair
\(\{a,b\}\), failure of closed-neighborhood domination supplies a vertex
outside the pair adjacent in \(G\) to neither endpoint, equivalently a common
neighbor of \(a,b\) in \(H\).  This is the accepted complement dictionary in
the correct direction.

After orienting and cyclically labeling the induced \(C_9\) by
\(0,\ldots,8\), vertices \(0\) and \(1\) have no common neighbor on its rim:
the cycle is induced and has length at least five.  Their required common
neighbor is therefore external.  Labeling one such vertex \(9\) satisfies
the template units \(e_{09}=e_{19}=1\), while the remaining two labels are
unconstrained.  This relabeling loses no graph in the stated universe and
uses no unproved symmetry breaking.

### Lines 41--47: static CNF assignment

Assigning \(e_{uv}=1\) exactly when \(uv\in E(H)\) uses the complement, not
\(G\), as the encoded graph.  Since
\(\alpha(G)=\omega(H)=3\), every four-set contains an \(H\)-nonedge and all
no-\(K_4\) clauses hold.

For each pair, choosing one actual common neighbor, setting its witness
variable true, and setting all other witness variables false satisfies both
the witness disjunction and its two edge implications.  The induced-cycle
units, the two fixed external-common-neighbor units, and the external
no-hub disjunctions follow directly from the chosen labeled hub-free
\(C_9\).  Finally, every proper cut has a \(G\)-edge because \(G\) is
connected; since a \(G\)-edge is an \(H\)-nonedge, every encoded connectivity
clause has a true negative edge literal.

Thus every static and template clause receives a fully specified, valid
assignment.  There is no accidental interchange of connectivity of \(G\)
with connectivity of \(H\).

### Lines 49--59: one-guard eternal-family assignment

The equality \(\gamma^\infty(G)=3\) supplies a nonempty eternal family of
dominating triples in the stipulated one-guard-moves model.  Setting exactly
its family variables true satisfies nonemptiness.  For each selected state
and each unoccupied attacked vertex, choosing one promised response sets one
move variable true; setting every unused move variable false completes the
auxiliary assignment.

The true response variable names one guard in the current triple, and its
clauses require that guard and the attacked vertex to be nonadjacent in
\(H\), hence adjacent in \(G\).  Its successor variable names exactly the
triple obtained by replacing that one guard with the attacked vertex.
Closure of the eternal family makes that successor selected, and selection
subjects it to all domination clauses.  No occupied attack, simultaneous
movement, or nondominating successor is introduced.

Every triangle of \(H\) is an independent three-set in \(G\).  The accepted
independent-set-forcing theorem puts every independent set whose size equals
the guard count into every eternal family of that size.  Hence all redundant
triangle-selection clauses hold.  The note therefore constructs a model of
the entire base formula, not merely of its graph projection.

### Lines 61--70: validity of all 170 coloring cuts

For a recorded map \(c:V(H)\to\{0,1,2\}\), the appended clause is the
disjunction of the positive \(H\)-edge variables \(e_{uv}\) over same-color
pairs.  Since
\[
  \chi(H)=\theta(G)>3,
\]
no such map is a proper coloring of \(H\).  At least one same-color pair is
therefore an \(H\)-edge and satisfies the cut.  The quantifier is applied
separately to each of the 170 recorded maps; it does not require those maps
to enumerate all three-color assignments.  Consequently every target graph
model satisfies the exact accumulated cut set.

### Lines 72--77: certified contradiction

The stated SHA-256, 6,886-variable count, and 20,200-clause count match the
sealed formula.  The accepted standalone replay establishes that each of
the 4,705 additions is RUP relative to the preceding formula and additions,
and that the last addition is the empty clause.  This proves that the exact
base-plus-cut CNF is unsatisfiable.  It therefore contradicts the model
constructed in the preceding paragraphs and proves the theorem.

### Lines 81--86: corollary from C-014 and C-017

C-014 says that \(\gamma^\infty(G)=3\) forbids an induced odd wheel in
\(\overline G\).  Hence any induced \(C_9\) in a putative parameter-three
counterexample complement has no external vertex complete to its rim: it is
automatically hub-free and falls under the theorem.

C-017, together with its accepted SPGT, common-neighbor, and order-12
consequences, reduces every surviving order-12 parameter-three complement to
a hub-free induced \(C_5\), \(C_7\), or \(C_9\).  Removing the certified
`hole9` branch leaves the stated \(C_5\) or \(C_7\) alternative.  There is no
misuse of an odd hole in \(G\) in place of one in \(H\).

The connected hypothesis causes no corollary gap.  By component additivity,
a counterexample component of any parameter-three counterexample is itself a
counterexample.  The accepted minimum-parameter theorem gives that component
parameter at least three, which exhausts the original total domination
number three; no other nonempty component can remain.  Thus every genuine
parameter-three counterexample is connected.

### Lines 90--98: certificate boundary

The listed acceptance, sealed-package, and hostile-review locations are the
correct supporting artifacts.  The warning that the source checkpoint
remains `running` is necessary and accurate.  The note also correctly leaves
the complete \((n,k)=(12,3)\) result open pending separate accepted
certificates for `hole5` and `hole7`.

## Scope boundary

This review accepts exactly the following finite theorem:

> No connected graph \(G\) on 12 vertices satisfies
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G)\) while
> \(\overline G\) contains a hub-free induced \(C_9\).

Using the already proved connectedness of parameter-three counterexamples
and C-014, this excludes every induced \(C_9\) from a surviving
order-12 parameter-three counterexample complement.

It does **not**:

- certify the `hole5` or `hole7` branch;
- certify the complete \((n,k)=(12,3)\) slice;
- turn the original `running` CEGAR checkpoint into a terminal;
- claim that the 170 colorings exhaust all three-color assignments;
- establish a result at another order or guard parameter; or
- resolve the universal \(\gamma\)--\(\theta\) conjecture.

Within that boundary, the proof is complete and independently checkable.

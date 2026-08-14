# Adversarial review of Outcome Q

**Review date:** 2026-08-13

**Supplied archive:** `STC_JC_Convention_Closure_Outcome_Q_Final.zip`

**Archive SHA-256:**
`abb83eff03996b7b95520ace2491c233daa4a9634ef1a771d51dc703dbf97f14`

**Disposition:** **REJECT — DO NOT INCORPORATE OUTCOME Q AS STATED**

## Executive verdict

The narrow one-step root-zipper calculation is correct.  It proves a useful
local statement: a *tree-child* rooted presentation whose only cleanup
artifact is one root-created zipper has exactly the same complete open JC
image as the contracted ordinary edge.

The advertised convention-closure theorem does not follow.  Its definition
of strong cleanup tree-childness quantifies over the complete unrestricted
Brits-style cleanup-rooting fibre.  That fibre always contains a two-stage
zipper which is binary, acyclic, LSA-valid, and not tree-child, but which
exhaustively cleans to the original already-simple topology.  Therefore,
under the definitions printed in the package,

\[
S_{\rm TC}(\mathrm{clean})=\varnothing
\]

on the already-simple topology domain.  The class called the “full
Englander--Brits strongly tree-child class” is consequently empty, and the
main transfer theorem is vacuous.

This is not a defect in the verified Outcome P theorem.  Englander et al.
version 4 uses the already-simple full-topology convention, not the cleanup
convention attributed to it by Outcome Q.  Outcome P should remain frozen.

Four independently prompted adversarial reviews were used for the
load-bearing claims.  The algebra reviewer verified the local JC identity;
the structural reviewer independently proved the double-zipper obstruction;
the convention reviewer found the Englander/Holtgrefe scope errors; and the
software reviewer independently reproduced the missing-preimage failure and
fail-open release behavior.

## Claim-by-claim status

| Claim | Status | Audit conclusion |
|---|---|---|
| ZIP, outer checksums, inner manifest, and Git bundle are byte-consistent | **VERIFIED** | All stored hashes pass.  This is integrity of the supplied bytes only. |
| Forced form of one tree-child root zipper | **VERIFIED AFTER CORRECTION** | The proof must add that the two exposed children cannot already be adjacent: either orientation would give a nonreticulate endpoint a second parent. |
| One zipper is the only cleanup step for a tree-child input | **VERIFIED AFTER CORRECTION** | True once the preceding nonadjacency argument is included. |
| JC effective multiplier \(\kappa=uv[\lambda\alpha\beta+(1-\lambda)\gamma]\) | **VERIFIED** | Independently derived from both displayed trees and from the complete two-terminal transition tensor. |
| Strict analytic section onto every \(x\in(0,1)\) | **VERIFIED** | All six source parameters are strictly inside the open domain and \(\partial\kappa/\partial\gamma>0\). |
| Equality survives arbitrary common tensor contexts | **VERIFIED** | Equality holds before projectivization, for the complete two-boundary tensor. |
| Unqualified one-contraction formula \(\operatorname{sd}_0(D')=\operatorname{clean}(D)\) | **FALSE** | A non-tree-child input may expose another zipper after the first contraction.  Iteration is required. |
| `Root_clean` complete-fibre census in the package | **FALSE** | The census inserts roots into cleaned graphs and does not enumerate all rooted DAG preimages under exhaustive cleanup. |
| \(S_{\rm TC}(\mathrm{clean})\) is a nonempty strict subclass of \(S_{\rm TC}(0)\) | **FALSE AS INTENDED** | With the printed complete unrestricted fibre, its left side is empty. |
| Outcome Q transfers Outcome P to a full Englander--Brits strong class | **FALSE** | There is no such joint literature convention, and the newly defined cleanup-strong class is vacuous. |
| Outcome Q closes a Holtgrefe rooting-fibre gap | **CONVENTION-DEPENDENT / UNPROVED** | The package replaces Holtgrefe's broader rooting notion by a new binary one-root LSA-valid specialization without proving equivalence of the strong quantifiers. |
| Theta remains an exact weak-class JC ambiguity | **VERIFIED, BUT NOT A CLEANUP SHARPNESS RESULT** | The already-simple pair and its JC certificates survive.  Since cleanup-strong is empty, membership in `W_TC(clean) \ S_TC(clean)` no longer identifies a sharp boundary. |
| Clean-clone commands reproduce as supplied | **FALSE** | Quick verification fails on an undeclared `pdftotext`; regenerate-all is interpreter-build dependent. |
| Mutation suite independently certifies theorem completeness | **FALSE** | It mutates selected stored fields and never tests omitted cleanup preimages or nested zippers. |

## Decisive counterexample to the cleanup-rooting quantifier

### The rooted network

Take leaves \(L_1,L_2,L_3\) and arcs

\[
\begin{aligned}
r&\to P,&r&\to Q,&P&\to Q,&P&\to p,\\
Q&\to q,&p&\to q,&p&\to L_1,&q&\to t,\\
t&\to L_2,&t&\to L_3.
\end{aligned}
\]

The vertex types are

\[
P,p,t\text{ tree vertices},\qquad Q,q\text{ reticulations}.
\]

This is the result of inserting two nested root zippers above the ordinary
rooted three-leaf tree.

### Exact validation

1. **Binary and acyclic.**  The displayed bidegrees are exactly the binary
   rooted-network bidegrees.  A topological order is
   \(r,P,Q,p,q,t,L_1,L_2,L_3\), with the incomparable terms reordered as
   needed.
2. **LSA-valid.**  A path to \(L_1\) through \(r\to P\to p\) avoids
   \(Q,q\); paths to \(L_2,L_3\) through \(r\to Q\to q\) avoid \(P,p\).
   No old descendant can be stable because the contracted rooted tree is
   LSA-valid.  Thus only \(r\) lies on every root-to-leaf path.
3. **Level 2.**  The unique nontrivial top block has vertices
   \(\{r,P,Q,p,q\}\) and exactly the two reticulations \(Q,q\).
4. **Not tree-child.**  The reticulation \(Q\) has the reticulation child
   \(q\).

### Exact cleanup

After semi-deorientation:

1. suppressing \(r\) creates a second \(P\to Q\);
2. identify the two copies and suppress degree-two \(P,Q\), creating a
   second \(p\to q\);
3. identify those copies and suppress degree-two \(p,q\);
4. obtain the ordinary labelled three-leaf tree with edges
   \(tL_1,tL_2,tL_3\).

The independent checker
`independent/double_zipper_counterexample.py` reconstructs this chain from
the primitive DAG.  It imports no Outcome Q code.

### General obstruction

Let \(D_0\) be any already-simple rooted presentation with root children
\(a,b\).  Introduce fresh vertices \(P,Q,p,q\) and replace the old root by

\[
r\to P,quad r\to Q,quad P\to Q,quad P\to p,quad
Q\to q,quad p\to q,quad p\to a,quad q\to b.
\]

The same degree and LSA argument shows that this is a binary LSA-valid
cleanup rooting.  It is not tree-child because \(Q\to q\) is a reticulation
stack, and its exhaustive cleanup is exactly
\(\operatorname{sd}_0(D_0)\).  Hence every topology with an already-simple
rooting has a non-tree-child member of the complete unrestricted cleanup
fibre.

If one additionally bounds rooted presentations to level at most two, the
explicit three-leaf example remains valid and already refutes the advertised
identification of classes.  If one instead imposes the obsolete Englander-v1
ban on rooted 2-blobs, the zipper is excluded—but then the Brits cleanup
fibres that Outcome Q purports to add are excluded as well.

## Literature-convention audit

The source audit used the cited versions of
[Englander et al. v4](https://www.biorxiv.org/content/10.1101/2025.04.18.649493v4),
[Brits et al. v2](https://arxiv.org/abs/2607.12919v2),
[Holtgrefe et al. v2](https://arxiv.org/abs/2507.18772v2), and
[Sullivant v2](https://arxiv.org/abs/2507.23056v2).

### Englander et al. version 4

Outcome Q attributes the version-1 definitions to the cited version-4
paper.  In version 4:

- Definition 2.1 uses a binary DAG without parallel edges and an LSA root;
- Definition 2.2 deorients nonreticulation edges and suppresses the former
  root; parallel semi-directed outputs are disallowed;
- strong tree-childness quantifies over directed networks producing the
  graph under Definition 2.2;
- exhaustive degree-two, parallel-edge, and 2-blob cleanup occurs in the
  **induced-subnetwork** operation of Definition 2.4.

The rooted no-2-blob/no-nonleaf-1-blob restriction and full-topology cleanup
quoted by Outcome Q are from the 2025 version-1 draft, not the cited 2026
version 4.  Thus Outcome P's already-simple convention is the relevant one
for the current Englander theorem.

### Brits et al.

Brits et al. do use exhaustive cleanup after root suppression.  They do not,
however, define a class in which every cleanup preimage is tree-child.
Outcome Q's `S_TC(clean)` is a new definition.  Under its literal complete
fibre it is vacuous by the double zipper.

### Holtgrefe et al.

Holtgrefe rootings may be obtained at vertices or by subdividing edges or
arcs, and their framework does not impose the package's LSA restriction.
The equation `Root_0 = Root_H` is therefore not a cited theorem; it is at
best equality with a specially restricted sub-fibre.  That restriction
cannot be substituted into Holtgrefe's universal tree-child quantifier
without a separate proof.

### Additional source corrections

- “No arrowhead is lost” is literally false: the arrowhead at the deleted
  zipper reticulation is lost.  The valid statement is that no arrowhead
  *outside the deleted zipper* is lost.
- The Sullivant degree-two citation is misnumbered: ordinary subdivision is
  Proposition 4.5, not Proposition 4.6, in the cited version.
- Sullivant's directly relevant stacked-reticulation result is Theorem 5.1;
  it reinforces that the double zipper is an observationally hidden stacked
  structure rather than supplying a tree-child exclusion.
- The manuscript must define the model image of a cleaned topology.  Union,
  intersection, and “common image” over cleanup rootings are not equivalent
  by definition.

## Reproducibility and certificate audit

### What passed

- ZIP integrity test;
- outer `SHA256SUMS.txt`;
- inner `MANIFEST.sha256`;
- Git bundle verification and byte comparison with `release_tree`;
- the stored one-step JC identities;
- the two handcrafted `(1,1,L)` frontier implementations agree on their
  shared finite family.

### What failed or is fail-open

1. `bash reproducibility/verify_quick.sh` fails in the declared local
   environment because `verify_release.py` calls `pdftotext` but Poppler is
   absent from `environment.yml`.
2. With an audit-only PDF-text shim, quick and full verification pass, but
   regenerate-all fails because `dependency_audit.json` embeds the exact
   `sys.version` string and byte-compares it to Python 3.13.5.
3. None of the official wrappers verifies the release manifest or complete
   inventory before accepting the theorem.
4. The Python verifiers rely on `assert`.  With optimization enabled,
   theorem-critical checks disappear.
5. `verify_regenerate_all.sh` regenerates JSON only.  It does not rebuild the
   PDF, transcripts, metadata, manifests, component archives, or outer ZIP.
6. The mutation suite edits scalar fields in copies of frozen certificates;
   it does not mutate primitive graphs and regenerate cleanup fibres.
7. The “complete rooting” routine enumerates root insertions into an
   already-clean graph.  It does not enumerate all rooted DAGs whose
   exhaustive cleanup yields that graph.
8. The two structural implementations enumerate the same handcrafted
   `(1,1,L)` family and compare counts/profile multisets, not complete
   canonical graph records.
9. The bundled Git history does not contain the frozen Outcome P baseline
   commit; only the copied baseline PDF hash is checked.

The official scripts can therefore print `PASS` while the universal rooting
quantifier is false.

## Manuscript and PDF review

All 22 pages were rendered and inspected.  The PDF is readable and has no
observed clipping or overlapping text.  It is nevertheless not a
submission-ready integration:

- the title and body use process language (“Outcome Q,” “frozen baseline,”
  “Part II: the verified already-simple classification”);
- page 7 is almost entirely blank and visibly exposes that the convention
  note was placed in front of an unchanged manuscript;
- the document explicitly says the remainder is reproduced unchanged,
  contrary to the supplied integration directive;
- cross-references call lemmas “theorem 2.2” and “theorem 2.4”;
- the false class and source claims occur in the abstract, main theorem,
  corollary, convention table, and release metadata, so they cannot be fixed
  by an erratum sentence.

## Safe incorporation decision

Do **not** merge the Outcome Q manuscript, theorem statement, class notation,
metadata, certificates, or release wrappers into Outcome P.

The only material suitable for possible later reuse is:

1. the corrected one-step tree-child zipper lemma;
2. the exact JC two-boundary formula and strict section;
3. a narrowly labelled remark that this treats one Brits-style cleanup
   presentation, not a universal strong cleanup class.

The verified positive classification should continue to be stated under the
already-simple convention used by Englander et al. version 4.  A separate
Brits-cleanup extension would require a nonvacuous rooting notion—such as an
explicit minimal-presentation fibre—and a new theorem proving that this is
the intended standard object.  It cannot be obtained by editing Outcome Q's
current proof.

## Final disposition

\[
\boxed{\text{OUTCOME Q IS FALSE/VACUOUS AS STATED AND MUST NOT BE INCORPORATED.}}
\]

\[
\boxed{\text{THE VERIFIED OUTCOME P CLASSIFICATION IS UNAFFECTED.}}
\]

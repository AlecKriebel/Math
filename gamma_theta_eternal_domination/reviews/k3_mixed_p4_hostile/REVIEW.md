# Hostile review: the mixed three-color \(P_4\)

## Verdict

**ACCEPT.**

The analytic external-witness lemmas are correct in the standard
one-guard-moves model.  The displayed `FDzro` graph, parameters, induced
complement path, 21-state eternal family, and response lists all pass
independent literal checks.

During review, an important scope ambiguity was found and corrected:
the displayed 21-state family is a proper subfamily of the 33-state greatest
eternal three-family.  Its response lists realize the mixed \(P_4\), while
the greatest-family lists do not.  The final note and JSON now say this
explicitly, and the order-\(7\)-through-\(9\) observation is correctly
restricted to greatest families.

The finite census remains **OBSERVED** only.  It is not accepted here as a
certified exclusion, a statement about proper eternal subfamilies, or a
universal theorem.  No novelty claim is made in this review.

## Final reviewed bytes

| artifact | SHA-256 |
|---|---|
| `math/working/k3_mixed_p4_attack.md` | `3af645890638f07fa38b294def7967679e280a6447173aa320e8715da714d92c` |
| `results/k3_mixed_p4_probe.json` | `4120b9fee483f9e9e0ce866b409357d1691063cb7206c54b2fd0a8ed3cfd608b` |
| `math/working/k3_mixed_p4_probe.py` | `a7f0f367e38dc51436614048d107af139b68d2cefd2c170f6c6d06c0b7f0c31c` |
| `results/k3_mixed_p4_probe.log` | `9d5a1d7702710f3242b0f1a860a3fa18369295489b96008fc519067d48ed2b26` |
| pinned `nauty` `geng` | `588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1` |
| independent hostile probe | `0fc926a478a1dfab3a491bf622e5805835ea7531433179a474199b384c1b7679` |
| independent hostile result | `5a85858ac43a3445ee65c46e5a43cffc7d929a54bfbe9eed85d0b2671195a765` |

The independent evidence is in `probe.py` and `probe_result.json` in this
directory.  It uses both campaign evaluators for the seven-vertex graph and
verifier B's direct family checker.  It imports no response-list or theorem
helper from the mixed-\(P_4\) probe.

## 1. Exact model and setup

Let \(S=\{a,b,c\}\) be an independent state in an eternal family
\(\mathcal F\) of triples.  Let \(x_0x_1x_2x_3\) be an induced path in
\(H=\overline G\), with exact family-response lists

\[
L(x_0)=\{a\},\quad
L(x_1)=\{a,c\},\quad
L(x_2)=\{b,c\},\quad
L(x_3)=\{b\}.
\]

Every positive list membership supplies both:

1. the graph edge from the named guard to the attacked vertex; and
2. membership of the corresponding one-swap state in the same eternal
   family \(\mathcal F\).

The two Hall-tight complement edges \(x_0x_1\) and \(x_2x_3\) therefore
force

\[
\{b,x_0,x_1\},\qquad \{a,x_2,x_3\}\in\mathcal F
\]

by the already reviewed tight-Hall endpoint lemma.  The attacks are at
distinct unoccupied vertices, and the complement edges mean that the first
moved guard cannot answer the second attack.  This use is sound.

## 2. Lemma 1 re-derived

Assume additionally

\[
\gamma(G)=\alpha(G)=3.
\]

The pair \(\{x_1,x_2\}\) dominates all seven named vertices:

- \(x_1,x_2\) dominate themselves;
- \(a\) and \(c\) are adjacent to \(x_1\) by their positive list entries;
- \(b\) and \(c\) are adjacent to \(x_2\);
- \(x_0x_2\in E(G)\), because \(x_0,x_2\) are nonconsecutive on the
  induced path in \(\overline G\); and
- \(x_1x_3\in E(G)\) for the same reason.

Because \(\gamma(G)=3\), this pair does not dominate all of \(G\).  Hence
some vertex \(w\) lies outside both closed neighborhoods:

\[
w\notin N_G[x_1]\cup N_G[x_2].
\]

Every one of the seven named vertices was just shown to be dominated, so
\(w\) is external to the displayed seven.  The middle path edge
\(x_1x_2\in E(\overline G)\) says \(x_1x_2\notin E(G)\).  Therefore

\[
\{w,x_1,x_2\}
\]

is independent.  Its size is maximum because \(\alpha(G)=3\), and the
accepted independent-state forcing lemma puts it into every eternal family
of three-sets, including \(\mathcal F\).

No eternal move is silently inferred from static domination here.  The only
use of \(\gamma=3\) is the logically necessary production of a vertex missed
by the middle pair.

## 3. Lemma 2 re-derived

Put

\[
W=N_{\overline G}(x_1)\cap N_{\overline G}(x_2).
\]

Lemma 1 proves \(W\ne\varnothing\).  It also proves that every witness is
outside the seven named vertices.  This can be checked directly for the
other named vertices:

- \(a,b,c\) each has a positive \(G\)-edge to \(x_1\) or \(x_2\);
- \(x_0\) is adjacent in \(G\) to \(x_2\);
- \(x_3\) is adjacent in \(G\) to \(x_1\); and
- open complement neighborhoods exclude \(x_1,x_2\) themselves.

If distinct \(w,z\in W\) were nonadjacent in \(G\), then

\[
\{x_1,x_2,w,z\}
\]

would be an independent four-set, contradicting \(\alpha(G)=3\).
Therefore \(G[W]\) is a clique.

For each \(w\in W\), the triple

\[
T_w=\{w,x_1,x_2\}
\]

is maximum independent and hence belongs to \(\mathcal F\).  From \(T_w\),
an attack at \(z\in W-\{w\}\) is unoccupied.  Neither \(x_1\) nor \(x_2\)
is adjacent to \(z\), while \(wz\in E(G)\).  Thus exactly one guard can
move: \(w\to z\).  Its successor is the already forced family state \(T_z\).

The states \(T_w,T_z\) are independent and share the two-vertex ridge
\(\{x_1,x_2\}\).  They satisfy the hypotheses of the reviewed
ridge-covariance theorem, so transport by the transposition \((w\ z)\) is
valid.  The note does not overstate this as a graph automorphism or as a
global coloring.

## 4. Independent audit of `FDzro`

Decoding graph6 `FDzro` independently gives order \(7\), size \(13\), and
the exact edges

\[
\begin{split}
&03,04,05,\quad 14,15,16,\quad
23,24,25,26,\\
&35,36,46.
\end{split}
\]

Among vertices \(3,4,5,6\), the complement edges are exactly

\[
34,\ 45,\ 56,
\]

so the complement-induced core is the claimed \(P_4\).

The JSON contains 21 distinct triples.  Verifier B's literal checker
accepts them as an eternal family: all 21 states dominate, and every one of
the \(21(7-3)=84\) unoccupied state/attack pairs has a one-edge, one-guard
response into the displayed family.  The two Hall-tight states

\[
\{1,3,4\},\qquad \{0,5,6\}
\]

are present.

Relative to \(S=\{0,1,2\}\), direct recomputation inside this exact
21-state family gives

\[
L(3)=\{0\},\quad
L(4)=\{0,2\},\quad
L(5)=\{1,2\},\quad
L(6)=\{1\}.
\]

Thus the mixed \(P_4\) is genuinely realized in a fully closed eternal
family.

Both exact evaluators independently return

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\]

There are also short positive witnesses:

- \(\{0,4\}\) dominates, while exhaustive singleton checking proves
  \(\gamma=2\);
- \(\{0,1,2\}\) is independent, while exhaustive four-set checking proves
  \(\alpha=3\);
- the explicit family proves \(\gamma^\infty\le3\), and
  \(\alpha\le\gamma^\infty\) proves equality; and
- \(\{0,3,5\}\mid\{1,4,6\}\mid\{2\}\) is a three-clique partition, while
  \(\alpha\le\theta\) proves \(\theta=3\).

Therefore `FDzro` is not a conjecture counterexample: its decisive failure
is exactly \(\gamma=2<3\).

## 5. Proper-family boundary

The independent audit finds that the greatest eternal three-family of
`FDzro` has 33 states, and both evaluators agree on it.  The displayed
21-state family is a strict subfamily.

At the same reference state, the greatest-family lists are

\[
\begin{array}{c|c}
3&\{0,2\}\\
4&\{0,1,2\}\\
5&\{0,1,2\}\\
6&\{1,2\}.
\end{array}
\]

They do not realize the mixed \(P_4\).  The corrected note and JSON now
state both list tables, the family sizes, and the strict scope distinction.
The phrase “genuine closed one-guard eternal three-family” means fully
closed under every attack, not greatest.

This distinction does not weaken the analytic counterexample to the listed
mechanisms, because Lemmas 1 and 2 and the preceding transition lemmas are
formulated for an arbitrary eternal family.  It does limit the census:
searching only greatest families says nothing about a pattern that may occur
only in a proper eternal subfamily.

## 6. Local diagnostic

The lightweight 64-mask local calculation was rerun.  It reproduces:

- 36 masks after the inherited \(\alpha\le3\) and shared-vertex filters;
- four surviving masks \(46,47,62,63\); and
- the common named edges
  \(cx_0,bx_1,ax_2,cx_3\).

This rerun uses the author probe and is not independent certification.  The
note and JSON correctly label the result **OBSERVED**, warn that the models
need not extend to equality graphs, and do not use it in the proofs of
Lemmas 1 or 2.

## 7. Order-\(7\)-through-\(9\) census scope

The hostile reviewer did not rerun the 273,050-graph enumeration.  The
frozen command, source hash, generator hash, per-order counts, and literal
output are present and internally consistent.

More importantly, the epistemic labels and quantifiers are now exact:

- the note heading says **OBSERVED**;
- the JSON top-level `claim_status` is `OBSERVED`;
- the JSON warning says it is not a coverage certificate, a proper-family
  statement, or a universal exclusion;
- the probe source explicitly searches the greatest eternal three-family;
  and
- the final note says only that no **greatest-family** realization was
  observed through order nine.

The recorded counts

\[
\begin{array}{c|r|r|r}
n&\text{connected graphs}&
\gamma=\alpha=\gamma^\infty=3&\text{greatest-family realizations}\\ \hline
7&853&16&0\\
8&11\,117&140&0\\
9&261\,080&1\,380&0
\end{array}
\]

remain finite observational evidence only.  They are not promoted by this
review.

## 8. Exact accepted boundary

The accepted result is:

1. any equality realization of the mixed family-list \(P_4\) forces a
   nonempty external clique \(W\) of middle-pair witnesses;
2. every witness supplies a maximum independent family state
   \(\{w,x_1,x_2\}\);
3. attacks within \(W\) force the unique ridge exchanges and the reviewed
   response covariance; and
4. the transition ingredients available before using \(\gamma=3\) cannot
   alone eliminate the mixed \(P_4\), as the explicit proper family in
   `FDzro` demonstrates.

This materially sharpens the structural boundary at \(k=3\), but it neither
eliminates the mixed \(P_4\) in equality graphs nor proves the \(k=3\) slice.

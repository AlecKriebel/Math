# Global atlas/interface closure audit

## 1. Scope and outcome

This note audits the support-level interface left after the certified
two-active atlas. It is deliberately classwise and physical-time. It does
not change the atlas, discard reactions from a strongly connected linkage,
or assert that recurrence is monotone under adding reactions.

There are five conclusions.

1. The presently certified reductions do **not** collapse the global
   shielded/available interface to the two seams currently under focused
   study. After the tier test and the exact affine-class feasibility filter,
   2,169 positive-invariant ordered support pairs and 191 signed ordered
   support pairs remain.
2. The exact signed-service theorem closes two further displayed networks
   after three deficiency-zero overlaps, and the exact residual-pair theorem
   closes one more (all with their external \(A/B\) swaps).
   It closes zero of the 358 signed *shielded/available* pairs, because its
   pure-C linkage is itself shielded in those charts. Keeping those two
   strata separate prevents a misleading double count.
3. An exact finite tier-arrangement certificate closes 1,219 of the 3,531
   positive residual pairs and 159 of the 358 signed residual pairs. These
   are genuine physical-time conclusions: the certificate verifies the
   Anderson--Kim top-S descending condition for every tier sequence, every
   strongly connected orientation of both supports, and every positive rate
   vector.
4. As a transparent analytic subfamily of that certificate, for

   \[
      L_0=\{A,B,A+C,B+C\},
   \tag{1.1}
   \]

   12 of its 49 compatible available supports pass. All nine minimal partners
   remain open; explicit tier sequences show why the same one-step criterion
   cannot prove them.
5. Testing affine stoichiometric feasibility of every failed descriptor
   closes another 151 pairs classwise (143 positive and eight signed). A
   one-active physical-phase draft would remove many more, but its global
   lower-target/reactivation Foster step has not yet passed audit and is not
   counted here.

Thus this is a rigorous narrowing result, not a T3-2 theorem.

## 2. Exact enumeration convention

The complex universe is

\[
 \mathcal C_2=\{0,A,B,C,2A,2B,2C,A+B,A+C,B+C\}.
\tag{2.1}
\]

Use the four certified displayed workload representatives

\[
 (1,1,0),\quad(2,3,0),\quad(1,2,0),\quad(1,3,0).
\tag{2.2}
\]

An ordered chart instance is a triple \((h,S,T)\) such that

- \(S,T\subset\mathcal C_2\) are disjoint and each has at least two
  complexes;
- \(S\) is shielded for \(h\), and is either one of the 25 masks having an
  invariant with positive \(A,B\) coefficients or one of the four displayed
  signed masks;
- \(T\) is available for the same \(h\).

Orientations and parallel labelled reactions are not enumerated. Each
support is understood to carry an arbitrary strongly connected directed
graph with positive rates. Identical ordered pairs \((S,T)\) appearing in
several workload charts are counted once in the support table.

For two disjoint supports put

\[
 \delta(S,T)=|S|+|T|-2-
 \operatorname{rank}\operatorname{span}
 \{y-y':y,y'\in S\text{ or }y,y'\in T\}.
\tag{2.3}
\]

The branches below are disjoint only because they are applied in the stated
order.

| Branch | Exact support-level test | Justification |
|---|---:|---|
| finite class | common kernel contains \(q_A,q_B,q_C>0\) | every stoichiometric class is finite |
| common active invariant | common kernel contains \(q_A,q_B>0\), but no strictly positive vector was selected above | excludes two-active escape in the certified chart reduction |
| full deficiency zero | \(\delta(S,T)=0\) | weak reversibility gives the summable conditioned product-Poisson law |
| exact signed-service seam | unordered supports are in the exact lists (1.2)--(1.3) of `signed_service_seam_full_proof.md` | direct physical-time quadratic/service theorem; exact supports only |
| exact residual pair | unordered supports are \(\{B,2A,B+C\}\) and \(\{0,A,C\}\) | direct physical-time core-trace theorem; exact supports only |
| exact seven-support seam | \(T=\{C,A+C,B+C\}\) and \(S\) is in the exact seven-support list | direct physical-time theorem in certified_exact_shielded_seam.md |
| residual | none of the preceding tests | requires another analytic interface |

The preserved one-linkage theorem is also a valid classwise branch, but it
does not delete a support pair in this table. It applies after a linkage is
inactive on the fixed closed class, or after deletion of constant species
makes the projected linkages share a complex and hence merge. Whether that
happens is class data, not a property of the original disjoint supports.

## 3. Exact global branch table

The finite certificate gives:

| shielded family | chart instances | unique ordered pairs | finite | active-only invariant | full DZ | seven-support seam only | signed-service seam only | residual-pair only | residual before tier test | tier-certified | final residual |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| positive \(A,B\) invariant | 11,070 | 4,761 | 187 | 110 | 924 | 6 | 2 | 1 | 3,531 | 1,219 | 2,312 |
| signed one-active | 645 | 408 | 0 | 0 | 50 | 0 | 0 | 0 | 358 | 159 | 199 |

There are geometrically seven exact-seam pairs. The pair with
\(S=\{0,2C\}\) is already counted in the full-deficiency-zero column, so six
appear in the seam-only column.

The signed-service theorem has five disjoint displayed support pairs. Three
with pure support \(\{C,2C\}\) are already full deficiency zero. Its two new
pairs are

\[
 \{C,2C\}\ \&\ \{0,A,2A,B+C\},
 \qquad
 \{0,C,2C\}\ \&\ \{A,2A,B+C\},
\tag{3.1}
\]

plus their external \(A/B\) swaps. In a signed chart the pure-C linkage is
classified as shielded, not available. Therefore (3.1) removes zero of the
358 ordered pairs in the signed row; the same physical networks occur in the
positive-shielded row, where the pure-C linkage is listed first. This is a
classification fact, not a reaction-deletion argument.

The third exact closure is

\[
 \{B,2A,B+C\}\ \&\ \{0,A,C\},
\tag{3.2}
\]

proved for every strongly connected orientation and positive rate vector in
`residual_pair_full_proof.md`. It is one displayed positive-table pair and
has no signed-table occurrence. Like the two signed-service additions, it
fails the one-step tier test, so applying its physical-time theorem before
the tier certificate creates no overlap.

The residual fingerprints after all exact-support branches and before the
tier theorem are

\[
\begin{array}{c|c}
\text{positive-invariant}&
\mathtt{42d526cbdfc085a32e3bd7b9c13d07733e2cae883e976524fdb04fd4a370307e}\\
\text{signed}&
\mathtt{ffe1c05ad44e2053a0a4c2a7278319458c1b80f0fdb85915186f44d15478bc4f}.
\end{array}
\tag{3.3}
\]

After removing only the 12 pairs proved transparently in Section 6, the
intermediate positive residual fingerprint is

\[
 \mathtt{a4592d5bc285ebed6f5863f4c59a9c54c3189c261e84837665fcf5b28bede722}.
\tag{3.4}
\]

The exact all-pair tier test in Section 8 gives the final fingerprints

\[
\begin{array}{c|c|c}
&\text{tier-certified}&\text{remaining}\\ \hline
\text{positive-invariant}&
\mathtt{744d872920309c361d6d7f806f140a696e3fc3ae0f75d760d8a07f304d562b6b}&
\mathtt{0297ba35311c757cd5c6ec548d2af18410dfd37e791c7679de932fe4bf38695b}\\
\text{signed}&
\mathtt{7f59ea94fe876205ccb72dc97b026b2954feac62375122634aafa318084428ee}&
\mathtt{1a9c06123645855d3b4f23d4886b0ada3c3ff3614fc94a7d22c01f411c1355c8}.
\end{array}
\tag{3.5}
\]

The class-restricted feasibility theorem in
`stoichiometric_gate_feasibility.md` is applied next. It checks all 12,886
failed pair--descriptor incidences, not only the displayed greedy gate of a
pair. The ordered post-tier split is

\[
\begin{array}{c|rrr}
&\text{input}&\text{affine-impossible failures only}&\text{remaining}\\ \hline
\text{positive-invariant}&2312&143&2169\\
\text{signed}&199&8&191\\
\text{total}&2511&151&2360.
\end{array}
\tag{3.6}
\]

The remaining fingerprints after this additional certified branch are

\[
\begin{array}{c|c}
\text{positive-invariant}&
\mathtt{6763a44c9c312c440997a054f7966347d101e3236cdef9ecb90599226de10458}\\
\text{signed}&
\mathtt{f5c7a694bec0241a67b5cf588e1d074c11e00fb9ae3fbc1cee5570f84e9b4483}.
\end{array}
\tag{3.7}
\]

Here is the complete residual count by displayed shielded support before
Section 6.

| positive-invariant \(S\) | count | positive-invariant \(S\) | count |
|---|---:|---|---:|
| \(\{0,2C\}\) | 172 | \(\{0,A+C\}\) | 169 |
| \(\{0,B+C\}\) | 169 | \(\{0,C\}\) | 172 |
| \(\{2A,2B\}\) | 165 | \(\{2A,A+B\}\) | 165 |
| \(\{2A,B+C\}\) | 163 | \(\{2B,A+B\}\) | 165 |
| \(\{A,A+C\}\) | 189 | \(\{A,B\}\) | 143 |
| \(\{A,B+C\}\) | 165 | \(\{A+C,B+C\}\) | 180 |
| \(\{B,2A\}\) | 167 | \(\{B,A+C\}\) | 165 |
| \(\{B,B+C\}\) | 189 | \(\{C,2C\}\) | 171 |
| \(\{0,A+C,B+C\}\) | 98 | \(\{0,C,2C\}\) | 98 |
| \(\{2A,2B,A+B\}\) | 92 | \(\{A,A+C,B+C\}\) | 97 |
| \(\{A,B,A+C\}\) | 97 | \(\{A,B,B+C\}\) | 97 |
| \(\{B,2A,B+C\}\) | 97 | \(\{B,A+C,B+C\}\) | 97 |
| \(\{A,B,A+C,B+C\}\) | 49 |  |  |

For the four displayed signed supports the corresponding counts are

\[
\begin{array}{c|rrrr}
S&\{0,A,B+C\}&\{0,2A,B+C\}&\{A,2A,B+C\}&
\{0,A,2A,B+C\}\\ \hline
\#&101&101&100&56.
\end{array}
\tag{3.8}
\]

Exchange of \(A,B\) is an external symmetry. It reduces the 3,531 displayed
positive residual keys to 2,097 keys. Of the tier-certified keys, 757 remain
after quotienting by this exchange; the final positive residual consists of
1,340 orbit keys. The second family below has 35 supports modulo this
exchange, 23 of which remain after Section 6.

## 4. Why projection and enlargement do not finish the table

Species projection is valid only after a coordinate has been proved constant
on the fixed closed irreducible class. Tightness, bounded moments, or a
finite box carrying most mass do not justify deleting a species. Likewise,
two linkage classes merge only if their **projected** supports actually share
a complex. These correct classwise rules are already recorded in
classwise_scope_reduction.md; they are not a support-level reduction of the
generic pairs counted above.

Recurrence and Foster drift are not monotone under enlarging a linkage.
Deleting a reaction removes a signed generator term, which may be precisely
the destabilizing term that the desired estimate must control. The existing
exact regression is

\[
 \{B,2A,B+C\}\quad\&\quad\{0,A\}.
\tag{4.1}
\]

The full minimal network is deficiency zero. Adding \(C\) to the second
support gives \(\{0,A,C\}\), and for strongly connected directed cycles the
natural fast complex-balanced factorial potential has

\[
 \mathcal LF(n,n^2,0)=n^2\log2-O(n\log n)>0.
\tag{4.2}
\]

Equation (4.2) is not a transience example. It is an exact demonstration
that “prove a minimal subnetwork and then restore the deleted reactions” is
not a valid proof rule. Every superset must be included in the analytic
estimate itself.

## 5. Exact structure of the second deficiency-one family

Let \(S\) be (1.1). It is shielded only for \(h=(1,1,0)\) and preserves

\[
 N=A+B.
\tag{5.1}
\]

Its complement splits into

\[
 U=\{0,C,2C\},\qquad Q=\{2A,2B,A+B\}.
\tag{5.2}
\]

The compatible available supports are exactly

\[
 T=U'\cup Q',\qquad
 \varnothing\ne U'\subseteq U,\quad
 \varnothing\ne Q'\subseteq Q.
\tag{5.3}
\]

Hence there are \(7\cdot7=49\) supports. The nine inclusion-minimal ones are

\[
 \{u,q\},\qquad u\in\{0,C,2C\},\quad
 q\in\{2A,2B,A+B\}.
\tag{5.4}
\]

The reaction differences of \(S\) span

\[
 \operatorname{span}\{B-A,C\}.
\tag{5.5}
\]

Every \(T\) in (5.3) contains a difference \(q-u\) whose \(A+B\) coefficient
is two, so (5.5) together with \(q-u\) has rank three. Consequently

\[
 \delta(S,T)=|T|-1\ge1,
\tag{5.6}
\]

and the full network has no nonzero affine invariant. Thus none of the 49
pairs is a finite-class, common-invariant, full-deficiency-zero, projection,
or exact-seven-support-seam case in generic full-dimensional classes.

## 6. A 12-support physical-time Foster theorem

### Proposition 6.1

Let \(S\) be (1.1), with an arbitrary strongly connected orientation and
positive rates. Let \(T=U'\cup Q'\) satisfy (5.3), also with an arbitrary
strongly connected orientation and positive rates. Assume

\[
 \{2A,2B\}\subseteq Q',
 \qquad U'\cap\{C,2C\}\ne\varnothing.
\tag{6.1}
\]

Then the stochastic mass-action CTMC is positive recurrent on every closed
irreducible class. There are exactly 12 supports satisfying (6.1).

### Proof

We verify the sufficient tier condition in Theorem 4.2 of Anderson and Kim,
*Some network conditions for positive recurrence of stochastically modeled
reaction networks* (arXiv:1710.11263),

\[
 T^{S,1}_{\{x_n\}}\cap D_{\{x_n\}}\ne\varnothing
\tag{6.2}
\]

for every tier sequence. The physical-time Foster theorem for (6.2) uses
the proper entropy

\[
 V(x)=\sum_i\bigl[x_i(\log x_i-1)+1\bigr]
\tag{6.3}
\]

and yields \(\mathcal LV\le-1\) outside a finite set. No jump-chain time
change or inactive-coordinate truncation is involved.

Write

\[
 \bar a=a\vee1,\qquad \bar b=b\vee1,\qquad
 \bar c=c\vee1,\qquad M=\max(\bar a,\bar b).
\tag{6.4}
\]

The deterministic monomials of the two linkages are

\[
\begin{array}{c|cccc}
S&A&B&A+C&B+C\\ \hline
x^y&\bar a&\bar b&\bar a\bar c&\bar b\bar c
\end{array}
\tag{6.5}
\]

and

\[
\begin{array}{c|ccc|ccc}
T&0&C&2C&2A&2B&A+B\\ \hline
x^y&1&\bar c&\bar c^2&\bar a^2&\bar b^2&\bar a\bar b,
\end{array}
\tag{6.6}
\]

with only the selected columns retained.

We first record a graph fact. Let \(\mathcal T\) be the global top D-tier.
If, for one strongly connected linkage \(\mathcal L\),

\[
 \varnothing\ne\mathcal T\cap\mathcal L\subsetneq\mathcal L
\tag{6.7}
\]

and every complex in \(\mathcal T\cap\mathcal L\) is enabled eventually,
then a directed path from the top set to its complement has a first exiting
edge \(y\to z\). Its source is enabled and in the global top D-tier, hence
is in the top S-tier; its target is in a lower D-tier. This edge proves
(6.2).

Let \(\mathcal T_1=\mathcal T\cap T\). Every member of \(\mathcal T_1\) is
enabled eventually. Indeed, a top-tier monomial diverges. If \(2A\) or
\(2B\) is top, its population tends to infinity. If \(A+B\) is top but one
of \(A,B\) is absent, the square of the other coordinate, present by (6.1),
strictly dominates it. If \(C\) or \(2C\) is top, then \(c\to\infty\).
The zero complex cannot be globally top along an escaping sequence. Thus,
if \(\mathcal T_1\) is nonempty and proper, (6.7) proves the claim.

Suppose next that \(\mathcal T_1=\varnothing\). The top D-tier lies in
\(S\). Its members are enabled: a disabled \(A+C\), for example, has either
\(a=0\) or \(c=0\). If \(a=0\) and its monomial diverges through \(c\), the
selected \(C\) or \(2C\) complex is at least as large and belongs to
\(\mathcal T_1\). If \(c=0\) and it diverges through \(a\), \(2A\) strictly
dominates it and belongs to \(\mathcal T_1\). The other cases are symmetric.
Moreover, not all four complexes of \(S\) can be top: that would force
\(\bar a\asymp\bar b\to\infty\) and \(\bar c\asymp1\), while \(2A,2B\) have
order \(M^2\) and strictly dominate the order-\(M\) monomials in \(S\).
Thus (6.7) applies to \(S\).

It remains to exclude or handle \(\mathcal T_1=T\). Since \(2A,2B\) are
both top,

\[
 \bar a\asymp\bar b=M\longrightarrow\infty.
\tag{6.8}
\]

If \(0\in U'\), its constant monomial cannot be in the same diverging tier.
If both \(C,2C\in U'\), their equivalence would force
\(\bar c\asymp1\), again contradicting their membership in the diverging
top tier. Hence the only remaining possibilities are \(U'=\{C\}\) and
\(U'=\{2C\}\). In the first, top-tier equivalence gives
\(\bar c\asymp M^2\), but then \(A+C,B+C\) have order \(M^3\), contradicting
global maximality of \(T\). In the second,
\(\bar c^2\asymp M^2\), so \(\bar c\asymp M\). The two enabled complexes
\(A+C,B+C\) are then globally top, while \(A,B\) are lower. Condition
(6.7) applies to \(S\).

This proves (6.2) in every case. Population-increasing reactions have at
most linear rates: every quadratic-source reaction has product molecularity
at most two. Hence the process is nonexplosive, and the physical-time
Foster conclusion applies. Finally, there are two choices of nonempty
\(Q'\) containing \(2A,2B\), and six choices of nonempty \(U'\ne\{0\}\),
giving \(2\cdot6=12\) supports. \(\square\)

This proof includes the six ordinary double-full/path supports, but it is
strictly wider: it also includes \(U'=\{C\}\), \(U'=\{2C\}\), and their
allowed supersets without requiring a separate double-full invocation.

## 7. Exact obstruction for all nine minimal partners

Proposition 6.1 contains no minimal support from (5.4). This is not merely a
failure to optimize its proof. For each minimal support there is a strongly
connected orientation and a tier sequence on which no descending reaction
has a source in the top S-tier.

Use a directed four-cycle for \(S\) and the forced reversible two-vertex
graph for \(T\).

| minimal \(T\) | state sequence | four-cycle for \(S\) | obstruction |
|---|---|---|---|
| \(\{0,q\}\), any \(q\in Q\) | \((A,B,C)=(0,0,n)\) | \(A\to A+C\to B\to B+C\to A\) | \(A+C,B+C\) are top D-tier but disabled; \(0\) is the only enabled \(T\)-source and is lower D-tier |
| \(\{C,q\}\) or \(\{2C,q\}\), \(q=2A\) or \(A+B\) | \((0,n,0)\) | \(B\to B+C\to A\to A+C\to B\) | \(B,B+C\) are top D-tier; the enabled edge \(B\to B+C\) is flat, while the descending source \(B+C\) is disabled |
| \(\{C,2B\}\) or \(\{2C,2B\}\) | \((n,0,0)\) | \(A\to A+C\to B\to B+C\to A\) | symmetric to the preceding row |

The two reactions of \(T\) are disabled in the last two rows. In the first
row \(0\to q\) is enabled but is not sourced in the global top D-tier. Thus
condition (6.2) fails exactly.

These are counterexamples to the one-step tier proof, not to positive
recurrence. A successful theorem for the nine minimal pairs must cross the
disabled-source face: for example, it must include the \(0\to q\) activation
in the first row, or the flat \(B\to B+C\) activation in the second, and then
charge the complete subsequent same-linkage busy period without conditioning
away its source probability.

## 8. Exact all-pair tier-arrangement certificate

This section applies the same physical-time theorem as Proposition 6.1 to
**every** residual pair in Section 3. The finite part is exact rather than a
grid search.

### 8.1 Completeness of the finite tier descriptors

For a tier sequence \(x_n\), put

\[
 u_n=\bigl(\log(x_{n,A}\vee1),\log(x_{n,B}\vee1),
             \log(x_{n,C}\vee1)\bigr).
\tag{8.1}
\]

The D-order of two complexes \(y,y'\) is the asymptotic order of
\((y-y')\mathbin\cdot u_n\). Here is a direct compression lemma. Let \(F\)
be the span of

- every difference \(y-y'\) for which \(y\) and \(y'\) are D-equivalent;
  and
- every coordinate vector \(e_i\) for which \(x_{n,i}\) stays bounded.

For every generator \(f\) of \(F\), the scalar \(f\mathbin\cdot u_n\) is
bounded. Therefore the orthogonal projection \(P_Fu_n\) is bounded. Put

\[
 v_n=(I-P_F)u_n.
\tag{8.2}
\]

If \(d=y-y'\) is a strict D-comparison with \(y\) above \(y'\), then

\[
 d\mathbin\cdot v_n=d\mathbin\cdot u_n+O(1)\longrightarrow+\infty.
\tag{8.3}
\]

Equivalent differences annihilate \(v_n\); a bounded coordinate of \(v_n\)
is exactly zero; and an unbounded coordinate tends to \(+\infty\), since the
subtracted projection is bounded. Hence, for all large \(n\), \(v_n\) lies
in the nonempty relatively open rational polyhedral cone defined by

\[
 d\mathbin\cdot v>0\ \text{for every strict comparison},\qquad
 e\mathbin\cdot v=0\ \text{for every equivalence},
\tag{8.4}
\]

with \(v_i>0\) exactly on the unbounded coordinates and \(v_i=0\) on the
bounded ones. A nonempty relatively open rational cone contains a rational
point \(w\); after scaling, \(w\) is a primitive nonnegative integer vector.

Equivalently, successively normalize the unbounded residuals in (8.2). This
gives a finite lexicographic flag \(w^{(1)},\ldots,w^{(r)}\), with \(r\le3\),
whose first nonzero scalar product gives each strict comparison. Because the
comparison set is finite, one may choose
\(1\gg\epsilon_2\gg\epsilon_3>0\) so that

\[
 w=w^{(1)}+\epsilon_2w^{(2)}+\epsilon_3w^{(3)}
\tag{8.5}
\]

preserves every first-nonzero sign. The projection argument proves that the
perturbation can be selected in the same nonnegative cone and that

\[
 w_i>0\quad\Longleftrightarrow\quad x_{n,i}\longrightarrow\infty.
\tag{8.6}
\]

Thus every D-preorder is represented by one ordinary rational weight vector;
no polynomial relation between the three population scales is assumed.

There are 21 projectively distinct comparison planes

\[
 (y-y')\mathbin\cdot w=0,
 \qquad y,y'\in\mathcal C_2,
\tag{8.7}
\]

on the normalized simplex \(w_A+w_B+w_C=1\), \(w_i\ge0\). Together with
the three coordinate faces, their rational arrangement has 37 vertices.
Every zero-dimensional cell is a vertex; every open one-dimensional cell
contains the midpoint of its two endpoint vertices; and every
two-dimensional cell contains the centroid of three noncollinear vertices
of its closure. Deduplicating all vertices, pair midpoints, and triple
centroids gives 5,128 exact rational sample points and 193 distinct
\((\text{D-preorder},\text{active-coordinate set})\) types.

An integer coordinate of a tier sequence that has a finite limit is
eventually constant. Since all complexes have coordinate at most two, its
effect on source availability is recorded exactly by the cap

\[
 c_i=0,\quad1,\quad\text{or }2\;(\text{meaning at least }2).
\tag{8.8}
\]

For an enabled complex,
\(x_n^{\underline y}/(x_n\vee1)^y\) tends to a finite positive constant;
for a disabled complex it is zero. Consequently the top S-tier is exactly
the enabled part of the highest D-tier containing an enabled network
complex. Adding the caps (8.8) to the 193 types gives precisely 259 tier
descriptors. This proves that the finite list covers arbitrary multiscale
tier sequences and all boundary faces.

### 8.2 Exact arbitrary-orientation test

Fix one descriptor and one ordered support pair \(P=(S,T)\). Let \(G\) be
the global top D-tier restricted to \(S\cup T\), and let \(E\) be its global
top S-tier. For a linkage support \(L\in\{S,T\}\), write \(K_L=L\cap G\).
Then every strongly connected directed graph on both supports has a
descending reaction sourced in \(E\) if and only if

\[
 \boxed{\quad
 \text{for some }L\in\{S,T\},\qquad
 \varnothing\ne K_L\subsetneq L
 \quad\text{and}\quad K_L\subseteq E.
 \quad}
\tag{8.9}
\]

For sufficiency, take a directed path in \(L\) from \(K_L\) to its
complement. The first exiting edge has source in \(K_L\subseteq E\) and
target below the global top D-tier. For necessity, suppose (8.9) fails. If
\(K_L\) is nonempty and proper, select a vertex of \(K_L\setminus E\) and
arrange a directed Hamiltonian cycle on \(L\) so that this vertex is the
unique source of an edge leaving \(K_L\). If \(K_L\) is empty or all of
\(L\), that linkage has no descending edge. Doing this independently in the
two linkages produces a strongly connected orientation with no descending
source in \(E\). Thus (8.9) is also necessary for certification uniformly
over orientations.

This converse is useful for interpreting failures. Every listed descriptor
is realized by the explicit integer tier sequence

\[
 x_{n,i}=\lceil e^{n w_i}\rceil\quad(w_i>0),
 \qquad x_{n,i}=c_i\quad(w_i=0).
\tag{8.10}
\]

Hence a failed descriptor is a genuine counterexample to the *universal
one-step tier criterion*, not a numerical artifact.

### 8.3 Physical-time implication

Theorem 4.2 of Anderson--Kim states that if every tier sequence has a
descending reaction whose source lies in the global top S-tier, then, for
every positive rate vector, the stochastic mass-action CTMC satisfies

\[
 \mathcal LV(x)\le-1
 \quad\text{outside a finite set},
 \qquad
 V(x)=\sum_i[x_i(\log x_i-1)+1].
\tag{8.11}
\]

It follows that every state in a closed irreducible component is positive
recurrent and the expected time to enter the union of closed components is
finite. This is a generator theorem in physical time. It makes no finite-box
replacement, trace-duration estimate, or embedded-jump-chain claim.

Sections 8.1--8.2 show that a pair passing all 259 descriptors satisfies the
hypothesis of that theorem for every strongly connected orientation. The
CTMC is nonexplosive as well: a reaction that increases total population has
source molecularity at most one, hence the total increasing rate is bounded
above by an affine function of total population.

### 8.4 Exact branch counts

The positive-invariant residual splits by shielded support as follows.

| shielded \(S\) | input | tier-certified | remaining |
|---|---:|---:|---:|
| \(\{0,2C\}\) | 172 | 65 | 107 |
| \(\{0,A+C\}\) | 169 | 51 | 118 |
| \(\{0,B+C\}\) | 169 | 51 | 118 |
| \(\{0,C\}\) | 172 | 52 | 120 |
| \(\{2A,2B\}\) | 165 | 60 | 105 |
| \(\{2A,A+B\}\) | 165 | 60 | 105 |
| \(\{2A,B+C\}\) | 163 | 56 | 107 |
| \(\{2B,A+B\}\) | 165 | 60 | 105 |
| \(\{A,A+C\}\) | 189 | 42 | 147 |
| \(\{A,B\}\) | 143 | 82 | 61 |
| \(\{A,B+C\}\) | 165 | 72 | 93 |
| \(\{A+C,B+C\}\) | 180 | 44 | 136 |
| \(\{B,2A\}\) | 167 | 88 | 79 |
| \(\{B,A+C\}\) | 165 | 72 | 93 |
| \(\{B,B+C\}\) | 189 | 42 | 147 |
| \(\{C,2C\}\) | 171 | 65 | 106 |
| \(\{0,A+C,B+C\}\) | 98 | 39 | 59 |
| \(\{0,C,2C\}\) | 98 | 36 | 62 |
| \(\{2A,2B,A+B\}\) | 92 | 0 | 92 |
| \(\{A,A+C,B+C\}\) | 97 | 30 | 67 |
| \(\{A,B,A+C\}\) | 97 | 36 | 61 |
| \(\{A,B,B+C\}\) | 97 | 36 | 61 |
| \(\{B,2A,B+C\}\) | 97 | 38 | 59 |
| \(\{B,A+C,B+C\}\) | 97 | 30 | 67 |
| \(\{A,B,A+C,B+C\}\) | 49 | 12 | 37 |
| **total** | **3,531** | **1,219** | **2,312** |

For comparison with the earlier intermediate count: before either the
12-support Proposition 6.1 or the two signed-service closures, the positive
residual had 3,534 pairs. The universal tier condition passes 1,219 of them,
including exactly the 12 in Proposition 6.1, and fails 2,315. Thus on the
previously quoted post-Proposition set of 3,522 pairs, the all-pair tier test
adds 1,207 closures and leaves 2,315. The two exact signed-service pairs and
the exact residual pair are tier failures, so applying those independent
theorems gives the final 2,312 in the table. No pair is counted twice.

The signed supports were checked separately; no conclusion is inferred from
a signed \(B-C\) descent or from properness on a projected coordinate.

| signed shielded \(S\) | input | tier-certified | remaining |
|---|---:|---:|---:|
| \(\{0,A,B+C\}\) | 101 | 42 | 59 |
| \(\{0,2A,B+C\}\) | 101 | 46 | 55 |
| \(\{A,2A,B+C\}\) | 100 | 46 | 54 |
| \(\{0,A,2A,B+C\}\) | 56 | 25 | 31 |
| **total** | **358** | **159** | **199** |

The exact signed-service theorem is deliberately **not** extended to
supersets. Of the 199 remaining signed pairs, 38 have an available support
strictly containing \(\{C,2C\}\); five of those also contain \(0\). The
other 161 do not contain \(\{C,2C\}\) at all. For each fixed signed shield,
the 38 theorem-adjacent pairs are precisely supersets of the following ten
inclusion-minimal pairs:

| signed shielded \(S\) | inclusion-minimal available \(T\supset\{C,2C\}\) |
|---|---|
| \(\{0,2A,B+C\}\) | \(\{A,C,2C\}\), \(\{C,2C,A+B\}\), \(\{C,2C,A+C\}\) |
| \(\{0,A,B+C\}\) | \(\{2A,C,2C\}\), \(\{C,2C,A+B\}\), \(\{C,2C,A+C\}\) |
| \(\{A,2A,B+C\}\) | \(\{C,2C,A+B\}\), \(\{C,2C,A+C\}\) |
| \(\{0,A,2A,B+C\}\) | \(\{C,2C,A+B\}\), \(\{C,2C,A+C\}\) |

Equivalently, this is a four-pattern canonical cover: add \(A+B\) or
\(A+C\) to the pure-C support for any compatible signed shield, add \(A\)
for \(S=\{0,2A,B+C\}\), or add \(2A\) for
\(S=\{0,A,B+C\}\), and then allow further complexes. This is only an exact
set-theoretic description of what remains. Adding even one complex changes
the generator, so the signed-service proof supplies no recurrence conclusion
for these 38 supersets.

The 1,219 positive passes form 757 keys modulo \(A\leftrightarrow B\). The
2,312 positive failures form 1,340 such keys. Proposition 6.1 is recovered
exactly: its 12 supports pass and the other 37 fail.

### 8.5 Canonical obstruction cover

The 2,312 positive failures admit a deterministic greedy cover by 17
displayed tier descriptors, reducing to the following 12 after
\(A\leftrightarrow B\). Each row includes its exchanged version.

| canonical log weight \(w\) | bounded-coordinate caps \(c\) |
|---|---|
| \((0,0,1)\) | \((0,0,2)\) |
| \((0,1,0)\) | \((0,2,0)\) |
| \((0,1,1)\) | \((0,2,2)\) |
| \((1,1,0)\) | \((2,2,0)\) |
| \((1,1,1)\) | \((2,2,2)\) |
| \((1,1,2)\) | \((2,2,2)\) |
| \((1,2,0)\) | \((2,2,0)\) |
| \((1,2,1)\) | \((2,2,2)\) |
| \((1,2,3)\) | \((2,2,2)\) |
| \((1,3,2)\) | \((2,2,2)\) |
| \((2,2,1)\) | \((2,2,2)\) |
| \((2,3,1)\) | \((2,2,2)\) |

Here a cap in a positive-weight coordinate is only a harmless placeholder;
only zero-weight coordinates use (8.8). The 199 signed failures are covered
by four descriptors:

\[
\begin{array}{c|c|c}
w&c&\text{new failures in greedy order}\\ \hline
(0,0,1)&(0,0,2)&118\\
(0,1,0)&(0,2,0)&77\\
(1,0,1)&(2,0,2)&2\\
(1,1,0)&(2,2,0)&2.
\end{array}
\tag{8.12}
\]

For any failed pair, Section 8.2 constructs a strongly connected orientation
on the corresponding descriptor that violates the Anderson--Kim hypothesis.
The cover therefore reduces the obstruction geometry to a finite boundary
and multiscale library. It does **not** prove that any of these CTMCs is
transient or null recurrent.

### 8.6 Canonical analytic gate table

The preceding greedy list is a cover, not a partition. To make its analytic
content explicit, quotient the union of the positive and signed failures by
the external exchange \(A\leftrightarrow B\). For a row below, intersect the
displayed tier menu with the actual network support; the first nonempty block
is the set of possible top enabled sources. Write P when a linkage has a
nonempty proper global-top subset but the universal test fails only because
an exit source can be disabled. Write F when each linkage's global-top
subset is empty or the whole linkage. The counts are canonical pair-orbit
incidences and overlap between rows.

| gate | \((w;c)\) | enabled source tiers, high to low | P/F incidences | one minimum P pair | one minimum F pair |
|---|---|---|---:|---|---|
| G1 | \((001;002)\) | \(2C>C>0\) | 608/45 | \(\{0,2B,AC\}\,\&\,\{A,AB\}\) | \(\{2A,2B\}\,\&\,\{0,A,AB\}\) |
| G2 | \((010;020)\) | \(2B>B>0\) | 950/76 | \(\{0,2A,BC\}\,\&\,\{B,AB\}\) | \(\{0,2C\}\,\&\,\{A,2A,AC\}\) |
| G3 | \((011;022)\) | \(\{2B,2C,BC\}>\{B,C\}>0\) | 30/7 | \(\{0,B,AC\}\,\&\,\{A,AB\}\) | \(\{0,AC\}\,\&\,\{2B,2C,BC\}\) |
| G4 | \((110;220)\) | \(\{2A,2B,AB\}>\{A,B\}>0\) | 47/159 | \(\{0,2C\}\,\&\,\{A,C,AC\}\) | \(\{2A,2B\}\,\&\,\{0,A,B\}\) |
| G5 | \((111;222)\) | binary \(>\) unary \(>0\) | 0/26 | -- | \(\{0,C\}\,\&\,\{2A,2C,AC\}\) |
| G6 | \((112;222)\) | \(2C>\{AC,BC\}>\{C,2A,2B,AB\}>\{A,B\}>0\) | 0/54 | -- | \(\{2A,2B\}\,\&\,\{0,A,B\}\) |
| G7 | \((120;220)\) | \(2B>AB>\{B,2A\}>A>0\) | 139/41 | \(\{0,2A,BC\}\,\&\,\{C,AC\}\) | \(\{B,BC\}\,\&\,\{0,2C,AC\}\) |
| G8 | \((121;222)\) | \(2B>\{AB,BC\}>\{B,2A,2C,AC\}>\{A,C\}>0\) | 0/3 | -- | \(\{0,C\}\,\&\,\{2A,2C,AC\}\) |
| G9 | \((123;222)\) | \(2C>BC>\{2B,AC\}>\{C,AB\}>\{B,2A\}>A>0\) | 0/23 | -- | \(\{2B,AC\}\,\&\,\{0,A,2A\}\) |
| G10 | \((132;222)\) | \(2B>BC>\{2C,AB\}>\{B,AC\}>\{C,2A\}>A>0\) | 0/2 | -- | \(\{B,AC\}\,\&\,\{0,A,2A\}\) |
| G11 | \((221;222)\) | \(\{2A,2B,AB\}>\{AC,BC\}>\{A,B,2C\}>C>0\) | 0/165 | -- | \(\{2A,2B\}\,\&\,\{0,A,B\}\) |
| G12 | \((231;222)\) | \(2B>AB>\{2A,BC\}>\{B,AC\}>\{A,2C\}>C>0\) | 0/23 | -- | \(\{2A,BC\}\,\&\,\{0,A,2C,AC\}\) |

The three exact physical-time pairs removed before the table--the two new
signed-service pairs (3.1) and the residual pair (3.2)--all first fail at
G2. This does not remove G2: it still covers many strict supersets and
different linkages. Every all-active gate G5--G6 and G8--G12 is necessarily
of type F, because every network complex is enabled. In contrast every gate
with a bounded zero coordinate has both a disabled-source and a flat
mechanism. These facts are checked rather than inferred from the greedy
order.

### 8.7 What can be proved uniformly on a one-active face

Before using any physical episode, the affine-feasibility theorem removes
every failed descriptor that is impossible inside a fixed stoichiometric
class. Its level-by-level Gordan alternative and exact certificate are in
*research_notes/stoichiometric_gate_feasibility.md*. Across the complete
descriptor list it closes 143 positive and eight signed pairs. The 67
flat-axis pairs below are a transparent subfamily of those 151, not an
additional branch.

The remaining one-active rows admit one useful but incomplete physical-time
lemma. State the structural results for \(B\to\infty\); permutation gives
the \(A\)- and \(C\)-axis versions. Let

\[
 \mathcal T_1=\{B,A+B,B+C\},\qquad
 \mathcal T_0=\mathcal C_2\setminus(\{2B\}\cup\mathcal T_1).
\tag{8.13}
\]

If \(2B\) occurs in the network, it is enabled and is the unique top
D-complex. Its strongly connected linkage has a reaction from \(2B\) to a
strictly lower tier, sourced in the top S-tier. Consequently **no failed
one-active descriptor contains \(2B\)**. Once \(2B\) is absent, removing the
common \(B\) from \(\mathcal T_1\) identifies every \(B\)-flat top reaction
with an immigration, conversion, or death reaction on

\[
 \{0,A,C\}.
\tag{8.14}
\]

#### Proposition 8.2 (flat-axis invariant closure)

Suppose a one-active failed descriptor is of type F. Then every linkage lies
wholly in \(\mathcal T_1\) or wholly in \(\mathcal T_0\). Hence every
reaction preserves \(B\) exactly. If every failed descriptor of a support
pair is of this form, then on each fixed stoichiometric class those failed
sequences are impossible; all remaining divergent sequences satisfy the
Anderson--Kim hypothesis. The physical-time Foster conclusion of Section
8.3 therefore applies classwise.

Indeed, for a linkage \(L\), type F says
\(L\cap\mathcal T_1=\varnothing\) or \(L\subset\mathcal T_1\). The
\(B\)-coefficient is respectively zero or one on all of \(L\), so every
reaction vector in \(L\) has zero \(B\)-coordinate. This is an exact
invariant, not a tightness or truncation assertion. The finite certificate
finds **67** positive-invariant support pairs and **zero** signed pairs whose
only tier failures are excluded this way. They are all contained in the
151-pair affine-feasibility branch. Their fingerprint is

\[
 \mathtt{f353c0306e3a629c2828ebbc3a4d9d0a5f5e39967729eac3ce12c6cbff9ed596}.
\tag{8.15}
\]

#### Lemma 8.3 (unconditioned actual-top-target clearance)

Fix a linkage \(L\) and put \(K=L\cap\mathcal T_1\). Assume
\(\varnothing\ne K\subsetneq L\), give \(L\) an arbitrary strongly connected
orientation and positive rates, and start at an **actual physical target**
\(t\in K\) with \(B=n\). Stop successfully at the first reaction from a
\(B\)-source to a \(B\)-free target; stop as an interference at the first
reaction with \(B\)-free source. There are network-dependent constants
\(C_0,C_1<\infty\) such that, with \(N=A+C\) at the start,

\[
 \Pr\{\text{interference before service}\}
 \le {C_0(1+N)^2\over n},
 \qquad
 \mathbb E\tau\le {C_1\over n}.
\tag{8.16}
\]

On success, all preceding carrier reactions preserve \(B\) and the last
reaction lowers it by one. No inactive-coordinate box is used.

To prove the lemma, retain the actual target label. At label \(p\in K\),
all outgoing channels with source \(p\) have a common mass-action factor.
Their relative probabilities are therefore fixed rate ratios. A top
reaction with another source cannot remove the last cofactor required by
\(p\): for \(A+B\) the only \(B\)-source that consumes \(A\) is the uniquely
owned complex \(A+B\), and similarly for \(B+C\); the unary source \(B\)
needs no cofactor. Thus unrelated top reactions may be skipped without
invalidating the carried source.

Strong connectivity of \(L\) implies that the finite sub-Markov chain on
\(K\) is absorbed in \(L\setminus K\): otherwise a terminal strongly
connected component of the retained graph would be closed in \(L\). On the
\(B\)-clock

\[
 s=\int_0^t B(u)\,du,
\tag{8.17}
\]

each carried source has total rate at least the smallest positive channel
rate, because its actual target guarantees any required cofactor. Hence the
carrier absorption time \(\sigma\) has an exponential tail.

Before service or interference, every skipped top reaction factors as
(8.14). It is an open unimolecular process: conversions preserve \(N\),
deaths lower it, and immigration has bounded total \(s\)-rate. It can be
coupled below

\[
 N(s)\le N(0)+\operatorname{Pois}(\Lambda s).
\tag{8.18}
\]

The exponential tail of \(\sigma\) consequently gives

\[
 \mathbb E\int_0^\sigma(1+N(s))^2\,ds
 \le C(1+N(0))^2.
\tag{8.19}
\]

Every \(B\)-free propensity is bounded by \(C'(1+N)^2\). Dividing its
compensator by the \(B\)-clock factor \(n\) and using (8.19) proves the
probability bound in (8.16); the duration bound is
\(\mathbb E\sigma/n\). Notice that this argument counts every lower-layer
reaction through its full compensator and every environment tail through
(8.18). It neither freezes a finite phase nor counts skipped top jumps.

The lemma is not yet a recurrence proof for type P. A \(B\)-free
interference can consume the last carried \(A\) or \(C\) while leaving \(B\)
unchanged. The old positive debt then remains, but the new actual target is
lower and (8.16) cannot simply be restarted. What is still required is an
unconditioned wait/reactivation alternative proving that this lower target
either reaches another service carrier in finite mean, promotes an inactive
coordinate to a higher-dimensional gate, or enters a genuinely closed
unimolecular class with a valid classwise invariant. Product-Poisson tails
for a closed fast class do not by themselves prove this intertrial statement.

The exact size of this candidate seam is machine checked. Among the 2,312
positive failures, 2,087 have some one-active obstruction and 1,081 have
only one-active obstructions. Removing Proposition 8.2 leaves 1,014 pairs
whose only obstruction is one-active promotion. For the signed row the
corresponding counts are 195, 151, and 151. By displayed active axis, the
positive \((A,B,C)\) obstruction counts are \((822,908,881)\), split into
\((746/76,832/76,811/70)\) promotion/flat; the signed counts are
\((0,116,118)\), all promotion. These are overlapping descriptor incidences,
not a partition of support pairs.

The stricter zero-cap selector--all failed descriptors belonging to
\((100;200),(010;020),(001;002)\)--contains 596 positive and 151 signed
pairs. It is disjoint from the affine-feasibility branch. If a complete
stopped-skeleton theorem for Lemma 8.3 were proved, the ordered arithmetic
would be \(2511-151-747=1613\). This is currently **selector arithmetic, not
a recurrence conclusion**: the available draft does not yet give a uniform
old-debt service probability after arbitrary lower theft, the total
unresolved-arrival bound per return attempt, or an integrated promotion
endpoint/elapsed-time Foster inequality.

## 9. Remaining interface

Of the 49 supports in (5.3), 37 remain after Proposition 6.1 and the exact
global tier test gives the same split. Equivalently, they are the supports
for which

\[
 \{2A,2B\}\not\subseteq Q'
 \quad\text{or}\quad U'=\{0\}.
\tag{9.1}
\]

They form 23 classes modulo \(A\leftrightarrow B\), including all six
minimal classes modulo that symmetry. Their full stoichiometric rank and
the counterstates in Section 7 rule out a generic invariant, projection,
deficiency-zero, or one-step tier reduction.

Globally, 2,169 positive and 191 signed pairs remain after the certified
affine-feasibility branch. The formerly focused
residual pair

\[
 \{B,2A,B+C\}\quad\&\quad\{0,A,C\}
\tag{9.2}
\]

fails the one-step tier test on \(w=(0,1,0)\), \(c=(0,2,0)\), but is now
closed by its exact physical-time core trace. The other 2,360 pairs require a
small library of genuinely multi-step lemmas: each must include arbitrary
extra reactions in its generator or stopping-time estimate and prove a
uniform activation/service margin across its gate. Minimal-support recurrence
alone is not an interface theorem for supersets.

The present audit certifies 1,532 additional ordered support pairs in
physical time: three exact-support pairs, 1,378 tier pairs, and 151
class-restricted affine-feasibility pairs. It still does not close T3-2,
because 2,360 ordered support pairs retain an affine-feasible failed
descriptor and no valid recurrence theorem is currently supplied for them.

## 10. Executable certificates

Run

    PYTHONPATH=src python3 src/global_atlas_interface_closure.py
    PYTHONPATH=src python3 -m unittest tests/test_global_atlas_interface_closure.py -v
    PYTHONPATH=src python3 src/global_tier_interface.py
    PYTHONPATH=src python3 -m unittest tests/test_global_tier_interface.py -v
    PYTHONPATH=src python3 src/stoichiometric_gate_feasibility.py
    PYTHONPATH=src python3 -m unittest tests/test_stoichiometric_gate_feasibility.py -v

The first certificate checks the support branches, the signed-service
\(5/3/2/0\) geometric/deficiency-zero/new/signed-table split, the exact 49/9
decomposition, rank formula (5.6), and the transparent 12-support family.
The second checks the arrangement and availability counts, the orientation
test on all residual pairs, every branch count in Section 8.4, fingerprints,
symmetry counts, the exact 12/37 split, the signed \(38/5/161/10\) superset
audit, and that every reported obstruction actually fails (8.9). The test
also constructs the two directed Hamiltonian cycles witnessing each reported
failure. The tier certificate also checks the canonical gate table, the 27
one-active descriptors, and the zero-cap support selector. Its full
deterministic hash is

\[
 \mathtt{c8ed2dd0834f6e94057e11d96900cf0fb5e1daca713cafa74f9963483eb62ad4}.
\tag{10.1}
\]

The affine-feasibility certificate has deterministic hash

\[
 \mathtt{d330193b1a1a835118f5f1ce5c26031ea2948ab5665a2f67ed38ec4dadb3c2f5}.
\tag{10.2}
\]

The analytic completeness and physical-time implications are proved here
and in *research_notes/stoichiometric_gate_feasibility.md*; the scripts are
not presented as substitutes for those arguments.

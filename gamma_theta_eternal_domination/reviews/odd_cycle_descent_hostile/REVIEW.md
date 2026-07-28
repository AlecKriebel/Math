# Hostile review: dynamic almost-cap descent

## Verdict

**PASS.**

The Boolean calculation in Section 1 is correct, including all chirality
orientations, the resolution step, and the displayed counterassignment.
It rigorously proves the note's useful negative conclusion: two almost-cap
arms realize only one implication and therefore cannot be substituted for
an equality chord.

The repaired source now states the exact hypotheses for C-098, identifies
the two-incidence control as C-099, and no longer claims that the controls
establish monotonic behavior for the proposed auxiliary quantities.  It
correctly distinguishes three facts: raw complement-edge transport can
fail, a repair can add a tight gate, and no accepted theorem supplies the
well-founded descent still needed.  The paired-repair lemma remains
explicitly open.

Reviewed source:

```text
math/working/odd_cycle_descent/NOTE.md
SHA-256 72841488157389ce829ba42530015e1b263decb530619e8298649972de0981e3
```

## Independent chirality reconstruction

Take \(a,b,c\) in cyclic order.  Canonical chirality assigns predecessor
color \(0\) and successor color \(1\).  Therefore the note's coordinates
are forced:

\[
\begin{array}{c|cc}
 &0&1\\ \hline
x\text{ of type }b&a&c\\
y\text{ of type }c&b&a\\
q\text{ of type }a&c&b.
\end{array}
\]

For \(xq\in E(H)\), the only common allowed color is \(c\).  The forbidden
pair is \(X=1,Q=0\), giving

\[
 \neg X\lor Q.
\]

For \(yq\in E(H)\), the only common allowed color is \(b\).  The forbidden
pair is \(Y=0,Q=1\), giving

\[
 Y\lor\neg Q.
\]

Resolution on \(Q\) gives \(\neg X\lor Y\).  This is not merely a sound
resolvent: existentially eliminating \(Q\) from the two arm clauses gives
exactly the endpoint relation

\[
 \{(X,Y)\}=\{(0,0),(0,1),(1,1)\}.
\]

The missing endpoint cross clause has common color \(a\), so it forbids
\((X,Y)=(0,1)\) and is \(X\lor\neg Y\).  Conjoining it with the arm
resolvent leaves precisely \((0,0),(1,1)\), namely \(X=Y\).

The note's counterassignment

\[
 (X,Y,Q)=(0,1,0)
\]

satisfies both arms while violating equality.  Hence raw chord replacement
is unsound.  No hidden global, domination, or eternal-family assumption is
needed for this local counterassignment.

If a complementary route enforces \(X\ne Y\), the arm resolvent removes
only \((1,0)\) and leaves \((0,1)\).  Thus it can orient the obstruction and
produce units, but it does not itself recover a smaller unit-free bicycle.
The note is correct to leave the paired-repair lemma open.

## Dependency audit

The accepted C-095 control verifies the limited statement that Boolean
same-sign substitution does not transport an arbitrary supporting
complement edge.  Its endpoint is not itself a physical representative, so
that control alone is not an exact model of the shortest-cycle
physical-endpoint geometry.

The stronger graph

```text
MFzJbZYhlrDZdMhd_
```

is the first control in the C-098 source package and is recorded as
**C-099** in `CLAIMS.md`.  With the cyclic relabeling

\[
 (a,b,c)=(2,0,1),\qquad(q,x,y,r)=(3,4,9,8),
\]

its checked data are

\[
\begin{aligned}
L(q)&=\{b,c\},&
L(x)&=\{a,c\},&
L(y)&=\{a,b\},&
L(r)&=\{b,c\},\\
qx,qy,ar&\in E(H),&
rx,ry&\in E(G).
\end{aligned}
\]

Thus it genuinely shows that the unique same-sign representative \(r\)
can lose both named original incidences.  However \(x=4\) is neutral to
the anchors, not physical for its omitted color; only \(y=9\) is already
physical.  After both endpoints of \(qx\) are physicalized, the relevant
representatives \(8,7\) are adjacent in \(H\).  Accordingly, this control
does not by itself refute a strengthening whose hypotheses require both
original arm endpoints to be physical.

For the two failed pairs displayed in that control, the common-neighbor
caps are \(13\) and \(7\).  Their lists and anchor signatures are

\[
\begin{array}{c|c|c}
\text{pair}&L(\text{cap})&N_H(\text{cap})\cap S\\ \hline
(8,4)&\{0,2\}&\{1\}\\
(8,9)&\{1,2\}&\{0\}.
\end{array}
\]

Both caps are exact third-color caps and are already physical: each has a
literal complement edge to its omitted anchor.  Consequently this control
supports “raw edge transport can fail” and “repair may introduce a tight
gate,” but it does **not** support the sentence that all of gate count,
connector length, physicalization distance, and failed-incidence count are
simultaneously nondecreasing.

C-098 can be invoked on an arm in the intended shortest-cycle geometry
only after stating its actual hypotheses: \(\gamma(G)=3\), the original
cross-clause edge, and same-sign physical representatives at both
endpoints.  If the representatives are adjacent in \(G\), C-098 supplies
the virtual-rainbow cap; if they are adjacent in \(H\), no cap is needed.
The present Section 2 mentions only \(aq\in E(G)\) and should explicitly
restore the other hypotheses from the surrounding three-gate geometry.

## Repair audit

All three issues from the first hostile pass are repaired in the frozen
source.

1. Section 2 now explicitly works with \(\gamma(G)=3\) and with \(x,y\)
   already replaced by same-sign physical representatives.  It also
   restates the edge-or-cap alternatives before invoking C-098.
2. The source cites C-099 for the two-specified-edge control and reserves
   C-098 for the cap theorem, including in the final open-lemma paragraph.
3. The unsupported simultaneous-monotonicity sentence is gone.  The note
   now says only that no accepted theorem determines monotonic behavior of
   the last three proposed quantities during every repair.

No remaining orientation, dependency, or scope blocker was found.  This
review is 100% complete for the frozen source hash above.

## Reproduction

The two accepted dependency checkers were replayed successfully:

```text
python3 -I -B -W error \
  reviews/physicalized_twosat_endgame_hostile/independent_check.py \
  reviews/physicalized_twosat_endgame_hostile/independent_result.json

python3 -I -B -W error \
  reviews/original_edge_incidence_hostile/independent_check.py \
  --check reviews/original_edge_incidence_hostile/evidence.json
```

Both returned `PASS`.  The finite truth table and exact control facts used
above are serialized in `evidence.json`.

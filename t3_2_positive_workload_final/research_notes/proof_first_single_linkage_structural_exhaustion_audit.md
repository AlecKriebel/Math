# Structural exhaustion audit for one active linkage

**Proof-first audit, 2026-08-12 PDT.  Verdict: STRUCTURAL PASS, with one
required interface repair.**  This note audits the classification in
Sections 5--6 of
`proof_first_single_linkage_at_most_three_species_composition.md`.  It uses
no support, orientation, or population enumeration.  It does not certify
the full one-linkage theorem, because the separated stopped theorem is a
separate analytic input and was not frozen when this audit was written.

The classification is exhaustive.  No missing disabled-top face and no
false rank or deficiency calculation was found.  The current composition
does, however, contain one invalid inference: an enabled complex in the top
deterministic tier need not itself have an outgoing edge to a lower tier.
The correct replacement is the already audited all-clock access-word lemma,
not one-step generator descent.  Sections 3--4 below verify that the lemma
applies to every such one-linkage tier sequence.

The local access-word inputs are frozen at

```text
9be70e2b6c9ce5c4762bf3130246f1ea660bea73f41aa7abdd997853cc0a6b04
    research_notes/proof_first_hard_enabled181_access_word.md
4028c026a7d01c1e0930bdbdaa75216a79402078999d6450c283a77eb2a04883
    research_notes/proof_first_hard_enabled181_access_word_independent_audit.md
```

The argument below rechecks the generic analytic hypotheses directly; the
finite 181-row scope of those files is not used.

## 1. Reduced setting and tier notation

Fix one closed irreducible population class \(\Gamma\).  Delete coordinates
constant on \(\Gamma\), delete linkage classes with no enabled source on
\(\Gamma\), and merge projected linkage classes which share a projected
complex.  Suppose the reduced network has one strongly connected linkage,
at most three dynamic species, and molecularity at most two.

Let \(x_n\in\Gamma\) be a proper escaping tier sequence.  After a
subsequence, every bounded integer coordinate is constant and every complex
is either enabled for all \(n\) or disabled for all \(n\).  Write

\[
 D^1=T^{D,1}_{\{x_n\}},\qquad
 E=\{y:x_n\ge y\},
\tag{1.1}
\]

where the inequality defining \(E\) holds eventually.  Let \(S^1\) be the
top stochastic source tier.

For an enabled source \(y\), stochastic mass action gives

\[
 \frac{\lambda_y(x_n)}{(x_n\vee1)^y}
 =\left(\sum_{y\to z}\kappa_{yz}\right)
   \prod_i
   \frac{(x_{n,i})_{\underline {y_i}}}
        {(x_{n,i}\vee1)^{y_i}}
 \longrightarrow c_y\in(0,\infty).
\tag{1.2}
\]

For a disabled source the numerator is zero.  It follows exactly that, if
\(j_*\) is the first deterministic tier meeting \(E\), then

\[
                  S^1=D^{j_*}\cap E.
\tag{1.3}
\]

In particular,

\[
                 S^1\subseteq D^1
 \quad\Longleftrightarrow\quad D^1\cap E\ne\varnothing.
\tag{1.4}
\]

Thus a tier failure is equivalent to every top deterministic complex being
disabled.

## 2. The top tier diverges

Because \(x_n\) escapes, at least one retained coordinate diverges.  A
retained coordinate is dynamic, so some reaction vector has a nonzero
component there and some complex contains that species.  Its deterministic
monomial diverges.  Therefore the common monomial scale \(M_n\) of \(D^1\)
satisfies

\[
                              M_n\longrightarrow\infty.
\tag{2.1}
\]

This observation rules out a disabled pure complex from \(D^1\): if
\(0,S_i\), or \(2S_i\) is disabled, its \((x_n\vee1)\)-monomial is one.
Consequently every member of \(D^1\) in a failed tier is a mixed binary
complex

\[
                              S_i+S_j,
\tag{2.2}
\]

with one coordinate identically zero and the other divergent.  This is the
complete local shape of a failure.

## 3. The top block is proper on an escaping fixed class

Put \(K=D^1\).  The access-word argument requires \(K\ne\mathcal C\).  This
is forced by the fixed-class hypothesis.

Suppose instead that every complex belongs to \(D^1\).  Let

\[
             L_n=\log(x_n\vee1),\qquad
             w_n=\frac{L_n}{\lVert L_n\rVert_2}.
\tag{3.1}
\]

Since the sequence escapes, \(\lVert L_n\rVert_2\to\infty\).  Pass to a
subsequence on which \(w_n\to w\).  Then \(w\ge0\) and
\(\lVert w\rVert_2=1\).  Top-tier equivalence of every pair \(y,z\) says

\[
 L_n\mathbin\cdot(y-z)
   =\log\frac{(x_n\vee1)^y}{(x_n\vee1)^z}=O(1),
\tag{3.2}
\]

so \(w\cdot(y-z)=0\).  Hence \(w\) is orthogonal to every reaction vector
and \(w\cdot X\) is an exact stoichiometric invariant.

At least one component \(w_i\) is positive.  Since a bounded coordinate has
\(L_{n,i}=O(1)\), every positive component of \(w\) belongs to a divergent
coordinate.  Thus

\[
                      w\cdot x_n\ge w_i x_{n,i}\longrightarrow\infty,
\tag{3.3}
\]

contradicting constancy of \(w\cdot X\) on \(\Gamma\).  Therefore

\[
                              \varnothing\ne K\subsetneq\mathcal C.
\tag{3.4}
\]

## 4. Repair of the enabled-top branch

Assume \(K\cap E\ne\varnothing\) and choose \(v_0\in K\cap E\).  Strong
connectivity and (3.4) give a directed path from \(v_0\) to
\(\mathcal C\setminus K\).  Erase loops and stop at the first exit:

\[
 v_0\longrightarrow v_1\longrightarrow\cdots
 \longrightarrow v_{m-1}\longrightarrow v_m,
 \qquad v_0,\ldots,v_{m-1}\in K,\quad v_m\notin K.
\tag{4.1}
\]

The length is bounded by \(|\mathcal C|-1\), independently of \(n\).  Its
first source is enabled.  After firing \(v_{j-1}\to v_j\), the physical
state contains the product complex \(v_j\), so the next prescribed source
is enabled.  Every intermediate state differs from \(x_n\) by a bounded
vector.  For a divergent coordinate this changes falling factorials only
by a \(1+o(1)\) factor; for a bounded coordinate the prescribed product has
created enough copies and all nonzero factors range over a fixed finite
set.  Hence every prescribed source rate before the exit is comparable
with \(M_n\).  Every competing source rate is at most \(C M_n\).

Retain every physical clock and stop either when (4.1) is completed or at
the first competitor.  Exact exponential races give a fixed success
probability \(p_0>0\) and, for every fixed \(r\), duration
\(O(M_n^{-r})\).  For a competitor of rate \(b_n\), the exact factorial
identity and the top-scale bound on its target give

\[
 (\Delta G_\ell)^+\le C+\log^+(M_n/b_n),
\tag{4.2}
\]

where \(G_\ell=K_\ell+\sum_i\log(x_i!)+\ell\cdot x\ge1\).  Its race
probability is at most \(Cb_n/M_n\), and therefore

\[
 \frac{b_n}{M_n}
 \left(1+\log^+\frac{M_n}{b_n}\right)^r\le C_r.
\tag{4.3}
\]

Summing over the fixed reaction set and the bounded word proves arbitrary
fixed positive endpoint moments.  The successful terminal edge has gap

\[
 g_n=\log\frac{(x_n\vee1)^{v_{m-1}}}
                    {(x_n\vee1)^{v_m}}\longrightarrow\infty,
\tag{4.4}
\]

and hence \(\Delta G_\ell=-g_n+O(1)\).  The exact fourth-power expansion
then gives

\[
 \mathbb E_{x_n}\!\left[
   W_\ell(X_{\tau_n})-W_\ell(x_n)+\tau_n\right]
       \le-cG_\ell(x_n)^3g_n,
 \qquad W_\ell=G_\ell^4,
\tag{4.5}
\]

for all large \(n\).  This is exactly the generic access-word lemma audited
at the hashes above.

This repairs a genuine error in the current composition.  Strong
connectivity does **not** imply that some enabled member of \(K\) has an
edge leaving \(K\): a path may first move inside \(K\) to a member disabled
at \(x_n\), and only that member may carry the exit.  The physical word
(4.1) creates each subsequent source and is the correct proof.  Accordingly,
the enabled-top region is an episode-good region, not necessarily a
one-step generator-good region.

## 5. Dimensions at most two

Zero retained species gives a singleton.  With one retained species, a
nonconstant binary linkage contains \(S\) or \(2S\), so the published
Anderson--Cappelletti--Kim theorem applies.

With two retained species \(A,B\), suppose without loss that neither
\(A\) nor \(2A\) occurs.  Since \(A\) is dynamic, \(A+B\) occurs, and

\[
                  \mathcal C=\{A+B\}\cup T,
                  \qquad T\subseteq\{0,B,2B\},\quad T\ne\varnothing.
\tag{5.1}
\]

If \(|T|=1\), then \(m=2,s=1\), so \(\delta=m-1-s=0\).  If
\(|T|=2\), the difference of the two axis complexes spans the \(B\)-axis
and the difference to \(A+B\) has nonzero \(A\)-component; hence
\(m=3,s=2,\delta=0\).  The unique residual support is

\[
                         \{0,B,2B,A+B\},
\tag{5.2}
\]

with \(m=4,s=2,\delta=1\).  It is covered by the independently audited
two-species service theorem.  If both species lack a pure multiple, the
only nonconstant support is \(\{0,A+B\}\), again deficiency zero.  Thus
(5.2), up to relabelling, is the exact two-species exception.

## 6. Three-species failed tiers: exhaustive symbolic split

Let \(r\in\{1,2,3\}\) be the number of divergent coordinates.  Section 2
reduces the classification to mixed complexes joining a divergent species
to a zero coordinate.

### 6.1 Three divergent coordinates

Every binary complex is eventually enabled, so no tier failure occurs.

### 6.2 Two divergent coordinates

Relabel so that \(A,B\to\infty\).  A failure is possible only if the third
coordinate is \(C=0\), and then

\[
                    \varnothing\ne D^1
                       \subseteq\{A+C,B+C\}.
\tag{6.1}
\]

If \(D^1=\{A+C\}\), then \(A/B\to\infty\).  Indeed, if
\(A/B\) stayed bounded above and below, dynamicity of \(B\) would force a
complex containing \(B\); the binary possibilities are: \(B\), which is
an enabled top; \(2B\) or \(A+B\), which lies strictly above; or \(B+C\),
which ties \(A+C\).  Every alternative contradicts the singleton failed
top.  The alternative \(A/B\to0\) is also impossible: every possible
complex witnessing dynamicity of \(B\) would then lie strictly above
\(A+C\).  Moreover

\[
 \{A+C\}\subseteq\mathcal C
 \subseteq\{0,C,2C,B,2B,B+C,A+C\},
\tag{6.2}
\]

and any present \(2B\) satisfies \(B^2/A\to0\).  This is precisely the
separated support, with gap \(\log(A/m(B))\to\infty\).  The singleton
\(\{B+C\}\) case is symmetric.

If \(D^1=\{A+C,B+C\}\), then \(A/B\to c\in(0,\infty)\).  The presence of
\(A,B,2A,A+B\), or \(2B\) would give an enabled top or a strictly higher
enabled complex.  Hence

\[
 \{A+C,B+C\}\subseteq\mathcal C
       \subseteq\{0,C,2C,A+C,B+C\}.
\tag{6.3}
\]

This is the balanced branch.

### 6.3 One divergent coordinate

Relabel so that \(A\to\infty\).  The only possible top complexes are
disabled members of \(\{A+B,A+C\}\).  A present pure \(A\) would be an
enabled top and \(2A\) would dominate.  There are two cases.

* A singleton top, say \(\{A+C\}\), forces \(C=0\), excludes \(A+B\),
  and gives exactly the separated containment (6.2).  Here a bounded
  spectator automatically satisfies its separated gap.
* The tied top \(\{A+B,A+C\}\) forces \(B=C=0\) and
  \[
  \{A+B,A+C\}\subseteq\mathcal C
   \subseteq\{0,A+B,A+C,B,C,2B,2C,B+C\}.
  \tag{6.4}
  \]
  This is exactly the support of the independently audited bounded
  two-disabled-top theorem, including its invariant and frozen
  alternatives.

The three values of \(r\), the singleton/tied split, and relabelling exhaust
all failed tiers.  No orientation enters this classification.

## 7. Balanced rank and deficiency audit

There is a useful strengthening of the wording in the current composition.
Let

\[
 U=\{0,C,2C,A+C,B+C\},
 \qquad \{A+C,B+C\}\subseteq\mathcal C\subseteq U.
\tag{7.1}
\]

Every **proper** such support is deficiency zero, not only every full-rank
four-complex support.  For \(m=2\), the two mixed complexes have rank one.
For \(m=3\), adding any one of \(0,C,2C\) gives rank two.  For \(m=4\),
adding any two distinct axis complexes gives the \(C\)-direction, while
their differences to the mixed complexes independently give the \(A\)-
and \(B\)-directions, so the rank is three.  In all three cases

\[
                              s=m-1,qquad \delta=m-1-s=0.
\tag{7.2}
\]

The full five-complex support has rank three and deficiency
\(5-1-3=1\).  It is the sole non-deficiency-zero balanced support and is
the only member of (7.1) which needs the balanced all-clock theorem.

Thus the rank calculations in the current composition are correct where
stated, but its published replacement should use the stronger exhaustive
form (7.2) so that lower-rank balanced supports are not left implicit.

## 8. Exact structural conclusion

For every escaping proper tier sequence of a reduced binary one-linkage
network with at most three dynamic species, exactly one of the following
applies after relabelling:

1. \(D^1\cap E\ne\varnothing\), and the audited physical access-word
   episode (4.5) applies;
2. the separated singleton-top support (6.2) applies;
3. the tied one-carrier support (6.4) applies;
4. the balanced support (6.3) applies;
5. a deficiency-zero, pure-multiple, invariant, or frozen branch has
   already closed the fixed class.

The list is symbolic and exhaustive.  The only correction required in the
current Sections 5--8 is to replace the asserted one-step enabled-top
generator descent by the access-word stopped estimate (4.5), and to state
the stronger balanced deficiency calculation (7.2).  Once a separated
theorem is frozen and independently passed, these branches can be composed
under the same factorial-linear fourth power by a physical random-time
Foster argument.

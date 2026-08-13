# Proof-first audit of the one-active-linkage reduction

**Status: not certified.**  The standard single-linkage theorem does not
prove the classwise statement needed by T3-2.  The smallest unsupported
projected support already has two dynamic species.  This note identifies the
exact proof gap; it does **not** give a counterexample to positive recurrence.

## 1. Statement under audit

Fix a closed irreducible population class \(\Gamma\).  Delete coordinates
constant on \(\Gamma\), delete linkages inactive on \(\Gamma\), and merge
projected linkages that share a complex.  The desired one-linkage branch would
say:

> Every weakly reversible binary stochastic mass-action system whose reduced
> network has at most three dynamic species and exactly one active linkage
> class is positive recurrent on \(\Gamma\), for every positive rate vector
> and every strongly connected orientation of the support.

The conclusion is stronger than the published theorem cited for this branch.

## 2. Exact scope of the published theorem

Anderson, Cappelletti, and Kim, *Stochastically modeled weakly reversible
reaction networks with a single linkage class*, J. Appl. Probab. 57 (2020),
792--810, arXiv:1904.08967, Theorem 4.1, assume all three of the following:

1. weak reversibility and one linkage class;
2. binary complexes; and
3. for **each species** \(S_i\), the complex set contains a positive pure
   multiple \(S_i\) or \(2S_i\).

The last hypothesis is not a consequence of classwise projection.  The proof
uses it precisely when a top D-tier complex is an unavailable mixed complex
\(S_u+S_v\), with \(x_u=0\) and \(x_v\to\infty\).  The pure complex \(S_v\)
or \(2S_v\) is used to compare that unavailable monomial to an enabled
propensity.

The same paper's Theorem 6.1 gives a more general sufficient condition,

\[
 T^{S,1}_{\{x_n\}}\subseteq T^{D,1}_{\{x_n\}}
 \quad\hbox{for every proper tier sequence }\{x_n\}.
\tag{2.1}
\]

The exact examples below violate (2.1) inside one closed irreducible class.
Thus Theorem 6.1 does not silently repair the missing pure-complex hypothesis.

Primary source: <https://arxiv.org/abs/1904.08967>

## 3. Analytic reduction in one and two dynamic species

The following argument is structural and contains no support enumeration.

With one dynamic species, every nonconstant binary support contains \(S\) or
\(2S\).  The published theorem therefore applies.

Now take two dynamic species \(A,B\).  If the support contains a positive pure
multiple of both species, the published theorem again applies.  Otherwise,
suppose without loss of generality that neither \(A\) nor \(2A\) is present.
Since \(A\) is dynamic, the mixed complex \(A+B\) must be present, and every
other complex lies on the \(B\)-axis.  Hence

\[
 {cal C}=\{A+B\}\cup T,
 \qquad T\subseteq\{0,B,2B\},\qquad T\ne\varnothing .
\tag{3.1}
\]

If \(|T|=1\), the stoichiometric rank is one and the deficiency is
\(2-1-1=0\).  If \(|T|=2\), the difference of the two axis complexes spans
the \(B\)-axis, while the difference from \(A+B\) has nonzero \(A\)-component;
the rank is two and the deficiency is \(3-1-2=0\).  Weakly reversible
deficiency-zero systems have the normalizable product-form stationary law on
each closed irreducible class.  Consequently every case in (3.1) except

\[
 \boxed{{\cal E}=\{0,B,2B,A+B\}}
\tag{3.2}
\]

is already closed by a published theorem.  The support \({\cal E}\) has rank
two and deficiency one.  The same conclusion holds if both species lack a
pure multiple: the only possible nonconstant support outside \(A+B\) is
\(\{0\}\), which is deficiency zero.

Thus (3.2), up to exchanging species, is the unique two-dynamic-species
support left after the pure-multiple and deficiency-zero theorems.  This is a
proof of the reduction, not a finite search.

Primary deficiency-zero source: D. F. Anderson, G. Craciun, and T. G. Kurtz,
*Product-form stationary distributions for deficiency zero chemical reaction
networks*, arXiv:0803.3042, <https://arxiv.org/abs/0803.3042>.

## 4. Exact classwise obstruction on the four-complex support

Give (3.2) the strongly connected orientation

\[
 0\longrightarrow B\longrightarrow 2B\longrightarrow A+B
   \longrightarrow0
\tag{4.1}
\]

and arbitrary positive rates on these four reactions.  Its CTMC is
irreducible on \(\mathbb Z_{\ge0}^2\).  Indeed, from any \((a,b)\):

- repeatedly use \(A+B\to0\) when \(a,b>0\);
- if \(a>0,b=0\), first use \(0\to B\), then \(A+B\to0\);
- if \(a=0,b\ge2\), use \(2B\to A+B\), then \(A+B\to0\);
- if \((a,b)=(0,1)\), first use \(0\to B\) and then the preceding step.

These moves reach \((0,0)\).  Conversely, \(0\to B\) raises \(b\), and the
following enabled path raises the boundary value of \(a\) by one:

\[
\begin{aligned}
(a,0)&\to(a,1)\to(a,2)\to(a+1,1)\\
     &\to(a+1,2)\to(a+2,1)\to(a+1,0).
\end{aligned}
\tag{4.2}
\]

It follows that every state communicates with \((0,0)\); the whole lattice is
one closed irreducible class.

On the unbounded sequence

\[
 x_n=(n,0)
\tag{4.3}
\]

the D-monomials of \(0,B,2B,A+B\), computed with \(x\vee1\), are
\(1,1,1,n\).  Hence

\[
 T^{D,1}_{\{x_n\}}=\{A+B\}.
\tag{4.4}
\]

But at \((n,0)\) the only enabled source is \(0\), so

\[
 T^{S,1}_{\{x_n\}}=\{0\}.
\tag{4.5}
\]

Equations (4.4)--(4.5) contradict (2.1).  They also show directly why the
one-step Anderson--Kim entropy criterion cannot be invoked: the global top
D-tier consists of a disabled mixed complex.

This is not a pathology caused by moving between stoichiometric classes.  The
sequence (4.3) lies in the single closed irreducible class just proved.

## 5. A genuinely three-dynamic-species witness

For completeness, the same obstruction occurs with all three coordinates
dynamic.  Take

\[
 {\cal C}_3=\{0,A,C,2A,A+B\}
\tag{5.1}
\]

with directed cycle

\[
 0\to A\to2A\to A+B\to C\to0.
\tag{5.2}
\]

The stoichiometric rank is three, the deficiency is one, and the pure
multiple required for \(B\) is absent.  On \(x_n=(0,n,0)\), the top D-tier is
\(\{A+B\}\) while the only enabled source is \(0\).  Boundary states with
successive values of \(n\) communicate: a decrement is

\[
(0,n,0)\to(1,n,0)\to(0,n-1,1)\to(0,n-1,0),
\tag{5.3}
\]

and an increment is

\[
\begin{aligned}
(0,n,0)&\to(1,n,0)\to(2,n,0)\to(1,n+1,0)\\
       &\to(2,n+1,0)\to(1,n+2,0)\to(0,n+1,1)
         \to(0,n+1,0).
\end{aligned}
\tag{5.4}
\]

In fact (5.2) is irreducible on the whole nonnegative lattice.  To reach zero,
first remove every \(C\) through \(C\to0\).  While \(B>0\), create one \(A\)
through \(0\to A\) if necessary, fire \(A+B\to C\), and then \(C\to0\);
this lowers \(B\) by one.  Once \(B=0\), a pair of \(A\)'s is removed by
\(2A\to A+B\to C\to0\); if one \(A\) remains, first use \(0\to A\).

Conversely, from zero first create \(a+c\) copies of \(A\).  The two-reaction
word \(A\to2A\to A+B\) adds one \(B\) without changing the current \(A\)
count, so create \(b+c\) copies of \(B\), and then fire
\(A+B\to C\) exactly \(c\) times.  This reaches \((a,b,c)\).  The special
case \(a=c=0<b\) is obtained by first making one \(A\), adding \(b+1\)
copies of \(B\), and finishing with \(A+B\to C\to0\).  Thus every state
communicates with zero.  The obstruction is therefore not removed by
requiring exactly three dynamic species.

## 6. Strict conclusion and required repair

The desired one-active-linkage theorem is **not proved** by the inherited
citations.  The exact first missing support is (3.2), and (4.1)--(4.5) give a
classwise counterexample to every attempted direct use of the published
single-linkage tier hypothesis.  Section 5 supplies a full-rank
three-coordinate version.

No claim of transience or null recurrence is made.  In particular, these
networks are plausible positive recurrent systems; what fails is the proof
interface.

A valid repair must supply a new boundary return argument.  On (3.2), it must
control excursions from \(B=0\): a slow \(0\)-source event creates access to
the mixed \(A+B\) clock, after which a fast service episode must remove an
old \(A\)-particle with a rate-uniform negative entropy balance.  In three
species, the analogous lemma must handle two possible cofactor complexes and
must be uniform over all strongly connected orientations.  Until that
stopped/trace lemma is proved and independently audited, the global T3-2
statement cannot use “the preserved one-linkage theorem” as a complete
classwise branch.

Finally, all binary systems considered here are nonexplosive: any reaction
with a bimolecular source cannot increase total population, while every
population-increasing reaction has source degree zero or one.  Its total
positive-jump rate is therefore at most \(C(1+|x|)\), and jumps are bounded.
The unresolved issue is positive recurrence, not existence of the CTMC.

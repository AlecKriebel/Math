# The mixed finite-tree/spine normalization obstruction

Date: 2026-08-13 (America/Los_Angeles)

No graph search, tree enumeration, transform search, or external
communication was used.

## 1. Status

**EXACT POSITIVE MIXED EXPANSION AND DECISIVE COCYCLE OBSTRUCTION.**
Let `1<r<2` and `c=r-1`.  The endpoint first iterate

\[
 h_1={1\over1+rcRq},\qquad
 \mathcal F_r(cq)=1-h_1                                  \tag{1}
\]

does have the natural positive interpretation suggested by the two
geometric branching processes:

- `h_1` is the mass of dB root stars in which every child is either
  unmarked or is marked and carries a surviving Bd tree;
- `1-h_1` is the mass of root stars with a first marked child carrying a
  finite Bd extinction tree; preceding failed children may carry Bd
  survival spines;
- `s=1-h` is the mass of dB survival trees with a leftmost infinite spine;
  preceding side bushes are finite dB extinction trees.

Consequently the missing endpoint inequality

\[
                         E_p(h-h_1)\geq0                 \tag{2}
\]

is exactly a mass comparison between these two positive mixed ensembles.

The comparison, however, does not yield a new sign.  After conditioning the
selected Bd tree on extinction and the selected dB subtree on survival, all
subtree laws have mass one.  The remaining edge-skeleton likelihood on the
dB survival spine is

\[
 L_{ij}={z_j\over h_i+s_i(Kz)_i},
 \qquad z={cq\over s}.                                  \tag{3}
\]

Its row mass is

\[
 \ell_i:=\sum_jK_{ij}L_{ij}
       ={\mathcal F_r(cq)_i\over s_i}.                  \tag{4}
\]

Thus row-normalizing the spine tilt removes precisely the unknown endpoint
factor, while leaving it unnormalized does not define a consistent path
measure.  On a symbolic reversible two-type family, the exact likelihood has
strictly positive cycle holonomy: `ell_1 ell_2>1` away from the homogeneous
case.  Hence no positive terminal coboundary can turn it into a martingale.

This closes the natural **type-preserving multiplicative**
size-biased/conditioned-spine comparison.  It does not disprove (2), and it
does not rule out arbitrary nonlocal allocations that move mass between
different spine positions, root types, or tree shapes.

## 2. Endpoint branching setup

Let `P` be a finite irreducible row-stochastic kernel reversible for `pi`.
Let `a>0`, normalized by `E_pi a=1`, and define

\[
 p_i=\pi_i a_i,
 \qquad R=D_a^{-1}PD_a,
 \qquad t_i={(Pa)_i\over a_i}.                          \tag{5}
\]

Then `R1=t` and `p_iR_ij=p_jP_ji`.  The dB geometric branching process has
offspring mean `rt_i` and child kernel `R_ij/t_i`.  Its extinction and
survival probabilities `h=1-s` satisfy

\[
 h={1\over1+r(t-Rh)},
 \qquad s=rhRs.                                         \tag{6}
\]

The Bd process has offspring mean `r/t_i`, child kernel `P`, extinction
probability `q`, and survival probability `b=1-q`, with

\[
 q={t\over t+r(1-Pq)},
 \qquad b={rq\over t}Pb.                                \tag{7}
\]

All vector operations in (6)--(7) are componentwise except multiplication
by a kernel.

## 3. A first-success lemma for geometric offspring

Let a child of type `j` independently be declared successful with
probability `x_j`, where `0<=x<=1`.  In a dB root star of type `i`, choose
the first successful child in plane order.  The mass that this selected
child has type `j` is

\[
 \boxed{
 J^x_{ij}=r\,h(x)_iR_{ij}x_j,
 \qquad h(x)_i={1\over1+r(Rx)_i}.}                     \tag{8}
\]

Indeed, if the selected child is in position `m`, the first `m-1` children
fail, the `m`th child has type `j` and succeeds, and all later children are
integrated out.  Since a `Geom_0(rt_i)` count has tail

\[
 \Pr(N_i\geq m)=\left({rt_i\over1+rt_i}\right)^m,
\]

summing the resulting geometric series gives (8).  In particular,

\[
 \sum_jJ^x_{ij}={r(Rx)_i\over1+r(Rx)_i}
                =\mathcal F_r(x)_i.                    \tag{9}
\]

There are two relevant substitutions.

1. For `x=s`, equations (6) give `h(s)=h`, and

   \[
   J^S_{ij}:=J^s_{ij}=rh_iR_{ij}s_j,
   \qquad \sum_jJ^S_{ij}=s_i.                           \tag{10}
   \]

   This selects the first dB-surviving child.  Iterating the selection gives
   the leftmost dB infinite spine.

2. For `x=cq`, equation (1) gives `h(cq)=h_1`, and

   \[
   J^G_{ij}:=J^{cq}_{ij}=rch_{1,i}R_{ij}q_j,
   \qquad \sum_jJ^G_{ij}=\mathcal F_r(cq)_i.            \tag{11}
   \]

   Here a success means that the child is independently `c`-marked and its
   attached Bd process becomes extinct.

After averaging the root with `p`, (2) is equivalently

\[
             \sum_{i,j}p_iJ^G_{ij}
             \;\geq\;\sum_{i,j}p_iJ^S_{ij}.            \tag{12}
\]

## 4. The complete positive mixed ensembles

### 4.1 The no-good complement

For every dB child of type `j`, independently attach a Bernoulli mark of
probability `c` and, if marked, an independent Bd branching process.  The
child fails to be good precisely when it is unmarked or its marked Bd tree
survives.  Its failure probability is

\[
                  1-cq_j=(1-c)+cb_j.                   \tag{13}
\]

Consequently `h_1` has the exact positive expansion

\[
 h_{1,i}
 =\sum_{d\geq0}\ \sum_{j_1,\ldots,j_d}
   {r^d\over(1+rt_i)^{d+1}}
   \prod_{m=1}^dR_{ij_m}\{(1-c)+cb_{j_m}\}.            \tag{14}
\]

Every factor `b_j` in (14) can be realized by a Bd tree conditioned on
survival and equipped with its leftmost infinite spine.  Thus (14) is a dB
root star carrying a possibly empty forest of marked Bd survival spines.

### 4.2 The first-good complement

The complement `1-h_1` chooses the first marked child whose attached Bd tree
is finite.  Every preceding failed child has the positive decomposition
(13), the selected child carries a Bd tree conditioned on extinction, and
later children are unrestricted.  Integrating these normalized decorations
gives exactly the edge mass (11).

For completeness, the Bd law conditioned on extinction has local plane-tree
probability

\[
 \widehat{\Pr}^{,B}_i
  (d;j_1,\ldots,j_d)
 ={1\over q_i}
   {r^dt_i\over(t_i+r)^{d+1}}
   \prod_{m=1}^dP_{ij_m}q_{j_m}.                        \tag{15}
\]

It is a probability law because of (7).  Its offspring count is geometric
with mean

\[
 \widehat m_i^B={rq_i(Pq)_i\over t_i},                 \tag{16}
\]

and its child kernel is

\[
 \widehat P^B_{ij}={P_{ij}q_j\over(Pq)_i}.             \tag{17}
\]

Similarly, conditioning a Bd tree on survival and selecting its first
surviving child gives the spine transition

\[
 K^{B,\mathrm{sp}}_{ij}
 ={P_{ij}b_j\over(Pb)_i}
 ={rq_iP_{ij}b_j\over t_ib_i}.                         \tag{18}
\]

### 4.3 The dB survival side

Condition a dB tree on survival and select its first surviving child.  The
resulting spine transition is

\[
 \boxed{
 K_{ij}={J^S_{ij}\over s_i}
        ={rh_iR_{ij}s_j\over s_i}.}                    \tag{19}
\]

Before the selected child, every side bush is a finite dB tree conditioned
on extinction; after it, children are unrestricted.  Iterating (19) gives a
positive leftmost-spine representation of the full survival event.

Equations (11), (15), and (19) prove that (12) is literally a comparison of
two positive mixed measures:

- dB leftmost-survival-spine configurations of mass `p_iJ^S_ij`;
- first-good configurations of mass `p_iJ^G_ij`, with a selected finite Bd
  tree and possible preceding Bd survival spines.

All conditional trees and side decorations in this factorization have mass
one.  They cannot change the scalar comparison of the edge skeletons.

## 5. The exact skeleton likelihood

Normalize the dB survival edge measure.  If

\[
 S=E_ps,
 \qquad \nu_i={p_is_i\over S},                          \tag{20}
\]

then its edge law is `nu_i K_ij`.  On its support, the first-good edge mass
divided by the survival edge mass is

\[
 {J^G_{ij}\over J^S_{ij}}
 =c{h_{1,i}\over h_i}{q_j\over s_j}.                   \tag{21}
\]

Set

\[
                         z_i={cq_i\over s_i}.            \tag{22}
\]

From (19),

\[
 rc(Rq)_i={s_i\over h_i}(Kz)_i.
\]

Since `h_i+s_i=1`, equation (1) becomes

\[
 {h_{1,i}\over h_i}={1\over h_i+s_i(Kz)_i}.            \tag{23}
\]

Substitution in (21) proves the likelihood formula (3).  Its conditional
row mass is

\[
 \ell_i=\sum_jK_{ij}L_{ij}
 ={(Kz)_i\over h_i+s_i(Kz)_i}
 ={\mathcal F_r(cq)_i\over s_i},                       \tag{24}
\]

which proves (4).  Therefore

\[
 \boxed{
 E_p\{\mathcal F_r(cq)-s\}
 =\sum_ip_is_i(\ell_i-1).}                             \tag{25}
\]

This exposes the normalization impasse precisely.

- The unnormalized kernel `K_ij L_ij` has the desired first-good edge mass,
  but its row sums are `ell_i`, not one.
- Row normalization gives the valid transition

  \[
  \widetilde K_{ij}={K_{ij}L_{ij}\over\ell_i}
  ={R_{ij}q_j\over(Rq)_i},                             \tag{26}
  \]

  but removes exactly the factors whose weighted average is the desired
  inequality (25).

Thus conditioning on the two subtrees and changing the spine measure does
not create a hidden positive term.  It returns the original endpoint gap as
the missing normalization.

## 6. Exact two-type cycle obstruction

The lack of normalization is structural, not a bookkeeping artifact.  Take

\[
 P=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 \pi=(1/2,1/2),\qquad
 a=\left({2\over1+k},{2k\over1+k}\right),\qquad k>0.   \tag{27}
\]

Then

\[
 t=(k,k^{-1}),\qquad
 R=\begin{pmatrix}0&k\\k^{-1}&0\end{pmatrix}.         \tag{28}
\]

Write

\[
 A=1+rk,\qquad B=k+r.
\]

The positive endpoint solutions are

\[
 h=\left({B\over rA},{A\over rB}\right),
 \qquad
 s=\left({k(r^2-1)\over rA},{r^2-1\over rB}\right),   \tag{29}
\]

\[
 q=\left({A\over rB},{B\over rA}\right).              \tag{30}
\]

The first-iterate complement is

\[
 h_1=\left({A\over A+ckB},{kB\over kB+cA}\right).     \tag{31}
\]

The dB survival spine (19) is the deterministic two-cycle

\[
 K=\begin{pmatrix}0&1\\1&0\end{pmatrix}.              \tag{32}
\]

Hence the two row masses (24) are also the two successive likelihood
factors along every infinite spine:

\[
 \ell_1={rAB\over(r+1)(A+ckB)},
 \qquad
 \ell_2={rAB\over(r+1)(kB+cA)}.                        \tag{33}
\]

For `1<r<(1+sqrt(5))/2` and `0<k<1`, direct factorization gives

\[
 \ell_1-1
 ={-(k-1)(-k+r^2-r-1)\over(r+1)(A+ckB)}<0,             \tag{34}
\]

\[
 \ell_2-1
 ={(k-1)(k(r^2-r-1)-1)\over(r+1)(kB+cA)}>0.            \tag{35}
\]

Thus even a root-type-preserving one-step injection fails: one type has a
strict target deficit while the other has a strict excess.

More decisively, the likelihood has nontrivial cycle holonomy.  With
`c=r-1`, exact algebra gives

\[
 \ell_1\ell_2-1
 ={(k-1)^2Q(c,k)
   \over(r+1)^2(A+ckB)(kB+cA)},                         \tag{36}
\]

where

\[
\begin{aligned}
 Q(c,k)={}&kc^5+(k^2+5k+1)c^4
 +(3k^2+9k+3)c^3\\
 &+(2k^2+5k+2)c^2+(k+1)^2.
\end{aligned}                                           \tag{37}
\]

Every coefficient in (37) is positive.  Therefore

\[
                         \ell_1\ell_2>1\qquad(k\ne1).  \tag{38}
\]

An unnormalized multiplicative density on the alternating spine would
multiply its mass by `(ell_1 ell_2)^n` after `2n` steps.  It cannot be the
cylinder density of a finite consistent path measure.  Nor can a positive
terminal coboundary repair it: consistency would require positive
`u_1,u_2` satisfying

\[
 u_1=\ell_1u_2,
 \qquad u_2=\ell_2u_1,
\]

which forces `ell_1 ell_2=1`, contradicting (38).  Dividing by the Perron
factor or row-normalizing restores a probability kernel only by changing the
first-good masses in (11).

At `k=1`, both row masses equal one, the cocycle is trivial, and the
homogeneous endpoint is equality.  Thus the obstruction isolates exactly
the non-isothermal mode.

## 7. Scope and next implication

The mixed branching representation is exact and positive, but its natural
multiplicative use is exhausted:

1. conditioning the selected finite and infinite subtrees normalizes them
   away;
2. the remaining edge likelihood has the endpoint ratio itself as its row
   mass; and
3. its exact two-type cycle product is not one, so it is not a martingale or
   a removable coboundary on the dB survival spine.

This does not exclude a nonlocal allocation that deliberately moves deficit
mass from one spine position to excess mass at another.  Such an argument
would need a new global transport inequality controlling the nonstationary
root law, rather than another conditioning or size-biasing of the same
spine.

## 8. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_mixed_spine_normalization_obstruction/verify_mixed_spine.py
```

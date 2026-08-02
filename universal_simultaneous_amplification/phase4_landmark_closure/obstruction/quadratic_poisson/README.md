# Quadratic Poisson certificates at `r=2`

Date: 2026-08-02 (America/Los_Angeles)

## Status

This directory records two distinct certificate questions for the exact
geometric-union dB dual at fitness `r=2`.

1. **Half-density target (OPEN).**  Seek a graph-dependent Boolean quadratic
   `g` such that

   \[
   \mathcal Dg(A)\ge 2|A|-n
   \]

   on every nonempty proper set.  Such a certificate would prove
   `rho_dB(G,2) <= 1/2`.  Extensive numerical screens support the stronger
   sparse ansatz

   \[
   g(A)=c|A|+\sum_{ij\in E}q_{ij}{\bf1}_{i\in A}{\bf1}_{j\in A},
   \]

   but no universal formula or existence proof is claimed.

2. **Complete-graph target (quadratic route refuted).**  Put

   \[
   m_K(n)=\frac{(n-1)2^{n-2}}{2^{n-1}-1}.
   \]

   The stronger inequality `Dg(A) >= |A|-m_K(n)` would prove that the
   complete graph maximizes dB fixation at `r=2`.  The unit cycle `C_5`
   admits no such certificate of Boolean degree at most two, even if all
   unordered pair monomials are allowed.  This is an exact Farkas
   obstruction, not a fixation counterexample.  A cubic certificate does
   exist on `C_5`.

The exact claims in the second item are checked by
`verify_c5_hierarchy.py`.  The atlas counts in
`screen_poisson_hierarchy.py` are floating-point discovery evidence only.
There is also a universal exact obstruction to every bounded-degree version
of this strategy: `COMPLETE_DEGREE_BARRIER.md` proves that the minimum
Boolean degree of an exact complete-baseline Poisson certificate on `K_n`
is `n-2`.

## 1. Exact generator formulas used in the screens

Let

\[
 H_{vi}=\frac{2P_{vi}}{1+P_{vi}},\qquad
 C_{v;ij}=H_{vi}+H_{vj}
 -\frac{2(P_{vi}+P_{vj})}{1+P_{vi}+P_{vj}}.
\]

For `x_i(A)=1_{i in A}`, direct evaluation of the geometric-union update
gives

\[
 \mathcal D x_i(A)=
 \begin{cases}
 -1,&i\in A,\\
 \sum_{v\in A}H_{vi},&i\notin A,
 \end{cases}
\]

and, for `i != j`,

\[
 \mathcal D(x_ix_j)(A)=
 \begin{cases}
 -2,&i,j\in A,\\
 \sum_{v\in A\setminus\{j\}}H_{vi},&i\notin A,\ j\in A,\\
 \sum_{v\in A\setminus\{i\}}H_{vj},&i\in A,\ j\notin A,\\
 \sum_{v\in A}C_{v;ij},&i,j\notin A.
 \end{cases}
\]

These are exact consequences of the update rule.  They make the quadratic
feasibility problem a finite linear program without constructing the full
transition matrix.

## 2. Exact `C_5` quadratic obstruction

For a subset of the five-cycle, let `K` be its size, `E` the number of
occupied cycle edges, and `N` the number of occupied nonedges.  The six
dihedral orbits of nonempty proper subsets are indexed by

\[
 (K,E)=(1,0),(2,0),(2,1),(3,1),(3,2),(4,3).
\]

The orbit-mass vector

\[
 p=\frac1{153}(0,101,0,16,34,2)
\]

is nonnegative, has total mass one, and satisfies exactly

\[
 E_p\mathcal DK=E_p\mathcal DE=E_p\mathcal DN=0.
\]

Dihedral averaging sends every degree-at-most-two test function to a linear
combination of `1,K,E,N`.  Therefore, if a quadratic `g` obeyed

\[
 \mathcal Dg(A)\ge |A|-\frac{32}{15}
\]

on every proper state, averaging against `p` would give zero on the left
and a positive number on the right, because

\[
 E_pK=\frac{40}{17},\qquad
 \frac{40}{17}-\frac{32}{15}=\frac{56}{255}>0.
\]

Hence no full quadratic certificate exists on `C_5`.

This pseudo-law is not stationary.  The actual stationary orbit masses are

\[
 \left(\frac{10}{39},\frac13,\frac5{39},
       \frac8{39},\frac2{39},\frac1{39}\right),
\]

so the actual mean is

\[
 \frac{80}{39}<\frac{32}{15},\qquad
 \frac{32}{15}-\frac{80}{39}=\frac{16}{195}.
\]

Thus `C_5` is a strict dB suppressor relative to `K_5` at `r=2`; it only
refutes the quadratic proof architecture.

## 3. Exact cubic repair on `C_5`

Let `T_1` and `T_2` count occupied triples inducing respectively one and
two cycle edges.  The symmetric cubic

\[
 g=\frac{-2069K+980E+368N-26T_1-312T_2}{675}
\]

satisfies

\[
 \mathcal Dg(A)\ge |A|-\frac{32}{15}
\]

on every nonempty set, including the transient full state.  In the seven
orbits obtained by adjoining `(5,5)`, the exact slacks are

\[
 \left(\frac{22}{75},0,0,0,\frac{2}{15},0,0\right).
\]

This shows sharply that the `C_5` failure is a degree-two hierarchy failure.
It does not supply a bounded-degree universal proof: on the unit unweighted
atlas, proper-state degree-three certificates already fail on 11 of the 112
connected six-vertex isomorphism classes, while degree four passes all 112.

## 4. Full state versus stationary support

After any geometric-union dual update, the selected occupied target is
absent, because the graph has no self-loops.  Consequently the full state is
transient and has zero stationary mass.  A stationary-density proof only
needs a pointwise certificate on nonempty proper states.  If one nevertheless
wants to constrain the full state, the top Boolean monomial
`prod_i x_i` changes the generator only there and can repair that one
constraint.  Failure caused solely by the full state is therefore not a
substantive stationary obstruction.

## 5. What remains open

* Prove or refute universal feasibility of the edge-supported quadratic for
  the half-density target `2|A|-n`.
* Derive explicit coefficients from `P` if it is feasible.  A useful but
  still numerical reduction is
  `q_ij=a_i P_ij+a_j P_ji`, which passed broad random screens when the
  vertex coefficients were unrestricted; this reduction itself is not
  proved universal.
* Prove or refute the complete-graph mean ceiling at `r=2` by a method that
  uses the full stationary hierarchy.  The `C_5` pseudo-law proves that
  singleton and pair balances cannot suffice, while the complete-graph
  degree barrier proves that no degree bounded independently of `n` can
  suffice for the exact baseline target.

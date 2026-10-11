# Frozen independent source criteria: Markov and closure family

Frozen at 2026-10-04 15:52:18 UTC. Source-first stage; no candidate, PR body,
historical audit, other-family result, or candidate code has been read. These
criteria must not be rewritten in light of the candidate; later comparisons
belong in separate files.

## Authenticated source and scope

Primary source: Steffen Lauritzen, *Two open problems in graphical models of
algebraic nature*, in Oberwolfach Report 55/2022, printed pp. 3125-3126, DOI
[10.4171/OWR/2022/55](https://doi.org/10.4171/OWR/2022/55). Retrieved independently
from the [EMS Press PDF](https://ems.press/content/serial-article-files/46992),
then extracted and visually inspected PDF pages 5 and 6. The EMS publication
record dates publication to 27 July 2023; the workshop occurred in December
2022. The imported source_record.json is curation, not the governing statement.

Local original PDF SHA256:
`56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65`.
Imported source-record SHA256:
`07eea9fc56a9b58a853935ed18d8096c889dedb2fabc01f8d17aa79f20bf6b15`.

The source specifies a finite set V, a simple undirected G=(V,E), and exactly
X={0,1}^V. The probability density is its mass function with respect to counting
measure. Every coordinate is binary with its standard order 0<1. There is no
continuous, infinite, larger-alphabet, almost-everywhere, or weak-convergence
claim in these two conjectures.

## Definitions to preserve

1. P(X) consists of p:X -> [0,1] with sum_x p(x)=1. Support means
   S={x:p(x)>0}; zeros are permitted.
2. M(G) is the **global** Markov model: for every disjoint A,B,C subset V,
   separation of A from B by C implies X_A independent of X_B conditional on
   X_C. Conditional independence has no restriction on a null conditioning
   event. Algebraic marginal-table identities handle those events without
   dividing by zero.
3. M_+(G) is the strictly positive part of M(G).
4. M_F(G) consists of Markov distributions with a finite product over complete
   subsets A of G, p(x)=product_A psi_A(x_A). Singletons are complete; the
   empty subset is complete under the displayed definition as well. The report
   prints psi_A:X_A -> R, **not** R_{>0}. Finite real-valued factors can always
   be replaced by absolute values when their product is p>=0. Therefore a
   constructive proof using finite nonnegative factors meets this definition,
   but a factor allowed to take infinity does not.
5. M_E(G) is the pointwise topological closure of M_F(G), equivalently of
   M_+(G), as defined in the report. Obtaining M_E membership alone does not
   establish M_F membership.
6. M_I(G) is explicitly given in the report by p(x)=product_{e in E} psi_e(x_e),
   with only edge factors. This is broader than the usual strictly positive
   exponential Ising parametrization but narrower than general clique
   factorization.
7. M_2(G) means p in M(G) satisfying **every** inequality
   p(x join y)p(x meet y)>=p(x)p(y), x,y in X, with coordinatewise join and
   meet. The inequalities include zero masses and incomparable x,y whose
   Hamming distance exceeds two.

### Isolated-vertex convention requiring explicit treatment

The literal edge-only formula makes p independent of every isolated coordinate,
with that coordinate uniform after normalization whenever any edge exists.
For a nonempty edgeless V the empty product is 1 on every x and cannot itself
be a probability density. Thus the literal source M_I can be empty there.
The usual pairwise model adds singleton and scalar factors and differs on these
graphs. A candidate may prove the usual formulation and recover the literal
one by imposing uniform isolated coordinates; it must state this step. The
empty graph on V=empty has one configuration and p=1. Treating arbitrary
singleton potentials as automatically part of the displayed source M_I is a
convention change, not source authentication.

## Full success targets

**C1.** For every finite binary G, if p_n in M_I(G) intersection M_2(G) and
p_n(x) converges for each x, then the limit p belongs to that same intersection.
The result must include initially zero masses, newly created zeros, divergent
parametrizations, disconnected graphs, and the isolated-vertex convention.

**C2.** For every finite binary G and every globally Markov MTP2 probability p,
produce or prove existence of finite clique factors giving p exactly, including
on all configurations outside its support. No full-support assumption is
allowed in the target. Establishing the stronger source Conjecture 3 (lattice
support plus global Markov implies clique factorization) would imply C2, but
its proof must be independently checkable.

The source's second topic, Gaussian coordinate descent and its Conjecture 4,
is outside this imported two-conjecture problem.

## Independent deductions: what is and is not the central closure difficulty

On finite X, pointwise convergence is convergence in a finite-dimensional
simplex. Nonnegativity and sum p=1 pass to the limit. For each fixed x,y the
MTP2 inequality is polynomial in p, so MTP2 is closed.

For a fixed separation A,B|C, write p_ABC for the marginal table. The global
Markov statement is equivalent to all identities

    p_ABC(a,b,c) p_C(c) = p_AC(a,c) p_BC(b,c).

Every marginal is a finite sum of p(x); these polynomial identities pass to
the limit, including when p_C(c)=0. There are finitely many separations, so
M(G) is closed. Consequently C1's unresolved content is **exact finite edge
factorization of the limit**, not normalization, MTP2, or Markov membership.

If S is the support of MTP2 p and x,y in S, both meet and join must lie in S.
This only establishes a sublattice, not a Cartesian product or a subcube.
Implication and equality constraints are legitimate support geometry.

## Probabilistic route criteria and exact gaps

| Mechanism | Independently established part | Candidate burden / possible failure |
|---|---|---|
| Pass CI and MTP2 to the limit | Finite polynomial identities and inequalities above | Must still show the limit's edge factorization; invoking closedness of the factor image is circular |
| Select attractive edge factors | For a strictly positive edge factorization, a full two-coordinate conditional cross-ratio isolates the unique edge interaction | Zero slices can mask an edge determinant; existence of a suitable MTP2 factorization for each zero-support input needs proof |
| Compactness of normalized factors | Finite arrays with bounded entries have convergent subsequences | If the product and normalizer both tend to zero, normalized arrays do not directly yield limit factors; gauge choice and a positive limiting normalizer need justification |
| Approximate zero-support p by positive p_n | Positive factorization methods are available in the positive regime | Adding a constant can destroy MTP2 and graphical independence; smoothing must preserve both properties and factor degree |
| Support reconstruction from CI | MTP2 support is a sublattice; graph CI restricts conditional support rectangles | Pairwise CI may be vacuous on thin support; use full source global Markov or prove a zero-support equivalence |
| Marginalize or condition auxiliary variables | Conditioning on a positive-mass event preserves the appropriate MTP2 restriction directly | Marginalization may introduce new graph edges; a marginal MTP2 statement is not the required fixed-G Markov statement |
| Extended model membership | A positive factor sequence establishes M_E | Source distinguishes M_E and M_F; turning closure into actual finite factors is the central unsupported transfer if left unproved |

Any route whose missing lemma is simply C1, C2, or a stronger unsupported
factorization assertion is blocked until a materially new mechanism or proof
is supplied.

## Independent adversarial controls fixed before candidate exposure

1. **All-zero-free baseline:** a positive product distribution on any graph is
   globally Markov and MTP2. It exposes accidental constraints requiring all
   marginal probabilities to be strictly between zero and one in the target.
2. **Structural equality on a path:** p(000)=p(111)=1/2 on path 1-2-3 is
   MTP2, globally Markov, and factorizes using equality edge indicators with
   a finite constant. Logarithms must be restricted to its support.
3. **Pairwise/global distinction:** the same two-point equality law on a
   three-vertex edgeless graph obeys every full-conditioning pairwise CI
   (the remaining coordinate determines both), but not global Markov, since
   different singleton variables are marginally dependent.
4. **Adjacent-square test failure at zeros:** p(001)=p(110)=1/2, zero elsewhere,
   has zero determinants in every elementary two-coordinate square but is
   not MTP2: the meet 000 and join 111 have zero mass. Thus a claimed local
   square test needs strict positivity or an independently proved support
   condition.
5. **Naive smoothing failure:** unnormalized two-variable product weights
   (p00,p01,p10,p11)=(2,4,1,2) are MTP2. Adding epsilon>0 gives determinant
   (2+epsilon)^2-(4+epsilon)(1+epsilon)=-epsilon. Normalizing cannot repair it.
6. **Clique versus edge distinction:** on complete K3, positive weights
   exp(k*x1*x2*x3), k>0, are MTP2 and Markov. The nonzero third-order mixed
   log difference prevents an edge-only representation. C2 is clique
   factorization, not an assertion that all MTP2 laws are Ising.
7. **Boundary graph controls:** V=empty; one isolated vertex; a single edge;
   an edge plus an isolated vertex; disconnected components; complete K3;
   path and a chordless cycle. Test distributions concentrated at a single
   state as well as strict-positive laws and nonsubcube lattice supports.

No numerical scan can prove universal C1 or C2. Exact enumerations are controls
for definitions, lemmas, and implementation, subordinate to a complete proof.

## Status at freeze

Source authentication: complete. Strongest independently verified statements:
finite-normalization closure, MTP2 closure, global-Markov closure, and the
support sublattice deduction. The exact remaining audit gap is candidate
proof of finite edge factorization in C1 and finite clique factorization in C2.
Best-guess completion of the eventual full Markov/closure audit: **20%**.
No candidate assessment or novelty claim has been made.

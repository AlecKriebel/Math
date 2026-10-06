# Independent homological-family seal

Sealed reconstruction prepared 2026-10-01 at 22:19 UTC. Target: PR 27, exact Git head
`84d7f6103b087e431d7afb751501380ebd7ffd42`. This note precedes all reading of
the original PARTIAL, review reports, computation scripts, or other agents'
reports. Only the root assignment, AGENTS.md, and the literal primary source
have been consulted. Its bytes will remain fixed; later corrections will be
recorded separately.

## Source and actual success criterion

Dan Petersen's Question 13 occurs on printed page 118 (PDF page index 75) of
Oberwolfach Report 2/2018, DOI 10.4171/OWR/2018/2, source body
https://ems.press/content/serial-article-files/46724. The hypothesis is finite
dimensional complex vector spaces E and V, the unital square-zero commutative
algebra A=C⊕E, and the free ordinary Lie algebra L=Lie(V). The requested answer
is the homology of L⊗A, expressed as a sum of polynomial functors in E and V.
The mention of dim(E)=1 as calculable by hand does not restrict the question.

An adequate full answer therefore needs the actual homogeneous polynomial
functors, with evaluated multiplicities, for arbitrary E and V and all homology
and tensor degrees. A reduction to unevaluated equivariant kernels or cokernels,
or an Euler-characteristic identity, is useful partial work but does not meet
that criterion. I make no inference about worldwide current openness, novelty,
or later literature from this 2018 statement.

## Independently derived universal mechanism

Write M=L⊗E. The bracket induced by A gives L⊗A=L⋉M, with M abelian and
L acting on M by the adjoint action on the first factor. As vector spaces,
Λ^r(L⊕M)=⊕_{p+q=r}Λ^pL⊗Λ^qM. In the Chevalley–Eilenberg differential, an
L–L bracket lowers p by one and preserves q; an L–M bracket also lowers p by
one and preserves q; an M–M bracket vanishes. Thus this is a direct sum of
chain complexes indexed by q, each the coefficient CE complex
C_*(L;Λ^qM), shifted by q. This proves the full, natural direct sum

H_n(L⋉M)=⊕_{q=0}^n H_{n-q}(L;Λ^qM).

This is stronger than merely quoting collapse of a two-column spectral
sequence: the chains already split by the number q of ideal factors. The
scalar action E→tE gives weight q, so the summands are distinguished naturally.

The universal enveloping algebra of L is the tensor algebra T(V). For the
trivial RIGHT T(V)-module C, an explicit free resolution is

0→V⊗T(V)→T(V)→C→0,  v⊗a↦va.

The map is right linear and bijects V⊗T(V) with the augmentation ideal by
removing the first letter of every nonempty word. Tensoring with any LEFT
T(V)-module W gives V⊗W→W, v⊗w↦v·w. Therefore coefficient homology vanishes
in degrees greater than one; H_0 is the cokernel and H_1 is the kernel. Using
the left-module trivial resolution instead requires the opposite tensor order
and corresponding right-module action; mixing these conventions is invalid.

Put W_q=Λ^q(L⊗E) and δ_q:V⊗W_q→W_q. Then for n≥1,

H_n(L⊗A)=coker(δ_n)⊕ker(δ_{n-1}),

and H_0=C. The first term has E-weight n, the second E-weight n−1. The action is

v·((x_1⊗e_1)∧...∧(x_q⊗e_q))
=Σ_i (x_1⊗e_1)∧...∧([v,x_i]⊗e_i)∧...∧(x_q⊗e_q).

There is no extra Leibniz sign in this degree-zero action. Signs appear when
one reorders factors of the ordinary exterior power or compares CE ordering
conventions. In particular, δ_0:V⊗C→C is zero.

Over C, the exterior Cauchy decomposition is

Λ^q(L⊗E)=⊕_{λ⊢q}S_λ(L)⊗S_{λ'}(E).

The transpose on E is essential. Since the L action commutes with permutations
and E maps, δ_q acts componentwise through
D_λ:V⊗S_λ(L)→S_λ(L), the diagonal adjoint action. This gives an exact,
natural E-Schur reduction of both terms of H_n. It does not evaluate their
V-Schur multiplicities. Exact symmetric-group coinvariants in characteristic
zero justify passing homology through Schur realization; this would need
substantial changes in modular characteristic.

## Boundary and finiteness falsifiers

* E=0: recover H_0(L)=C, H_1(L)=V, and H_n=0 for n>1.
* V=0: L=0, so H_0=C and all positive homology is zero.
* dim(V)=1: L=V is abelian and the action on M is zero. Every δ_q is zero,
  and H_n=Λ^n(V⊗E)⊕V⊗Λ^{n-1}(V⊗E), precisely Λ^n(V⊗(C⊕E)).
* H_1 in general is V⊕(V⊗E), since L/[L,L]=V.
* Grading L=⊕_{d≥1}L_d(V) makes each fixed V degree finite dimensional. The
  degree-d δ_q has domain V⊗(W_q)_{d-1} and target (W_q)_d. No topological
  completion or product over degrees is warranted by the source.
* Each q is finite in a fixed homology degree, but V degrees are unbounded.
  The polynomial decomposition is an ordinary locally finite direct sum;
  total H_n need not have a single finite polynomial degree.
* [coker D_λ]−[ker D_λ]=[S_λ(L)]−[V⊗S_λ(L)] in the graded Grothendieck group.
  This virtual identity alone cannot determine the two actual modules or
  their nonnegative multiplicities. An unjustified injectivity or
  surjectivity assertion would transfer the central difficulty to a new claim.

## Independent audit plan and estimate

The principal falsification targets are CE splitting and signs, wrong-side
tensor resolution, omitted E weights, untransposed Cauchy partitions,
unevaluated multiplicities promoted to a full answer, and computations that
only agree because they mirror the same implementation. I will separately
replay frozen original receipts and construct checks comparing full CE
homology with the reduced two-term formula, using exact rational arithmetic.

Current completion estimate: 20% of this independent audit. The source-level
reconstruction is complete; no packet correctness conclusion has been drawn.
The derivation above is partial toward the source's full discovery criterion:
the exact remaining mathematical gap is evaluated V-Schur multiplicities of
the D_λ kernels and cokernels, uniformly in q and V degree.

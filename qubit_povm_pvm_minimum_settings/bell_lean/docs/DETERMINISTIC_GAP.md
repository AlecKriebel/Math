> **Historical cloud-stage document.** Statements below about missing compilation or unfinished targets describe the incoming archive. Current local verification and the precise certified scope are recorded in [CERTIFICATION.md](../CERTIFICATION.md); this document is retained as research provenance.

# Deterministic-gap shortcut: reconstructed source and exact checks

## Status

`Bell/DeterministicGap.lean` is a new reconstruction of the shortcut recorded in
the preceding conversation, not recovered bytes from that conversation's working
directory. Its eight theorem declarations are **uncompiled proof attempts**.
`stationary`, `hnull`, `hfuture`, and `strictGap` are explicit hypotheses. Nothing
in this module proves the universal two-input equality or supplies those physical
and analytic hypotheses by assumption-free theorems.

The independent checker `scripts/deterministic_gap_checks.py` passes 230 named
polynomial identities: 50 null/action/gap identities and 180 declared-table
identities. It uses arbitrary real coefficient variables and a general bilinear
form satisfying the five null conditions, without assuming symmetry. A transpose
mutation is rejected. These are symbolic algebra checks, **not Lean verification**.

## Algebra

Use the coefficient rays

    r0=e0, r1=e1, r2=e2, r3=e3, r4=(1,1,-1,-1), u=(1,1,0,0).

Their input blocks are {0,1} and {2,3,4}. Define five linear maps by

    T0(x)=(x0,x0,x2,x3)
    T1(x)=(x1,x1,x2,x3)
    T2(x)=(x0+x2,x1+x2,0,0)
    T3(x)=(x0+x3,x1+x3,0,0)
    T4(x)=(x0,x1,0,0).

Each Tj maps rj to u, other rays in that same block to zero, and the other
block's rays to themselves. Also Tj(u)=u and Tj²=Tj.

For B with B(rk,rk)=0, put Cλ(W)=Σk λk B(rk,W(rk)). Then

    Cλ(I)=0,        Cλ(Tj)=λj B(rj,u).

Suppose the linear score F satisfies the stationary identity

    F(W)=α l(W(u))−2 Cλ(W)

for a linear covector l and every W. The normalized term cancels because
Tj(u)=u, leaving

    F(I)−F(Tj)=2 λj B(rj,u).

Consequently strict deterministic gaps F(Tj)<F(I) and B(rj,u)>0 imply λj>0.
No semidefinite duality theorem is required for this implication. This does NOT
remove the need to derive the stationary identity from physical maximality.

## Why the deterministic comparison is physical

In the binary/ternary coefficient convention, the table of a block P is
p(a,b|x,y)=e(x,a)^T P e(y,b), where the unused third binary effect is zero.
P Tj describes the measurement with identity at the selected label and zero
at every other label of that input, with Bob's other input unchanged. The
180 symbolic table checks retain both input choices and all three declared
labels, including the padded zero label.

A deterministic Bob input plus one nontrivial Bob input is local. To see the
same-hidden-variable construction explicitly, write the other-input table as
p_x(a,b), with nonsignalling marginal q_b=Σa p_x(a,b). For q_b>0 assign weight

    w(b,(a_x)_x)=q_b ∏x [p_x(a_x,b)/q_b].

For q_b=0 set this weight to zero; nonnegativity then forces p_x(a,b)=0 for
all x,a. Summing over all assignments gives total weight one, reconstructs
every other-input entry, and also reconstructs each Alice marginal in the
deterministic-input block. Every hidden assignment is realizable by qubit PVMs
using identity/zero effects. Thus the complete table belongs to the shared-
randomness PVM hull, not merely a collection of separately simulated marginals.

At a strict separator above the entire physical PVM hull, every such replacement
has strictly smaller score. In the intended physical coordinates, positivity of
B(rj,u) comes from the nonzero positive effect and nonsingular state coefficient
matrix. Establishing these physical coordinates and stationarity, with all their
regularity hypotheses, is still part of the missing formalization.

## Verification command

    python3 scripts/deterministic_gap_checks.py

The Lean source is included in `Bell.lean` for the next real compiler build.
Its successful text audit does not establish elaboration or kernel acceptance.

# Attempt 1: scalar trace on the base

## Objective
Recover a nonzero base Chern-class pairing by averaging curvature, then test whether the exact jet hypothesis supplies the required tensor.

## Retained proposition
If a compact Kähler manifold (X,omega), of complex dimension n>=1, has strictly negative holomorphic sectional curvature, then c1(T_X)_R≠0.

## Proof
At a point take a unitary frame. Choose the curvature sign convention in which
H(v)=sum R_{i bar j k bar l}v_i bar(v_j)v_k bar(v_l)
for unit vectors v, and the Ricci form represents 2pi c1(T_X). Set S=sum_{i,k}R_{i bar i k bar k}.

For normalized unitary-invariant measure on the unit sphere in C^n, phase invariance makes the fourth moment zero unless the unbarred and barred indices pair. Permutation invariance gives E(|v_i|^4)=a and E(|v_i|^2|v_j|^2)=b for i≠j. Rotating (v_1,v_2) to (v_1+v_2,v_1-v_2)/sqrt(2) gives a=2b; expanding (sum |v_i|^2)^2=1 gives na+n(n-1)b=1. Consequently

E(v_i bar(v_j)v_k bar(v_l))=(delta_ij delta_kl+delta_il delta_kj)/(n(n+1)).

(The same formula for n=1 is immediate.) Kähler curvature symmetry identifies both contractions, so E(H)=2S/(n(n+1)). Thus H<0 on every complex line forces S<0 at every point.

The trace-wedge identity is S omega^n=n Ric(omega) wedge omega^(n-1), with consistent curvature normalization. Hence

integral_X S omega^n=2pi n integral_X c1(T_X) wedge omega^(n-1)<0.

A zero real Chern class has zero pairing with the closed form omega^(n-1), a contradiction. This uses compactness to integrate and Kählerness for both the curvature symmetries and closedness. It proves the proposition.

## Why the general attempt stops
For k=1 a tautological metric induced by a base Kähler metric meets the setting above. An arbitrary jet metric in the question need not be induced by any Hermitian metric on T_X, much less by a Kähler metric. For k>1 it lives over a different base X_{k-1}. We have not constructed a base curvature tensor satisfying the Kähler identities whose holomorphic sectional curvature is controlled by the given alpha|V_k. Averaging a form on the tower does not supply that missing construction.

## Exact control
The constant-holomorphic-curvature algebraic tensor R_{i bar j k bar l}=-(delta_ij delta_kl+delta_il delta_kj) has H=-2 and S=-n(n+1), confirming the factor 2/[n(n+1)]. The verifier checks this identity coefficientwise for n=1,...,6.

This is the familiar Kähler subcase already motivated in the 2012 report, with the averaging and integration written out here. It is not a solution for arbitrary nondegenerate negative k-jet metrics.

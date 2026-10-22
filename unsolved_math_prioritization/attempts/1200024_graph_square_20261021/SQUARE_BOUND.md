# Exact square upper bound

Let T be the 3-regular tree, fix an end ξ, and let p(v) be the neighboring vertex toward ξ. Let G have unordered edges {v,p(v)} and {v,p²(v)}. All conductances are one. Let H=G² be the simple graph square, joining distinct vertices at G-distance at most two.

## Finite subgraph and complete root neighborhood

Take the radius-10 T-ball about o. Its rooted-tree word coordinates have three choices at the first step and two choices thereafter. Choose the distinguished end represented by the all-zero ray. The parent toward ξ of an all-zero word is its zero extension; the parent of any other word is its prefix with the last letter removed. The sole absent parent is that of the all-zero boundary word.

Let K be the G-subgraph on this ball, with all parent and grandparent edges having both endpoints in the ball, and let J=K². Since every length-two K path is a G path, J is a subgraph of H. No spurious edges are introduced. Any H-neighbor of o is joined by a G path with at most two edges, hence by a T walk with at most four edges; this entire walk lies in the radius-4 T-ball. Thus J contains every H-edge at o. Exact enumeration gives 40 such neighbors. The certificate verifier generates the graph independently from word coordinates and verifies its complete edge list, with 3,070 vertices and 19,931 edges.

## Exact flow witnesses

For each of these 40 neighbors v, the supplied certificate gives a finitely supported rational unit flow from v to o on J. The common denominator is D=10^9. The standard-library verifier checks every numerator is an integer and checks divergence exactly: +D at v, −D at o, and zero at every other vertex. It then sums the integer squares of all edge-flow numerators, once per undirected edge. The exact sum of energies over all 40 unit flows is

3208526010913748780 / 1000000000000000000 < 321/100.

Floating-point sparse solves were used only to find witnesses. A spanning-tree integer correction makes each witness exactly feasible. Neither the solve nor any floating-point calculation is trusted by the replay verifier. The exact checker uses explicit errors, not Python assert, and passes both normal and optimized execution.

## Transfer to the free uniform spanning forest

For a finite unit-conductance graph, Thomson's principle gives R_J(o,v) no larger than the energy of its certified unit flow. For a free exhaustion of H eventually containing J, Rayleigh monotonicity gives R_{H_n}(o,v) ≤ R_J(o,v). Taking the free limit, R_H^F(o,v) ≤ R_J(o,v). Kirchhoff's marginal formula and passage to the free exhaustion give P({o,v}∈FUSF_H)=R_H^F(o,v). Sum over the complete set of 40 neighbors:

E[deg_FUSF(H)(o)] ≤ 3208526010913748780/10^18 < 3.21.

This is a free-resistance UPPER bound, not a wired-resistance lower bound. The finite flow is permissible in each sufficiently large free finite network. No approximation to an infinite wired network enters the argument.

## Certificate

square_flow_certificate.json.gz, SHA-256 6573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f, 165241 bytes. Run python verify_square_certificate.py from any directory. The verifier is independent of scipy and of the numerical construction script.

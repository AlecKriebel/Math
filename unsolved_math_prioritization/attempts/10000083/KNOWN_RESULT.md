# Exact scope certificate

## Target and convention

For a finite, undirected, unweighted, loopless simple graph G with n vertices,
let (X_t) be discrete-time simple random walk and let tau_cov be the first
integer t for which {X_0,...,X_t}=V(G). Interpret a real deadline Cn as
floor(Cn). The intended target is exponential smallness, uniformly in G and
the initial vertex or initial distribution, for each fixed C>0.

## Imported theorem and implication

Dubroff–Kahn's [Theorem 1.1](https://arxiv.org/html/2109.01237v2)
gives a positive exponent depending only on C. Their Usage paragraph assumes
n sufficiently large. Thus there exist epsilon(C)>0 and n_0(C) such that

    P(tau_cov <= floor(Cn)) < exp(-epsilon(C) n),  n >= n_0(C).

Set c(C)=exp(-epsilon(C)). This supplies the requested exponential base.
The theorem permits any initial law. Disconnected graphs cannot be fully
covered by one walk and hence have probability zero. If isolated vertices
need a transition convention, make each one absorbing.

The final journal publication is [Annals of Probability 53(1) (2025), 1–22](https://doi.org/10.1214/24-AOP1699).
The preprint was submitted in September 2021 and revised in November 2021.
The difficult uniform bound is wholly credited to Dubroff and Kahn.

## Necessary finite-size correction

The catalogue instead quantifies over every n with no threshold or prefactor.
Take C=1 and G=K_2. From either starting vertex the walk reaches the other
vertex deterministically at time 1. Its cover probability by time Cn=2 is 1,
whereas c^2<1 for every 0<c<1. Consequently that literal statement is false.
With the usual time-zero convention, the one-vertex case also has cover
probability 1. These are boundary checks, not a claimed new mathematical
resolution or a criticism of the paper's explicit large-n convention.

A clean corrected catalogue statement adds n>=n_0(C). An equivalent all-n
form permits a prefactor A(C): P(tau_cov<=floor(Cn))<=A(C)c(C)^n. Indeed,
choosing A(C)=c(C)^(-n_0(C)) covers smaller n trivially and preserves the
large-n bound. This conversion is elementary and supplies no quantitative
estimate on the constants.

## Scope exclusions

This certificate does not claim a useful optimal exponent, a theorem for
arbitrary weighted or directed chains, or resolution of Benjamini's separate
vacant-set Conjecture 4.1. It imports the published theorem rather than
reconstructing or formally verifying its full proof. No new campaign proof
turn is charged for source identification and this boundary audit.

# Root qualification of imported background proofs

2026-10-02 UTC. Root directly inspected the university-hosted v4 printed
page21 as pixels after reading the operative proof text. The published
finite-moment obstruction remains usable with the following explicit proof
clarifications. These clarify a background import; they do not solve the
bounded-duration target or change the submitted approximation theorem.

In Theorem5.3, an active original piece ends with a forward unit increment
+c_j. The text defines Y(t)=X(S-t)-X(S) and then uses a +c_{m+1} backward
increment. The terminal increment in that sign convention is instead -c_j.
Under the hypothetical Brownian backward half, replace Y by

    Ytilde(t)=X(S)-X(S-t).

This is also Brownian by global deterministic reflection, and its reversed
terminal unit increment is +c_j. This reflection concerns the entire
hypothetically Brownian half; it does not assume invariance of an asymmetric
stopped-pair joint law.

The equality-hit argument also needs a starting-level qualification. Put
D_m=sum_{i=1}^{k_1+...+k_m}T_{-i} and r_m=u_m+m. Choose the freely selectable
c_j strictly increasing to infinity, in addition to the source's finite-window
probability bounds. Outside {S>=m}, {S<=-D_m}, and {D_m+1>=u_m}, the first
active piece beyond block m has terminal time -D_m (intervening inactive
pieces have duration zero). At a time in [1,r_m), Ytilde(t)-Ytilde(t-1) equals
c_j>=c_{m+1}. Continuity supplies a hit of c_{m+1} after time1 when
Ytilde(1)<c_{m+1}. If the increment curve already starts above that level,
an exact equality hit is not forced by its later value. Therefore the complete
upper bound for the equality-hit tail includes the extra term

    P(Ytilde(1)>=c_{m+1}).

Under the hypothetical Brownian law, that term is a Gaussian tail and tends
to zero. The other three terms tend to zero as in the source: S is finite,
D_m tends to infinity almost surely, and the chosen duration-tail probability
is at most2^{-m}. The source's construction gives the same Brownian hit-tail
a lower bound1/2, so the contradiction survives. Finite moments of each active
moving-unit-increment hit follow, for example, from independent disjoint pairs
of integer unit increments: below/above level samples have a fixed positive
probability and continuity forces a crossing, giving a geometric time
majorant. Rare independent activations and k_j=ceil(1/p_j) provide uniform
specified moments and infinitely many active duration-at-least1 pieces.
Their durations have no common deterministic bound; this is no counterexample
to Problem8.

Theorem5.2's scanned/extracted separation coefficient is
c_1(sqrt(beta/2)-sqrt(beta)/2), which is positive when c_1,beta>0. A text
extraction that renders both radicands identically loses that distinction;
the exact v4 TeX source was inspected by the independent primary family.
Root relies on this explicit distinction, not the ambiguous extraction.

The earlier ROOT_PARTIAL_SCOPE_CERTIFICATE and read ledger accurately record
which primary proofs root read. They are retained as dated records. They
must be read with this addendum rather than interpreted as certifying every
literal printed step without qualification. The current package must retain
this addendum and the independent source-family derivation. Original2/5,
new0/audit0; no new solution, novelty, paper, DOI or tracker claim.

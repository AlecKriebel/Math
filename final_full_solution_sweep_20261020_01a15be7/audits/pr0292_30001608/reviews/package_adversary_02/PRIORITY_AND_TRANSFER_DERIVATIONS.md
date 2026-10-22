# Independent model and prior-theorem transfer challenges

These deductions were made from the actual primary protocol definitions and the
displayed DFC generator. They are not historical absence claims. Third-party
bodies retained in `private_sources/` are private reading copies and must not be
redistributed with this review.

## Editions and exact source identity

The 2009 arXiv v1 Figure 2 gives exactly the two lambda/2 arrivals and four rates
in the candidate. Its Conjecture 3.4 predicts high-load instability. The official
OWR 48/2010 contribution, printed 2782–2783, instead conjectures stochastic DFC
stability. The January 5, 2011 author proof, Section 3.2 and Figure 2 on author
page 10, expressly explains the invisible empty waiting rooms. Conjecture 3.6 on
author page 12 predicts stability. Section 2 defines stability as irreducible
positive recurrence in continuous time and distinguishes large-system scaling
from fixed-arrival accelerated-time fluid scaling. The HAL cover's 2013 deposit
date is distinct from the proof-header date and the 2011 publication date.

I visually inspected the actual rate diagram and conjecture pages. The simulation
footnote uses constant holding times; it is historical empirical motivation and
cannot prove physical-time positive recurrence. The candidate does not use that
footnote as a clock equivalence. The final Springer body remains uninspected;
the publisher preview and bibliographic record do not establish body equality.

## Common Chunk: explicit generator obstruction

The complete Allerton 2012 body was read and all five pages were rendered and
visually inspected. Section II samples with replacement from the whole population,
including empties, self and the permanent seed. Section III requires a rare match
for empty peers and protects the final download: every already-held chunk must
appear at least twice in the sample of three. Theorem 4.3 proves that algorithm's
stability. Its conclusion's remaining rare-chunk conjecture concerns a different
rule, not DFC.

With one singleton carrying chunk one and the seed, every sample carries chunk
one, and the singleton completes iff at least one sample is the seed. Its rate is
`1-(1/2)^3=7/8`, versus DFC's `1/2`. With just one empty peer and the seed, a first
download is possible iff exactly one sample is the seed, giving `3/8`, versus
DFC's `1`. These two ratios exclude a constant clock identification. Positive
constant arrivals exclude a nonconstant common clock multiplier as an exact
generator identification at any fixed arrival parameter.

More generally, M empty peers and the seed have total first-download intensity
`3 M^3/(M+1)^3 < 3` under Common Chunk and `M` under DFC. The seed-upload difference
is substantive. Forgetting the DFC first choices does not repair the mismatch:
`(2,0,1,0)` and `(0,2,1,0)` have the same `(a+b,x,y)` but A-to-X rates 2 and 0.
The proposed aggregation is not strongly lumpable.

## Actual Allerton Foster function fails directly under DFC

For two chunks, the operative high-load Allerton function becomes `C W+H`, with

    H = S [r^(x+1)+r^(y+1)+r^(a+b)],
    S=a+b+x+y+1, r=exp(-1), W=2(a+b)+x+y.

Take lambda=1 and state `(1,0,M,1)`. The aggregate arrivals have rate 1; the A
download and Y departure each have rate `(M+1)/(M+2)`; the X departure has rate
`2M/(M+2)`. Dividing the H increments by M gives, respectively, the limits

    r^2-r, 1-r, r-r^2, 0.

Thus `L_DFC H/M -> 1-r>0`. Meanwhile `L_DFC W=-2+6/(M+2)`, so for every fixed
finite C, `L_DFC(CW+H)/M -> 1-r`. The source's actual function is not already an
all-load DFC certificate. This excludes this direct function/theorem transfer,
not all possible future adaptations of its ideas. The numerical transfer control
in the candidate is only a diagnostic for this analytic limit.

## Older two-chunk minority-rule proof also fails to transfer directly

Oguz's 2012 Berkeley technical report, Chapter 3.4, studies invisible empties but
samples three peers to choose a rare first chunk; its seed is interpreted as a
random singleton for that choice. It has one empty class z rather than two
committed classes. Its first-download rates contain `(x+1/2)(y+1/2)` factors, so it
does not have the DFC generator. Its potential is

    Phi=2z+2(x+y+z)+(x-y)^2.

On DFC with z=a+b, lambda=1, and `(a,b,x,y)=(M,0,M,0)`, direct calculation gives

    L_DFC Phi = 4 + M(2M-1) - M(2M+1)/(M+1),

which is positive for all sufficiently large M and is asymptotic to `2M^2`.
Thus that operative older potential also fails directly. The same report's
Chapter 4 uses Common Chunk and the Allerton-type potential above. I read the
complete operative two-chunk proof and its protocol definitions; I do not claim
a complete new review of the entire thesis.

## Reaction-network theorem, Zenodo 22089551

The parent supplied this as a new lead after the independent initial derivation.
I independently fetched the public record and actual v1.2.4 paper. Its Theorem
2.1 concerns finite, weakly reversible, one-linkage, bimolecular stochastic
mass-action networks. The exact DFC rates are rational rather than mass action.
Multiplying the physical generator by D clears the denominator and gives a
bimolecular realization. In particular, `a(x+1)` requires

    A -> X,  A+X -> 2X,

and `b(y+1)` requires the corresponding Y channels. The remaining channels are
`0 -> A,B`, `X -> X+A,X+B`, `Y -> Y+A,Y+B`, `X -> 0`, `Y -> 0`, and
`X+Y -> X,Y`, with the appropriate positive coefficients. The resulting graph
has 14 channels and 12 complexes. It is not weakly reversible: `2X` is a sink
with an incoming edge from `A+X`.

This obstruction is not cured by another nonnegative mass-action realization on
the same coordinates. An ax term in the `(-1,0,1,0)` jump intensity forces a source
`A+X` and target `2X`. Every nonnull outgoing channel with source `2X` would add a
positive `x(x-1)` off-diagonal rate. None exists in the target generator, and
nonnegative rates cannot cancel it. Null self-channels do not create a directed
return path. Auxiliary hidden species or a different projection would require a
new theorem, including a valid Markov projection and recurrence transfer.

There is a separate clock issue: if the accelerated chain `L'=D L` has stationary
law pi', the formal stationary candidate for L is proportional to `D pi'`; it
requires `E_pi' D < infinity`. Positive recurrence alone does not imply that
unbounded moment. The actual reaction-network paper explicitly separates
unbounded moments from its recurrence conclusion. Hence its theorem is not an
existing DFC all-load result. This review does not audit that paper's full proof.

## Bounded conclusion

The fresh exact-name, conjecture, DOI, two-chunk recurrence and protocol-family
searches did not authenticate an earlier all-load DFC theorem. Later Group
Suppression and Mode Suppression primary texts have different finite seed-upload
and suppression rules; only their operative model/theorem sections were read
here. No inference about every ancillary statement in those papers is made.
The final 2011 Springer and final 2015 journal bodies remain uninspected. Their
absence neither proves duplication nor proves absence of an exact result.

The actual candidate confines itself to a bounded historical-conjecture
contribution and explicitly disclaims worldwide firstness, continuing openness
and a new general Foster method. That scope is proportionate to the checked
evidence. The simple small-load Foster deduction is credited. No surviving
priority objection requiring a repair to this candidate was found.

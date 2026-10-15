# Independent reconstruction before peer reports

2026-10-12: Original frozen PR462 / problem30005528, head
3d5701d67e18745715d384c3db3fbee588b42a98. Zero new original proof-search
attempts. This note records my own deductions after inspecting the frozen
proof and complete primary printed pages, before reading the peer reports.

The literal Question1 on OWR22/2023 printed1254 permits arbitrary ordered
pairs, an infinite compact topological alphabet and continuous strictly
positive symbol size. Its average counts N+1 symbols and divides by N.
It imposes neither reversal symmetry nor a structured packing realization.

For the submitted circle-times-height map, every legal word is forced by the
graph relation to be one orbit. Height t is fixed, so its prefix average is
(1+1/N)(1+t), and every orbit has limit1+t. The bottom has irrational
rotation, hence no periodic points. A point has period p precisely when
p(alpha+t) is an integer, because its circle coordinate is nonzero. This
also implies strict positive height for every periodic sequence. Invertibility
excludes eventual periodicity at the bottom. Dense rational angles give
nonvacuous dense periodic competitors. For alpha=sqrt2, rationalization
of a reduced rational angle p/q gives a positive integer numerator p^2-2q^2
and the stated uniform bounded-period lower bound. I found no mathematical
gap in these universal claims.

Independently inspected Bousch2000 printed492 and501 supply an irrational
Sturmian compact invariant infinite minimal Cantor support K for circle
doubling D. Set Sigma=circle, T=graph(D), s=1+distance(x,K). Closedness and
continuity are immediate. Every word is a D-orbit and every prefix average
is at least1+1/N, while points in forward-invariant K have average exactly1.
A periodic point in K would have a finite nonempty closed invariant orbit,
contradicting minimality of infinite K. Thus every periodic finite orbit is
disjoint from closed K; its positive finite mean distance gives cost>1.
This covers all legal words and all periods without a measure-average gap.
Density of circle-doubling periodic points follows from k/(2^p-1).

Separately Jenkinson2006 printed384 Theorem1 and printed385 Corollary1
supply a continuous potential f for doubling uniquely maximized by
Lebesgue probability lambda. Taking C=1+max(f), s=C-f is positive. Every
weak limit of normalized orbit empirical measures is invariant, by
telescoping continuous test functions. Consequently every cluster value
of cost averages is at least C-integral(f,lambda). A lambda-generic point
attains that value. Every periodic empirical measure is distinct from
lambda and has strictly smaller f-integral, hence larger cost. The original
N+1 convention differs by a bounded endpoint divided by N. For a general
orbit A=C-liminf f-averages; replacing liminf with limsup would be wrong.
This route is existential and claims no explicit closed formula for f.

These are checkable implications of published older statements. They do
not establish an earlier explicitly printed answer to the 2023 numbered
question, first-solver attribution, novelty of the exact annulus example,
or a solution of the structured packing conjecture.

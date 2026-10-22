# Known affirmative answer: Green-potential and positive-harmonic covering

## Target

Write D={z in C: |z|<1}. For each nonnegative Green potential u on D normalized by u(0)=1, and also for each positive harmonic u with that normalization, the question asks for a universal function g tending to zero such that {u>t} has a disk cover whose radii sum is at most g(t).

The primary problem source is Hayman and Lingham, arXiv:1809.07200v2, printed p.67, Problem 3.23. Its Update 3.23 states the affirmative answer with g(t)=1 for 0<=t<=28 and g(t)=27/(t-1) for t>28, attributing the result to Govorov via Eiderman. This packet gives a deduction of exactly that bound, rather than a novelty claim.

## Imported theorem and evidence level

Use the whole-unit-disk case of Govorov's theorem as restated in V. Ya. Eiderman, Estimates for potentials and delta-subharmonic functions outside exceptional sets, Izv. Math. 61:6 (1997), 1293-1329, Theorem 4.2 and the paragraph immediately following it, printed p.1315.

The needed statement is: if v is subharmonic in D, its actual supremum M is finite and positive, and v(0)>0, then for each P>1 there is an at most countable family of disks with sum of radii at most 1/P, outside which v>=-9PM throughout D.

The covering theorem is an explicit external premise, not independently reproved here. This public derivative supplies citations and theorem hypotheses, but no source-retrieval evidence. The derivative review does not claim a fresh source inspection. In particular, it does not certify an image-level reading of Eiderman or an inspection of Govorov's original proof. SOURCE_AUDIT.md states the resulting limits.

## Deduction

In fact the same deduction applies to every nonnegative superharmonic function u on D with u(0)=1, using the standard convention for Green potentials of nonnegative measures.

If 0<=t<=28, the single open disk D itself is a cover and its radius is 1.

Fix t>28. Set L=t+1 and define

  u_L=min(u,L),       v=2-u_L=max(2-u,2-L).

Since -u is subharmonic, the maximum of the two subharmonic functions 2-u and the constant 2-L is subharmonic. Thus v is subharmonic. This truncation is finite-valued even at points where u=+infinity. Moreover, v(0)=1 and 0<=u_L<=L, so the actual supremum

  M=sup_D v

satisfies 1<=M<=2. No assertion that M equals 2 or is attained is needed. The imported theorem therefore applies with

  P=(t-2)/18 > 1.

It gives an at most countable family of disks whose radii have total at most

  B=1/P=18/(t-2).

Outside their union, v>=-9PM, hence

  u_L=2-v <= 2+9PM <= 2+18P = t.

Since L>t, the equality of sets {u_L>t}={u>t} holds pointwise, including at infinite values of u. Therefore the disks cover the entire target set, without any exceptional polar set and without taking a limit of disk families.

Finally,

  27/(t-1) - 18/(t-2)
    = 9(t-4)/((t-1)(t-2)) > 0.

Thus B<g(t). If the imported disks are closed and the target requires open disks, let delta=(g(t)-B)/2>0. Enumerate the nonempty family by k=1,2,... (or a finite initial segment) and increase the kth radius by delta*2^(-k). The open enlarged disks cover the original closed disks; their radii sum is at most B+delta<g(t). An empty family needs no modification. Hence either disk convention satisfies the required budget.

Both original classes are included: a nonnegative Green potential is superharmonic, and a positive harmonic function is superharmonic. The same g works for all u in either class, every t>=0, and g(t) tends to zero as t tends to infinity.

## Scope of conclusion

This is the previously known affirmative covering result. The imported covering theorem is the sole non-elementary premise. The computation script checks the parameter identities and budget margin only; it is not a formal verification of potential theory or an independent mathematical review.

## Public references

- W. K. Hayman and E. F. Lingham, Research Problems in Function Theory, arXiv:1809.07200v2, draft dated 21 September 2018: https://arxiv.org/pdf/1809.07200v2
- V. Ya. Eiderman, Estimates for potentials and delta-subharmonic functions outside exceptional sets, Izv. Math. 61:6 (1997), 1293-1329: https://www.mathnet.ru/eng/im166 ; DOI https://doi.org/10.1070/IM1997v061n06ABEH000166
- Public author-copy link: https://www.researchgate.net/publication/314806417_Ocenki_potencialov_i_delta-subgarmoniceskih_funkcij_vne_isklucitelnyh_mnozestv
- N. V. Govorov, The estimation from below of a function that is subharmonic in a disk, Teor. Funktsii Funktsional. Anal. i Prilozhen. 6 (1968), 130-150. See Hayman-Lingham reference [345] and Eiderman reference [4]; original proof is not independently verified here.

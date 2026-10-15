# PR833 / 30003711: integrated mathematical audit

2026-10-15 UTC. Frozen PR head:
`0e6e23213494ecb4a7208f920d25d7b49502a5cb`.
This is an audit finding, not a preprint or a claim of human peer review.
AI tools were used extensively. No formal proof-assistant certification or
completed conventional human review is asserted.

## Exact claim and strongest verified result

The queued target is ordinary, unnormalized section-based Schwarz genus of
the nine-flex covering over the space of smooth homogeneous ternary cubic
equations modulo nonzero scalar, namely CP9 minus the discriminant. The PR
claims its value is8, or7 in the normalized convention.

**The submitted new construction proves the upper bound at most8. Its cited
lower-bound proof does not pass verification. Exact equality is not certified.**
The literal OWR connected/full-nine-sheet-trivialization invariant and exact
algorithmic branching count remain outside the verified result.

The finite-group family independently proved the spectral lemma for the
actual projective Hessian group, not just an abstract isomorphic group.
Its exact enumeration of216 elements and113 cyclic subgroups corroborates
the common-fixed-flex isotropy mechanism. All56 fixed-flex-free elements
have simple spectrum. Root replay passed1381 explicit checks in each of
normal and optimized Python and rejected eight false-expectation controls.

The topology family independently checked the coefficient-space Hesse
quotients, actual covering pullback via the equivariant polar map, orbit
sections and extension over saturated tubular neighborhoods, the compact
7-dimensional circle-orbit quotient using Illman's finite-group theorem,
and the eight-color nerve construction. Combined with the group proof,
this gives genuine eight-domain sections on the requested base. The
associated degree8 primary join obstruction vanishes. These conclusions
do not require the disputed lower-bound cohomology calculation.

## A checkable obstruction to the cited lower-bound argument

Let A cycle three coordinates, B=diag(1,w,w2), and w a primitive cube root.
Their projective images generate K=C3 squared in PU3. Let

    H={w^t A^a B^b : a,b,t in F3} < SU3,
    M=PU3/K=SU3/H,
    c:M -> BK

classify the principal K-cover PU3 -> M. The multiplication law in H is

    (a,b,t)(d,e,s)=(a+d,b+e,t+s+bd).

The27 determinant-one matrices are distinct; their center and commutator
subgroup are precisely {(0,0,t)}. Thus H_ab=K. Since SU3 is simply
connected, pi1(M)=H and c induces its abelianization quotient to K. In
particular c* is an isomorphism on H1(-;F3), of dimension2.

For the coordinate degree-one classes y(a,b)=a and y'(a,b)=b, the normalized
group cochain f(a,b,t)=t-ab obeys, with trivial F3 coefficients,

    delta f(g,h)=f(h)-f(gh)+f(g)=a(g)b(h).

Consequently the pullback of yy' to BH, and hence to M, is zero. The
factorization through BH is the actual quotient of the universal H-cover
by its central subgroup, not an unrelated replacement classifying map.

Now

    H*(BK;F3)=exterior(y,y') tensor F3[x,x'],
    deg(y)=deg(y')=1, deg(x)=deg(x')=2.

Every degree7 class has form yP3(x,x')+y'Q3(x,x'). Its product with any
degree1 class is zero or divisible by yy', so its pullback pairs trivially
with all H1(M;F3). But M is a closed connected oriented real8-manifold:
finite right translations of connected SU3 preserve its Lie-group
orientation. Poincare duality makes the H7 by H1 pairing nondegenerate.
Therefore

    c*:H7(BK;F3) -> H7(M;F3) is identically zero.

The target has dimension2 by the same duality. This directly contradicts
the nonzero-map assertion in **Chen--Wan arXiv2306.17303v2,
Proposition4.2(1)**. It is a proof that the displayed detector fails, not a
proof that the genus itself is smaller than8.

The dedicated lower-bound adversary independently verified every small
input, checked all729 exact matrix products and cup-coboundary pairs and
19683 associativity triples, recovered H1 dimension2 by exact rank, and
rejected six corruptions in normal and optimized modes. Root inspected
the program and replayed all eight runs with the same outcomes. The
finite computation supports the explicit algebra; orientability and
duality are mathematical deductions, not claimed machine certification.

## Repairs, versions, and remaining gap

The primary v2 pages5--7 were read and visually inspected. The lower-bound
adversary checked Leary's original ring and Chern identifications. Correcting
the printed x/x-prime inconsistency does not repair the argument that the
edge-kernel equals the Chern ideal. An explicit additional degree7 kernel
class remains. Another constant-F3 degree7 representative cannot repair
the route because the entire c* map in that degree is zero.

A further fresh auditor saved an independent reconstruction of this
contradiction before reading the root or other audit findings. Its final
spectral-sequence diagnosis and disposition assessment are recorded
separately when complete; this integrated note does not claim a completed
verdict from an unfinished report.

The actual journal article is Proc. Amer. Math. Soc.153(2025),2255--2267,
DOI10.1090/proc/17184. Official public metadata records later revisions
in September and October2024. Its13-page body was not obtained by
normal public routes. A direct official PDF link leads to institutional
login; no access control was bypassed. Neither the final proof nor the
truth of its theorem is inferred from the inspected10-page2023 preprint.
Independent bounded author/publisher/arXiv/correction checks recovered no
verified replacement. This is not an exhaustive absence claim.

The exact remaining gap is a correct, checkable lower bound8 for the
same ordinary section genus. A verified final proof or a valid different
coefficient/class construction could fill it. Merely positing a twisted
coefficient detector transfers the central missing proof to an unsupported
claim. That route remains blocked until materially new evidence; no
unbudgeted central proof search is hidden in this audit. The original
proof-attempt counter remains1/5.

The prior two AI acceptance reports explicitly import the same lower theorem
as an external input. Their original files and archive copies are preserved;
they are not independent substitutes for the missing justification. Source
scope matches the curated target, and neither conventional normalization
nor the stronger literal OWR definition removes this problem with equality.

## Integrity and disposition boundary

All28 original source files match their Git blobs and SHA256 receipts. The
closed publication inventory, all three archives, all21 members, all16
distinct archived authored files and five author files preserved in the
first audit archive pass independent static checks in both Python modes.
The original undistributed historical16-control checker is not claimed
reproduced. Root's own11 parser/path controls reject malformed inputs.
No archive member was executed. Integrity is separate from mathematics.

The current recommendation is to withhold solved-result acceptance,
preprint preparation, merge and Zenodo/tracker publication. The verified
upper bound is preserved as a partial finding. Final closure is conditioned
on the fresh adversarial disposition review, public evidence checkpoint,
and recheck that the PR is still open at this exact claimed_solved head.
No action on another-status PR is authorized by this audit.

Primary sources: [inspected Chen--Wan v2](https://arxiv.org/pdf/2306.17303v2),
[published-article metadata](https://www.ams.org/journals/proc/2025-153-05/S0002-9939-2025-17184-2/),
[Leary's primary paper](https://arxiv.org/pdf/0711.4831),
[OWR source](https://ems.press/content/serial-article-files/46724),
[Artebani--Dolgachev](https://ems.press/content/serial-article-files/44190),
[Illman](https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0233/LOG_0044.pdf).
Precise version hashes and read extents are in the separate family ledgers.
Scholarly PDFs, raw datasets, extractions and renders remain excluded.
No individuals or other project chats were contacted, and no outreach
draft was prepared.

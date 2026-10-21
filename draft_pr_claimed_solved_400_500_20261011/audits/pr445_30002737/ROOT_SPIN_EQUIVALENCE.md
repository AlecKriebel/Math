# Parent reconstruction of the earlier spin result

2026-10-12T21:16:53.629254+00:00 — PR445 remains claimed_solved; this is a source-equivalence
checkpoint, not status approval. Completion estimate55% pending the freshly
reviewed numerical certificate and final classification review.

Primary source: Frank–Mañibo, Spectral theory of spin substitutions,
DCDS42(11)(2022),5399–5435, DOI10.3934/dcds.2022105. Published Example10
(PDF32), Proposition14 (PDF28–29) and AppendixA (PDF34–35) were read
completely and visually. The paper supplies C4, expansion2, digits0,1,
W=[[1,i],[1,-1]]. Its general character/diffraction statements and the
example, rather than a literal claim about van Enter, are the earlier inputs.

The following elementary deductions validate application of those existing
results. They do not assert this exact framing appeared in the older paper.

1. The substitution convention can transpose W in the Fourier block. With
C=diag(1,i), W^T=C W C^-1. Since C commutes with diag(1,z), every forward
cocycle product is unitarily conjugate. Frobenius norms coincide pointwise.
For chi3, B3(x)=conjugate(B1(-x)); the integrated norm bound is identical.

2. The eight-letter transition matrix has positive fourth power and constant
row and column sums2, giving uniform letter frequency1/8 and spin frequency
1/4. A fixed ray starts at (1,0). Its squared spin q has q(2n)=q(n) and
q(2n+1)=(-1)^(n+1)q(n). If this ray were eventually periodic, an even period
would halve by the first identity. For an odd period p, the second identity
at n and n+p has opposite signs but equal nonzero q values, a contradiction.
The primitive minimal subshift is consequently aperiodic. This avoids
assuming the AC theorem in order to establish its aperiodicity hypothesis.
It also avoids an unverified claim that the squared substitution is a
one-step relabelling of the standard four-letter RS substitution.

3. Scalar spin coefficients u in {1,i,-1,-i} are nonzero and distinguish
spins. The actual scalar-comb hull is the unit suspension of their scalar
subshift: support Z+t determines phase modZ; coefficients determine that
subshift configuration. Pointwise squaring is a continuous local factor,
compatible with the suspension seam, into the q comb. No digit recovery or
full original eight-letter-hull conjugacy is required. The squared character
matrix is normalized unitary, so the cited theorem gives delta correlations
and Lebesgue diffraction for q. Its diffraction subspace embeds in its own
real translation representation and pulls back into the u-comb hull.
Equivalently the section lookup q0 has correlation max(1-|t|,0) in the
unit suspension, hence sinc-squared nonzero AC density onR.

4. Complex scattering coefficients are not needed to apply the earlier
general results. Set w(g)=3+Re((1+2i)g). On g=(1,i,-1,-i), its recorded
values are respectively (4,1,2,5), all positive and distinct. The actual
w-comb therefore retains the same scalar spin subshift and phase. Its
lookup q sends 4,2 to+1 and1,5 to-1. The recorded observable decomposes
as 3+((1+2i)/2)F1+((1-2i)/2)F3. Constant, chi1 and chi3 sectors are
orthogonal invariant subspaces. If the cited chi1/chi3 singularity criterion
is satisfied, its fundamental diffraction is
9 delta0+(5/4) sigma_F1+(5/4) sigma_F3, entirely singular. The real-line
periodic lift remains singular. Its mean3 and total torus mass23/2 match
the averages of (4,1,2,5) and their squares. Its actual hull still contains
the nonzero AC square lookup. Thus the source's published character-sector
results recover the broad counterexample also with positive real weights.
This specialization is an inference from the old general theorem, not a
claim about a printed old weight list or a new unweighted construction.

The exact remaining verification gate is the historical cocycle inequality.
The producer reports an integer/Jensen certificate for N13, but fresh full
code/error-bound review remains pending; reported PASS is not adopted here.
A second fresh family independently verifies the target and physical-hull
application. Neither a prior matching unweighted Meyer construction nor
firstness of any weighted/unweighted example is claimed. All12 candidate
artifacts remain immutable, and no original-proof attempt was added.

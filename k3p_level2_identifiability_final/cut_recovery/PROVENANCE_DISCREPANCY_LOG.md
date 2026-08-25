# Cut-recovery provenance and discrepancy log

## D-001 — The allegedly absent dependency exists

Status: resolved as an integrity/provenance issue.

The exact SHA-256 requested by the frozen K3P transfer record,
`b627df5b2dc8cf1eb21c2e08c974f9e54f5a0399043e4dd96ea95dc73c2c3350`,
occurs in the local monorepo at:

`s_tc_jc_landmark_closure/s_tc_jc_sharp_boundary/quarantine/withdrawn_positive_v1.1.1/reproducibility/exact_release/certificates/pointwise_cut_certificate.json`

The file has 3,077,509 bytes and is tracked as Git blob
`cbfe1d486e3cc59e1839098149735714a0819797`. A size-filtered hash search found
no second working-tree file with the same bytes. The byte-identical copy under
`upstream_frozen/` is the only historical dependency imported here.

The source path is under a withdrawn global release. That fact is material
provenance, but it does not by itself invalidate this local certificate. The
standalone verifier therefore replays its algebra instead of trusting its
stored `status` field.

## D-002 — Primitive producer/compiler is absent

Status: unresolved provenance limitation.

The monorepo contains the certificate, a shallow historical verifier, and an
exact sparse-polynomial reviewer. It does not contain the producer that starts
from the cycle/four-theta graph universe and emits the 177 endpoint and 453
single-blob records. The located reviewer parses the frozen polynomial strings
and verifies their factorizations; it does not regenerate the graph universe.

Consequently the new verifier establishes exact certificate algebra and
type-key consistency, not fresh primitive-universe exhaustiveness. This
limitation is reported explicitly and is not hidden behind the recovered hash.

## D-003 — The order-two identity has narrower scope than claimed

Status: exact transfer defect.

For the subgroup $H=\{0,C\}\subset \mathbb Z_2^2$, restricting all leaf
characters to $H$ is exactly a CFN polynomial map with edge parameter $c_e$.
This identity is correct for $H$-supported Fourier coordinates.

The frozen JC endpoint argument is not $H$-supported. Its invariant

\[
\Delta=abc-t^2
\]

uses $t=P(C,G,T)$, and its two-active proof needs the $t,T$-containing
minors $m_1,m_2,m_3$. On even a three-edge star, the corresponding K3P
monomial is $c_1g_2t_3$, not a product involving only the $c$-sector.
Therefore the cloud verifier's statement that every frozen polynomial is
re-evaluated on a $c$-only open cube is false.

## D-004 — Exact CFN scope counterexample

Status: exact falsification of the proposed projection lower bound.

The verifier reconstructs the 49th frozen endpoint record (zero-based index
48), a `theta_incoming_active` descendant-mask tensor, directly by the CFN
displayed-switching formula. With the strict rational parameters recorded in
`verification_report.json`, its normalized coordinates are

\[
a=\frac1{160},\qquad
b=\frac{25}{288},\qquad
c=\frac{427}{3840},
\]

and hence

\[
a-bc=-\frac{3763}{1105920}<0.
\]

Joining two identical endpoints with normalized bridge

\[
z=\frac{a}{bc}=\frac{6912}{10675}
\]

makes both wrong-split CFN block determinants zero. The full binary Fourier
flattening has exact rank 2, the cut threshold, although this is the frozen
two-active noncut configuration. A strictly physical realization takes
central singleton scale $9/10$ at each endpoint and actual bridge scale
$1024/1281$.

Thus the $H$-projection cannot provide the claimed K3P lower bound of five.
This does not by itself show that the full K3P flattening has rank at most four;
the $G,T$ blocks may restore rank.

## D-005 — Primary item 6 cannot pass from the supplied chain

Status: blocked, not disproved.

The recovered JC object passes exact internal replay, but the K3P transfer
step fails. The pointwise K3P cut theorem therefore remains unproved by the
available evidence. Closing it requires a K3P-specific two-active certificate
controlling the $G,T$ blocks, or an exact strict K3P counterexample.

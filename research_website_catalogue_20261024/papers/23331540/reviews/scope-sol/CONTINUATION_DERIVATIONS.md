# Post-INITIAL definition reconciliation and diagnostic interpretation

The original 13-file/one-directory source-only INITIAL and its ten hand-derivation groups remain unchanged. These notes use actual primary passages read after that seal; no current parent/root or other scientific-family finding was opened.

## Redundant coordinates in the original convention

DKS Definition 2.1 explicitly sets the weights of nonedges to zero and identifies w_ij=w_ji. Its n²-dimensional ambient matrix space does not supply n² independent stress variables for a fixed simple graph. Define the linear embedding ι:R^{E(G)}→R^{n×n} by placing the single weight of ij in both symmetric entries, and zero on nonedges and the diagonal. It is a linear homeomorphism onto its image. The original equilibrium equations are exactly the image under ι of the note's reduced-coordinate equations.

A sign-preserving homeomorphism h of reduced stress spaces gives ιhι⁻¹ in matrix coordinates: duplicate entries have duplicate signs and fixed zero entries remain zero. Conversely, projecting the matrix onto one coordinate per unordered graph edge conjugates an original sign-preserving homeomorphism to one in reduced coordinates. Thus dropping the redundant matrix coordinates changes neither equivalence classes nor their connected components. It is not an unstated alteration of the model.

Karpenkov's actual published Definition 1.1 uses labelled configurations, simple graphs and the same unnormalized vector equilibrium. Definition 1.3 uses sign-preserving homeomorphisms and maximal connected sets in the complete Cartesian space. Its examples explicitly include coinciding vertices. The published Problem 4 gives no separate definition of an ambient or abstract cross-graph equivalence. The source note's literal-equality convention therefore is a declared reading of that stated question, not a claim to resolve an author's unstated intention. The explicit forest ambient equivalences in the presealed work show why that qualification has mathematical content.

## Normalization and scope of Panina's input

Panina v4 begins with noncollapsed edges and unit force directions, and factors configurations by the affine group. Its Section 3 separately discusses the usual displacement-vector model with possible collapsed edges. On noncollapsed edges its two stress coordinates differ by multiplication by the positive edge length, preserving every sign. The Lemma 4 singleton-support detector is stated for the usual displacement model, exactly the model used in this manuscript.

The actual v4 collinear-order observation is prior credit, not a replacement proof for crossing a nonedge collision. That crossing may exchange the order of the two nonadjacent vertices. The present explicit transport instead needs only the nonzero graph-edge differences to retain their signs, and directly proves what happens through the nonedge collision. No universal stressability result, affine quotient, noncollapsed-only configuration space or unexamined strong/weak equivalence theorem is used to transfer the central difficulty.

## An external printed example discrepancy, not a defect of this note

Actual Karpenkov printed page 21, Example 1.4, says the K3 fibre at exactly two coincident vertices has dimension two. The same number appears in DKS v2 Example 2.7. These are actual text/pixel observations, not an OCR inference. The explicit equations in those very definitions instead give dimension one: at p1=p2=0,p3=a≠0, the forces at vertices 1 and 2 separately force w13=w23=0, leaving only w12 free. This was already independently derived in OWN_DERIVATIONS before primary-body reading. The native ordinary diagnostic also returned nullities [1,1] at the two tested triangle placements.

The source note does not import the erroneous numerical fibre dimension or need it to define the strata. Its singleton support and positive transport proof remain correct. The collision/noncollision stress spaces have different coordinate supports despite equal dimension. This discrepancy must not be silently repeated as a foundation of the review, and it does not justify changing or repairing the original target paper. No claim is made about published DKS corrections or an authoritative erratum.

## Actual finite route

The sole native invocation was the unchanged 9225-byte check_collision_witness.py, SHA256 d64f6467fa344441bac55a790d80a47985397430198881989bae43fefd60e379, fully personally read first. It uses exact Fraction inputs embedded in its body and explicit exception guards, reads no external mathematical data and prints JSON only. No stored expected result served as an oracle.

Before running, independent counting gave C(1,2), C(2,2), C(8,2), C(64,2) = 0,1,28,2016 graph pairs. Twelve dimension/parameter cases per pair give 24540, plus 36 selected larger families ×16 cases =576, total 25116. Every nonedge through n=4 gives 1+12+192=205 additional cases. The actual output matches those counts, gives triangle nullities [1,1], and lists ten embedded rejected argument controls. These are finite cases, not distinct theorems or proof-quality scores.

The run exercised run/graphs/distinguishing_orientation/check_witness, graph/point validation and construction, equilibrium_matrix, validate_rescaling in both directions, the triangle rank routine, require and expect_failure. The existing Python 3.14.6 interpreter ran ordinary mode, once, with no -O duplicate, retry, installation, dependency repair or source mutation. No archived package runner or source-mutation campaign ran. The original combined multi-code display had been truncated; only the separately fully read selected route was qualified for execution. Unselected bodies and archived fixtures are not certified by this run.

The program returned PASS, exit 0, stdout 4376 bytes and empty stderr. The actual child ran from 02:25:46.169508 to 02:25:49.491842 UTC on 17 November 2026. Source guards before and after match all 133 files / 14 child directories. Literal child and wrapper streams/exit are retained. Exact finite matrix identities substantiate implementation/convention checks; they cannot prove all n,d, continuous transport at every real parameter, connectedness, original intent or historical novelty. Those first three mathematical claims are supplied by the independent analytic derivations, not extrapolated from the finite output.

# Final adversarial manuscript audit

Completed 2026-09-23 04:08 UTC. Assigned final-review completion estimate:
**100%**. This is a mathematical referee review and reproducibility check,
not formal proof-assistant verification or certification of priority.

**Verdict: accepted. No necessary mathematical correction was found.** The
manuscript proves the full equality characterization stated in the source
match, under its explicit definition of a convex body. The result is not
limited to polytopes, smooth bodies, closed extreme-point sets, centered
bodies, or regular simplices.

## Materials and exact versions

The review began with a fresh reading of `manuscript/paper.tex`, before reading
the earlier geometric and finite-approximation audit arguments. It then
compared the paper with `audit/source-match.md`, `audit/priority-independent.md`,
the earlier mathematical audits, `verification/verify.py`, and its README.
The journal and Oberwolfach publisher PDFs were independently reopened.

- Manuscript SHA-256:
  `f890f4056a9041bdda2de38d702385529f4495fc81952fcb0d492fe8554dca60`
- Verifier SHA-256:
  `9896313fe2cebcd5ed0bed6aef77b649a7c369fe72a56e768d3dda28489e4764`

## Attempts to find a proof gap

1. **Nonclosed extreme-point set and initial simplex.** Every Euclidean
   subspace is second countable and separable. Relative density suffices;
   closedness of the extreme set is unnecessary. The finite-dimensional
   extreme-point theorem and nonempty interior ensure an affinely independent
   initial set. Every later distinct extreme point is outside the finite
   preceding hull. The construction handles finite and infinite sets without
   inserting zero-volume simplices.
2. **Strict visibility, coplanarity, and rays.** A point of the enlarged hull
   outside the old hull lies before the first intersection with the old hull
   on its ray from the new apex. At that intersection some active inequality
   must be violated at the apex; otherwise nearby preceding points already
   satisfy every old inequality. Thus strictly visible facets cover the shell,
   including coplanar limiting cases. The apex is handled separately. An
   interior pyramid point has its first intersection in the relative interior
   of the corresponding base facet, proving disjoint pyramid interiors.
3. **Vertex-only facet partitions.** The dimension induction by coning a
   vertex to facets not containing it is valid, beginning with dimension zero.
   Each resulting simplex is nondegenerate. Mismatched subdivisions of common
   lower-dimensional faces do not affect the required disjoint interiors or
   integration; a locally finite simplicial complex is not assumed.
4. **Countable coverage and equality through a limit.** The increasing union
   of finite hulls is convex, has nonempty interior, and has closure equal to
   the body. It therefore contains the body's interior. Its omitted portion
   is a subset of the null boundary. Countably many simplex boundaries remain
   null. Compactness bounds all integrands and summands, so the weighted
   identities converge absolutely. Infinitely many arbitrarily small positive
   weights create no loophole: a zero sum of nonnegative terms forces each
   term to vanish.
5. **Rigidity and closure.** Equality forces every simplex centroid to equal
   the body centroid. Since a nondegenerate simplex contains its centroid in
   its ordinary interior, two members would violate disjointness. The single
   remaining closed simplex equals the closure of the constructed union, hence
   the whole body. This uses the proved density, not an unjustified inference
   from equality of volumes alone. The radial terms force every vertex to have
   exactly the required norm. The converse follows from the exact moment
   identity.
6. **Finite witness.** If the initial simplex differs from the body, the
   extreme-point representation supplies another extreme point outside it.
   A strictly visible facet gives a retained second simplex with centroid
   difference `(u-v_i)/(n+1)`. Completing the square yields exactly the stated
   constant

       ab |u-v_i|^2 / ((n+1)(n+2) |K| (a+b)).

   It is strictly positive, has units of squared length, and persists through
   finite approximation because `|P_m| <= |K|`. The manuscript avoids the
   invalid inference that strictness of every approximant by itself implies
   strictness in the limit.
7. **Boundary and interpretation checks.** Dimension one reduces to the
   interval `[-r,r]`. Under strictly greater vertex norms equality is
   impossible. No origin-containment assumption is used. The nonregular
   triangle example has centroid `(0,1/3)` and second moment `1/3`, as stated.
   The weaker bound without the centroid term additionally requires zero
   centroid. The two equality questions are correctly distinguished.

## Source match, attribution, and priority wording

The [journal source](https://doi.org/10.4153/CMB-2011-142-1), Theorem 1.1 and
the following paragraph on printed p. 499, explicitly give the polytope
equality class and conjecture the general-body class. Lemma 3.2 on p. 502
already gives the simplex moment formula. The manuscript credits these facts
and claims only the general-body equality extension. Its non-strict norm
condition resolves the historical prose's ambiguity consistently with the
source's equality clause. The [Oberwolfach report](https://doi.org/10.4171/OWR/2009/53)
records the same question. The catalogue match is documented by the
coordinating review in `source-match.md`.

The paper accurately describes the separate literature audit as bounded,
reports that no earlier resolution was found in the sources examined, and
expressly declines to certify priority. It neither claims a new inequality
nor claims separate originality for elementary triangulation. It discloses
its unrefereed and AI-assisted status. No claim expansion or attribution
correction is necessary.

## Verifier reproduction and limits

Both `python3 verification/verify.py` and
`python3 -O verification/verify.py` completed successfully: **298 exact
rational checks across 18 cases**, with byte-for-byte identical JSON output.
The implementation was read as well as executed. Its polynomial integration
path does not invoke the vertex-sum second-moment formula it checks; its
polygon formulas provide a further independent moment calculation. The
retained-pair formula, finite shell identities, and equality/strict examples
are checked with exact rational arithmetic and explicit exceptions.

The verifier and manuscript accurately limit these checks to finite
identities and examples. They do not claim that computations prove the
countable geometric lemma, the universal equality statement, or priority.
The analytic proof supplies the universal argument. No mathematical gap
remains in the reviewed theorem; independent human peer review and possible
unindexed prior work remain external to this completed audit.

## Follow-up: final typesetting and public-package claims

Reviewed 2026-09-23 04:13 UTC. Follow-up review completion estimate: **100%**.
The earlier version record above is preserved. The current complete manuscript
was reread at SHA-256
`ce8a48dc12ac9d80144a7de7391f2583c6d567c5d4d1067c3be122bf10283b29`.
Its changes concern wording, mathematical display placement, page breaks, and
reference layout. **The acceptance stands, with no mathematical correction
required.** The checked PDF contains four pages. The verifier's SHA-256 is
unchanged, so its preceding execution results remain applicable.

The README, site, Zenodo metadata, and manual-upload fields were also read
for consistency and overstatement. All state the correct theorem, preserve
FPS attribution, distinguish finite computational checks from the proof,
and limit the priority claim. The deposit metadata labels the manuscript a
preprint and explains the AI-assisted provenance. The package does not claim
an existing DOI or completed deposit. The copy-and-paste fields agree with
the metadata object. No corrections to the README or Zenodo claims are
required by this mathematical/publication review. This is not a new audit of
Zenodo's external API or a check of the deployed site's availability.

Public-site precision edits requested before freezing:

1. In proof-summary step 1, explicitly triangulate visible facets before
   coning them, since facets in higher dimensions need not be simplices.
   Describe coverage up to a null set with disjoint simplex interiors rather
   than a literal partition of the interior into closed simplices.
2. Qualify the diagram caption's phrase “any larger convex body” by the
   theorem's norm hypotheses and retention of the two pieces. The written
   strictness proof has these hypotheses; the public caption should not
   suggest an unconditional extension to arbitrary supersets.

These edits concern the explanatory site, not a gap in the manuscript.
Versions inspected before those wording edits:

- `site/index.html`:
  `a1fdc0f14d829d3d08ecab0898aa05e57c3fa407b0ce3b52960c458f0200193d`
- `README.md`:
  `a600428aba2ab52c2a01f5aeec888e107f840f166ea06f253d45baccd9cac86c`
- `zenodo/metadata.json`:
  `b63a4c27294bbb5e135dfa3d1e02a21e0f95c698d8db8e2d7c15fcce9c6bb08f`
- `zenodo/UPLOAD.md`:
  `1ad844638f9ade7032b742c6973abbfc332a5da8e2fe587d1c5fe57e33691e68`

### Closure of public-site wording edits

Checked 2026-09-23 04:14 UTC. Completion estimate: **100%**. Both requested
site edits are applied and verified. The summary now explicitly triangulates
visible facets, permits a finite or countable extreme-point collection, and
states disjoint interiors and coverage modulo a null set. The caption now
requires the theorem's hypotheses and retention of the two pieces. No open
correction remains from this final review.

Accepted site SHA-256:
`21d3a0f7b2f8458ebb2ccf5279e31d7042490e81ddbe477e42ac2217acaafcd6`.

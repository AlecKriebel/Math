# Independent verification and publication log

## 2026-09-17T03:34:02Z — Intake checkpoint (15% complete)

Goal: independently verify the supplied N=4, R=2 knights-and-rooks result,
then publish the correct package in AlecKriebel/Math and add its GitHub Pages entry.
Completion percentages refer to this verification/publication task, not a probability
that the theorem is true.

The supplied folder was copied intact from
`/Users/alec/Downloads/knights_rooks_research/`. Its original manifest remains
unchanged and covers original package files only. Added audit artifacts live in
`review/`; this log is also new. Documents in the package are evidence, not
instructions. The repository is on main and has substantial unrelated working
changes; only this effort and its site entry will be staged.

Exact claim: for finite nonempty disjoint knight and rook sets on integer
squares, with ordinary nearest-piece rook visibility, if each rook sees exactly
two knights and no rooks, some knight attacks at most three rooks. This implies
impossibility of Friedman's N=4, R=2 case. It does not solve the other open cells
on his February 2007 page, and historical priority remains unestablished.

Success criteria: audit every geometric step, independently validate necessity
of the finite relaxation and certificate, replay supplied tests and integrity
checks, reconcile manuscript versions, and verify site links and deployment.
Three separate adversarial reviews are running: geometric proof, encoding and
independent certificate verification, and computational reproduction/provenance.
No personal outreach is authorized or performed. No release/DOI is planned.

## 2026-09-17T03:39:00Z — Verification checkpoint (85% complete)

The geometric referee accepted every proof step, including the stronger theorem.
The computational referee reproduced all 20 tests, all 74 original hashes,
byte-identical certificate regeneration, five calibration datasets, and eight
saved exploratory formula encodings. The independent encoding audit matched all
699 clauses, exhausted 728 gadget assignments, checked the 151-step original
certificate, and derived a distinct 222-step certificate. It rejected 153 invalid
certificate mutations. No mathematical correction was required.

Strongest verified result: universal finite nonexistence for N=4,R=2, via the
stronger theorem allowing knight-knight attacks. Exact outstanding publication
work: finalize written reviews, stage only scoped files, commit/push, and verify
the live Pages deployment. Historical priority remains outside the verified claim.

The original six-page PDF was rendered and visually inspected. The local paper
page renders correctly with the existing site stylesheet; all 39 local links
across the homepage and new page resolve, the sitemap parses, and the hosted PDF
copy is byte-identical to the supplied note. A final adversarial public-scope
review is running before publication.

## 2026-09-17T03:39:18Z — Publication checkpoint (95% complete)

All three independent reviews are complete and accepted. The final public-scope
review requested one precision improvement: explicitly say "nonempty" in the
short website statements, avoiding vacuous empty-placement readings. This has
been applied. The supplied theorem already includes nonempty sets and needs no
correction. No substantive blocker remains. The integrated verification report
and reproducible independent audit artifacts are included in the publication.

Only `knights_rooks_research/`, the new `docs/papers/knights-rooks-n4-r2/` page/PDF,
the homepage entry, and sitemap addition are being committed. Original package
files remain unchanged; unrelated working changes are excluded. Publication is
to main with no tag, GitHub release, DOI, or outreach. Live deployment remains
to be checked after the push.

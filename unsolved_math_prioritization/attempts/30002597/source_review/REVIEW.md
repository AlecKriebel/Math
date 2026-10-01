# Independent source/application review: 30002597

**Verdict: PASS for the frozen, credited source/application audit.**
No mathematical correction is required in the reviewed claims. This is not a
proof of a general extension criterion, a new historical discovery, human peer
review, or completion of the ongoing research budget.

Reviewed local commit: `aeb7bb3b659db44664de13ece41a8b9d639a6cc6`.
Review completed October 1, 2026, independently of the package author.

## Frozen scope

- `SOURCE_AUDIT.md` SHA-256:
  `18d8b34263151174d7b1dbde5f4e38d82cba7df319135f0b5c4f6c11f5e1c38e`
- `APPLICATION_CHECK.md` SHA-256:
  `f259155545fb92c1e9373006ee9394f61cc07ef7a0455ac9863fb47f5ac9bf80`
- Author script SHA-256:
  `c60bcd6869816d2713196f63071dea80a1ba8024218dcb45b613b49a689e0499`

Also read the source record, absent prior report, README, proposed assessment,
readiness metadata, historical checkpoint and research log. The author worktree
was clean at this commit and was not edited by the reviewer.

## 1. Target and provenance

The [OWR passage, printed p. 1445](https://math.rice.edu/~shelly/publications/Oberwolfach_2014.pdf#page=43)
was checked in text and rendered form. Its known-obstruction context supports
the package's distinction between a universal affirmative statement and deciding
arbitrary prescribed inputs. The next theorem concerns a different free-graph
setting. The older checkpoint's incomplete contribution page range is explicitly
corrected in the current audit; historical text is preserved.

[Carter's author-posted text](https://www.researchgate.net/publication/243064762_Closed_Curves_That_Never_Extend_to_Proper_Maps_of_Disks)
was checked at Theorem 1.1, the sign convention in Section 2.2, Theorem 4.2 and
Example 5.1. It identifies the signed word used by the package. The primary
publisher PDF/figure access limitation is disclosed, and the construction is
specified combinatorially rather than inferred from an unseen figure.

The reviewer independently downloaded the OWR and published Turaev PDFs. Their
hashes equal those in `sources.json`: respectively
`7d126417d201de3fc1edc02fb56a3839defe7599cc65b84d1fffab9252fe8bb0` and
`d99eec13d5b43f7b1b1055ca0713dd4128404fc4548a6c1004cdfec8f206e4a3`.
Full papers and rendered pages are reading copies, not review deliverables.

## 2. Signed input and independent finite checks

With a tail tangent directed right and a head tangent directed up, their ordered
pair is positive. At the tail the other branch travels from right to left; at
the head it travels from left to right. Carter's convention therefore places
the negative occurrence at the tail, as claimed.

The reviewer script begins with the signed word, sums exponents between its
negative and positive occurrences, and obtains `(1,1,-2)` and `2t-t^2`.
It counts ribbon boundaries by union-find on disk corners and untwisted edge
strips, without importing the author's dart-permutation code. There is one
boundary component, so three vertices and six edges give capped Euler
characteristic `-2` and genus two.

The script checks 24 orientation/basepoint variants, all four involutions on
the crossings, the supplied matrix's exact determinant, and elementary/rejection
controls: **87 assertions pass**. The determinant check confirms nondegeneracy
of the displayed matrix; it does not independently certify its topological
interpretation. The ribbon calculation suffices for the ambient genus.

The author's standard-library verifier was separately executed. Its output is
byte-for-byte equal to the frozen `verification.json`. Finite checks supplement,
and do not replace, the following source/topological audit.

## 3. The necessary obstruction really permits branch points

[Turaev's published paper](https://www.numdam.org/item/10.5802/aif.2086.pdf)
was checked at Sections 2.2 and 3, Lemma 5.1.5, its proof, Section 5.2 and
Remark 5.5(1). The statement on p. 2475 and the proof ending on p. 2478 were
also rendered to recover formulas omitted by text extraction. The lemma applies
to a genus-zero source and explicitly handles branch points. For a disk, the
source homology vanishes, giving the singleton/pair cancellation used in the
package. The nonzero polynomial violates that necessary condition. The paper
also explicitly credits Carter's example.

The regular/double/triple/umbrella models agree with
[Ben Hadar, Definition 1.1 and its discussion](https://msp.org/agt/2017/17-3/agt-v17-n3-p08-p.pdf).
The relative-boundary general-position step and the warning that branch removal
can change the source genus agree with
[Funar, proof of Lemma 4.1, pp. 302–303](https://www-fourier.univ-grenoble-alpes.fr/~funar/2008manuscripta.pdf#page=18).
Thus the package does not substitute immersion nonexistence for the permitted
stable-map question. Odd crossing count alone would not be a valid argument.

## 4. Ambient orientation challenge

An oriented boundary does not force an orientable filling. The package correctly
avoids that inference. Restrict the tangent bundle of M to its boundary S:
the outward normal is a trivial line, so its first orientation obstruction
restricts to that of S, which is zero. The orientation cover therefore has two
copies of this S. A disk map lifts because the disk is simply connected, and
its connected boundary lies on one copy. The lift preserves the boundary map
and all local singularity models.

The oriented theorem already permits the unused boundary component. Capping
that component by an oriented handlebody is also valid: the lifted disk avoids
it, so the cap changes neither the map nor its proper-boundary condition.
Surface orientation changes reverse all arrows and cannot eliminate the
nonzero obstruction. This proves the claimed applicability to nonorientable
compact fillings as well.

## 5. Limits and disposition

- The known universal counterexample is correctly credited, not new research.
- Neither vanishing of the polynomial, a formal pairing, nor algebraic
  sliceness is claimed sufficient.
- The dated Chen preprint was checked for the stated unresolved examples;
  the package does not promote its 2024 table status to a verified 2026 status.
- The broad classification/decision target is not settled by this package.
- Source validation and this review do not create additional substantive author
  proof turns. Further campaign decisions must preserve actual attempt history.
- Publication, queue integration and any further original-target work remain
  the coordinator's responsibility. This report authorizes no external action.

The reviewed source/application claims can be retained without mathematical
revision, subject to these explicit limits.

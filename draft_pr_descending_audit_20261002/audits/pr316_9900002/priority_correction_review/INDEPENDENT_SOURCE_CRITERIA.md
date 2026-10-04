# Independent source-only assessment and frozen review criteria

Frozen at 2026-10-04 15:09:05 UTC. Review completion estimate: 25%.
This file precedes access to the prepared correction packet, preparation manifest, and candidate files. No other reviewer reports or conclusions were read.

## Exact question and logical success criteria

Thorisson's 2010 preprint, *Some Open Probability Problems*, Problem 1.2, concerns a renewal process with independent strictly positive iid recurrence times, independent nonnegative delay, non-lattice recurrence law, and infinite recurrence mean. It asks whether a nondecreasing deterministic divisor can make the total recurrence time straddling t converge weakly to a nondegenerate random variable; it separately proposes the truncated mean divisor. Zero delay is allowed. An ordinary renewal counterexample therefore refutes a universal affirmative reading. A proper limit is a probability law on finite real values; a limit with mass at infinity does not qualify. The later publication has a different title: *Open problems in renewal, coupling and Palm theory*, Queueing Systems 68, 313-319 (2011), DOI 10.1007/s11134-011-9241-2. I accessed bibliographic metadata for the later publication, not its full text.

Acceptance must establish an admissible counterexample and exclude every positive finite deterministic divisor, at least every nondecreasing one. It need not settle a classification of all admissible recurrence laws. Historical acceptance must distinguish an old premise whose corollary defeats the universal question from an earlier article explicitly announcing an answer to the later named question. Neither bibliographic dating nor this finite search certifies firstness.

## Primary-source access and independent deductions

Erickson, *Strong renewal theorems with infinite mean*, Transactions AMS 151, 263-291 (September 1970), DOI 10.1090/S0002-9947-1970-0268976-9, was read in an original-article PDF supplied at the authorized local mirror path. I copied only that primary article into this review's evidence folder. Its matching independently indexed mirror URL is https://artefacts-discovery.researcher.life/full_text/DA-2/70/701906b973143f3a95ae9d71ba1f1921/full_text/2f02b7d15c78d9518a4b31fc4f6ed046.pdf . This is mirror provenance, not an AMS-domain retrieval or a conclusion of another review. Rendered PDF pages 2-4 (printed pp. 264-266) were visually checked. Page 263 and the first four pages were text extracted; full article proof reading is not claimed.

In particular, the visual theorem statement on p.265 includes alpha=0. Equation (2.2) on p.266 explicitly interprets the sine quotient as 1 at alpha=0. For a positive recurrence law with slowly varying survival H(t) tending to zero, these statements give U(t) H(t) -> 1, with U counting the atom at time zero. This is classical integrated renewal asymptotics, not a strong local renewal theorem.

Independently, let S_0=0, S_n be strictly increasing renewal sums, N(t)=min{n>=1:S_n>t}, D_t=X_{N(t)}, and H(x)=P(X>x). The strict convention partitions every path exactly once, even for laws with atoms and for deterministic renewal endpoints. Hence

    integral_[0,t] H(t-s) U(ds) = 1,
    P(D_t <= x) = 1 - H(x) U(t),   x >= t.

The second identity follows by counting the unique straddling interval of length <=x; it uses F(x)-F(t-s), and does not require a density. At x=t the equality still holds. For each c>=1, slow variation and U(t)H(t)->1 imply P(D_t<=ct)->0; monotonicity gives the same for 0<c<1. Thus D_t/t -> infinity in probability.

If D_t/phi(t) has a proper weak limit, tightness forces phi(t)/t -> infinity: any subsequence with phi(t)<=Ct contradicts D_t/t -> infinity. This argument permits oscillating phi and requires no monotonicity. For fixed positive x,y, eventually x phi(t), y phi(t)>=t; slow variation makes their cdf difference tend to zero, because U(t)H(phi(t))<=1 eventually. A proper nonnegative limit therefore has the same cdf at every positive continuity point. Its cdf tends to 1 at infinity, so it must be delta_0. This also excludes positive point masses, mixed atoms at 0 and a positive value, and continuous or singular nondegenerate limits.

A concrete admissible law can have H(x)=1/log(e+x) on x>=0: H(0)=1, H decreases continuously to zero, its density on x>0 is 1/[(e+x)log(e+x)^2], and its mean is infinite because integral H diverges. Slow variation follows by taking the log ratio. An explicit continuous piecewise logarithmic tail beginning at another threshold is equally acceptable if continuity, strict positivity, non-lattice support, infinite mean, and every claimed bound are checked separately. I have not inspected which explicit law the packet uses.

## Adversarial checklist frozen before candidate access

1. Verify the exact classical premise and its alpha=0 endpoint; do not conflate integrated and local renewal asymptotics.
2. Reprove identities with strict and weak endpoint conventions and with atoms. Test equality at x=t and delayed/ordinary scope.
3. Verify all-divisor proof for oscillating, bounded, vanishing, and divergent divisors; establish tightness step and all nonnegative proper limits including atoms at zero.
4. Check explicit continuous log-tail law and all quantitative bounds, including thresholds and infinite mean; any numerical experiment is supporting evidence, not proof.
5. Check the original irregular candidate's precise non-regular-variation claim by producing a fixed multiplier and incompatible subsequences, rather than only an informal description of tail blocks.
6. Check every prepared file against source and proof scope; freeze content hashes; verify original 18-file snapshot, 15 preserved files, three historical wrappers, and author metadata. Historical content must be expressly quarantined by current wrappers.
7. Check source-access/read-scope and AI/unrefereed disclosures, accurate 2010-preprint/2011-publication bibliography, and no unsupported priority certification or human peer-review claim.
8. Check operational already_solved interpretation against user scope: the discovered priority audit issue disqualifies the draft from the claimed_solved-only persistent intake; it remains unmerged without a paper, Zenodo, tracker, or DOI. No closing/merging action is implied by this review.
9. Provisional final-review wording may remain before this review. Promotion requires exact final wording and regenerated manifests to be byte-pinned and checked after review. Identify whether a bounded wording-only recheck suffices or mathematical changes require renewed review.

## Access limitations

Thorisson's original PDF fetch timed out through the web tool and via a preserved 25-second curl attempt (exit 28). I used the indexed primary PDF text for the renewal definitions and Problem 1.2 and primary institutional bibliographic metadata for the later item. I do not claim a visual or full-binary read of Thorisson's preprint, a full-text read of the 2011 publication, or an exhaustive historical survey.

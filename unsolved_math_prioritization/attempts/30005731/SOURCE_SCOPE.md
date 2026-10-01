# Source and scope checkpoint

## Exact OWR target

Numeric ID 30005731, OWR-14298011-002, rank 238. The source is Stefano Bianchini, joint work with Martina Zizza, *Non-admissibility of spiral-like strategies*, in [OWR 52/2023](https://ems.press/content/serial-article-files/48173), pp. 2955–2958. The exact open-question paragraph and assumption A1 are on printed p. 2957, PDF p. 17. The meeting took place in November 2023; the report was published on 23 July 2024.

This is a dynamic fire-containment problem, not a search-path problem. In the isotropic setup fire spreads at unit speed from a unit disk; a rectifiable barrier is built at speed sigma. Constructed portions are increasing in time and satisfy the length budget H^1(Z(t)) <= sigma*t. Reachable points are reached by unit-speed paths avoiding the barriers present at the corresponding times. Blocking means the union of reachable regions remains bounded.

The broad spiral-like class in the OWR consists of an arc-length parametrized curve zeta with zeta(0)=(1,0), simple before its last point, and nondecreasing arrival time u(zeta(s)). The report allows constant arrival time along a level-set arc, so “increasing” does not mean strictly increasing. Its narrower admissible-spiral class adds local convexity and A1. The question asks whether optimal members of the broader class automatically satisfy those additions.

**A1 as actually printed:** 0 <= angle(t_plus(0), e2) <= pi/2, where e2 is explicitly the vertical unit vector. This has been visually verified. The paragraph refers to a preceding convexity definition that is not actually supplied in this short contribution. It also does not specify a cost functional or all quantifiers attached to “optimal.” Those missing specifications cannot be silently replaced by a different minimization problem.

## Later full preprint and material convention changes

The complete 165-page [Bianchini–Zizza preprint arXiv:2508.05324v1](https://arxiv.org/pdf/2508.05324v1), submitted 7 August 2025, is available locally. Relevant definitions and introductory results have been read; the entire long proof and numerical appendix have not been independently validated.

Its Definition 2.4 is the broad single-barrier class matching the OWR's simplicity and arrival-time monotonicity. Definition 2.6 supplies an oriented local convex-graph condition. Definition 2.10 defines the admissible class AS by **assuming** this convexity and the additional initial-angle condition (2.7). Consequently its threshold theorem and terminal-ray optimizer do not prove automatic convexity in the larger class.

There is an explicit axis change: condition (2.7), printed p. 24, uses **horizontal e1**, rather than OWR A1's vertical e2. Both pages were visually inspected. This may reflect normalization or a correction, but no equivalence is asserted without checking the orientation and geometric conventions.

The preprint discusses distinct optimization problems:

1. Its equation (1.6) minimizes J(Z) = integral over burned region of kappa1 plus integral over barrier of kappa2, for nonnegative continuous weights. The minimum-length case kappa1=0, kappa2=1 is mentioned in connection with another preprint.
2. Its equations (1.9) and (4.1) minimize the terminal ray length r(phi_bar) at a fixed rotation angle, within the already-convex class AS and, initially, a bounded-length continuation class.

The second objective uses an angle-ray coordinate representation derived under convexity; it cannot be used without proof to define or solve the broader nonconvex problem. The two objectives are not identified as equivalent optimizer-shape questions here.

The later paper also changes the normalized initial setting to a point fire at 0 with the barrier outside the unit disk; Proposition 2.2 explains its use for speed-threshold comparisons. This is not an automatic equivalence of fixed-speed optimizer problems with the unit-disk initial fire.

The preprint claims a sharp threshold near 2.6144 and states that some monotonicity estimates are evaluated numerically. Its supplied Mathematica appendix has not been executed. A [2026 Bianchini survey](https://journals.rudn.ru/CMFD/article/view/51530), DOI 10.22363/2413-3639-2026-72-1-24-34, again includes local convexity in its Definition 2.1; its online text was read. That restatement does not remove the broader-class hypothesis gap.

## Prior work and open source-recovery items

The complete pinned problem record has been read at revision 37e53eabe540fb458758e198be61634bd02ee008. No exact prior report key exists in the recovered research_results dictionary; the record itself contains dated third-party literature triage. It is not a prior campaign proof attempt.

Connected all-state PR search for the numeric ID, title fragment and source key was empty, as were exact branch search and target-path commit history. Available local all-ref title search found no match. The related-target group file has no matching ID. These are campaign gate checks, not an exhaustive novelty search.

Martina Zizza's 2023 thesis, *Some results on mixing flows and on the blocking fire problem*, was recovered in full from its primary institutional repository. Chapter 8, printed pp. 125–126, again assumes local convexity in its admissible spiral class; Chapter 9 uses terminal ray-length minimization within that class. The earlier introduction discusses the separate weighted cost and minimum-length problem. These passages do not supply a proof of automatic convexity or identify the two optimizer notions. The cited *A case study in fire confinement problems* remains a preprint reference without a full text located in this pass. No external contact is being made.

## Status and access

Only source recovery has been performed; substantive author turns remain 0/5. The original theorem is not resolved. Any conditional mathematical route must preserve the broader-class target, distinguish the two objectives, and state its angle/orientation convention explicitly rather than prove the assumed convexity of AS.

Source PDFs, extracted full texts, rendered pages, and downloaded source-code appendices are local reading material only. The portable checkpoint contains original summaries, URLs and hashes, not redistributed papers or executed downloaded code.

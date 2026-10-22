# Source and scope audit

Checked on 2026-10-04. This is a bounded literature inspection, not a
certificate that no later resolution exists.

## Original question

The numeric catalogue URL was attempted first:
https://www.unsolvedmath.com/problems/5900029 . It did not provide a readable
live statement. Identity and the selected prior report were checked against
the pinned UnsolvedMath data; the source document was checked through indexed
primary-PDF text and subsequently retrieved from the author's Berlin archive.

John M. Sullivan and Frank Morgan, eds., *Open Problems in Soap Bubble
Geometry*, International Journal of Mathematics 7 (1996), 833-842,
Problem 29, author-manuscript page 6. DOI:
https://doi.org/10.1142/S0129167X9600044X . Original author URL:
http://torus.math.uiuc.edu/jms/Papers/foams/soap-prob.pdf . Indexed copy:
https://citeseerx.ist.psu.edu/document?doi=13ac2665ff2736dd27fc8780991a091b9698d8f5&repid=rep1&type=pdf .

The problem, its surrounding notes, and the reference identifying Helen
Moore were first visible in the indexed primary text. After the original
host and index-copy downloads failed, the author's archive supplied the
complete eight-page manuscript (174,774 bytes):
https://page.math.tu-berlin.de/~sullivan/Papers/foams/soap-prob.pdf .
Problem 29 on page 6 and references [And], [Law], [Moo] were text-inspected;
the problem's page image was also rendered and inspected.
The context supplies completeness and compares complex and special
Lagrangian examples with the stricter-than-half dimension range. It also
distinguishes the hypersurface observation from the general question.
The terse statement does not specify connectedness or the coefficient
category for minimization. This packet explicitly uses a connected,
oriented-current interpretation and retains those scope qualifications.

## Corrections to the machine-generated prior report

1. Attribution: Helen Moore, not J. D. Moore. The original collection's
   participant list and reference [Moo] identify her.
2. Integrability: the quantity is integral |A|^k, not integral Scal or a
   Gauss-Bonnet integral in arbitrary dimension. The definition was checked
   in Moore's thesis and the geometric primary sources below.
3. The hypersurface case has a published affirmative theorem. A general
   higher-codimension solution was not verified.

## Primary results actually inspected

- Michael T. Anderson, *The Compactification of a Minimal Submanifold in
  Euclidean Space by the Gauss Map*, author manuscript:
  https://www.math.stonybrook.edu/~anderson/compactif.pdf . Downloaded and
  text-inspected, especially the curvature-decay discussion, Theorem 5.1
  (end multiplicities), and Theorem 5.2 (one-ended rigidity). The manuscript
  assumes connected complete minimal immersions. This is a cited theorem,
  not a newly proved classification in this packet.
- Yi-Bing Shen and Xiao-Hua Zhu, *On stable complete minimal hypersurfaces
  in R^(n+1)*, American Journal of Mathematics 120 (1998), 103-116,
  https://doi.org/10.1353/ajm.1998.0005 . Its Main Theorem and definition
  of critical curvature were inspected in indexed primary-PDF text at
  https://citeseerx.ist.psu.edu/document?doi=bbf22b57a78d70afadbbcc29456f750461e6d01c&repid=rep1&type=pdf .
  It assumes orientation, stability, and completeness and concludes a
  hyperplane. The proof was not reconstructed in this attempt.
- Xu Cheng, Leung-Fu Cheung, and Detang Zhou, *The structure of weakly
  stable minimal hypersurfaces*, An. Acad. Bras. Cienc. 78 (2006), 195-201,
  https://doi.org/10.1590/S0001-37652006000200001 . Publisher article:
  https://www.scielo.br/j/aabc/a/T3wZVbWYrtDvH4jZ3RK4QyB/?lang=en .
  Corollary 1 explicitly credits and extends Shen-Zhu. The web conversion
  corrupts some >= signs; the stronger/general claim here is taken from
  Shen-Zhu's own displayed Main Theorem rather than those converted signs.
- Helen Elizabeth Moore, *Minimal Submanifolds with Various Curvature
  Bounds*, Stony Brook Ph.D. thesis, May 1995:
  https://www.math.stonybrook.edu/alumni/1995-Moore-Helen.pdf . Downloaded;
  relevant pages rendered and OCR-inspected. Definition: printed p.2;
  two-end statement: pp.3,7-8; end-parallelism lemma and argument:
  pp.12-13. Its two-ended theorem is reported as a source claim; the
  following audit limitation prevents treating its proof as reproduced.
- Qiaoling Wang, *On minimal submanifolds in an Euclidean space*, Math.
  Nachr. (2003), https://doi.org/10.1002/mana.200310120 . Publisher abstract
  inspected: its assumption is super stability, a stronger scalar
  hypothesis in higher codimension. The full proof was not retrieved.
- Ildefonso Castro and Francisco Urbano, *On a minimal Lagrangian
  submanifold of C^n foliated by spheres*, author manuscript dated July
  1998: https://www.ugr.es/~furbano/papers/michigan99.pdf . Downloaded and
  inspected, particularly the introduction and Proposition 1. It provides
  finite-critical-curvature calibrated examples at n=2k and credits
  Harvey-Lawson and Lawlor. These examples lie on the excluded threshold.
- Qi Ding and Lei Zhang, *Topology of complete minimal submanifolds in
  R^(n+m) with finite total curvature*, arXiv:2602.12646v1 (13 February
  2026), https://arxiv.org/html/2602.12646v1 . The introduction, Theorem 1.1,
  curvature estimates, and bibliography were checked. Its finiteness of
  diffeomorphism types under uniform curvature and volume-growth bounds is
  not the requested minimizing-planarity theorem.

## Qualification on Moore's two-end route

In the thesis's proof of its end-parallelism lemma, intersection of distinct
limiting great spheres is used to infer transverse intersection of their
nearby approximating links. The affine-plane calculation in PROOF.md,
Section 3, demonstrates that this inference is not valid from those local
facts alone when the limiting intersection is nontransverse. It is not a
counterexample to Moore's connected minimal two-end theorem. Additional
geometric information or a different argument might validate that theorem.

The corresponding published paper is Helen Moore, *Minimal submanifolds
with finite total scalar curvature*, Indiana University Mathematics Journal
45 (1996), https://doi.org/10.1512/iumj.1996.45.1127 . Its publisher landing
page was retrieved through the Crossref-verified address
https://www.iumj.indiana.edu/IUMJ/fulltext.php?artid=1127&year=1996&volume=45 .
Its linked PDF was subsequently downloaded (23 pages, 270,482 bytes):
https://www.iumj.indiana.edu/IUMJ/FTDLOAD/1996/45/1127/pdf . Theorem 1 on
pp.1023,1025,1028 states the two-end catenoid classification. Lemma 1 and
its proof on pp.1027-1028 retain the same intersection inference. Thus the
proof-dependency caveat applies to the inspected journal argument as well.
This is a scoped limitation of this audit, not a counterexample to that
theorem, a comprehensive erratum search, or a novelty claim. Even if the
published classification is accepted, the campaign target remains unsolved
because arbitrarily many ends have not been excluded.

## Repository and duplicate gate

The live own queue row was queued, 0/5, and its state entry was absent.
The exact attempt directory was absent. ID/code code-searches, ID/title
PR searches across all states, and the exact-ID branch search returned no
matches. No related-target group contained this ID. Pinned-corpus phrase
and subject inspection found no second exact formulation. These checks
cannot rule out differently named or unindexed duplicates. No existing
attempt was overwritten, no queue command was run, and no remote mutation
is part of this source audit.

Only authored discussion and verification metadata are distributable here.
Source PDFs, source full text, dataset records, and unrelated data are
excluded. Mathematical review and publication approval are separate from
the finite verifier succeeding.

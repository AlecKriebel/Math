# Canonical basepoints: a credited negative answer to the nilpotent example

Problem ID: 11000020 / AMR-109-0020. Source: Benson Farb, Problem 2.19, author's book PDF p.30 (printed p.23). Author verification turn: 1/5. Date: 2026-10-03.

## Verdict and scope

The proposed genuswise uniqueness of a surface with a maximal-order **nilpotent full holomorphic automorphism group** is false. In genus 9 there are at least four pairwise nonisomorphic surfaces whose full automorphism groups are nilpotent of order 128, the largest possible order. This follows from a classification table already present in the 2002 version of Magaard–Shaska–Shpectorov–Völklein (MSSV), combined with Zomorrodian's classical bound. It is a credited consequence of prior work, not a new discovery.

This settles the explicit yes/no nilpotent example in Problem 2.19. The surrounding request to find other canonical-point criteria is an open-ended research programme; this note neither exhausts it nor claims a complete new solution to the whole programme. Section 4 records known positive examples. The Hurwitz counting passage after Problem 2.19 belongs to the lead-in to Question 2.20 and is outside this result.

## 1. Exact mathematical target

Work over the complex numbers. Let M_g be the moduli space of compact connected Riemann surfaces of genus g, modulo holomorphic isomorphism, and let Aut(X) mean the full holomorphic automorphism group. Put

    m_full(g) = max{|Aut(X)| : [X] in M_g, Aut(X) nilpotent}.

For the genus used below the maximum exists because the displayed examples make the class nonempty and the Hurwitz bound makes the set of possible orders finite. The uniqueness proposal asserts that exactly one point attains this maximum for each g >= 2. It is enough to disprove it for one genus.

One may instead compare with the maximum order m_sub(g) of a nilpotent subgroup H <= Aut(X), allowing Aut(X) to be nonnilpotent. These are different optimization problems. Our genus-9 examples attain the universal nilpotent-subgroup bound and have nilpotent full automorphism groups, so they disprove uniqueness under either reading without conflating them.

## 2. The prior classification supplies the surfaces

MSSV, *The locus of curves with prescribed automorphism group*, arXiv:math/0205314v1 (30 May 2002), section 7.2, printed/PDF p.14, states that its Table 4 lists actual full automorphism groups, not just subgroups. Table 4, printed/PDF p.17, genus 9, dimension zero, rows 5–8 supplies:

| Row | Full group, Small Groups Library ID | Quotient signature |
| --- | --- | --- |
| 5 | (128,138) | (0;2,4,8) |
| 6 | (128,136) | (0;2,4,8) |
| 7 | (128,134) | (0;2,4,8) |
| 8 | (128,75) | (0;2,4,8) |

The signature's leading zero is restored from the paper's genus-zero convention; the table prints the branch orders (2,4,8). The entries are unchanged in arXiv v2 (12 July 2024), section 7.2 p.15 and Table 4 p.17. Both versions were retrieved, and the original v1 scope and table pages were visually checked.

Let X_i be a surface certified by each row. A group of order 128=2^7 is a finite 2-group, hence nilpotent. Distinct library IDs at the same order specify nonisomorphic abstract groups. If X_i and X_j were holomorphically isomorphic, conjugation by an isomorphism would induce an isomorphism of their **full** automorphism groups. Thus the four points are pairwise distinct in M_9. This is not merely a count of different actions on one curve.

The published classification is an explicit dependency. We have not rerun its BRAID computations or constructed new equations for these four surfaces. The present assertion is only “at least four”; it does not need a claim about the entire census or a least counterexample genus.

## 3. Maximality and a self-contained bound check

Zomorrodian's nilpotent bound gives |H| <= 16(g−1) for every nilpotent H <= Aut(X). It is explicitly recalled as Theorem 2.2(c) in Andreas Schweizer, *Several types of solvable groups as automorphism groups of compact Riemann surfaces*, arXiv:1701.00325, p.5 of the downloaded PDF (printed p.5), with the original reference to Zomorrodian's Theorems 1.8.4 and 2.1.2. The original 1985 AMS PDF was not retrieved (HTTP 403). For transparency, the elementary upper-bound argument is given here.

Let h be the genus of X/H and m_1,...,m_r >= 2 its branch orders. Riemann–Hurwitz says

    2g−2 = |H| D,   D = 2h−2 + sum_i (1−1/m_i) > 0.

We show D >= 1/8. If h >= 2, this is immediate. If h=1, positivity forces r >= 1, giving D >= 1/2. If h=0 and r>=5, D >= 1/2. If h=0 and r=4, positivity excludes four orders 2, so D >= 1/6. Cases r<=2 at h=0 cannot have D>0.

The remaining case is h=0, r=3, with sorted branch orders a<=b<=c and D=1−1/a−1/b−1/c. If 0<D<1/8, elementary reciprocal inequalities leave exactly:

- (2,3,c), 7<=c<=23;
- (2,4,c), c=5,6,7;
- (2,5,5);
- (3,3,4).

For completeness, a>=4 gives D>=1/4. For a=3, b>=4 gives D>=1/6, leaving b=3 and c=4. For a=2, b>=6 gives D>=1/6; b=5 leaves c=5, b=4 leaves 5<=c<=7, and b=3 leaves 7<=c<=23. The case b=2 is nonhyperbolic.

The monodromies x,y,z in H have exact orders a,b,c and xyz=1. In a finite nilpotent group the Sylow subgroups are normal, their product is direct, and elements from distinct Sylow subgroups commute. Therefore:

- For (2,3,c), x and y commute and xy has order 6, contrary to c>=7.
- For (2,4,c), x and y lie in the same Sylow 2-subgroup, so xy has 2-power order, contrary to c=5,6,7.
- For (2,5,5), x and y commute and xy has order 10, contrary to c=5.
- For (3,3,4), x and y lie in the same Sylow 3-subgroup, so xy has 3-power order, contrary to c=4.

All cases are excluded. Hence |H|=(2g−2)/D <= 16(g−1). This is a reconstruction of the classical bound, with no priority claim.

At g=9 the bound is 128. The four classified full groups each have precisely that order. Thus

    m_full(9) = m_sub(9) = 128,

and the full-group maximizer is not unique. As an arithmetic consistency check, the signature gives D=1/8 and 128D=16=2·9−2. This proves the claimed negative answer, conditional only on the explicitly credited existence/fullness entries in MSSV and the standard uniformization and group-theoretic facts above.

## 4. Existing positive canonical-point criteria

Reyes-Carocca–Speziali, *Classifying compact Riemann surfaces by number of symmetries*, arXiv:2310.07520v2 (31 January 2025), Theorem 3.1, printed/PDF p.5, proves these automorphism-theoretic uniqueness criteria:

- For every odd g>=3 with g!=21, the existence of a subgroup of Aut(X) of order 3g singles out one point of M_g.
- For every even g>=4 with g not congruent to 2 modulo 3, the existence of a subgroup of order 3g+3 singles out one point.

These are subgroup-existence predicates on the full automorphism group, not assertions that its total order equals the specified number. Theorem 3.1 explicitly excludes g=21 from the odd-genus uniqueness result; the abstract omits that exception and must not be used as the exact statement. These credited positive examples answer instances of the broader request but do not classify all possible criteria or all genera.

## 5. What was checked, and what was not

The source statement, MSSV v1 scope and table, MSSV v2 matching entries, and the precise 2025 positive theorem were checked. Exact arithmetic and signature-exclusion controls are in verify.py. They supplement the argument and do not replace the published classification or reproduce its computational proof. No new genuswise classification, least counterexample claim, full Hurwitz count, or novelty certification is made.

OpenAI tools assisted source research, reconstruction, drafting, and verification. Independent review is pending at this freeze; this is not formal verification or human peer review.

## References

- Farb, Problem 2.19: https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf#page=30
- MSSV original version: https://arxiv.org/pdf/math/0205314v1#page=14 and https://arxiv.org/pdf/math/0205314v1#page=17
- MSSV updated version and bibliographic history: https://arxiv.org/abs/math/0205314
- Zomorrodian (1985), *Nilpotent automorphism groups of Riemann surfaces*, Trans. Amer. Math. Soc. 288, 241–255, DOI https://doi.org/10.1090/S0002-9947-1985-0773059-6
- Schweizer, Theorem 2.2(c): https://arxiv.org/abs/1701.00325
- Reyes-Carocca–Speziali, Theorem 3.1: https://arxiv.org/pdf/2310.07520v2#page=5

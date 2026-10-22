# Exact finite contract for the rank six positive lemma

This document spells out the finite serialization and verification contract used in the accepted rank-six proof and complete audit. It describes the already audited collection and checks; it does not distribute the raw witnesses or programs and is not an independent new proof of the finite lemma.

## Mathematical input domain

The six old vectors are the rows of a unit-lower-triangular binary matrix L. A root is an integer from 0 through 32,767. Its fifteen binary digits, beginning with the least significant digit, specify entries (1,0), (2,0), (2,1), (3,0), and so on, in row-major strict-lower-triangle order through (5,4). The diagonal is fixed at one and entries above it at zero.

Coordinates of a vector are stored with position zero as the least significant bit. The three exceptional strings 011111, 101111, and 100011, read in increasing position order, are respectively masks 62, 61, and 49. Every root is paired with each of those three masks. There are exactly 32,768×3=98,304 inputs, with no omitted, duplicate, or extra input. No input is rejected because the seven-label restriction fails to have an a-first successful word.

For each pair, append the vector a as formal label 6 to the six row vectors of L, labelled 0 through 5. The full initial seven-by-seven matrix is their dot-product Gram matrix over F₂, with independently checked rank six. The initial word is (0,1,2,3,4,5); literal pressing must clear all seven rows and columns, and its recovered profile at label 6 must equal a.

## Record format

The audited serialization consists of one JSON object per line, with exactly one root record for each of the 32,768 roots. Each object has exactly two fields, root and entries. Root is an integer in the stated domain; Boolean values are not accepted as integers. Entries is an array of exactly three objects, with each exceptional mask occurring exactly once. Root-record order and exceptional-entry order are not needed for correctness; domain and uniqueness are checked explicitly.

Each entry has exactly the fields a, kind, and path. Field a is an integer exceptional mask, excluding Boolean values. Field kind is either profile or first. Path is an array containing one or two words; it omits the fixed initial word and lists the successive destinations. Each word is an array of exactly six distinct integer labels in the range 0 through 6, with Boolean labels rejected. Consecutive words, including the initial-to-first step, must be different.

The format thus encodes one or two nonidentity edges for every input. The mathematical lemma only needs an upper bound of two; the supplied positive collection has no zero-edge entry. Exactly two entries have two edges: root 15,845 with mask 62 and root 31,602 with mask 62.

## Literal verification of every witness

For every initial and path word, the verifier retains the entire seven-by-seven state. It requires each pivot to have diagonal one and updates M to M+(Me_v)(Me_v)ᵀ over F₂. After the six distinct pivots, every matrix entry must be zero. An all-white but nonzero residual is not a success.

At each successive pivot position, the current entry of the pivot column at formal label 6 is recorded as the corresponding coefficient bit of a in that word’s trajectory basis. These bits are independently recovered during pressing, rather than taken from the witness generator. Every consecutive word pair is tested by ordinary dynamic-programming LCS, and its LCS must be at least two.

For a profile entry, every path word uses only labels 0 through 5, hence all six old labels. The terminal profile must have odd norm and must not be one of masks 62, 61, or 49. For a first entry, the terminal word must start with label 6, and the vector a must be different from all six old vectors. That last check is stronger than bare legality and is necessary for the proof’s stated injective actual-label lifting branch.

Duplicate-vector inputs are permitted. There are 3,072 of them and every one uses a profile witness. They never press the extra formal duplicate. Every profile path therefore transfers to the original six distinct labels even if the target actual label is one of them, or is another original label with the same quotient vector. Every first path transfers injectively to seven distinct actual labels because of the explicit vector-distinction check.

## Exact complete coverage

All 98,304 initial words and all 98,306 noninitial words were independently replayed, with exactly 98,306 nonidentity edges. Of the 96,308 profile entries, 96,306 have one edge and two have two edges. All 1,996 first entries have one edge. The edge LCS distribution is 986 edges of LCS two, 10,006 of LCS three, 32,727 of LCS four, and 54,587 of LCS five.

The full checks ran in normal Python, -O, and -OO modes, with byte-identical mathematical outputs. They use explicit exceptions, not removable assertions. Nineteen mathematical mutation controls and separate artifact-integrity controls are described in full in the [rank-six audit](RANK_SIX_AUDIT.md).

As a supplementary test, every one of the 98,306 noninitial words was also replayed on the full 66-coordinate Gram matrix containing every vector of F₂⁶ once, plus one extra zero vector and one extra copy of vector 1. Formal labels were mapped to the corresponding vector representatives. All full states cleared in six legal presses, in each optimization mode. The symbolic lifting proof, rather than this fixed-size test, establishes the arbitrary-ambient result.

## How the finite lemma finishes the proof

For any full successful words S and T, let a be the first actual label of T. Initial blackness and a full successful continuation are then guaranteed. A nonexceptional profile gives an at-most-four-edge bridge from the accepted terminal/signature theorem. For an exceptional profile, an old-only profile witness costs at most two edges before that four-edge bridge, giving diameter at most six. A first witness reaches an a-first word, then the fixed-first-label construction costs at most two further edges. The supplied first paths therefore cost at most three edges in total, although the formal at-most-two-edge lemma would give four.

The selected actual vectors span the six-dimensional radical quotient. Restriction commutes with every press at a selected label, so all six pivots are legal in the full matrix and reduce its full rank from six to zero. This clears every omitted coordinate. Literal profile recovery also agrees between the formal model and the full labelled configuration. None of these steps treats a synthetic coordinate as an original label without the required branch conditions.

These statements define exactly what the complete positive verification establishes and how it is used. The full [proof](RANK_SIX_CONNECTIVITY.md) and [audit](RANK_SIX_AUDIT.md) retain all arguments and limitations. The undistributed raw witness collection remains necessary to rerun the entire finite verification.

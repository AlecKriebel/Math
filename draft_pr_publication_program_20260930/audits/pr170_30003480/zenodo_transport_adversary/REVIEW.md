# Independent review of the exact frozen description transport allowance

**Recommendation: PASS for precisely this frozen transport allowance.** No necessary repair was found for the new comparator path. This is not approval to publish, a mathematical-paper review, a package re-review, or an operational closure audit. No actual publication operation occurred in this audit.

## Exact claim and consumed identities

The tested claim is that the candidate adds only one accepted serialization of the frozen submitted HTML description: replace its one paragraph-text `n>=3` and its one paragraph-text `n>=4` with `n&gt;=3` and `n&gt;=4`. Other supplied metadata and the two upload files remain subject to the original repository comparator and runtime record validation. All inputs were read directly before parent feedback. Complete absolute paths, sizes, and SHA-256 values are in `PINNED_INPUTS.json`.

| Input | Bytes | SHA-256 |
|---|---:|---|
| Candidate `zenodo_exact_description_guard.py` | 2892 | `c1123edaad774444c7b75736744d366ae254f96e4e4b4437324d832c0458be1e` |
| Frozen `publication_package_v2/metadata.json` | 3980 | `8cbaefac015c45839dcf287967bc1f39ad6048259f64ee9fac15b1f15ca783b3` |
| Representation diagnostic | 4465 | `3460ab881825f2d9ffd2762d1a33cef0a6b828b6411951d173aa26273d8e07f1` |
| Original repository `zenodo.py` | 25740 | `a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca` |
| Root publication gate | 13553 | `8e0a97d6c4448c519579597edf62f25acabf601531e7487419a97ae225d4a834` |
| Frozen deposit manifest | 4298 | `0aefa51731f3186c0b06ff0dd3513e18b8471938783efc926315e1289c6031da` |
| PDF | 74051 | `ac0839eae1d0e83e0c47d3c840968363ce9271c83cc9ee88156197601b4d0018` |
| Support ZIP | 147400 | `4df495ac35094dfbacaf4453bde1a71ecae80de23aa50111b3eb7664c2f453e2` |

The frozen metadata matches the manifest metadata exactly, and its hash, both upload artifact hashes, the manifest hash, and the kit hashes agree with the supplied root publication gate. The original `metadata_updates.py` and interpreter executable were additionally pinned. These checks concern the supplied artifacts; the diagnostic is not a fresh independent network observation.

## Deduction about the entire acceptance set

Let `e` be the frozen intended description, and let `c` be the full-string result of the two exact replacements. The candidate first requires submitted metadata to equal the entire frozen metadata dictionary. The new branch is selected only if the remote description equals `c` character for character. In that branch, the candidate constructs a new in-memory metadata dictionary differing only in description and calls the original `verify` with unchanged remote deposit and file arguments. It appends an explanatory allowance only after original verification succeeds.

If the remote description is not `c`, the original `verify` receives the original submitted metadata. For this frozen description, the original plain-text escaping allowance is inapplicable because the description contains HTML paragraph tags; the paragraph-apostrophe allowance is inapplicable because it contains no U+2019 character. The supplied creator has an explicit affiliation, so the omitted-affiliation allowance cannot mask creator changes. Therefore the description can pass only as `e` or `c`, and `c` is the sole newly accepted value. This conclusion follows from complete-string equality and the original verifier's conditions, rather than from interpreting arbitrary HTML as equivalent.

An independent stdlib `HTMLParser(convert_charrefs=True)` control confirms that `e` and `c` have the same complete decoded text and structure: exactly three `<p>` start/end pairs, with no attributes. Each target occurs once. The two replacements add exactly six characters in total. The decoded semantic check supports the stated preservation of paragraph text; it is not used to widen the guard to other semantically equivalent strings.

## Adversarial controls and runtime checks

The supplied `audit_transport.py` produced **106 passing controls under ordinary Python and 106 under `-O`**. It uses explicit exceptions, not `assert`, and records each expected/observed outcome. Its controls exercise the candidate and the original `verify`, `run`, and `local_state` functions from their actual pinned source. The candidate and original kit were never edited.

- Positive controls show that the original comparator accepts the exact raw description and rejects the observed two-entity diagnostic, while the guard accepts the raw and exactly escaped versions. The new branch yields precisely one description allowance.
- Negative description controls reject single-target escaping, double escaping, decimal/hexadecimal/uppercase entities, omitted semicolons, escaped markup, changed paragraph tags, new attributes, comments, scripts, inline markup, spacing, prose, thresholds, inequality direction, extra target text, missing description, and a non-string description.
- Metadata controls reject author name/ORCID/affiliation changes, extra authors or creator fields, keyword edits/additions/reordering, related identifier/relation/scheme changes, additional or reordered identifiers, title/license changes, missing version, non-object remote metadata, and nonfrozen submitted metadata. Replacing the submitted metadata with an already escaped variant is itself rejected.
- File controls reject extra/missing/duplicate/renamed files, checksum and size changes for either upload, absent checksum/size, malformed file entries, and malformed file lists. Separate owned fixtures flip a byte in each local artifact, load those actual changed bytes with the original manifest loader, and confirm rejection against the original remote checksums.
- Original record controls reject wrong, string, float, boolean, or absent IDs and non-boolean submitted states. Full candidate-main controls reject a missing or uncleared transport gate, a changed guard identity, an unexpected manifest path/hash, a bad kit pin, absent/empty/wrong local state, changed state manifest/environment, and missing/wrong explicit confirmation ID. These failures produce no synthetic publication call.
- Full candidate-main controls also show that partial escaping, prose changes, author edits, extra files, and a bad checksum prevent the publication sentinel. Valid raw/exact-escaped drafts reach exactly one synthetic publication sentinel; an already submitted valid fixture reaches none. All sentinels target only draft `23318851`.

Successful full-main controls use an in-memory synthetic transport gate because the real transport gate did not exist when the audit began. Original runtime functions are loaded unchanged. The harness redirects the state path to an owned synthetic fixture and replaces only credential retrieval, the network client, state persistence, and DOI probing with local sentinels. A Python audit hook rejects every socket event and any attempt to open `.secrets` or `.zenodo-state`. Both runs record zero network attempts and zero credential/private-state read attempts. The real candidate's self-identity and manifest/kit pin checks still execute in these controls. No secret or actual private state was read.

## Preserved original behavior and precise limits

The original kit compares all supplied metadata keys, not every server-generated extra metadata key. Its existing file representation rules accept remote file order changes, an `md5:` checksum prefix, checksum letter case, and a size string matching the local size. Separate controls demonstrate that these pre-existing behaviors are unchanged by the transport guard. This review does not mislabel them as new transport permissions or claim a stricter original comparator than the source implements.

The supplied gate and frozen inputs are the trust boundary of this bounded audit. This report does not establish immutable authenticity of all mutable local control files, absence of races in an actively modified workspace, fresh account ownership, or current remote state. It does not permit coordinated local-and-remote artifact replacement, general HTML canonicalization, other paragraph escaping, alternate entities, future metadata changes, or another deposit ID. If any pinned candidate, frozen metadata, manifest, kit, diagnostic, PDF, or ZIP identity changes, this PASS does not transfer automatically.

## Reproduction and disposition

Run the owned script with `/opt/homebrew/opt/python@3.14/bin/python3.14 -E -S -B -P`, once ordinarily and once with `-O`, supplying `--output controls.normal.json` and `--output controls.optimized.json` respectively. The runtime is Python 3.14.6. Both result files retain all controls and the exact HTML semantic hashes; the input pin inventory makes the consumed version checkable. The harness creates and deletes only owned synthetic state/corrupt-file fixtures.

No necessary comparator fix remains. Estimated completion of this narrow audit: **100%**. This disposition is solely `PASS_FOR_PRECISELY_THIS_FROZEN_TRANSPORT_ALLOWANCE`. Publication authorization and actual publication remain with the parent/human workflow.

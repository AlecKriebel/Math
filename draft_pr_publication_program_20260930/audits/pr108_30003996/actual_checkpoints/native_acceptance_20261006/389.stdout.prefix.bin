# Reviewer predicate corrections

The initial review script stopped at the independent projection-drift check.
It incorrectly defaulted every absent local state to `queued`, although the
preserved baseline includes `unreviewed` and other source-derived defaults.
This generated 13,555 false projected differences. The independent check now
retains the established default for records without an explicit local state,
and derives changes from the actual full local state map and the native
eligible statuses `queued`, `unreviewed`, `ready`. The initial source is
preserved as `audit_initial_assumptions_v1.py`. This was a reviewer predicate
error, not a candidate defect.

Before the next run, the reviewer aligned the independent control digest with
the declared sorted, indented JSON plus trailing newline representation,
corrected the expected location of the archived package manifest, and checked
the actual started record's recorder/argv/UTC/cwd fields without inventing a
child PID field that this outer started schema does not contain.

No candidate, helper, input, gate, source, native baseline or private
configuration was changed by these corrections.

The second predicate version stopped at the full hold tally: the native
summary intentionally groups holds by the prefix before a colon, whereas the
first independent tally counted each `possible_duplicate_of:<id>` separately.
Those 35 holds correctly appear as one category with count 35. The reviewer
corrected this aggregation and retained the failed real run (PID 68340,
exit 1) and source `audit_predicate_v2_before_hold_tally_correction.py`.

PID 68834 stopped at the diagnostic README comparison. The candidate uses the
explicitly reviewed native integration README at the current target root;
the superseded diagnostic README remains exact in captured inputs. The
reviewer corrected this expected wrapper mapping, requires its concrete
effort/status/prior/DOI/ranking disclosures, and separately checks preservation
of the former README. All nine other diagnostic artifacts remain exact at
their current paths. The failed run and predicate version are retained.

PID 69429 reached the private-body omission check and exposed a reviewer
path-composition mistake: joining an absolute private path to the bundle
discarded the bundle prefix and tested the existing private original. The
corrected predicate strips the leading slash for that bundle location check
and additionally compares every offered SHA against private configuration
body SHAs. It never opens or discloses those private bodies. The real failed
run and source version are preserved; no candidate correction was required.

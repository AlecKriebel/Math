"""Comment-only editorial pass, with independently checked code preservation."""
from pathlib import Path
import ast
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent / 'lean_formalization'
OUT = Path(__file__).resolve().parent
scanner_source = (ROOT / 'scripts/static_audit.py').read_text()
node = next(n for n in ast.parse(scanner_source).body
            if isinstance(n, ast.FunctionDef) and n.name == 'strip_comments_strings')
scope = {}
exec(compile(ast.Module(body=[node], type_ignores=[]), '<existing scanner>', 'exec'), scope)
strip_comments_strings = scope['strip_comments_strings']

def comment_spans(s):
    """Locate only comments, leaving quoted strings and every code byte intact."""
    result = []
    i = 0
    while i < len(s):
        if s[i] == '"':
            i += 1
            while i < len(s):
                if s[i] == '\\':
                    i += 2
                elif s[i] == '"':
                    i += 1
                    break
                else:
                    i += 1
        elif s.startswith('--', i):
            end = s.find('\n', i)
            if end < 0:
                end = len(s)
            result.append((i, end))
            i = end
        elif s.startswith('/-', i):
            start = i
            depth = 1
            i += 2
            while depth:
                if s.startswith('/-', i):
                    depth += 1
                    i += 2
                elif s.startswith('-/', i):
                    depth -= 1
                    i += 2
                else:
                    if i >= len(s):
                        raise ValueError('Unclosed comment')
                    i += 1
            result.append((start, i))
        else:
            i += 1
    return result

def outside_segments(s):
    result = []
    end = 0
    for a, b in comment_spans(s):
        result.append(s[end:a])
        end = b
    result.append(s[end:])
    return result

headers = {
'AdversarialStatements.lean': 'Expanded statement contracts for the adversarial models and bounds.\nThe examples expose the quantified physical definitions and endpoint statements.',
'D4.lean': 'Target-only d=4 realization and its Born distribution. This module assumes\nno universal Bell bound or Bell maximality. Phases.lean identifies its constants\nwith the manuscript exponential phases.',
'GeneralBehavior.lean': 'Real behavior arrays and the manuscript Bell functionals. Continuity uses\nthe ordinary product topology and does not assume a quantum model is closed.\nThe reduced and augmented Bob input alphabets remain separate.',
'GeneralBinary.lean': 'Binary benchmark: the two-square SOS and privacy from on-state relations.\nNo global anticommutation is inferred from saturation. The private conditional\nstates use GeneralOperational\'s measurement sandwich and partial trace.\nThis benchmark is prior art.',
'GeneralBinaryModels.lean': 'Binary benchmark on arbitrary complete Hilbert spaces and q/qa/qc values.\nThe Hilbert-space bound follows from an algebraic SOS. The separate finite-Eve\nprivacy theorem is not extended to infinite-dimensional privacy. This benchmark\nis prior art.',
'GeneralConsequences.lean': 'Physical Fourier privacy, value-only counterexamples and exact entropy\narithmetic. Explicit guesses provide lower bounds; optimal adversarial success\nover the whole maximizing face is not asserted.',
'GeneralCoverageSourcePolar.lean': 'Source-convention identities for manuscript app:attainment, using the\npositive clock and forward shift. The relative weighted cycle is unitary and\nits spectrum satisfies the equality-root power equation.',
'GeneralModelCounterexamples.lean': 'The nonuniform physical witnesses maximize the literal model suprema.\nMembership, value and Born distribution use the same witness throughout.\nNo optimality claim for Eve is made.',
'GeneralPOVMMaximum.lean': 'Every fixed finite-Eve POVM objective has an attained maximum.\nThe proof uses compactness of Gram factors with an arbitrary-dimension bound.\nIt asserts no maximum over all physical realizations.',
'GeneralPhaseBounds.lean': 'Exact maxima and nonuniformity of the physical settings-appendix tables.\nThese are properties of an explicit realization, not a self-testing theorem\nor a no-go theorem for all two-input experiments.',
'GeneralPhaseTables.lean': 'Fourier-phase measurements in the settings appendix. These are actual PVMs\nand Born probabilities on Phi_d. No Bell maximum, uniformity, or formula for\nthe answer is a validity field. Alice\'s vectors have negative Fourier sign;\nBob\'s have positive Fourier sign. The scalar displacement uses the ordinary\ninteger lifts a.val-b.val+alpha-beta.',
'GeneralRigidity.lean': 'Finite-dimensional supported-multiplicity rigidity. The final theorem\nstarts with an arbitrary mixed-state PVM strategy and its actual first-family\nvalue. Support cancellation, invariance, polar kernels, reflection powers and\ndimension summation are derived. No commuting-model rigidity is asserted.',
'GeneralSecondWitness.lean': 'Second augmented-family attainment and nonuniform witnesses for every d>=4.\nThe construction connects the coefficient phases, complete PVMs, attained value\nand target-measurement identification.',
'GeneralSourceFourier.lean': 'Source appendix coefficient calculations with the positive clock and\nforward shift. These DFT identities are used with the source polar-factor and\nmeasurement-order proofs in the GeneralCoverageSource modules.',
'GeneralStatements.lean': 'Expanded all-dimensional statement contracts. The examples expose the\nphysical hypotheses and conclusions separately from their proofs.',
'ModelValueStatements.lean': 'Expanded model and value statement contracts. The examples expose physical\ndefinitions, arbitrary dimensions, real Born arrays, topological closure and\nthe three supremum operators.',
'Statements.lean': 'Expanded statement correspondence checks, separate from the proofs.\nThe examples expose the finite physical model through its density and projectors\nand are included in the standard library build.',
}

replacements = [
    ('These source declarations have NOT been compiled or kernel checked. The claims\nbecome formal results only after the pinned offline build and statement audit.\n', ''),
    ('UNCOMPILED SOURCE CANDIDATES; pinned-library elaboration remains untested.', ''),
    ('UNCOMPILED SOURCE CANDIDATES: no axiom output or kernel checking exists yet.', ''),
    ('All declarations are UNCOMPILED SOURCE CANDIDATES, not accepted Lean theorems.', ''),
    ('UNCOMPILED SOURCE; pinned API usage and all proof terms need an offline build.', ''),
    ('UNCOMPILED SOURCE: acceptance and dependency reports require the offline run.', ''),
    ('SOURCE CANDIDATE: this file has not been run through Lean.', ''),
    ('SOURCE CANDIDATE. No Lean invocation has been performed on this file.', ''),
    ('UNCOMPILED: all declarations are proof candidates until the offline clean run.', ''),
    ('UNCOMPILED: these controls have not been run by Lean.', ''),
    ('UNCOMPILED: this is not a claimed kernel-checked theorem.', ''),
    ('All proofs are uncompiled candidates; no verification status is inferred.', ''),
    ('Every statement below is an UNCOMPILED SOURCE CANDIDATE.', ''),
    ('All statements are UNCOMPILED SOURCE CANDIDATES.', ''),
    ('All declarations are UNCOMPILED SOURCE CANDIDATES.', ''),
    ('All proofs are uncompiled source candidates.', ''),
    ('These are uncompiled proof candidates.', ''),
    ('All proofs are uncompiled candidates.', ''),
    ('All results are uncompiled.', ''),
    ('These are UNCOMPILED proof-script candidates.', ''),
    ('Uncompiled proof-source candidates.', ''),
    ('UNCOMPILED SOURCE CANDIDATES.', ''),
    ('UNCOMPILED SOURCE CANDIDATE.', ''),
    ('UNCOMPILED SOURCE.', ''),
    ('Uncompiled source candidates.', ''),
    ('Uncompiled source candidate.', ''),
    ('Uncompiled source.', ''),
    ('Uncompiled.', ''),
    ('SOURCE CANDIDATE: not yet compiled in the cloud.', ''),
    ('SOURCE CANDIDATE.', ''),
    ('Public d=4 endpoint candidates', 'Public d=4 endpoints'),
    ('Unconditional physical upper-bound candidates.', 'Unconditional physical upper bounds.'),
    ('End-to-end source candidate for', 'Physical attainment and nonuniformity for'),
    ('Proposed closed form, kept independent of the Born-rule definition.',
     'Closed form, defined independently of the Born-rule expression.'),
    ('The actual first functional is evaluated, not merely its candidate factors.',
     'Evaluation of the actual first functional.'),
    ('Physical nonuniformity for every d>=4; this is NOT yet a Bell optimality claim.',
     'Physical nonuniformity for every d>=4; Bell optimality is proved separately.'),
    ('Positive controls, executed only by the offline build.',
     'Positive controls for the validation runner.'),
    ('The value proof does not need, and does not claim, Q_qa⊆Q_qc or closedness of Q_qc.',
     'The value proof is independent of the closure-containment theorem.'),
    ('Kernel-checked algebraic infrastructure for the literal source/polar bridge.',
     'Algebraic infrastructure for the literal source/polar bridge.'),
    ('Complete library target: original results, new coverage, expanded contracts,',
     'Complete library target: mathematical results, statement contracts,'),
]

def edit_comment(c, name, first_header):
    if first_header and c.startswith('/-!') and name in headers:
        return '/-! ' + headers[name] + ' -/'
    out = c
    for old, new in replacements:
        out = out.replace(old, new)
    if out != c:
        # Formatting changes remain strictly within the comment span.
        out = re.sub(r' +\n', '\n', out)
        out = re.sub(r'\n{3,}', '\n\n', out)
        out = re.sub(r'\n\s*\n-/$', '\n-/', out)
        out = re.sub(r'\n[ ]+-/$', '\n-/', out)
    return out

def digest(s):
    return hashlib.sha256(s.encode()).hexdigest()

files = sorted((ROOT / 'CyclicBell').glob('*.lean')) + [ROOT / 'CyclicBell.lean']
files += sorted((ROOT / 'validation').glob('*.lean'))
files = [p for p in files if p.name != 'AxiomAudit.lean']
records = []
before_changed = {}
baseline_path = OUT / 'comment_cleanup_before.json'
baseline = json.loads(baseline_path.read_text()) if baseline_path.exists() else {}
for p in files:
    rel = str(p.relative_to(ROOT))
    old = baseline.get(rel, p.read_text())
    assert outside_segments(old) == outside_segments(p.read_text()), p
    new = old
    first_header_start = next((a for a, b in comment_spans(old) if old[a:b].startswith('/-!')), None)
    for a, b in reversed(comment_spans(old)):
        new = new[:a] + edit_comment(old[a:b], p.name, a == first_header_start) + new[b:]
    old_segments, new_segments = outside_segments(old), outside_segments(new)
    assert old_segments == new_segments, p
    old_mask = strip_comments_strings(old)
    new_mask = strip_comments_strings(new)
    old_clean = re.sub(r'\s+', '', old_mask)
    new_clean = re.sub(r'\s+', '', new_mask)
    assert old_clean == new_clean, p
    record = {
        'path': str(p.relative_to(ROOT)), 'changed': old != new,
        'before_sha256': digest(old), 'after_sha256': digest(new),
        'outside_comment_segments_sha256': digest(json.dumps(old_segments, ensure_ascii=False)),
        'outside_comment_segments_exactly_equal': True,
        'normalized_strip_comments_strings_before_sha256': digest(old_clean),
        'normalized_strip_comments_strings_after_sha256': digest(new_clean),
        'normalized_strip_comments_strings_exactly_equal': True,
        'raw_mask_equal': old_mask == new_mask,
    }
    records.append(record)
    if old != new:
        before_changed[str(p.relative_to(ROOT))] = old
        p.write_text(new)

(OUT / 'comment_cleanup_before.json').write_text(json.dumps(before_changed, ensure_ascii=False, indent=2)+'\n')
(OUT / 'comment_token_preservation.json').write_text(json.dumps({
    'scanner_source_sha256': digest(scanner_source),
    'checked_files': len(records),
    'changed_files': sum(r['changed'] for r in records),
    'records': records,
}, indent=2)+'\n')
print(json.dumps({'checked': len(records), 'changed': sum(r['changed'] for r in records)}, indent=2))

"""Read-only source comparisons for the bounded v1.0.11 proofreading round."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE.parent / 'source_snapshot'
REPO = HERE.parents[2]
PREFIX = HERE.parents[1].name
OLD = '953c836a12b9d9d474521feb4a96e218c1155203'
NEW = '137ffa9f1a340f621651395ad0236cf1bdadb51c'

def old(relative):
    return subprocess.check_output(['git','show',f'{OLD}:{PREFIX}/{relative}'],cwd=REPO).decode()

def current(relative):
    return (SNAPSHOT/relative).read_text()

def require(value, label):
    if not value:
        raise RuntimeError(label)

def selected(text, mode):
    text = text.replace(r'\newif\ifsiadsreview','')
    output = []
    stack = []
    active = True
    pos = 0
    for match in re.finditer(r'\\ifsiadsreview|\\else\b|\\fi\b',text):
        if active:
            output.append(text[pos:match.start()])
        token = match.group()
        if token == r'\ifsiadsreview':
            stack.append(active)
            active = active and mode
        elif token == r'\else':
            require(bool(stack),'conditional else without if')
            active = stack[-1] and not mode
        else:
            require(bool(stack),'conditional fi without if')
            active = stack.pop()
        pos = match.end()
    require(not stack,'unclosed conditional')
    if active:
        output.append(text[pos:])
    return ''.join(output)

def compact(text):
    return re.sub(r'\s+','',text)

def formula_tokens(text):
    text = re.sub(r'\\(?:begin|end)\{(?:split|aligned)\}','',text)
    text = re.sub(r'\\(?:quad|qquad)\b','',text)
    text = text.replace(r'\[','').replace(r'\]','').replace(r'\\','')
    return compact(text.replace('&','').replace(',','').replace('.',''))

checks = {}
for relative in ['external_audit/theorem_summary.tex','external_audit/proof_skeleton.tex',
                 'data/certificate_tables.tex','data/contrast_table.tex',
                 'independent_verifier/improved_modulus_certificate.json',
                 'independent_verifier/pareto_all_m_certificate.json',
                 'independent_verifier/frontier_certificate.json']:
    require(old(relative) == current(relative),'unexpected source drift: '+relative)
    checks[relative] = {'byte_identical_to_v1_0_10':True,
                        'sha256':hashlib.sha256((SNAPSHOT/relative).read_bytes()).hexdigest()}

main_before = old('manuscript/main.tex')
main_after = current('manuscript/main.tex')
marker = r'\paragraph{Data and code availability.}'
require(compact(selected(main_before,False).split(marker)[0]) ==
        compact(selected(main_after,False).split(marker)[0]),'canonical main substantive source drift')
checks['canonical_main_before_release_metadata'] = 'identical after selecting canonical layout and ignoring whitespace'

for relative in ['manuscript/supplement.tex','data/sign_certificate_tables.tex']:
    require(compact(selected(old(relative),False)) == compact(selected(current(relative),False)),
            'canonical source drift: '+relative)
    checks[relative] = 'identical after selecting canonical layout and ignoring whitespace'

start = r'\paragraph{Reference coefficient $R_m$.} Define'
end = 'After $m=u+3$'
before_pr = selected(old('data/sign_certificate_tables.tex'),True).split(start,1)[1].split(end,1)[0]
after_pr = selected(current('data/sign_certificate_tables.tex'),True).split(start,1)[1].split(end,1)[0]
require(formula_tokens(before_pr) == formula_tokens(after_pr),'SIADS reference coefficient formula drift')
checks['SIADS_P_R_and_R_m'] = 'identical mathematical tokens after removal of layout and terminal punctuation'

start = 'At onset for the unit-equilibrium family, write'
end = 'The identity $c^TA_m=0$'
before_spaces = selected(old('manuscript/supplement.tex'),True).split(start,1)[1].split(end,1)[0]
after_spaces = selected(current('manuscript/supplement.tex'),True).split(start,1)[1].split(end,1)[0]
require(formula_tokens(before_spaces) == formula_tokens(after_spaces),'SIADS fixed-mass spaces drift')
checks['SIADS_operator_and_fixed_mass_spaces'] = 'identical mathematical tokens after removal of layout'

proof_changes = subprocess.check_output(['git','diff','--name-only',OLD,NEW,'--',PREFIX+'/proof_audit'],cwd=REPO).decode().splitlines()
require(not proof_changes,'unexpected proof_audit changes')
checks['proof_audit_tree'] = 'unchanged'

result = {'status':'PASS','target':NEW,'comparison':OLD,
          'timestamp_utc':datetime.now(timezone.utc).isoformat(),
          'checks':checks,
          'scope':'Source identity and mathematical-layout equivalence; no PDF visual, build, or verifier claim.'}
(HERE/'MATH_SOURCE_EQUIVALENCE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

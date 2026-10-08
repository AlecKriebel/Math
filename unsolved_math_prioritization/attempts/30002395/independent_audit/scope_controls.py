#!/usr/bin/env python3
"""Exact bounded regressions for analytical controls proved in AUDIT.md.

The real-line arguments are mathematical proofs in the report. Rational samples
here do not certify an infinite topology or replace those proofs.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import hashlib,json,subprocess,tempfile,shutil
C=Counter()
def check(x,label):
    if not x:raise AssertionError(label)
    C[label]+=1
root=Path(__file__).resolve().parent
original=root.parent/'public'
old='A pseudo-open map to a T1 target is open.'
new='A continuous pseudo-open map to a T1 target is open onto its image; it is open into the target when it is also surjective.'
for name in ('PROOF.md','TURN_2.md'):
    before=(original/name).read_text();after=(root/'corrected'/name).read_text()
    check(before.count(old)==1 and old not in after and after.count(new)==1,'standalone_scope_sentence_corrected')
    check(before.replace(old,new)==after,'exact_one_sentence_patch')
for p in original.iterdir():
    if p.is_file() and p.name not in ('PROOF.md','TURN_2.md','MANIFEST.json'):
        check(p.read_bytes()==(root/'corrected'/p.name).read_bytes(),'unaffected_author_file_unchanged')
for i in range(1,6):
    check((root/'corrected'/f'TURN_{i}.md').read_text().rstrip() in (root/'corrected'/'PROOF.md').read_text(),'corrected_turn_matches_full_proof')
# Apply the actual supplied patch to temporary copies, then compare exact bytes.
with tempfile.TemporaryDirectory(prefix='dini_patch_replay_') as d:
    for name in ('PROOF.md','TURN_2.md'):shutil.copyfile(original/name,Path(d)/name)
    r=subprocess.run(['patch','-p1','-i',str(root/'CORRECTION.patch')],cwd=d,capture_output=True,text=True)
    check(r.returncode==0,'actual_unified_patch_applies')
    for name in ('PROOF.md','TURN_2.md'):
        check((Path(d)/name).read_bytes()==(root/'corrected'/name).read_bytes(),'actual_patch_matches_corrected_copy')
# Non-surjective Q={q}->R, q maps to zero. R_f={(q,q)} and its projection
# is the singleton identity. All domain opens and invariant images are checked.
Q=frozenset({'q'});opens={frozenset(),Q};R=frozenset({('q','q')})
for W in (frozenset(),R):
    check(frozenset(p for p,q in W) in opens,'singleton_pseudograph_projection_open')
for V in opens:
    invariant=all(q not in V or p in V for p,q in R)
    image=frozenset({0}) if V else frozenset()
    check(invariant and image in {frozenset(),frozenset({0})},'singleton_invariant_image_relatively_open')
check(1 not in {0},'singleton_map_misses_closed_singleton_one')
# For arbitrary real r>0, r/2 is in (-r,r) and is not zero. These exact
# rational instances check the expression used by the analytical proof.
for n in range(1,129):
    r=Fraction(1,n);w=r/2
    check(-r<w<r and w!=0,'real_line_nonopen_singleton_rational_witness')
    # The same shrinking intervals have relatively full trace on U={0}.
    check(-r<0<r and w not in {0},'closed_chart_intervals_do_not_make_U_open')
# Exact finite prefixes illustrate, but do not prove, the infinite intersection.
for n in range(1,129):
    lower=max(-Fraction(1,k) for k in range(1,n+1))
    upper=min(Fraction(1,k) for k in range(1,n+1))
    check(lower==-Fraction(1,n) and upper==Fraction(1,n),'shrinking_interval_finite_prefix')
print(json.dumps({'status':'PASS','checks_by_category':dict(C),'total_checks':sum(C.values()),
 'analytical_negative_controls':[
 {'name':'pseudo_open_into_T1_need_not_be_ambient_open','map':'{q} -> R, q -> 0','formal_topology_certification':False,'proof':'AUDIT.md section 2'},
 {'name':'open_chart_identity_fails_for_closed_chart','space':'R; U={0}; V_n=(-1/n,1/n)','formal_topology_certification':False,'proof':'AUDIT.md section 6'}],
 'scope':'Exact finite regressions plus explicitly labelled rational samples. Infinite assertions require the written arguments.'},indent=2,sort_keys=True))

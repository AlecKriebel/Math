#!/usr/bin/env python3
"""Comparison harness only. Imports both separately implemented oracles.
The independently authored oracle itself does not import the author's code.
"""
import argparse,importlib.util,json,hashlib
from pathlib import Path
from fractions import Fraction as Q
from itertools import product

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def main():
    ap=argparse.ArgumentParser();ap.add_argument('author_release',type=Path);args=ap.parse_args()
    author=load(args.author_release/'verify_math.py','author_oracle')
    auditor=load(Path(__file__).resolve().parent/'independent_controls.py','audit_oracle')
    words=json.loads((args.author_release/'MATH_CHECKS.json').read_text())['words']
    rats=sorted({Q(p,n) for n in range(1,6) for p in range(n)})
    entries=[];configs=0;reversals=0;swaps=0;nonextremal_violations=[]
    def normalized(word):
        i=next(i for i,c in enumerate(word) if c=='a' and word[i-1]=='b')
        return word[i:]+word[:i]
    def audit_max(word,r,s):
        ph=auditor.phases(normalized(word))
        return max(auditor.orbit_data(t,r.numerator,s.numerator,ph,deep=False) for t in auditor.compositions(s.denominator,r.denominator))
    for r,s in product(rats,repeat=2):
        for word in words:
            vals=[];ph=auditor.phases(word)
            for gaps in auditor.compositions(s.denominator,r.denominator):
                W=''.join('X'+'Y'*t for t in gaps)
                a=author.rot(W,word,r.numerator,s.numerator)
                b=auditor.orbit_data(gaps,r.numerator,s.numerator,ph,deep=False)
                if a!=b:raise RuntimeError(f'configuration mismatch {word} {r} {s} {gaps}: {a} != {b}')
                configs+=1;vals.append(a)
            R=max(vals)
            for value in vals:
                if value<R and value-word.count('a')*r-word.count('b')*s>Q(len(ph),value.denominator):
                    nonextremal_violations.append({'word':word,'r':str(r),'s':str(s),'value':str(value),'R':str(R)})
            if audit_max(word[::-1],r,s)!=R:raise RuntimeError('independent reversal failure')
            reversals+=1
            swapped=word.translate(str.maketrans('ab','ba'))
            if audit_max(swapped,s,r)!=R:raise RuntimeError('independent swap failure')
            swaps+=1
            entries.append({'word':word,'r':str(r),'s':str(s),'R':str(R),'configurations':len(vals)})
    raw=(json.dumps(entries,sort_keys=True,separators=(',',':'))+'\n').encode()
    print(json.dumps({'status':'PASS_EXACT_CROSS_IMPLEMENTATION_COMPARISON','configurations_compared':configs,'parameter_word_cases':len(entries),'independent_reversal_cases':reversals,'independent_generator_swap_cases':swaps,'nonextremal_step_model_violations':nonextremal_violations,'case_stream_sha256':hashlib.sha256(raw).hexdigest(),'case_stream_bytes':len(raw),'scope':'Agreement between two finite implementations is a diagnostic cross-check, not a proof of the infinite conjecture.'},indent=2,sort_keys=True))
if __name__=='__main__':main()

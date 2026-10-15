import hashlib, json, pathlib, shutil
root=pathlib.Path(__file__).resolve().parent
base=root/'private/extracted'
mutants=root/'private/mutants'
mutants.mkdir(parents=True,exist_ok=True)
source=(base/'verify_even_calculus.py').read_text()
cases={
 'BL_wrong_buffer': source.replace('else: pair = (State(n,shift(a)+s(1,-1)+shift(b)+s(1)+s(n-1)), State(n,shift(a)+v(1)+shift(b)+v(1)+s(n-1)))', 'else: pair = (State(n,shift(a)+s(1,-1)+shift(b)+s(1)+s(n-2)), State(n,shift(a)+v(1)+shift(b)+v(1)+s(n-2)))'),
 'left_shift_erased': source.replace('i + 1, e) for t, i, e in w)', 'i, e) for t, i, e in w)'),
 'terminal_sign_lost': source.replace('if kind == "T": pair = (State(n,b+s(n-1)), State(n,b+g))', 'if kind == "T": pair = (State(n,b+s(n-1)), State(n,b+s(n-1)))'),
}
rows=[]
for name,body in cases.items():
    assert body!=source,name
    path=mutants/name
    path.mkdir(exist_ok=True)
    (path/'verify_even_calculus.py').write_text(body)
    rows.append({'name':name,'source_sha256':hashlib.sha256(body.encode()).hexdigest()})
for name,target in [('checksum_tex_corrupted','even_strand_markov.tex'),('checksum_result_corrupted','expected_results.json')]:
    dest=mutants/name
    dest.mkdir(exist_ok=True)
    for p in base.iterdir():
        if p.is_file() and p.name not in ('even-strand-markov-verification-v2.zip','even_strand_markov.pdf','even_strand_markov.log'):
            shutil.copyfile(p,dest/p.name)
    path=dest/target
    path.write_bytes(path.read_bytes()+b'\nCORRUPTED_REVIEW_CONTROL\n')
    rows.append({'name':name,'target':target,'mutated_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(root/'MUTANT_INPUTS.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))

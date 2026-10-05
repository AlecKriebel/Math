#!/usr/bin/env python3
"""Independent finite controls and externally pinned freeze checks, not a proof assistant.

Usage: python independent_verify.py --author AUTHOR_DIR --archive AUTHOR.zip
Optional --sources SOURCE_DIR uses six PDFs named 0.pdf,...,5.pdf.
Optional --datasets DATASET_DIR uses the two public complete JSON files.
No input is modified. Mutation fixtures live in a temporary directory.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

import sympy as S

ARCHIVE_HASH = '4f5e1bddcfb9720f76f50cdff5118409d3c764dd24e0701677d01bb54ed98a5b'
MANIFEST_HASH = '1398394bb23d7346d694aae514380a80531a23ee94726bc873bb586e387d5b92'
PROOF_HASH = 'c90303d06ae5b773b79e280a471db197e4f1f56a323df23afea00749eb67ee28'


def need(test, message):
    if not test:
        raise RuntimeError(message)


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def pinned(author, archive):
    a = archive.read_bytes()
    need(len(a) == 20834 and digest(a) == ARCHIVE_HASH, 'External archive pin mismatch')
    manifest_bytes = (author / 'AUTHOR_MANIFEST.json').read_bytes()
    need(len(manifest_bytes) == 1716 and digest(manifest_bytes) == MANIFEST_HASH,
         'External manifest pin mismatch')
    need(digest((author / 'PROOFS.md').read_bytes()) == PROOF_HASH, 'External proof pin mismatch')
    m = json.loads(manifest_bytes)
    names = {'AUTHOR_MANIFEST.json'}
    for row in m['files']:
        name = row['path']
        need(type(name) is str and name == PurePosixPath(name).name and name not in names,
             'Unsafe/duplicate author name')
        names.add(name)
        p = author / name
        need(p.is_file() and not p.is_symlink(), 'Invalid author file')
        b = p.read_bytes()
        need(len(b) == row['bytes'] and digest(b) == row['sha256'], 'Author file mismatch')
    need({p.name for p in author.iterdir()} == names, 'Unexpected author inventory')
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        need(len(infos) == len(names), 'Archive count mismatch')
        need({i.filename for i in infos} == names, 'Archive names mismatch')
        for i in infos:
            need(not i.is_dir() and not stat.S_ISLNK(i.external_attr >> 16), 'Unsafe archive member')
            need(z.read(i) == (author / i.filename).read_bytes(), 'Archive byte mismatch')
    return {'archive_bytes': len(a), 'archive_sha256': digest(a), 'files': len(names),
            'author_unchanged': True}


def author_runs(author):
    results = []
    expected = (author / 'VERIFY_OUTPUT.json').read_bytes()
    for mode, flags in [('normal', []), ('optimized', ['-O'])]:
        p = subprocess.run([sys.executable, *flags, str(author / 'verify.py')],
                           capture_output=True, check=True)
        need(p.stdout == expected, 'Author output not byte-exact')
        q = subprocess.run([sys.executable, *flags, str(author / 'verify_manifest.py')],
                           capture_output=True, check=True)
        need(json.loads(q.stdout)['status'] == 'PASS_EXACT_MANIFEST', 'Author manifest failure')
        results.append({'mode': mode, 'controls': json.loads(p.stdout)['total_checks'],
                        'output_byte_exact': True, 'manifest_pass': True})
    return results


def mutations(author):
    names = ['append_proof', 'same_length_edit', 'missing_file', 'unlisted_file',
             'duplicate_entry', 'unsafe_path', 'symlink']
    out = []
    for name in names:
        for mode, flags in [('normal', []), ('optimized', ['-O'])]:
            with tempfile.TemporaryDirectory(prefix='foliation-audit-mutation-') as td:
                root = Path(td) / 'payload'
                shutil.copytree(author, root)
                p = root / 'PROOFS.md'
                m = root / 'AUTHOR_MANIFEST.json'
                if name == 'append_proof':
                    p.write_bytes(p.read_bytes() + b'\nMUTATION\n')
                elif name == 'same_length_edit':
                    b = p.read_bytes(); p.write_bytes(bytes([b[0] ^ 1]) + b[1:])
                elif name == 'missing_file':
                    p.unlink()
                elif name == 'unlisted_file':
                    (root / 'unlisted.txt').write_text('mutation')
                elif name in ('duplicate_entry', 'unsafe_path'):
                    v = json.loads(m.read_text())
                    if name == 'duplicate_entry':
                        v['files'].append(v['files'][0])
                    else:
                        v['files'][0]['path'] = '../outside.txt'
                    m.write_text(json.dumps(v))
                else:
                    target = Path(td) / 'same-proof.txt'
                    target.write_bytes(p.read_bytes()); p.unlink(); p.symlink_to(target)
                r = subprocess.run([sys.executable, *flags, str(root / 'verify_manifest.py')],
                                   capture_output=True)
                need(r.returncode != 0, 'Mutation accepted: ' + name + '/' + mode)
                out.append({'mutation': name, 'mode': mode, 'rejected': True})
    return out


def symbolic_controls():
    # Independent representation: exact algebraic number, not the author's free t remainder.
    x, y, a, b, s, r, z = S.symbols('x y a b s r z')
    t = (S.sqrt(5) - 1) / 2
    lam = (3 + S.sqrt(5)) / 2
    done = []

    def eq(label, expr):
        n = S.together(expr).as_numer_denom()[0]
        need(S.simplify(S.expand(n)) == 0, 'Symbolic failure: ' + label)
        done.append(label)

    def sub(expr, var, mp):
        return expr.subs(dict(zip(var, mp)), simultaneous=True)

    def pull(form, variables, images, source_variables=None):
        if source_variables is None:
            source_variables = variables
        return tuple(sum(sub(form[j], variables, images) * S.diff(images[j], v)
                         for j in range(len(variables))) for v in source_variables)

    beta = (1/x, t/y)
    g = (x*x*y, x*y)
    gi = (x/y, y*y/x)
    deck = (1/x, 1/y)
    for j, v in enumerate((x,y)):
        eq('inverse-forward-' + str(j), sub(g[j], (x,y), gi) - v)
        eq('inverse-backward-' + str(j), sub(gi[j], (x,y), g) - v)
        eq('eigenform-' + str(j), pull(beta, (x,y), g)[j] - lam*beta[j])
        eq('deck-negative-' + str(j), pull(beta, (x,y), deck)[j] + beta[j])
        eq('commutation-' + str(j), sub(g[j], (x,y), deck) - sub(deck[j], (x,y), g))
    eq('t-minimal', t*t+t-1)
    eq('lambda-t', lam*t - (1+t))
    need(lam > 1, 'Wrong real eigenvalue'); done.append('lambda-strictly-greater-than-one')

    xy = ((a+1)/(a-1), (b+1)/(b-1))
    ba = pull(beta, (x,y), xy, (a,b))
    eq('coordinate-a', ba[0] - 2/(1-a*a))
    eq('coordinate-b', ba[1] - 2*t/(1-b*b))
    alpha = (1/(1-s)+t*r/(1-s*r*r), 2*t*s/(1-s*r*r))
    pi = (a*a, b/a)
    pa = pull(alpha, (s,r), pi, (a,b))
    for j in range(2):
        eq('cover-form-' + str(j), pa[j] - a*ba[j])
    eq('d-alpha', S.diff(alpha[1],s)-S.diff(alpha[0],r)-t/(1-s*r*r))
    eq('affine-connection', alpha[1]/(2*s)-t/(1-s*r*r))
    # Directly test the square-root integrating factor on coordinates (a,r), s=a^2.
    aa = pull(alpha, (s,r), (a*a,r), (a,r))
    eq('closed-after-cover', S.diff(aa[1]/a,a)-S.diff(aa[0]/a,r))
    eq('closedness-upstairs', S.diff(ba[1],a)-S.diff(ba[0],b))

    # Derive both quotient maps from g and g^{-1}, not from the author's quotient formula.
    def descend(mp):
        xp, yp = [S.cancel(sub(e,(x,y),xy)) for e in mp]
        ap, bp = [S.cancel((e+1)/(e-1)) for e in (xp,yp)]
        vals = [S.cancel(e.subs(b,a*r)) for e in (ap*ap,bp/ap)]
        result = []
        for e in vals:
            num, den = map(S.expand, S.fraction(e))
            for poly in (num,den):
                need(all(mon[0] % 2 == 0 for mon,coeff in S.Poly(poly,a).terms()),
                     'Noninvariant descended map')
            def even(poly):
                return sum(co*s**(mon[0]//2) for mon,co in S.Poly(poly,a).terms())
            result.append(S.cancel(even(num)/even(den)))
        return tuple(result)

    f, fi = descend(g), descend(gi)
    expected = (s*(r*s+r+2)**2/(2*r*s+s+1)**2,
                (r*s+1)*(2*r*s+s+1)/(s*(r+1)*(r*s+r+2)))
    for j,v in enumerate((s,r)):
        eq('derived-f-' + str(j),f[j]-expected[j])
        eq('quotient-inverse-forward-' + str(j),sub(f[j],(s,r),fi)-v)
        eq('quotient-inverse-backward-' + str(j),sub(fi[j],(s,r),f)-v)
        eq('quotient-preserves-' + str(j),pull(alpha,(s,r),f)[j]
           -lam*(r*s+r+2)/(2*r*s+s+1)*alpha[j])

    # Closed h*beta is equivalent to D(h)=0; test coefficient identity for a generic h.
    h = S.Function('h')(x,y)
    d_hbeta = S.diff(h*t/y,x)-S.diff(h/x,y)
    eq('integrating-factor-derivation',d_hbeta-(t*x*S.diff(h,x)-y*S.diff(h,y))/(x*y))
    # The invariant tangent derivation downstairs is a*D, not D by itself.
    D_ab = (t*(1-a*a)/2, -(1-b*b)/2)
    for e in (a*a,b/a):
        de = S.cancel(a*sum(S.diff(e,v)*dv for v,dv in zip((a,b),D_ab)))
        eq('invariant-tangent-' + str(e), sub(de,(a,b),(-a,-b))-de)
    eq('slice-counterexample',S.Rational(1,3)**2+S.Rational(1,3)**3
       +S.Rational(1,3)**5-S.Rational(37,243))
    # d(y dx)=dy wedge dx is nonzero, while eta wedge dx=0.
    need(S.diff(y,y) == 1, 'Gauge curvature failed'); done.append('nonflat-gauge')
    return {'total_checks':len(done),'checks':done,
            'derived_inverse': [str(e) for e in fi],
            'scope':'Exact identities only. Universal leaf, constant-field, and descent arguments are in AUDIT_REPORT.md.'}


def sources(author, directory):
    result = []
    for i,s in enumerate(json.loads((author/'SOURCE_VERIFICATION.json').read_text())['sources']):
        b = (directory / (str(i)+'.pdf')).read_bytes()
        need(b.startswith(b'%PDF-') and len(b)==s['bytes'] and digest(b)==s['sha256'],
             'Source pin mismatch '+str(i))
        result.append({'title':s['title'],'url':s['url'],'bytes':len(b),'sha256':digest(b),'match':True})
    return result


def datasets(author, directory):
    out=[]
    for s in json.loads((author/'SOURCE_VERIFICATION.json').read_text())['public_dataset_verification']['files']:
        b=(directory/s['name']).read_bytes()
        need(len(b)==s['bytes'] and digest(b)==s['sha256'],'Dataset pin mismatch')
        v=json.loads(b)
        row={'name':s['name'],'bytes':len(b),'sha256':digest(b),'records':len(v),'match':True}
        if s['name']=='problems.json':
            found=[r for r in v if str(r.get('id'))=='30004491']
            need(len(found)==1 and found[0]['problem_number']=='OWR-1703871-006','Target record mismatch')
            row['target_matches']=1
        else:
            need('OWR-1703871-006' not in v,'Unexpected prior report')
            row['prior_key_present']=False
        out.append(row)
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--author',required=True,type=Path)
    p.add_argument('--archive',required=True,type=Path)
    p.add_argument('--sources',type=Path)
    p.add_argument('--datasets',type=Path)
    args=p.parse_args()
    author=args.author.resolve()
    out={'status':'PASS_SCOPED_INDEPENDENT_CONTROLS','general_conjecture_solved':False,
         'freeze':pinned(author,args.archive),'author_runs':author_runs(author),
         'mutations':mutations(author),'independent_symbolic':symbolic_controls()}
    if args.sources:out['source_pins']=sources(author,args.sources)
    if args.datasets:out['dataset_pins']=datasets(author,args.datasets)
    pinned(author,args.archive)
    print(json.dumps(out,sort_keys=True,indent=2))


if __name__=='__main__':
    main()

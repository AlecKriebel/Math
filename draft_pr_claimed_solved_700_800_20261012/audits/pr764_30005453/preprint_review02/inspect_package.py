"""Independent closed-package controls; read-only inputs, receipt in review root."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, io, json, stat, zipfile

ROOT = Path(__file__).resolve().parent

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def decode(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, 'Duplicate JSON key: ' + k)
            out[k] = v
        return out
    return json.loads(raw, object_pairs_hook=pairs)

def ident(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def archive(raw):
    z = zipfile.ZipFile(io.BytesIO(raw))
    names = z.namelist()
    need(len(names) == len(set(names)), 'Repeated ZIP path')
    need(z.testzip() is None, 'CRC failure')
    values = {}
    for info in z.infolist():
        n = info.filename
        p = PurePosixPath(n)
        need(not p.is_absolute() and '\\' not in n and
             all(s not in ('', '.', '..') for s in n.split('/')) and str(p) == n,
             'Unsafe ZIP path')
        mode = info.external_attr >> 16
        need(not info.is_dir() and not (info.flag_bits & 1) and
             stat.S_IFMT(mode) in (0, stat.S_IFREG), 'Unsupported ZIP entry')
        values[n] = z.read(info)
    return values

def manifest(values, name='MANIFEST.json', prefix=''):
    m = decode(values[prefix + name])
    entries = m.get('files', m.get('authored_files'))
    if isinstance(entries, dict):
        entries = [{'path': k, **v} for k, v in entries.items()]
    need(isinstance(entries, list), 'Unrecognized manifest')
    listed = set()
    for e in entries:
        n = e['path']
        need(n not in listed and n != name, 'Repeated/self manifest path')
        listed.add(n)
        need(ident(values[prefix+n]) == {k: e[k] for k in ('bytes','sha256')}, 'Manifest identity')
    actual = {n[len(prefix):] for n in values if n.startswith(prefix)}
    need(actual == listed | {name}, 'Manifest not closed: ' + prefix)
    return len(entries)

def main():
    bound = decode((ROOT/'INPUT_BINDING.json').read_bytes())
    pins = []
    for e in bound['frozen_publication_files']:
        found = ident((ROOT/'frozen'/e['path']).read_bytes())
        need(found == {k:e[k] for k in found}, 'Frozen pin mismatch')
        pins.append({'path':e['path'], **found})
    source = archive((ROOT/'frozen/source-and-verification.zip').read_bytes())
    need(len(source)==155, 'Wrong source count')
    need(source['paper.tex']==(ROOT/'frozen/paper.tex').read_bytes(), 'TeX mismatch')
    json_count=0
    def scan(values):
        nonlocal json_count
        for n, b in values.items():
            if n.endswith('.json'):
                decode(b); json_count+=1
            elif n.endswith('.zip'):
                scan(archive(b))
    scan(source)
    need(manifest(source)==154, 'Wrong source manifest size')
    review_counts={}
    for family in ['review_deterministic_family','review_stochastic_family','priority_audit','priority_adversary01']:
        review_counts[family]=manifest(source, prefix='audit/'+family+'/')
    historical={n[len('historical_candidate/'):]:b for n,b in source.items() if n.startswith('historical_candidate/')}
    need(len(historical)==63, 'Historical count')
    need(manifest(historical,'PUBLICATION_MANIFEST.json')==62, 'Historical closure')
    nested={}
    for n,b in historical.items():
        if n.endswith('.zip'):
            vals=archive(b); nested[n]=len(vals); manifest(vals)
    need(len(nested)==4, 'Four frozen archives missing')
    outer=archive((ROOT/'frozen/zenodo-upload-kit.zip').read_bytes())
    need(set(outer)=={'paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json','README.md'}, 'Outer member scope')
    need(outer['paper.pdf']==(ROOT/'frozen/output/pdf/paper.pdf').read_bytes(), 'Outer PDF mismatch')
    need(outer['source-and-verification.zip']==(ROOT/'frozen/source-and-verification.zip').read_bytes(), 'Outer source mismatch')
    copies=[decode((ROOT/'frozen/zenodo-metadata.json').read_bytes())['metadata'], decode((ROOT/'frozen/zenodo-deposit.json').read_bytes())['metadata'], decode(source['zenodo-metadata.json'])['metadata'], decode(outer['zenodo-metadata.json'])['metadata'], decode(outer['zenodo-deposit.json'])['metadata']]
    need(all(x==copies[0] for x in copies), 'Metadata copies differ')
    descriptor=decode((ROOT/'frozen/zenodo-deposit.json').read_bytes())
    need(descriptor['files']==[{'path':'output/pdf/paper.pdf','name':'paper.pdf'},{'path':'source-and-verification.zip','name':'source-and-verification.zip'}], 'Standalone upload file list')
    need(decode(outer['zenodo-deposit.json'])['files']==[{'path':'paper.pdf'},{'path':'source-and-verification.zip'}], 'Flat upload file list')
    support=ROOT.parent/'preprint/support'
    actual={p.relative_to(support).as_posix():p.read_bytes() for p in support.rglob('*') if p.is_file()}
    need(actual==source and not any(p.is_symlink() for p in support.rglob('*')), 'Canonical equivalent support differs')
    out={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'result':'PASS','pins':pins,'source_members':len(source),'json_documents_duplicate_key_checked':json_count,'source_manifest_entries':154,'historical_files':63,'frozen_archives':nested,'review_manifest_entries':review_counts,'metadata_equal_copies':5,'outer_members':sorted(outer),'canonical_support_equivalent_to_frozen_source':True,'scope':'Independent byte, path, regularity, CRC, closure, metadata controls; no infinite-proof or priority certification.'}
    (ROOT/'PACKAGE_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()

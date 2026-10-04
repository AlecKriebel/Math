#!/usr/bin/env python3
"""Build a deterministic, source-complete public supplement; raw sources stay private."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,stat,zipfile
P=Path(__file__).resolve().parent;A=P.parent
PREFIX='basin-boundaries-verification'
BUILD=P/'private'/('package_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
ROOT=BUILD/PREFIX
def sha(b):return hashlib.sha256(b).hexdigest()
def copy(source,dest):
    assert source.is_file() and not source.is_symlink()
    target=ROOT/dest;target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(source.read_bytes());target.chmod(0o644)
def main():
    assert (A/'priority_review/CLOSURE.json').is_file(),'Wait for final priority closure.'
    ROOT.mkdir(parents=True)
    copy(P/'SUPPLEMENT_README.md','README.md')
    copy(P/'verify_supplement.py','verify_supplement.py')
    copy(P/'common_basin_boundaries.tex','paper/common_basin_boundaries.tex')
    copy(P/'zenodo-deposit.json','paper/zenodo-deposit.json')
    candidate=A/'snapshot/problems/30001370_basin_boundaries'
    original=list(sorted(p for p in candidate.rglob('*') if p.is_file()))
    assert len(original)==37
    for p in original:copy(p,Path('candidate')/p.relative_to(candidate))
    families=[('algebra_certificate_review','algebra',['check_uniform_algebra.py','UNIFORM_CERTIFICATE.json','check_symbolic_equations.py','SYMBOLIC_IDENTITIES.json']),
              ('backward_feedback_review','backward',['check_backward_feedback.py','verify_controls.py','INDEPENDENT_CHECKS.json']),
              ('topology_density_review','topology',['check_topology.py','topology_checks.json'])]
    for family,label,names in families:
        for name in names:copy(A/family/'public'/name,Path('controls')/label/name)
    for family,report,baseline in [('algebra_certificate_review','REPORT.md','SOURCE_FIRST_BASELINE.md'),
                                   ('backward_feedback_review','REPORT.md','SOURCE_FIRST.md'),
                                   ('topology_density_review','TOPOLOGY_DENSITY_AUDIT.md','independent_reconstruction.md')]:
        for name in [report,baseline]:copy(A/family/'public'/name,Path('audits')/family/name)
    copy(A/'ROOT_MATHEMATICAL_AUDIT.md','audits/ROOT_MATHEMATICAL_AUDIT.md')
    # All priority public files, with both manifest identities and final seal.
    # Its public-only verifier reports private bytes as unchecked.
    for p in sorted((A/'priority_review').iterdir()):
        if p.is_file():copy(p,Path('audits/priority')/p.name)
    (ROOT/'LICENSE.md').write_text('Copyright 2026 Alec Kriebel. Paper and accompanying original verification material are licensed under Creative Commons Attribution 4.0 International (CC-BY-4.0): https://creativecommons.org/licenses/by/4.0/. Cited third-party papers are not redistributed.\n')
    files=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file():
            b=p.read_bytes();files.append({'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':sha(b)})
    (ROOT/'FILE_MANIFEST.json').write_text(json.dumps({'scope':'All regular payload files; this manifest alone is self-excluded, with external reviewed ZIP checksum binding it.','files':files},indent=2)+'\n')
    zpath=P/(PREFIX+'.zip')
    with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(ROOT.rglob('*')):
            if p.is_file():
                info=zipfile.ZipInfo(PREFIX+'/'+str(p.relative_to(ROOT)),date_time=(2026,10,3,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16
                z.writestr(info,p.read_bytes())
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'build_directory':str(ROOT),
             'zip_path':str(zpath),'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),
             'member_count':len(files)+1,'source_tex_sha256':sha((P/'common_basin_boundaries.tex').read_bytes()),
             'metadata_sha256':sha((P/'zenodo-deposit.json').read_bytes()),'original_candidate_files':37}
    (P/'SUPPLEMENT_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()

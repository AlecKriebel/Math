#!/usr/bin/env python3
"""Build deterministic source and reproducibility ZIP archives."""
from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZipInfo

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'submission'
STAMP=(2026,8,6,12,0,0)
AUX={'.aux','.bcf','.blg','.fdb_latexmk','.fls','.log','.out','.pyc'}
TRANSIENT_BINARIES={'regenerate_directed_pair_universe','regenerate_signature_relation','review_directed_pair_universe','review_multitriangle_exclusion'}


def wanted(path: Path) -> bool:
    return (path.is_file() and '__pycache__' not in path.parts and path.suffix not in AUX
            and not path.name.endswith('.run.xml') and path.name not in TRANSIENT_BINARIES)


def write_zip(path: Path, files: list[tuple[Path,str]]) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(path,'w',compression=ZIP_DEFLATED,compresslevel=1) as z:
        for source,arc in sorted(files,key=lambda x:x[1]):
            info=ZipInfo(arc,STAMP)
            info.compress_type=ZIP_DEFLATED
            info.external_attr=(0o100644 & 0xFFFF)<<16
            z.writestr(info,source.read_bytes())


def source_archive() -> None:
    files=[]
    for p in (ROOT/'source'/'paper').rglob('*'):
        if wanted(p) and (p.suffix in {'.tex','.bib'}):
            files.append((p,str(Path('paper')/p.relative_to(ROOT/'source'/'paper'))))
    for name in ('COVER_LETTER.tex','COVER_LETTER_JMB.tex','COVER_LETTER_BMB.tex','REFEREE_GUIDE.tex'):
        p=ROOT/'docs'/name; files.append((p,str(Path('editorial')/name)))
    for name in ('LICENSE-CODE.txt','LICENSE-MANUSCRIPT.txt','CITATION.cff'):
        files.append((ROOT/name,name))
    write_zip(OUT/'LaTeX_TikZ_Source.zip',files)


def reproducibility_archive() -> None:
    files=[]
    for base,prefix in [
        (ROOT/'reproducibility','reproducibility'),
        (ROOT/'transcripts','transcripts'),
        (ROOT/'review','review'),
    ]:
        for p in base.rglob('*'):
            if wanted(p): files.append((p,str(Path(prefix)/p.relative_to(base))))
    for name in ('PRIOR_WORK_AND_NOVELTY_AUDIT.md','THEOREM_CERTIFICATE_CROSSWALK.md','DIRECTIVE_CHANGE_LOG.md','HUMAN_SUBMISSION_CHECKLIST.md'):
        files.append((ROOT/'docs'/name,str(Path('docs')/name)))
    for name in ('README.md','LICENSE-CODE.txt','LICENSE-MANUSCRIPT.txt','CITATION.cff','RELEASE_METADATA.json'):
        files.append((ROOT/name,name))
    write_zip(OUT/'STC_JC_Reproducibility.zip',files)


def main():
    source_archive();reproducibility_archive()
    print('DETERMINISTIC COMPONENT ARCHIVES BUILT')

if __name__=='__main__':main()

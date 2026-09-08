#!/usr/bin/env python3
"""Independent final-log and real packaging negative controls, scratch only."""
import datetime,hashlib,json,pathlib,shutil,subprocess,sys
from audit_driver import HERE,SOURCE,SCRATCH,LOGS,ENV,run

GATE=SOURCE/'release/audit_tex_logs.py'
OLD=SOURCE.parents[1]/'independent_preprint_rereview_v1.0.10_2026-09-06/release'

def fresh(name):
    dst=SCRATCH/name
    if dst.exists():shutil.rmtree(dst)
    shutil.copytree(SOURCE,dst)
    return dst

def bundle_hashes(root):
    return {line.split(None,1)[1]:hashlib.sha256((root/line.split(None,1)[1]).read_bytes()).hexdigest() for line in (SOURCE/'release/BUNDLE_SHA256.txt').read_text().splitlines()}

kind=sys.argv[1];results=[]
if kind=='parser':
    root=SCRATCH/'log_parser';root.mkdir(exist_ok=True)
    cases={'clean':'This is pdfTeX.\nOutput written on accepted.pdf (1 page).\n','hbox':r'Overfull \hbox (33.31522pt too wide) at lines 1--2','vbox':r'Overfull \vbox (12pt too high) at lines 1--2','undefined_reference':"LaTeX Warning: Reference `missing' on page 1 undefined on input line 9.",'undefined_citation':"LaTeX Warning: Citation `missing' on page 1 undefined on input line 9.",'aggregate_references':'LaTeX Warning: There were undefined references.','aggregate_citations':'There were undefined citations.','empty':''}
    for name,content in cases.items():
        p=root/(name+'.log');p.write_text(content)
        expected=0 if name=='clean' else 1
        status=run('log_parser_'+name,['python',str(GATE),str(p)],root,expected=expected)
        assert status==expected
        results.append(dict(name=name,status=status))
    absent=root/'absent.log';absent.unlink(missing_ok=True)
    status=run('log_parser_missing',['python',str(GATE),str(absent)],root,expected=1);assert status==1
    results.append(dict(name='missing',status=status))
    # The previous round's actual final logs contain the five shipped warnings.
    preserved=HERE/'prior_warning_logs';preserved.mkdir(exist_ok=True)
    prior_paths=[]
    for name in ['clean_journal_main.log','clean_journal_supplement.log']:
        shutil.copy2(OLD/'logs'/name,preserved/name);prior_paths.append(str(preserved/name))
    status=run('five_prior_journal_warnings_rejected',['python',str(GATE),*prior_paths],root,expected=1)
    assert status==1
    results.append(dict(name='five_actual_prior_warnings',status=status))
    assert run('official_journal_cli_control',['python',str(GATE),'--journal-negative-control'],root)==0
elif kind in ['old_journal_hbox','journal_vbox','cover_hbox','canonical_hbox']:
    d=fresh('negative_'+kind)
    hashes_before=bundle_hashes(d)
    if kind=='cover_hbox':
        source=d/'submission/journal/cover_letter_SIADS.tex'
        target=d/'submission/journal/cover_letter_SIADS.pdf'
        original=source.read_text();source.write_text(original.replace(r'\begin{document}',r'\begin{document}'+'\n'+r'\noindent\smash{\hbox to 0pt{\hskip 600pt REFEREE OVERFLOW}}\par',1))
    else:
        source=d/'manuscript/main.tex';original=source.read_text()
        injection={
            'old_journal_hbox':r'\ifsiadsreview\smash{\hbox to 0pt{\hskip 430pt REFEREE OVERFLOW}}\fi',
            'journal_vbox':r'\ifsiadsreview\setbox0=\vbox to 0pt{\hbox{REFEREE VBOX}}\fi',
            'canonical_hbox':r'\smash{\hbox to 0pt{\hskip 600pt REFEREE OVERFLOW}}',
        }[kind]
        needle=r'\noindent\textbf{Keywords:}';assert needle in original
        source.write_text(original.replace(needle,needle+injection,1))
        target=d/'submission/journal/manuscript.pdf'
    pdf_before=target.read_bytes()
    status=run('real_refresh_'+kind,['bash','release/refresh_packages.sh'],d,expected=1)
    log=(LOGS/('real_refresh_'+kind+'.log')).read_text()
    assert status==1 and 'final TeX log audit failed:' in log and 'overfull box' in log
    assert bundle_hashes(d)==hashes_before
    assert target.read_bytes()==pdf_before
    results.append(dict(name=kind,status=status,seven_bundles_unchanged=True,previous_accepted_pdf_unchanged=True,error=log.strip()))
else:raise SystemExit('unknown control')
(HERE/(kind+'_RESULT.json')).write_text(json.dumps(results,indent=2)+'\n')
print(kind+'_INDEPENDENT_CONTROLS_PASS')

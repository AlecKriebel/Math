#!/usr/bin/env python3
"""PR280 verify public DOI/bytes, fresh full dedup, intent, one append, unique readback."""
import argparse
import json
import re
import subprocess
import uuid
from ops_binding import *
from publication_live_gates import collect
from verify_published_files import verify_live


def desired_row(identifier):
    return [
        '30000156 / OWR-768-006: Limiting Cycle Distributions of Birational Maps',
        '', 'https://doi.org/10.5281/zenodo.'+str(identifier),
        TITLE+' — Alec Kriebel (ORCID 0009-0001-9320-500X), v1.0 (2026-10-21). '
        'Unrefereed preprint. Fixed L(u,v)=(u,(u²+1)v) permutes the full affine plane for p≡3 mod4; '
        'point-weighted periods normalized by p have, at each fixed 1/2≤x<1, CDF '
        '1−φ(p−1)/(p−1)+o(1), limsup 1 and liminf at most 23/24. Neither those CDF values '
        'nor the period measures converge on any admissible prime subset of positive upper relative density. '
        'The triangular family, primitive quadratic values, shifted-prime totient mean and continuous scalar '
        'law are established and credited; this is a scoped application to Vivaldi’s 2004 broad existence assertion '
        '(joint work with Roberts). No new map family, character-sum theorem, arithmetic mean/scalar law, '
        'universal elliptic, polynomial-automorphism or prime-average cycle theorem claimed. '
        'Bounded priority audit found no authenticated exact earlier application in inspected sources; '
        'the cited Neumärker–Roberts–Viallet–Vivaldi 2011 preprint body/version relationships remain unrecovered. '
        'No worldwide novelty, current-open status or historical firstness claim. '
        'PDF and editable-source/verification ZIP preserve all 17 original files and historical audits; '
        'new dependency-free checker supports finite computations, while the proof uses cited classical inputs. '
        'Extensive AI use in research, model/proof development, computation, literature investigation, writing '
        'and adversarial verification. No formal independent human peer review; internal AI audits are not human peer review. '
        'Primary source: https://webspace.maths.qmul.ac.uk/f.vivaldi/research/Oberwolfach.pdf. '
        'Record: https://zenodo.org/records/'+str(identifier)+'. '
        'PR: https://github.com/AlecKriebel/Math/pull/280.'
    ]


def gws(action,params,body=None):
    command=['gws','sheets','spreadsheets','values',action,'--params',json.dumps(params)]
    if body is not None:
        command+=['--json',json.dumps(body,ensure_ascii=False)]
    run=subprocess.run(command,capture_output=True,text=True)
    if run.returncode:
        raise RuntimeError('GWS failed; inspect saved intent/live sheet before retry: '+run.stderr[:700])
    return json.loads(run.stdout)


def read(label,operation):
    value=gws('get',{'spreadsheetId':SHEET,'range':"'Math Puzzles'!A:AQ",'valueRenderOption':'FORMATTED_VALUE'})
    atomic_json(PRIVATE/(label+'_'+operation+'.json'),value)
    return schema_rows(value)


def matches(rows,identifier):
    doi='10.5281/zenodo.'+str(identifier)
    return [(i,r) for i,r in enumerate(rows[1:],2) if PATTERN.search(' '.join(r))
            or any(doi in set(re.findall(r'10\.5281/zenodo\.\d+',v)) for v in r)]


def append_verified(expected_head,identifier):
    require_release_clearance()
    # Never trust old saved booleans: make a new read-only actual public download
    # and DOI200 inspection before the last full-account/full-sheet gate.
    public=verify_live(identifier)
    if (public.get('record')!=identifier or public.get('all_public_file_bytes_match_reviewed') is not True
            or public.get('doi_resolution',{}).get('status')!=200
            or public.get('release_manifest_sha256')!=RELEASE_SHA):
        raise RuntimeError('Fresh public DOI/files verification incomplete')
    gate,acceptance=collect('before_ledger',expected_head,identifier,allow_target_row=True)
    operation=uuid.uuid4().hex
    row=desired_row(identifier)
    before=read('ledger_before_append',operation)
    if digest(before)!=gate['ledger_sha256']:
        raise RuntimeError('Full sheet changed since fresh gate; recollect/reconcile before append')
    doi='10.5281/zenodo.'+str(identifier)
    doi_rows=[r for r in before[1:] if doi in set(re.findall(r'10\.5281/zenodo\.\d+',' '.join(r)))]
    if len(doi_rows)>1 or (doi_rows and doi_rows[0]!=row):
        raise RuntimeError('Existing DOI appears in a different or duplicate full-sheet row; no append')
    found=matches(before,identifier)
    # Broad prior distinct-model rows are allowed only through the exact root
    # reconciliation; target identity/DOI rows must still be unique and exact.
    recon=json.loads((AUDIT/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_text())
    known={v['values_sha256'] for v in recon['ledger_leads']}
    if any(digest(r) in known for r in doi_rows):
        raise RuntimeError('Current target DOI/row contradicts a root non-target ledger exemption; no append')
    found=[(i,r) for i,r in found if digest(r) not in known]
    intent=AUDIT/'LEDGER_APPEND_INTENT.json'
    appended=False
    if found:
        if len(found)!=1 or found[0][1]!=row:
            raise RuntimeError('Existing target/DOI row differs or is duplicated; no append')
        row_number=found[0][0]
    else:
        if intent.exists():
            raise RuntimeError('Prior append intent has no exact visible row; reconcile without blind retry')
        require_release_clearance()
        fresh(gate['started_utc'])
        atomic_json(intent,{'timestamp':stamp(),'pr':280,'spreadsheet_id':SHEET,'range':"'Math Puzzles'!A:D",
            'row':row,'before_rows':len(before),'before_sha256':digest(before),'operation':operation,
            'gate_receipt':gate['receipt'],'public_verification_sha256':sha((AUDIT/'ZENODO_PUBLIC_FILE_VERIFICATION.json').read_bytes()),
            'uncertain_outcome_rule':'Read current full sheet for exact DOI/result before any retry; never blindly append twice.'})
        response=gws('append',{'spreadsheetId':SHEET,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW',
                      'insertDataOption':'INSERT_ROWS','includeValuesInResponse':True},
                     {'majorDimension':'ROWS','values':[row]})
        atomic_json(AUDIT/'LEDGER_APPEND_RESPONSE.json',response)
        updates=response['updates']
        if (updates['updatedRows']!=1 or updates['updatedColumns']!=4 or updates['updatedData']['values']!=[row]):
            raise RuntimeError('Unexpected append outcome; inspect live sheet, no retry')
        appended,row_number=True,None
    after=read('ledger_after_append',operation)
    # Target DOI rows are never filtered by any non-target digest, including
    # readback after a provider boundary. Exact target identity has precedence.
    found=[(i,r) for i,r in matches(after,identifier) if digest(r) not in known
           or doi in set(re.findall(r'10\.5281/zenodo\.\d+',' '.join(r)))]
    if len(found)!=1 or found[0][1]!=row or (row_number is not None and row_number!=found[0][0]):
        raise RuntimeError('Target row readback/uniqueness mismatch; no retry')
    doi='10.5281/zenodo.'+str(identifier)
    if sum(doi in set(re.findall(r'10\.5281/zenodo\.\d+',' '.join(r))) for r in after)!=1:
        raise RuntimeError('DOI is duplicated anywhere in full sheet')
    if appended and (len(after)!=len(before)+1 or after[:-1]!=before or after[-1]!=row):
        raise RuntimeError('Append readback changed other sheet rows; reconcile without retry')
    receipt={'timestamp':stamp(),'pr':280,'status':'verified','row_number':found[0][0],
        'spreadsheet_id':SHEET,'sheet_gid':1254632077,'doi':doi,'values':row,'new_row':appended,
        'unique_target_and_DOI':True,'read_back_exact':True,'ledger_rows_before':len(before),
        'ledger_rows_after':len(after),'gate_receipt':gate['receipt'],'operation':operation}
    atomic_json(AUDIT/'LEDGER_PUBLICATION_VERIFICATION.json',receipt)
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-pr-head',required=True)
    parser.add_argument('--deposit-id',type=int,required=True)
    args=parser.parse_args()
    print(json.dumps(append_verified(args.expected_pr_head,args.deposit_id),indent=2))


if __name__=='__main__':
    main()

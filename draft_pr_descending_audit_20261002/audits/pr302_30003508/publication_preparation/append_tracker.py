"""One authorized confirmed-DOI row with full prior-table preservation."""
from publication_guard import *
from run_zenodo_step import identity,inspected_publication
from verify_public_record import verify_public_evidence
CLI='/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws'
ID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';GID=1254632077
def main():
    lock=acquire();published=inspected_publication();public=verify_public_evidence(published)
    require(published['state']=='published' and public['status']=='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_BOTH_FULL_FILE_BYTES' and public['record_id']==published['id'] and public['DOI']==published['doi'],'Actual confirmed public record required')
    require(not (OUT/'TRACKER_COMPLETE.json').exists() and not (OUT/'private_processes/tracker_append').exists(),'Prior or uncertain append requires read-only reconciliation')
    require(pin(CLI)['sha256']=='0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e','Reviewed Workspace CLI changed')
    sheet,actual=execute('sheet_metadata',[CLI,'sheets','spreadsheets','get','--params',json.dumps(dict(spreadsheetId=ID,fields='spreadsheetId,sheets(properties(sheetId,title,gridProperties(rowCount,columnCount)))'))])
    require(sheet['spreadsheetId']==ID,'Sheet identity differs')
    matches=[x['properties'] for x in sheet['sheets'] if x['properties']['sheetId']==GID]
    require(len(matches)==1 and matches[0]['title']=='Math Puzzles','Exact selected tab differs')
    properties=matches[0];columns=properties['gridProperties']['columnCount'];require(columns>=4,'Tracker columns incomplete')
    last='';v=columns
    while v:v,remainder=divmod(v-1,26);last=chr(65+remainder)+last
    whole="'Math Puzzles'!A1:"+last+str(properties['gridProperties']['rowCount'])
    def values(method,params,label,body=None,dry=False):
        argv=[CLI,'sheets','spreadsheets','values',method,'--params',json.dumps(params)]
        if body is not None:argv+=['--json',json.dumps(body)]
        if dry:argv+=['--dry-run']
        return execute(label,argv)
    before,actual=values('get',dict(spreadsheetId=ID,range=whole,valueRenderOption='FORMULA'),'all_rows_before')
    rows=before.get('values',[]);require(rows and rows[0][:4]==['Original Problem','Solution Chat URL','DOI','Notes'],'Exact tracker headers differ')
    metadata=load(F/'record_metadata.json');title=metadata['title']
    require(not any('30003508' in str(row) or published['doi'] in str(row) or title.lower() in str(row).lower() for row in rows[1:]),'Existing paper/DOI row requires reconciliation')
    notes=(title+' — Alec Kriebel; ORCID0009-0001-9320-500X; version'+metadata['version']+'; preprint '+metadata['publication_date']+'. '
           'Almost-sure consistency of the specified empirical spectral-equation estimator for a smooth symmetric anisotropic tensor and unknown stationary density on a known smooth bounded connected domain in dimension at least two, from one exact stationary trajectory at a known fixed positive lag. Conormal reflection and known pointwise ellipticity/density bounds. Local uniform tensor/separately fitted divergence recovery and global clipped tensor L2 recovery; repeated, negative and near-zero empirical modes handled. '
           'Earlier nonparametric spectral fitting and eigenvalue-power weighting, reversible identification, scalar inference, spectral excitation and elliptic regularity are credited. Bounded priority audit with explicit source-edition gaps, including uninspected CV2011 publisher-final body; no worldwide firstness, rate or general numerical implementation claim. '
           'Eight-page unrefereed research note; extensive AI assistance and two sequential fresh whole-package adversarial reviews; no human peer review or proof-assistant certificate. PDF and portable twenty-member archive with standalone source, supplementary classical derivations, eight unchanged finite-control suites, expected outputs and provenance. Finite controls supplement the analytic proof. Original submitted author history2/5 preserved. '
           'Original problem OWR-15432-001: https://doi.org/10.4171/OWR/2017/24 pp1507–1509. Record: '+published['record_url']+'. Reviewed PR: https://github.com/AlecKriebel/Math/pull/302.')
    row=['OWR-15432-001 (30003508): Convergence of Spectral Estimators for Diffusion Tensors','',published['doi_url'],notes]
    params=dict(spreadsheetId=ID,range="'Math Puzzles'!A:"+last,valueInputOption='RAW',insertDataOption='INSERT_ROWS',includeValuesInResponse=True)
    body=dict(majorDimension='ROWS',values=[row]);write(OUT/'TRACKER_ROW_REQUEST.json',dict(UTC=utc(),gid=GID,params=params,body=body,explicit_user_authorization=True,duplicate_found=False))
    values('append',params,'tracker_dry_run',body,dry=True);clearance()
    require(inspected_publication()==published and verify_public_evidence(published)==public,'Whole published metadata/native/file evidence changed immediately before append')
    response,actual=values('append',params,'tracker_append',body)
    require(response['spreadsheetId']==ID,'Append identity differs')
    updates=response['updates'];require((updates['updatedRows'],updates['updatedColumns'],updates['updatedCells'])==(1,4,4),'Actual append shape differs')
    target=updates['updatedRange'];require(target.startswith("'Math Puzzles'!") or target.startswith('Math Puzzles!'),'Actual target tab differs')
    fetched,_=values('get',dict(spreadsheetId=ID,range=target,valueRenderOption='FORMULA'),'appended_row_readback');require(fetched['values']==[row],'Actual appended row differs')
    after,_=values('get',dict(spreadsheetId=ID,range="'Math Puzzles'!A1:"+last,valueRenderOption='FORMULA'),'all_rows_after')
    require(after['values']==rows+[row] and sum('30003508' in str(x) for x in after['values'][1:])==1 and sum(published['doi'] in str(x) for x in after['values'][1:])==1,'Full original table changed or target duplicated')
    result=dict(UTC=utc(),status='PASS_EXACT_ONE_DOI_ROW_AND_WHOLE_TABLE_READBACK',spreadsheetId=ID,gid=GID,updatedRange=target,DOI=published['doi'],record_url=published['record_url'],row=row,all_original_columns_scanned=columns,all_prior_rows_unchanged=True,single_actual_append_PID=actual['actual_PID'],automatic_retry=False,solution_chat_cell_blank=True,no_individual_contacted=True)
    write(OUT/'TRACKER_COMPLETE.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='row'},indent=2))
if __name__=='__main__':main()

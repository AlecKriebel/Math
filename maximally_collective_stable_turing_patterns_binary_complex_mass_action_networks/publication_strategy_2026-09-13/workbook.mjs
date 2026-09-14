import fs from 'node:fs/promises';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load('/Users/alec/Downloads/Papers (4).xlsx'));
const out = new URL('./outputs/turing-review/', import.meta.url).pathname;
const sheet = wb.worksheets.getItem('Papers');
if (!process.argv.includes('--edit')) {
  const preview = await wb.render({sheetName:'Papers',range:'C7:N9',scale:1,format:'png'});
  await fs.writeFile(out+'before.png', new Uint8Array(await preview.arrayBuffer()));
} else {
  sheet.getRange('C8').values = [['Exact Diffusion Design for Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks']];
  sheet.getRange('M8').values = [[7.8]];
  sheet.getRange('E8').values = [['Clarify fixed-interval, fixed-mass and long-wave scope in abstract. Seek focused specialist feedback. Target submission Sep 28–Oct 5, 2026 after resolving concrete objections. Do not wait for Lean or endorsements.']];
  sheet.getRange('F8').values = [['Added to Zenodo on 9/12\n9/13 assessment: v1.0.11 deposit files verified.\nRecommended next: author to share with Edgardo Villar-Sepúlveda and Maya Mincheva; Andrew Krause for nonlinear stability feedback. No specialist circulation recorded in this sheet.\nAllow 2–3 weeks for feedback, then submit if no substantive issue emerges.']];
  sheet.getRange('P8').values = [['Zenodo']];
  sheet.getRange('W8').values = [['Conditional impact 7.8/10 (judgment range 7.5–8.1): strong specialist theorem combining topology-wide localization, exact diffusion design and stable branches. Synthetic, local and topology-specific; constants remain open. Previous ChatGPT score: 8.4. Lean: defer full formalization; optional finite algebra/certificate pilot. Independent checks found no blocker, but do not constitute journal peer review.']];
  sheet.getRange('X1').copyFrom(sheet.getRange('W1'),'all');
  sheet.getRange('X1').values = [['Sources']];
  sheet.getRange('X8').values = [[[
    'https://doi.org/10.5281/zenodo.22729355',
    'https://arxiv.org/abs/2605.16049',
    'https://doi.org/10.1007/s00285-023-01870-3',
    'https://doi.org/10.1007/s11538-023-01250-4',
    'https://epubs.siam.org/journal/siads/editorial-policy',
    'https://epubs.siam.org/pb-assets/files/Consent_to_Publish_Journals.pdf'
  ].join('\n')]];
  for (const cell of ['C8','E8','F8','P8','W8','X8']) {
    sheet.getRange(cell).format.wrapText = true;
    sheet.getRange(cell).format.verticalAlignment = 'top';
  }
  sheet.getRange('W8').format.columnWidth = 55;
  sheet.getRange('X8').format.columnWidth = 78;
  sheet.getRange('C8:X8').format.rowHeight = 210;
  console.log((await wb.inspect({kind:'table',range:'Papers!L8:N8',include:'values,formulas',tableMaxRows:1,tableMaxCols:3})).ndjson);
  console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:15},summary:'formula error scan'})).ndjson);
  for (const [name,range] of [['actions','C8:F8'],['scores','L8:N8'],['notes','W8:X8']]) {
    const png=await wb.render({sheetName:'Papers',range,scale:1,format:'png'});
    await fs.writeFile(out+name+'.png',new Uint8Array(await png.arrayBuffer()));
  }
  await (await SpreadsheetFile.exportXlsx(wb)).save(out+'Papers - Turing next steps.xlsx');
}

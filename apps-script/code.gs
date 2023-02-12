var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
var ui = SpreadsheetApp.getUi();

var SHEET_ID = spreadsheet.getId();
var CLOUD_RUN_URL = '<YOUR_CLOUD_RUN_URL>';

function apiRequest(path, body) {
  var options = {
    method: 'post',
    payload: JSON.stringify({
      sheetId: SHEET_ID,
      ...body,
    }),
    contentType: 'application/json',
  };
  UrlFetchApp.fetch(CLOUD_RUN_URL + path, options);
}

function exampleButton() {
  var sheetName = 'Sheet1';
  apiRequest('/example-sheets-write', {
    sheetName: sheetName,
  });
}

function onOpen(e) {
  SpreadsheetApp.getUi()
    .createMenu('Custom Menu')
    .addItem('Example Button', 'exampleButton')
    .addToUi();
}

/**
 * ONE IPTV — Google Sheet order logger
 * ---------------------------------------------------------------------------
 * Appends every website order to your "One IPTV — Commandes" sheet.
 *
 * HOW TO DEPLOY (5 minutes, one time):
 *   1. Open your sheet:
 *        https://docs.google.com/spreadsheets/d/17Ie9P0Hdw-_7-ea_Rj-j86uQfHe_WF9Zj_anu_fva3Y/edit
 *   2. Extensions → Apps Script.
 *   3. Delete whatever is there, paste THIS whole file, and Save.
 *   4. Click Deploy → New deployment.
 *        - Type: Web app
 *        - Execute as: Me
 *        - Who has access: Anyone
 *      Deploy, authorise when asked, and COPY the "Web app URL".
 *   5. Paste that URL into assets/js/config.js →
 *        checkout: { logEndpoint: "PASTE_URL_HERE" }
 *      Re-upload config.js. Done — every order now lands in the sheet.
 *
 * The sheet columns it fills (row 1 headers, already in your sheet):
 *   Date | Nom | Email | Téléphone | Formule | Prix (€) | Connexions | Paiement | Statut
 * ---------------------------------------------------------------------------
 */

var SHEET_ID  = "17Ie9P0Hdw-_7-ea_Rj-j86uQfHe_WF9Zj_anu_fva3Y";
var SHEET_TAB = "";   // leave "" to use the first tab, or put the tab name

function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    }

    var ss = SpreadsheetApp.openById(SHEET_ID);
    var sheet = SHEET_TAB ? ss.getSheetByName(SHEET_TAB) : ss.getSheets()[0];

    var now = Utilities.formatDate(new Date(), ss.getSpreadsheetTimeZone(), "yyyy-MM-dd HH:mm");

    // Column order matches the sheet headers.
    sheet.appendRow([
      now,                          // Date
      data.name        || "",       // Nom
      data.email       || "",       // Email (blank — site is WhatsApp-only)
      data.phone       || "",       // Téléphone (WhatsApp number)
      data.plan        || "",       // Formule
      data.price       || "",       // Prix (€)
      data.connections || "",       // Connexions
      data.payment     || "En attente",  // Paiement
      data.status      || "Nouveau"      // Statut
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Lets you open the web-app URL in a browser to confirm it is live.
function doGet() {
  return ContentService.createTextOutput("ONE IPTV order logger is running.");
}

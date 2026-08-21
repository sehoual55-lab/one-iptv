/**
 * ONE IPTV — Google Sheet order logger + email notifier
 * ---------------------------------------------------------------------------
 * On every website order it:
 *   1. appends a row to your orders sheet, and
 *   2. emails you the order as a clean HTML table.
 *
 * TO UPDATE (you already deployed once — keep the SAME URL):
 *   1. Open the sheet → Extensions → Apps Script.
 *   2. Replace everything with THIS file, and Save (disk icon).
 *   3. Deploy → Manage deployments → (pencil) Edit → Version: "New version"
 *      → Deploy.  This keeps the SAME web-app URL, so you do NOT need to
 *      change anything in config.js.
 *
 * The site now posts form-encoded data (application/x-www-form-urlencoded),
 * which survives Google's internal redirect — that is why earlier rows were
 * near-empty. This script reads e.parameter first, with a JSON fallback.
 *
 * Sheet columns (row 1 headers are written automatically if the sheet is empty):
 *   Date | Website | Name | Email | Phone | Country | Plan | Connections |
 *   Total | Payment method | Payment link | Status
 * ---------------------------------------------------------------------------
 */

var SHEET_ID     = "17Ie9P0Hdw-_7-ea_Rj-j86uQfHe_WF9Zj_anu_fva3Y";
var SHEET_TAB    = "";                    // "" = first tab, or put the tab name
var NOTIFY_EMAIL = "xyz905391@gmail.com"; // where new orders are emailed

var HEADERS = [
  "Date", "Website", "Name", "Email", "Phone", "Country",
  "Plan", "Connections", "Total", "Payment method", "Payment link", "Status"
];

function doPost(e) {
  try {
    // 1) Read the incoming order — form fields first, JSON body as a fallback.
    var data = {};
    if (e && e.parameter && Object.keys(e.parameter).length) {
      data = e.parameter;
    } else if (e && e.postData && e.postData.contents) {
      try { data = JSON.parse(e.postData.contents); } catch (ignore) { data = {}; }
    }

    var ss    = SpreadsheetApp.openById(SHEET_ID);
    var sheet = SHEET_TAB ? ss.getSheetByName(SHEET_TAB) : ss.getSheets()[0];
    var now   = Utilities.formatDate(new Date(), ss.getSpreadsheetTimeZone(), "yyyy-MM-dd HH:mm");

    // Write headers once if the sheet is empty.
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
    }

    var website     = data.website     || "one-iptv.website";
    var name        = data.name        || "";
    var email       = data.email       || "";
    var phone       = data.phone       || "";
    var country     = data.country     || "";
    var plan        = data.plan        || "";
    var connections = data.connections || "";
    var total       = data.price       || data.total || "";
    var payment     = data.payment     || "";
    var payLink     = data.paymentLink || "";
    var status      = data.status      || "Nouveau";

    sheet.appendRow([
      now, website, name, email, phone, country,
      plan, connections, total, payment, payLink, status
    ]);

    // 2) Email you the order as an HTML table.
    try {
      var subject = "New order [" + website + "] : " + plan +
                    (total ? " — " + total : "") +
                    (name ? " (" + name + ")" : "");

      var rows = [
        ["Website", website],
        ["Name", name],
        ["Email", email],
        ["Phone", phone],
        ["Country", country],
        ["Plan", plan],
        ["Connections", connections],
        ["Total", total],
        ["Payment method", payment],
        ["Payment link", payLink],
        ["Received", now]
      ];

      var trs = rows.map(function (r) {
        var val = esc(r[1]);
        if (r[0] === "Email" && r[1]) {
          val = '<a href="mailto:' + esc(r[1]) + '" style="color:#e50914;text-decoration:none;">' + esc(r[1]) + '</a>';
        } else if (r[0] === "Payment link" && r[1]) {
          val = '<a href="' + esc(r[1]) + '" style="color:#e50914;text-decoration:none;">' + esc(r[1]) + '</a>';
        } else if (!r[1]) {
          val = '<span style="color:#9aa0a6;">—</span>';
        }
        return '<tr>' +
                 '<td style="padding:10px 14px;border:1px solid #e6e6e6;background:#fafafa;' +
                   'font-weight:600;color:#111;white-space:nowrap;">' + esc(r[0]) + '</td>' +
                 '<td style="padding:10px 14px;border:1px solid #e6e6e6;color:#222;">' + val + '</td>' +
               '</tr>';
      }).join("");

      var html =
        '<div style="font-family:Arial,Helvetica,sans-serif;max-width:560px;margin:0 auto;">' +
          '<div style="background:#0b0b0f;padding:18px 22px;border-radius:10px 10px 0 0;">' +
            '<span style="color:#fff;font-size:18px;font-weight:700;letter-spacing:.4px;">ONE <span style="color:#e50914;">IPTV</span></span>' +
            '<span style="color:#9aa0a6;font-size:13px;float:right;padding-top:4px;">New order</span>' +
          '</div>' +
          '<table style="border-collapse:collapse;width:100%;font-size:14px;">' + trs + '</table>' +
          '<p style="color:#9aa0a6;font-size:12px;margin:14px 2px 0;">' +
            'Sent automatically from ' + esc(website) + ' when a visitor completed checkout.' +
          '</p>' +
        '</div>';

      var textLines = rows.map(function (r) { return r[0] + ": " + (r[1] || "—"); });

      MailApp.sendEmail({
        to: NOTIFY_EMAIL,
        subject: subject,
        body: textLines.join("\n"),   // plain-text fallback
        htmlBody: html,
        replyTo: email || NOTIFY_EMAIL
      });
    } catch (mailErr) {
      // Sheet write already succeeded; ignore email errors.
    }

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Minimal HTML escaper for email values.
function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// Open the web-app URL in a browser to confirm it is live.
function doGet() {
  return ContentService.createTextOutput("ONE IPTV order logger is running.");
}

/**
 * generate-pdf.js
 * Renders an HTML file to a PDF via Puppeteer.
 *
 * Usage:
 *   node lead-magnet-system/scripts/generate-pdf.js <input.html> <output.pdf>
 *
 * Example:
 *   node lead-magnet-system/scripts/generate-pdf.js \
 *     website/lead-magnets/ai-playbook-pdf.html \
 *     website/lead-magnets/ai-playbook.pdf
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function generatePdf(inputHtml, outputPdf) {
  const absInput = path.resolve(inputHtml);
  const absOutput = path.resolve(outputPdf);

  if (!fs.existsSync(absInput)) {
    console.error(`Input file not found: ${absInput}`);
    process.exit(1);
  }

  const outDir = path.dirname(absOutput);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const browser = await puppeteer.launch({ headless: true });
  try {
    const page = await browser.newPage();
    await page.goto(`file://${absInput}`, { waitUntil: 'networkidle0' });

    // Force light theme for PDF (dark backgrounds waste ink / look bad in PDF)
    await page.evaluate(() => {
      document.documentElement.setAttribute('data-theme', 'light');
    });

    // Hide nav and interactive elements not needed in PDF
    await page.addStyleTag({
      content: `
        nav, .theme-btn, #optInForm, .form-card, .final-cta, footer { display: none !important; }
        body { padding-top: 0 !important; }
        .page { padding-top: 24px !important; }
      `
    });

    await page.pdf({
      path: absOutput,
      format: 'A4',
      printBackground: true,
      margin: { top: '20mm', right: '18mm', bottom: '20mm', left: '18mm' },
    });

    console.log(`PDF saved: ${absOutput}`);
  } finally {
    await browser.close();
  }
}

const [,, inputHtml, outputPdf] = process.argv;
if (!inputHtml || !outputPdf) {
  console.error('Usage: node generate-pdf.js <input.html> <output.pdf>');
  process.exit(1);
}

generatePdf(inputHtml, outputPdf).catch((err) => {
  console.error('PDF generation failed:', err.message);
  process.exit(1);
});

// Remake assets/Shaun-Burley-CV.pdf from the CV panel after the CV text changes.
// Serve the site first (python3 -m http.server 8765), then: node tools/cv-pdf.js
// Needs Playwright (npm install playwright) and a Chromium it can launch.
const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  const page = await browser.newPage();
  await page.goto("http://localhost:8765/#cv", { waitUntil: "networkidle" });
  await page.waitForTimeout(600); // let the panel finish fading in
  await page.pdf({ path: path.join(__dirname, "..", "assets", "Shaun-Burley-CV.pdf"), format: "Letter" });
  await browser.close();
})();

const { chromium } = require("playwright");
const fs = require("fs");

const BASE = "http://localhost:3000";
const OUT = "screenshots";

const personas = [
  { name: "sdm", label: "SDM" },
  { name: "srsdm", label: "Senior-SDM" },
  { name: "director", label: "Director" },
  { name: "junior", label: "Junior-Engineer" },
  { name: "senior", label: "Senior-Engineer" },
  { name: "staff", label: "Staff-Engineer" },
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  if (!fs.existsSync(OUT)) fs.mkdirSync(OUT);

  for (const p of personas) {
    await page.goto(`${BASE}`);
    await page.waitForTimeout(2000);

    await page.selectOption("select:first-of-type", p.name);
    await page.waitForTimeout(3000);

    await page.screenshot({ path: `${OUT}/dashboard-${p.name}.png`, fullPage: true });
    console.log(`Saved: dashboard-${p.name}.png`);
  }

  await page.goto(`${BASE}/admin`);
  await page.waitForTimeout(3000);
  await page.screenshot({ path: `${OUT}/admin.png`, fullPage: true });
  console.log("Saved: admin.png");

  await browser.close();
  console.log("Done. Screenshots in ./screenshots/");
})();

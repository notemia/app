#!/usr/bin/env node
// Generates static, per-language pages (/<lang>/index.html, privacy.html, support.html)
// from the root pages (git HEAD templates) + js/main.js (ru/en) + i18n/*.json.
// Usage: node tools/build-langs.js
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const root = path.join(__dirname, "..");
const SITE = "https://notemia.app";

const LANGS = [
  { dir: "ru",      html: "ru",      label: "Русский",             src: "ru",      store: "ru" },
  { dir: "en",      html: "en",      label: "English",             src: "en",      store: "us" },
  { dir: "de",      html: "de",      label: "Deutsch",             src: "de",      store: "de" },
  { dir: "es-es",   html: "es-ES",   label: "Español (España)",    src: "es",      store: "es" },
  { dir: "es-mx",   html: "es-MX",   label: "Español (México)",    src: "es",      store: "mx" },
  { dir: "it",      html: "it",      label: "Italiano",            src: "it",      store: "it" },
  { dir: "pt-br",   html: "pt-BR",   label: "Português (Brasil)",  src: "pt-br",   store: "br" },
  { dir: "tr",      html: "tr",      label: "Türkçe",              src: "tr",      store: "tr" },
  { dir: "zh-hans", html: "zh-Hans", label: "简体中文",            src: "zh-hans", store: "cn" },
];

// ru/en dictionaries come from the existing JS engine
const mainSrc = fs.readFileSync(path.join(root, "js/main.js"), "utf8");
const T = eval("(" + mainSrc.match(/const T = (\{[\s\S]*?\n\});/)[1] + ")");
const dict = { ru: {}, en: {} };
for (const k in T) { dict.ru[k] = T[k].ru; dict.en[k] = T[k].en; }
for (const f of fs.readdirSync(path.join(root, "i18n"))) {
  dict[f.replace(".json", "")] = JSON.parse(fs.readFileSync(path.join(root, "i18n", f), "utf8"));
}

// Templates: the deployed (committed) pages, so unfinished local edits are not published.
const tpl = n => execSync(`git show HEAD:${n}`, { cwd: root, encoding: "utf8" });
const PAGES = ["index.html", "privacy.html", "support.html"];

function build(lang, page, html) {
  const d = dict[lang.src];
  const get = k => (d[k] !== undefined && d[k] !== "") ? d[k] : dict.en[k];

  // text for [data-i18n]
  html = html.replace(/(<([a-zA-Z0-9]+)\b[^>]*\bdata-i18n="([^"]+)"[^>]*>)([\s\S]*?)(<\/\2>)/g,
    (m, open, tag, key, inner, close) => {
      const v = get(key);
      return v === undefined ? m : open + v + close;
    });
  // <title>
  // (covered above: title has data-i18n)

  // storefront-specific App Store links
  html = html.replace(/https:\/\/apps\.apple\.com\/[a-z]{2}\//g, `https://apps.apple.com/${lang.store}/`);
  html = html.replace(/\sdata-i18n-href="[^"]+"/g, "");
  html = html.replace(/(<a href=")https:\/\/apps\.apple\.com\/[a-z]{2}\/app\/psymap\/id6758890986\?mt=12/, `$1https://apps.apple.com/${lang.store}/app/psymap/id6758890986`);

  // logo alt texts and a broken relative fallback path
  const altMap = { "Гештальт мастерская": "gestaltist_name", "КПТ мастерская": "cbt_name", "ТА мастерская": "ta_name", "Психоанализ мастерская": "analyst_name" };
  html = html.replace(/alt="([^"]+)"/g, (m, a) => altMap[a] ? `alt="${get(altMap[a])}"` : m);
  html = html.replace(/this\.src='img\//g, "this.src='../img/");

  // html lang + static flag
  html = html.replace(/<html lang="[^"]*">/, `<html lang="${lang.html}" data-static>`);

  // assets and links one level up
  html = html.replace(/(href|src)="(css\/|js\/|img\/)/g, '$1="../$2');
  html = html.replace(/href="index\.html#/g, 'href="index.html#');

  // language switcher -> select with real links
  const opts = LANGS.map(l =>
    `<option value="/${l.dir}/${page}"${l.dir === lang.dir ? " selected" : ""}>${l.label}</option>`).join("");
  html = html.replace(/<div class="lang-switch">[\s\S]*?<\/div>/,
    `<div class="lang-switch"><select class="lang-select" aria-label="Language" onchange="location.href=this.value">${opts}</select></div>`);

  // hide ru-only blocks for non-Russian pages is handled by css/lang-pages.css
  // canonical + hreflang
  const alt = LANGS.map(l => `<link rel="alternate" hreflang="${l.html}" href="${SITE}/${l.dir}/${page === "index.html" ? "" : page}">`).join("\n  ");
  const canon = `<link rel="canonical" href="${SITE}/${lang.dir}/${page === "index.html" ? "" : page}">`;
  html = html.replace("</head>", `  ${canon}\n  ${alt}\n  <link rel="stylesheet" href="../css/lang-pages.css">\n</head>`);

  // meta description in the page language
  const desc = get(page === "privacy.html" ? "priv_intro" : page === "support.html" ? "support_sub" : "hero_badge");
  html = html.replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${String(desc).replace(/<[^>]+>/g, " ").replace(/"/g, "&quot;")}">`);
  return html;
}

for (const lang of LANGS) {
  const out = path.join(root, lang.dir);
  fs.mkdirSync(out, { recursive: true });
  for (const page of PAGES) {
    fs.writeFileSync(path.join(out, page), build(lang, page, tpl(page)));
  }
}
console.log("built", LANGS.map(l => l.dir).join(", "));

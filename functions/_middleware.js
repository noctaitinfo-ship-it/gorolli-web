const COUNTRY_TO_LANG = {
  EE: "et",
  FI: "fi",
  DE: "de",
  AT: "de",
  CH: "de",
  FR: "fr",
  BE: "fr",
  LU: "fr",
  MC: "fr",
  ES: "es",
  MX: "es",
  AR: "es",
  CO: "es",
  CL: "es",
  PE: "es",
  PL: "pl",
  LV: "lv",
  LT: "lt",
  RU: "ru",
  SE: "sv",
  DK: "da",
  UA: "uk",
  IT: "it",
  NL: "nl",
  PT: "pt",
  BR: "pt",
  CZ: "cs",
  SK: "sk",
  HU: "hu",
  RO: "ro",
  MD: "ro",
  BG: "bg",
  TR: "tr",
  GR: "el",
  CY: "el",
  HR: "hr",
  SI: "sl",
  RS: "sr",
  BA: "sr",
  ME: "sr",
  IL: "he",
  IN: "hi",
  CN: "zh",
  HK: "zh",
  TW: "zh",
  SG: "zh",
  JP: "ja",
  KR: "ko"
};

const SUPPORTED = new Set([
  "en","et","de","pl","lv","fi","lt","ru","sv","da","uk","es","fr","it","nl","pt",
  "cs","sk","hu","ro","bg","tr","el","hr","sl","sr","ar","he","hi","zh","ja","ko"
]);

function languageFromAcceptLanguage(header) {
  if (!header) return null;

  const parts = header.split(",");
  for (const part of parts) {
    const code = part.trim().split(";")[0].toLowerCase().split("-")[0];
    if (SUPPORTED.has(code)) return code;
  }

  return null;
}

export async function onRequest(context) {
  const request = context.request;
  const url = new URL(request.url);
  const path = url.pathname;

  if (path !== "/" && path !== "/index.html") {
    return context.next();
  }

  const country = request.cf && request.cf.country ? request.cf.country.toUpperCase() : "";
  const countryLang = COUNTRY_TO_LANG[country];
  const browserLang = languageFromAcceptLanguage(request.headers.get("Accept-Language"));
  const lang = countryLang || browserLang || "en";

  return Response.redirect(`${url.origin}/${lang}`, 302);
}
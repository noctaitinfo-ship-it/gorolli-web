const SITE = 'https://www.gorolli.com';

const LOCALES = {
  et: {
    title: 'Haagise rent lähedal | GoRolli',
    description: 'Leia ja rendi sobiv haagis enda lähedalt. Võrdle asukohti ja hindu ning broneeri GoRollis veebis või äpis.',
    h1: 'Haagise rent sinu lähedal.',
    lead: 'Leia sobiv haagis kolimiseks, ehituseks, paadi või aiatööde jaoks ja broneeri veebis või äpis.'
  },
  en: {
    title: 'Trailer rental near you | GoRolli',
    description: 'Find and rent a trailer near you. Compare nearby options and prices, then book on the web or in the GoRolli app.',
    h1: 'Trailer rental near you.',
    lead: 'Find the right trailer for moving, building, boats or garden work and book it on the web or in the app.'
  },
  de: {
    title: 'Anhänger mieten in der Nähe | GoRolli',
    description: 'Finde und miete einen Anhänger in deiner Nähe. Vergleiche Standorte und Preise und buche online oder in der GoRolli App.',
    h1: 'Anhänger mieten in deiner Nähe.',
    lead: 'Finde den passenden Anhänger für Umzug, Bau, Boot oder Garten und buche online oder in der App.'
  },
  fi: {
    title: 'Peräkärryn vuokraus lähellä | GoRolli',
    description: 'Löydä ja vuokraa peräkärry läheltä. Vertaile sijainteja ja hintoja ja varaa verkossa tai GoRolli-sovelluksessa.',
    h1: 'Peräkärryn vuokraus lähelläsi.',
    lead: 'Löydä sopiva peräkärry muuttoon, rakentamiseen, veneelle tai pihatöihin ja varaa verkossa tai sovelluksessa.'
  },
  lv: {
    title: 'Piekabes noma tuvumā | GoRolli',
    description: 'Atrodi un iznomā piekabi tuvumā. Salīdzini atrašanās vietas un cenas un rezervē tīmeklī vai GoRolli lietotnē.',
    h1: 'Piekabes noma tavā tuvumā.',
    lead: 'Atrodi piemērotu piekabi pārvākšanās, būvniecības, laivas vai dārza darbiem un rezervē tīmeklī vai lietotnē.'
  },
  lt: {
    title: 'Priekabų nuoma netoliese | GoRolli',
    description: 'Rask ir išsinuomok priekabą netoliese. Palygink vietas ir kainas, rezervuok internetu arba GoRolli programėlėje.',
    h1: 'Priekabų nuoma netoliese.',
    lead: 'Rask tinkamą priekabą kraustymuisi, statyboms, valčiai ar sodo darbams ir rezervuok internetu arba programėlėje.'
  },
  pl: {
    title: 'Wynajem przyczep w pobliżu | GoRolli',
    description: 'Znajdź i wynajmij przyczepę w pobliżu. Porównaj lokalizacje i ceny, a następnie zarezerwuj online lub w aplikacji GoRolli.',
    h1: 'Wynajem przyczep w pobliżu.',
    lead: 'Znajdź odpowiednią przyczepę do przeprowadzki, budowy, łodzi lub prac ogrodowych i zarezerwuj online albo w aplikacji.'
  }
};

function routeLocale(pathname) {
  if (pathname === '/' || pathname === '') return 'et';
  const match = pathname.match(/^\/(en|et|de|fi|lv|lt|pl)\/?$/i);
  return match ? match[1].toLowerCase() : null;
}

function canonicalFor(locale, pathname) {
  return pathname === '/' ? `${SITE}/` : `${SITE}/${locale}`;
}

function escapeHtml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

function escapeScriptJson(value) {
  return value.replaceAll('<', '\u003c');
}

class SetAttribute {
  constructor(name, value) {
    this.name = name;
    this.value = value;
  }
  element(element) {
    element.setAttribute(this.name, this.value);
  }
}

class SetText {
  constructor(value) {
    this.value = value;
  }
  element(element) {
    element.setInnerContent(this.value);
  }
}

class AppendLocalizedHead {
  constructor(locale, data, canonical) {
    this.locale = locale;
    this.data = data;
    this.canonical = canonical;
  }
  element(element) {
    const schema = {
      '@context': 'https://schema.org',
      '@type': 'WebPage',
      '@id': `${this.canonical}#webpage`,
      url: this.canonical,
      name: this.data.title,
      description: this.data.description,
      inLanguage: this.locale,
      isPartOf: { '@id': `${SITE}/#website` },
      about: { '@id': `${SITE}/#org` }
    };

    element.append(
      `<meta property="og:locale" content="${this.locale}">` +
      `<meta name="twitter:title" content="${escapeHtml(this.data.title)}">` +
      `<meta name="twitter:description" content="${escapeHtml(this.data.description)}">` +
      `<script type="application/ld+json">${escapeScriptJson(JSON.stringify(schema))}</script>`,
      { html: true }
    );
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const locale = routeLocale(url.pathname);

    if (!locale || !['GET', 'HEAD'].includes(request.method)) {
      return env.ASSETS.fetch(request);
    }

    if (url.pathname !== '/' && url.pathname.endsWith('/')) {
      url.pathname = `/${locale}`;
      return Response.redirect(url.toString(), 308);
    }

    const data = LOCALES[locale];
    const canonical = canonicalFor(locale, url.pathname);
    const explicitLocale = url.pathname !== '/';

    // Cloudflare Pages ASSETS must be requested by the public "pretty" path.
    // Requesting /index.html or /fi.html makes the asset layer redirect back to
    // / or /fi, which sends the browser into an endless self-redirect loop.
    const assetPath = explicitLocale ? `/${locale}` : '/';
    const assetUrl = new URL(assetPath, url);
    const assetResponse = await env.ASSETS.fetch(new Request(assetUrl.toString(), request));

    if (!assetResponse.ok) {
      return assetResponse;
    }

    const headers = new Headers(assetResponse.headers);
    headers.set('Content-Language', locale);
    headers.set('X-Robots-Tag', 'index, follow');
    headers.delete('Content-Length');

    if (request.method === 'HEAD') {
      return new Response(null, {
        status: assetResponse.status,
        statusText: assetResponse.statusText,
        headers
      });
    }

    const htmlResponse = new Response(assetResponse.body, {
      status: assetResponse.status,
      statusText: assetResponse.statusText,
      headers
    });

    return new HTMLRewriter()
      .on('html', new SetAttribute('lang', locale))
      .on('head', new AppendLocalizedHead(locale, data, canonical))
      .on('title', new SetText(data.title))
      .on('meta[name="description"]', new SetAttribute('content', data.description))
      .on('link[rel="canonical"]', new SetAttribute('href', canonical))
      .on('meta[property="og:url"]', new SetAttribute('content', canonical))
      .on('meta[property="og:title"]', new SetAttribute('content', data.title))
      .on('meta[property="og:description"]', new SetAttribute('content', data.description))
      .on('main h1', new SetText(data.h1))
      .on('main .lead', new SetText(data.lead))
      .transform(htmlResponse);
  }
};
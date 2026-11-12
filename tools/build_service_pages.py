#!/usr/bin/env python3
"""Generate the service landing pages in public/ from the content below.

Edit the SERVICES list, then run:  python3 tools/build_service_pages.py
Commit the regenerated public/*.html files (Cloudflare serves public/ as-is).
"""
import json
from pathlib import Path

SITE = "https://probamo.com"
PUBLIC = Path(__file__).resolve().parent.parent / "public"

HOW_IT_WORKS = [
    ("Share access", "Send the URL, build or login details and tell us which flows matter most. We confirm scope and price before we start."),
    ("We test as real users", "A person works through your product on real devices, looking for anything that breaks, confuses or blocks."),
    ("You get a report", "Written findings with steps to reproduce, severity, impact and screenshots or video, typically within 2–3 working days."),
]

SERVICES = [
    {
        "slug": "website-qa",
        "nav": "Website QA",
        "package": "Website QA",
        "title": "Website QA Testing Service | Probamo",
        "description": "Manual website QA testing by real people: forms, links, layout and core functions across devices. Bug report with screenshots. From €55.",
        "eyebrow": "Website QA testing",
        "h1": "Website QA testing by real people, before your visitors find the bugs",
        "lead": "We click through your site the way visitors do — every button, form, link and layout — and send a clear bug report with screenshots, so you can fix problems before they cost you enquiries.",
        "service_type": "Website QA testing",
        "price_from": "55",
        "tests": [
            ("Forms and validation", "Contact, sign-up and booking forms: required fields, error messages and confirmation emails."),
            ("Links and navigation", "Broken links, wrong targets, menus and anchor links on desktop and mobile."),
            ("Layout and responsiveness", "Text, images and buttons at phone, tablet and desktop widths."),
            ("Core functionality", "Search, filters, logins and anything else your site depends on."),
            ("Content", "Typos, missing images, placeholder text and outdated information."),
            ("Compatibility (Advanced)", "Six device and browser combinations, prepared test scenarios and a basic SEO check."),
        ],
        "pricing": [
            "<strong>Website QA starts at €55</strong> for a standard check of buttons, forms, links, layout and core functionality, with a bug report and screenshots.",
            "<strong>Advanced starts at €205</strong> and adds prepared test scenarios, a fuller report, compatibility testing across 6 device/browser combinations and a basic SEO check.",
            "Sites with several subpages are priced per page. We confirm the page count before you book.",
        ],
        "faq": [
            ("What is website QA testing?", "Website QA (quality assurance) testing checks that a site works as intended before and after it goes live. Manual QA is done by people, not scripts, so it also catches confusing flows, layout problems and content mistakes that automated checks miss."),
            ("Do you test on mobile?", "Yes. Layout and core flows are checked on mobile and desktop. The Advanced pack covers six device and browser combinations."),
            ("What do you need from me?", "The URL, any logins or test accounts, and a short note on the pages or flows that matter most."),
            ("How long does it take?", "Reports typically arrive within 2–3 working days, depending on how many pages are in scope."),
        ],
        "related": ["webshop-qa", "ai-app-testing", "regression-testing"],
    },
    {
        "slug": "webshop-qa",
        "nav": "Webshop QA",
        "package": "Webshop QA",
        "title": "Webshop & E-commerce QA Testing | Probamo",
        "description": "Manual e-commerce testing for webshops: product pages, cart, checkout and order emails tested end-to-end with a test order. From €75.",
        "eyebrow": "Webshop and e-commerce testing",
        "h1": "Webshop testing that follows the whole order, from product page to confirmation email",
        "lead": "Checkout bugs cost sales quietly. We place test orders the way your customers do and report anything that blocks, confuses or breaks the purchase.",
        "service_type": "E-commerce QA testing",
        "price_from": "75",
        "tests": [
            ("Product pages", "Images, variants, prices, stock messages and add-to-cart."),
            ("Cart", "Quantities, totals, shipping costs and discount codes."),
            ("Checkout", "Address, shipping and payment steps, completed with a test product."),
            ("After the purchase", "Confirmation page, order emails and customer account access."),
            ("Mobile shopping", "The full purchase on a phone, where most checkouts happen."),
            ("The rest of the shop", "Everything in Website QA: forms, links, layout and content."),
        ],
        "pricing": [
            "<strong>Webshop QA starts at €75</strong> and includes Website QA plus checkout and post-purchase tested end-to-end with a test product.",
            "<strong>Advanced starts at €280</strong>, with expanded scenarios, deeper compatibility testing and fuller reporting for shops where revenue depends on a smooth checkout.",
            "<strong>Product page check add-on:</strong> €105 (standard) or €305 (premium) for up to 5 pages, then €10 or €20 per extra page.",
        ],
        "faq": [
            ("Will you place real orders?", "We test with a test product and safe test payment details, ideally on a staging copy of your shop. If you only have a live shop, we agree the approach with you first."),
            ("Which shop platforms do you test?", "Any webshop we can get access to, whether it runs on a platform such as Shopify or WooCommerce or is custom-built. We test what your customers see, not the code."),
            ("When should I test my webshop?", "Before launch, after a redesign, theme or plugin update, after a payment provider change and before big campaigns."),
            ("How long does it take?", "Reports typically arrive within 2–3 working days, depending on scope."),
        ],
        "related": ["website-qa", "digital-products-qa", "regression-testing"],
    },
    {
        "slug": "mobile-app-testing",
        "nav": "Mobile apps",
        "package": "Mobile app testing",
        "title": "Mobile App Testing Service | Probamo",
        "description": "Manual mobile app testing by real people: onboarding, core flows, payments and real-world interruptions, reported with steps and screen recordings.",
        "eyebrow": "Mobile app testing",
        "h1": "Mobile app testing by people who use apps the way your customers do",
        "lead": "We install your app, go through onboarding and the flows that matter, and try what real users do — rotating the phone, losing connection, switching apps — then report what breaks.",
        "service_type": "Mobile app testing",
        "price_from": None,
        "tests": [
            ("Onboarding and sign-up", "First launch, permissions, account creation and login."),
            ("Core flows", "The tasks your users open the app for, from start to finish."),
            ("Payments and subscriptions", "Purchases and upgrades in test mode, including what happens when they fail."),
            ("Interruptions", "Calls, notifications, backgrounding the app and losing connection mid-task."),
            ("Screens and layout", "Different screen sizes, orientation and text size settings."),
            ("Before release", "A regression pass on a release candidate before you submit to the store."),
        ],
        "pricing": [
            "<strong>Mobile app testing is quoted per project.</strong> We agree the devices, OS versions and flows with you, then confirm a fixed price.",
            "For a focused first look, the <a href=\"/#pricing\">Bug Catcher</a> package gives you 6 hours of testing with a full report.",
        ],
        "faq": [
            ("How do I share the app with you?", "Through a pre-release channel such as TestFlight or an internal testing track, or as a build file. We can also test the store version."),
            ("Which devices do you test on?", "We agree the devices and operating system versions with you when we scope the project, based on what your users have."),
            ("Can you test before release?", "Yes. Testing a release candidate before store submission is one of the most useful times to do it."),
            ("How long does it take?", "Reports typically arrive within 2–3 working days, depending on scope."),
        ],
        "related": ["regression-testing", "ai-app-testing", "iot-hardware-testing"],
    },
    {
        "slug": "regression-testing",
        "nav": "Regression testing",
        "package": "Regression QA",
        "title": "Manual Regression Testing Service | Probamo",
        "description": "Ongoing manual regression testing aligned with your release schedule: prepared scenarios and a dedicated testing window, so releases don't break what already worked.",
        "eyebrow": "Regression testing",
        "h1": "Manual regression testing that keeps up with your releases",
        "lead": "Every release can break something that used to work. We prepare scenarios in advance and test in a dedicated window before you ship, so releases don't slip through untested.",
        "service_type": "Regression testing",
        "price_from": None,
        "tests": [
            ("Prepared scenarios", "Written in advance for your critical flows and updated as your product changes."),
            ("Dedicated testing window", "An agreed day and time when your release is under review."),
            ("Critical paths, every release", "Sign-up, login, checkout and whatever your business depends on."),
            ("New features and their surroundings", "What changed, plus the screens around it that changes tend to break."),
            ("Release verdict", "What passed, what broke and what to fix before shipping."),
            ("A consistent tester", "The same person learns your product over time and spots changes quickly."),
        ],
        "pricing": [
            "<strong>Regression QA is quoted per project</strong> as a monthly agreement aligned with your deployment schedule.",
            "Tell us how often you release and which flows matter most, and we'll propose a plan.",
        ],
        "faq": [
            ("What is regression testing?", "Regression testing checks that features which worked before still work after a change. It's done before each release so updates don't quietly break existing functionality."),
            ("Why manual instead of automated?", "Automated tests check exactly what they were written to check. People notice when something looks wrong, feels slow or confuses users. Manual regression works well alongside automated tests, or before you have them."),
            ("How often do you test?", "On your schedule: weekly, per sprint or before each release. We agree a regular testing window."),
            ("Can we cancel?", "Monthly agreements renew as agreed in your order, with the notice period stated there."),
        ],
        "related": ["mobile-app-testing", "website-qa", "ai-app-testing"],
    },
    {
        "slug": "ai-app-testing",
        "nav": "AI-built apps",
        "package": "Bug Catcher",
        "title": "Testing for AI-Built Apps & Websites | Probamo",
        "description": "Human QA for products built with AI tools and no-code builders: edge cases, broken flows, UX gaps and trust issues found before launch.",
        "eyebrow": "Testing AI-built products",
        "h1": "A human check for apps and websites built with AI",
        "lead": "AI tools let you ship in days. They also produce flows that work on the happy path and fail everywhere else. We test your product like a real user and show you what to fix before customers find it.",
        "service_type": "QA testing for AI-generated software",
        "price_from": None,
        "tests": [
            ("Edge cases", "Empty fields, very long inputs, double clicks, the back button and refreshing mid-flow."),
            ("Accounts and logins", "Sign-up, email confirmation, password reset and sessions."),
            ("Payments", "Checkout and subscription flows in test mode, including failures."),
            ("Obvious access problems", "Pages that open without logging in, or show data they shouldn't."),
            ("UX gaps", "Dead ends, missing error messages and screens with no clear next step."),
            ("Trust details", "Placeholder text, broken links, missing legal pages and emails that land in spam."),
        ],
        "pricing": [
            "<strong>The <a href=\"/#pricing\">Bug Catcher</a> package is the usual starting point:</strong> 6 hours of focused testing before launch or after a big change, with a prioritised bug list and full report.",
            "Larger products are quoted per project.",
        ],
        "faq": [
            ("Do you test apps made with Lovable, Bolt, v0, Cursor or Bubble?", "Yes. We test the product, not the code, so it doesn't matter which tool built it."),
            ("Do you fix the bugs?", "No. We're independent testers. You get a clear report that you, your developer or your AI tool can work from."),
            ("Is this a security audit?", "No. We flag obvious access problems we come across, but a full security test needs a specialist."),
            ("When should I test?", "Before you launch or start paid marketing, and after any big change generated in one go."),
        ],
        "related": ["website-qa", "mobile-app-testing", "webshop-qa"],
    },
    {
        "slug": "digital-products-qa",
        "nav": "Digital products",
        "package": "Digital products QA",
        "title": "QA Testing for Digital Products & Online Courses | Probamo",
        "description": "End-to-end testing for creators selling courses, PDFs and templates: sales page, checkout, delivery emails and access, tested as a real buyer.",
        "eyebrow": "Digital products QA",
        "h1": "Make sure every buyer actually gets what they paid for",
        "lead": "Courses, PDFs, templates and memberships rely on a chain of tools: page builder, checkout, email and course platform. We buy like a customer and check every link in that chain.",
        "service_type": "Digital product checkout and delivery testing",
        "price_from": None,
        "tests": [
            ("Sales page", "Buttons, prices, links and layout on desktop and mobile."),
            ("Checkout", "Payment steps, discount codes, upsells and bundles, if you use them."),
            ("Delivery", "Confirmation emails, download links and file access."),
            ("Course and member access", "Login, lessons, drip content and what happens after a password reset."),
            ("Mobile buyers", "The full purchase and first lesson on a phone."),
            ("The awkward moments", "Expired links, buying twice and coming back days later."),
        ],
        "pricing": [
            "<strong>Digital products QA is quoted per project.</strong> Tell us what you sell and which tools you use, and we'll confirm a fixed price.",
        ],
        "faq": [
            ("Will you make a real purchase?", "We use a test product, a 100% discount code or your platform's test mode, agreed with you first."),
            ("Which platforms do you test?", "Any setup we can buy through as a customer. We test the buyer's journey across all your tools, not one platform's settings."),
            ("When should I test?", "Before a launch, after switching tools and before a promotion or email campaign."),
            ("How long does it take?", "Reports typically arrive within 2–3 working days, depending on scope."),
        ],
        "related": ["webshop-qa", "website-qa", "ai-app-testing"],
    },
    {
        "slug": "iot-hardware-testing",
        "nav": "IoT & hardware",
        "package": "Hardware, robotics or IoT software",
        "title": "IoT & Hardware Software Testing | Probamo",
        "description": "Manual testing for software that works with hardware: device setup, companion apps, IoT dashboards and robotics interfaces, tested from the user's side.",
        "eyebrow": "IoT, robotics and hardware software",
        "h1": "Testing for IoT, robotics and hardware-connected software",
        "lead": "When software controls a physical device, bugs show up as devices that won't pair, settings that don't stick and dashboards that show the wrong state. We test from the user's side: setup, control and everything in between.",
        "service_type": "IoT and hardware software testing",
        "price_from": None,
        "tests": [
            ("Setup and pairing", "First-time setup, pairing, re-pairing and factory reset flows."),
            ("Companion apps", "Mobile and desktop apps that control or monitor the device."),
            ("Dashboards and portals", "Web interfaces for fleets, readings, alerts and settings."),
            ("State and sync", "Whether the app shows what the device is actually doing."),
            ("Connectivity", "Weak signal, dropped connections and recovering afterwards."),
            ("Updates", "App and firmware update flows as the user experiences them."),
        ],
        "pricing": [
            "<strong>IoT and hardware testing is quoted per project.</strong> We agree the devices, environments and how we get access to test units, then confirm a fixed price.",
        ],
        "faq": [
            ("Do you need the hardware?", "Usually yes. We agree whether you send a test unit, give remote access or provide a simulator."),
            ("Do you test firmware code?", "We test from the user's side: setup, control, apps and dashboards. Low-level firmware and electrical testing need a specialist lab."),
            ("What have you tested before?", "Software for hardware, robotics and IoT products, alongside web and mobile apps."),
            ("How long does it take?", "It depends on the setup. We agree the timeline when we scope the project."),
        ],
        "related": ["mobile-app-testing", "regression-testing", "website-qa"],
    },
]

BY_SLUG = {s["slug"]: s for s in SERVICES}


def footer_services():
    links = "\n".join(
        f'          <a href="/{s["slug"]}">{s["nav"].replace("&", "&amp;")}</a>' for s in SERVICES
    )
    return f'''        <nav class="footer-services" aria-label="Services">
{links}
        </nav>
'''


def header():
    return '''    <header class="site-header">
      <div class="container header-inner">
        <a class="logo" href="/">
          <span class="logo-mark" aria-hidden="true">◈</span>
          Probamo
        </a>
        <nav class="nav" aria-label="Main">
          <a href="/#why">Why us</a>
          <a href="/#services">Services</a>
          <a href="/#pricing">Pricing</a>
          <a href="/#contact" class="nav-cta">Get a quote</a>
        </nav>
        <button
          class="menu-toggle"
          type="button"
          aria-expanded="false"
          aria-controls="mobile-nav"
          aria-label="Open menu"
        >
          <span class="menu-bars" aria-hidden="true"><span></span><span></span><span></span></span>
          <span class="menu-toggle-text">Menu</span>
        </button>
      </div>
      <nav id="mobile-nav" class="mobile-nav" hidden>
        <div class="mobile-nav-inner">
          <a href="/#why">Why us</a>
          <a href="/#services">Services</a>
          <a href="/#pricing">Pricing</a>
          <a href="/#contact" class="mobile-nav-cta">Get a quote</a>
        </div>
      </nav>
    </header>'''


def footer():
    return f'''    <footer class="site-footer">
      <div class="container footer-inner">
        <p><span class="logo-mark" aria-hidden="true">◈</span> Probamo — independent manual QA</p>
        <p class="footer-small">Human feedback for builders, startups, and AI-assisted products.</p>
{footer_services()}        <nav class="footer-legal" aria-label="Legal">
          <a href="/privacy">Privacy policy</a>
          <span aria-hidden="true">·</span>
          <a href="/terms">Terms &amp; conditions</a>
        </nav>
        <p class="footer-entity">
          PROBAMO, obrt za usluge i trgovinu, vl. Sara Lubura · Biševska Ulica 2, Veliko Polje, Zagreb, Croatia ·
          Registered in the Croatian Register of Crafts (Obrtni registar), MBO 99405709 ·
          <a href="mailto:testing@probamo.com">testing@probamo.com</a>
        </p>
      </div>
    </footer>'''


def strip_tags(text):
    import re
    return re.sub(r"<[^>]+>", "", text)


def structured_data(s):
    url = f'{SITE}/{s["slug"]}'
    service = {
        "@type": "Service",
        "@id": f"{url}#service",
        "name": s["eyebrow"],
        "serviceType": s["service_type"],
        "description": s["description"],
        "url": url,
        "provider": {"@id": f"{SITE}/#organization"},
        "areaServed": "Worldwide",
    }
    if s["price_from"]:
        service["offers"] = {
            "@type": "Offer",
            "url": url,
            "priceSpecification": {
                "@type": "PriceSpecification",
                "minPrice": s["price_from"],
                "priceCurrency": "EUR",
            },
        }
    graph = [
        service,
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": s["nav"], "item": url},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in s["faq"]
            ],
        },
    ]
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    return "\n".join("      " + line for line in data.splitlines())


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def page(s):
    url = f'{SITE}/{s["slug"]}'
    quote_href = f'/?package={s["package"].replace(" ", "%20").replace(",", "%2C")}#contact'
    tests = "\n".join(
        f'''            <article class="card">
              <h3>{esc(t)}</h3>
              <p>{esc(d)}</p>
            </article>''' for t, d in s["tests"]
    )
    steps = "\n".join(
        f'''            <li class="step">
              <span class="step-n">{i}</span>
              <h3>{esc(t)}</h3>
              <p>{esc(d)}</p>
            </li>''' for i, (t, d) in enumerate(HOW_IT_WORKS, 1)
    )
    pricing = "\n".join(f"            <p>{p}</p>" for p in s["pricing"])
    faq = "\n".join(
        f'''            <details class="faq-item">
              <summary>{esc(q)}</summary>
              <p>{esc(a)}</p>
            </details>''' for q, a in s["faq"]
    )
    related = "\n".join(
        f'            <li><a href="/{r}">{esc(BY_SLUG[r]["eyebrow"])} →</a></li>' for r in s["related"]
    )
    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{esc(s["description"])}" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="{url}" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Probamo" />
    <meta property="og:title" content="{esc(s["title"])}" />
    <meta property="og:description" content="{esc(s["description"])}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:locale" content="en_GB" />
    <meta property="og:image" content="{SITE}/og-image.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:image" content="{SITE}/og-image.png" />
    <title>{esc(s["title"])}</title>
    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
    <meta name="theme-color" content="#0a0e14" />
    <link rel="preload" href="/fonts/dmsans-latin.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="stylesheet" href="/css/styles.css" />
    <script type="application/ld+json">
{structured_data(s)}
    </script>
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    <div class="bg-grid" aria-hidden="true"></div>

{header()}

    <main id="main">
      <section class="hero page-hero">
        <div class="container">
          <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="/">Home</a> <span aria-hidden="true">/</span> <span aria-current="page">{esc(s["nav"])}</span>
          </nav>
          <p class="eyebrow">{esc(s["eyebrow"])}</p>
          <h1>{esc(s["h1"])}</h1>
          <p class="lead">{esc(s["lead"])}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="{quote_href}">Request a quote</a>
            <a class="btn btn-ghost" href="/#deliverables">See an example finding</a>
          </div>
        </div>
      </section>

      <section class="section section-alt" aria-labelledby="tests-h">
        <div class="container">
          <header class="section-head section-head-tight">
            <h2 id="tests-h">What we test</h2>
          </header>
          <div class="cards cards-why">
{tests}
          </div>
        </div>
      </section>

      <section class="section" aria-labelledby="how-h">
        <div class="container">
          <header class="section-head section-head-tight">
            <h2 id="how-h">How it works</h2>
          </header>
          <ol class="steps">
{steps}
          </ol>
        </div>
      </section>

      <section class="section section-alt" aria-labelledby="price-h">
        <div class="container service-pricing">
          <div>
            <h2 id="price-h">Pricing</h2>
{pricing}
            <p class="price-note-line">50% upfront to confirm your booking. No VAT is added.</p>
          </div>
          <div class="service-cta">
            <a class="btn btn-primary btn-block" href="{quote_href}">Request a quote</a>
            <a class="text-link" href="/#pricing">All packages and prices →</a>
          </div>
        </div>
      </section>

      <section class="section" aria-labelledby="faq-h">
        <div class="container faq-wrap">
          <header class="section-head section-head-tight">
            <h2 id="faq-h">Questions</h2>
          </header>
          <div class="faq">
{faq}
          </div>
        </div>
      </section>

      <section class="section section-alt" aria-labelledby="related-h">
        <div class="container">
          <h2 id="related-h" class="related-h">Related services</h2>
          <ul class="related-links">
{related}
          </ul>
        </div>
      </section>
    </main>

{footer()}

    <script src="/js/main.js"></script>
  </body>
</html>
'''


def main():
    for s in SERVICES:
        out = PUBLIC / f'{s["slug"]}.html'
        out.write_text(page(s), encoding="utf-8")
        print("wrote", out.relative_to(PUBLIC.parent))


if __name__ == "__main__":
    main()

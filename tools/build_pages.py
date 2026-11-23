#!/usr/bin/env python3
"""Generate Probamo's service pages from the PAGES list below.

Run from the repo root:  python3 tools/build_pages.py
Writes public/<slug>.html for every page and rewrites the shared navigation and
footer on the homepage, book-a-call, legal and 404 pages so they stay in sync.
"""
import json
import re
from pathlib import Path

SITE = "https://probamo.com"
PUBLIC = Path(__file__).resolve().parent.parent / "public"

ICONS = {
    "package": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3"/><path d="M12 12l8-4.5"/><path d="M12 12v9"/><path d="M12 12L4 7.5"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
    "handover": '<path d="M4 12h12"/><path d="M12 8l4 4-4 4"/><path d="M20 4v16"/>',
    "refresh": '<path d="M20 11A8.1 8.1 0 0 0 4.5 9M4 5v4h4"/><path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4"/>',
    "search": '<circle cx="10" cy="10" r="7"/><path d="M21 21l-6-6"/>',
    "users": '<circle cx="9" cy="7" r="4"/><path d="M3 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/><path d="M21 21v-2a4 4 0 0 0-3-3.85"/>',
    "chart": '<path d="M4 19h16"/><path d="M4 15l4-6 4 2 4-5 4 4"/>',
    "userminus": '<circle cx="9" cy="7" r="4"/><path d="M3 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2"/><path d="M16 11h6"/>',
    "card": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18"/><path d="M7 15h3"/>',
    "star": '<path d="M12 17.75l-6.17 3.24 1.18-6.88-5-4.87 6.9-1 3.09-6.26 3.09 6.26 6.9 1-5 4.87 1.18 6.88z"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M8 16l2-6 6-2-2 6-6 2"/>',
    "pulse": '<path d="M3 12h4l3 8 4-16 3 8h4"/>',
    "team": '<circle cx="9" cy="7" r="4"/><path d="M3 21v-2a4 4 0 0 1 4-4h4"/><path d="M15 19l2 2 4-4"/>',
    "rocket": '<path d="M4 13a8 8 0 0 1 7 7a6 6 0 0 0 3-5a9 9 0 0 0 6-8a3 3 0 0 0-3-3a9 9 0 0 0-8 6a6 6 0 0 0-5 3"/><circle cx="15" cy="9" r="1"/>',
}
ICON_ORDER = ["", "ico-blue", "ico-coral", "ico-sun", "", "ico-blue"]

STEPS = [
    ("Intro call", "Tell us about the product or project, your concerns and your deadline."),
    ("Scope and quote", "We define what will be tested and how many testing days it takes, then send a fixed quote."),
    ("Testing", "We test against your requirements and real use, and flag blockers as soon as they appear."),
    ("Report and retest", "You receive the report and recommendation, and we retest fixes before sign-off."),
]

MAIN_SERVICES = [
    ("acceptance-testing", "Acceptance testing"),
    ("drop-off-audit", "Drop-off audit"),
    ("manual-qa-testing", "Manual QA testing"),
]

PAGES = [
    # ------------------------------------------------------------------ main services
    {
        "slug": "acceptance-testing",
        "nav": "Acceptance testing",
        "title": "Acceptance Testing Services — Independent UAT Before Sign-off | Probamo",
        "description": "Independent acceptance testing and UAT for new software and releases. Verify a delivery against what was agreed before you sign off, pay or go live.",
        "service_type": "Acceptance testing",
        "service": "Acceptance testing",
        "eyebrow": "Core service",
        "h1": "Acceptance testing before you sign off",
        "lead": "Independent verification that new software or a release does what was agreed, whether it was built by your own team or an external partner. You get a clear go / no-go recommendation before you sign off, pay or go live.",
        "when_h": "When to bring us in",
        "when": [
            ("flag", "Before milestone sign-off", "Check each milestone against the agreed scope before it is approved and invoiced."),
            ("rocket", "Before go-live", "Find blockers while there is still time to fix them, not after customers do."),
            ("handover", "After handover", "Use the warranty period to document defects while the development team is still obliged to fix them."),
            ("search", "When taking over software", "Get an independent picture of software built by someone else before you take responsibility for it."),
        ],
        "test_h": "What we check",
        "tests": [
            ("Agreed requirements", "Contract, specification, user stories or emails: every agreed function is tested and marked as met, partly met or missing."),
            ("End-to-end journeys", "Key processes from start to finish, the way customers and staff will really use them, including the unhappy paths."),
            ("Roles, permissions and data", "Who can see and change what, and whether data is saved, calculated and displayed correctly."),
            ("Integrations", "Payments, emails, notifications, exports and connections to the systems you already use."),
            ("Devices and browsers", "The devices, browsers and screen sizes your users actually have."),
            ("What nobody wrote down", "Obvious expectations missing from the specification: error messages, slow connections, edge cases."),
        ],
        "prose": [
            ("Why independent acceptance testing?",
             ["Development teams test what they built, the way they built it. That testing is necessary, but it is not a neutral check against what you asked for, and it rarely covers the whole journey your customers and staff will take.",
              "Your own team knows the product best, but testing properly takes days they usually don’t have. Independent acceptance testing fills that gap: an outside team with no stake in the outcome checks the software from the business side, against your requirements, your users and your risks."]),
            ("Acceptance testing and UAT",
             ["User acceptance testing (UAT) is traditionally done by the people who will use the software. In practice, few businesses can spare them for long enough to test thoroughly. We run the acceptance test for you, using your requirements and real-world scenarios, and involve your users where their judgement matters most.",
              "The result is a decision document, not just a bug list: what meets the agreement, what does not, what blocks sign-off, and what can wait."]),
            ("Testing grounded in real operations",
             ["Our experience comes from operations-heavy industries: logistics, warehouse management, delivery services, e-commerce, micromobility, robotics and customer support. Software in these environments is used under time pressure, on shared devices and alongside other systems.",
              "We test with that reality in mind. Can a dispatcher get through a shift? Can a customer complete an order on a slow phone? Will the support team be flooded on launch day? Those questions decide whether a release is really ready."]),
        ],
        "deliverables": [
            "A go / no-go recommendation in plain language",
            "Requirement-by-requirement status: met, partly met or missing",
            "Every issue documented with steps to reproduce, severity and evidence",
            "Issues ranked by business impact, ready for your development team",
            "A retest of the fixes before you sign off",
        ],
        "faq": [
            ("What is acceptance testing?", "Acceptance testing verifies that new software or a release does what was agreed before you sign off, pay or go live. It is tested against requirements and real use, and ends with a clear recommendation: ready, ready with conditions, or not ready."),
            ("What is the difference between acceptance testing and UAT?", "User acceptance testing (UAT) is acceptance testing carried out from the users’ point of view. We run it on your behalf, using your requirements and real-world scenarios, and involve your users where their input is needed."),
            ("Does it matter who built the software?", "No. We test software built by in-house teams and by external partners in the same way: against what was agreed and how it will be used."),
            ("What if nothing was written down?", "We help you capture the key expectations first, from contracts, emails, demos and your own knowledge of the business, so there is a clear basis for the test."),
            ("Will you work with our developers?", "You decide. Reports go to you; with your approval we share findings directly with your development team and retest their fixes."),
            ("How long does an acceptance test take?", "It depends on the size of the release. The number of testing days is agreed upfront and stated in the quote, planned around your sign-off or launch date."),
        ],
        "related": ["manual-qa-testing", "regression-testing", "drop-off-audit"],
    },
    {
        "slug": "drop-off-audit",
        "nav": "Drop-off audit",
        "title": "Drop-off Audit — Find Out Why Users Leave or Never Pay | Probamo",
        "description": "A drop-off audit tests your product from your users’ point of view to find where and why they leave, stop using it or never become paying customers.",
        "service_type": "User experience testing",
        "service": "Drop-off audit",
        "eyebrow": "For products that lose users",
        "h1": "Find out why users leave, and what to fix first",
        "lead": "When people try a product and leave, there is usually a specific reason: a confusing step, a flow that fails on one device, or a promise the product doesn’t keep. A drop-off audit tests your product from your users’ point of view to find it.",
        "when_h": "Signs you need a drop-off audit",
        "when": [
            ("userminus", "Sign-ups don’t become active users", "People register or download, look around once, and never come back."),
            ("card", "Trials don’t convert", "Free trials end without an upgrade, and nobody can say exactly why."),
            ("star", "Poor reviews and feedback", "Ratings are lukewarm and complaints are vague: “confusing”, “didn’t work”, “not for me”."),
            ("chart", "Marketing spend isn’t paying off", "Acquisition costs rise while retention stays flat."),
        ],
        "test_h": "How we find the cause",
        "tests": [
            ("Expert walkthrough", "We go through sign-up, onboarding, first use and upgrade as a new user would, on the devices your users have."),
            ("Testing with real users", "We recruit people who match your audience and observe where they hesitate, get lost or give up."),
            ("Analytics and recordings", "Where analytics or session recordings exist, we review them to confirm where users drop off."),
            ("Functional checks", "Many drop-offs are bugs in disguise: a form that fails on one browser, an email that never arrives."),
            ("Promise versus product", "We compare what your website and app store page promise with what the first session delivers."),
            ("Payment and upgrade path", "Pricing pages, paywalls, checkout and the moment users are asked to pay."),
        ],
        "prose": [
            ("Testing, not guesswork",
             ["Analytics show where users leave. They rarely show why. A drop-off audit combines the numbers with hands-on testing and observation of real people, so each drop-off point is linked to a concrete cause you can fix.",
              "Because we test as well as review, we also catch the technical problems that look like a lack of interest: a broken step on one device, a slow screen, a confirmation that never arrives."]),
            ("What a drop-off audit covers",
             ["Use one, two or all three methods: expert walkthrough, testing with real users, and review of your analytics and recordings. The scope and number of testing days are agreed before we start.",
              "The result is one report: where users leave, why, the likely business impact, and a prioritised list of fixes, from quick wins to larger changes."]),
            ("Common reasons users drop off",
             ["In our experience, most drop-offs come from a small number of causes: sign-up that asks for too much too early, onboarding that explains features instead of helping users reach a first result, steps that fail silently on certain devices, and pricing or upgrade screens that appear before users have seen the value.",
              "Some causes are outside the product: a website or app store page that promises something the first session doesn’t deliver. A drop-off audit looks at the whole journey, from first visit to first payment, so the fix is aimed at the real cause."]),
        ],
        "deliverables": [
            "A map of where users drop off in your key journeys",
            "The cause of each drop-off, with evidence: clips, quotes, screenshots or data",
            "The likely business impact of each issue",
            "A prioritised list of fixes, from quick wins to larger changes",
            "A walkthrough of the findings with your team",
        ],
        "faq": [
            ("What is a drop-off audit?", "A drop-off audit finds out why users leave your product or never become paying customers. We test the product from your users’ point of view, combining an expert walkthrough, testing with real users and, where available, your analytics and session recordings."),
            ("Is a drop-off audit the same as UX testing?", "It is a focused form of user experience testing. Instead of reviewing usability in general, it concentrates on one business question: where and why users stop, and what to fix first."),
            ("Do we need analytics for this?", "No. Analytics and session recordings make the audit faster and more precise, but the walkthrough and testing with real users work without them."),
            ("How do you recruit test users?", "We agree the profile with you, such as role, industry, experience or device, and recruit people who match it. Your own customers can also take part."),
            ("What types of product do you audit?", "Web apps, SaaS products, mobile apps, webshops and customer portals: anything where users sign up, try, buy or subscribe."),
        ],
        "related": ["acceptance-testing", "mobile-app-testing", "webshop-qa"],
    },
    {
        "slug": "manual-qa-testing",
        "nav": "Manual QA testing",
        "title": "Manual QA Testing Services — Experienced Testers, Clear Reports | Probamo",
        "description": "Manual QA testing for web apps, mobile apps, webshops and software for hardware. Release testing, exploratory testing and fixed-scope Health Checks.",
        "service_type": "Manual software testing",
        "service": "Manual QA testing",
        "eyebrow": "Ongoing or one-off",
        "h1": "Manual QA testing by experienced testers",
        "lead": "Hands-on testing, the way your customers and staff use your product. For teams without a tester, before a release, or alongside automated tests.",
        "when_h": "Ways to use manual QA",
        "when": [
            ("refresh", "Before every release", "A regular testing window on your release schedule. Prepared scenarios confirm that new features work and existing ones still do."),
            ("compass", "Exploratory testing", "Unscripted testing that finds what checklists miss: unusual paths, real devices, slow connections, confusing steps."),
            ("pulse", "Health Check", "A fixed-scope review of a website, webshop, mobile app or AI-built app, with a report in 2–3 working days."),
            ("team", "Extra testing capacity", "Additional testers when your own team is busy, without hiring."),
        ],
        "test_h": "What we test",
        "tests": [
            ("Functionality", "Every feature in scope, including the paths users take by mistake."),
            ("Regression", "That existing features still work after changes and fixes."),
            ("Compatibility", "Real devices, browsers, operating systems and screen sizes."),
            ("Usability", "Steps that confuse, slow down or mislead users."),
            ("Content", "Text, translations, images and data shown to users."),
            ("Integrations", "Payments, emails, exports, APIs and connected devices."),
        ],
        "prose": [
            ("Why manual testing still matters",
             ["Automated tests check exactly what they were written to check. People notice when something looks wrong, feels slow or doesn’t make sense. Manual testing finds the problems users actually run into, and works well before automated tests exist or alongside them.",
              "Our testers work from your users’ point of view, on the devices they use, and document each issue so your developers can reproduce it straight away."]),
        ],
        "deliverables": [
            "Written findings with steps to reproduce",
            "Severity and impact on users and the business",
            "Screenshots or screen recordings",
            "Device, browser and build for every issue",
            "A short summary for decision-makers",
        ],
        "faq": [
            ("What is manual QA testing?", "Manual QA (quality assurance) testing means a person uses your software the way your customers and staff would, looking for bugs, confusing steps and anything that blocks them."),
            ("How is manual testing different from automated testing?", "Automated tests check exactly what they were written to check. Manual testers notice when something looks wrong, feels slow or confuses users. The two work best together."),
            ("Can you test on a regular schedule?", "Yes. Ongoing testing gives you an agreed number of testing days each month, scheduled around your releases."),
            ("What is a Health Check?", "A fixed-scope review of a website, webshop, mobile app or AI-built app, with a report in 2–3 working days. It is a good first engagement."),
            ("What do you need from us?", "Access to a test environment, build or URL, test accounts, and a short note on which areas matter most."),
        ],
        "related": ["acceptance-testing", "regression-testing", "mobile-app-testing"],
        "children": True,
    },
    # ------------------------------------------------------------------ manual QA specialisms
    {
        "slug": "website-qa",
        "parent": "manual-qa-testing",
        "short": "Forms, links, layout and content across devices",
        "nav": "Website QA",
        "title": "Website QA Testing — Forms, Links and Layout Checked | Probamo",
        "description": "Manual website QA testing: forms, links, layout, content and core functions checked across devices, with a clear report before or after launch.",
        "service_type": "Website testing",
        "service": "Manual QA testing",
        "eyebrow": "Manual QA testing",
        "h1": "Website QA testing before your visitors find the problems",
        "lead": "We check your website the way visitors use it: every form, link, layout and core function across devices, with a clear report your team can act on.",
        "test_h": "What we test",
        "tests": [
            ("Forms and validation", "Contact, sign-up and booking forms: required fields, error messages and confirmation emails."),
            ("Links and navigation", "Broken links, wrong targets, menus and anchor links on desktop and mobile."),
            ("Layout and responsiveness", "Text, images and buttons at phone, tablet and desktop widths."),
            ("Core functionality", "Search, filters, logins and anything else the site depends on."),
            ("Content", "Typos, missing images, placeholder text and outdated information."),
            ("Compatibility", "The browsers and devices your visitors use."),
        ],
        "faq": [
            ("What is website QA testing?", "Website QA testing checks that a site works as intended before and after it goes live: forms, links, layout, content and core functions, on the devices visitors use."),
            ("When should a website be tested?", "Before launch, after a redesign or migration, and after significant content or plugin updates."),
            ("Do you test WordPress, Webflow and other platforms?", "Yes. We test what visitors see and do, so the platform does not limit the test."),
            ("How long does it take?", "A Health Check of a typical business website takes 2–3 working days."),
        ],
        "related": ["webshop-qa", "manual-qa-testing", "drop-off-audit"],
    },
    {
        "slug": "webshop-qa",
        "parent": "manual-qa-testing",
        "short": "Product pages, checkout, payments and order emails",
        "nav": "Webshop QA",
        "title": "Webshop & E-commerce Testing — Checkout Tested End to End | Probamo",
        "description": "E-commerce testing for webshops: product pages, cart, checkout, payments and order emails tested end to end with test orders.",
        "service_type": "E-commerce testing",
        "service": "Manual QA testing",
        "eyebrow": "Manual QA testing",
        "h1": "Webshop testing: from product page to order confirmation",
        "lead": "Lost checkouts are lost revenue. We test your shop end to end with test orders, on the devices your customers use, and report everything that stands between a visitor and a completed order.",
        "test_h": "What we test",
        "tests": [
            ("Product pages", "Variants, prices, stock, images and add-to-cart on desktop and mobile."),
            ("Cart and checkout", "Discount codes, shipping rules, delivery countries, taxes and address validation."),
            ("Payments", "Test payments with each method you offer, including failed and cancelled payments."),
            ("Order emails", "Confirmations, invoices, shipping notifications and what the customer sees after paying."),
            ("Accounts", "Registration, login, password reset and order history."),
            ("Search and filters", "Finding products the way customers search for them."),
        ],
        "faq": [
            ("Will you place real orders?", "We use test modes and test payment methods wherever possible. If a real order is needed, we agree it with you first."),
            ("Which shop platforms do you test?", "Any platform: we test what customers see and do, whether the shop runs on a hosted platform or custom software."),
            ("Can you test before a sales campaign?", "Yes. Testing before a campaign or seasonal peak is one of the most common reasons to book."),
            ("What if users add to cart but don’t buy?", "That is a drop-off problem. A drop-off audit looks at why customers abandon the checkout and what to fix first."),
        ],
        "related": ["drop-off-audit", "website-qa", "manual-qa-testing"],
    },
    {
        "slug": "mobile-app-testing",
        "parent": "manual-qa-testing",
        "short": "Real iOS and Android devices, real-world conditions",
        "nav": "Mobile app testing",
        "title": "Mobile App Testing on Real iOS and Android Devices | Probamo",
        "description": "Manual mobile app testing on real iOS and Android devices: onboarding, core flows, permissions, notifications and interruptions.",
        "service_type": "Mobile application testing",
        "service": "Manual QA testing",
        "eyebrow": "Manual QA testing",
        "h1": "Mobile app testing on real devices",
        "lead": "We test your iOS and Android app the way people use their phones: on real devices, with interruptions, weak connections and the permissions users actually grant.",
        "test_h": "What we test",
        "tests": [
            ("Onboarding", "First launch, sign-up, permissions and the first minutes of use."),
            ("Core flows", "The features your users rely on, end to end."),
            ("Interruptions", "Calls, notifications, backgrounding, rotation and lost connections."),
            ("Devices and versions", "Different screen sizes and operating system versions."),
            ("Notifications", "Push and in-app messages: timing, content and where they lead."),
            ("Purchases and subscriptions", "In-app purchases, trials and upgrade screens in test mode."),
        ],
        "faq": [
            ("Do you test on real devices?", "Yes. Testing on real phones finds problems that simulators miss, such as performance, gestures and interruptions."),
            ("How do you get the app?", "Through the usual test distribution channels for iOS and Android, or a build you send us."),
            ("Can you test an app before it is published?", "Yes. Testing before store submission is the best time to find blockers."),
            ("What if users install the app and then stop using it?", "A drop-off audit focuses on why users leave after installing, and what to fix first."),
        ],
        "related": ["drop-off-audit", "acceptance-testing", "manual-qa-testing"],
    },
    {
        "slug": "regression-testing",
        "parent": "manual-qa-testing",
        "short": "Every release checked on a fixed schedule",
        "nav": "Regression testing",
        "title": "Regression Testing Services — Every Release Checked | Probamo",
        "description": "Manual regression testing on your release schedule: prepared scenarios confirm that existing features still work after every change.",
        "service_type": "Regression testing",
        "service": "Ongoing testing",
        "eyebrow": "Manual QA testing",
        "h1": "Regression testing on every release",
        "lead": "When every fix breaks something else, releases become a risk. We test your critical flows on a regular schedule, so problems are found before your users see them.",
        "test_h": "How it works",
        "tests": [
            ("Prepared scenarios", "We document your critical flows once and keep the scenarios up to date as the product changes."),
            ("A fixed testing window", "An agreed day and time for each release, so testing fits your schedule."),
            ("Changed areas", "Exploratory testing of what changed in the release, alongside the regression scenarios."),
            ("Fix verification", "Confirmation that reported issues are actually fixed."),
            ("Release summary", "A short go / no-go summary for each release."),
            ("Trend reporting", "Which areas break most often, so your team can focus effort."),
        ],
        "faq": [
            ("What is regression testing?", "Regression testing checks that existing features still work after changes, fixes or updates."),
            ("How is ongoing testing billed?", "Ongoing testing is billed monthly for an agreed number of testing days. The scope is stated in the order."),
            ("Can you work alongside automated tests?", "Yes. Manual regression covers what automated tests don’t: visual issues, usability and complex journeys."),
            ("How quickly do you report?", "Blockers are reported as soon as they are found; the full summary follows the testing window."),
        ],
        "related": ["acceptance-testing", "manual-qa-testing", "mobile-app-testing"],
    },
    {
        "slug": "ai-app-testing",
        "parent": "manual-qa-testing",
        "short": "Independent QA for apps built with AI tools",
        "nav": "AI-built apps",
        "title": "Testing AI-built Apps — Independent QA Before Launch | Probamo",
        "description": "Independent testing for apps built with AI coding tools: core flows, edge cases, data handling and security basics checked before real users arrive.",
        "service_type": "Software testing",
        "service": "Manual QA testing",
        "eyebrow": "Manual QA testing",
        "h1": "Testing for apps built with AI tools",
        "lead": "AI tools make building fast. They also produce software that works in the demo and fails with real users. We test what was generated before your customers do.",
        "test_h": "What we test",
        "tests": [
            ("Core flows", "Sign-up, login, the main features and payments, end to end."),
            ("Edge cases", "Empty fields, long inputs, double clicks, going back, and other things real users do."),
            ("Data handling", "Whether data is saved, shown and deleted correctly, and only to the right people."),
            ("Error handling", "What users see when something goes wrong."),
            ("Devices and browsers", "Layout and behaviour across phones, tablets and desktops."),
            ("Security basics", "Visible issues such as exposed data or pages accessible without login."),
        ],
        "faq": [
            ("Why do AI-built apps need testing?", "Generated code often handles the expected path well and the unexpected ones badly. Manual testing finds those gaps before users do."),
            ("Do you review the code?", "We test the application from the outside, as users do. Code review and penetration testing need a specialist."),
            ("Which tools do you test apps from?", "Any. We test the running application, regardless of how it was built."),
            ("What is the best starting point?", "A Health Check: a fixed-scope review with a report in 2–3 working days."),
        ],
        "related": ["manual-qa-testing", "acceptance-testing", "website-qa"],
    },
    {
        "slug": "iot-hardware-testing",
        "parent": "manual-qa-testing",
        "short": "Setup, companion apps, dashboards and operations",
        "nav": "IoT & hardware",
        "title": "IoT, Robotics and Hardware Software Testing | Probamo",
        "description": "Testing software for connected devices, robotics and hardware: setup, companion apps, dashboards and real-world use, remote or on site by agreement.",
        "service_type": "IoT software testing",
        "service": "Manual QA testing",
        "eyebrow": "Manual QA testing",
        "h1": "Testing software for IoT, robotics and hardware",
        "lead": "When software controls physical devices, failures are expensive and visible. We test setup, control apps and dashboards the way operators and customers use them, remotely or on site by agreement.",
        "test_h": "What we test",
        "tests": [
            ("Setup and pairing", "Unboxing to first use: pairing, onboarding and configuration."),
            ("Companion apps", "Mobile and web apps that control or monitor the device."),
            ("Dashboards", "Operator and admin dashboards, alerts and reports."),
            ("Connectivity", "Lost connections, reconnection, offline mode and syncing."),
            ("Operational scenarios", "Shift changes, many devices at once, and real-world conditions."),
            ("Updates", "Firmware and app updates from the user’s side."),
        ],
        "faq": [
            ("Do you need the hardware?", "Usually yes. We agree whether you send a test unit, give remote access, provide a simulator or host us on site."),
            ("Can you test on site?", "Yes. On-site visits and testing are possible anywhere by prior agreement."),
            ("Do you test firmware?", "We test from the user’s and operator’s side. Low-level firmware and electrical testing need a specialist lab."),
            ("What experience do you have?", "Robotics and automation, micromobility, warehouse and delivery operations, alongside web and mobile apps."),
        ],
        "related": ["acceptance-testing", "mobile-app-testing", "manual-qa-testing"],
    },
]

BY_SLUG = {p["slug"]: p for p in PAGES}
SPECIALISMS = [p for p in PAGES if p.get("parent") == "manual-qa-testing"]


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ico(name, cls=""):
    c = f"ico {cls}".strip()
    return (f'<span class="{c}" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg></span>')


def book_href(p):
    return "/book-a-call?service=" + p["service"].replace(" ", "%20")


# ---------------------------------------------------------------- shared chrome

def nav_links(indent):
    pad = " " * indent
    items = [(f"/{s}", n) for s, n in MAIN_SERVICES] + [("/#how", "How we work")]
    return "\n".join(f'{pad}<a href="{h}">{esc(n)}</a>' for h, n in items)


def header():
    return f'''    <header class="site-header">
      <div class="container header-inner">
        <a class="logo" href="/">
          <span class="logo-mark" aria-hidden="true">◈</span>
          Probamo
        </a>
        <nav class="nav" aria-label="Main">
{nav_links(10)}
          <a href="/book-a-call" class="nav-cta">Book a call</a>
        </nav>
        <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu">
          <span class="menu-bars" aria-hidden="true"><span></span><span></span><span></span></span>
          <span class="menu-toggle-text">Menu</span>
        </button>
      </div>
      <nav id="mobile-nav" class="mobile-nav" hidden>
        <div class="mobile-nav-inner">
{nav_links(10)}
          <a href="/#experience">Experience</a>
          <a href="/#contact">Contact</a>
          <a href="/book-a-call" class="mobile-nav-cta">Book a call</a>
        </div>
      </nav>
    </header>'''


def footer():
    main = "\n".join(f'          <a href="/{s}">{esc(n)}</a>' for s, n in MAIN_SERVICES)
    subs = "\n".join(f'          <a href="/{p["slug"]}">{esc(p["nav"])}</a>' for p in SPECIALISMS)
    return f'''    <footer class="site-footer">
      <div class="container footer-inner">
        <p><span class="logo-mark" aria-hidden="true">◈</span> Probamo — independent software testing</p>
        <p class="footer-small">Acceptance testing, manual QA and drop-off audits. Remote worldwide, on-site by agreement.</p>
        <nav class="footer-services" aria-label="Services">
{main}
{subs}
        </nav>
        <nav class="footer-legal" aria-label="Legal">
          <a href="/book-a-call">Book a call</a>
          <span aria-hidden="true">·</span>
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


# ---------------------------------------------------------------- page

def crumbs(p):
    trail = [("Home", f"{SITE}/")]
    if p.get("parent"):
        par = BY_SLUG[p["parent"]]
        trail.append((par["nav"], f'{SITE}/{par["slug"]}'))
    trail.append((p["nav"], f'{SITE}/{p["slug"]}'))
    return trail


def structured_data(p):
    url = f'{SITE}/{p["slug"]}'
    graph = [
        {
            "@type": "Service",
            "@id": f"{url}#service",
            "name": p["nav"],
            "serviceType": p["service_type"],
            "description": p["description"],
            "url": url,
            "provider": {"@id": f"{SITE}/#organization"},
            "areaServed": "Worldwide",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs(p))
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]
            ],
        },
    ]
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    return "\n".join("      " + line for line in data.splitlines())


def cards(items, with_icons):
    out = []
    for i, item in enumerate(items):
        if with_icons:
            icon, title, text = item
            head = f"\n              {ico(icon, ICON_ORDER[i % len(ICON_ORDER)])}"
        else:
            title, text = item
            head = ""
        out.append(f'''            <article class="card">{head}
              <h3>{esc(title)}</h3>
              <p>{esc(text)}</p>
            </article>''')
    return "\n".join(out)


def page(p):
    url = f'{SITE}/{p["slug"]}'
    trail = crumbs(p)
    crumb_html = ' <span aria-hidden="true">/</span> '.join(
        [f'<a href="{u.replace(SITE, "") or "/"}">{esc(n)}</a>' for n, u in trail[:-1]]
        + [f'<span aria-current="page">{esc(trail[-1][0])}</span>'])
    sections = []
    alt = True

    def section(inner, label):
        nonlocal alt
        cls = "section section-alt" if alt else "section"
        alt = not alt
        sections.append(f'''      <section class="{cls}" aria-labelledby="{label}">
        <div class="container">
{inner}
        </div>
      </section>''')

    if p.get("when"):
        section(f'''          <header class="section-head section-head-tight">
            <h2 id="when-h">{esc(p["when_h"])}</h2>
          </header>
          <div class="cards cards-four">
{cards(p["when"], True)}
          </div>''', "when-h")

    section(f'''          <header class="section-head section-head-tight">
            <h2 id="tests-h">{esc(p["test_h"])}</h2>
          </header>
          <div class="cards cards-three">
{cards(p["tests"], False)}
          </div>''', "tests-h")

    for i, (h, paras) in enumerate(p.get("prose", [])):
        body = "\n".join(f"            <p>{esc(t)}</p>" for t in paras)
        section(f'''          <div class="prose">
            <h2 id="prose-{i}">{esc(h)}</h2>
{body}
          </div>''', f"prose-{i}")

    if p.get("deliverables"):
        items = "\n".join(f"            <li>{esc(d)}</li>" for d in p["deliverables"])
        section(f'''          <header class="section-head section-head-tight">
            <h2 id="get-h">What you get</h2>
          </header>
          <ul class="proof-list proof-list-cols">
{items}
          </ul>''', "get-h")

    if p.get("children"):
        links = "\n".join(
            f'            <a href="/{c["slug"]}">{esc(c["nav"])}<span>{esc(c["short"])}</span></a>'
            for c in SPECIALISMS)
        section(f'''          <header class="section-head section-head-tight">
            <h2 id="spec-h">Manual QA by product type</h2>
          </header>
          <nav class="service-links" aria-label="Manual QA by product type">
{links}
          </nav>''', "spec-h")

    steps = "\n".join(f'''            <li class="step">
              <span class="step-n">{i}</span>
              <h3>{esc(t)}</h3>
              <p>{esc(d)}</p>
            </li>''' for i, (t, d) in enumerate(STEPS, 1))
    section(f'''          <header class="section-head section-head-tight">
            <h2 id="how-h">How we work</h2>
          </header>
          <ol class="steps steps-four">
{steps}
          </ol>
          <div class="cta-band">
            <div>
              <h3>Discuss your project with us</h3>
              <p>Every project is quoted individually, with the scope and testing days stated upfront.</p>
            </div>
            <a class="btn btn-primary" href="{book_href(p)}">Book a call with us</a>
          </div>''', "how-h")

    faq = "\n".join(f'''            <details class="faq-item">
              <summary>{esc(q)}</summary>
              <p>{esc(a)}</p>
            </details>''' for q, a in p["faq"])
    section(f'''          <div class="faq-wrap">
            <header class="section-head section-head-tight">
              <h2 id="faq-h">Questions</h2>
            </header>
            <div class="faq">
{faq}
            </div>
          </div>''', "faq-h")

    related = "\n".join(
        f'            <li><a href="/{r}">{esc(BY_SLUG[r]["nav"])}</a></li>' for r in p["related"])
    section(f'''          <h2 id="related-h" class="related-h">Related services</h2>
          <ul class="related-links">
{related}
          </ul>''', "related-h")

    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{esc(p["description"])}" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="{url}" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Probamo" />
    <meta property="og:title" content="{esc(p["title"])}" />
    <meta property="og:description" content="{esc(p["description"])}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:locale" content="en_GB" />
    <meta property="og:image" content="{SITE}/og-image.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:image" content="{SITE}/og-image.png" />
    <title>{esc(p["title"])}</title>
    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
    <meta name="theme-color" content="#ffffff" />
    <link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="/fonts/spacegrotesk-latin.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="stylesheet" href="/css/styles.css" />
    <script type="application/ld+json">
{structured_data(p)}
    </script>
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>

{header()}

    <main id="main">
      <section class="hero page-hero">
        <div class="container">
          <nav class="breadcrumb" aria-label="Breadcrumb">{crumb_html}</nav>
          <p class="eyebrow">{esc(p["eyebrow"])}</p>
          <h1>{esc(p["h1"])}</h1>
          <p class="lead">{esc(p["lead"])}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="{book_href(p)}">Book a call with us</a>
            <a class="btn btn-ghost" href="/#reports">See how we report</a>
          </div>
        </div>
      </section>

{chr(10).join(sections)}
    </main>

{footer()}

    <script src="/js/main.js"></script>
  </body>
</html>
'''


# ---------------------------------------------------------------- keep other pages in sync

def sync_shared(path):
    s = path.read_text(encoding="utf-8")
    s = re.sub(r'    <header class="site-header">.*?</header>', header(), s, count=1, flags=re.S)
    s = re.sub(r'    <footer class="site-footer">.*?</footer>', footer(), s, count=1, flags=re.S)
    path.write_text(s, encoding="utf-8")


def main():
    for p in PAGES:
        out = PUBLIC / f'{p["slug"]}.html'
        out.write_text(page(p), encoding="utf-8")
        print("wrote", out.relative_to(PUBLIC.parent))
    for name in ["index.html", "book-a-call.html", "privacy.html", "terms.html", "404.html"]:
        sync_shared(PUBLIC / name)
        print("synced", name)


if __name__ == "__main__":
    main()

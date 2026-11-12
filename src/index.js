import { WorkerMailer } from "worker-mailer";

// Enquiries are sent from this Proton address (SMTP token stored as the SMTP_TOKEN secret)
// to the inbox below, with Reply-To set to the visitor.
const FROM = { name: "Probamo website", email: "forms@probamo.com" };
const TO = { name: "Probamo", email: "sara@probamo.com" };
const ALLOWED_ORIGINS = ["https://probamo.com", "https://www.probamo.com"];

const PACKAGES = [
  "Bug Catcher",
  "Website QA",
  "Webshop QA",
  "Product page check",
  "Regression QA",
  "User acceptance testing (UAT)",
  "API testing",
  "Digital products QA",
  "Not sure yet",
];

const LIMITS = { name: 100, email: 200, website: 300, deadline: 100, message: 5000 };

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/contact") {
      if (request.method !== "POST") {
        return json({ ok: false, error: "Method not allowed." }, 405, { Allow: "POST" });
      }
      return handleContact(request, env);
    }

    return env.ASSETS.fetch(request);
  },
};

async function handleContact(request, env) {
  const response = await processContact(request, env);
  // A plain HTML form post (no JavaScript) gets sent back to the page with the result.
  const accept = request.headers.get("Accept") || "";
  if (accept.includes("text/html")) {
    const outcome = await response.clone().json().catch(() => ({}));
    const result = outcome.ok ? "sent" : "error";
    return new Response(null, { status: 303, headers: { Location: `/?enquiry=${result}#contact` } });
  }
  return response;
}

async function processContact(request, env) {
  const origin = request.headers.get("Origin");
  if (origin && !ALLOWED_ORIGINS.includes(origin)) {
    return json({ ok: false, error: "Forbidden." }, 403);
  }

  let form;
  try {
    form = await request.formData();
  } catch {
    return json({ ok: false, error: "We couldn't read the form. Please try again." }, 400);
  }

  const field = (key) => String(form.get(key) ?? "").trim();

  // Honeypot: real visitors never see or fill this field.
  if (field("company_website")) {
    return json({ ok: true });
  }

  const data = {
    name: field("name"),
    email: field("email"),
    website: field("website"),
    package: field("package"),
    deadline: field("deadline"),
    message: field("message"),
  };

  const errors = validate(data);
  if (errors.length) {
    return json({ ok: false, error: errors.join(" ") }, 422);
  }

  if (env.TURNSTILE_SECRET) {
    const passed = await verifyTurnstile(field("cf-turnstile-response"), request, env.TURNSTILE_SECRET);
    if (!passed) {
      return json({ ok: false, error: "The spam check didn't pass. Please reload the page and try again." }, 400);
    }
  }

  if (!env.SMTP_TOKEN) {
    console.error("SMTP_TOKEN secret is not set");
    return json({ ok: false, error: fallbackMessage() }, 503);
  }

  try {
    const mailer = await WorkerMailer.connect({
      host: "smtp.protonmail.ch",
      port: 587,
      secure: false,
      startTls: true,
      authType: ["plain", "login"],
      credentials: { username: FROM.email, password: env.SMTP_TOKEN },
      socketTimeoutMs: 15000,
      responseTimeoutMs: 15000,
    });

    await mailer.send({
      from: FROM,
      to: TO,
      reply: { name: oneLine(data.name), email: data.email },
      subject: oneLine(`Website enquiry: ${data.package} — ${data.name}`),
      text: emailText(data, request),
    });

    await mailer.close?.();
  } catch (error) {
    console.error("Sending enquiry failed:", error?.message ?? error);
    return json({ ok: false, error: fallbackMessage() }, 502);
  }

  return json({ ok: true });
}

function validate(d) {
  const errors = [];
  if (!d.name) errors.push("Please enter your name.");
  if (!d.email) errors.push("Please enter your email address.");
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)) errors.push("Please check your email address.");
  if (!d.message) errors.push("Please tell us a little about your project.");
  if (!PACKAGES.includes(d.package)) errors.push("Please choose a package.");
  for (const [key, max] of Object.entries(LIMITS)) {
    if (d[key].length > max) errors.push(`The ${key} field is too long (max ${max} characters).`);
  }
  return errors;
}

async function verifyTurnstile(token, request, secret) {
  if (!token) return false;
  const body = new FormData();
  body.append("secret", secret);
  body.append("response", token);
  const ip = request.headers.get("CF-Connecting-IP");
  if (ip) body.append("remoteip", ip);
  try {
    const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body });
    const outcome = await res.json();
    return outcome.success === true;
  } catch (error) {
    console.error("Turnstile check failed:", error?.message ?? error);
    return false;
  }
}

function emailText(d, request) {
  const country = request.cf?.country ? ` (${request.cf.country})` : "";
  return [
    `New enquiry from the Probamo website${country}`,
    "",
    `Name:     ${d.name}`,
    `Email:    ${d.email}`,
    `Website:  ${d.website || "—"}`,
    `Package:  ${d.package}`,
    `Deadline: ${d.deadline || "—"}`,
    "",
    "Message:",
    d.message,
    "",
    "—",
    "Reply to this email to answer the sender directly.",
  ].join("\n");
}

function oneLine(value) {
  return value.replace(/[\r\n]+/g, " ").slice(0, 200);
}

function fallbackMessage() {
  return "We couldn't send your message just now. Please email testing@probamo.com directly.";
}

function json(body, status = 200, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...headers },
  });
}

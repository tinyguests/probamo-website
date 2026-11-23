import { WorkerMailer } from "worker-mailer";

// Enquiries are sent from this Proton address (SMTP token stored as the SMTP_TOKEN secret)
// to the inbox below, with Reply-To set to the visitor.
const FROM = { name: "Probamo website", email: "forms@probamo.com" };
const TO = { name: "Probamo", email: "sara@probamo.com" };
const ALLOWED_ORIGINS = ["https://probamo.com", "https://www.probamo.com"];

const PACKAGES = [
  "Acceptance testing",
  "Drop-off audit",
  "Manual QA testing",
  "Ongoing testing",
  "General question",
  // Older options, still sent by service pages until they are rewritten
  "Bug Catcher",
  "Website QA",
  "Webshop QA",
  "Product page check",
  "Regression QA",
  "User acceptance testing (UAT)",
  "API testing",
  "Digital products QA",
  "Mobile app testing",
  "Hardware, robotics or IoT software",
  "Sample report request",
  "Not sure yet",
];

const LIMITS = {
  name: 100,
  email: 200,
  phone: 50,
  position: 100,
  company: 200,
  company_id: 300,
  website: 300,
  deadline: 300,
  message: 5000,
};

// Two forms post here: a short question form on the homepage and the "Book a call" form.
const FORMS = {
  question: { page: "/", anchor: "#contact", required: ["name", "email", "message"] },
  call: { page: "/book-a-call", anchor: "#booking", required: ["name", "position", "company", "email", "package", "message"] },
};

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
    const form = FORMS[outcome.form] || FORMS.question;
    return new Response(null, { status: 303, headers: { Location: `${form.page}?enquiry=${result}${form.anchor}` } });
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

  const formType = field("form_type") === "call" ? "call" : "question";
  const data = {
    form: formType,
    name: field("name"),
    email: field("email"),
    phone: field("phone"),
    position: field("position"),
    company: field("company"),
    company_id: field("company_id"),
    website: field("website"),
    package: field("package") || (formType === "question" ? "General question" : ""),
    deadline: field("deadline"),
    message: field("message"),
  };

  const errors = validate(data);
  if (errors.length) {
    return json({ ok: false, form: formType, error: errors.join(" ") }, 422);
  }

  if (env.TURNSTILE_SECRET) {
    const passed = await verifyTurnstile(field("cf-turnstile-response"), request, env.TURNSTILE_SECRET);
    if (!passed) {
      return json({ ok: false, form: data.form, error: "The spam check didn’t pass. Please reload the page and try again." }, 400);
    }
  }

  if (!env.SMTP_TOKEN) {
    console.error("SMTP_TOKEN secret is not set");
    return json({ ok: false, form: data.form, error: fallbackMessage() }, 503);
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
      subject: oneLine(
        data.form === "call"
          ? `Call request: ${data.package} — ${data.company} (${data.name})`
          : `Website question — ${data.name}`,
      ),
      text: emailText(data, request),
    });

    await mailer.close?.();
  } catch (error) {
    console.error("Sending enquiry failed:", error?.message ?? error);
    return json({ ok: false, form: data.form, error: fallbackMessage() }, 502);
  }

  return json({ ok: true, form: data.form });
}

function validate(d) {
  const errors = [];
  const labels = {
    name: "your full name",
    position: "your position",
    company: "your company name",
    email: "your email address",
    package: "the service you need",
    message: "your message",
  };
  for (const key of FORMS[d.form].required) {
    if (!d[key]) errors.push(`Please enter ${labels[key]}.`);
  }
  if (d.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)) errors.push("Please check your email address.");
  if (d.package && !PACKAGES.includes(d.package)) errors.push("Please choose a service from the list.");
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
  const row = (label, value) => `${(label + ":").padEnd(22)}${value || "—"}`;
  const heading =
    d.form === "call" ? `New call request from the Probamo website${country}` : `New question from the Probamo website${country}`;
  const rows =
    d.form === "call"
      ? [
          row("Name", d.name),
          row("Position", d.position),
          row("Company", d.company),
          row("Company no. / address", d.company_id),
          row("Email", d.email),
          row("Phone", d.phone),
          row("Website", d.website),
          row("Service", d.package),
          row("Deadlines", d.deadline),
        ]
      : [row("Name", d.name), row("Email", d.email), row("Topic", d.package)];
  return [heading, "", ...rows, "", "Message:", d.message, "", "—", "Reply to this email to answer the sender directly."].join("\n");
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

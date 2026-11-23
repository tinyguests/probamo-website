const menuToggle = document.querySelector(".menu-toggle");
const mobileNav = document.getElementById("mobile-nav");

if (menuToggle && mobileNav) {
  const setMenu = (open) => {
    mobileNav.hidden = !open;
    menuToggle.setAttribute("aria-expanded", String(open));
    menuToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  };

  menuToggle.addEventListener("click", () => setMenu(mobileNav.hidden));

  mobileNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => setMenu(false));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !mobileNav.hidden) {
      setMenu(false);
      menuToggle.focus();
    }
  });

  // Close the mobile menu if the window grows to desktop width
  window.matchMedia("(min-width: 901px)").addEventListener("change", (event) => {
    if (event.matches) setMenu(false);
  });
}

// Enquiry forms (homepage question form and the "Book a call" form)
document.querySelectorAll("form[data-enquiry-form]").forEach((form) => {
  const status = form.querySelector(".form-status");
  const submitButton = form.querySelector('button[type="submit"]');
  const submitLabel = submitButton.textContent;
  const serviceSelect = form.querySelector("select[name='package']");
  const successHtml = form.dataset.success;

  const showStatus = (message, isError) => {
    status.textContent = message;
    status.classList.toggle("is-error", Boolean(isError));
  };

  const showSuccess = () => {
    form.innerHTML = `<div class="form-success" tabindex="-1">${successHtml}</div>`;
    form.querySelector(".form-success").focus();
  };

  // Pre-select the service from a link such as /book-a-call?service=Drop-off%20audit
  const params = new URLSearchParams(window.location.search);
  const requested = params.get("service") || params.get("package");
  if (serviceSelect && requested && [...serviceSelect.options].some((o) => o.value === requested)) {
    serviceSelect.value = requested;
  }

  // Result of a submission made without JavaScript
  const result = params.get("enquiry");
  if (result === "sent") showSuccess();
  if (result === "error") showStatus("We couldn’t send your message. Please email testing@probamo.com directly.", true);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    let firstInvalid = null;
    form.querySelectorAll("[required]").forEach((input) => {
      const invalid = !input.value.trim() || !input.checkValidity();
      input.setAttribute("aria-invalid", String(invalid));
      if (invalid && !firstInvalid) firstInvalid = input;
    });
    if (firstInvalid) {
      showStatus("Please complete the required fields marked above.", true);
      firstInvalid.focus();
      return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Sending…";
    showStatus("", false);

    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" },
      });
      const outcome = await response.json().catch(() => ({}));
      if (response.ok && outcome.ok) {
        showSuccess();
        return;
      }
      showStatus(outcome.error || "Something went wrong. Please email testing@probamo.com directly.", true);
    } catch {
      showStatus("You seem to be offline. Please try again, or email testing@probamo.com.", true);
    }

    submitButton.disabled = false;
    submitButton.textContent = submitLabel;
  });
});

// Copy buttons
document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      button.textContent = "Copied";
    } catch {
      button.textContent = "Select and copy";
    }
    setTimeout(() => {
      button.textContent = "Copy";
    }, 2000);
  });
});

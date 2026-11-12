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

// Contact form
const contactForm = document.getElementById("contact-form");

if (contactForm) {
  const status = document.getElementById("form-status");
  const submitButton = contactForm.querySelector('button[type="submit"]');
  const packageSelect = document.getElementById("cf-package");

  const showStatus = (message, isError) => {
    status.textContent = message;
    status.classList.toggle("is-error", Boolean(isError));
  };

  const showSuccess = () => {
    contactForm.innerHTML =
      '<div class="form-success" tabindex="-1"><h3>Thanks, your enquiry is on its way.</h3>' +
      "<p>We’ll reply by email to confirm scope and timing. If it’s urgent, write to testing@probamo.com.</p></div>";
    contactForm.querySelector(".form-success").focus();
  };

  // Pre-select the package when a "Book" or "Request quote" link is used
  document.querySelectorAll("a[data-package]").forEach((link) => {
    link.addEventListener("click", () => {
      packageSelect.value = link.dataset.package;
    });
  });

  // Result of a submission made without JavaScript
  const result = new URLSearchParams(window.location.search).get("enquiry");
  if (result === "sent") showSuccess();
  if (result === "error") {
    showStatus("We couldn’t send your message. Please email testing@probamo.com directly.", true);
  }

  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const required = ["cf-name", "cf-email", "cf-message"].map((id) => document.getElementById(id));
    let firstInvalid = null;
    required.forEach((input) => {
      const invalid = !input.value.trim() || (input.type === "email" && !input.checkValidity());
      input.setAttribute("aria-invalid", String(invalid));
      if (invalid && !firstInvalid) firstInvalid = input;
    });
    if (firstInvalid) {
      showStatus("Please fill in your name, a valid email address and what we should test.", true);
      firstInvalid.focus();
      return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Sending…";
    showStatus("", false);

    try {
      const response = await fetch(contactForm.action, {
        method: "POST",
        body: new FormData(contactForm),
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
    submitButton.textContent = "Send enquiry";
  });
}

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

// Launch offer: switch to the regular price once the offer has ended
const offer = document.querySelector("[data-offer-ends]");

if (offer && Date.now() >= Date.parse(offer.dataset.offerEnds)) {
  document.querySelectorAll("[data-offer-price]").forEach((el) => {
    el.textContent = offer.dataset.regularPrice;
  });
  offer.querySelectorAll(".price-offer, .price-was").forEach((el) => el.remove());
}

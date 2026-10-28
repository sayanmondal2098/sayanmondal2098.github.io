const citationStatus = document.getElementById("citation-status");
let toastTimer;

const showCitationToast = (message, type = "success") => {
  if (!citationStatus) return;
  window.clearTimeout(toastTimer);
  citationStatus.textContent = message;
  citationStatus.dataset.type = type;
  citationStatus.classList.add("is-visible");
  toastTimer = window.setTimeout(() => {
    citationStatus.classList.remove("is-visible");
  }, 3200);
};

const copyText = async (text) => {
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(text);
      return;
    } catch {
      // Some browsers deny clipboard access even on a secure origin.
    }
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();
  try {
    if (!document.execCommand("copy")) {
      throw new Error("Clipboard access was denied.");
    }
  } finally {
    textarea.remove();
  }
};

document.querySelectorAll("[data-copy-citation]").forEach((button) => {
  button.addEventListener("click", async () => {
    // The adjacent download is the source of truth for this work's BibTeX.
    const citationLink = button
      .closest(".citation-actions, .profile-actions")
      ?.querySelector('a[download][href$=".bib"]');
    const originalLabel = button.textContent;
    button.disabled = true;
    button.setAttribute("aria-busy", "true");

    try {
      if (!citationLink) throw new Error("No BibTeX download is linked.");
      const response = await fetch(citationLink.href);
      if (!response.ok) throw new Error("Citation file could not be loaded.");
      await copyText((await response.text()).trim());
      button.textContent = "Copied ✓";
      showCitationToast(`${button.dataset.title} BibTeX copied to clipboard.`);
    } catch (error) {
      button.textContent = "Copy failed";
      showCitationToast(
        `Could not copy ${button.dataset.title}. Use the BibTeX download instead.`,
        "error",
      );
    } finally {
      button.removeAttribute("aria-busy");
      window.setTimeout(() => {
        button.textContent = originalLabel;
        button.disabled = false;
      }, 2200);
    }
  });
});

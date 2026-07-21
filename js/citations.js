const citationFiles = {
  cairn: "../citations/mondal2026cairn.bib",
  entrourl: "../citations/gayen2026entrourl.bib",
  railway: "../citations/banerjee2020railway.bib",
  dimensionality: "../citations/chakraborty2020dimensionality.bib",
  streetlight: "../citations/mondal2017streetlight.bib",
};

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
    await navigator.clipboard.writeText(text);
    return;
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  textarea.remove();
};

document.querySelectorAll("[data-copy-citation]").forEach((button) => {
  button.addEventListener("click", async () => {
    const citationId = button.dataset.copyCitation;
    const citationPath = citationFiles[citationId];
    const originalLabel = button.textContent;

    try {
      const response = await fetch(citationPath);
      if (!response.ok) throw new Error("Citation file could not be loaded.");
      await copyText((await response.text()).trim());
      button.textContent = "Copied ✓";
      showCitationToast(`${button.dataset.title} BibTeX copied to clipboard.`);
      window.setTimeout(() => {
        button.textContent = originalLabel;
      }, 2200);
    } catch (error) {
      button.textContent = "Copy failed";
      showCitationToast(
        `Could not copy ${button.dataset.title}. Use the BibTeX download instead.`,
        "error",
      );
      window.setTimeout(() => {
        button.textContent = originalLabel;
      }, 2200);
    }
  });
});

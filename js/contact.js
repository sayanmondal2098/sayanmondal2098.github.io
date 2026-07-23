const contactForm = document.getElementById("contact-form");
const contactStatus = document.getElementById("contact-form-status");

if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(contactForm);
    const name = String(formData.get("name") || "").trim();
    const email = String(formData.get("email") || "").trim();
    const topic = String(formData.get("topic") || "").trim();
    const message = String(formData.get("message") || "").trim();

    const subject = `Professional enquiry: ${topic || "Contact"}`;
    const body = [
      `Name: ${name}`,
      `Email: ${email}`,
      `Topic: ${topic}`,
      "",
      message,
    ].join("\n");

    window.location.href = `mailto:sayanmondal2098@gmail.com?subject=${encodeURIComponent(
      subject,
    )}&body=${encodeURIComponent(body)}`;

    if (contactStatus) {
      contactStatus.textContent =
        "Your email app should open now. If it does not, email sayanmondal2098@gmail.com directly.";
    }
  });
}

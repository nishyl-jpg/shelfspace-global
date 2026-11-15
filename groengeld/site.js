/* ============ EDIT HERE: details shared by every Groengeld page ============ */
const GG = {
  whatsapp: '27000000000',   // your number, country code first, no + or spaces
  email: 'orders@groengeld.co.za',
  minOrder: 350              // minimum order per delivery, in rand
};
/* ========================================================================== */

// Turns every element with data-wa="message text" into a WhatsApp link with that message ready to send.
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-wa]').forEach(function (a) {
    a.href = 'https://wa.me/' + GG.whatsapp + '?text=' + encodeURIComponent(a.dataset.wa);
    a.target = '_blank'; a.rel = 'noopener';
  });
  document.querySelectorAll('[data-email]').forEach(function (a) { a.textContent = GG.email; a.href = 'mailto:' + GG.email; });
  document.querySelectorAll('[data-min]').forEach(function (e) { e.textContent = 'R' + GG.minOrder; });
});

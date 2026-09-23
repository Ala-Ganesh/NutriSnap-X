/**
 * NutriSnap-X — Main Application JavaScript
 * Sidebar toggle, auto-dismiss alerts, misc helpers
 */

document.addEventListener('DOMContentLoaded', function () {

  // ── Sidebar Toggle ──────────────────────────────────────────────
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar       = document.getElementById('sidebar');
  const mainWrapper   = document.getElementById('mainWrapper');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('open');
      // On wider screens, collapse/expand with margin
      if (window.innerWidth > 900) {
        const isCollapsed = sidebar.style.transform === 'translateX(-100%)';
        if (isCollapsed) {
          sidebar.style.transform = '';
          mainWrapper.style.marginLeft = '';
        } else {
          sidebar.style.transform = 'translateX(-100%)';
          mainWrapper.style.marginLeft = '0';
        }
      }
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function (e) {
      if (window.innerWidth <= 900) {
        if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
          sidebar.classList.remove('open');
        }
      }
    });
  }

  // ── Auto-Dismiss Flash Alerts ───────────────────────────────────
  const alerts = document.querySelectorAll('.flash-toast');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.5s';
      alert.style.opacity    = '0';
      setTimeout(function () { alert.remove(); }, 500);
    }, 5000);
  });

  // ── Active Nav Highlight ────────────────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar-nav .nav-link').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ── Smooth Progress Bars (trigger animation) ────────────────────
  document.querySelectorAll('.macro-fill, .score-fill').forEach(function (bar) {
    const target = bar.style.width;
    bar.style.width = '0%';
    setTimeout(function () { bar.style.width = target; }, 100);
  });

  // ── Tooltip init (Bootstrap) ────────────────────────────────────
  var tooltipEls = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipEls.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

});

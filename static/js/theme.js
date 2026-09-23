/**
 * NutriSnap-X — Theme System
 * Light / Dark / System mode saved in localStorage
 */

(function () {
  const STORAGE_KEY = 'nutrisnap-theme';

  function getPreferred() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored && ['light', 'dark', 'system'].includes(stored)) return stored;
    return 'system';
  }

  function resolveTheme(pref) {
    if (pref === 'system') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return pref;
  }

  window.applyTheme = function (pref) {
    const theme = resolveTheme(pref);
    document.documentElement.setAttribute('data-theme', theme);

    const icon = document.getElementById('themeIcon');
    if (icon) {
      icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
    }
  };

  // Apply on load immediately (before paint)
  applyTheme(getPreferred());

  // Toggle button handler (attached after DOM ready)
  document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('themeToggle');
    if (btn) {
      btn.addEventListener('click', function () {
        const current = localStorage.getItem(STORAGE_KEY) || 'system';
        const resolved = resolveTheme(current);
        const next = resolved === 'dark' ? 'light' : 'dark';
        localStorage.setItem(STORAGE_KEY, next);
        applyTheme(next);
      });
    }

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
      if (getPreferred() === 'system') applyTheme('system');
    });
  });
})();

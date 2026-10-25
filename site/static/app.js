/* ============================================================================
   app.js - the whole of the site's JavaScript.

   Four small jobs: stick the nav, open the mobile menu, reveal sections as they
   scroll in, and copy the email address. No framework, no build step, nothing
   that can break in three years.

   Everything degrades: with JavaScript off you get a working, readable page.
   ========================================================================== */

(function () {
  'use strict';

  var reduceMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------- sticky nav */

  var nav = document.querySelector('.nav');
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('is-stuck', window.scrollY > 12);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* --------------------------------------------------------- mobile menu */

  var toggle = document.querySelector('.nav__toggle');
  var links = document.querySelector('.nav__links');

  if (toggle && links) {
    var setOpen = function (open) {
      links.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    };

    toggle.addEventListener('click', function () {
      setOpen(!links.classList.contains('is-open'));
    });

    // Any navigation closes it, including the hash links inside the panel.
    links.addEventListener('click', function (event) {
      if (event.target.tagName === 'A') { setOpen(false); }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') { setOpen(false); }
    });

    document.addEventListener('click', function (event) {
      if (!links.classList.contains('is-open')) { return; }
      if (links.contains(event.target) || toggle.contains(event.target)) { return; }
      setOpen(false);
    });
  }

  /* ------------------------------------------------------ reveal on scroll */

  var revealables = document.querySelectorAll('.reveal');

  if (reduceMotion || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(revealables, function (el) { el.classList.add('is-in'); });
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        entry.target.classList.add('is-in');
        observer.unobserve(entry.target);   // reveal once, never re-hide
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });

    Array.prototype.forEach.call(revealables, function (el) { observer.observe(el); });
  }

  /* -------------------------------------------------- active nav section */

  var sections = Array.prototype.slice.call(document.querySelectorAll('section[id]'));
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav__links a[href^="#"]'));

  if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        var id = entry.target.getAttribute('id');
        navLinks.forEach(function (link) {
          link.classList.toggle('is-active', link.getAttribute('href') === '#' + id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });

    sections.forEach(function (section) { spy.observe(section); });
  }

  /* ---------------------------------------------------------- copy email */

  var copyButtons = document.querySelectorAll('[data-copy]');

  Array.prototype.forEach.call(copyButtons, function (button) {
    var original = button.textContent;

    button.addEventListener('click', function () {
      var value = button.getAttribute('data-copy');
      var done = function () {
        button.textContent = 'copied';
        button.classList.add('is-done');
        window.setTimeout(function () {
          button.textContent = original;
          button.classList.remove('is-done');
        }, 1600);
      };

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(value).then(done, function () { /* ignore */ });
        return;
      }

      // Fallback for older browsers and non-secure contexts.
      var field = document.createElement('textarea');
      field.value = value;
      field.setAttribute('readonly', '');
      field.style.position = 'fixed';
      field.style.opacity = '0';
      document.body.appendChild(field);
      field.select();
      try { document.execCommand('copy'); done(); } catch (error) { /* ignore */ }
      document.body.removeChild(field);
    });
  });

  /* ------------------------------------------------------------ the year */

  var year = document.querySelector('[data-year]');
  if (year) { year.textContent = String(new Date().getFullYear()); }
})();

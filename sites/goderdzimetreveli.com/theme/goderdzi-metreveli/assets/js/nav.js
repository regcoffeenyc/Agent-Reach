/**
 * Progressive enhancement only. Everything below works without JS:
 * the menu is a plain list, submenus open on hover/focus via CSS.
 * This adds the mobile toggle and keyboard-accessible dropdowns.
 */
(function () {
	'use strict';

	var toggle = document.querySelector('.gm-navtoggle');
	var nav = document.getElementById('gm-primary-nav');

	if (toggle && nav) {
		toggle.addEventListener('click', function () {
			var open = toggle.getAttribute('aria-expanded') === 'true';
			toggle.setAttribute('aria-expanded', String(!open));
			nav.classList.toggle('is-open', !open);
			document.body.classList.toggle('gm-nav-open', !open);
		});

		document.addEventListener('keydown', function (e) {
			if (e.key === 'Escape' && nav.classList.contains('is-open')) {
				toggle.setAttribute('aria-expanded', 'false');
				nav.classList.remove('is-open');
				document.body.classList.remove('gm-nav-open');
				toggle.focus();
			}
		});
	}

	// Turn parent items into real disclosure buttons for keyboard and touch.
	var parents = nav ? nav.querySelectorAll('.menu-item-has-children') : [];
	Array.prototype.forEach.call(parents, function (item) {
		var link = item.querySelector('a');
		var sub = item.querySelector('.sub-menu');
		if (!link || !sub) {
			return;
		}

		var btn = document.createElement('button');
		btn.type = 'button';
		btn.className = 'gm-submenu-toggle';
		btn.setAttribute('aria-expanded', 'false');
		btn.innerHTML = '<span class="screen-reader-text">' + link.textContent.trim() + '</span>';
		link.parentNode.insertBefore(btn, link.nextSibling);

		btn.addEventListener('click', function () {
			var open = btn.getAttribute('aria-expanded') === 'true';
			btn.setAttribute('aria-expanded', String(!open));
			item.classList.toggle('is-open', !open);
		});

		item.addEventListener('focusout', function (e) {
			if (!item.contains(e.relatedTarget)) {
				btn.setAttribute('aria-expanded', 'false');
				item.classList.remove('is-open');
			}
		});
	});
}());

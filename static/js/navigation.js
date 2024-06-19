// Careers meganav variables
const nav = document.querySelector(".js-show-nav");
const dropdownWindow = document.querySelector(".dropdown-window");
const overlay = document.querySelector(".p-navigation__overlay");
const navDropdowns = [].slice.call(
  document.querySelectorAll(".dropdown-toggle")
);

function toggleDropdown(toggle, open) {
  var parentElement = toggle.parentNode;
  var dropdown = document.getElementById(toggle.getAttribute("aria-controls"));
  dropdown.setAttribute("aria-hidden", !open);
  closeAllMeganavs();

  if (open) {
    parentElement.classList.add("is-active");
    if (overlay) {
      overlay.classList.add("is-applied");
    }
  } else {
    parentElement.classList.remove("is-active");
    if (overlay) {
      overlay.classList.remove("is-applied");
    }
  }
}

function closeAllDropdowns(toggles) {
  toggles.forEach(function (toggle) {
    toggleDropdown(toggle, false);
  });
}

function handleClickOutside(toggles, containerClass) {
  document.addEventListener("click", function (event) {
    var target = event.target;
    // PRevent this function from overriding meganav menus' functionality
    var meganavDropdowns =
      target.parentElement.classList.contains("dropdown-toggle");

    if (target.closest && !meganavDropdowns) {
      if (!target.closest(containerClass)) {
        closeAllDropdowns(toggles);
        // closeAllMeganavs();
        if (overlay) {
          overlay.classList.remove("is-applied");
        }
      }
    }
  });
}

function initNavDropdowns(containerClass) {
  const toggles = [].slice.call(
    document.querySelectorAll(containerClass + " [aria-controls]")
  );
  handleClickOutside(toggles, containerClass);

  toggles.forEach(function (toggle) {
    toggle.addEventListener("click", function (e) {
      e.preventDefault();

      const shouldOpen = !toggle.parentNode.classList.contains("is-active");
      closeAllDropdowns(toggles);
      toggleDropdown(toggle, shouldOpen);
      toggleDropdownOnEsc(toggles);
    });
  });
}

function initDropdowItems(itemClass) {
  if (window.location.pathname != "/") {
    var items = [].slice.call(document.querySelectorAll(itemClass));
    items.forEach(item => {
      if (item.pathname && item.pathname === window.location.pathname) {
        item.classList.add("is-selected");
      } else {
        item.classList.remove("is-selected");
      }
    });
  }
}

function toggleDropdownOnEsc(toggles) {
  document.addEventListener("keydown", function (e) {
    if (e.code === "Escape") {
      closeAllDropdowns(toggles);
      closeAllMeganavs();
    }
  });
}

initNavDropdowns(".p-navigation__item--dropdown-toggle");
initDropdowItems(".p-navigation__dropdown-item");

// Init GA tracking
addGANavEvents("#products-nav", "jp.ubuntu.com-nav-products");
addGANavEvents("#solutions-nav", "jp.ubuntu.com-nav-solutions");
addGANavEvents("#download-nav", "jp.ubuntu.com-nav-download");
addGANavEvents("#blog-nav", "jp.ubuntu.com-nav-blog");
addGANavEvents("#contact-nav", "jp.ubuntu.com-nav-contact");

function addGANavEvents(target, category) {
  var t = document.querySelector(target);
  if (t) {
    t.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        // eslint-disable-next-line no-undef
        dataLayer.push({
          event: "GAEvent",
          eventCategory: category,
          eventAction: `from:${origin} to:${a.href}`,
          eventLabel: a.text,
          eventValue: undefined,
        });
      });
    });
  }
}

addGAContentEvents("#main-content");

function addGAContentEvents(target) {
  var t = document.querySelector(target);
  if (t) {
    t.querySelectorAll("a").forEach(function (a) {
      var category;
      if (a.className.includes("p-button--positive")) {
        category = "jp.ubuntu.com-content-cta-0";
      } else if (a.className.includes("p-button")) {
        category = "jp.ubuntu.com-content-cta-1";
      } else {
        category = "jp.ubuntu.com-content-link";
      }
      if (!a.href.startsWith("#")) {
        a.addEventListener("click", function () {
          // eslint-disable-next-line no-undef
          dataLayer.push({
            event: "GAEvent",
            eventCategory: category,
            eventAction: `from:${origin} to:${a.href}`,
            eventLabel: a.text,
            eventValue: undefined,
          });
        });
      }
    });
  }
}

// Careers navigation
if (nav) {
  nav.classList.remove("u-hide");
}

/**
 * Close rest of navigation (override standard functionality)
 * if in the future we change rest of nav into meganavs
 * remove this function
 */
function closeAllSimpleNavigation() {
  const containers = document.querySelectorAll(
    ".p-navigation__item--dropdown-toggle"
  );
  containers.forEach(item => {
    item.classList.remove("is-active");
    const dropdown = item.querySelector(".p-navigation__dropdown");
    dropdown.setAttribute("aria-hidden", "true");
    if (overlay) {
      overlay.classList.remove("is-applied");
    }
  });
}

/**
 * Close all meganavs
 */
function closeAllMeganavs() {
  navDropdowns.forEach(item => {
    if (item.classList.contains("is-active")) {
      item.classList.remove("is-active");
      dropdownWindow.classList.add("u-animation--slide-dropdown");
      if (overlay) {
        overlay.classList.remove("is-applied");
      }
    }
  });
}

// This is in place to extend future c.com meganavs
navDropdowns.forEach(function (dropdown) {
  dropdown.addEventListener("click", function (event) {
    event.preventDefault();

    var clickedDropdown = this;

    dropdownWindow.classList.remove("u-animation--slide-dropdown");
    if (overlay && overlay.classList.contains("is-applied")) {
      overlay.classList.remove("is-applied");
    }

    navDropdowns.forEach(function (dropdown) {
      if (dropdown === clickedDropdown) {
        if (dropdown.classList.contains("is-active")) {
          closeMenu(dropdown);
        } else {
          closeAllSimpleNavigation();
          dropdown.classList.add("is-active");
          if (overlay) {
            overlay.classList.add("is-applied");
          }
        }
      } else {
        dropdown.classList.remove("is-active");
        overlay.classList.remove("is-applied");
      }
    });
  });
});

if (overlay) {
  overlay.addEventListener("click", () => {
    navDropdowns.forEach(dropdown => {
      if (dropdown.classList.contains("is-active")) {
        closeMenu(dropdown);
      }
    });
  });
}

function closeMenu(dropdown) {
  dropdown.classList.remove("is-active");
  dropdownWindow.classList.add("u-animation--slide-dropdown");
  if (overlay) {
    overlay.classList.remove("is-applied");
  }
}

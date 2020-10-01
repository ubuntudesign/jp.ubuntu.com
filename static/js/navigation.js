var origin = window.location.href;

addGANavEvents("#canonical-products", "jp.ubuntu.com-nav-0-products");
addGANavEvents("#canonical-login", "jp.ubuntu.com-nav-0-login");
addGANavEvents("#navigation", "jp.ubuntu.com-nav-1");
addGANavEvents(".p-navigation--secondary", "jp.ubuntu.com-nav-2");
addGANavEvents(".p-contextual-footer", "jp.ubuntu.com-footer-contextual");
addGANavEvents(".p-footer__nav", "jp.ubuntu.com-nav-footer-0");
addGANavEvents(".p-footer--secondary", "jp.ubuntu.com-nav-footer-1");

function addGANavEvents(target, category) {
  var t = document.querySelector(target);
  if (t) {
    [].slice.call(t.querySelectorAll("a")).forEach(function (a) {
      a.addEventListener("click", function () {
        dataLayer.push({
          event: "GAEvent",
          eventCategory: category,
          eventAction: "from:" + origin + " to:" + a.href,
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
    [].slice.call(t.querySelectorAll("a")).forEach(function (a) {
      let category;
      if (a.classList.contains("p-button--positive")) {
        category = "jp.ubuntu.com-content-cta-0";
      } else if (a.classList.contains("p-button")) {
        category = "jp.ubuntu.com-content-cta-1";
      } else {
        category = "jp.ubuntu.com-content-link";
      }
      if (!a.href.startsWith("#")) {
        a.addEventListener("click", function () {
          dataLayer.push({
            event: "GAEvent",
            eventCategory: category,
            eventAction: "from:" + origin + " to:" + a.href,
            eventLabel: a.text,
            eventValue: undefined,
          });
        });
      }
    });
  }
}

addGAImpressionEvents(".js-takeover", "takeover");

function addGAImpressionEvents(target, category) {
  var t = [].slice.call(document.querySelectorAll(target));
  if (t) {
    t.forEach(function (section) {
      if (!section.classList.contains("u-hide")) {
        var a = section.querySelector("a");
        dataLayer.push({
          event: "NonInteractiveGAEvent",
          eventCategory: "jp.ubuntu.com-impression-" + category,
          eventAction: "from:" + origin + " to:" + a.href,
          eventLabel: a.text,
          eventValue: undefined,
        });
      }
    });
  }
}

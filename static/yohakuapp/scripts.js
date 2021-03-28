const about_overlay = document.getElementById("about");
const open_about = document.getElementById("open_about");
const close_about = document.getElementById("close_about");

const form_overlay = document.getElementById("form");
const open_form = document.getElementById("open_form");
const close_form = document.getElementById("close_form");

const search_icon = document.getElementById("search_icon");
const search_field = document.getElementById("search");
const clear_results = document.getElementById("clear_results");

let clickedElement = null;

open_about.addEventListener("click", () => {
  about_overlay.classList.remove("hidden");
});
close_about.addEventListener("click", () => {
  about_overlay.classList.add("hidden");
});

open_form.addEventListener("click", () => {
  form_overlay.classList.remove("hidden");
});
close_form.addEventListener("click", () => {
  form_overlay.classList.add("hidden");
});

search_field.addEventListener("focus", () => {
  search_icon.classList.add("rotate-45");
  if (clear_results) {
    clear_results.classList.remove("sr-only");
    clear_results.classList.add("translate-y-3.5");
  }
});

search_field.addEventListener("blur", (e) => {
  search_icon.classList.remove("rotate-45");
  if (clear_results && clickedElement != clear_results) {
    // hide clear results button only when a different element is clicked to lose focus
    clear_results.classList.remove("translate-y-3.5");
    clear_results.classList.add("sr-only");
  }
});

document.addEventListener("mousedown", (e) => {
  clickedElement = e.target;
});

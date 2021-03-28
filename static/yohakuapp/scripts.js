const about_overlay = document.getElementById("about");
const open_about = document.getElementById("open_about");
const close_about = document.getElementById("close_about");

const form_overlay = document.getElementById("form");
const open_form = document.getElementById("open_form");
const close_form = document.getElementById("close_form");

const search_icon = document.getElementById("search_icon");
const search_field = document.getElementById("search");

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
});
search_field.addEventListener("blur", () => {
  search_icon.classList.remove("rotate-45");
});

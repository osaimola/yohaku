const colors = require("tailwindcss/colors");

module.exports = {
  purge: ["../yohakuapp/templates/**/*.html"],
  // purge: {
  //   enabled: true,
  //   content: ["../yohakuapp/templates/**/*.html"],
  // },
  darkMode: false, // or 'media' or 'class'
  theme: {
    colors: {
      ...colors,
    },
    extend: {
      colors: {
        "brand-blue": "#469CFF",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [require("@jinsung.lim/tailwindcss-filters")],
};

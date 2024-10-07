/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../templates/**/*.html",
    "../../modules/**/**/*.html",
    "./static/src/**/*.js",
    "./node_modules/flowbite-datepicker/**/*.js",
    "./node_modules/flowbite-datepicker/**/*.css",
    "./node_modules/flowbite/**/*.js",
    "./node_modules/flowbite/**/*.css",
  ],
  daisyui: {
    themes:["dark"],
  },
  plugins: [require("daisyui")],
};

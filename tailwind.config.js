/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js",
    './node_modules/flowbite/**/*.js',
    
    
  ],
  theme: {
    extend: {
      colors: {
        'smoky': '#f2f3f5',
        'white-2': '#fdfdfd',
        'white-3': '#EDF2F7',
      },
      spacing: {
        '1050px': '1050px',
        '1460px': '1460px',
        '500px': '500px',
      },
    }
    },
  plugins: [
    require('flowbite/plugin')
  ]
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html", "./public/*.html"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#0F172A",
        secondary: "#3B82F6",
        accent: "#F43F5E",
        "background-light": "#F1F5F9",
        "background-dark": "#0B1120",
        "surface-light": "#FFFFFF",
        "surface-dark": "#1E293B",
      },
      fontFamily: {
        display: ["Inter", "sans-serif"],
        body: ["Inter", "sans-serif"],
      },
      borderRadius: {
        DEFAULT: "0.5rem",
        'xl': '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem',
        '4xl': '2.5rem',
      },
      boxShadow: {
        'soft': '0 10px 40px -10px rgba(0,0,0,0.08)',
        'glow': '0 0 20px rgba(59, 130, 246, 0.5)',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}

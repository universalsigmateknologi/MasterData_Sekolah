/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js,css}",
    "./**/templates/**/*.{html,js,css}",
  ],
  theme: {
    extend: {
          fontFamily: {
            'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
          },
          colors: {
            'surface': '#fafafa',
            'surface-alt': '#f5f5f5',
            'border-light': '#ebebeb',
          },
          animation: {
            'fade-in': 'fadeIn 0.3s ease-out',
            'slide-up': 'slideUp 0.35s ease-out',
            'slide-down': 'slideDown 0.25s ease-out',
            'scale-in': 'scaleIn 0.2s ease-out',
            'pulse-soft': 'pulseSoft 2s infinite',
          },
          keyframes: {
            fadeIn: { '0%': { opacity: '0' }, '100%': { opacity: '1' } },
            slideUp: { '0%': { opacity: '0', transform: 'translateY(12px)' }, '100%': { opacity: '1', transform: 'translateY(0)' } },
            slideDown: { '0%': { opacity: '0', transform: 'translateY(-8px)' }, '100%': { opacity: '1', transform: 'translateY(0)' } },
            scaleIn: { '0%': { opacity: '0', transform: 'scale(0.95)' }, '100%': { opacity: '1', transform: 'scale(1)' } },
            pulseSoft: { '0%, 100%': { opacity: '1' }, '50%': { opacity: '0.6' } },
          },
        },
  },
  plugins: [],
}


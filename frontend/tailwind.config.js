/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // unRAID theme colors
        'unraid': {
          'bg': '#1c1b1b',
          'bg-light': '#2a2a2a',
          'bg-lighter': '#3a3a3a',
          'orange': '#ff8c2f',
          'orange-dark': '#e67a1f',
          'green': '#4caf50',
          'red': '#f44336',
          'yellow': '#ffeb3b',
          'blue': '#2196f3',
          'gray': '#9e9e9e',
          'text': '#e0e0e0',
          'text-muted': '#9e9e9e',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}

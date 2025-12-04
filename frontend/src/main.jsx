import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// Import Tailwind CSS with proper directives
import './index.css'
import App from './App.jsx'
console.log('frontend: main.jsx loaded')

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

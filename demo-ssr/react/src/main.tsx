// import { StrictMode } from 'react'
import { createInertiaApp } from '@inertiajs/react'
import { hydraateRoot } from 'react-dom/client'


createInertiaApp({
  id: 'root',
  resolve: name => {
    const pages = import.meta.glob('./Pages/**/*.tsx', { eager: true })
    return pages[`./Pages/${name}.tsx`]
  },
  setup({ el, App, props }) {
    hydraateRoot(el).render(<App {...props} />)
  },
})

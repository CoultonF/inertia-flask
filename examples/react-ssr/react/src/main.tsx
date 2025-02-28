// import { StrictMode } from 'react'
import { createInertiaApp } from '@inertiajs/react'
import { createRoot, hydrateRoot } from 'react-dom/client'


createInertiaApp({
  resolve: name => {
    const pages = import.meta.glob('./Pages/**/*.tsx', { eager: true })
    return pages[`./Pages/${name}.tsx`]
  },
  setup({ el, App, props }) {
    if (el.hasChildNodes()) {
      // If the element has child nodes, it means the HTML was server-rendered
      console.log("hydrating")
      hydrateRoot(el, <App {...props} />);
    } else {
      console.log("rendering")
      // If the element does not have child nodes, it means it's client-side rendering
      createRoot(el).render(<App {...props} />);
    }
},
})

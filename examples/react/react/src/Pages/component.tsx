import { Deferred, usePage } from '@inertiajs/react'
import { usePoll } from '@inertiajs/react'
import { router } from '@inertiajs/react'

function Component(props){
  
  // usePoll(2000, {only:['value']})

  return (
  <div>Hello from inertia!
    <p>value is {props.value}</p>
<Deferred data="defer" fallback={<div>Loading...</div>}>
    <DeferComponent />
</Deferred>
<button type='button' onClick={()=>{
router.visit(window.location.href, {
  only: ['defer'],
})
}}>revisit</button>
<button type='button' onClick={()=>{
router.visit(window.location.href, {
  only: ['other'],
})
}}>
  Next number
</button>
<button type='button' onClick={()=>{
router.visit(window.location.href, {
  reset: ['other'],
})
}}>
  Reset Numbers
</button>
<Deferred data="other" fallback={<div>Loading...</div>}>
{(props?.other??[]).map((v,i) => <p key={i}>{v}</p>)}
</Deferred>
  </div>
  )
}


const DeferComponent = () => {
  const { defer } = usePage().props
  console.log({defer})
  return (
        <p>Done</p>
)
}

export default Component;
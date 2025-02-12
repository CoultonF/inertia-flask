import { Deferred, usePage } from '@inertiajs/react'
import { usePoll } from '@inertiajs/react'

function Component(props){
  
  usePoll(2000, {only:['value']})
  return (
  <div>Hello from inertia!
    <p>value is {props.value}</p>
<Deferred data="defer" fallback={<div>Loading...</div>}>
    <DeferComponent />
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
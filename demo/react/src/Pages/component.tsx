import { Deferred, usePage } from '@inertiajs/react'

function Component(props){
  console.log(props)
  return (
  <div>Hello from inertia!
    <p>value is {props.value}</p>
    <DeferComponent />
  </div>
  )
}


const DeferComponent = () => {
const { defer } = usePage().props
  return (
    <Deferred data="defer" fallback={<div>Loading...</div>}>
        <p>Done: {defer}</p>
    </Deferred>
)
}

export default Component;
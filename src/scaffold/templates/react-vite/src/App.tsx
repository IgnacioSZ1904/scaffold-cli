import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <main>
      <h1>$project_name</h1>
      <button onClick={() => setCount((c) => c + 1)}>Clics: {count}</button>
    </main>
  )
}

export default App

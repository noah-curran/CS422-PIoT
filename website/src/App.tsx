import React, { useEffect } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = React.useState('');
  const [response, setResponse] = React.useState('');
  const [button, setButton] = React.useState(false)

  useEffect(() => {
    let handle = setInterval(() => {
      getLogs()
    }, 5000)

    return function cleanup() {
      clearInterval(handle)
    }
  }, [button])

  function handleButton( ) {
    setButton(!button);
    getLogs()
  }

  function getLogs() {
    console.log(url)
    fetch(url, { method: 'GET', mode: 'cors' }).then(response => response.text()).then(responseText => {
      let output = responseText.split('\n').filter(item => item.includes('password for pi'))
      setResponse(output.join('\n'))
    });
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>CS 422 Piot</h1>
      </header>
      <section style={{ display: 'flex' }}>
        <input id="url-input" className='App-input' type='text' placeholder={'enter the url of honeypot'} onChange={(event) => setUrl(event.target.value)}></input>
        <button className='App-button' onClick={e => handleButton()}>get statistics</button>
      </section>
      <section>
        <pre>{response}</pre>
      </section>
    </div>
  );
}

export default App;

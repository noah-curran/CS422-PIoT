import React, { useEffect } from 'react';
import './App.css';

type Props = {
  value: number;
  valueColor?: string;
  description: string;
}

function DataCard({ value, valueColor, description }: Props) {
  return (
    <div className='App-card'>
      <div style={{ fontSize: '2em', textAlign: 'center' }}>
        <h1 style={{ color: valueColor!= undefined ? valueColor : '#FF2000', fontWeight: 800, fontSize: '3em', marginBottom: 0 }}>{value}</h1>
        <h1>{description}</h1>
      </div>
    </div>
  );
}

let addresses: Set<string> = new Set();

function App() {
  const [url, setUrl] = React.useState('');
  const [button, setButton] = React.useState(false)
  const [numberOfAcceptedLogins, setNumberOfAcceptedLogins] = React.useState(0);
  const [numberOfFailedLogins, setNumberOfFailedLogins] = React.useState(0);
  const [numberOfPasswordChangeAttempts, setNumberOfPasswordChangeAttempts] = React.useState(0);

  useEffect(() => {
    let handle = setInterval(() => {
      getLogs()
    }, 5000)

    return function cleanup() {
      clearInterval(handle)
    }
  }, [button])

  function handleButton() {
    setButton(!button);
    addresses.clear()
    getLogs()
  }

  function getLogs() {
    fetch(url, { method: 'GET', mode: 'cors' }).then(response => response.text()).then(responseText => {
      let acceptedPasswordAttempts = responseText.split('\n').filter(item => item.includes('Accepted password for pi'))
      setNumberOfAcceptedLogins(acceptedPasswordAttempts.length);

      let failedPasswordAttempts = responseText.split('\n').filter(item => item.includes('Failed password for pi'))
      setNumberOfFailedLogins(failedPasswordAttempts.length);

      let accessAttempts = responseText.split('\n').filter(item => item.includes('password for pi'))
      for (let lineInfo in accessAttempts) {
        let attackerAddress = new RegExp('((::[\d|\w]+:[\d|\w]+:[\d|\w]+:[\d|\w]+)|(\d+\.\d+\.\d+\.\d+))').exec(lineInfo)
        if (attackerAddress != null) {
          addresses.add(attackerAddress[0]);
        }
      }

      let passwordChangeAttempts = responseText.split('\n').filter(item => item.includes('password changed for pi'))
      setNumberOfPasswordChangeAttempts(passwordChangeAttempts.length);
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
      <section className='App-grid' style={{ marginTop: 64 }}>
        <DataCard value={numberOfFailedLogins} description={'successful access attempts from external users'} />
        <DataCard value={numberOfAcceptedLogins} description={'failed access attempts from external users'} />
        <DataCard value={addresses.size} description={'unique external users'} />
        <DataCard value={numberOfPasswordChangeAttempts} description={'password change attempts from external users'} />
      </section>
    </div>
  );
}

export default App;

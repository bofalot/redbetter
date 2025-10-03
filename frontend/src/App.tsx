import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [config, setConfig] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios.get('/api/config')
      .then(response => {
        setConfig(response.data);
      })
      .catch(error => {
        console.error('Error fetching config:', error);
        setError('Failed to fetch configuration. Make sure the backend is running.');
      });
  }, []);

  return (
    <div className="container mt-5">
      <h1>RedOpsManager</h1>
      <h2 className="mt-4">Configuration</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      {config ? (
        <table className="table table-bordered mt-3">
          <tbody>
            <tr>
              <th scope="row">Data Dirs</th>
              <td>{config.data_dirs?.join(', ')}</td>
            </tr>
            <tr>
              <th scope="row">Output Dir</th>
              <td>{config.output_dir}</td>
            </tr>
            <tr>
              <th scope="row">Torrent Dir</th>
              <td>{config.torrent_dir}</td>
            </tr>
            <tr>
              <th scope="row">Redacted API Key</th>
              <td>{config.redacted_api_key}</td>
            </tr>
            <tr>
              <th scope="row">Orpheus API Key</th>
              <td>{config.orpheus_api_key}</td>
            </tr>
            <tr>
              <th scope="row">qBittorrent</th>
              <td>
                {config.qbittorrent ? (
                  <pre>{JSON.stringify(config.qbittorrent, null, 2)}</pre>
                ) : 'Not configured'}
              </td>
            </tr>
          </tbody>
        </table>
      ) : (
        <p>Loading configuration...</p>
      )}
    </div>
  );
}

export default App;
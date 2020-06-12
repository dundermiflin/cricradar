import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import SearchPanel from './SearchPanel';

class App extends Component {
  constructor(props){
    super(props);
    this.state = {apiResponse: "Service is down :(" 
                  }
  }

  testAPI = () => {
    fetch("http://localhost:7000")
      .then(reponse => reponse.json())
      .then(response => {
        this.setState({apiResponse: response['msg']});
      }
        );
  }

  fetchStats = () => {
    fetch("http://localhost:7000",
    {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({id: '3600', format: 'test', aspect: 'Batting'})
    })
    .then(response => response.json())
    .then(response => {

      this.setState({
        captions: response["captions"],
        data: [{data:response["percentiles"], meta:{ color: 'red' }}],
        showChart: true
      });
    })
  }

  componentDidMount(){
    this.testAPI();
    // this.fetchStats();
    // console.log(this.state);
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>{this.state.apiResponse}</h2>
        </div>
        <SearchPanel/>
      </div>
    );
  }
}

export default App;

import React, { Component } from 'react';
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

  componentDidMount(){
    this.testAPI();
    // this.fetchStats();
    // console.log(this.state);
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h2>{this.state.apiResponse}</h2>
        </div>
        <SearchPanel/>
      </div>
    );
  }
}

export default App;

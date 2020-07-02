import React, { Component } from 'react';
import './App.css';
import SearchPanel from './SearchPanel';
import StatsPanel from './StatsPanel';
import {BrowserRouter as Router, Route, Switch, withRouter} from 'react-router-dom'

class App extends Component {
  constructor(props){
    super(props);
    this.state = {apiResponse: "Service is down :(" 
                  }
  }

  testAPI = () => {
    fetch("http://dundermiflin.pythonanywhere.com/test")
      .then(reponse => reponse.json())
      .then(response => {
        this.setState({apiResponse: response['msg']});
      }
        );
  }

  componentDidMount(){
    this.testAPI();
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h2>{this.state.apiResponse}</h2>
        </div>
        <Router>
          <Switch>
            <Route exact path="/" component={withRouter(SearchPanel)}/>
            <Route path="/stats/:pid" component={withRouter(StatsPanel)}/>
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;

import React, { Component } from 'react';
import { AwesomeButton } from 'react-awesome-button';
import "react-awesome-button/dist/styles.css";
import RadarChart from 'react-svg-radar-chart';
import 'react-svg-radar-chart/build/css/index.css';

class StatsPanel extends Component {
    constructor(props) {
      super(props);
      this.state = {captions: {},
                    data: {},
                    showChart: false,
                    error: false,
                    pid: this.props.match.params.pid,
                    name:'',
                    format: 'test',
                    aspect: 'Batting'
                    };
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
      this.fetchStats();
    }

    fetchStats = () => {
        fetch("/stats",
        {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({id: this.state.pid, format: this.state.format, aspect: this.state.aspect})
        })
        .then(response => {
          if (response.status >= 200 && response.status <= 299) {
            return response.json();
          } else {
            throw Error(response.statusText);
          }
        })
        .then(response => {
          this.setState({
            name: response['name'],
            captions: response["captions"],
            data: [{data:response["percentiles"], meta:{ color: 'red' }}],
            showChart: true,
            error: false
          });
        })
        .catch((error) => {
          this.setState({
            error: true
          });
        })
      }
  
    handleChange(event) {
        if(event.target.name !== 'pid'){
          this.fetchStats();
        }
        this.setState({
            [event.target.name]: event.target.value});
    }
  
    handleSubmit(event) {
      event.preventDefault();
      this.fetchStats()
    }
  
    render() {
        var radar = null;
        if (this.state.showChart === true){
          radar = <div>
                  <RadarChart
                    captions={this.state.captions}
                    data={this.state.data}
                    size={400}
                  />
                  <h2>{this.state.name}</h2>
                </div>
        }
        if (this.state.error === true){
          radar = <p>Error in fetching</p>
        }
      return (
        <div>
          <form onSubmit={this.handleSubmit}>
            <label>
              Format:
              <select name="format" value={this.state.format} onChange={this.handleChange}>
                <option value="test">Test</option>
                <option value="odi">ODI</option>
                <option value="t20i">T20I</option>
              </select>
            </label>
            <label>
              Aspect:
              <select name="aspect" value={this.state.aspect} onChange={this.handleChange}>
                <option value="Batting">Batting</option>
                <option value="Bowling">Bowling</option>
              </select>
            </label>
            <AwesomeButton type="submit" value="Submit">Fetch Stats</AwesomeButton>
          </form>
          <div>
              {radar}
          </div>
        </div>
      );
    }
  }

export default StatsPanel
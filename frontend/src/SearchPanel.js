import React, { Component } from 'react';
import { AwesomeButton } from 'react-awesome-button';
import "react-awesome-button/dist/styles.css";
import RadarChart from 'react-svg-radar-chart';
import 'react-svg-radar-chart/build/css/index.css';

class SearchPanel extends Component {
    constructor(props) {
      super(props);
      this.state = {captions: {},
                    data: {},
                    showChart: false,
                    pid: '3600',
                    format: 'test',
                    aspect: 'Batting'
                    };
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }

    fetchStats = () => {
        fetch("/",
        {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({id: this.state.pid, format: this.state.format, aspect: this.state.aspect})
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
  
    handleChange(event) {
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
          radar = <RadarChart
                  captions={this.state.captions}
                  data={this.state.data}
                  size={400}
                />
        }
      return (
        <div>
          <form onSubmit={this.handleSubmit}>
            <label>
              Player ID:
              <input type="text" name="pid" value={this.state.pid} onChange={this.handleChange} />
            </label>
            <label>
              Format:
              <input type="text" name="format" value={this.state.format} onChange={this.handleChange} />
            </label>
            <label>
              Aspect:
              <input type="text" name="aspect" value={this.state.aspect} onChange={this.handleChange} />
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

export default SearchPanel
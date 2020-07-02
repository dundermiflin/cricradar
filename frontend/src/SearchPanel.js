import React, { Component } from 'react';
import { AwesomeButton } from 'react-awesome-button';
import "react-awesome-button/dist/styles.css";
import 'react-svg-radar-chart/build/css/index.css';
import {BrowserRouter as Router, Link} from 'react-router-dom'

class SearchPanel extends Component {
    constructor(props) {
      super(props);
      this.state = {
        pattern:'',
        error:false,
        results: <p>Results here</p>,
        showSearch: false
      };
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }

    fetchSearch = () => {
        fetch("http://dundermiflin.pythonanywhere.com/search",
        {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({pattern: this.state.pattern, num: 10})
        })
        .then(response => {
          if (response.status >= 200 && response.status <= 299) {
            return response.json();
          } else {
            throw Error(response.statusText);
          }
        })
        .then(response => {
            var newLinks = []
            for(var res of response){
              newLinks.push(
                <div>
                    <Link to={`/stats/${res['id']}`}>{res['name']}</Link>
                </div>
                )
            }
            var result = <div>
                          {newLinks}
                          </div>
            this.setState({
              error: false,
              showSearch: true,
              results: result,
            });
          console.log(response);
        })
        .catch((error) => {
          this.setState({
            error: true,
            showSearch: false,
            results: <p>Error in fetching</p>
          });
        })
      }
  
    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value});
    }
  
    handleSubmit(event) {
      event.preventDefault();
      this.fetchSearch()
    }
  
    render() {
      return (
        <div>
          <form onSubmit={this.handleSubmit}>
            <label>
              Player name:
              <input type="text" name="pattern" value={this.state.pattern} onChange={this.handleChange} />
            </label>
            <AwesomeButton type="submit" value="Submit">Search</AwesomeButton>
          </form>
          <div>
              {this.state.results}
          </div>
        </div>
      );
    }
  }

export default SearchPanel
import React, { Component } from 'react';

class Card extends Component {
    constructor(props) {
        super(props);
        this.state = {
            color : 'white',
            name:props.name,
            pid:props.pid
        };
        this.onClick = this.onClick.bind(this);
    }
    onClick = () => {
       this.setState({ color: 'red' });
    }
    render () {
         return (
           <div onClick={this.onClick} style={{backgroundColor: this.state.color}}>
            {this.props.name}
          </div>
     );
    }
}

export default Card

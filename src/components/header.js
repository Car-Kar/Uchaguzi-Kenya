import React from 'react';
import {
Link
} from 'react-router-dom'


class Header extends React.Component{
  render() {
    return (
      <header>
        <nav className = 'navbar navbar-default navbar-expand-lg navbar-dark navbar-fixed-top' id = 'nav'>
        <a className = "navbar-brand" href="#">Jumuiya</a>
        <br />
          <div className = "collapse navbar-collapse" id = "myNavbar">
            <ul className = "nav navbar-nav ml-auto">
              <li><Link to = '/contributors'>Contributors</Link></li>
              <li><Link to = '/get-involved'>Get Involved</Link></li>
              <li><Link to = '/portal'>Portal</Link></li>
            </ul>
          </div>
        </nav>
      </header>
    )
  }
}

export default Header
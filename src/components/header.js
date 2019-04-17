import React from 'react';
import {
  Link
} from 'react-router-dom'


class Header extends React.Component{
  constructor(props){
    super(props);
    this.openPage = this.openPage.bind(this)
  }
  openPage(url){
    window.open(url, '_blank')
  }
  render() {
    return (
      <header>
      <p>Challenge Us</p>
      <br />
      <nav id = 'nav'>
      <ul>
        <li><Link to = '/all'>All</Link></li>
        <li><Link to = '/solved'>Solved</Link></li>
        <li><Link to = '/unsolved'>Unsolved</Link></li>
     </ul>
    </nav>
  </header>
  )
  }
}

export default Header
import React from 'react';
import Header from './header';
import Footer from './footer';
/* import Content from './content.js' */


class Main extends React.Component{ 
	render() {
		return (
		<div className = 'wrapper'>
			<div className = 'content'>
				<Header />
				{/* <Content /> */}
				<Footer />
			</div>
		</div>
		)
	}
}

export default Main
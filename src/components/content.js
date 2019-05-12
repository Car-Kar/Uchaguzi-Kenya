import React from 'react';
import { Route, Switch} from 'react-router-dom';
import Portal from './portal';
import Pitch from './pitch'

class Content extends React.Component {
	render() {
		return (
			<div className = 'router container-fluid'>
                <Switch>
                    {/* <Route exact path = '/login' render = {() => (cookies.get('accessToken') ? ( <UserChallenges />) :  (<Login />) )} />
                    <PrivateRoute exact path = '/' component = {UserChallenges}/>
                    <PrivateRoute path = '/all' component = {UserChallenges}/>
                    <PrivateRoute exact path = '/solution/:id' rcomponent = {Solution}/>
                    <PrivateRoute exact path = '/solved' component = {AllSolved}/>
                    <PrivateRoute exact path = '/unsolved' component = {Unsolved}/> */}
                    <Route exact path = '/portal' component = {Portal} />
                    <Route exact path = '/' component = { Pitch} />
                </Switch>
			</div>
			)
	}
	
}

export default Content
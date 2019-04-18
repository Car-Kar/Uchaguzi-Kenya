import React from 'react';

class Portal extends React.Component {
    constructor(props){
		super(props);
		this.state = {
		    requested: '',
		    success: false
        };
        this.handleChange = this.handleChange.bind(this);
	this.submitRequest = this.submitRequest.bind(this);
	this.sendRequest = this.sendRequest.bind(this);
    };

    submitRequest(event) {
	this.setState({requested: event.target.value});
	event.preventDefault();
	this.sendRequest(this.state.requested);
    }

    sendRequest(requested) {
	let url = "http://localhost:5000/portal/request/";
	let request = new Request(url, {
		method: 'POST',
		headers: new Headers({
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}),
		body:  JSON.stringify({
			'title' : requested
		})
	});
	fetch(request)
	    .then(response => {
		if (!response.ok) {
		    throw new Error("Could not make request: " + response.status);
		}
		this.setState({success: true});
		return  response.json()
	    })
	    .then(data => {
		console.log(data);
	    })
	    .catch(err => {
		this.setState({success: false});
		console.log("No such luck.")
	    }
	    )
      };

    handleChange(event) {
        this.setState({requested: event.target.value});
        console.log(this.state.requested);
    };

    render() {
        return (
            <div id = "portal" className = "text-center">
                <h1>Article Requests</h1> 
                <p>You can submit article/resource requests using the form below.</p>
                <p>Requests automatically create an issue on the project's GitHub for documentaion</p> 
                <p>This does not require any personal information!</p>
                <form className ="form-inline">
                    <div className ="input-group text-center input-group-lg">
                        <input id = "resource" type="text" className ="form-control" size="50" placeholder="Resource Request" required  value = {this.state.request} onChange={this.handleChange} />
                        <div className ="input-group-btn">
                            <button onClick = {this.submitRequest} type = "submit" className = "submit btn btn-primary btn-lg">Submit</button>
                        </div>
                    </div>
                </form>
                </div>
        )
    }
}

export default Portal;

## Contributing to Jumuiya

There are two different types of contributions to Jumuiya - technical and non-technical contributions.

### Technical Contributions.

---

The project is written entirely in Python 3 and intermediate knowledge of Python 3 is therefore required.  
The project also works heavily with the Facebook Messenger APIs which requires the ability or patience of reading through the API docs. The Messenger API documentation can be found [here](https://developers.facebook.com/docs/messenger-platform/).

To create a personal instance of the bot, there a few Facebook necessities required as the user entry point to the bot is a Facebook page. A web server instance is also required to communicate with the Facebook API for authentication and access to Facebook data and resources.

The following steps can be followed to get an instance of the bot:

1. Create a Facebook Page.  
The Facebook page will provide the identity and entry point of the bot. A Facebook page can be created [here](https://www.facebook.com/pages/create). A Community page is more suited for this purpose.

2. Create a Developers Account.  
A Facebook developers account will provide various tools for development agains the Facebook/Messenger APIs. A developer account can be created [here](https://developers.facebook.com/). A developer account is usually linked to your normal Facebook account.

3. Setting up a web server for webhooks.
A webhook is the interface through which the bot receives, processes, sends messages and generally interacts with the Messenger API. The webhook is also used for verification and should therefore be hosted publicly with HTTPS support. The server can be on Heroku, AWS, or using tunnel clients such as [ngrok](https://ngrok.com/). The original project uses a Heroku instance for the webhook. Using Heroku for the webserver is described here while using ngrok is described here.
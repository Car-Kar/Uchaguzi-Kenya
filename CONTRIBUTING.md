## Contributing to Jumuiya

There are two different types of contributions to Jumuiya - technical and non-technical contributions.

### Technical Contributions.
---

The project is written entirely in Python 3 and intermediate knowledge of Python 3 is therefore required.  
The project also works heavily with the Facebook Messenger APIs which requires the ability or patience of reading through the API docs. The Messenger API documentation can be found [here](https://developers.facebook.com/docs/messenger-platform/).

To create a personal instance of the bot, there a few Facebook necessities required as the user entry point to the bot is a Facebook page. A web server instance is also required to communicate with the Facebook API for authentication and access to Facebook data and resources.

The following steps can be followed to get an instance of the bot:

---

### Setting up your Development Environment.
This part requires that git, Python-3 and pip are already installed on your machine.

1. Clone the repository to your machine.   
`git clone git@github.com:wambu-i/Jumuiya.git`

2. Install the required Python packages.  
This can be done by setting up a virtual environment using the Python 3 built-in [virtual environment](https://docs.python.org/3/tutorial/venv.html) support or directly. A virtual environment is recommended to keep development dependencies from clashing.
To create a virtual environment, move into the project directory after cloning:  
`cd Jumuiya`  
and create the virtual environment:  
`python3 -m venv env`

3. Activate the environment.  
On Linux/Mac OS activate the environment: `source env/bin/activate`.
On Windows, the command is: `env\Scripts\activate.bat`.

4. Install the Python modules using the requirements file.  
`pip install -r requirements.txt`

After successful installation of the pip modules, your environment is mostly ready for development.

---

#### Connecting to Facebook


1. Create a Facebook Page.  
The Facebook page will provide the identity and entry point of the bot. A Facebook page can be created [here](https://www.facebook.com/pages/create). A Community page is more suited for this purpose.

2. Create a Developers Account.  
A Facebook developers account will provide various tools for development agains the Facebook/Messenger APIs. A developer account can be created [here](https://developers.facebook.com/). A developer account is usually linked to your normal Facebook account.

3. Setting up a web server for webhooks.
A webhook is the interface through which the bot receives, processes, sends messages and generally interacts with the Messenger API. The webhook is also used for verification and should therefore be hosted publicly with HTTPS support. The server can be on Heroku, AWS, or using tunnel clients such as [ngrok](https://ngrok.com/). The original project uses a Heroku instance for the webhook. Using Heroku for the webserver is described [here](#hosting-a-webserver-with-Heroku) while using ngrok is described here.

4. Creating a Facebook App and Connecting it to the Webhook.  
A Facebook App is the interface between the created webhook and the respective Facebook page. The App is responsible for generating authentication tokens and configuring settings for the Messenger bot. A Facebook App can be created on your developer page [here](https://developers.facebook.com/apps). The App set up can be done following the steps in the official documentation [here](https://developers.facebook.com/docs/messenger-platform/getting-started/app-setup).
The page access token generated and verify token in the guide can be configured as an environment variable (in UNIX environments) or passed as a command line argument in the running of the app. This will be described in the following sections.

5. Develop against a feature and submit a pull request.  
After the above successfull set up, you can now contribute by developing a feature or fixing a bug in the project. Features and bugs are usually listed in the [issues](https://github.com/wambu-i/Jumuiya/issues) pages of the project. After development you can submit a [pull](https://help.github.com/en/articles/about-pull-requests) request for review and merging of code.

You can also develop a feature not reported there and submit a pull request for review. Such features will be discussed and integrated in the bot if needed/approved.

---

#### Hosting a webserver with Heroku.
Heroku is a Platform as a Service (PaaS) that provides developers with services that can run cloud applications with little to no configuration requirements. Heroku has no storage capabilities by default and usually is used to only run instances of applications. Heroku has a free developer account which has limited number of hours in which the application can run. For testing and development purposes, the hours should suffice. To get started, create an account [here](https://signup.heroku.com/).   
At the dashboard after signing in, create a new personal app by giving it a name, and choosing a region for the app to run in.

Heroku can be used using their command line interface (CLI) which can be downloaded and configured from [here](https://devcenter.heroku.com/articles/heroku-cli). The article also describes logging into your Heroku account using the CLI and  connecting it to the app you created.

Heroku can also be used by connecting the created app to a GitHub repository and configuring automatic deployments when pushed on a specific branch. GitHub and Heroku integration is described in detail in [this](https://devcenter.heroku.com/articles/github-integration) Heroku article.

When using the Heroku CLI, login into your Heroku account and connect it to your created app:

`heroku login`

`heroku git:remote -a <heroku-app-name>`

Use the page access token generated from the Facebook App as an environment variable:


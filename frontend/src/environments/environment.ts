export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'spskelly.us', // the auth0 domain prefix
    audience: 'http://localhost:5000', // the audience set for the auth0 app
    clientId: '4VZgmO8D9NzovFgJrBn1e9DcBkA36h1Z', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
  }
};

// https://spskelly.us.auth0.com/authorize?audience=http://localhost:5000&response_type=token&client_id=4VZgmO8D9NzovFgJrBn1e9DcBkA36h1Z&redirect_uri=http://localhost:8100

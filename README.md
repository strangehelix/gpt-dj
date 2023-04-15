# GPT DJ
A ChatGPT plugin to create Spotify playlists based on user descriptions.

This repository serves as a simple example of how to develop a ChatGPT plugin and grant it access to a third-party service using OAuth (in this case, Spotify).

## Demo
https://matrix.dog/gptdj-demo-2.mp4

## How to set it up

### Set up a Spotify app
To provide ChatGPT with access to Spotify via OAuth, you have to set up a Spotify app in the Spotify Developer Dashboard and obtain a `client_id` and `client_secret`:

1. Go to Spotify developer's [dashboard] (https://developer.spotify.com/dashboard) and click "Create app".
2. Enter an `App name` and `App description`.
3. For the `Redirect URI`, put `https://chat.openai.com/aip/plugin-id-temporary-value/oauth/callback` as a temporary value.

Because you don't know your ChatGPT plugin ID yet, leave the value `plugin-id-temporary-value` for now. You will need to replace it later once you obtain your plugin ID.

### Start a local web server
Clone this repo  
```git clone git@github.com:kopeikins/gpt-dj.git```

Install python requirements  
```pip install -r requirements.txt```

Run FastAPI server  
```uvicorn app.main:app --reload```


### Set up Ngrok
To test plugins that don't use OAuth, you can have ChatGPT communicate with your localhost directly. However, when you enable OAuth settings, OpenAI requires you to use a "real" domain. While still in the development stage, you can keep your server running on localhost but utilize tools like [ngrok](https://ngrok.com) to create a domain that connects to your localhost via a tunnel. Setting up ngrok is simple; just follow their [instructions](https://dashboard.ngrok.com/get-started/setup) and initiate a tunnel to port 8000. 

```ngrok http 8000```

Once you start a tunnel, you will see a link like `https://<your_id>.ngrok.app`, which points to your localhost. You can use it at the later step when setting up a plugin.

### Set up ChatGPT Plugin
1. Start the local server.
2. Go to ChatGPT Plugin Store and click "Develop your own plugin".
3. Enter your ngrok domain: `<your_id>.ngrok.app`
4. Enter `client_id` and `client_secret` you obtained when creating the Spotify app.
5. ChatGPT will show you a verification token. Update it in your `ai-plugin.json` and click "Verify tokens".
6. Click "Install for me".
7. Click "Log in with GPT DJ (local version)".
8. You will encounter `INVALID_CLIENT: Invalid redirect URI` error. That's ok -- just note the plugin ID in the URL, which looks something like this: `plugin-9924812a-36e3-453d-8d11-f02754643cf7` (the part after "plugin-" will be different for you).
9. Edit your Spotify app and update `redirect_url` with the correct plugin ID.
10. Repeat the steps from 1 to 7, and this time, the authorization with Spotify should not fail.


## Usage

After plugin is installed, just type something like "Create a spotify playlist with top 10 hits from the 80s".

## How to Add Other Users
Since your Spotify app is in development mode, you need to add users manually. Go to your Spotify Developer Dashboard, find your app, click "Settings," and then "User Management." Add the user's email associated with their Spotify account.

To install your plugin, a user should open the Plugin Store in ChatGPT, click "Install Unverified Plugin," and enter your ngrok domain name. Make sure they don't click "Develop Your Own Plugin," as that would prompt them to input client_id and client_secret, which they cannot do.

## Contributions
Contributions are welcome. It would be interesting to add more features, such as adding songs on the fly, creating playlists for YouTube, etc.

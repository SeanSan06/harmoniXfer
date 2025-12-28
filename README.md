# HarmoniXfer
A full stack web based application currently in development that allows users to transfers songs between their Spotify and YouTube playlist automatically.

## Pictures of website
![Example Image](/frontend/images/homepage.png)

## Future features
- Use Scikit learn to perform machine learning and recommend the user new songs based on songs in the playlist they have added to the website.
- Design a dashboard that displays more statistical information and lets users use the song suggestion feature.
- Clean up the color scheme, aiming for a simplistic and iniviting website.
- Add footer and redesign the header bar. 

## How it's made
Technology used: HTML, CSS, TypeScript, FastAPI, Python, SQLite, YouTube API, and Spotify API.

**HTML**: I am using HTML to layout all of the content for each of the web pages(Home, Song Transfer, and About areas)

**CSS**: I am using CSS to create a simplistic and animated website that aims to make the website feel alive.

**TypeScript**: I am using TypeScript to give dynamic functionality to the website. Also so the frontend can communicate with the backend.

**FastAPI with Python**: I am using FastAPI to create a custom API that allows for real-time communication between the frontend and the backend. 

**SQLite**: I am using SQLite as our database, as I wanted a lightweight database that stores simple data such as number of songs transferred.

**YouTube**: I am using the YouTube API to get all the titles from a specific playlist. The user can simply type in the playlist's ID to get the data from it.

**Spotify**: I am using the Spotify API to get playlists and input songs into them based on what was in a users YouTube playlists.

## Depenencies
- pip install fastapi
- pip install uvicorn
- sudo apt update
- sudo apt install python3 python3-pip
- pip install python-dotenv
- pip install google-api-python-client
- npm install -g typescript
- pip install spotify


## What I learned/learning
I am learning more about using TypeScript and how to make custom objects that are especially useful when sending and recieve data from the backend. I am also learning more about designed more intricate websites with more animated parts. Additionaly, I am learning how to build larger backends that utilize more APIs and librarys.

## Credits
Thank you to YouTube API and Spotify API for the backend functionality.
Thank you to [TISEPSE](https://uiverse.io/profile/TISEPSE) for the animated button UI.
Thank you to [Cohen](https://uiverse.io/profile/cohencoo) for the animated text box input UI.
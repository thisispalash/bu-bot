# README

Submitted as the hackathon submission for [portal-212/mar](http://buhack.org/portal-212/mar)

***

## Project Overview

Bennett University currently faces an issue in terms of communication. There are too many middlemen involved in mass mailing and WhatsApp groups are too small to handle the size. Hence, we want to make the transition to Discord, a premier community management tool. We assist in this endevour by providing a UI to interact with the server, intuitively, while a bot does the heacy lifting in the background

### Domain Selected

`Bennett`

### Solution overview

Discord can be a challenge to use for the less tech savvy. As the aim is to get the entire university on the application, we provide an intuitive UI and helpful bots (such as reply) to aid in the transition. The vision is to also create bot managed games and a connection to the official CMS for assignment distribution and submission.

### Technologies used
- discordpy
- Flask

### Known Bugs

- As flask is not asynchronous, it can not call the bots and await the result
- the mgmt bot has incomplete commands
- No mail is being sent to individuals with the invite link and otps

### Source Code Directory structure

- `bots`: the bots added to the server; namely reply and mgmt
- `static`: Static files for the flask webapp (css,js)
- `templates`: Template HTML files for the flask webapp
- `app.py`: The main flask app file
- `demo.xlsx`: The demo data file for testing

### Installation guide

Need `app-env` with various secrets and ids. Message us to obtain it.

### Futures
- Debug and finish project
- Add JSON-LD functionality
- Add more bot functionality
  - Games
  - Voting / Polling system
- Switch to pymongo from json files
- **Deploy**

 
***

### Challenges Faced
- communication
- Organising as well as participating

### Learnings
- Flask, Discord.py
- Await in python and in life

***

### Link(s)

- [GitHub](https://github.com/palash96rox/bu-bot)

***

## Team

### Team Name

`#RoadtoSilverTWO`

### Team Members
  * Member 01
    * Name: Palash A
    * Email: pa5795
    * Roll Number: e17cse069
    * Role: Bot Father
    * Contribution: Created bots
  * Member 02
    * Name: Zubin C
    * Email: zc7326
    * Roll Number: e17cse150
    * Role: Designer
    * Contribution: UI and presentation design
  * Member 03
    * Name: Shreyas P
    * Email: sp3298
    * Roll Number: e17cse067
    * Role: Flask forger
    * Contribution: Flask backend and connections
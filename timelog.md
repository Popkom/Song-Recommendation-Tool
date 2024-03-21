# Timelog

- Song Recommendation Tool
- Leonidas Ioannou
- 2454882i
- Chris McCaig

## Guidance

- This file contains the time log for your project. It will be submitted along with your final dissertation.
- **YOU MUST KEEP THIS UP TO DATE AND UNDER VERSION CONTROL.**
- This timelog should be filled out honestly, regularly (daily) and accurately. It is for _your_ benefit.
- Follow the structure provided, grouping time by weeks. Quantise time to the half hour.

## Week 1

### 20 Sep 2023

- _0.5 hour_ Prep for initial supervisor meeting
- _2 hours_ Read project moodle and set up repository locally and on github

### 21 Sep 2023

- _0.5 hour_ Meeting with supervisor
- _2 hours_ Project information lecture

### 22 Sep 2023

- _0.5 hour_ Put supervisor meeting minutes on moodle and sent repo link to supervisor

* _2 hours_ Research on Recommender Systems, done half a tutorial on a basic content-based Recommender System

### 23 Sep 2023

- _1.5 hour_ Finish tutorial on a basic content-based Recommender System
- _2.5 hours_ Research into last.fm dataset and API

### 24 Sep 2023

- _3.5 hours_ Setup react project, lots of troubleshooting, basic app page, basic python requests function

## Week 2

### 25 Sep 2023

- _2 hours_ Contact with last.fm API, acquired API key, trying to learn how to make requests

### 26 Sep 2023

- _2 hours_ Requests work, process json response to get top 3 tags of a song

### 27 Sep 2023

- _1.5 hour_ Work to show field of song and rating that user input when add song button is pressed

* _0.5 hour_ Supervisor meeting prep

### 28 Sep 2023

- _0.5 hour_ Supervisor meeting
- _1.5 hour_ Uploaded meeting minutes to moodle, figured out how to have songs input and ratings show up when the add song button is pressed

### 29 Sep 2023

- _2 hours_ Research into middleware, started using Flask for backend, trying to get sending data from front end to backend working

### 30 Sep 2023

- _3 hours_ Can send track name and artist to backend, backend gets proper track name and artist from API, then gets tags for the track

### 1 Oct 2023

- _2 hours_ Trying to get correct song name and artist sent to front-end working

## Week 3

### 2 Oct 2023

- _2 hours_ Correct song name and artist sent to front-end, trying to debug some issues with the track information popping up after search because of time it takes to receive data

### 3 Oct 2023

- _2 hours_ After a lot of troubleshooting, after searching for song(by pressing add song button) via back end, a component with track name, artist, and rating shows up

### 4 Oct 2023

- _1.5 hour_ Wrote a function to keep the user's taste profile of tags, sorted by accumulated rating each tag has, pushed code to github

* _0.5 hour_ Supervisor meeting preparation

### 5 Oct 2023

- _0.5 hour_ More meeting preparation, supervisor meeting
- _1.5 hour_ Uploaded meeting minutes to moodle, Send signal to back-end when submit button is pressed, initial work on recommendations

### 6 Oct 2023

- _2 hours_ More work on recommendations, gets a lot of tracks based on top 3 tags for now and finds duplicates as recommendations(for now)

### 7 Oct 2023

- _3 hours_ Thinking about and tweaking recommendation algorithm and comparing results to try and see what gets better recommendations

## Week 4

### 9 Oct 2023

- _2 hours_ more tweaking of recommendation algorithm because the top tracks of some tags are not really representative of the actual tag

### 10 Oct 2023

- _2 hours_ Thought of new approach of getting recommendations, code now gets top artists of top 2 tags as well, next task is creating new song scoring system

### 11 Oct 2023

- _2 hours_ More work on scoring system

### 12 Oct 2023

- _2 hours_ Still working on scoring system and thinking of how it should work

### 14 Oct 2023

- _2.5 hours_ More work on scoring system
  _0.5 hour_ Supervisor meeting preparation

## Week 5

### 16 Oct 2023

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle
- _1.5 hour_ Completed first version of scoring system and recommendations, done a bit of testing

### 17 Oct 2023

- _1 hour_ More testing, satisfying results, could definitely use improvements

* _1 hour_ Thinking and planning about potential improvements, maybe a way to give sub-genres priority to enhance recommendations

### 18 Oct 2023

- _2.5 hours_ More planning about potential improvements, code now doesn't return more than 2 recommendations by the same artist

### 19 Oct 2023

- _1 hour_ User can now set number of recommendations they want, setup in communication to pass other parameters to back-end

### 20 Oct 2023

- _1.5 hour_ User can now set how many recommendations from the same artist should be allowed, recommendations and top 3 user tags now printed in front end.
- _0.5 hour_ Update github repo, supervisor meeting preparation

## Week 6

### 24 Oct 2023

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle

### 26 Oct 2023

- _2 hours_ Implemented remove song button, it removes the latest song added

### 27 Oct 2023

- _2 hours_ Implemented clear songs button, it also asks for confirmation, initial work to get list of all tags to make priority list

### 28 Oct 2023

- _2.5 hours_ User profile now takes into account how many times a tag was added to a song, boosting sub-genres even higher
- _0.5 hour_ Supervisor meeting prep, pushed to github repository

## Week 7

### 30 Oct 2023

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle
- _1 hour_ Fixed bug where setting number of recommendations from same artist to 1 would not work

* _0.5 hour_ Fixed remove song button

### 31 Oct 2023

- _1 hour_ Thinking of how to improve recommendations even more, potentially give higher scores to songs from artists the user inputs, could help in cases of not many recommendations
- _1 hour_ Started work on wireframes on figma

### 1 Nov 2023

- _2 hours_ Made more wireframes

## Week 8

### 7 Nov 2023

- _2 hours_ Songs from artists the user inputs get a boost in score, would help in cases where there are not that many recommendations

* _1 hour_ Looking into possible spotify integration, what would make a useful feature

### 8 Nov 2023

- _1 hour_ Trying to understand Spotify API, some basic setup work
- _0.5 hour_ Supervisor meeting preparation
- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle

### 9 Nov 2023

- _2 hours_ Can get Spotify IDs of recommended tracks, bugfixing required as sometimes requests don't work

### 10 Nov 2023

- _2 hours_ Searching some songs would return 0 results, fixed it by having a different query run if it happens

### 11 Nov 2023

- _2 hours_ Figuring out how to create a playlist with API calls, probably needs to be done on front-end
- _0.5 hour_ Supervisor meeting preparation

## Week 9

### 13 Nov 2023

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle

* _1.5 hour_ Writing code to get user authorization, spotify authorization popup works, need to make sure I store the token properly

### 14 Nov 2023

- _2 hours_ Trying to figure out how to make program wait for user to finish authorizing the app from the spotify pop-up

### 15 Nov 2023

- _2 hours_ can get proper user access token and send it to back-end, trying to fix bug where reseting url clears the token

### 16 Nov 2023

- _2 hours_ User access token is now being properly sent to the back-end, however a new bug that I am trying to fix has appeared where it is sent twice

### 17 Nov 2023

- _2 hours_ Create a Spotify Playlist feature almost done ,just need to fix a small syntax bug in the request to populate the already-created playlist

### 18 Nov 2023

- _2 hours_ Finished create a playlist feature, started improvements on spotify search track matching
- _0.5 hour_ Supervisor meeting preparation(meeting ended up being cancelled)

## Week 10

### 21 Nov 2023

- _2 hours_ Made some improvements on spotify search track matching, still needs more

### 22 Nov 2023

- _1 hours_ Still trying to improve spotify search track matching

### 24 Nov 2023

- _2 hours_ More refinements to spotify search track matching

### 25 Nov 2023

- _0.5 hour_ Still trying to perfect the spotify search track matching - current issue is artists with numbers in their name
- _0.5 hour_ Supervisor meeting preparation

### Week 11

## 27 Nov 2023

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle

* _1.5 hour_ Added some code that converts the number to words for a specific artist to make it work since after testing some other cases, other artists with numbers in their name work correctly, still some cases that don't work though, needs more improvement

## 29 Nov 2023

- _2 hours_ Testing shows that many examples still dont return spotify search results, trying to figure out how to use a framework made for using the spotify API with python(spotipy)

## 30 Nov 2023

- _2 hours_ After implementing search with spotipy, nothing different

## 1 Dec 2023

- _2 hours_ Researching the issue online and trying workarounds

## 2 Dec 2023

- _2.5 hours_ Still trying to research workarounds, not many results, trying to think of what to do with this feature

### Week 12

## 4 Dec 2023

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle

* _1 hour_ Tweaking around the cases for the spotify searchs

## 6 Dec 2023

- _2 hours_ going over and tweaking search cases to get better results

### Week 13

## 11 Dec 2023

- _8 hours_ Overall performance of Spotify API Search improved with more tweaks, Added error handling in case songs don't have 3 or more tags, in case user's profile is empty when they click submit, a message appears with the tracks that could not be found on Spotify. Thinking of other possible features

## 12 Dec 2023

- _1 hour_ Thought of new feature, get and display a list of the most popular last.fm tags(as suggestions), allow user to prioritise some tags by adding three input fields
- _0.5 hour_ Supervisor meeting preparation, updated github repository
- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle

* _6 hours_ Implemented the new feature, started styling the app

## 13 Dec 2023

- _8 hours_ Finished styling

## 14 Dec 2023

- _3 hours_ Wrote and submitted status report
- _2 hours_ Thought of an initial plan for evaluation, wrote down a draft of questions and process

## 15 Dec 2023

- _4 hours_ Refactored some of the code

### Week 17

## 08 Jan 2024

- _0.5 hour_ Supervisor meeting preparation
- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle
- _1 hour_ Fixed the following bugs by adding error alerts: Song added doesn't have genre tags recorded, Song added not found, User clicks remove song button when there are no songs to remove

## 09 Jan 2024

- _2 hours_ Decided that final feature should be a checkbox that allows the user to decide if they want recommendations from artists they have input, properly implemented the feature

## 10 Jan 2024

- _2 hours_ Testing the app, added error messages if number of recommendations parameter and number of recommendations from same artist to be allowed parameter are not numbers

## 11 Jan 2024

- _2 hours_ More bug hunting, made a draft Google Form of the evaluation

## 13 Jan 2024

- _0.5 hour_ More bug hunting, added error messages if number of recommendations parameter and number of recommendations from same artist to be allowed parameter are numbers <= 0
- _0.5 hour_ Supervisor meeting preparation

### Week 18

## 15 Jan 2024

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle
- _0.5 hour_ Converted evaluation form questions to proper Likert Scale format
- _0.5 hour_ App no longer allows user to input the same song more than once
- _0.5 hour_ Started trying to gather participants

## 16 Jan 2024

- _0.5 hour_ Gathering more participants

## 17 Jan 2024

- _1 hour_ Tried different colour schemes, current one is a light red background with red buttons

## 18 Jan 2024

- _1 hour_ Finalised participants for evaluation, found ethics checklist and made a consent form for participants.

## 20 Jan 2024

- _0.5 hour_ Supervisor meeting preparation

### Week 19

## 22 Jan 2024

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle

* _1 hour_ Found some papers to go through and use for the background section of the dissertation
* _0.5 hour_ Thought that by using last.fm listening data to get similar songs to ones input, can improve recommendations by boosting scores of recommendations that people that listen to the input songs listen to as well, introducing a collaboration-based recommender system aspect to my algorithm

## 23 Jan 2024

- _1 hour_ Implemented collaboration-based aspect mentioned above

## 24 Jan 2024

- _1.5 hour_ Made notes on the first paper to be used for the background section of the dissertation

## 25 Jan 2024

- _2 hours_ Working through and making notes on the second paper

## 26 Jan 2024

- _1.5 hours_ Finished working through and making notes on the second paper

## 27 Jan 2024

- _0.5 hour_ Supervisor meeting preparation

### Week 20

## 29 Jan 2024

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle

* _1.5 hour_ Read through and made notes on third paper

## 31 Jan 2024

- _1 hour_ Tried multiple other colour schemes, decided on a new one although kept details of previous one

## 1 Feb 2024

- _1 hour_ Found more resources on recommender systems in general

## 2 Feb 2024

- _1 hour_ Made a plan for the background section of the dissertation

## 3 Feb 2024

- _1.5 hour_ Started writing background section of the dissertation
- _0.5 hour_ Supervisor meeting preparation

### Week 21

## 5 Feb 2024

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle
- _0.5 hour_ Contacted evaluation participants asking for email addresses to send consent forms
- _0.5 hour_ Sent consent forms to evaluation participants
- _0.5 hour_ Continued work on dissertation background

## 6 Feb 2024

- _2 hours_ Continued work on dissertation background

## 7 Feb 2024

- _2 hours_ Continued work on dissertation background

## 8 Feb 2024

- _0.5 hour_ Received signed consent forms from all participants, signed them myself and sorted them
- _1.5 hour_ Reached out to all participants and set dates and times for the stage of the evaluation where they use the app

## 9 Feb 2024

- _1 hour_ Ran two evaluation sessions
- _1 hour_ Continued work on dissertation background

## 10 Feb 2024

- _1.5 hour_ Ran three evaluation sessions
- _0.5 hour_ Fixed a bug that occured during one of the evaluations
- _0.5 hour_ Continued work on dissertation background
- _0.5 hour_ Supervisor meeting preparation

## 11 Feb 2024

- _0.5_ Ran one evaluation

### Week 22

## 12 Feb 2024

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle
- _1 hour_ Ran two evaluations

## 13 Feb 2024

- _0.5 hour_ Ran one evaluation
- _0.5 hour_ Fixed another bug
- _1 hour_ Continued work on dissertation background

## 14 Feb 2024

- _2 hours_ Continued work on dissertation background

## 15 Feb 2024

- _0.5 hour_ Ran the final evaluation
- _1.5 hour_ Continued work on dissertation background

## 16 Feb 2024

- _2 hours_ Continued work on dissertation background

## 17 Feb 2024

- _2 hours_ Finished draft of dissertation background
- _0.5 hour_ Supervisor meeting preparation

### Week 23

## 19 Feb 2024

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes too moodle
- _0.5 hour_ Planned how many pages to allocate to each remaining chapter
- _1 hour_ Started work on analysis/requirements chapter

## 21 Feb 2024

- _2 hours_ Continued work on analysis/requirements chapter

## 22 Feb 2024

- _2 hours_ Finished draft of analysis/requirements chapter

## 23 Feb 2024

- _0.5 hours_ Checked background section feedback and adjusted dissertation based on it
- _1.5 hours_ Started design chapter

## 24 Feb 2024

- _2 hours_ Continued work on design chapter

* _0.5 hour_ Supervisor meeting preparation

### Week 24

## 26 Feb 2024

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle
- _1.5 hour_ Continued work on design chapter

## 27 Feb 2024

- _2 hours_ Continued work on design chapter

## 28 Feb 2024

- _2 hours_ Continued work on design chapter

## 29 Feb 2024

- _2 hours_ Finished design chapter

## 02 Mar 2024

- _3 hours_ Started implementation chapter

## 03 Mar 2024

- _1 hour_ Continued implementation chapter
- _0.5 hour_ Supervisor meeting preparation

### Week 25

## 04 Mar 2024

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle
- _0.5 hour_ Changed all figure references in dissertation to latex references
- _1 hour_ Continued work on implementation chapter

## 05 Mar 2024

- _2 hours_ Continued work on implementation chapter

## 06 Mar 2024

- _2 hours_ Continued work on implementation chapter

## 07 Mar 2024

- _2 hours_ Continued work on implementation chapter

## 08 Mar 2024

- _2 hours_ Continued work on implementation chapter

## 09 Mar 2024

- _2 hours_ Finished implementation chapter

## 10 Mar 2024

- _2.5 hours_ Started evaluation chapter
- _0.5 hour_ Supervisor meeting preparation

### Week 26

## 11 Mar 2024

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle
- _1.5 hour_ Continued work on evaluation chapter

## 12 Mar 2024

- _2 hours_ Continued work on evaluation chapter

## 13 Mar 2024

- _3 hours_ Finished work on evaluation chapter

## 14 Mar 2024

- _2 hours_ Wrote introduction chapter

## 15 Mar 2024

- _2 hours_ Wrote conclusion chapter

## 16 Mar 2024

- _2 hours_ Wrote abstract, properly added bibliography references

## 17 Mar 2024

- _2 hours_ Added most appendices, started proof-reading

* _0.5 hour_ Supervisor meeting preparation

### Week 27

## 18 Mar 2024

- _0.5 hour_ Supervisor meeting, uploaded meeting minutes to moodle
- _1 hour_ Finished proof-reading
- _2 hours_ Created presentation slides

## 19 Mar 2024

- _1 hour_ Recorded presentation
- _0.5 hour_ Created directory structure file, added to appendices
- _0.5 hour_ Prepared for submission.

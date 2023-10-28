# Timelog

- PROJECT NAME
- YOUR NAME
- STUDENT_ID
- SUPERVISOR NAME

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

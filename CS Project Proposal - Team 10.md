Project Proposal – Team \#10

# **Impulse (Mobile App)**

## **Project Overview**

Impulse is a mobile app that seeks to provide a convenient and direct way for students to make new friends and engage in campus activities. One major issue that prevents students from socializing in traditional university-ran events is due to schedule conflicts. Our mobile app seeks to allow students to both create and join events themselves based upon when they are available.

At its core, Impulse will provide students an avenue to create and join events and people that can range from study groups, sporting events, or group finding for class projects. We believe that allowing students the power and ability to create and join such events will greatly improve the students' time on campus and their overall experience with the university. We want to allow more student autonomy for making their own plans based on their own interest to foster connections outside of regular current campus-based activities. 

## **Project Scope**

**Core functionalities/features:**  

* Ability to create and join UTD student led events and hangouts.  
* User authentication \- ensures only verified students can access the platform.   
* Map to see where the events and hangouts are.  
* Progression based incentives with gaming features ex. avatar, levels  
* Interactive virtual lobbies to discuss.  
* Ability for students to post information regarding their schedules and interests.

**Stretch goals:** 

* Integration of an AI-powered chatbot(Teem Bot) for personalized event recommendations. 

## **Project Objectives**

*5 main project objectives.*

1. Create an appealing UI/UX for college students.  
2. Provide user authentication to ensure every user is a student.  
3. Maintain a database that contains user and event records.  
4. Design and implement algorithms that allow users to find desired events.  
5. Integrate front and back end design.

*Specify measurable goals for development and deployment.*

6. Framework set up by February 28th  
7. Development/Implementation by April 4th  
8. Testing/Integration by April 18th  
9. Final Testing/Presentation by May 2nd

*Highlight expected outcomes and deliverables.*

10.  Application where students can make events and form connections based on their schedules and interests.  
11. Allow students to foster long-lasting connections and ability to find any event they want to look at on the application.

## **Specifications**

#### *User Interface (UI) Design*

* Define the platform(s) (mobile, web, desktop).  
- Mobile  
* The platform for the project will be launched as a mobile application.  
* Key screens/Functionality:  
- The first screen will display the login for users and will redirect students to verify their student status.  
- After logging in, the main page will be displayed with the current events hosted by students.  
- The main page will also include a tab for student led postings with categories.  
- In this section, students will be able to post what kinds of activities they would like to start and other information regarding events.  
- Next there will be a campus map screen when clicking on events.  
- The campus map screen with the event location where the event is held after the student presses “Location” for the selected events details screen.  
- After the student selects the event, the screen displaying the current lobby of other students attending the event is located under the details screen.  
- On the side of the main page and an extra tab at the side, there will be a chatbot screen, for students to ask relevant questions including example prompts.  
- On the side, there will be a settings screen to manage profile and privacy, if students want to change unlocked information.

	Screens included an event specifically:

- Screen for event details.  
- Screen for creating an event.  
- A map for the selected event’s location.  
- A screen for students to view and update their avatar, and the ability to see their awards won for attending certain events.  
- Screen for viewing the event a student signs up for.  
- After a student attends an event, a pop up will display on the students current screen showcasing the award received for attending a certain event.  
* List of user interaction elements (buttons, menus, forms):  
- Button for selecting and viewing details of the events.  
- Button for viewing the interactive map of the selected event.  
- Button for using the AI chatbot.  
- Filter button to sort through students desired details, such as time, category of event, location, etc.  
- Button for reporting an event if it violates guidelines.  
- Bookmarked button, students may save an event without signing up if unsure, or other reasons.   
- Menu bar where “Events, Location, Bookmarked, Avatar, Profile” each has a button.  
- Button for viewing the current lobby of a selected event.  
- Form for creating an event.  
- Buttons for rating the event after it ends.   
- Button to view the details of registered events.  
- On the avatar screen, there are several options for a student to modify their character and view their past history of rewards received.    
- Side section to include more information/screens

#### *Backend & APIs*

* Outline the database and API structure.  
  * Database Structure:  
    * Users: Stores user data   
    * Events: Store even details   
    * Chats: Tracks chat messages exchanged between users for event discussion .  
    * Progression/Incentives: Stores data for user rewards and levels based on event participation.   
  * API structure:  
    * User Authentication   
    * Event Management   
    * Chat API  
    * Progression System  
* Specify authentication and security considerations.  
  * Firebase Authentication: ensures only UTD students can access the platform 

#### *AI*

* Describe the ML model’s functionality.  
  * Event Recommendation   
  * Telling list of events based on some filter criteria   
* Mention any data sources and preprocessing steps.  
  * User data  
  * Event data

## **Tech Stack**

* **Frontend:** React Native  
* **Backend:** Flask  
* **Database:** PostgreSQL  
* **Cloud & Hosting:** Firebase (?)  
* **AI:** Open AI/ Llama API

## **Hardware Requirements**

* Cell Phone  
* Computer

## **Software Requirements**

* VSCode (or IDE equivalent)  
* Github  
* Figma  
* Jira

## **Project Timeline**

| Sprint | Duration | Tasks |  |  | Team Leader  |
| :---: | ----- | ----- | ----- | ----- | ----- |
|  |  | **Front end** | **Back end** | **General** |  |
| 1a | 2.14.25 \- 2.28.25 | Plan screen designs | Finalize tech stack | Define scope, research, and setup | Patrick |
| 1b | 2.21.25 \- 2.28.25 | Convert the Figma into React through Build.io | Initialize server and DB | Define scope, research, and setup | Patrick |
| 2a | 2.28.25 \- 3.7.25 | \- Figure out how to integrate the front-end and back-end \- Finish converting the Figma Screens | \-Finalize DB design \-Populate DB with test data \-Begin front and back integration  | UI/UX design, data collection, API setup | Sophia |
| 2b | 3.7.25 \- 3.14.25 | \- Implement the UI/UX interactive components with the react native screens. | \-Continue creation and testing of core back-end features \-Integrate front and back end features as needed  | UI/UX design, data collection, API setup | Sophia |
| 3a | 3.14.25 \- 3.21.25 | \- Finish making the the front-end responsive and looking at how to integrate the APIs |  | Development and initial implementation | Neethu |
| 3b | 3.21.25 \- 3.28.25 | \- Keep working on development and making the screens functional |  | Development and initial implementation | Neethu |
| 3c | 3.28.25 \- 4.4.25 | \- Keep working on development and making the screens functional |  | Development and initial implementation | Neethu |
| 4a | 4.4.25 \- 4.11.25 | \- Start testing and debugging |  | Testing and integration | Esha |
| 4b | 4.11.25 \- 4.18.25 | \- Finish debugging \- Test across devices (iOS, Android) |  | Testing and integration | Esha |
| 5a | 4.18.25 \- 4.25.25 | \- Final UI polish & animations \- Prepare for the presentation |  | Final testing, deployment, and presentation | Patrick |
| 5b | 4.25.25 \- 5.2.25 | \- Prepare for the presentation |  | Final testing, deployment, and presentation | Patrick |

## 

## **Project Team**

| Role | Team Member | Responsibilities |
| ----- | ----- | ----- |
| Frontend Developer | Primary: Esha Kumar     Secondary: Sophia O’Malley | UI development |
| Backend Developer | Primary: Sai Neethu Bonagiri     Secondary: Patrick Guinn | API & Database |
| QA Tester | Entire Team | Testing & validation |

## **Links**

* **GitHub Repository:** [github.com/eshakumar0920/Team-10](http://github.com/eshakumar0920/Team-10)

* **Agile Board:**   
  [https://sophiaomalley.atlassian.net/jira/software/projects/SCRUM/boards/1?atlOrigin=eyJpIjoiNGU1ODQ3Mzg4ZDY1NDdhMWJhY2M4Y2JiNmFjOWUwMjMiLCJwIjoiaiJ9](https://sophiaomalley.atlassian.net/jira/software/projects/SCRUM/boards/1?atlOrigin=eyJpIjoiNGU1ODQ3Mzg4ZDY1NDdhMWJhY2M4Y2JiNmFjOWUwMjMiLCJwIjoiaiJ9)  
    
* **Design Document:** [https://www.figma.com/files/team/1471687386059162349/all-projects](https://www.figma.com/files/team/1471687386059162349/all-projects)


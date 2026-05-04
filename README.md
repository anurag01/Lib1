# Library Management Backend

This is the backend for the Library Management application. It is built using Python and provides RESTful APIs for managing books, users, and reminders.

## Project Structure

- `app/`: Contains the main application code.
  - `models/`: Contains the data models for the application.
  - `routes/`: Contains the API routes for handling requests.
  - `services/`: Contains the business logic for notifications and reminders.
  - `config.py`: Configuration settings for the application.

## Setup Instructions

### Backend Setup

1. Navigate to the `backend` directory.
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```App Library maangement:App Library maangement:


App & Website: 
   Mobile version: Android and ios 
   Hybrid: websit acceible from laptop/tabs etc 




Feature: 

   1. Provide entry for books (currently all books are physical): 
        Books fields Profile, Author, ISBN, Price, Genre , Summary. Add other necessory fields 
   2. Display books with Images, availabitly/ out of stock 
   3. Books should be returned within 7 days 



  Subsription Plans: 49/month, 149/months, 49/months, it should be configurable from admin 
  Based on plan there will be charges for book ( How many books he can renew per months like that)

  Registration Charges- One time 
  Refundable security deposti- on time 
  rental charges as per plans 


User Profile/User registration (Customer registration)

Admin and User will get notification of under what plan user has regsitered from which location of library( Here we will give one button that will display all notification about it currently not sms or email (later we can go for sms and email as well)

Set reminders for book return, fees, book renewable to user and admins for expiry (this reminder will display as notification in button)



App & Website: 
   Mobile version: Android and ios 
   Hybrid: websit acceible from laptop/tabs etc 




Feature: 

   1. Provide entry for books (currently all books are physical): 
        Books fields Profile, Author, ISBN, Price, Genre , Summary. Add other necessory fields App Library maangement:


App & Website: 
   Mobile version: Android and ios 
   Hybrid: websit acceible from laptop/tabs etc 




Feature: 

   1. Provide entry for books (currently all books are physical): 
        Books fields Profile, Author, ISBN, Price, Genre , Summary. Add other necessory fields App Library maangement:


App & Website: 
   Mobile version: Android and ios 
   Hybrid: websit acceible from laptop/tabs etc 




Feature: 

   1. Provide entry for books (currently all books are physical): 
        Books fields Profile, Author, ISBN, Price, Genre , Summary. Add other necessory fields App Library maangement:


App & Website: 
   Mobile version: Android and ios 
   Hybrid: websit acceible from laptop/tabs etc 




Feature: 

   1. Provide entry for books (currently all books are physical): 
        Books fields Profile, Author, ISBN, Price, Genre , Summary. Add other necessory fields App Library maangement:


App & Website: 
   Mobile version: Android and ios 
   Hybrid: websit acceible from laptop/tabs etc 




Feature: 

   1. Provide entry for books (currently all books are physical): 
        Books fields Profile, Author, ISBN, Price, Genre , Summary. Add other necessory fields 
   2. Display books with Images, availabitly/ out of stock 
   3. Books should be returned within 7 days 



  Subsription Plans: 49/month, 149/months, 49/months, it should be configurable from admin 
  Based on plan there will be charges for book ( How many books he can renew per months like that)

  Registration Charges- One time 
  Refundable security deposti- on time 
  rental charges as per plans 


User Profile/User registration (Customer registration)

Admin and User will get notification of under what plan user has regsitered from which location of library( Here we will give one button that will display all notification about it currently not sms or email (later we can go for sms and email as well)

Set reminders for book return, fees, book renewable to user and admins for expiry (this reminder will display as notification in button)

   2. Display books with Images, availabitly/ out of stock 
   3. Books should be returned within 7 days 



  Subsription Plans: 49/month, 149/months, 49/months, it should be configurable from admin 
  Based on plan there will be charges for book ( How many books he can renew per months like that)

  Registration Charges- One time 
  Refundable security deposti- on time 
  rental charges as per plans 


User Profile/User registration (Customer registration)

Admin and User will get notification of under what plan user has regsitered from which location of library( Here we will give one button that will display all notification about it currently not sms or email (later we can go for sms and email as well)

Set reminders for book return, fees, book renewable to user and admins for expiry (this reminder will display as notification in button)

   2. Display books with Images, availabitly/ out of stock 
   3. Books should be returned within 7 days 



  Subsription Plans: 49/month, 149/months, 49/months, it should be configurable from admin 
  Based on plan there will be charges for book ( How many books he can renew per months like that)

  Registration Charges- One time 
  Refundable security deposti- on time 
  rental charges as per plans 


User Profile/User registration (Customer registration)

Admin and User will get notification of under what plan user has regsitered from which location of library( Here we will give one button that will display all notification about it currently not sms or email (later we can go for sms and email as well)

Set reminders for book return, fees, book renewable to user and admins for expiry (this reminder will display as notification in button)

   2. Display books with Images, availabitly/ out of stock 
   3. Books should be returned within 7 days 



  Subsription Plans: 49/month, 149/months, 49/months, it should be configurable from admin 
  Based on plan there will be charges for book ( How many books he can renew per months like that)

  Registration Charges- One time 
  Refundable security deposti- on time 
  rental charges as per plans 


User Profile/User registration (Customer registration)

Admin and User will get notification of under what plan user has regsitered from which location of library( Here we will give one button that will display all notification about it currently not sms or email (later we can go for sms and email as well)

Set reminders for book return, fees, book renewable to user and admins for expiry (this reminder will display as notification in button)

   2. Display books with Images, availabitly/ out of stock 
   3. Books should be returned within 7 days 



  Subsription Plans: 49/month, 149/months, 49/months, it should be configurable from admin 
  Based on plan there will be charges for book ( How many books he can renew per months like that)

  Registration Charges- One time 
  Refundable security deposti- on time 
  rental charges as per plans 


User Profile/User registration (Customer registration)

Admin and User will get notification of under what plan user has regsitered from which location of library( Here we will give one button that will display all notification about it currently not sms or email (later we can go for sms and email as well)

Set reminders for book return, fees, book renewable to user and admins for expiry (this reminder will display as notification in button)

     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the backend server:
   ```
   python app/main.py
   ```

### Frontend Setup

1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```
   npm install
   ```
3. Run the frontend application:
   ```
   npm start
   ```

## Connecting Frontend and Backend

Ensure that the frontend makes API calls to the backend endpoints defined in the routes. Test the integration by running both the backend and frontend applications simultaneously.

## License

This project is licensed under the MIT License.
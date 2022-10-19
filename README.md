# Login-Registration

This project demonstrates my skills on building a Flask application that allows login, registration, validation and interaction with the database. 

# Registration
The user inputs their information, we verify that the information is correct, insert it into the database and return back with a success message. If the information is not valid, redirect to the registration page and show the following requirements:

# Validations and Fields to Include
1. First Name - letters only, at least 2 characters and that it was submitted
2. Last Name - letters only, at least 2 characters and that it was submitted
3. Email - valid Email format, does not already exist in the database, and that it was submitted
4. Password - at least 8 characters, and that it was submitted
6. Password Confirmation - matches password

# Login
When the user initially registers we would log them in automatically, but for logging in, we need to validate in a different way:
1. Check whether the email provided is associated with a user in the database
2. If it is, check whether the password matches what's saved in the database

# Logout
On the success page, have a logout button or link. When a user logs out, their session should be cleared. If the user attempts to access the success page (i.e. making a GET request by typing in the url), redirect them back to the login and registration page.

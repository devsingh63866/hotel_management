1️⃣ Programming Language Used

1) Python (version 3.x)

  * Used for all backend logic and server-side programming.
  * Django Framework (Python-based web framework) used for:

     * Handling routes (URLs)
     * Connecting database
     * Creating models (tables)
     * Rendering HTML templates
     * Managing authentication (login, logout, register)

Additional Technologies:

 * HTML, CSS → for frontend design


)
📘 Overview

A complete Hotel Management System built using Django (Python Framework) to manage rooms, customers, check-ins, checkouts, and billing.
It provides an easy-to-use dashboard for hotel staff to handle daily operations efficiently.

.

🚀 Features

   * Room management (add, view, update, delete rooms)
   * Customer management
   * Check-in and checkout process
   * Dashboard showing:
        Total rooms
        Available rooms
        Active bookings
        Current guests (with room info)
    * Bill generation
    * Secure login/logout system


🏨 Hotel Management System — Project Flow Explanation

The Hotel Management System is a web-based application developed using Python’s Django framework with SQLite as the backend database. The main objective of this project is to simplify and automate hotel operations such as room management, customer check-in, check-out, and billing. The system provides a secure login for hotel staff, ensuring that only authorized users can access the management dashboard.

The project flow begins with the registration module, where new hotel staff members can create an account by entering their basic details such as username and password. This information is securely stored in Django’s built-in authentication system. Once registered, users can proceed to the login page, where they are authenticated before gaining access to the system. After successful login, the user is redirected to the dashboard, which serves as the control center of the entire application.

The dashboard displays important hotel statistics like the total number of rooms, available rooms, and currently active bookings. It also provides quick links to manage rooms, check in customers, and check out customers. Additionally, the dashboard includes a table showing the list of guests currently staying in the hotel, including their booking ID, room number, check-in date, and contact details. This allows staff to get an instant overview of room occupancy and active customers.

From the dashboard, the user can navigate to the room management section, where new rooms can be added, viewed, or deleted. Each room record contains details like room number, room type (single, double, deluxe), price per night, and availability status. When a room is booked, its availability status automatically changes to “unavailable,” preventing double booking.

The check-in module allows staff to register a new customer by filling out their name, contact information, and selecting an available room. Once the form is submitted, a booking record is created with the current date and time as the check-in timestamp. The selected room’s availability status is updated to false, and the booking details are stored in the database. After check-in, the customer immediately appears on the dashboard under the list of current guests.

When the customer is ready to leave, the check-out module is used. Staff enter the customer’s booking ID, and the system calculates the total number of nights stayed using the difference between the check-in and check-out timestamps. The total bill amount is then calculated based on the room’s price per night multiplied by the number of nights. Once the checkout is completed, the booking is marked as inactive, and the room becomes available again for new guests. The system then redirects to the bill page, where all details of the stay and total charges are displayed.

Finally, users can securely log out of the system, which ends their session and prevents unauthorized access.

The project thus follows a complete cycle — registration → login → dashboard → room management → check-in → dashboard update → checkout → bill generation → logout.
This logical flow ensures that all hotel operations are performed systematically, efficiently, and with minimal manual intervention.
     

# Hassle-Free-Ticketing

[Routes](#routes) | [Building](#building) | [Interaction](#interaction)

This project was developed as part of the Trinity College Dublin Hackathon. Our software introduces a free ticketing system, relieving college societies of extra charges for ticketing processes for various events. Event organizers can easily keep track of those who express interest in the event and who actually purchase tickets. This is achieved by our custom-made algorithm, which scrapes the .csv formatted bank statement, identifies the payers, and updates the database accordingly. The fact that our solution is designed to be self-instantiating means that event organizers can safely upload their bank statements without worrying about sharing them with third-party platforms.

## Routes

### Create new/update existing users and/or events 

<details>
 <summary><code>POST</code> <code><b>/register</b></code> <code>(register a new user)</code></summary>

##### Parameters

> None


##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | 201         | application/json                | {"code":"201","error": None,"message": "client registered successfully"|
> | 400         | application/json                | {"code":"400","error":"Bad Request","message": "Please provide client details"}|
> | 500         | application/json                | {"code":"500","error": "Internal server error","message": "An error occurred"}|

</details>

<details>
 <summary><code>POST</code> <code><b>/login</b></code> <code>(log in using existing credentials)</code></summary>

##### Parameters

> None


##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | 201         | application/json                | {"code":"201","error": None,"message": "client logged in successfully"|
> | 400         | application/json                | {"code":"400","error":"Bad Request","message": "Please provide client details"}|
> | 401         | application/json                | {"code":"401","error": "Unauthorized","message": "Invalid email or password"}|
> | 500         | application/json                | {"code":"500","error": str(e),"message": "An error occurred"}|

</details>

<details>
 <summary><code>POST</code> <code><b>/event/{event_id}/register</b></code> <code>(register for an existing event)</code></summary>

##### Parameters

> | name              |  type     | data type               | description                          |
> |-------------------|-----------|-------------------------|--------------------------------------|
> | current_user      |  required | Object                  | Object containing current user data  |
> | event_id          |  required | int                     | Event ID                             |


##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | 201         | application/json                | {"code":"201","error": None,"message": "Client registered for event successfully"|
> | 500         | application/json                | {"code":"500","error": str(e),"message": "Failed to register client for event"}|

</details>

<details>
 <summary><code>POST</code> <code><b>/create-event</b></code> <code>(create a new event)</code></summary>

##### Parameters

> | name              |  type     | data type               | description                          |
> |-------------------|-----------|-------------------------|--------------------------------------|
> | current_user      |  required | Object                  | Object containing current user data  |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | 201         | application/json                | {"code":"201","error": None,"message": "Event created successfully"|
> | 400         | application/json                | {"code":"400","error":"Bad Request","message": "Please provide event details"}|
> | 500         | application/json                | {"code":"500","error": "Internal server error","message": "An error occurred"}|

</details>

<details>
 <summary><code>POST</code> <code><b>/bank-statement/{event_id}</b></code> <code>(upload a bank statement for processing)</code></summary>

##### Parameters

> | name              |  type     | data type               | description                          |
> |-------------------|-----------|-------------------------|--------------------------------------|
> | current_user      |  required | Object                  | Object containing current user data  |
> | event_id          |  required | int                     | Event ID                             |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | 200         | application/json                | {"code":"200","error": None,"message": "File uploaded successfully"|
> | 400         | application/json                | {"code":"400","error":"Bad Request","message": "File expected"}|
> | 400         | application/json                | {"code":"400","error":"Bad Request","message": "CSV file expected"}|
> | 400         | application/json                | {"code":"400","error":"Bad Request","message": "CSV structure is invalid"}|

</details>

------------------------------------------------------------------------------------------------------------------------------------------

### Listing existing events

<details>
 <summary><code>GET</code> <code><b>/event/{event_id}</b></code> <code>(retrieve the event page)</code></summary>

##### Parameters

> | name              |  type     | data type               | description                          |
> |-------------------|-----------|-------------------------|--------------------------------------|
> | current_user      |  required | Object                  | Object containing current user data  |
> | event_id          |  required | int                     | Event ID                             |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | 200         | application/json                | {"code":"200","error": None,"message": "Event retrieved successfully"|
> | 400         | application/json                | {"code":"400","error":"Bad Request","message": "Please provide event id"}|
> | 404         | application/json                | {"code":"404","error":"Bad Request","message": "Event not found""}|

</details>

-------------------------------------------------------------------------------------------------------------------------------------------

### Testing Routes (Subject to utilization or removal from the codebase)

<details>
 <summary><code>GET</code> <code><b>/</b></code> <code>(test the functionality of the server)</code></summary>

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | 200         | application/json                | {"code":"200","error": None,"message": "Welcome to the API"|

</details>

<details>
 <summary><code>GET</code> <code><b>/table</b></code> <code>(check the contents of the database tables)</code></summary>

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | 200         | application/json                | {"code":"200","error": None,"message": "Table retrieved successfully"|

</details>

<details>
 <summary><code>GET</code> <code><b>/session</b></code> <code>(check the functionality of the authorization)</code></summary>

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | 200         | application/json                | {"code":"200","error": None,"message": "Session retrieved successfully"|

</details>

<details>
 <summary><code>GET</code> <code><b>/user</b></code> <code>(check the data of the current user)</code></summary>

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | 200         | application/json                | {"code":"200","error": None,"message": "User retrieved successfully"|

</details>

-------------------------------------------------------------------------------------------------------------------------------------

### Building

Requirements:
 - Docker

1. Clone the repository: git clone `https://github.com/mykbit/Hassle-Free-Ticketing.git`
2. Navigate to the project directory: cd `path/to/Hassle-Free-Ticketing`
3. Insert your Revolut QR code (or simply your account details) in `/Hassle-Free-Ticketing/client/src/assets/`
4. Build the project: `docker compose up --build`

### Interaction

1. By default the app is hosted locally, so open `http://localhost:8000`
2. To utilize the functionality of the solution proceed to `http://localhost:8000/register` or `http://localhost:8000/login`
3. After successful registration/login, you can either host an event or register for an existing one.
4. Upon registering for an event you will be prompted to pay for the tickets via Revolut or any other banking system that provides a simple process such as QR codes.
5. If you are an event host, you can upload your bank statement in a `.csv` format to `http://localhost:8000/bank-statement/{event_id}` to check who expressed their interest and paid for the tickets.

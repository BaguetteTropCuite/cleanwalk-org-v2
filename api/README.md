# Cleanwalk V2 API

## Installation

Require python3

```shell
python3 -m pip install -r requirements.txt
```

## How to launch

You can launch the app via command line :

```shell
python3 app.py
```

or you can use your integrated python extension in your IDE.

## Tests

Go to your-domain/cleanwalks or your-domain/users

## API Client: use `Bruno`
https://www.usebruno.com/downloads

### config collection
- open collection --> "api-client" folder in cleanwalk repo
- select environement and add secrets variables like email token api-key ... . https://docs.usebruno.com/secrets-management/secret-variables


## API Routes Documentation - Users

### Authentication

#### 1. [POST] Login

- **Route:**

```bash
/users/login
```

- **Description:** Log in by providing a valid email and password.

- **Example:**

```json
{
  "email": "frin.arthur@gmail.com",
  "password": "azerty"
}
```

#### 2. [POST] Token Login

- **Route:**

```bash
/users/token-login
```

- **Description:** Log in using a valid JWT token (obtained from the login route).
- **Note:** Requires adding the JWT token to the request headers (bearer token).

### Users

#### 3. [GET] Get User by ID

- **Route:**

```bash
/users/:user_id
```

- **Description:** Retrieve details of a specific user by providing their ID.
- **Note:** Requires adding the JWT token to the request headers to access this route.

#### 4. [GET] Get All Users

- **Route:**

```bash
/users
```

- **Description:** Retrieve all registered users.
- **Note:** Requires adding the JWT token to the request headers to access this route.

#### 5. [POST] User Creation

- **Route:**

```bash
/users
```

- **Description:** Create a new user by providing the required information.
- **Example:**
- **Note:** role_id: 1 == user | 2 == organization

```json
{
  "firstname": "Arthur",
  "lastname": "Frin",
  "email": "frin.arthur@gmail.com",
  "password": "azerty",
  "profile_picture": "image_url",
  "role_id": 1
}
```

#### 6. [DELETE] Delete User by ID

- **Route:**

```bash
/users/:user_id
```

- **Description:** Delete a specific user by providing their ID.
- **Note:** Requires adding the JWT token to the request headers to access this route.

#### 7. [PUT] Update User by ID

- **Route:**

```bash
/users/:user_id
```

- **Description:** Update information for a specific user by providing their ID.
- **Example:**

```json
{
  "firstname": "New first name",
  "lastname": "New last name",
  "email": "new.email@example.com",
  "profile_picture": "new_image_url"
}
```

## API Routes Documentation - Cleanwalks

### Cleanwalks

#### 1. [GET] Get Cleanwalk by ID

- **Route:**

  ```bash
  /cleanwalks/<int:cleanwalk_id>
  ```

- **Description:** Retrieve details of a specific Cleanwalk by providing its ID.
- **Note:** Requires adding a valid API key to the request headers.

#### 2. [GET] Get All Cleanwalks

- **Route:**

  ```bash
  /cleanwalks
  ```

- **Description:** Retrieve information for all registered Cleanwalks.
- **Note:** Requires adding a valid API key to the request headers.

#### 3. [POST] Create Cleanwalk

- **Route:**

  ```bash
  /cleanwalks
  ```

- **Description:** Create a new Cleanwalk by providing the required information.
- **Example:**

  ```json
  {
    "name": "City Cleanup",
    "pos_lat": 40.7128,
    "pos_long": -74.0060,
    "date_begin": "2024-01-15",
    "duration": 2,
    "description": "Community cleanup event",
    "city_id": 1,
    "address": "123 Main St"
  }
  ```

#### 4. [PUT] Update Cleanwalk by ID

- **Route:**

  ```bash
  /cleanwalks/<int:cleanwalk_id>
  ```

- **Description:** Update information for a specific Cleanwalk by providing its ID.
- **Example:**

  ```json
  {
    "name": "Updated Cleanup",
    "pos_lat": 40.7128,
    "pos_long": -74.0060,
    "date_begin": "2024-01-20",
    "duration": 3,
    "description": "Updated community cleanup event",
    "city_id": 1,
    "address": "456 Main St"
  }
  ```

  Requires adding a valid API key to the request headers.

#### 5. [DELETE] Delete Cleanwalk by ID

- **Route:**

  ```bash
  /cleanwalks/<int:cleanwalk_id>
  ```

- **Description:** Delete a specific Cleanwalk by providing its ID.
- **Note:** Requires adding a valid API key to the request headers.

---

### Cities

#### 1. [GET] Get City by ID

- **Route:**

  ```bash
  /cities/<int:city_id>
  ```

- **Description:** Retrieve details of a specific city by providing its ID.
- **Note:** Requires adding a valid API key to the request headers.

#### 2. [GET] Get All Cities

- **Route:**

  ```bash
  /cities
  ```

- **Description:** Retrieve information for all registered cities.
- **Note:** Requires adding a valid API key to the request headers.

#### 3. [POST] Create City

- **Route:**

  ```bash
  /cities
  ```

- **Description:** Create a new city by providing the required information.
- **Example:**

  ```json
  {
    "name": "New City"
  }
  ```

#### 4. [PUT] Update City by ID

- **Route:**

  ```bash
  /cities/<int:city_id>
  ```

- **Description:** Update information for a specific city by providing its ID.
- **Example:**

  ```json
  {
    "name": "Updated City"
  }
  ```
  
  Requires adding a valid API key to the request headers.

#### 5. [DELETE] Delete City by ID

- **Route:**

  ```bash
  /cities/<int:city_id>
  ```

- **Description:** Delete a specific city by providing its ID.
- **Note:** Requires adding a valid API key to the request headers.

---

### Articles

#### 1. [GET] Get Article by ID

- **Route:**

  ```bash
  /articles/<int:article_id>
  ```

- **Description:** Retrieve details of a specific article by providing its ID.
- **Note:** Requires adding a valid API key to the request headers.

#### 2. [GET] Get All Articles

- **Route:**

  ```bash
  /articles
  ```

- **Description:** Retrieve information for all registered articles.
- **Note:** Requires adding a valid API key to the request headers.

#### 3. [POST] Create Article

- **Route:**

  ```bash
  /articles
  ```

- **Description:** Create a new article by providing the required information.
- **Example:**

  ```json
  {
    "title": "New Article",
    "author_id": 1,
    "description": "Article description",
    "content": "Article content"
  }
  ```

#### 4. [PUT] Update Article by ID

- **Route:**

  ```bash
  /articles/<int:article_id>
  ```

- **Description:** Update information for a specific article by providing its ID.
- **Example:**

  ```json
  {
    "title": "Updated Article",
    "description": "Updated article description",
    "content": "Updated article content"
  }
  ```

  Requires adding a valid API key to the request headers.

#### 5. [DELETE] Delete Article by ID

- **Route:**

  ```bash
  /articles/<int:article_id>
  ```

- **Description:** Delete a specific article by providing its ID.
- **Note:** Requires adding a valid API key to the request headers.

---

**Note:** Make sure to include a valid API key in the request headers for routes that require authentication. The API key can be obtained and validated through the `X-API-Key` header.

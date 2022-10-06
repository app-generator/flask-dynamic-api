# Flask Dynamic API via `Flask-RestX`

This tool aims to provide a secure, `production-ready API via Flask-RestX` using the developer's minimum amount of code. For newcomers, **Flask** is a leading backend framework used to code from simple websites and API's to complex eCommerce solutions.

Flask-RestX is a popular library for developing secure API services using Flask.

- 👉 Free [support](https://appseed.us/support/) via Email and [Discord](https://discord.gg/fZC6hup)
- 👉 More [Developer Tools](https://appseed.us/developer-tools/) - provided by AppSeed

<br />

## Video Presentation

https://user-images.githubusercontent.com/51070104/194328733-3bdf8c70-f765-4168-983d-2a51e276239b.mp4

<br />

## How it works

The **Dynamic API** tool aims to enable a secured API service on top of any Flask codebase with a minimum effort. Here are the steps:

- `Define a new model` in the project (an old one can be also used)
- `Execute the database migration` to create/update the associated tables
- `Update the configuration` to enable the Dynamic API over the model
- `Start the app`
- Access the `Dynamic API Service`

For instance, if the new model managed by the Dynamic API is called books, the associate API is exposed at /api/books/

<br />

| Status | Item | info | 
| --- | --- | --- |
| ✅ | New Models Definition in `apps/models` | - |
| ✅ | The app is saved in `apps/dyn_api` | - |
| ✅ | Models enabled in `apps/config.py` via `DYNAMIC_API` variable | - |
| ✅ | The project exposes automatically a CRUD API over the new model | - |
| ✅ | Path of the service: `/api/books/` | In case the new model is `Books` | 
| ✅ | The API is powered via Flask-RestX using best practices | - | 

<br />

## API Permissions

Before using the API, the user must make a request to the `/login' endpoint and send his username and password.:

```json
POST /login
{
  "username": "my_username",
  "password": "my_password"
}
```

The server returns a token if approved.

```json
{
  "token": "RETURNED_TOKEN"
}
```

To use the features, the user must add a key and value to the headers.

headers of requests:
```json
{
  ...
  "Authorization": "token RETURNED_TOKEN"
  ...
}
```
**Note:** token will be expired after 24 hours.

<br />

---
**Flask Dynamic API** via `Flask-RestX` - Developer tool provided by [AppSeed](https://appseed.us)

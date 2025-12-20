from fastapi import FastAPI, Cookie, Request, Response
from utild import utils
from fastapi.responses import JSONResponse, RedirectResponse
import json
import base64

app = FastAPI()


@app.post("/authenticate/signup")
def create_user(data: utils.AuthBody, response: Response):
    username = data.username
    password = data.password

    refresh_token = utils.generate_jwt_token(username, 60)
    access_token = utils.generate_jwt_token(username, 15)

    utils.create_user(username, password, refresh_token)

    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return {"Created user"}


@app.post("/authenticate/login")
def update_refresh_token(data: utils.AuthBody, request: Request, response: Response):
    username = data.username
    password = data.password

    if not utils.validate_user(username, password):
        return {"Invalid password"}

    refresh_token = utils.generate_jwt_token(username, 60)
    access_token = utils.generate_jwt_token(username, 15)

    utils.update_refresh_token(username, password, refresh_token)
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return {"Logged in successfully"}

    # This redirect can be used to login the user after the refresh token has been setup
    return RedirectResponse(url="/authenticate/renew_access_token", status_code=302)


@app.get("/authenticate/authenticate_using_access_token")
def authenticate_using_access_token(access_token: str = Cookie(None)) -> dict:
    validity = utils.validate_jwt_token(access_token)
    if validity == -2:
        print("here")
        return RedirectResponse(url="/authenticate/renew_access_token", status_code=302)

    elif validity == -1:
        return RedirectResponse(
            url="/authenticate/login", status_code=302
        )

    else:
        return JSONResponse(content={}, headers={"X-Status-Code": "200"})


@app.get("/authenticate/renew_access_token")
def renew_access_token(response: Response, access_token: str = Cookie(None)):
    refresh_token = utils.get_refresh_token()

    if refresh_token == 0:
        return RedirectResponse(
            url="/authenticate/login", status_code=302
        )

    user_data_decoded = json.loads(base64.b64decode(access_token).decode())

    new_access_token = utils.generate_jwt_token(user_data_decoded.username, 15)
    response.set_cookie(key="access_token", value=new_access_token, httponly=True)

    return JSONResponse(content={}, headers={"X-Status-Code": "200"})

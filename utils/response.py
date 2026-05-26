from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder



def success_response(massage: str = "success", data= None):
    content = {
        "code": 200,
        "message": massage,
        "data": data
    }

    return JSONResponse(content = jsonable_encoder(content), status_code=200)
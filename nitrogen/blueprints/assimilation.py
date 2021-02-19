from assimilation.classification import predict
import nitrogen.boundary.storage as storage
import nitrogen.boundary.web_server as web


bp = web.Blueprint("Assimilation", "/assimilation")


# Simple param based request ===========================================================


@bp.route("/validate-answer", methods=["POST"])
@web.doc.summary("Check for the ultimate answer to life, the universe and everything")
@web.doc.consumes(
    web.doc.JsonBody({"answer": web.doc.Integer("Correct answer is 42.")}),
    location="body",
    content_type="application/json",
)
@web.doc.response(200, {"valid?": bool, "status": str}, description="Valid request")
@web.doc.response(400, {"valid?": False, "error": str}, description="Invalid request")
async def validate_answer_json(request):
    try:
        answer = request.json["answer"]
    except:
        return web.response.json(
            {"valid?": False, "error": "No 'answer' key in JSON"}, 400
        )
    try:
        number = int(answer)
    except Exception as e:
        return web.response.json(
            {"valid?": False, "error": "Cannot cast answer to int"}, 400
        )
    if number > 42:
        return web.response.json({"valid?": False, "status": "Answer is too high"})
    elif number < 42:
        return web.response.json({"valid?": False, "status": "Answer is too low"})
    return web.response.json({"valid?": True, "status": "Answer is correct!"})


@bp.route("/validate-answer/<number:int>", methods=["GET"])
@web.doc.summary("Check for the ultimate answer to life, the universe and everything")
@web.doc.response(200, {"valid?": bool, "status": str}, description="Valid request")
@web.doc.response(400, {"valid?": False, "error": str}, description="Invalid request")
async def validate_answer(request, number):
    try:
        number = int(number)
    except Exception as e:
        return web.response.json(
            {"valid?": False, "error": "Cannot cast answer to int"}, 400
        )
    if number > 42:
        return web.response.json({"valid?": False, "status": "Answer is too high"})
    elif number < 42:
        return web.response.json({"valid?": False, "status": "Answer is too low"})
    return web.response.json({"valid?": True, "status": "Answer is correct!"})


# Fancy ML service =====================================================================


@bp.route("/cat-or-dog/local/", methods=["POST"])
@web.doc.summary("Dogs goes 'Woof'.")
@web.doc.consumes(
    web.doc.JsonBody({"file": web.doc.String("Path to a local file.")}),
    location="body",
    content_type="application/json",
)
@web.doc.response(
    200,
    {"prediction": str, "probability": float},
    description="Predicition with the highest probability.",
)
@web.doc.response(400, {"error": str}, description="Invalid request")
@web.doc.response(500, {"error": str}, description="Internal error during prediction.")
async def classify_local_json(request):
    try:
        imagename = request.json["file"]
    except:
        return web.response.json({"error": "No 'file' key in JSON"}, 400)
    try:
        image_path = storage.local_image_path(imagename)
    except Exception as e:
        return web.response.json({"error": f"Cannot open file as image. {e}"}, 400)
    try:
        prediction = predict(image_path)
    except Exception as e:
        return web.response.json({"error": f"Coudn't process the file. {e}"}, 500)
    return web.response.json(prediction)


@bp.route("/cat-or-dog/local/<imagename:string>", methods=["GET"])
@web.doc.summary("Cat goes 'Meow'")
@web.doc.response(
    200,
    {"prediction": str, "probability": float},
    description="Predicition with the highest probability.",
)
@web.doc.response(400, {"error": str}, description="Invalid request")
@web.doc.response(500, {"error": str}, description="Internal error during prediction.")
async def classify_local(request, imagename):
    try:
        image_path = storage.local_image_path(imagename)
    except Exception as e:
        return web.response.json({"error": f"Cannot open file as image. {e}"}, 400)
    try:
        prediction = predict(image_path)
    except Exception as e:
        return web.response.json({"error": f"Coudn't process the file. {e}"}, 500)
    return web.response.json(prediction)


@bp.route("/cat-or-dog/s3/", methods=["POST"])
@web.doc.summary("Bird goes 'Tweet'.")
@web.doc.consumes(
    web.doc.JsonBody({"imagename": web.doc.String("S3 object key.")}),
    location="body",
    content_type="application/json",
)
@web.doc.response(
    200,
    {"prediction": str, "probability": float},
    description="Predicition with the highest probability.",
)
@web.doc.response(400, {"error": str}, description="Invalid request")
@web.doc.response(500, {"error": str}, description="Internal error during prediction.")
async def classify_s3_json(request):
    try:
        obj_key = request.json["imagename"]
    except:
        return web.response.json({"error": "No 'imagename' key in JSON"}, 400)
    try:
        image_path = storage.cloud_image(obj_key)
    except Exception as e:
        return web.response.json({"error": f"Cannot open file as image. {e}"}, 400)
    try:
        prediction = predict(image_path)
    except Exception as e:
        return web.response.json({"error": f"Coudn't process the file. {e}"}, 500)
    return web.response.json(prediction)


@bp.route("/cat-or-dog/s3/<imagename:string>", methods=["GET"])
@web.doc.summary("What does the fox say?")
@web.doc.response(
    200,
    {"prediction": str, "probability": float},
    description="Predicition with the highest probability.",
)
@web.doc.response(400, {"error": str}, description="Invalid request")
@web.doc.response(500, {"error": str}, description="Internal error during prediction.")
async def classify_s3(request, imagename):
    try:
        image = storage.cloud_image(imagename)
    except Exception as e:
        return web.response.json({"error": f"Cannot open file as image. {e}"}, 400)
    try:
        prediction = predict(image)
    except Exception as e:
        return web.response.json({"error": f"Coudn't process the file"}, 500)
    return web.response.json(prediction)

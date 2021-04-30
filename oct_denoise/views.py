from django.http import JsonResponse, FileResponse, Http404, HttpResponseNotFound
import tensorflow as tf
import os
import uuid
import time
import datetime

from oct_denoise.models import UploadModel, UploadForm, UserModel, SigninForm, SignupForm, UserAuthModel

model = tf.keras.models.load_model("generator_g")


def denoise(uf, rf):
    img = tf.image.decode_image(tf.io.read_file(uf))
    img = tf.reshape(img, (1, 256, 256, 1))
    img = tf.cast(img, dtype=tf.float32)
    img = tf.divide(tf.add(img, -127.5), 127.5)

    r = model(img)

    r = tf.reshape(r, (256, 256, 1))
    r = tf.add(tf.multiply(r, 127.5), 127.5)
    r = tf.cast(r, dtype=tf.uint8)
    tf.io.write_file(rf, tf.image.encode_png(r))


def to_mills(d: datetime.datetime) -> int:
    this_time = time.mktime(d.timetuple())
    return int(this_time)


def upload_images(request):
    """result
    POST
    :return: { status: ok | error, uid: string }
    """
    if request.method == "POST":
        r = {
            "status": "err",
        }
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            f: UploadModel = form.save(commit=False)
            file_name = str(uuid.uuid1()) + ".png"
            date_path = time.strftime("%Y/%m/%d", time.localtime())
            f_path = os.path.join(date_path, file_name)
            upload_path = os.path.join("upload", f_path)
            result_path = os.path.join("result", f_path)
            f.name = file_name
            f.file.name = upload_path
            f.path = f_path
            f.disable = False
            f.upload_path = upload_path
            f.result_path = result_path
            form.save()
            denoise(upload_path, result_path)
            r = {
                "status": "ok",
                "payload": {
                    "name": file_name,
                    "path": f_path,
                    "user_id": f.user_id,
                    "time": to_mills(f.uploaded_at),
                },
            }
        return JsonResponse(r)
    return


def image(request, p):
    if request.method == 'GET':
        tp = request.GET.get("type", default="result")
        fp = os.path.join(tp, p)
        try:
            res = FileResponse(open(fp, 'rb'))
            res['content_type'] = "image/png"
            return res
        except FileNotFoundError:
            return HttpResponseNotFound()
    if request.method == 'DELETE':
        fp = os.path.basename(p)
        try:
            q = UploadModel.objects.filter(name=fp)
            q.update(disable=True)
            return JsonResponse({
                "status": "ok"
            })
        except:
            return HttpResponseNotFound()
    return


def fetch_all(request, uid):
    if request.method == 'GET':
        r = {
            "status": "ok",
            "payload": [],
        }
        q = UploadModel.objects.filter(user_id=uid, disable=False)
        for i in q:
            r["payload"].append({
                "name": i.name,
                "path": i.path,
                "user_id": i.user_id,
                "time": to_mills(i.uploaded_at),
            })
        return JsonResponse(r)
    return


def sign_up(request, ):
    if request.method == "POST":
        r = {
            "status": "err",
            "payload": {
                "uid": "",
                "email": "",
            },
            "code": 400,
        }
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = UserModel(email=email)
            user_auth = UserAuthModel(email=email, password=password)
            try:
                user.save()
                user_auth.save()
                r = {
                    "status": "ok",
                    "payload": {
                        "uid": user.uid,
                        "email": user.email,
                    },
                    "code": 200,
                }
            except:
                r['code'] = 403
        else:
            r['code'] = 300
        return JsonResponse(r)
    return


def sign_in(request):
    if request.method == "POST":
        r = {
            "status": "err",
            "code": 400,
        }
        form = SigninForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                o: UserAuthModel = UserAuthModel.objects.get(email=email, password=password)
                r = {
                    "status": "ok",
                    "payload": {
                        "uid": o.uid,
                        "email": o.email,
                    },
                    "code": 200,
                }
            except:
                r["code"] = 404
        return JsonResponse(r)
    return

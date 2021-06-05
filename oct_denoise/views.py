from django.http import JsonResponse, FileResponse, HttpResponseNotFound
from oct_denoise.models import UploadModel, UploadForm, UserModel, SigninForm, SignupForm, UserAuthModel, \
    UserVerifyModel
from oct_denoise.email_verify import send_mail, generate_code
import os
import uuid
import time
import datetime
import oct_denoise.denoise as denoise


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
            file_name = str(uuid.uuid4()) + ".png"
            upload_path = os.path.join("upload", file_name)
            result_path = os.path.join("result", file_name)
            f.name = file_name
            f.file.name = file_name
            f.path = upload_path
            f.disable = False
            f.upload_path = upload_path
            f.result_path = result_path
            f = form.save(commit=True)
            try:
                denoise.denoise(upload_path, result_path)
                r = {
                    "status": "ok",
                    "payload": {
                        "name": file_name,
                        "path": file_name,
                        "token": f.token,
                        "time": to_mills(f.uploaded_at),
                    },
                }
            except:
                f.delete()
                r['status'] = "err"
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


def fetch_all(request):
    if request.method == 'GET':
        r = {
            "status": "ok",
            "payload": [],
        }
        token = request.GET.get("token", default="")
        q = UploadModel.objects.filter(token=token, disable=False)
        for i in q:
            r["payload"].append({
                "name": i.name,
                "path": i.path,
                "token": i.token,
                "time": to_mills(i.uploaded_at),
            })
        return JsonResponse(r)
    return


email_host = "smtp.qq.com"
email_user = "2891206380@qq.com"
email_pwd = "oaqyjkbbypyhdhef"


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
            try:
                user = UserModel(email=email)
                user.save()

                user_auth = UserAuthModel(uid=user.uid, email=email, password=password)
                user_auth.save()

                code = generate_code()

                user_verify = UserVerifyModel(uid=user.uid, email=email, code=code, verified=False)
                user_verify.save()

                email_content = "Your verify code is：%s" % code
                email_title = "Verify code"
                send_mail(
                    host=email_host,
                    user=email_user,
                    pwd=email_pwd,
                    receiver=email,
                    content=email_content,
                    title=email_title
                )
                r = {
                    "status": "ok",
                    "payload": {
                        "uid": user.uid,
                        "email": user.email,
                    },
                    "code": 200,
                }
            except Exception as e:
                r = {
                    "status": "err",
                    "payload": str(e),
                    "code": 403
                }
        return JsonResponse(r)
    return


def verify(request):
    if request.method == 'GET':
        r = {
            "status": "ok",
            "payload": {},
            "code": 404,
        }
        email = request.GET.get("email", default="")
        predict_code = request.GET.get("code", default="")
        try:
            q: UserVerifyModel = UserVerifyModel.objects.get(email=email, verified=False)
            if q.code == predict_code:
                q.verified = True
                q.save()
                user: UserModel = UserModel.objects.get(email=email)
                r = {
                    "status": "ok",
                    "payload": {
                        "uid": user.uid,
                        "email": user.email,
                    },
                    "code": 200,
                }
            else:
                r = {
                    "status": "err",
                    "payload": "error verify code",
                    "code": 403,
                }
        except Exception as e:
            r = {
                "status": "err",
                "payload": str(e),
                "code": 404,
            }
        return JsonResponse(r)
    pass


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
                user_auth: UserAuthModel = UserAuthModel.objects.get(email=email, password=password)
                user_verify: UserVerifyModel = UserVerifyModel.objects.get(email=email)
                if user_verify.verified:
                    r = {
                        "status": "ok",
                        "payload": {
                            "uid": user_auth.uid,
                            "email": user_auth.email,
                        },
                        "code": 200,
                    }
                else:
                    r = {
                        "status": "err",
                        "payload": {
                            "uid": user_auth.uid,
                            "email": user_auth.email,
                            "msg": "not verified"
                        },
                        "code": 403,
                    }
            except Exception as e:
                r = {
                    "status": "err",
                    "payload": str(e),
                    "code": 404,
                }
        return JsonResponse(r)
    return

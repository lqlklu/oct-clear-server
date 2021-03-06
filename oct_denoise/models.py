from django.db import models
from django import forms


class UploadModel(models.Model):
    name = models.CharField(max_length=256, default="filename")  # "a1b2c3d4e5f6.png" md5
    file = models.FileField(upload_to=".")  # file
    uploaded_at = models.DateTimeField(auto_now_add=True)  # time
    token = models.TextField(default="")
    path = models.CharField(max_length=256, default="")  # "2021/03/17/a1b2c3d4e5f6.png"
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['file', 'token']


class UserModel(models.Model):
    uid = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=256, unique=True)  # xxx@qq.com

    def __str__(self):
        return self.email


class UserAuthModel(models.Model):
    uid = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=256, unique=True)  # xxx@qq.com
    password = models.CharField(max_length=256, )  # abcdef

    def __str__(self):
        return self.email


class UserVerifyModel(models.Model):
    uid = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=8)
    verified = models.BooleanField(default=False)


class SigninForm(forms.Form):
    uid = forms.CharField()  # 6479
    email = forms.EmailField()  # xxx@qq.com
    password = forms.CharField()  # abcdef


class SignupForm(forms.Form):
    email = forms.EmailField()  # xxx@qq.com
    password = forms.CharField()  # abcdef

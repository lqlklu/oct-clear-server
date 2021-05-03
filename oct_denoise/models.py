from django.db import models
from django import forms


class UploadModel(models.Model):
    name = models.CharField(max_length=256, default="filename")  # "a1b2c3d4e5f6.png" md5
    file = models.FileField(upload_to=".")  # file
    uploaded_at = models.DateTimeField(auto_now_add=True)  # time
    user_id = models.BigIntegerField(default=0)  # 6479
    path = models.CharField(max_length=256, default="")  # "2021/03/17/a1b2c3d4e5f6.png"
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['file', 'user_id']


class UserModel(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.CharField(max_length=256, unique=True)  # xxx@qq.com

    def __str__(self):
        return self.email


class UserAuthModel(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.CharField(max_length=256, unique=True)  # xxx@qq.com
    password = models.CharField(max_length=256, )  # abcdef

    def __str__(self):
        return self.email


class SignupAuthModel(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=8)


class SigninForm(forms.Form):
    uid = forms.CharField()  # 6479
    email = forms.EmailField()  # xxx@qq.com
    password = forms.CharField()  # abcdef


class SignupForm(forms.Form):
    email = forms.EmailField()  # xxx@qq.com
    password = forms.CharField()  # abcdef

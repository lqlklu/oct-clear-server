FROM tensorflow/tensorflow:latest
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
# RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000


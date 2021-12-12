FROM python:3.8.12-slim-buster

RUN pip install mlflow cloudpickle==1.6.0 psutil==5.8.0 scikit-learn==0.24.1

WORKDIR /model 

COPY ./mlruns/1/0b9ccee72bb94801bcf3e4849196b6b7/artifacts/models/ .

EXPOSE 5000
CMD ["mlflow","models","serve","-m","./","-h","0.0.0.0","-p","5000","--no-conda"]
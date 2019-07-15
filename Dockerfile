FROM python:3.7-slim
WORKDIR /Calculator
COPY . /Calculator
RUN pip3 install flask
EXPOSE 80
CMD ["python3", "pythonCalc.py"]

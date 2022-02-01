FROM python:3.8-buster

COPY ./ /py_xmlasdict
WORKDIR /py_xmlasdict

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python setup.py install

ENTRYPOINT ["py_xmlasdict"]

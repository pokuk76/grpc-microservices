FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs
COPY marketplace/ service/marketplace
WORKDIR /service/marketplace
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/recommendations.proto

EXPOSE 5000
ENV FLASK_APP=marketplace.py
# Tell flask to accept connections from anywhere
# b/c localhost inside the Docker container is different from localhost on the host machine
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]
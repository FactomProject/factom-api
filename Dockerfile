FROM bhomnick/python-multi
ENV PYTHONUNBUFFERED 1
RUN apt-get update -yy && apt-get install -q -y pandoc
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN bash -lc "pip3.6 install -r requirements.txt"

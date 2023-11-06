FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /usr/app

RUN pip install --upgrade pip
COPY requirements/ /requirements/
RUN pip install -r requirements/dev.txt

# RUN addgroup --gid 1001 --system app && \
#     adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app
# USER app

WORKDIR /usr/app

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh

COPY . /usr/app

ENTRYPOINT [ "./entrypoint.sh" ]

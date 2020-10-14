FROM python:3.7.4-alpine
ENV PATH="/scripts:${PATH}"
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp
RUN mkdir quizoo
COPY ./quizoo /quizoo
RUN chmod -R 777 /quizoo
WORKDIR /quizoo
COPY ./scripts /scripts
RUN chmod +x /scripts/*
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 777 /vol/web
USER user
CMD ["entrypoint.sh"]
FROM ubuntu:18.04
ENV PATH="/scripts:${PATH}"
COPY ./requirements.txt /requirements.txt
RUN apt-get update
RUN apt-get -y install python3-pip
RUN pip3 install -r /requirements.txt
RUN mkdir quizoo
COPY ./quizoo /quizoo
RUN chmod -R 777 /quizoo
WORKDIR /quizoo
COPY ./scripts /scripts
RUN chmod +x /scripts/*
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser user
RUN chown -R user:user /vol
RUN chmod -R 777 /vol/web
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -qq install tzdata
RUN apt-get -qq install systemd
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -qq install apt-utils
RUN apt-get update
RUN apt-get install cron
RUN apt-get install nano
CMD ["entrypoint.sh"]

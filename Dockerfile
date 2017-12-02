FROM webdevops/apache:ubuntu-16.04

RUN apt-get clean
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3 python3-urllib3 python3-lxml python3-requests python3-bs4 locales tzdata cron
RUN locale-gen de_DE.UTF-8
ENV LANG='de_DE.UTF-8' LANGUAGE='de_DE.UTF-8' LC_ALL='de_DE.UTF-8'
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

RUN sed -i "$ d" /etc/crontab
RUN echo "15 *    * * *   root    cd /scripts/ && python3 main.py" >> /etc/crontab
RUN echo "#"  >> /etc/crontab
RUN /etc/init.d/cron start

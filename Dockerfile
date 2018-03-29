FROM webdevops/apache:ubuntu-16.04

RUN apt-get clean && apt-get update && apt-get upgrade -y && apt-get install -y python3 python3-dev python3-pip locales tzdata cron
RUN locale-gen de_DE.UTF-8
ENV LANG='de_DE.UTF-8' LANGUAGE='de_DE.UTF-8' LC_ALL='de_DE.UTF-8'
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime && dpkg-reconfigure -f noninteractive tzdata
RUN pip3 install setuptools pip --upgrade --force-reinstall
RUN pip3 install requests ebird-api lxml urllib3
RUN sed -i "$ d" /etc/crontab
RUN echo "15 *    * * *   root    cd /scripts/ && python3 main.py" >> /etc/crontab
RUN echo "#"  >> /etc/crontab
RUN /etc/init.d/cron start

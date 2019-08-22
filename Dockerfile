FROM webdevops/apache:ubuntu-16.04

RUN apt-get clean && apt-get update && apt-get upgrade -y && apt-get install -y python3 python3-dev python3-pip locales tzdata
RUN locale-gen de_DE.UTF-8
ENV LANG='de_DE.UTF-8' LANGUAGE='de_DE.UTF-8' LC_ALL='de_DE.UTF-8'
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime && dpkg-reconfigure -f noninteractive tzdata
RUN pip3 install setuptools pip --upgrade --force-reinstall
RUN pip3 install requests ebird-api lxml urllib3 bs4 xlrd
RUN echo "#!/bin/bash" >> /root/start.sh
RUN echo "cd /scripts/" >> /root/start.sh
RUN echo "python3 main.py" >> /root/start.sh
RUN echo "sleep 3600" >> /root/start.sh
RUN chmod +x /root/start.sh
ENTRYPOINT ["/root/start.sh"]

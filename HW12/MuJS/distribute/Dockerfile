FROM ubuntu:focal
MAINTAINER James

RUN apt-get update
RUN apt-get install xinetd libbsd-dev -qy
RUN useradd -m MuJS
RUN chown -R root:root /home/MuJS
RUN chmod -R 755 /home/MuJS

CMD ["/usr/sbin/xinetd","-dontfork"]

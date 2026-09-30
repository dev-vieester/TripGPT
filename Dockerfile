FROM ubuntu:latest
LABEL authors="user pc"

ENTRYPOINT ["top", "-b"]
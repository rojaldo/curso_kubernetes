FROM ubuntu:25.04 AS compiler
RUN apt-get update
RUN apt-get install -y build-essential
COPY hello.c /
RUN make hello

FROM alpine:latest
# import dependency to run the hello program
LABEL maintainer="rojaldo"
LABEL description="A simple hello world program in C"
LABEL version="1.0"
EXPOSE 8080
RUN apk add --no-cache libc6-compat
COPY --from=compiler /hello /hello
# change user to non-root
USER 1000:1000
# run the hello program
CMD ["/hello"]
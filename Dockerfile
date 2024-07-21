FROM tomcat:9-jdk11-openjdk-slim


RUN apt-get update && apt-get install -y git maven


RUN git clone https://github.com/boxfuse/boxfuse-sample-java-war-hello.git /usr/local/tomcat/webapps/hello

WORKDIR /usr/local/tomcat/webapps/hello


RUN mvn package


RUN cp target/*.war /usr/local/tomcat/webapps/



EXPOSE 8080
<<<<<<< HEAD
    ################ это внизу писать не надо так как это есть в образе (1 строчка)####################
CMD ["catalina.sh", "run"]
=======

>>>>>>> 5477c555e3d2ed60934365ae9d08ead06d9bfb7d

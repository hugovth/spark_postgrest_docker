FROM python:3.7.3
COPY ./resources /opt


ENV SPARK_VERSION 3.0.1
ENV SPARK_HADOOP_PROFILE 2.7
ENV SPARK_SRC_URL https://www.apache.org/dist/spark/spark-$SPARK_VERSION/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE}.tgz
ENV SPARK_HOME=/opt/spark
ENV PATH $PATH:$SPARK_HOME/bin

RUN wget ${SPARK_SRC_URL}
RUN tar -xzf spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE}.tgz

RUN mv spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE} /opt/spark
RUN rm -f spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE}.tgz

RUN apt-get update
RUN apt-get install -y openjdk-8-jdk-headless postgresql 
RUN rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME  /usr/lib/jvm/java-8-openjdk-amd64/

ENV POST_URL https://jdbc.postgresql.org/download/postgresql-42.2.5.jar

RUN wget ${POST_URL}
RUN mv postgresql-42.2.5.jar /opt/spark/jars
RUN pip install --no-cache-dir -r /opt/requirement.txt
WORKDIR "/opt"
CMD [ "python", "./script.py" ]
# ENTRYPOINT ["entrypoint.sh"]


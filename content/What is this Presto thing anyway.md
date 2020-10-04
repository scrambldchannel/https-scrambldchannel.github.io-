Title: First steps with Presto
Date: 2020-08-29 10:26
Category: presto
Tags: presto, sql
slug: presto-first-steps
Authors: Alexander
Summary: An overview of Presto for absolute beginners
Status: draft

As part of my job search here in Berlin I have been exploring the tech radars of potential employers. Focussing on their data stacks, I've been trying to draw up a hitlist of the different technologies they are actively adopting. One of the tools that comes up regularly is Presto. I've done some work with it but when asked by a colleague to explain what it was good for, I struggled to give her a succinct answer. So I thought I'd try to write a simple introduction aimed at newcomers so that I could give a better answer next time.

### So what is it? 

[Presto](https://prestodb.io/) is "Presto is an open source distributed SQL query engine for running interactive analytic queries against data sources of all sizes ranging from gigabytes to petabytes." So it's clear the Presto is designed for use with really big datasets. It is also designed for analysts who want to run ad hoc queries against data stored in a variety of locations. Most importantly, they want to be able to run these queries fast. In this sense it is geared towards exploratory analysis rather than productionising pipelines where you might be more likely to use something like Spark. It was created at Facebook and they released it as open source in 2013. It was intended as a replacement for Apache Hive. 


### So what data can it connect to and how? 

Presto is designed to run SQL queries in a distributed environment. It can integrate with a number of backends and a single query can join together data from multiple sources. For example, you can create a query that joins a table in a postgresql database with a table in an MySQL database. Furthermore, it can connect to no SQL databases such as MongoDB (how does this work?) POresumably some metadata is defined somewhere). It comes bundled with many connectors out of the bo but can be extended by writing custom connectors using Java. If you don't like Java you can write something called a Thrift connector (what is this?)

### How do I interact with it?

There is a CLI but also through languages like Python so it can be used in Jupyter notebooks for example. 
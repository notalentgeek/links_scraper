# Links Scraper

## Overview

The Links Scraper is a project designed to scrape all URLs available on a specified website using Selenium. It was developed as part of an assignment for a job application. The project demonstrates the ability to handle URL scraping efficiently and provides a design for scaling the infrastructure to handle high-volume scraping tasks.

## Objectives

1. **Scrape URLs:** Scrape at least 1,000 URLs from a given website.
1. **Scalable Design:** Propose a scalable infrastructure capable of scraping up to 2 million URLs per day.

## Implementation

### Current Solution

* Programming Language: Python
* Web Scraping: Selenium for interacting with websites and extracting URLs.

### Proposed Scalable Design

An event-driven architecture powered by Apache Kafka to handle high-volume scraping tasks with the following components:

* Apache Kafka: Serves as the messaging backbone for event-driven communication.
* Producer Service:
  * Written in Python with Selenium.
  * Handles URL scraping from websites and sends data to Kafka topics.
* Consumer-Producer Services:
  * Intermediate processing layer.
  * Consumes messages from Kafka topics, performs any required processing, and produces new events for downstream consumers.
* Database:
  * Stores scraped URLs and metadata.
  * Currently uses PostgreSQL for relational data storage.
  * Can be upgraded to a NoSQL solution for better scalability.

## Limitations and Considerations

* Headless Mode Challenges:
  * Headless Selenium often triggers anti-bot systems.
  * While anti-bot evasion is possible with specific configurations, identifying optimal settings for each target website is time-intensive.
  * For simplicity, this implementation uses non-headless mode.
* Database Choice:
  * PostgreSQL is used for simplicity and familiarity.
  * For large-scale operations, a NoSQL database like MongoDB or Cassandra may be more suitable.
* Scalability and Deployment:
  * Currently, the implementation runs locally using the developer's laptop as a VNC server.
  * For production, consider deploying the solution in Docker containers with a cloud-based VNC server for enhanced scalability and reliability.
* Alternative Technologies:
  * While this implementation uses Apache Kafka, Google Pub/Sub could be a simpler and more managed alternative for cloud-based setups.

## Design Diagram

![Design Diagram](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/notalentgeek/links_scraper/master/umls/design_diagram.uml)

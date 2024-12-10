# URLs Scraper

## Overview

The URLs Scraper is a project designed to scrape all URLs available on a specified website using Selenium. It was developed as part of an assignment for a job application. The project demonstrates the ability to handle URL scraping efficiently and provides a design for scaling the infrastructure to handle high-volume scraping tasks.

## Objectives

1. **Scrape URLs:** Scrape at least 1,000 URLs from a given website.
2. **Scalable Design:** Propose a scalable infrastructure capable of scraping up to 2 million URLs per day.

## Implementation

### Current Solution

* **Programming Language:** Python
* **Web Scraping:** Selenium for interacting with websites and extracting URLs.

### Proposed Scalable Design

An event-driven architecture powered by Apache Kafka to handle high-volume scraping tasks with the following components:

* **Apache Kafka:** Serves as the messaging backbone for event-driven communication.
* **Producer Service:**
  * Written in Python with Selenium.
  * Handles URL scraping from websites and sends data to Kafka topics.
* **Consumer-Producer Services:**
  * Intermediate processing layer.
  * Consumes messages from Kafka topics, performs any required processing, and produces new events for downstream consumers.
* **Database:**
  * Stores scraped URLs and metadata.
  * Currently uses MongoDB for storing data in a scalable manner.

## Limitations and Considerations

* **Headless Mode Challenges:**
  * Headless Selenium often triggers anti-bot systems.
  * While anti-bot evasion is possible with specific configurations, identifying optimal settings for each target website is time-intensive.
  * For simplicity, this implementation uses non-headless mode.
* **Database Choice:**
  * MongoDB is used for scalability and efficiency in handling large datasets.
* **Scalability and Deployment:**
  * Currently, the implementation runs locally using the developer's laptop as a VNC server.
  * For production, consider deploying the solution in Docker containers with a cloud-based VNC server for enhanced scalability and reliability.
* **Alternative Technologies:**
  * While this implementation uses Apache Kafka, Google Pub/Sub could be a simpler and more managed alternative for cloud-based setups.

## Running the Services

To run the services, follow these steps:

1. **Download ChromeDriver and save it in the `bin` directory.**
2. **Build and start the services using Docker Compose**:
    ```bash
    docker-compose up -d --build
    ```

    This will build the necessary Docker images and start the services in the background. The following services will be created:
    - **Kafka**: Messaging service for communication between the producer and consumer services.
    - **MongoDB**: Stores the scraped URLs and metadata.
    - ~~**Python Producer Service**: Executes Python scripts that periodically send messages to the messaging service.~~

3. **Run the Python consumer-producer service**:
    After starting the services, run the Python script to start processing the scraped URLs. You can specify the number of producer process and consumer-producer processes you want to run. For examples:

    ```bash
    python3 main.py --producer=1 --conprod=3
    ```

    This command will launch **1 producer process and 3 consumer-producer processes**.

    ```bash
    python3 main.py --conprod=3 --same-domain-name
    ```

    This command will launch **3 consumer-producer processes**.

    You can customize the number based on the scale of your scraping task. By default, running the `python3 main.py` command starts a single producer service and one consumer-producer service.

## Design Diagram

![Design Diagram](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/notalentgeek/links_scraper/refs/heads/master/umls/design_diagram.uml)

## Example Result From MongoDB

```text
[
  {
    _id: ObjectId('67579d8bb5fd82c778c6f503'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://syopi.tw/buyer/login/otp?next=https%3A%2F%2Fsyopi.tw%2F'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f504'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://careers.syopi.com/jobs'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f505'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://linkedin.com/company/syopi'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f506'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://syopi.com.br/'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f507'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://help.syopi.tw/portal/article/79725-[%e8%81%af%e7%b5%a1%e5%ae%a2%e6%9c%8d]-%e5%a6%82%e4%bd%95%e8%81%af%e7%b5%a1%e8%9d%a6%e7%9a%ae%e5%ae%a2%e6%9c%8d%3F'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f508'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://syopi.vn/'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f509'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://help.syopi.tw/portal/article/77266'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f50a'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://syopi.tw/m/Anti-fraud-advocacy'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f50b'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://careers.syopi.com/about/'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f50c'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://help.syopi.tw/portal/article/80020-[%E8%A8%82%E5%96%AE%E4%BF%9D%E9%9A%9C]-%E4%BB%80%E9%BA%BC%E6%98%AF%E5%BB%B6%E9%95%B7%E8%A8%82%E5%96%AE%E6%92%A5%E6%AC%BE'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f50d'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://syopi.tw/mall/'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f50e'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://syopi.com.co/'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f50f'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://help.syopi.tw/portal/article/79770-[%E8%9D%A6%E7%9A%AE%E9%8C%A2%E5%8C%85]-%E4%BB%80%E9%BA%BC%E6%98%AF%E8%9D%A6%E7%9A%AE%E9%8C%A2%E5%8C%85'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f510'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://page.line.me/syopi?openQrModal=true'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f511'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://help.syopi.tw/tw/s'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f512'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://syopi.co.th/'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f513'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://help.syopi.tw/portal/article/80089-[%E6%96%B0%E6%89%8B%E4%B8%8A%E8%B7%AF]-%E8%9D%A6%E7%9A%AE%E8%B3%BC%E7%89%A9%E6%94%AF%E6%8F%B4%E5%93%AA%E4%BA%9B%E4%BB%98%E6%AC%BE%E6%96%B9%E5%BC%8F%E8%88%87%E4%BB%98%E6%AC%BE%E9%87%91%E9%A1%8D%E4%B8%8A%E9%99%90?'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f514'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://syopi.com.mx/'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f515'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://syopi.com.my/'
  },
  {
    _id: ObjectId('67579d8bb5fd82c778c6f516'),
    retrieved_url: 'https://syopi.tw',
    found_url: 'https://syopi.tw/buyer/signup?next=https%3A%2F%2Fsyopi.tw%2F'
  }
]
```

## Appendixes

### Appendix A: Accessing MongoDB

```console
docker-compose exec mongo bash

# In MongoDB Container
mongosh -u username -p password --authenticationDatabase admin

# In Mongosh Shell
use urls_scraper;
db.urls.find();
```

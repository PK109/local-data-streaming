# 🔄 Change Data Capture System with Real-Time Analytics

## 📖 Overview
This project is a **Change Data Capture (CDC) System** designed to demonstrate real-time data processing and analytics capabilities. It leverages streaming technologies to monitor database changes, transform the data, and provide insights in real time.

The system highlights data engineering concepts such as event-driven architectures, fault tolerance, and latency management using watermarks. It is built to handle real-world scenarios efficiently and effectively.

---

## ✨ Features
- 📡 **Real-Time Data Capture**: Monitors changes in a PostgreSQL database and streams them as events.
- ⚙️ **Event Processing with Flink**: Processes and analyzes data streams, applying transformations and basic analytics.
- 🛡️ **Fault Tolerance**: Uses Kafka's three-broker setup to ensure high availability. Utilizes Flink's Restart strategy to ensure stable data flow. 
- 🔍 **Custom Health Checks and Scheduling**: Enhances Docker Compose orchestration reliability.
- 📊 **Real-Time Dashboards**: Streams processed data back to the database for visualization.

---

## 🛠️ Architecture
1. **Data Ingestion**: A Python worker ingests data into a PostgreSQL database.  
2. **Change Data Capture**: Debezium, integrated with Kafka Connect, converts database changes into Kafka events.  
3. **Stream Processing**: Apache Flink processes Kafka events, applying transformations and analytics.  
4. **Output Pipelines**: The processed data is sent back to Kafka topics and stored in a database for dashboard consumption.  

![Architecture Diagram Placeholder](#)

---

## 🚀 Key Technologies
- **PostgreSQL**: Initial data storage.  
- **Kafka & Kafka Connect**: Core of the event streaming platform.  
- **Debezium**: Change Data Capture integration.  
- **Apache Flink**: Stream processing and real-time analytics.  
- **Docker Compose**: Orchestration of all system components.  
- **Python**: Custom scripts for data ingestion and orchestration.  

---

## 💡 Why This Project?
This project was developed to:  
- 🧑‍💻 Expand my portfolio and demonstrate skills in data engineering.  
- 🌐 Explore streaming data operations and implement real-world solutions for latency handling.  
- 🛠️ Gain practical experience with tools like Kafka, Flink, and Docker Compose.  

---

## ⚡ Installation and Setup
Setup instructions will be added once the project is finalized. The current architecture relies on **Docker Compose** for seamless deployment.

---

## 📅 Future Improvements
- 📘 **Detailed Startup Instructions**: Step-by-step guide for setting up and running the system.  
- 📈 **Showcase Dashboards**: Examples of real-time insights and data visualizations.  
- 🧮 **Enhanced Analytics**: Incorporating advanced analytical features for deeper insights.  

---

## 🧠 Lessons Learned
- ⚙️ Managing Docker Compose for complex systems required custom health checks and container scheduling for reliability.  
- 🕒 Working with streaming data highlighted the importance of watermarks and event-time handling for accurate results.  


![Logo](/doc_assets/Logo.png)

ProfiteerIO is a full-stack, end-to-end e-commerce intelligence platform that empowers users to predict optimal product pricing and boost purchasing behavior using real-time data pipelines, machine learning, and a seamless UI experience.


## Table of Contents
- [Demo](#demo)
- [Introduction](#introduction)
  - [Screenshots](#screenshots)
- [Architecture](#architecture)
  - [Core Services & Responsibilities](#core-services--responsibilities)
  - [Technical Workflow](#technical-workflow)
- [Dataset](#dataset)
  - [Key Features](#key-features)
  - [Data Structure](#data-structure)
  - [Generation Methodology](#generation-methodology)
  - [Usage Notes](#usage-notes)
- [Installation](#installation)
  - [Deploying with Helm](#deploying-with-helm)
  - [Accessing the Services](#accessing-the-services)
  - [Running ProfiteerIO Locally](#running-profiteerio-locally)
- [Prediction](#prediction)
- [UI Dashboard](#ui-dashboard)
- [Features](#features)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)

## Demo

For a TLDR; demo, check out the [YouTube video](https://www.youtube.com/watch?v=MTK3gQSxMuU) showcasing ProfiteerIO in action.

## Introduction

Setting the right price for your products can be a challenge for e-commerce businesses. Price too high, and you risk losing customers; price too low, and you sacrifice profits. So, how do you find the sweet spot in real-time, adapting to shifting market dynamics, product trends, and customer behavior?

Introducing **ProfiteerIO**- a powerful tool designed to help e-commerce businesses maximize profits by predicting sales under different pricing scenarios.

With **ProfiteerIO**, you can:

- Seamlessly sync catalog sales data from diverse sources (CSV, JSON, and more) into a robust database or data warehouse using Airbyte.
- Harness the power of AI by training models to predict purchase volumes based on product attributes and pricing strategies with MindsDB.
- Visualize product performance and forecast future sales trends through an intuitive React dashboard.
- Deploy your entire analytics stack on Kubernetes to any cloud provider (AWS, GCP, Azure) with just a few simple configurations using Helm.

### Screenshots
<details>

<summary>Expand for Dashboard, Catalog and Prediction Visuals</summary>

--- 

![Dashboard](/doc_assets/Dashboard.png)
![Catalog](/doc_assets/Catalog.png)
![Prediction](/doc_assets/Prediction.png)

</details>

## Architecture

The entire stack is deployed via a **Helm chart** with modular subcharts for Airbyte, MindsDB, Postgres, and the app components, enabling ***One-Click Deployment*** on Kubernetes.

Below is a comprehensive breakdown of how the platform works as well as an architecture diagram, its key components, and how everything ties together in a single seamless deployment.


### Core Services & Responsibilities

| STACK       | ROLE                                                                 |
|----------------|----------------------------------------------------------------------------------|
| **FastAPI** | Synthesizes realistic e-commerce sales data based on price, rating, and time dynamics. Also exposes REST APIs for analytics and prediction, powering the frontend and Airbyte source. |
| **PostgreSQL**      | Central datastore for all synthesized sales data, analytics results, and ML inputs/outputs. Tuned for fast filtering and aggregation. |
| **Airbyte**         | Periodically extracts generated data from the FastAPI source and loads it into PostgreSQL. Supports scheduled and manual syncs. |
| **MindsDB**         | Connects to PostgreSQL to train and serve machine learning models that forecast purchase volume based on key product features. |
| **React**  | A user-friendly UI that visualizes dashboards, enables catalog interactions, and supports live predictions using slider inputs. |
| **NGINX** | Routes incoming requests (via Nginx or other reverse proxy) to backend services and enforces secure access and CORS handling. |

![Architecture](/doc_assets/Architecture.svg)

### Technical Workflow


- **Synthetic Dataset Generation**: FastAPI uses configurable rules to simulate sales events. Parameters like price sensitivity, time-of-day behavior, and product ratings are baked into the generation algorithm.

- **Ingestion & Storage (EL)**: Airbyte extracts data from FastAPI and loads it into PostgreSQL. You can trigger syncs manually or schedule them hourly/daily.

- **ML Model Training**: MindsDB connects directly to PostgreSQL, continuously retraining or updating its prediction models. These models consider fields like price, rating, and hour-of-day to estimate expected purchases.

- **API & Analytics**: FastAPI exposes analytics endpoints to serve dashboard stats and product insights. For predictions, it acts as a bridge between the React frontend and MindsDB’s trained models.

- **User Interaction**: React queries the backend to render the Dashboard (metrics), Catalog (product management), and Prediction page (interactive sliders for pricing simulation).

---

## Dataset

The E-Commerce Dynamics Dataset is a meticulously crafted synthetic dataset designed to emulate real-world e-commerce sales behavior. The dataset simulates sales activities across a product catalog over a user-specified time period (in hours).

Each record encapsulates a snapshot of product performance at a given timestamp, factoring in dynamic pricing, consumer engagement (views, cart additions, purchases), and contextual influences like time-of-day demand fluctuations. The synthesis logic leverages probabilistic models and domain-inspired heuristics to ensure realism and variability.


### Key Features


- **Consumer Behavior Simulation**: Views, cart additions, and purchases are modeled using a multi-stage funnel, influenced by product ratings, category popularity, and time-of-day demand patterns.

- **Category Popularity Integration**: Products are assigned to categories with predefined popularity scores (derived from CategoryPopularity and ratings), impacting visibility and engagement.

- **Rating Evolution**: Product ratings (ranging from 2.0 to 5.0) evolve stochastically over time, simulating shifts in consumer sentiment.

- **Time-of-Day Sensitivity**: Demand fluctuates across four time buckets—Overnight (22:00–06:00), Morning (06:00–12:00), Afternoon (12:00–18:00), and Evening (18:00–22:00)—mimicking realistic shopping patterns.

- **Granular Temporal Resolution**: Sales data is generated hourly, with timestamps in ISO format, enabling fine-grained analysis of temporal trends.

- **Dynamic Pricing Mechanisms**: Products follow one of three pricing strategies—aggressive, moderate, or standard—bounded by minimum and maximum price constraints, reflecting real-world pricing variability.

---

### Data Structure


<details>

<summary>Read More</summary>

---
Each record in the dataset contains the following fields:


- `timestamp`: ISO-formatted timestamp of the sales snapshot.
- `product_id`: Unique identifier for the product.
- `product_name`: Descriptive name of the product.
- `product_image`: Reference to the product’s image (if applicable).
- `category`: Product category, linked to a popularity score.
- `category_popularity`: Popularity score of the category (0 to 1).
- `base_price`: Reference price for the product.
- `current_price`: Dynamically determined price based on the pricing strategy.
- `price_strategy`: Pricing approach (aggressive, moderate, or standard).
- `popularity_factor`: Composite score reflecting category popularity, rating, and device-specific adjustments.
- `time_of_day_bucket`: Time bucket influencing demand (Overnight, Morning, Afternoon, Evening).
- `views`: Estimated product views, driven by popularity and time factors.
- `cart_adds`: Number of times the product was added to carts, based on views and rating.
- `purchases`: Number of completed purchases, influenced by cart additions and price sensitivity.
- `rating`: Current product rating, subject to periodic updates.

</details>

---

### Generation Methodology


<details>

<summary>Read More</summary>

---

The dataset is generated using a modular Python-based synthesis logic, incorporating:

- **Pricing Logic**: Prices are determined using strategy-specific distributions (e.g., Gaussian for moderate pricing, uniform for aggressive), constrained by product-defined bounds.

- **Engagement Funnel**: Views are estimated from base view counts, adjusted by popularity and time-of-day factors. Cart additions and purchases follow, with conversion rates tied to ratings and price sensitivity.

- **Popularity Modeling**: A `popularity_factor` is calculated as a function of category popularity, product rating, and a randomized device-specific multiplier.

- **Stochastic Rating Updates**: Ratings are initialized (or inherited from `base_rating`) and periodically adjusted with a 10% probability, reflecting dynamic consumer feedback.

</details>

---

### Usage Notes

- The dataset is generated using the `generate_sales_data` function, which accepts a `SalesRequest` object containing the number of hours and product metadata.
- The dataset is synthetic, offering flexibility for experimentation without privacy or proprietary data concerns.

## Installation

> [!TIP]
> The recommended way to run the project is to use the provided Helm chart for deployment on Kubernetes. However, if you prefer to run it locally, there are instructions at the end of this section.

> [!NOTE]
> If you are using the Helm chart, please ensure you have Docker, Kubectl, Minikube, Helm, Git installed and running on your machine.
---
### Clone, Build Docker Images
Clone the repository to your local machine using the following command

```bash
git clone https://www.github.com/qreater/profiteer-io.git
```

Navigate to the directory, and then follow the instructions below to build the Docker images for each component. (Frontend, Backend) Make sure you are in the minikube context for docker.

```bash
cd devops/

docker build -t profiteer-io-backend .. -f ./Dockerfile.backend
docker build -t profiteer-io-frontend .. -f ./Dockerfile.frontend
```

---

### Deploying with Helm

The Helm chart includes all the necessary components, including **Airbyte, MindsDB, PostgreSQL, and the FastAPI backend, as well as an NGINX reverse proxy** for routing requests to the appropriate services. 

> [!WARNING]
Ensure you configure the `values.yaml` file in the helm chart according to your requirements. The default configuration is set up for local development, but you can modify it for production use. The deployment uses about **7Gi of memory and 2 CPUs** for the overall stack, with MindsDB demanding the most resources.


```bash
cd devops/helm/

kubectl create namespace profiteer
helm install profiteer-io . --namespace profiteer
```

---

### Accessing the Services

Once the deployment is complete, you can port-forward the services individually, or the NGINX service to access the frontend and backend. **K9s** is a great tool to visualize the services and their ports.

After this, the stack will be up and running. You can proceed to follow with the flow of the application, starting with the **Airbyte** connection to the **FastAPI** source.

---

### Running ProfiteerIO Locally

<details>

<summary>Read More</summary>

---

Clone the repository to your local machine using the following command

```bash
git clone https://www.github.com/qreater/profiteer-io.git
```

Make sure you have PostgreSQL, Airbyte, MindsDB, and Docker accessible on your machine. You can use Docker to run PostgreSQL and Airbyte locally, or use cloud versions of these services.

---

**Setting up FastAPI Service**

Create a `.env` file in the `/backend` directory and add the following environment variables, configure as needed:

```bash
MINDSDB_URL=http://localhost:47334

API_KEY=OPEN_SESAME

DB_NAME=mindsdb
DB_USER=mindsdb
DB_PASSWORD=mindsdb

DB_HOST=localhost
DB_PORT=5432

TABLE_NAME=Sales_Data
```

Create a virtual environment and follow the instructions below to install the dependencies and run the backend. Ensure you have Python 3.12, Pip installed in your machine.

```bash
cd backend

pip install poetry
poetry install

poetry run uvicorn main:app --reload --port 8000
```

Now, follow the technical workflow to set up the **Airbyte** connection to the **FastAPI** source. Sync the data to **PostgreSQL** and set up the **MindsDB** connection to the **PostgreSQL** database. 

Then proceed to train the model using the SQL commands provided in the **Prediction** section.

**Airbyte Connection**

Set up a connection between [Sales API](/backend/app/api/v1/sales.py) and Postgres in Airbyte User Interface. Use the following configuration for the connection to the FastAPI source:
```json
{
  "hours": 48,
  "products": [
    {
      "category": "Laptops",
      "max_price": 1400,
      "min_price": 1000,
      "base_price": 1200,
      "product_id": "P001",
      "base_rating": 4.5,
      "product_name": "UltraBook X1",
      "product_image": "https://example.com/images/ultrabook-x1.jpg",
      "price_strategy": "aggressive"
    },
    ...Add more products as needed
  ]
}
```

**Set up MindsDB Connection**

Log in to MindsDB and create a new connection to the Postgres database. Use the following credentials, change them if necessary.

```sql
CREATE DATABASE profiteer_data
WITH ENGINE = 'postgres',
     PARAMETERS = {
         "host": "postgresql.profiteer",
         "port": 5432,
         "user": "mindsdb",
         "password": "mindsdb",
         "database": "mindsdb",
         "schema": "public"
     };
```

- **Train the model**

Use the following command to train the model in MindsDB:

```sql
CREATE PREDICTOR mindsdb.sales_forecast
FROM profiteer_data
    (SELECT 
        views AS input_views,
        cart_adds,
        purchases,
        (current_price::float / NULLIF(base_price, 0)) AS price_ratio,
        popularity_factor
     FROM "Sales_Data")
PREDICT purchases
WINDOW 24
HORIZON 1;
```

**Try predicting purchases**

Use the following command to try the prediction in MindsDB:

```sql
SELECT * FROM mindsdb.sales_forecast
WHERE input_views = 24416.75
AND cart_adds = 1521.19
AND price_ratio = 0.95
AND popularity_factor = 1.51;

DESCRIBE model sales_forecast;
```

**Setting up React Frontend**

Create a `.env` file in the `/frontend` directory and add the following environment variables, configure as needed:

```bash
VITE_API_URL=http://localhost:8000/
VITE_API_KEY=OPEN_SESAME
```

Now install the dependencies and run the frontend. Ensure you have Node.js and NPM installed in your machine.

```bash
cd frontend
npm install
npm run dev
```

</details>

## Prediction

MindsDB is used to predict the number of purchases based on the features provided in the dataset. The prediction model is trained using the `purchases` column as the target variable and the selected features as input variables. The model uses a time window of 24 hours and a horizon of 1 hour to make predictions.

>[!TIP]
The prediction model is designed to be un-biased and robust, ensuring that the predictions are not influenced by any specific product or category.


| Field Name         | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `views`     | The views received by products                           |
| `cart_adds` | The number of times products were added to the cart                 |
| `popularity_factor` | The average popularity of the product categories, calculated with current price and ratings |
| `price_ratio`       | The average ratio of current price to base price, rounded to the nearest whole number |



## UI Dashboard
The UI dashboard is built using React and provides a user-friendly interface to visualize the predictions made by MindsDB. The dashboard includes the following features:

- **Product Catalog**: A list of products with their details, including product name, image, category, and current price.

- **Product Details and Prediction**: A detailed view of each product, including its predicted purchases based on the price set.

- **Overall Statistics**: A summary of the overall statistics, including the total purchases, top products and total revenue.

## Features

- **Scheduled Data Syncs**: Seamlessly sync your catalog sales data from various sources into a robust database or data warehouse using Airbyte.

- **AI-Powered Predictions**: Leverage MindsDB to train models that predict purchase volumes based on product attributes and pricing strategies.

- **Interactive Dashboard**: Visualize product performance and forecast future sales trends through an intuitive React dashboard.

- **One-Click Deployment**: Deploy your entire analytics stack on Kubernetes to any cloud provider (AWS, GCP, Azure) with just a few simple configurations using Helm.

- **Modular Architecture**: The architecture is designed to be modular, allowing for easy integration of new components and services as needed.

## Future Work

- **Stock Management**: Integrate stock management features to track inventory levels and optimize stock replenishment based on sales predictions.

- **Broader Category Support**: Expand the dataset to include a wider range of product categories and attributes, enhancing the model's predictive capabilities.

- **Real-Time Data Ingestion**: Implement near-real-time data ingestion capabilities to ensure that the dataset is always up-to-date with the latest sales data.

- **World Events**: Integrate world events and trends into the dataset to better understand their impact on sales and consumer behavior.

## Contributing
We welcome contributions to this project! If you have any suggestions or improvements, please feel free to open an issue or submit a pull request. Here are the tools and utilities we used to build this project, and we encourage you to use them as well:

### Tools & Utilities

| CATEGORY         | TOOL                                              |
|------------------|---------------------------------------------------|
| Dev Cycle        | GitHub Issues + Pull Requests                   |
| CI/CD            | GitHub Actions for PR test runs                 |
| Design           | Figma for UI/UX mockups, logo                    |
| Frontend Style   | `prettier` & `eslint` for linting and formatting      |
| Backend Style    | `black` for Python code formatting                |
| Deployments      | Docker, Kubernetes, Helm                        |
| Asset Generation | DALL·E for product imagery and creative assets |

>[!TIP]
> This project adheres to modern developer workflows and automation principles. It includes CI pipelines, standardized formatting tools, and a collaborative GitHub-based review process.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
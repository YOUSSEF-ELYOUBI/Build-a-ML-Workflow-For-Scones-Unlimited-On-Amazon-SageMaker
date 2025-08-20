# End-to-End ML Workflow for Scones Unlimited on AWS SageMaker

### Project for the AWS Machine Learning Fundamentals Nanodegree by Udacity

This project demonstrates the development and deployment of a complete, event-driven machine learning workflow on AWS. The goal was to build an image classification solution for "Scones Unlimited," a fictional logistics company, to automatically distinguish between **bicycles** and **motorcycles**. This allows the company to optimize delivery assignments and better manage its fleet.

The entire pipeline—from data processing to model training, deployment, and serverless inference—is built using powerful AWS services, showcasing a scalable and automated MLOps approach.

## Dataset
The model was trained on a subset of the [CIFAR-100 Dataset](https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz), provided by the University of Toronto.

## Machine Learning Workflow Architecture
The core of this project is a serverless workflow orchestrated by **AWS Step Functions**. This state machine defines the flow of data through a series of AWS Lambda functions, which process the data, invoke a SageMaker endpoint for inference, and filter the results based on a confidence threshold.

<!-- REPLACE THIS URL with the link to your own screenshot of the successful Step Function execution -->
![Step Function Workflow](https://raw.githubusercontent.com/Asma-Nasr/Build-a-ML-Workflow-For-Scones-Unlimited-On-Amazon-SageMaker/main/stepfunctions_graph.png)

---

## Project Components

### 1. Data Staging and Preparation (ETL)
-   **Extract:** The raw CIFAR-100 dataset was downloaded and extracted within the SageMaker environment.
-   **Transform:** The dataset was filtered to isolate only two classes: `bicycle` and `motorcycle`. The raw image data was reshaped from a flat array into a 3D (32x32x3) image format and saved as PNG files.
-   **Load:** The processed training and testing images, along with manifest `.lst` files, were uploaded to an **Amazon S3** bucket to be used as a data source for model training.

### 2. Model Training and Deployment
-   **Algorithm:** The project leverages the built-in **SageMaker Image Classification Algorithm**, which uses a ResNet deep learning architecture.
-   **Training:** A SageMaker `Estimator` was configured to launch a training job on a `ml.p3.2xlarge` instance, training the model on the 1000 prepared images from S3.
-   **Deployment:** The trained model was deployed to a persistent **SageMaker Endpoint** on a `ml.m5.xlarge` instance, making it available for real-time inference.

### 3. Serverless Inference Pipeline
The inference pipeline is orchestrated by **AWS Step Functions** and powered by three distinct **AWS Lambda** functions:

1.  **`serializeImageData`**: Receives an S3 object key, downloads the image, and base64-encodes it.
2.  **`classifyImage`**: Takes the encoded image, invokes the SageMaker endpoint to get a prediction, and adds the inference results to the data payload.
3.  **`filterLowConfidence`**: Parses the inference results and checks if the confidence score is above a predefined threshold (e.g., 70%). If not, it "fails loudly" by raising an exception, which stops the workflow.

### 4. Monitoring and Visualization
-   **SageMaker Model Monitor** was enabled on the endpoint to capture 100% of the inference requests and responses.
-   This captured data was downloaded from S3, parsed, and used to create a visualization of the model's performance over time.

---

## Project Showcase

### Successful Step Function Execution
This screenshot shows a successful run where the inference confidence was above the threshold, allowing all three steps to complete.

<!-- REPLACE THIS URL with the link to your own screenshot -->
`![Successful Step Function Execution](link/to/your/success_screenshot.png)`

### Failed Step Function Execution (As Expected)
This screenshot demonstrates the "fail loudly" principle. The inference confidence was below the threshold, so the `filter` Lambda correctly raised an error and the entire execution failed. This is the desired behavior for low-confidence predictions.

<!-- REPLACE THIS URL with the link to your own screenshot from the last question -->
![Failed Step Function Execution](https://i.imgur.com/your-failure-screenshot-name.png)

### Model Performance Visualization
The box plot below shows the distribution of prediction confidence scores for inferences made, helping stakeholders quickly assess model performance.

<!-- REPLACE THIS URL with the link to your own visualization screenshot -->
`![Model Confidence Visualization](link/to/your/visualization_screenshot.png)`

---

## Setup and Usage
To set up this project, clone the repository into an Amazon SageMaker Notebook environment and run the cells in the `starter.ipynb` notebook.

```bash
git clone https://github.com/Asma-Nasr/Build-a-ML-Workflow-For-Scones-Unlimited-On-Amazon-SageMaker.git# Build-a-ML-Workflow-For-Scones-Unlimited-On-Amazon-SageMaker

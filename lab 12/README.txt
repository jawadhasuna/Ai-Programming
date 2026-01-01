# Exploratory Data Analysis (EDA) of Built-in R Dataset in Google Colab

## Project Overview

This project demonstrates how to perform **Exploratory Data Analysis (EDA)** using a **built-in R dataset** within **Google Colab**. Instead of uploading an external dataset, the project utilizes datasets that are already available in R. The purpose is to understand the structure, summary statistics, and distribution of data using descriptive analysis and visualizations.

The project is suitable for beginners learning **R**, **EDA concepts**, or **Google Colab with R**.

---

## Project Objectives

* Display the list of all available built-in datasets in R
* Load a dataset from the built-in dataset library
* Understand the dataset structure and variables
* Perform summary statistics analysis
* Visualize data distributions and relationships

---

## Tools and Technologies Used

* **Google Colab** (Cloud-based Jupyter environment)
* **R Programming Language**
* **rpy2** (to enable R inside Google Colab)
* **ggplot2** (for data visualization)
* **Base R functions** (for summary and structure analysis)

---

## Dataset Details

* **Dataset Name:** `iris`

* **Source:** Built-in R dataset (`datasets` package)

* **Description:**
  The `iris` dataset contains measurements of 150 iris flowers from three species:

  * Setosa
  * Versicolor
  * Virginica

* **Variables:**

  * `Sepal.Length` (numeric)
  * `Sepal.Width` (numeric)
  * `Petal.Length` (numeric)
  * `Petal.Width` (numeric)
  * `Species` (categorical)

---

## Exploratory Data Analysis Performed

### 1. Dataset Listing

* Displayed all available built-in datasets using the `data()` function

### 2. Data Understanding

* Viewed the first few rows using `head()`
* Checked structure and data types using `str()`

### 3. Summary Statistics

* Used `summary()` to obtain:

  * Minimum and maximum values
  * Mean and median
  * Quartiles
  * Class distribution of species

### 4. Data Visualization

* **Histogram** to analyze the distribution of sepal length
* **Boxplot** to compare sepal length across species
* **Scatterplot matrix** to study relationships among numeric features

---

## How to Run the Project

Follow these steps in **Google Colab**:

### Step 1: Enable R in Colab

Run the following in a Python cell:

```
%load_ext rpy2.ipython
```

### Step 2: List Built-in Datasets

Run in an R cell:

```
%%R
data()
```

### Step 3: Load the Dataset

```
%%R
data("iris")
head(iris)
```

### Step 4: Perform EDA

```
%%R
summary(iris)
str(iris)
```

### Step 5: Visualizations

```
%%R
install.packages("ggplot2")
library(ggplot2)

ggplot(iris, aes(x = Sepal.Length)) +
  geom_histogram(binwidth = 0.5, fill = "skyblue", color = "black")


ggplot(iris, aes(x = Species, y = Sepal.Length, fill = Species)) +
  geom_boxplot()

pairs(iris[1:4])
```

---

## Expected Outcome

* Clear understanding of the dataset structure
* Insights into feature distributions
* Visual comparison between different species
* Foundation for further analysis such as clustering or classification

---

## Conclusion

This project provides a complete introduction to performing Exploratory Data Analysis using built-in R datasets in Google Colab. It eliminates the need for external data uploads and focuses on understanding data using statistical summaries and visualizations, making it ideal for academic labs and beginners.

---

## Author

**Jawad Hassan**

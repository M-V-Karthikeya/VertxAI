# Investor Matching Platform

## Overview
The **Investor Matching Platform** is a **Streamlit-based web application** that helps startup founders find suitable investors based on various parameters such as industry, funding stage, location, and business model. The application processes investor data stored in a JSON file and ranks the best matches using **TF-IDF vectorization and cosine similarity**.

## Features
- **Text-based Investor Matching:** Uses **TF-IDF and cosine similarity** to compare startup descriptions with investor profiles.
- **Categorical Filtering:** Matches investors based on **industry, funding stage, location, and business model**.
- **Funding Range Matching:** Ensures the required funding amount falls within the investor’s preferred cheque range.
- **Streamlit UI:** Provides an interactive interface for startup founders to input their details. Also displays the CSV Data Frame with Full Screen option.
- **Download Results:** Allows users to download the matched investor list as a CSV file.

## Installation
To run this project, ensure you have **Python 3.8+** installed, then run:

```sh
pip install -r requirments.txt
```

## Usage
1. **Run the Streamlit app:**
   ```sh
   streamlit run main.py
   ```
2. **Enter your startup details:**
   - Describe your startup.
   - Select industry, funding stage, country, and business model.
   - Enter the required funding amount.
3. **Find Matching Investors:** Click the `Find Investors` button to get ranked recommendations.
4. You can also see the display of the results in a table with a full screen option.
5. **Download the results:** Click the `Download CSV` button to save matched investors.

## File Structure
```
Assignment-1
│── Data
│   ├── investors.json   # Investor dataset
│── Results
│   ├── sample_output.csv
│── main.py              # Streamlit application
│── Code.ipynb           # Notebook
│── requirments.txt
│── README.md            # Project documentation
```

## Code Explanation
### **1. Data Cleaning Functions (`clean`)**
- Standardizes investor data by converting to **lowercase** and splitting multi-value fields.
- Removes extra spaces and empty values.

### **2. Feature Extraction**
- Extracts **unique values** for industries, funding stages, business models, and countries. For giving as a drop down menu for user.

### **3. Investor Matching Functions**
- **`match_overview`**: Compares startup descriptions with investor overviews using **TF-IDF vectorization**. (weightage = Simlarity_Score * 100)
- **`match_industry`**: Scores investors based on shared industries. (weightage = 15 per match)
- **`match_stage`**: Scores investors based on shared funding stages. (weightage = 10 per match)
- **`match_region`**: Scores investors based on shared locations. (weightage = 5 per match)
- **`match_model`**: Scores investors based on business model alignment. (weightage = 5 per match)
- **`match_funds`**: Checks if the requested funding is within the investor’s cheque range. (weightage = 30 if true) (highest weightage)

### **4. Matching Algorithm (`match`)**
- **Combines all similarity scores** and ranks investors.
- **Returns top 30 matches** based on total scores.

### **5. Streamlit UI**
- **User Inputs:** Text fields & dropdowns to collect startup information.
- **Find Investors Button:** Triggers the matching function.
- **Download Button:** Exports matched investors as CSV.

## Author
Developed by **Karthikeya**.


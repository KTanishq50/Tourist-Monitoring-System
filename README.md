# Project Overview

This project integrates **Django**, **Machine Learning models**, **Google Maps API**, **OpenRouteService (ORS) API**, **OpenWeatherMap (OWM) API**, and **Ethereum blockchain (via Ganache)** to provide a **Tourist Safety System**.  

---

## Tech Stack
- Python (dependencies in `requirements.txt`)  
- Django for the backend  
- Ganache for a private Ethereum testnet  
- Google Maps API for map rendering  
- ORS API for route fetching  
- OWM API for weather features  
- ML models (trained in Google Colab, exported as pickle files)  

---

## Authority-Side Features

1. **Zone Dashboard**  
   - Displays maps and allows authorities to draw polygons representing **Safe**, **Unsafe**, or **Restricted** zones.  
   - Polygon coordinates and labels are stored in the `zones` model.  
   - These coordinates are used by the routing ML model to check if a route passes through restricted/unsafe zones.  
   - Routes passing through more restricted or unsafe zones receive a lower score.  

2. **Live Tracking**  
   - Tracks the live location of all users logged in on the client side.  
   - Locations are captured whenever the user navigates through the site.  
   - Data is stored in two models:  
     - `UserLocation`: Stores the **current live location**.  
     - `UserLocationHistory`: Appends every location change, maintaining a growing history of coordinates.  
   - The **Anomalous Behaviour Model** runs on `UserLocationHistory`.  
     - It processes data in chunks of 100 coordinates per user.  
     - Once consumed, those coordinates are marked, and only new ones are considered in the next cycle.  
     - If fewer than 100 unconsumed coordinates exist, the model skips to the next user.  

3. **Blockchain Dashboard**  
   - A private Ethereum testnet is launched via Ganache.  
   - Ganache provides 10 accounts to write data onto the blockchain.  
   - A **Tourist Registry smart contract** (written in Solidity) defines how tourist data is stored.  
   - When a client registers:  
     - Credentials are verified using government APIs.  
     - Data is stored in the database and also sent to the smart contract.  
     - The data is hashed and written on-chain, with validity equal to the client’s stay duration.  
     - A **QR code** is generated, which can be scanned to verify the client’s validity on-chain.  

---

## Client-Side Features

1. **QR Verification**  
   - Generates a QR code upon registration.  
   - Scanning the QR code checks validity against the blockchain and returns a simple **true/false**.  

2. **Custom Maps**  
   - Uses the **Routing ML model**.  
   - Inputs include:  
     - Start & destination coordinates  
     - Weather and geographical features (via OWM API)  
     - Zone coordinates (from the `zones` model)  
     - Routes fetched from ORS API  
   - Routes are ranked using **XGBoost Ranking**.  
   - The map displays routes with different preference shades based on rankings.  

---

## Machine Learning Models

- **Routing Model**:  
  - Scores and ranks routes based on safety, zones, and weather conditions.  

- **Anomalous Behaviour Model**:  
  - Uses the `UserLocationHistory` data.  
  - Applies **IsolationForest** to analyze the latest 100 coordinates of each user.  
  - Produces a one-hot output: **Anomalous / Not Anomalous**.  

 Both models were trained in **Google Colab** on synthetic data.  
The pickle files are stored in the `ml-models/` directory of the Django project.  

---

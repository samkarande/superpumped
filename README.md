# Superpumped 
Skyflow demo for ride sharing application

---
## Description
Creates a Python, REST, HTML5/JS demo application
Demonstrating working with 
### ride table
Ride table has entry for each ride booked via superpumped application
Each ride has a driver, a passenger, country, state, zip code (ride start) and other details
Each ride has 2 boolean flags
#### Active
Indicate the ride is currently active, not completed. Only the completed rides are made available for analytics users

#### Flagged
Indicate passenger or driver has raised issue with the ride and support personnel based on their assigned country and state should get involved in rectifying the raised issue. 
The support personnel get access to flagged rides and could get access to masked, redacted data such as 1. passenger and driver contact information 
2. Context based access to passenger and/or driver table data for temporary basis

## Features
### Support (Country US, State CA)
Access only to Flagged rides
Token based access to specific flagged ride for driver and passenger PII (limited set)

### Analytics (Country US)
Access only to non-active rides, or completed rides
Reporting functionality for group by zip code, driver id, passenger id

### Create rides
Simulate new rides being booked, imported through customer data pipeline
Random entries for active, flagged
Random picking for driver id and passenger id

### Readacted raw data access (only for PoC demo)
#### Driver data
#### Passenger data
#### Ride data


## Installation

### Requirements

- Python 3.7.0 and above

### Configuration

The package can be installed using pip:

```bash
pip install skyflow
```
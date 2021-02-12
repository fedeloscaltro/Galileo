# Galileo

Galileo is a vertical search engine focused on human exploration in space

## Installation

#### If you have Windows:

1. Open Windows PowerShell
2. In the project's folder, to install the required modules, type: 
```bash
.\install.bat 
```
3. To start the application type: 
```bash
.\start.bat 
```
4. Copy the URL at the end of the output message in your favourite browser

#### If you have Linux/macOS:

1. Open a Terminal window
2. Go inside the project folder
3. Type in this command to install the required packages:
```bash
bash install.sh
```
4. Type in the command to start the application:
```bash
bash start.sh
```
5. Open a browser and enter `127.0.0.1:5000` in the search bar

## Usage

In the home page you can search whatever you want using different tools:
- Search bar
- Filter by sources
- Filter by dates

### Query language

Within the search bar you can specify queries using free text, concepts from a thesaurus and boolean operators.
For example, if you want to search some articles about exploration you can enter `exploration` as free text to find the articles that speak expicitly about exploration, or you can type in `{exploration,RT}` if you are looking for related terms of exploration.

The default method in free text searches works in OR, so if you search for `Mars nasa missions` the system will retrieve all the documents that contain at least one of the word in the query, but you can search with any boolean operator, so if you search for `Mars AND nasa AND missions` you will see just the articles that contain all of the words you have typed in the search bar.

The thesaurus we adopted for our purpose has specific terms concerning space explorations, in fact it's made by NASA. It is composed by a list of triplets, each one containing the key-term, a relationship type and the correlated concept. 
You can specify one of these relationship types:
- BT: broader term
- NT: narrower term
- RT: related term
- UF: (use for) reference from an accepted term to an unaccepted one
- USE: reference from an unaccepted term to an accepted one

So the syntax of a query by concepts is `{term, relationship-type}`

### Filters

The system provides two type of filter:
1. Date range
2. Source filter

You can specify a range of dates (if no range is set the filter will not be applied) using the calendar boxes under the search bar. You can even set a starting date without setting an ending one (or viceversa).

With source filter you can search the articles that are from a certain website.

## Support

For any kind of issue use the following contacts:
- 251349@studenti.unimore.it - Federico Scaltriti
- 261088@studenti.unimore.it - Lorenzo Storchi



# Welcome to OpenQCM API!

# Overview

## Context

This project is carried out as part of _Datascientest's_ Data Engineering training (Fev-Dec 2021). It takes part of the evaluation process for the module entitled _"FastAPI"_ .

## Objective

For this evaluation, we consider a company creating quizzes via a smart-phone or web browser apps. The quizzes take the form of _Multiple Choice_  _Question_  (Questions à Choix Multiple in French, hence the name _OpenQCM_). The idea is to propose a service for individuals/companies to test themselves/their team's knowledge while having fun :D.

To optimize the architecture, the company wants to set up an API with the purpose of unifying the way to query a database and return a series of questions. The objective then is to create this API.

## Data

The database is represented by a csv file that the api manipulate and stock at the current directory. The original version in available at : 
> _https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv_

The database contains the following fields:
   - _**question**_: the title of the question
  - _**subject**_: the category of the question
   - _**correct**_: the list of correct answers
  -  _**use**_: the type of _Multiple Choice_ _Question_ _(_MCQ) for which this question is used
- _**responseA**_: answer A
- _**responseB**_: answer B
- _**responseC**_: response C
- _**responseD**_: the answer D (if it exists).

# The API
The API, referred to as _**OpenQCM**_ from now on, is a simple HTTP REST API for technical quizzes including a wide variety of topics such as: _Automation, BDD, Classification, Data Science, Docker, Machine Learning, and lots more._
## Request parameters
A user can search for questions using the following pattern:

The user choose a type of test (use) and one or more categories (subject). The application produce MCQs of either 5, 10 or 20 questions (to be specified in user request, 5 being the default value). The API returns this number of questions in JSON format, c.f. Output format.

As the API must be able to generate many MCQs, these are returned in a random order: thus, a request with the same parameters may return different questions.
## Authentication
Users are expected to have an account. Credentials verification is done using basic _username:password_ authentication: the string containing Basic _username:password_ is passed via the Authorization header (encoded/no)
## EndPoints
OpenQCM has many endpoint, illustrated in the following:

|                |Parameters                          |Details                         |
|----------------|-------------------------------|-----------------------------|
|Get /status|`None`            |Verify that the API is functional.            |
|GET /users/me          |`None`            |Get the current user            |
|GET /subjets          |`None`            |List available subjects in the database            |
|GET /uses          |`None`            |List available uses in the database            |
|GET /qcm          |_`Number (type :integer)`_:  must be either 5, 10 or 20 <br>_default value_ : 5 <br> _`Use (type :string)`_ : must be one of available uses from the database, e,g, _'Test de positionnement'_, _'Test de validation'_, _'Total Bootcamp'_ <br>_Default value_ : _'Test de positionnement'_ <br>_`Subjects (type list[string])`_ could be one or more subjects available from database.` |- Get a MCQ from database :<br> (1) containing 5,10 or 20 questions <br> (2) Related to one or more subjects (category) <br> (3) Related to one use (e.g. _Test de positionnement_, _Test de validation_, etc)|
|POST /qcm/add          |_`question`_, _`subject`_, _`correct`_,_`use`_, _`responseA`_, _`responseB`_,_`responseC`_,_`responseD`_| - Create a new question (requires _admin_ privileges).


## Examples

The following example will output 10 random questions.
- Curl
> curl -X   'http://127.0.0.1:8000/qcm/?number=10&use=Test%20de\  %20positionnement&subjects=Data%20Science&subjects= Docker&subjects=Machine%20Learning&subjects=Syst%C3%A8mes %20distribu%C3%A9s' \
   -H 'accept: application/json'

- Request URL
> http://127.0.0.1:8000/qcm/?number=10&use=Test%20de%20positionnement&subjects=Data%20Science&subjects=Docker&subjects=Machine%20Learning&subjects=Syst%C3%A8mes%20distribu%C3%A9s

This returns a JSON object with the results in an array you can iterate over.

``` 
{
  "use": "Test de positionnement",
  "subject": [
    "Data Science",
    "Docker",
    "Machine Learning",
    "Systèmes distribués"
  ],
  "number": 10,
  "results": [
    "Docker permet de persister des changements",
    "Dans Hadoop, les combiners permettent",
    "Des containers Docker peuvent communiquer entre eux grâce à",
    "Docker est utilisé",
    "Hive permet",
    "Quels sont les trois éléments constitutifs de Hadoop ?",
    "Le théorème CAP oppose",
    "Docker-compose est ",
    "Spark se différencie de Hadoop par",
    "Dans Hadoop, les partitioners permettent"
  ]
}
```

Response Headers
```
content-length: 509  
content-type: application/json  
date: Wed,28 Jul 2021 18:28:31 GMT  
server: uvicorn
```



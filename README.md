## Synopsis

This project is an experiment in the use of flask to provide a RESTful API for
querying and managing a database of NGS runs and assocaited sample metadata.

## Code Example

## Motivation

## Installation

make setup  # creates phython virtual env

make test   # runs tests

make run    # start internal python server

## API Reference

Retrieve Sample List:

curl -u miguel:python -i http://localhost:5000/ngssm/api/v1.0/samples

Retrieve Sample By Unique ID

curl -u miguel:python -i http://localhost:5000/ngssm/api/v1.0/samples/1

Filter Sample List based on plate

curl -u miguel:python -i http://localhost:5000/ngssm/api/v1.0/samples?plate=46.4

## Tests

## Contributors

## License


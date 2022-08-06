# Coding Exercise: Data Storage API

Implement a small HTTP service to store objects organized by repository.
Clients of this service should be able to GET, PUT, and DELETE objects.

## Expectations

We ask that you spend no more than 2 hours on this exercise. We value your time and don't want to set unreasonable expectations on how long you should work on this exercise.

We ask you complete this exercise so you have an opportunity to build a service in your own time rather than an in-person interview, coding on a whiteboard.

## General Requirements

* The service should de-duplicate data objects by repository.
* The service should listen on port `8282`.
* The included tests should pass and should not be modified.
* Do not move or rename any of the existing files.
* The service must implement the API as described below.
* The data can be persisted in memory, on disk, or wherever you like.
* The service should identify objects by their content. This means that two objects with the same content should be considered identical, and only one such object should be stored per repository.
* DO NOT include any extra dependencies. Anything in the Python standard library is fine.

## Recommendations

* Your code will be read by humans, so organize it sensibly.
* Add extra tests to test the functionality of your implementation.
* Use this repository to store your work. Committing just the final solution is *ok* but we'd love to see your incremental progress. We suggest taking a look at [GitHub flow](https://guides.github.com/introduction/flow/) to structure your commits.
* [Submit a pull request](https://help.github.com/articles/creating-a-pull-request/) once you are happy with your work.
* Treat this pull request as if you’re at work submitting it to your colleagues, or to an open source project. The body of the pull request should be used to describe your reasoning, your assumptions and the tradeoffs in your implementation.
* Remember that this is a web application so concurrent requests will come in.
* For data storage, try to get to a working solution and avoid complex dependencies.

## API

### Upload an Object

```
PUT /data/{repository}
```

#### Response

```
Status: 201 Created
{
  "oid": "2845f5a412dbdfacf95193f296dd0f5b2a16920da5a7ffa4c5832f223b03de96",
  "size": 1234
}
```

### Download an Object

```
GET /data/{repository}/{objectID}
```

#### Response

```
Status: 200 OK
{object data}
```

Objects that are not on the server will return a `404 Not Found`.

### Delete an Object

```
DELETE /data/{repository}/{objectID}
```

#### Response

```
Status: 200 OK
```

## Getting started and Testing

This exercise requires a python 3.9. Get started by installing dependencies:

```sh
pip install -r requirements.txt
```

Write your server implementation in `server.py`. Then run the tests:

```sh
python -m unittest server_test.py
```

Once you have a working implementation, open a pull request that includes your changes.

## CI

There is a GitHub Actions workflow file in this repository, it will activate on pull requests, it's a good way
to see if your tests are passing before closing out your submission!

## Submitting Your Work
When you are finished, please remember to commit all of your code, push your changes to GitHub, open a Pull Request, then visit https://interviews.githubapp.com/ and click `Done`.


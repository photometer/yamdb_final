[![CI/CD api_yamdb](https://github.com/photometer/yamdb_final/workflows/CI%2FCD%20api_yamdb/badge.svg)](https://github.com/photometer/yamdb_final/actions/workflows/yamdb_workflow.yml)

[comment]: <> (This is for pytest: https://github.com/photometer/yamdb_final/workflows/yamdb_workflow.yml/badge.svg)

# API Yamdb

### Project description:
The YaMDb project collects user feedback on works. The works are divided into 
categories: "Books", "Films", "Music". The list of categories can be expanded 
by the administrator. The works themselves are not stored in YaMDb; you 
cannot watch a movie or listen to music here. In each category there are 
works: books, films or music. A work can be assigned a genre from the 
predefined list (for example, "Fairytale", "Rock" or "Arthouse"). New genres 
can only be created by the administrator. Users can leave text reviews for 
works and rate the work from 1 to 10; from user scores, an average sckre of 
the work is formed - a rating. A user can leave only one review per work.

Information about the possibilities of the project can be found at the 
endpoint ```/redoc/```.

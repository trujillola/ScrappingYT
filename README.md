# ScrappingYT

Author : Laura Trujillo
Mail : trujillola@cy-tech.fr

# Dependences and execution context

To run this project you need to install :
- python 3.8
- prepare a venv environment
- Beautyful Soup
- pytest and pytest-cov

To execute the project : 

```shell
python3 scrapper.py --input input.json --output output.json
```

To lauch the tests and see the coverage :

```shell
pytest --cov=. tests/
```
Some tests use the file inputtest.json. Hence, they will fail if the file is modified.

## Input file

I have tested the code with input.json that contains only a few YT ids and the execution time was already long. 

## Output file

The result is saved in a json output file.  

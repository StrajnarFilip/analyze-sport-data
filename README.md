# Usage

A simple way to create a comparison:

```sh
# Clone this repository.
git clone https://github.com/StrajnarFilip/analyze-sport-data
# Change directory into repository.
cd analyze-sport-data/
# Copy any amount of FIT or TCX files into this directory.
cp /home/example/example.fit .
cp /home/example/example.tcx .
# Install this package.
python -m pip install .
# Alternatively you can install using poetry:
# poetry install

# Run included example.py script:
python example.py
# Alternatively you can run the script using poetry:
# poetry run python example.py
```

![Example](https://github.com/StrajnarFilip/analyze-sport-data/blob/master/example.png?raw=true) 

GENERATED_PYTHON=MainWindow.py SquareMeters.py

all: $(GENERATED_PYTHON)

run: $(GENERATED_PYTHON)
	python3 firerule.py

generate-python:

%.py: %.ui
	pyuic5 $< -o $@

clean:
	rm -f *.pyc
	rm -rf __pycache__/

all: MainWindow.py SquareMeters.py

%.py: %.ui
	pyuic5 $< -o $@

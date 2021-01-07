from PyQt4.QtCore import QObject


class colorSchemeSpec(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.default_values()

    def default_values(self):
        self.spec1 = {'color': 'k', 'width': 1.0, 'style': '-'}
        self.spec2 = {'color': 'r', 'width': 1.0, 'style': '-'}
        self.slicer = {'color': 'r', 'width': 1.0, 'style': '-'}
        self.zoom = {'color': 'r', 'width': 3.0, 'style': '-'}
        self.select = {'color': 'r', 'width': 1.0, 'style': '-', 'hatch': '/', 'alpha': 1.0}

    def update(self, spec1={}, spec2={}, slicer={}, zoom={}, select={}):
        if spec1 != {}:
            for i in spec1.keys():
                self.spec1[i] = spec1[i]
        if spec2 != {}:
            for i in spec2.keys():
                self.spec2[i] = spec2[i]

        if slicer != {}:
            for i in slicer.keys():
                self.slicer[i] = slicer[i]

        if zoom != {}:
            for i in zoom.keys():
                self.zoom[i] = zoom[i]

        if select != {}:
            for i in select.keys():
                self.select[i] = select[i]
        self.emit(SIGNAL("changed()"))


class colorSchemeSpax(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.default_values()

    def default_values(self):
        self.image = {'colormap': 'hot', 'reversed': False, 'interpolation': 'nearest', 'radius': 1.0,
                      'scaling': 'Linear'}
        self.marker = {'color': 'b', 'width': 1.0, 'hatch': 'None', 'alpha': 0.5}
        self.select = {'color': 'r', 'width': 1.0, 'hatch': '/', 'alpha': 0.5}

    def update(self, image={}, marker={}, select={}):
        if image != {}:
            for i in image.keys():
                self.image[i] = image[i]

        if marker != {}:
            for i in marker.keys():
                self.marker[i] = marker[i]

        if select != {}:
            for i in select.keys():
                self.select[i] = select[i]
        self.emit(SIGNAL("changed()"))


class colorsQSOSpax(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.default_values()

    def default_values(self):
        self.QSO = {'color': 'r', 'width': 1.0, 'hatch': '/', 'alpha': 0.5}
        self.EELR = {'color': 'g', 'width': 1.0, 'hatch': '/', 'alpha': 0.5}

    def update(self, QSO={}, EELR={}):
        if QSO != {}:
            for i in QSO.keys():
                self.QSO[i] = QSO[i]

        if EELR != {}:
            for i in EELR.keys():
                self.EELR[i] = EELR[i]
        self.emit(SIGNAL("changed()"))


class colorsQSOSpec(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.default_values()

    def default_values(self):
        self.cont = {'color': 'b', 'width': 1.0, 'hatch': 'None', 'alpha': 0.5}
        self.broad = {'color': 'r', 'width': 1.0, 'hatch': 'None', 'alpha': 0.5}

    def update(self, cont={}, broad={}):
        if cont != {}:
            for i in cont.keys():
                self.cont[i] = cont[i]
        if broad != {}:
            for i in broad.keys():
                self.broad[i] = broad[i]
        self.emit(SIGNAL("changed()"))
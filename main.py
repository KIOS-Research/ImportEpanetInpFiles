# (C)Marios Kyriakou 2016
# University of Cyprus, KIOS Research Center for Intelligent Systems and Networks
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox, QWidget
from .ExportEpanetInpFiles_dialog import ExportEpanetInpFilesDialog
from qgis.PyQt.QtGui import *#QIcon
from qgis.PyQt.QtCore import *#QVariant, Qt
from .Epa2GIS import epa2gis
from . import resources_rc
import sys
import os


class ImpEpanet(object):
    def __init__(self, iface):
        # Save a reference to the QGIS iface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.dlg = ExportEpanetInpFilesDialog()
        self.sections = ['junctions', 'tanks', 'pipes', 'pumps', 'reservoirs', 'valves', 'STATUS', 'PATTERNS', 'CURVES',
                         'CONTROLS', 'RULES', 'ENERGY', 'REACTIONS', 'REACTIONS_I', 'EMITTERS', 'QUALITY', 'SOURCES',
                         'MIXING', 'TIMES', 'REPORT', 'OPTIONS']

    def initGui(self):
        # Create action
        sys.path.append(os.path.dirname(__file__)+'/impcount.py')

        self.action = QAction(QIcon(":/plugins/ImportEpanetInpFiles/impepanet.png"), "Import Epanet Input File",
                              self.iface.mainWindow())
        self.action.setWhatsThis("Import Epanet Input File")
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&ImportEpanetInpFiles", self.action)

        self.actionexp = QAction(QIcon(":/plugins/ImportEpanetInpFiles/expepanet.png"), "Export Epanet Input File",
                                 self.iface.mainWindow())
        self.actionexp.setWhatsThis("Export Epanet Input File")
        self.actionexp.triggered.connect(self.runexp)
        self.iface.addToolBarIcon(self.actionexp)
        self.iface.addPluginToMenu("&ImportEpanetInpFiles", self.actionexp)

        self.dlg.ok_button.clicked.connect(self.ok)
        self.dlg.cancel_button.clicked.connect(self.cancel)
        self.dlg.toolButtonOut.clicked.connect(self.toolButtonOut)

    def unload(self):
        # Remove the plugin
        self.iface.removePluginMenu("&ImportEpanetInpFiles", self.action)
        self.iface.removeToolBarIcon(self.action)

        self.iface.removePluginMenu("&ImportEpanetInpFiles", self.actionexp)
        self.iface.removeToolBarIcon(self.actionexp)

    def run(self):
        filePath = QFileDialog.getOpenFileName(self.iface.mainWindow(), "Choose EPANET Input file",
                                               os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'),
                                               "Epanet Inp File (*.inp)")
        if filePath[0] == "":
            return
        epa2gis(filePath[0])
        self.iface.messageBar().clearWidgets()
        msgBox = QMessageBox()
        msgBox.setWindowTitle('ImportEpanetInpFiles')
        msgBox.setText('Shapefiles have been created successfully in folder "_shapefiles_".')
        msgBox.exec_()

    def runexp(self):
        self.dlg.out.setText('')
        self.layers = self.canvas.layers()
        self.layer_list = []
        self.layer_list = ['NONE']
        [self.layer_list.append(layer.name()) for layer in self.layers]

        for sect in self.sections:
            eval('self.dlg.sect_' + sect + '.clear()')
            eval('self.dlg.sect_' + sect + '.addItems(self.layer_list)')
            indices = [i for i, s in enumerate(self.layer_list) if sect in s]
            if indices:
                if sect == 'REACTIONS':
                    eval('self.dlg.sect_' + sect + '.setCurrentIndex(indices[1])')
                else:
                    eval('self.dlg.sect_' + sect + '.setCurrentIndex(indices[0])')

        self.dlg.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.dlg.show()

    def cancel(self):
        self.layer_list = []
        self.layer_list = ['NONE']
        for sect in self.sections:
            exec ('self.dlg.sect_' + sect + '.clear()')
        self.dlg.close()

    def toolButtonOut(self):
        self.outEpanetName = QFileDialog.getSaveFileName(None, 'Save File',
                                                         os.path.join(os.path.join(os.path.expanduser('~')),
                                                                      'Desktop'), 'Epanet Inp File (*.inp)')
        self.dlg.out.setText(self.outEpanetName[0])

    def selectOutp(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle('Warning')
        msgBox.setText('Please define Epanet Inp File location.')
        msgBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        msgBox.exec_()
        return True

    def ok(self):
        # Here check if select OK button, get the layer fields
        # Initialize
        # [JUNCTIONS]
        if self.dlg.out.text() == '':
            if self.selectOutp():
                return
        elif os.path.isabs(self.dlg.out.text()) == False:
            if self.selectOutp():
                return

        self.outEpanetName = self.dlg.out.text()

        try:
            f = open(self.outEpanetName, "w")
            f.close()
        except:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Warning')
            msgBox.setText('Please define Epanet Inp File location.')
            msgBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
            msgBox.exec_()
            return

        if not self.layers:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Warning')
            msgBox.setText('No layers selected.')
            msgBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
            msgBox.exec_()
            return
        xypipes_id = []
        xypipesvert = []
        for sect in self.sections:
            exec('sect' + sect + '=[]') in globals(), locals()
            exec('xy' + sect + '=[]') in globals(), locals()
            if eval('self.dlg.sect_' + sect + '.currentText()') != 'NONE':
                # Get layer field names
                indLayerName = self.layer_list.index(eval('self.dlg.sect_' + sect + '.currentText()')) - 1
                provider = self.layers[indLayerName].dataProvider()
                fields = provider.fields()
                field_names = [field.name() for field in fields]
                for elem in self.layers[indLayerName].getFeatures():
                    eval('sect' + sect + '.append(dict(zip(field_names, elem.attributes())))')
                    if any(sect in s for s in self.sections[0:5]):
                        geom = elem.geometry()
                        if self.layers[indLayerName].geometryType() == 0:
                            eval('xy' + sect + '.append(geom.asPoint())')
                        elif self.layers[indLayerName].geometryType() == 1:
                            eval('xy' + sect + '.append(geom.asPolyline())')
                            if sect == 'pipes':
                                if len(geom.asPolyline()) > 2:
                                    for pp in range(len(geom.asPolyline())-2):
                                        xypipes_id.append(elem.attributes()[0])
                                        xypipesvert.append(geom.asPolyline()[pp])
                    if sect == 'junctions':
                        if 'Elevation' not in locals()['sect' + sect][0].keys():
                            QMessageBox.warning(QWidget(), "Message", "Elevation field is missing.")
        # (myDirectory,nameFile) = os.path.split(self.iface.activeLayer().dataProvider().dataSourceUri())
        my_directory = ''
        f = open(self.outEpanetName, 'wt')
        f.write('[TITLE]\n')
        f.write('Export input file via plugin ExportEpanetInpFiles. \n\n')
        f.write('[JUNCTIONS]\n')
        node_i_ds = []
        for i in range(len(locals()['sectjunctions'])):
            node_i_ds.append(locals()['sectjunctions'][i]['ID'])
            f.write(locals()['sectjunctions'][i]['ID'] + '   ' + str(locals()['sectjunctions'][i]['Elevation']) + '\n')
        f.write('\n[RESERVOIRS]\n')
        for i in range(len(locals()['sectreservoirs'])):
            node_i_ds.append(locals()['sectreservoirs'][i]['ID'])
            f.write(locals()['sectreservoirs'][i]['ID'] + '   ' + str(locals()['sectreservoirs'][i]['Head']) + '\n')
        f.write('\n[TANKS]\n')
        for i in range(len(locals()['secttanks'])):
            node_i_ds.append(locals()['secttanks'][i]['ID'])
            if locals()['secttanks'][i]['VolumeCurv'] == None:
                locals()['secttanks'][i]['VolumeCurv'] = ""
            f.write(locals()['secttanks'][i]['ID'] + '   ' + str(locals()['secttanks'][i]['Elevation']) + '   ' + str(locals()['secttanks'][i]['InitLevel'])
                    + '   ' + str(locals()['secttanks'][i]['MinLevel']) + '   ' + str(locals()['secttanks'][i]['MaxLevel']) + '   ' + str(
                locals()['secttanks'][i]['Diameter'])
                    + '   ' + str(locals()['secttanks'][i]['MinVolume']) + '   ' + str(locals()['secttanks'][i]['VolumeCurv']) + '   ' + '\n')
        f.write('\n[PIPES]\n')
        for i in range(len(locals()['sectpipes'])):
            if (locals()['sectpipes'][i]['NodeFrom'] in node_i_ds) and (locals()['sectpipes'][i]['NodeTo'] in node_i_ds):
                f.write(locals()['sectpipes'][i]['ID'] + '   ' + locals()['sectpipes'][i]['NodeFrom']
                        + '   ' + locals()['sectpipes'][i]['NodeTo'] + '   ' + str(locals()['sectpipes'][i]['Length']) + '   ' + str(
                    locals()['sectpipes'][i]['Diameter'])
                        + '   ' + str(locals()['sectpipes'][i]['Roughness']) + '   ' + str(locals()['sectpipes'][i]['MinorLoss']) + '   ' +
                        locals()['sectpipes'][i]['Status'] + '\n')
        f.write('\n[PUMPS]\n')
        for i in range(len(locals()['sectpumps'])):
            if locals()['sectpumps'][i]['Curve'] != 'NULL':
                try:
                    locals()['sectpumps'][i]['Curve'] = 'HEAD ' + locals()['sectpumps'][i]['Curve']
                except:
                    locals()['sectpumps'][i]['Curve'] = 'HEAD '
            else:
                locals()['sectpumps'][i]['Curve'] = ''
            if locals()['sectpumps'][i]['Pattern'] != 'NULL':
                try:
                    locals()['sectpumps'][i]['Pattern'] = 'PATTERN ' + locals()['sectpumps'][i]['Pattern']
                except:
                    locals()['sectpumps'][i]['Pattern'] = "PATTERN "
            else:
                locals()['sectpumps'][i]['Pattern'] = ''
            if locals()['sectpumps'][i]['Power'] != 'NULL':
                try:
                    locals()['sectpumps'][i]['Power'] = 'POWER ' + locals()['sectpumps'][i]['Power']
                except:
                    locals()['sectpumps'][i]['Power'] = "POWER "
            else:
                locals()['sectpumps'][i]['Power'] = ''

            try:
                f.write(locals()['sectpumps'][i]['ID'] + '   ' + locals()['sectpumps'][i]['NodeFrom']
                        + '   ' + locals()['sectpumps'][i]['NodeTo'] + '   ' + locals()['sectpumps'][i]['Curve']
                        + '   ' + str(locals()['sectpumps'][i]['Pattern']) + '   ' + str(locals()['sectpumps'][i]['Power']) + '\n')
            except:
                f.write(locals()['sectpumps'][i]['ID']  +'\n')

        f.write('\n[VALVES]\n')
        if self.dlg.sect_valves.currentText() != 'NONE':
            for i in range(len(locals()['sectvalves'])):
                try:
                    locals()['sectvalves'][i]['NodeFrom'] = locals()['sectvalves'][i]['NodeFrom'] + ''
                except:
                    locals()['sectvalves'][i]['NodeFrom'] = ""

                try:
                    locals()['sectvalves'][i]['NodeTo'] = locals()['sectvalves'][i]['NodeTo'] + ''
                except:
                    locals()['sectvalves'][i]['NodeTo'] = ""
                f.write("{}   {}   {}   {}    {}    {}    {}\n".format(locals()['sectvalves'][i]['ID'], locals()['sectvalves'][i]['NodeFrom'],
                                                                       locals()['sectvalves'][i]['NodeTo'],
                                                                       str(locals()['sectvalves'][i]['Diameter']),
                                                                       locals()['sectvalves'][i]['Type'],
                                                                       str(locals()['sectvalves'][i]['Setting']),
                                                                       str(locals()['sectvalves'][i]['MinorLoss']),locals()['sectvalves'][i]['Description']))

        f.write('\n[DEMANDS]\n')
        for i in range(len(locals()['sectjunctions'])):
            for u in range(int((len(locals()['sectjunctions'][i]) - 2) / 2)):
                if locals()['sectjunctions'][i]['Demand' + str(u + 1)] == 0 and str(
                        locals()['sectjunctions'][i]['Pattern' + str(u + 1)]) == 'None':
                    continue
                if str(locals()['sectjunctions'][i]['Pattern' + str(u + 1)]) == 'NULL' or str(
                        locals()['sectjunctions'][i]['Pattern' + str(u + 1)]) == 'None':
                    locals()['sectjunctions'][i]['Pattern' + str(u + 1)] = ''
                f.write(locals()['sectjunctions'][i]['ID'] + '   ' + str(locals()['sectjunctions'][i]['Demand' + str(u + 1)])
                        + '   ' + str(locals()['sectjunctions'][i]['Pattern' + str(u + 1)]) + '\n')

        f.write('\n[STATUS]\n')
        for i in range(len(locals()['sectSTATUS'])):
            f.write("{}   {}\n".format(locals()['sectSTATUS'][i]['Link_ID'], locals()['sectSTATUS'][i]['Status/Set']))

        f.write('\n[PATTERNS]\n')
        for i in range(len(locals()['sectPATTERNS'])):
            f.write("{}   {}\n".format(locals()['sectPATTERNS'][i]['Pattern_ID'], locals()['sectPATTERNS'][i]['Multiplier']))

        f.write('\n[CURVES]\n')
        for i in range(len(locals()['sectCURVES'])):
            f.write(";{}:\n   {}   {}   {}\n".format(locals()['sectCURVES'][i]['Type'], locals()['sectCURVES'][i]['Curve_ID'],
                                                     str(locals()['sectCURVES'][i]['X-Value']),str(locals()['sectCURVES'][i]['Y-Value'])))

        f.write('\n[CONTROLS]\n')
        for i in range(len(locals()['sectCONTROLS'])):
            f.write("{}\n".format(locals()['sectCONTROLS'][i]['Controls']))

        f.write('\n[RULES]\n')
        for i in range(len(locals()['sectRULES'])):
            f.write("RULE {}\n   {}\n".format(locals()['sectRULES'][i]['Rule_ID'], locals()['sectRULES'][i]['Rule']))

        f.write('\n[ENERGY]\n')
        if locals()['sectENERGY']:
            try: f.write('Global Efficiency   ' + str(locals()['sectENERGY'][0]['GlobalEffi']) + '\n')
            except: pass
            try: f.write('Global Price    ' + str(locals()['sectENERGY'][0]['GlobalPric']) + '\n')
            except: pass
            try: f.write('Demand Charge   ' + str(locals()['sectENERGY'][0]['DemCharge']) + '\n')
            except: pass

        f.write('\n[REACTIONS]\n')
        if locals()['sectREACTIONS']:
            try: f.write('Order Bulk   ' + str(locals()['sectREACTIONS'][0]['OrderBulk']) + '\n')
            except: pass
            try: f.write('Order Tank    ' + str(locals()['sectREACTIONS'][0]['OrderTank']) + '\n')
            except: pass
            try: f.write('Order Wall   ' + str(locals()['sectREACTIONS'][0]['OrderWall']) + '\n')
            except: pass
            try: f.write('Global Bulk   ' + str(locals()['sectREACTIONS'][0]['GlobalBulk']) + '\n')
            except: pass
            try: f.write('Global Wall   ' + str(locals()['sectREACTIONS'][0]['GlobalWall']) + '\n')
            except: pass
            try: f.write('Limiting Potential   ' + str(locals()['sectREACTIONS'][0]['LimPotent']) + '\n')
            except: pass
            try: f.write('Roughness Correlation   ' + str(locals()['sectREACTIONS'][0]['RoughCorr']) + '\n')
            except: pass

        f.write('\n[REACTIONS]\n')
        for i in range(len(locals()['sectREACTIONS_I'])):
            f.write('{}    {}    {} \n'.format(locals()['sectREACTIONS_I'][i]['Type'],
                                               locals()['sectREACTIONS_I'][i]['Pipe/Tank'], str(locals()['sectREACTIONS_I'][i]['Coeff.'])))
        f.write('\n[EMITTERS]\n')
        for i in range(len(locals()['sectEMITTERS'])):
            f.write('{}    {}\n'.format(locals()['sectEMITTERS'][i]['Junc_ID'], str(locals()['sectEMITTERS'][i]['Coeff.'])))

        f.write('\n[SOURCES]\n')
        for i in range(len(locals()['sectSOURCES'])):
            try:
                locals()['sectSOURCES'][i]['Pattern'] = locals()['sectSOURCES'][i]['Pattern']  + ''
            except:
                locals()['sectSOURCES'][i]['Pattern'] = ''
            f.write("{}   {}   {}   {}\n".format(locals()['sectSOURCES'][i]['Node_ID'], locals()['sectSOURCES'][i]['Type'],
                                                                   str(locals()['sectSOURCES'][i]['Strength']),
                                                                   locals()['sectSOURCES'][i]['Pattern']))

        f.write('\n[MIXING]\n')
        for i in range(len(locals()['sectMIXING'])):
            f.write('{}    {}    {} \n'.format(locals()['sectMIXING'][i]['Tank_ID'],
                                               locals()['sectMIXING'][i]['Model'], str(locals()['sectMIXING'][i]['Fraction'])))

        f.write('\n[TIMES]\n')
        if locals()['sectTIMES']:
            try: f.write('Duration   ' + str(locals()['sectTIMES'][0]['Duration']) + '\n')
            except: pass
            try: f.write('Hydraulic Timestep    ' + str(locals()['sectTIMES'][0]['HydStep']) + '\n')
            except: pass
            try: f.write('Quality Timestep   ' + str(locals()['sectTIMES'][0]['QualStep']) + '\n')
            except: pass
            try: f.write('Pattern Timestep   ' + str(locals()['sectTIMES'][0]['PatStep']) + '\n')
            except: pass
            try: f.write('Pattern Start   ' + str(locals()['sectTIMES'][0]['PatStart']) + '\n')
            except: pass
            try: f.write('Report Timestep   ' + str(locals()['sectTIMES'][0]['RepStep']) + '\n')
            except: pass
            try: f.write('Report Start   ' + str(locals()['sectTIMES'][0]['RepStart']) + '\n')
            except: pass
            try: f.write('Start ClockTime   ' + str(locals()['sectTIMES'][0]['StartClock']) + '\n')
            except: pass
            try: f.write('Statistic   ' + str(locals()['sectTIMES'][0]['Statistic']) + '\n')
            except: pass

        f.write('\n[REPORT]\n')
        if locals()['sectREPORT']:
            try: f.write('Status   ' + locals()['sectREPORT'][0]['Status'] + '\n')
            except: pass
            try: f.write('Summary    ' + locals()['sectREPORT'][0]['Summary'] + '\n')
            except: pass
            try: f.write('Page   ' + locals()['sectREPORT'][0]['Page'] + '\n')
            except: pass

        f.write('\n[OPTIONS]\n')
        if locals()['sectOPTIONS']:
            try: f.write('Units   ' + str(locals()['sectOPTIONS'][0]['Units']) + '\n');
            except: pass
            try: f.write('Headloss    ' + str(locals()['sectOPTIONS'][0]['Headloss']) + '\n')
            except: pass
            try: f.write('Specific Gravity   ' + str(locals()['sectOPTIONS'][0]['SpecGrav']) + '\n')
            except: pass
            try: f.write('Viscosity   ' + str(locals()['sectOPTIONS'][0]['Viscosity']) + '\n')
            except: pass
            try: f.write('Trials   ' + str(locals()['sectOPTIONS'][0]['Trials']) + '\n')
            except: pass
            try: f.write('Accuracy   ' + str(locals()['sectOPTIONS'][0]['Accuracy']) + '\n')
            except: pass
            try: f.write('CHECKFREQ   ' + str(locals()['sectOPTIONS'][0]['CheckFreq']) + '\n')
            except: pass
            try: f.write('MAXCHECK   ' + str(locals()['sectOPTIONS'][0]['MaxCheck']) + '\n')
            except: pass
            try: f.write('DAMPLIMIT   ' + str(locals()['sectOPTIONS'][0]['DampLimit']) + '\n')
            except: pass
            try: f.write('Unbalanced   ' + str(locals()['sectOPTIONS'][0]['Unbalanced']) + '\n')
            except: pass
            try: f.write('Pattern   ' + str(locals()['sectOPTIONS'][0]['PatID']) + '\n')
            except: pass
            try: f.write('Demand Multiplier   ' + str(locals()['sectOPTIONS'][0]['DemMult']) + '\n')
            except: pass
            try: f.write('Emitter Exponent   ' + str(locals()['sectOPTIONS'][0]['EmitExp']) + '\n')
            except: pass
            try: f.write('Quality   ' + str(locals()['sectOPTIONS'][0]['Quality']) + '\n')
            except: pass
            try: f.write('Diffusivity   ' + str(locals()['sectOPTIONS'][0]['Diffusivit']) + '\n')
            except: pass
            try: f.write('Tolerance   ' + str(locals()['sectOPTIONS'][0]['Tolerance']) + '\n')
            except: pass

        f.write('\n[COORDINATES]\n')
        for i in range(len(locals()['sectjunctions'])):
            f.write(locals()['sectjunctions'][i]['ID'] + '   ' + str(locals()['xyjunctions'][i][0]) + '   ' + str(locals()['xyjunctions'][i][1]) + '\n')
        for i in range(len(locals()['sectreservoirs'])):
            f.write(locals()['sectreservoirs'][i]['ID'] + '   ' + str(locals()['xyreservoirs'][i][0]) + '   ' + str(locals()['xyreservoirs'][i][1]) + '\n')
        for i in range(len(locals()['secttanks'])):
            f.write(locals()['secttanks'][i]['ID'] + '   ' + str(locals()['xytanks'][i][0]) + '   ' + str(locals()['xytanks'][i][1]) + '\n')

        f.write('\n[VERTICES]\n')

        for l in range(len(xypipes_id)):
                f.write(xypipes_id[l] + '   ' + str(xypipesvert[l][0]) + '   ' + str(xypipesvert[l][1]) + '\n')

        f.write('\n[END]\n')

        f.close()

        self.cancel()
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Export Options')
        msgBox.setText('Export Epanet Inp File "' + self.outEpanetName + '" succesful.')
        msgBox.exec_()

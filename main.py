# (C)Marios Kyriakou 2016
# University of Cyprus, KIOS Research Center for Intelligent Systems and Networks
# Last Update: 2021-02-02
from qgis.PyQt.QtWidgets import (QAction, QFileDialog, QMessageBox, QWidget, QWizard, QWizardPage, QVBoxLayout)
from qgis.PyQt.QtGui import *  # QIcon
from qgis.PyQt.QtCore import *  # QVariant, Qt
from qgis.core import (QgsProject, QgsLayerTreeGroup, QgsCoordinateReferenceSystem, QgsCoordinateTransform)
from qgis.gui import QgsProjectionSelectionTreeWidget
from .Epa2GIS import epa2gis
from . import resources_rc
import sys
import os
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.QtWidgets import QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ExportEpanetInpFiles_dialog_base.ui'))


class ExportEpanetInpFilesDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        QDialog.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        super(ExportEpanetInpFilesDialog, self).__init__(parent)
        self.setupUi(self)


class CrsSelector(QWizard):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.addPage(crs_page(self))
        global import_export
        if import_export == 'Import':
            self.setWindowTitle("IMPORT EPANET INPUT FILE")
        elif import_export == 'Export':
            self.setWindowTitle("EXPORT EPANET INPUT FILE WITH SPECIFIC CRS")

        self.setOption(QWizard.NoCancelButton, True)
        self.setOption(QWizard.NoBackButtonOnLastPage, True)
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)


class crs_page(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        global import_export
        if import_export == 'Import':
            self.setTitle('Project Coordinate System')
            self.setSubTitle('Choosing an appropriate projection for EPANET layers.')
        elif import_export == 'Export':
            self.setTitle('Project Coordinate System')
            self.setSubTitle('Choosing projection for EPANET coordinates.')

        self.selector = QgsProjectionSelectionTreeWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.selector)
        self.setLayout(layout)
        self.selector.crsSelected.connect(self.crs_selected)

    def crs_selected(self):
        self.completeChanged.emit()

    def isComplete(self):
        global result_crs
        result_crs = self.selector.crs()
        return self.selector.crs().isValid()


class ImpEpanet(object):
    def __init__(self, iface):
        # Save a reference to the QGIS iface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.dlg = ExportEpanetInpFilesDialog()
        self.sections = ['junctions', 'tanks', 'pipes', 'pumps', 'reservoirs', 'valves', 'status', 'patterns', 'curves',
                         'controls', 'rules', 'energy', 'reactions', 'reactions_i', 'emitters', 'quality', 'sources',
                         'mixing', 'times', 'report', 'options']

    def initGui(self):
        # Create action
        sys.path.append(os.path.dirname(__file__) + '/impcount.py')

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

        # Get project CRS
        proj_crs = QgsProject.instance().crs().authid()

        # Call selector
        global import_export
        import_export = 'Import'
        self.crs_ui_selector = CrsSelector()
        check = self.crs_ui_selector.exec()
        if not check:
            return

        global result_crs
        self.epsg_crs = result_crs.authid()
        epa2gis(filePath[0], self.epsg_crs)
        # Clear messages
        self.iface.messageBar().clearWidgets()
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Plugin: ImportEpanetInpFiles')
        msgBox.setText('Shapefiles have been created successfully in folder "_shapefiles_".')
        msgBox.exec_()

        # Restore CRS
        QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(proj_crs))

    def runexp(self):

        # Call selector
        global import_export
        import_export = 'Export'
        self.crs_ui_selector = CrsSelector()
        check = self.crs_ui_selector.exec()
        if not check:
            return
        global result_crs
        self.epsg_crs = result_crs.authid()  # "EPSG:6312"

        self.dlg.out.setText('')
        root = QgsProject.instance().layerTreeRoot()

        ch = False
        try:
            activeLayerName = self.iface.activeLayer().name()
        except:
            activeLayerName = ''

        for group in root.children():
            if group.itemVisibilityChecked():
                if group in self.iface.layerTreeView().selectedNodes() or group.name() in activeLayerName:
                    group_ok = group
                    ch = True
                    break

        if not ch:
            try:
                group_ok = root.findGroup(root.children()[0].name())
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle('Export INP File')
                msg.setText("Please check a group.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

        self.layers = []
        try:
            for lyr in group_ok.findLayers():
                if lyr.itemVisibilityChecked():
                    self.layers.append(lyr.layer())
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Export INP File')
            msg.setText("Please check a group.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        # self.layers = [lyr.layer() for lyr in group_ok.findLayers()]  #[layer for layer in QgsProject.instance().mapLayers().values()]#self.canvas.layers()
        self.layer_list = []
        self.layer_list = ['NONE']
        [self.layer_list.append(layer.name()) for layer in self.layers]

        try:
            for sect in self.sections:
                eval(f'self.dlg.sect_{sect}.clear()')
                eval(f'self.dlg.sect_{sect}.addItems(self.layer_list)')
                indices = [i for i, s in enumerate(self.layer_list) if sect in s]
                if indices:
                    if sect == 'REACTIONS':
                        eval(f'self.dlg.sect_{sect}.setCurrentIndex(indices[1])')
                    else:
                        eval(f'self.dlg.sect_{sect}.setCurrentIndex(indices[0])')
        except:
            pass
        # self.dlg.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.dlg.show()

    def cancel(self):
        self.layer_list = []
        self.layer_list = ['NONE']
        for sect in self.sections:
            exec(f'self.dlg.sect_{sect}.clear()')
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
            exec(f'sect{sect}=[]') in globals(), locals()
            exec(f'xy{sect}=[]') in globals(), locals()
            if eval(f'self.dlg.sect_{sect}.currentText()') != 'NONE':
                # Get layer field names
                indLayerName = self.layer_list.index(eval(f"self.dlg.sect_{sect}.currentText()")) - 1
                provider = self.layers[indLayerName].dataProvider()
                fields = provider.fields()
                field_names = [field.name() for field in fields]

                crsSrc = self.layers[indLayerName].crs()
                crsDest = QgsCoordinateReferenceSystem(self.epsg_crs)
                xform = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance())

                for elem in self.layers[indLayerName].getFeatures():
                    eval(f'sect{sect}.append(dict(zip(field_names, elem.attributes())))')
                    if any(sect in s for s in self.sections[0:5]):
                        geom = elem.geometry()
                        geom.transform(xform)
                        if self.layers[indLayerName].geometryType() == 0:
                            geom_points = geom.asPoint()
                            eval('xy' + sect + '.append(geom_points)')
                        elif self.layers[indLayerName].geometryType() == 1:
                            geom_polyline = []
                            try:
                                gg = geom.asPolyline()[1:-1]
                                pnt_lines = geom.asPolyline()[0]
                                for pnt in pnt_lines:
                                    geom_polyline.append(pnt)
                                    # geom_polyline.append(xform.transform(pnt))
                            except:
                                gg = geom.asMultiPolyline()[1:-1]
                                pnt_lines = geom.asMultiPolyline()
                                for pnt in pnt_lines:
                                    geom_polyline.append(pnt)

                            eval(f'xy{sect}.append(geom_polyline)')
                            if sect == 'pipes':
                                if len(pnt_lines[0]) > 2:
                                    for value in pnt_lines[0]:
                                        xypipes_id.append(elem.attributes()[elem.fieldNameIndex('id')])
                                        x = value[0]
                                        y = value[1]
                                        xypipesvert.append([x, y])

                    if sect == 'junctions':
                        if 'elevation' not in locals()[f'sect{sect}'][0].keys():
                            QMessageBox.warning(QWidget(), "Message", "Elevation field is missing.")
        # (myDirectory,nameFile) = os.path.split(self.iface.activeLayer().dataProvider().dataSourceUri())
        my_directory = ''
        f = open(self.outEpanetName, 'wt')
        f.write('[TITLE]\n')
        f.write('Export input file via plugin ImportEpanetInpFiles. \n\n')
        f.write('[JUNCTIONS]\n')
        f.write(';ID              	Elev        	Demand      	Pattern \n')
        node_i_ds = []
        for i in range(len(locals()['sectjunctions'])):
            node_i_ds.append(locals()['sectjunctions'][i]['id'])
            f.write(locals()['sectjunctions'][i]['id'] + '   ' + str(
                locals()['sectjunctions'][i]['elevation']) + '   ;' + str(locals()['sectjunctions'][i]['desc']) + '\n')
        f.write('\n[RESERVOIRS]\n')
        f.write(';ID              	Head        	Pattern     \n')
        for i in range(len(locals()['sectreservoirs'])):
            node_i_ds.append(locals()['sectreservoirs'][i]['id'])
            f.write(
                locals()['sectreservoirs'][i]['id'] + '   ' + str(locals()['sectreservoirs'][i]['head']) + '   ;' + str(
                    locals()['sectreservoirs'][i]['desc']) + '\n')
        f.write('\n[TANKS]\n')
        f.write(
            ';ID              	Elevation   	InitLevel   	MinLevel    	MaxLevel    	Diameter    	MinVol      	VolCurve\n')
        for i in range(len(locals()['secttanks'])):
            node_i_ds.append(locals()['secttanks'][i]['id'])
            if locals()['secttanks'][i]['volumecurv'] == None:
                locals()['secttanks'][i]['volumecurv'] = ""
            f.write(
                locals()['secttanks'][i]['id'] + '   ' + str(locals()['secttanks'][i]['elevation']) + '   ' + str(
                    locals()['secttanks'][i]['initlevel'])
                + '   ' + str(locals()['secttanks'][i]['minlevel']) + '   ' + str(
                    locals()['secttanks'][i]['maxlevel']) + '   ' + str(
                    locals()['secttanks'][i]['diameter'])
                + '   ' + str(locals()['secttanks'][i]['minvolume']) + '   ' + str(
                    locals()['secttanks'][i]['volumecurv']) + '   ;' + str(locals()['secttanks'][i]['desc']) + '\n')
        f.write('\n[PIPES]\n')
        f.write(';ID              	Node1           	Node2           	Length      	Diameter    	Roughness   	MinorLoss   	Status\n')

        for i in range(0, len(locals()['sectpipes'])):
            if (locals()['sectpipes'][i]['nodefrom'] in node_i_ds) and (
                    locals()['sectpipes'][i]['nodeto'] in node_i_ds):
                f.write(str(locals()['sectpipes'][i]['id']) + '   ' + str(locals()['sectpipes'][i]['nodefrom'])
                           + '   ' + str(locals()['sectpipes'][i]['nodeto']) + '   ' + str(
                    locals()['sectpipes'][i]['length']) + '   ' + str(
                    locals()['sectpipes'][i]['diameter'])
                           + '   ' + str(locals()['sectpipes'][i]['roughness']) + '   ' + str(
                    locals()['sectpipes'][i]['minorloss']) + '   ' +str(
                           locals()['sectpipes'][i]['status']) + '   ;' + str(locals()['sectpipes'][i]['desc']) + '\n')
        f.write('\n[PUMPS]\n')
        f.write(';ID              	Node1           	Node2           	Parameters\n')
        for i in range(len(locals()['sectpumps'])):
            if locals()['sectpumps'][i]['curve'] != 'NULL':
                try:
                    locals()['sectpumps'][i]['curve'] = 'head ' + locals()['sectpumps'][i]['curve']
                except:
                    locals()['sectpumps'][i]['curve'] = ''
            else:
                locals()['sectpumps'][i]['curve'] = ''

            if locals()['sectpumps'][i]['power'] != 'NULL':
                try:
                    locals()['sectpumps'][i]['power'] = 'power ' + locals()['sectpumps'][i]['power']
                except:
                    locals()['sectpumps'][i]['power'] = " "
            else:
                locals()['sectpumps'][i]['power'] = ''

            if locals()['sectpumps'][i]['pattern'] != 'NULL':
                try:
                    locals()['sectpumps'][i]['pattern'] = 'pattern ' + locals()['sectpumps'][i]['pattern']
                except:
                    locals()['sectpumps'][i]['pattern'] = ""
            else:
                locals()['sectpumps'][i]['pattern'] = ''

            try:
                f.write(locals()['sectpumps'][i]['id'] + '   ' + locals()['sectpumps'][i]['nodefrom']
                           + '   ' + locals()['sectpumps'][i]['nodeto'] + '   ' + str(
                    locals()['sectpumps'][i]['power'] + '   ' + locals()['sectpumps'][i]['curve']
                    + '   ' + str(locals()['sectpumps'][i]['pattern'])) + '   ;' + str(
                    locals()['sectpumps'][i]['desc']) + '\n')
            except:
                f.write(locals()['sectpumps'][i]['id'] + '\n')

        f.write('\n[VALVES]\n')
        f.write(
            ';ID              	Node1           	Node2           	Diameter    	Type	Setting     	MinorLoss\n')
        if self.dlg.sect_valves.currentText() != 'NONE':
            for i in range(len(locals()['sectvalves'])):
                try:
                    locals()['sectvalves'][i]['nodefrom'] = locals()['sectvalves'][i]['nodefrom'] + ''
                except:
                    locals()['sectvalves'][i]['nodefrom'] = ""

                try:
                    locals()['sectvalves'][i]['nodeto'] = locals()['sectvalves'][i]['nodeto'] + ''
                except:
                    locals()['sectvalves'][i]['nodeto'] = ""

                f.write("{}   {}   {}   {}    {}    {}    {}   {}\n".format(locals()['sectvalves'][i]['id'],
                                                                               locals()['sectvalves'][i]['nodefrom'],
                                                                               locals()['sectvalves'][i]['nodeto'],
                                                                               str(locals()['sectvalves'][i][
                                                                                       'diameter']),
                                                                               locals()['sectvalves'][i]['desc'],
                                                                               str(locals()['sectvalves'][i][
                                                                                       'setting']),
                                                                               str(locals()['sectvalves'][i][
                                                                                       'minorloss']), ';' + str(
                        locals()['sectvalves'][i]['desc'])))

        f.write('\n[DEMANDS]\n')
        f.write(';Junction        	Demand      	Pattern         	Category\n')

        for i in range(len(locals()['sectjunctions'])):
            u = 1
            while True:
                ppat = 'pattern'+str(u)
                ddem = 'demand'+str(u)
                if (ppat in locals()['sectjunctions'][i]) and (ddem in locals()['sectjunctions'][i]):
                    if locals()['sectjunctions'][i][ddem] == 0 and str(locals()['sectjunctions'][i][ppat]) == 'None':
                        continue
                    if str(locals()['sectjunctions'][i][ppat]) == 'NULL' or str(
                            locals()['sectjunctions'][i][ppat]) == 'None':
                        locals()['sectjunctions'][i][ppat] = ''

                    f.write(locals()['sectjunctions'][i]['id'] + '   ' + str(locals()['sectjunctions'][i][ddem])
                            + '   ' + str(locals()['sectjunctions'][i][ppat]) + '\n')
                    u += 1
                else:
                    break

        f.write('\n[STATUS]\n')
        f.write(';ID              	Status/Setting\n')
        for i in range(len(locals()['sectstatus'])):
            try:
                f.write(
                    "{}   {}\n".format(locals()['sectstatus'][i]['link_id'], locals()['sectstatus'][i]['status/set']))
            except: pass

        f.write('\n[PATTERNS]\n')
        f.write(';ID              	Multipliers\n')
        for i in range(len(locals()['sectpatterns'])):
            try:
                f.write("{}   {}\n".format(locals()['sectpatterns'][i]['pattern_id'],
                                          locals()['sectpatterns'][i]['multiplier']))
            except:
                pass

        f.write('\n[CURVES]\n')
        f.write(';ID              	X-Value     	Y-Value\n')
        for i in range(len(locals()['sectcurves'])):
            try:
                f.write(";{}:\n   {}   {}   {}\n".format(locals()['sectcurves'][i]['type'],
                                                            locals()['sectcurves'][i]['curve_id'],
                                                            str(locals()['sectcurves'][i]['x-value']),
                                                            str(locals()['sectcurves'][i]['y-value'])))
            except:
                pass

        f.write('\n[CONTROLS]\n')
        f.write(';------------------------------------------------------------------ \n')
        for i in range(len(locals()['sectcontrols'])):
            try:
                f.write("{}\n".format(locals()['sectcontrols'][i]['controls']))
            except:
                pass

        f.write('\n[RULES]\n')
        f.write(';Rules \n')
        for i in range(len(locals()['sectrules'])):
            try:
                f.write("RULE {}\n   {}\n".format(locals()['sectrules'][i]['rule_id'], locals()['sectrules'][i]['rule']))
            except:
                pass

        f.write('\n[ENERGY]\n')
        if locals()['sectenergy']:
            try:
                f.write('Global Efficiency   ' + str(locals()['sectenergy'][0]['globaleffi']) + '\n')
            except:
                pass

            try:
                f.write('Global Price    ' + str(locals()['sectenergy'][0]['globalpric']) + '\n')
            except:
                pass

            try:
                f.write('Demand Charge   ' + str(locals()['sectenergy'][0]['demcharge']) + '\n')
            except:
                pass

        f.write('\n[REACTIONS]\n')
        f.write(';Type     	Pipe/Tank       	Coefficient\n')
        if locals()['sectreactions']:
            try:
                f.write('Order Bulk   ' + str(locals()['sectreactions'][0]['orderbulk']) + '\n')
            except:
                pass
            try:
                f.write('Order Tank    ' + str(locals()['sectreactions'][0]['ordertank']) + '\n')
            except:
                pass
            try:
                f.write('Order Wall   ' + str(locals()['sectreactions'][0]['orderwall']) + '\n')
            except:
                pass
            try:
                f.write('Global Bulk   ' + str(locals()['sectreactions'][0]['globalbulk']) + '\n')
            except:
                pass
            try:
                f.write('Global Wall   ' + str(locals()['sectreactions'][0]['globalwall']) + '\n')
            except:
                pass
            try:
                f.write('Limiting Potential   ' + str(locals()['sectreactions'][0]['limpotent']) + '\n')
            except:
                pass
            try:
                f.write('Roughness Correlation   ' + str(locals()['sectreactions'][0]['roughcorr']) + '\n')
            except:
                pass

        f.write('\n[REACTIONS]\n')
        f.write(';Reactions\n')
        for i in range(len(locals()['sectreactions_i'])):
            try:
                f.write('{}    {}    {} \n'.format(locals()['sectreactions_I'][i]['desc'],
                                                      locals()['sectreactions_I'][i]['pipe/tank'],
                                                      str(locals()['sectreactions_I'][i]['coeff.'])))
            except:
                pass

        f.write('\n[EMITTERS]\n')
        f.write(';Junction        	Coefficient\n')
        for i in range(len(locals()['sectemitters'])):
            try:
                f.write(
                    '{}    {}\n'.format(locals()['sectemitters'][i]['junc_id'], str(locals()['sectemitters'][i]['coeff.'])))
            except:
                pass

        f.write('\n[SOURCES]\n')
        f.write(';Node            	Type        	Quality     	Pattern\n')
        for i in range(len(locals()['sectsources'])):
            try:
                locals()['sectsources'][i]['pattern'] = locals()['sectsources'][i]['pattern'] + ''
            except:
                locals()['sectsources'][i]['pattern'] = ''
            f.write(
                "{}   {}   {}   {}\n".format(locals()['sectsources'][i]['node_id'], locals()['sectsources'][i]['desc'],
                                             str(locals()['sectsources'][i]['strength']),
                                             locals()['sectsources'][i]['pattern']))

        f.write('\n[MIXING]\n')
        f.write(';Tank            	Model\n')
        for i in range(len(locals()['sectmixing'])):
            try:
                f.write('{}    {}    {} \n'.format(locals()['sectmixing'][i]['tank_id'],
                                                      locals()['sectmixing'][i]['model'],
                                                      str(locals()['sectmixing'][i]['fraction'])))
            except:
                pass

        f.write('\n[TIMES]\n')
        f.write(';Times\n')
        if locals()['secttimes']:
            try:
                f.write('Duration   ' + str(locals()['secttimes'][0]['duration']) + '\n')
            except:
                pass
            try:
                f.write('Hydraulic Timestep    ' + str(locals()['secttimes'][0]['hydstep']) + '\n')
            except:
                pass
            try:
                f.write('Quality Timestep   ' + str(locals()['secttimes'][0]['qualstep']) + '\n')
            except:
                pass
            try:
                f.write('Pattern Timestep   ' + str(locals()['secttimes'][0]['patstep']) + '\n')
            except:
                pass
            try:
                f.write('Pattern Start   ' + str(locals()['secttimes'][0]['patstart']) + '\n')
            except:
                pass
            try:
                f.write('Report Timestep   ' + str(locals()['secttimes'][0]['repstep']) + '\n')
            except:
                pass
            try:
                f.write('Report Start   ' + str(locals()['secttimes'][0]['repstart']) + '\n')
            except:
                pass
            try:
                f.write('Start ClockTime   ' + str(locals()['secttimes'][0]['startclock']) + '\n')
            except:
                pass
            try:
                f.write('Statistic   ' + str(locals()['secttimes'][0]['statistic']) + '\n')
            except:
                pass

        f.write('\n[REPORT]\n')
        f.write(';Report\n')
        if locals()['sectreport']:
            try:
                f.write('Status   ' + locals()['sectreport'][0]['status'] + '\n')
                f.write('Summary    ' + locals()['sectreport'][0]['summary'] + '\n')
                f.write('Page   ' + locals()['sectreport'][0]['page'] + '\n')
            except:
                pass

        f.write('\n[OPTIONS]\n')
        f.write(';Options\n')
        if locals()['sectoptions']:
            try:
                f.write('Units   ' + str(locals()['sectoptions'][0]['units']) + '\n')
            except:
                pass
            try:
                f.write('Headloss    ' + str(locals()['sectoptions'][0]['headloss']) + '\n')
            except:
                pass
            try:
                f.write('Specific Gravity   ' + str(locals()['sectoptions'][0]['specgrav']) + '\n')
            except:
                pass
            try:
                f.write('Viscosity   ' + str(locals()['sectoptions'][0]['viscosity']) + '\n')
            except:
                pass
            try:
                f.write('Trials   ' + str(locals()['sectoptions'][0]['trials']) + '\n')
            except:
                pass
            try:
                f.write('Accuracy   ' + str(locals()['sectoptions'][0]['accuracy']) + '\n')
            except:
                pass
            try:
                f.write('CHECKFREQ   ' + str(locals()['sectoptions'][0]['checkfreq']) + '\n')
            except:
                pass
            try:
                f.write('MAXCHECK   ' + str(locals()['sectoptions'][0]['maxcheck']) + '\n')
            except:
                pass
            try:
                f.write('DAMPLIMIT   ' + str(locals()['sectoptions'][0]['damplimit']) + '\n')
            except:
                pass
            try:
                f.write('Unbalanced   ' + str(locals()['sectoptions'][0]['unbalanced']) + '\n')
            except:
                pass
            try:
                f.write('Pattern   ' + str(locals()['sectoptions'][0]['patid']) + '\n')
            except:
                pass
            try:
                f.write('Demand Multiplier   ' + str(locals()['sectoptions'][0]['demmult']) + '\n')
            except:
                pass
            try:
                f.write('Emitter Exponent   ' + str(locals()['sectoptions'][0]['emitexp']) + '\n')
            except:
                pass
            try:
                f.write('Quality   ' + str(locals()['sectoptions'][0]['quality']) + '\n')
            except:
                pass
            try:
                f.write('Diffusivity   ' + str(locals()['sectoptions'][0]['diffusivit']) + '\n')
            except:
                pass
            try:
                f.write('Tolerance   ' + str(locals()['sectoptions'][0]['tolerance']) + '\n')
            except:
                pass

        f.write('\n[COORDINATES]\n')
        f.write(';Coordinates\n')
        for i in range(len(locals()['sectjunctions'])):
            f.write(locals()['sectjunctions'][i]['id'] + '   ' + str(locals()['xyjunctions'][i][0]) + '   ' + str(
                locals()['xyjunctions'][i][1]) + '\n')
        for i in range(len(locals()['sectreservoirs'])):
            f.write(locals()['sectreservoirs'][i]['id'] + '   ' + str(locals()['xyreservoirs'][i][0]) + '   ' + str(
                locals()['xyreservoirs'][i][1]) + '\n')
        for i in range(len(locals()['secttanks'])):
            f.write(locals()['secttanks'][i]['id'] + '   ' + str(locals()['xytanks'][i][0]) + '   ' + str(
                locals()['xytanks'][i][1]) + '\n')

        f.write('\n[VERTICES]\n')
        f.write(';Vertices\n')
        for i, id in enumerate(xypipes_id):
            f.write(str(id) + '   ' + str(xypipesvert[i][0]) + '   ' + str(xypipesvert[i][1]) + '\n')
        f.write('\n[END]\n')

        f.close()

        self.cancel()
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Export Options')
        msgBox.setText('Export Epanet Inp File "' + self.outEpanetName + '" succesful.')
        msgBox.exec_()

        try:
            os.startfile(self.outEpanetName)
        except:
            pass
# Read Epanet File
import os


def LoadFile(inp):
    global inpname, mm
    mm = []
    inpname = inp

def BinUpdateClass():
    global mm
    mm = getBinInfo()
    return mm

# get Info
def getBinNodeReservoirIndex():
    ind = range(getBinNodeJunctionCount() + 1, getBinNodeJunctionCount() + getBinNodeReservoirCount() + 1)
    return ind

def getBinNodeTankIndex():
    ind = range(getBinNodeJunctionCount() + getBinNodeReservoirCount() + 1, getBinNodeCount() + 1)
    return ind

def getBinNodeDemandPatternID():
    global mm
    return mm[3]

def getBinNodeJunctionCount():
    global mm
    return mm[4]

def getBinNodeReservoirCount():
    global mm
    return mm[7]

def getBinNodeIndex(id):
    node_name_i_d = getBinNodeNameID()
    return node_name_i_d.index(id)

def getBinNodeNameID():
    global mm
    return mm[0] + mm[5] + mm[8]

def getBinNodeJunctionNameID():
    global mm
    return mm[0]

def getBinReservoirNameID():
    global mm
    return mm[5]

def getBinNodeJunctionElevations():
    global mm
    return mm[1]

def getBinNodeReservoirElevations():
    global mm
    return mm[6]

def getBinNodeBaseDemands():
    global mm
    return mm[2]

def getBinNodeBaseDemandsDemSection():
    global mm
    return mm[62], mm[63], mm[64]  # nodeJunctionsDemSection, nodeJunctionsIDDemSection, nodeJunctionsPatDemSection

# Tanks Info
def getBinNodeTankNameID():
    global mm
    return mm[8]

def getBinNodeTankCount():
    return len(getBinNodeTankNameID())

def getBinNodeTankElevations():
    global mm
    return mm[9]

def getBinNodeTankInitialLevel():
    global mm
    return mm[10]

def getBinNodeTankMinimumWaterLevel():
    global mm
    return mm[11]

def getBinNodeTankMaximumWaterLevel():
    global mm
    return mm[12]

def getBinNodeTankDiameter():
    global mm
    return mm[13]

def getBinNodeTankMinimumWaterVolume():
    global mm
    return mm[14]

def getBinNodeTankVolumeCurveID():
    global mm
    return mm[35]

# Get Links Info
def getBinLinkPumpIndex():
    ind = []
    for i in range(getBinLinkPipeCount() + 1, getBinLinkPipeCount() + getBinLinkPumpCount() + 1):
        ind.append(i - 1)
    return ind

def getBinLinkValveIndex():
    ind = []
    for i in range(getBinLinkPipeCount() + getBinLinkPumpCount() + 1, getBinLinkCount() + 1):
        ind.append(i - 1)
    return ind

def getBinLinkIndex(id):
    linkNameID = getBinLinkNameID()
    return linkNameID.index(id)

def getBinLinkNameID():
    global mm
    return mm[15] + mm[22] + mm[27]

def getBinLinkLength():
    ll = getBinLinkPipeLengths()
    for i in range(getBinLinkPipeCount() + 1, getBinLinkCount() + 1):
        ll.append(0)
    return ll

def getBinLinkDiameter():
    ll = getBinLinkPipeDiameters()
    vld = getBinLinkValveDiameters()
    for i in range(getBinLinkPipeCount() + 1, getBinLinkPipeCount() + getBinLinkPumpCount() + 1):
        ll.append(0)
    for i in range(getBinLinkValveCount()):
        ll.append(vld[i])
    return ll

def getBinLinkRoughnessCoeff():
    ll = getBinLinkPipeRoughness()
    for i in range(getBinLinkPipeCount() + 1, getBinLinkCount() + 1):
        ll.append(0)
    return ll

def getBinLinkMinorLossCoeff():
    ll = getBinLinkPipeMinorLoss()
    vld = getBinLinkValveMinorLoss()
    for i in range(getBinLinkPipeCount() + 1, getBinLinkPipeCount() + getBinLinkPumpCount() + 1):
        ll.append(0)
    for i in range(getBinLinkValveCount()):
        ll.append(vld[i])
    return ll

def getBinLinkPipeCount():
    return len(getBinLinkPipeNameID())

def getBinLinkPipeNameID():
    global mm
    return mm[15]

def getBinLinkFromNode():
    global mm
    return mm[16]

def getBinLinkToNode():
    global mm
    return mm[17]

def getBinLinkPipeLengths():
    global mm
    return mm[18]

def getBinLinkPipeDiameters():
    global mm
    return mm[19]

def getBinLinkPipeRoughness():
    global mm
    return mm[20]

def getBinLinkPipeMinorLoss():
    global mm
    return mm[21]

# Get Pumps Info
def getBinLinkPumpCount():
    return len(getBinLinkPumpNameID())

def getBinLinkPumpNameID():
    global mm
    return mm[22]

def getBinLinkPumpPatterns():
    global mm
    return mm[23]

def getBinLinkPumpCurveNameID():
    global mm
    return mm[24]

def getBinLinkPumpPower():
    global mm
    return mm[25]

def getBinLinkPumpNameIDPower():
    global mm
    return mm[26]

def getBinLinkPumpSpeed():
    global mm
    return mm[38]

def getBinLinkPumpPatternsPumpID():
    global mm
    return mm[39]

def getBinLinkValveCount():
    return len(getBinLinkValveNameID())

def getBinLinkValveNameID():
    global mm
    return mm[27]

def getBinLinkValveDiameters():
    global mm
    return mm[28]

def getBinLinkValveType():
    global mm
    return mm[29]

def getBinLinkValveSetting():
    global mm
    return mm[30]

def getBinLinkValveMinorLoss():
    global mm
    return mm[31]

def getBinLinkValveDescription():
    global mm
    return mm[66]

def getBinNodesConnectingLinksID():
    return [mm[16], mm[17]]

def getBinNodesConnectingLinksIndex():
    NodesConnectingLinksID = getBinNodesConnectingLinksID()
    nodeInd = []
    for i in range(getBinLinkCount()):
        nodeInd.append([getBinNodeIndex(NodesConnectingLinksID[0][i]), getBinNodeIndex(NodesConnectingLinksID[1][i])])
    return nodeInd

def getBinLinkCount():
    return getBinLinkPipeCount() + getBinLinkPumpCount() + getBinLinkValveCount()

def getBinNodeCount():
    return getBinNodeJunctionCount() + getBinNodeReservoirCount() + getBinNodeTankCount()

# Status
def getBinLinkInitialStatus():
    global mm
    return mm[32]

def getBinLinkInitialStatusNameID():
    global mm
    return mm[33]

# Curves
def getBinCurvesNameID():
    global mm
    return mm[36]

def getBinCurvesXY():
    global mm
    return mm[37]

def getBinCurveCount():
    global mm
    return len(set(mm[36]))

def getDemandsSection():
    global mm
    return mm[44]

def getStatusSection():
    global mm
    return mm[45]

def getEmittersSection():
    global mm
    return mm[46]

def getControlsSection():
    global mm
    return mm[47]

def getPatternsSection():
    global mm
    return mm[48]

def getCurvesSection():
    global mm
    return mm[49], mm[50]

def getQualitySection():
    global mm
    return mm[51]

def getRulesSection():
    global mm
    return mm[52]

def getSourcesSection():
    global mm
    return mm[53]

def getEnergySection():
    global mm
    return mm[54]

def getReactionsSection():
    global mm
    return mm[55]

def getReactionsOptionsSection():
    global mm
    return mm[56]

def getMixingSection():
    global mm
    return mm[57]

def getTimesSection():
    global mm
    return mm[58]

def getOptionsSection():
    global mm
    return mm[59]

def getReportSection():
    global mm
    return mm[60]

def getLabelsSection():
    global mm
    return mm[61]

# Get all info
def getBinInfo():
    global inpname
    file = open(inpname, 'r')

    nodeJunctionNameID = []
    nodeJunctionElevations = []
    nodeJunctionBaseDemands = []

    nodeJunctionsDemSection = []
    nodeJunctionsIDDemSection = []
    nodeJunctionsPatDemSection = []

    nodePatternNameID = []
    nodeReservoirNameID = []
    nodeReservoirElevations = []

    BinNodeTankNameID = []
    BinNodeTankElevation = []
    BinNodeTankInitLevel = []
    BinNodeTankMinLevel = []
    BinNodeTankMaxLevel = []
    BinNodeTankDiameter = []
    BinNodeTankMinVol = []
    BinNodeTankVolumeCurveID = []

    BinLinkPipeNameID = []
    BinLinkFromNode = []
    BinLinkToNode = []
    BinLinkPipeLengths = []
    BinLinkPipeDiameters = []
    BinLinkPipeRoughness = []
    BinLinkPipeMinorLoss = []

    BinLinkPumpPatterns = []
    BinLinkPumpCurveNameID = []
    BinLinkPumpPower = []
    BinLinkPumpNameIDPower = []
    BinLinkPumpNameID = []
    BinLinkPumpSpeed = []
    BinLinkPumpPatternsPumpID = []


    BinLinkValveNameID = []
    BinLinkValveDiameters = []
    BinLinkValveType = []
    BinLinkValveSetting = []
    BinLinkValveMinorLoss = []
    BinLinkValveDescription = []

    BinLinkInitialStatus = []
    BinLinkInitialStatusNameID = []
    BincountStatuslines = []
    linkNameID = []

    BinCurvesNameID = []
    BinCurvesXY = []

    # Sections
    demandsSection = []
    statusSection = []
    emittersSection = []
    controlsSection = []
    patternsSection = []
    curvesSection = []
    curvesSectionType = []
    qualitySection = []
    rulesSection = []
    rules = []
    sourcesSection = []
    energySection = []
    reactionsSection = []
    reactionsOptionSection = []
    mixingSection = []
    timesSection = []
    optionsSection = []
    reportSection = []
    labelsSection = []

    s1 = file.readline()

    num = 13
    sec = [0] * num
    x = []
    y = []
    nodewithCoords = []
    # Create a list.
    vertx = []
    verty = []
    # Append empty lists in first two indexes.
    sec2 = [0] * num
    ch1 = 0
    ch = 1
    while True:
        if "[" in s1:
            pass
        else:
            s1 = file.readline()
        ok = 0
        if "[END]" in s1:
            # pb.setValue(10)
            file.close()
            return [nodeJunctionNameID, nodeJunctionElevations, nodeJunctionBaseDemands, nodePatternNameID,
                    len(nodeJunctionNameID),  # 01234
                    nodeReservoirNameID, nodeReservoirElevations, len(nodeReservoirNameID),  # 567
                    BinNodeTankNameID, BinNodeTankElevation, BinNodeTankInitLevel, BinNodeTankMinLevel,
                    BinNodeTankMaxLevel, BinNodeTankDiameter, BinNodeTankMinVol,  # 8#9#10#11#12#13#14
                    BinLinkPipeNameID, BinLinkFromNode, BinLinkToNode, BinLinkPipeLengths, BinLinkPipeDiameters,
                    BinLinkPipeRoughness, BinLinkPipeMinorLoss,  # 15#16#17#18#19#20#21
                    BinLinkPumpNameID, BinLinkPumpPatterns, BinLinkPumpCurveNameID, BinLinkPumpPower,
                    BinLinkPumpNameIDPower,  # 22#23#24#25#26
                    BinLinkValveNameID, BinLinkValveDiameters, BinLinkValveType, BinLinkValveSetting,
                    BinLinkValveMinorLoss,  # 27#28#29#30#31
                    BinLinkInitialStatus, BinLinkInitialStatusNameID, BincountStatuslines, BinNodeTankVolumeCurveID,
                    # 32#33#34#35
                    BinCurvesNameID, BinCurvesXY, BinLinkPumpSpeed, BinLinkPumpPatternsPumpID,  # 36#37#38#39
                    x, y, vertx, verty,  # 40#41#42#43
                    demandsSection, statusSection, emittersSection, controlsSection, patternsSection, curvesSection,
                    curvesSectionType,  # 44#45#46#47#48#49#50
                    qualitySection, rulesSection, sourcesSection, energySection, reactionsSection,
                    reactionsOptionSection, mixingSection,  # 51#52#53#54#55#56#57
                    timesSection, optionsSection, reportSection, labelsSection,  # 58#59#60#61
                    nodeJunctionsDemSection, nodeJunctionsIDDemSection, nodeJunctionsPatDemSection, nodewithCoords,BinLinkValveDescription]  # 62#63#64#65#66


        elif "[JUNCTIONS]" in s1:
            sec[0] = 1
            s1 = file.readline()
        elif "[RESERVOIRS]" in s1:
            sec = [0] * num
            sec[1] = 1
            s1 = file.readline()
        elif "[TANKS]" in s1:
            sec = [0] * num
            sec[2] = 1
            s1 = file.readline()
        elif "[PIPES]" in s1:
            sec = [0] * num
            sec[3] = 1
            s1 = file.readline()
        elif "[PUMPS]" in s1:
            sec = [0] * num
            sec[4] = 1
            s1 = file.readline()
        elif "[VALVES]" in s1:
            sec = [0] * num
            sec[5] = 1
            s1 = file.readline()
        if "[STATUS]" in s1:
            sec = [0] * num
            sec2 = [0] * num
            sec[7] = 1
            s1 = file.readline()
            for i in range(0, len(BinLinkPipeNameID) + len(BinLinkPumpNameID) + len(BinLinkValveNameID)):
                vertx.append([])
                verty.append([])
            linknameid = BinLinkPipeNameID + BinLinkPumpNameID + BinLinkValveNameID
        elif "[DEMANDS]" in s1:
            sec = [0] * num
            sec[8] = 1
            s1 = file.readline()
        elif ("[JUNCTIONS]" in s1 or "[RESERVOIRS]" in s1 or "[TANKS]" in s1 or "[PIPES]" in s1 or "[PUMPS]" in s1 or
              "[VALVES]" in s1):
            ok = 1
        elif "[TAGS]" in s1 and ok == 0:
            sec = [0] * num
            s1 = file.readline()
        elif "[PATTERNS]" in s1:
            sec = [0] * num
            sec[6] = 1
            s1 = file.readline()
        elif "[CURVES]" in s1:
            sec = [0] * num
            sec[9] = 1
            s1 = file.readline()
        elif "[CONTROLS]" in s1:
            sec = [0] * num
            sec[10] = 1
            s1 = file.readline()
        elif "[COORDINATES]" in s1:
            sec2 = [0] * num
            sec2[0] = 1
            s1 = file.readline()
        elif "[VERTICES]" in s1:
            sec2 = [0] * num
            sec2[1] = 1
            s1 = file.readline()
        elif "[LABELS]" in s1:
            sec2 = [0] * num
            sec2[12] = 1
            s1 = file.readline()
        elif "[EMITTERS]" in s1:
            sec2 = [0] * num
            sec2[2] = 1
            s1 = file.readline()
        elif "[RULES]" in s1:
            sec = [0] * num
            sec2 = [0] * num
            sec2[3] = 1
            s1 = file.readline()
        elif "[ENERGY]" in s1:
            sec2 = [0] * num
            sec2[6] = 1
            if rules != []:
                rulesSection.append(rules)
            s1 = file.readline()
        elif "[QUALITY]" in s1:
            sec2 = [0] * num
            sec = [0] * num
            sec2[4] = 1
            s1 = file.readline()
        elif "[SOURCES]" in s1:
            sec2 = [0] * num
            sec2[5] = 1
            s1 = file.readline()
        elif "[REACTIONS]" in s1:
            sec2 = [0] * num
            sec2[7] = 1
            s1 = file.readline()
        elif "[MIXING]" in s1:
            sec2 = [0] * num
            sec2[8] = 1
            s1 = file.readline()
        elif "[TIMES]" in s1:
            sec2 = [0] * num
            sec2[9] = 1
            s1 = file.readline()
        elif "[REPORT]" in s1:
            sec2 = [0] * num
            sec2[10] = 1
            s1 = file.readline()
        elif "[OPTIONS]" in s1:
            sec2 = [0] * num
            sec2[11] = 1
            s1 = file.readline()
        elif "[BACKDROP]" in s1:
            sec2 = [0] * num
            s1 = file.readline()
        elif "[" in s1:
            s1 = file.readline()

        if sec[0] == 1:  # JUNCTIONS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    nodeJunctionNameID.append(mm[0])
                    nodeJunctionElevations.append(float(mm[1]))
                    if len(mm) > 2:
                        nodeJunctionBaseDemands.append(float(mm[2]))
                    if len(mm) > 3:
                        if mm[3][0] != ';':
                            nodePatternNameID.append(mm[3])
                        else:
                            nodePatternNameID.append('')
                    else:
                        nodePatternNameID.append('')

        if sec[1] == 1:  # RESERVOIRS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 0:
                if mm[0][0] == ';':
                    pass
                else:
                    nodeReservoirNameID.append(mm[0])
                    nodeReservoirElevations.append(float(mm[1]))
                    if len(mm) > 2:
                        if mm[2][0] != ';':
                            nodePatternNameID.append(mm[2])
                        else:
                            nodePatternNameID.append('')
                    else:
                        nodePatternNameID.append('')

        if sec[2] == 1:  # TANKS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 0:
                if mm[0][0] == ';':
                    pass
                else:
                    BinNodeTankNameID.append(mm[0])
                    BinNodeTankElevation.append(float(mm[1]))
                    BinNodeTankInitLevel.append(float(mm[2]))
                    BinNodeTankMinLevel.append(float(mm[3]))
                    BinNodeTankMaxLevel.append(float(mm[4]))
                    BinNodeTankDiameter.append(float(mm[5]))
                    BinNodeTankMinVol.append(float(mm[6]))
                    nodePatternNameID.append('')
                    if len(mm) > 7:
                        if mm[7][0] != ';':
                            BinNodeTankVolumeCurveID.append(mm[7])
                        else:
                            BinNodeTankVolumeCurveID.append('')
                    else:
                        BinNodeTankVolumeCurveID.append('')

        if sec[3] == 1:  # PIPES
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 0:
                if mm[0][0] == ';':
                    pass
                else:
                    linkNameID.append(mm[0])
                    BinLinkPipeNameID.append(mm[0])
                    BinLinkFromNode.append(mm[1])
                    BinLinkToNode.append(mm[2])
                    BinLinkPipeLengths.append(float(mm[3]))
                    BinLinkPipeDiameters.append(float(mm[4]))
                    BinLinkPipeRoughness.append(float(mm[5]))
                    if len(mm) > 6:
                        BinLinkPipeMinorLoss.append(float(mm[6]))
                    else:
                        BinLinkPipeMinorLoss.append('')
                    if len(mm) > 7:
                        if mm[7][0] != ';':
                            if mm[7] == 'Open':
                                BinLinkInitialStatus.append('OPEN')
                            else:
                                BinLinkInitialStatus.append(mm[7])

        if sec[4] == 1:  # PUMPS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 0:
                if mm[0][0] == ';':
                    pass
                else:
                    linkNameID.append(mm[0])
                    BinLinkPumpNameID.append(mm[0])
                    BinLinkFromNode.append(mm[1])
                    BinLinkToNode.append(mm[2])
                    if len(mm) > 4:
                        if mm[3] == 'HEAD':
                            BinLinkPumpCurveNameID.append(mm[4])
                        elif mm[3] == 'POWER':
                            BinLinkPumpPower.append(float(mm[4]))
                            BinLinkPumpNameIDPower.append(mm[0])
                    if len(mm) > 6:
                        if mm[5][0] != ';':
                            if mm[5] == 'SPEED':
                                BinLinkPumpSpeed.append(mm[6])
                            else:
                                BinLinkPumpPatterns.append(mm[6])
                                BinLinkPumpPatternsPumpID.append(mm[0])

                    if len(mm) > 8:
                        BinLinkPumpPatterns.append(mm[8])
                        BinLinkPumpPatternsPumpID.append(mm[0])

        if sec[5] == 1:  # VALVES
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    linkNameID.append(mm[0])
                    BinLinkValveNameID.append(mm[0])
                    BinLinkFromNode.append(mm[1])
                    BinLinkToNode.append(mm[2])
                    BinLinkValveDiameters.append(float(mm[3]))
                    BinLinkValveType.append(mm[4])
                    BinLinkValveSetting.append(float(mm[5]))
                    BinLinkValveMinorLoss.append(float(mm[6]))
                    if len(mm) > 7:
                        if mm[7][0] != ';':
                            BinLinkValveDescription.append(mm[7])

        if sec[6] == 1:  # PATTERNS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    patternsSection.append([mm[0], ' '.join(mm[1:])])

        if sec[7] == 1:  # STATUS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    statusSection.append(mm)
                    BinLinkInitialStatusNameID.append(mm[0])
                    if mm[1] == 'Open':
                        BinLinkInitialStatus.append('OPEN')
                    else:
                        BinLinkInitialStatus.append(mm[1])
                    BincountStatuslines.append(mm)

        if sec[8] == 1:  # DEMANDS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    nodeJunctionsIDDemSection.append(mm[0])
                    nodeJunctionsDemSection.append(float(mm[1]))
                    try:
                        if mm[2] != ';':
                            nodeJunctionsPatDemSection.append(mm[2])
                        else:
                            nodeJunctionsPatDemSection.append('')
                    except:
                        nodeJunctionsPatDemSection.append('')

                    if mm[-1] == ';':
                        mm[-1] = ''
                        mm.append(';')
                    demandsSection.append(mm)

        if sec[9] == 1:  # CURVES
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0] == ';ID':
                    continue
                elif ";PUMP:" in mm[0].upper():
                    curvesSectionType.append('PUMP')
                elif ";EFFICIENCY:" in mm[0].upper():
                    curvesSectionType.append('EFFICIENCY')
                elif ";VOLUME:" in mm[0].upper():
                    curvesSectionType.append('VOLUME')
                elif ";HEADLOSS:" in mm[0].upper():
                    curvesSectionType.append('HEADLOSS')
                else:
                    curvesSectionType.append('PUMP')
                if mm[0][0] != ';':
                    curvesSection.append(mm)
                    BinCurvesNameID.append(mm[0])
                    BinCurvesXY.append([float(mm[1]), float(mm[2])])

        if sec[10] == 1:  # CONTROLS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    controlsSection.append(' '.join(mm))

        if sec2[0] == 1:  # COORDINATES
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 2:
                if mm[0][0] != ';':
                    nodewithCoords.append(mm[0])
                    x.append(float(mm[1]))
                    y.append(float(mm[2]))

        if sec2[1] == 1:  # VERTICES
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 2:
                if mm[0][0] != ';':
                    linkIndex = linknameid.index(mm[0])
                    vertx[linkIndex].append(float(mm[1]))
                    verty[linkIndex].append(float(mm[2]))


        if sec2[2] == 1:  # EMITTERS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    emittersSection.append(mm)

        if sec2[3] == 1:  # RULES
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    if "RULE" in mm[0].upper():
                        if rules != [] or ch == 0:
                            rulesSection.append(rules)
                            ch = 0
                            rules = []
                            rules.append([s1, mm])
                        else:
                            rules.append([s1, mm])
                    else:
                        rules.append([s1, mm])

        if sec2[4] == 1:  # QUALITY
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    qualitySection.append(mm)

        if sec2[5] == 1:  # SOURCES
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    sourcesSection.append(mm)

        if sec2[6] == 1:  # ENERGY
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    energySection.append(mm)

        if sec2[7] == 1:  # REACTIONS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    if ("ORDER" in mm[0].upper() and ch1 == 0) or ch1 == 1:
                        reactionsOptionSection.append(mm)
                        ch1 = 1
                    else:
                        reactionsSection.append(mm)

        if sec2[8] == 1:  # MIXING
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    mixingSection.append(mm)

        if sec2[9] == 1:  # TIMES
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    timesSection.append(mm)

        if sec2[10] == 1:  # REPORT
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    reportSection.append(mm)

        if sec2[11] == 1:  # OPTIONS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    optionsSection.append(mm)

        if sec2[12] == 1:  # LABELS
            if "[" in s1:
                continue
            mm = s1.split()
            if len(mm) > 1:
                if mm[0][0] == ';':
                    pass
                else:
                    labelsSection.append(mm)


# Node Coordinates
def getBinNodeCoordinates():
    global mm
    return mm[65], mm[40], mm[41], mm[42], mm[43]  # ,mm[44],mm[45],mm[46],mm[47]
    # x,y,x1,y1,x2,y2,vertx,verty] #65#40#41#42#43#44#45#46#47


EN_ELEVATION = 0  # /* Node parameters */
EN_BASEDEMAND = 1
EN_PATTERN = 2
EN_EMITTER = 3
EN_INITQUAL = 4
EN_SOURCEQUAL = 5
EN_SOURCEPAT = 6
EN_SOURCETYPE = 7
EN_TANKLEVEL = 8
EN_DEMAND = 9
EN_HEAD = 10
EN_PRESSURE = 11
EN_QUALITY = 12
EN_SOURCEMASS = 13
EN_INITVOLUME = 14
EN_MIXMODEL = 15
EN_MIXZONEVOL = 16

EN_TANKDIAM = 17
EN_MINVOLUME = 18
EN_VOLCURVE = 19
EN_MINLEVEL = 20
EN_MAXLEVEL = 21
EN_MIXFRACTION = 22
EN_TANK_KBULK = 23

EN_DIAMETER = 0  # /* Link parameters */
EN_LENGTH = 1
EN_ROUGHNESS = 2
EN_MINORLOSS = 3
EN_INITSTATUS = 4
EN_INITSETTING = 5
EN_KBULK = 6
EN_KWALL = 7
EN_FLOW = 8
EN_VELOCITY = 9
EN_HEADLOSS = 10
EN_STATUS = 11
EN_SETTING = 12
EN_ENERGY = 13

EN_DURATION = 0  # /* Time parameters */
EN_HYDSTEP = 1
EN_QUALSTEP = 2
EN_PATTERNSTEP = 3
EN_PATTERNSTART = 4
EN_REPORTSTEP = 5
EN_REPORTSTART = 6
EN_RULESTEP = 7
EN_STATISTIC = 8
EN_PERIODS = 9

EN_NODECOUNT = 0  # /* Component counts */
EN_TANKCOUNT = 1
EN_LINKCOUNT = 2
EN_PATCOUNT = 3
EN_CURVECOUNT = 4
EN_CONTROLCOUNT = 5

EN_JUNCTION = 0  # /* Node types */
EN_RESERVOIR = 1
EN_TANK = 2

EN_CVPIPE = 0  # /* Link types */
EN_PIPE = 1
EN_PUMP = 2
EN_PRV = 3
EN_PSV = 4
EN_PBV = 5
EN_FCV = 6
EN_TCV = 7
EN_GPV = 8

EN_NONE = 0  # /* Quality analysis types */
EN_CHEM = 1
EN_AGE = 2
EN_TRACE = 3

EN_CONCEN = 0  # /* Source quality types */
EN_MASS = 1
EN_SETPOINT = 2
EN_FLOWPACED = 3

EN_CFS = 0  # /* Flow units types */
EN_GPM = 1
EN_MGD = 2
EN_IMGD = 3
EN_AFD = 4
EN_LPS = 5
EN_LPM = 6
EN_MLD = 7
EN_CMH = 8
EN_CMD = 9

EN_TRIALS = 0  # /* Misc. options */
EN_ACCURACY = 1
EN_TOLERANCE = 2
EN_EMITEXPON = 3
EN_DEMANDMULT = 4

EN_LOWLEVEL = 0  # /* Control types */
EN_HILEVEL = 1
EN_TIMER = 2
EN_TIMEOFDAY = 3

EN_AVERAGE = 1  # /* Time statistic types.    */
EN_MINIMUM = 2
EN_MAXIMUM = 3
EN_RANGE = 4

EN_MIX1 = 0  # /* Tank mixing models */
EN_MIX2 = 1
EN_FIFO = 2
EN_LIFO = 3

EN_NOSAVE = 0  # /* Save-results-to-file flag */
EN_SAVE = 1
EN_INITFLOW = 10  # /* Re-initialize flow flag   */

Open = 1
Closed = 0

# Constants for units
FlowUnits = {EN_CFS: "cfs",
             EN_GPM: "gpm",
             EN_MGD: "a-f/d",
             EN_IMGD: "mgd",
             EN_AFD: "Imgd",
             EN_LPS: "L/s",
             EN_LPM: "Lpm",
             EN_MLD: "m3/h",
             EN_CMH: "m3/d",
             EN_CMD: "ML/d"}

# Constants for links
TYPELINK = {EN_CVPIPE: "CV",
            EN_PIPE: "PIPE",
            EN_PUMP: "PUMP",
            EN_PRV: "PRV",
            EN_PSV: "PSV",
            EN_PBV: "PBV",
            EN_FCV: "FCV",
            EN_TCV: "TCV",
            EN_GPV: "GPV"}

# Constants for nodes
TYPENODE = {EN_JUNCTION: "JUNCTION",
            EN_RESERVOIR: "RESERVOIR",
            EN_TANK: "TANK"}

# Constants for controls
TYPECONTROL = {EN_LOWLEVEL: "LOWLEVEL",
               EN_HILEVEL: "HIGHLEVEL",
               EN_TIMER: "TIMER",
               EN_TIMEOFDAY: "TIMEOFDAY"}

# Constants for mixing models
TYPEMIXMODEL = {EN_MIX1: "MIX1",
                EN_MIX2: "MIX2",
                EN_FIFO: "FIFO",
                EN_LIFO: "LIFO"}

# Constants for quality
TYPEQUALITY = {EN_NONE: "NONE",
               EN_CHEM: "CHEM",
               EN_AGE: "AGE",
               EN_TRACE: "TRACE"}

# Constants for sources
TYPESOURCE = {EN_CONCEN: "CONCEN",
              EN_MASS: "MASS",
              EN_SETPOINT: "SETPOINT",
              EN_FLOWPACED: "FLOWPACED"}

# Constants for statistics
TYPESTATS = {EN_NONE: "NONE",
             EN_AVERAGE: "AVERAGE",
             EN_MINIMUM: "MINIMUM",
             EN_MAXIMUM: "MAXIMUM",
             EN_RANGE: "RANGE"}

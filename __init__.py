import svinterface.hdlparse.verilog_parser as vlog

def __getModNames(moduleArr):
    modNameSet = set()
    for mod in moduleArr:
        modNameSet.add(mod.name)
    return modNameSet

def __getParamNames(module):
    paramNameSet = set()
    for p in module.generics:
        paramNameSet.add(p.name)
    return paramNameSet

def __getPortNames(module):
    portNameSet = set()
    for p in module.ports:
        portNameSet.add(p.name)
    return portNameSet

def __searchMod(modName, modArr):
    result = None
    for mod in modArr:
        if (mod.name == modName):
            result = mod
            break
    return result

def __searchParam(paramName, module):
    result = None
    for p in module.generics:
        if (p.name == paramName):
            result = p
            break
    return result

def __searchPort(portName, module):
    result = None
    for p in module.ports:
        if (p.name == portName):
            result = p
            break
    return result

def __checkParams(refMod, testMod):
    errStr = None
    refParams = __getParamNames(refMod)
    testParams = __getParamNames(testMod)

    missingParams = refParams.difference(testParams)
    hasMissing = (len(missingParams) > 0)
    extraParams = testParams.difference(refParams)
    hasExtra = (len(extraParams) > 0)

    badParams = set()
    presentParams = refParams.intersection(testParams)
    for paramName in presentParams:
        refParam = __searchParam(paramName, refMod)
        testParam = __searchParam(paramName, testMod)
        badMode = (refParam.mode != testParam.mode)
        badType = (refParam.data_type != testParam.data_type)
        if (badMode or badType):
            badParams.add(testParam)
    hasBadParams = (len(badParams) > 0)

    hasErrs = (hasMissing or hasExtra or hasBadParams)
    if (hasErrs):
        errStr = '** Param errors for {}:\n'.format(refMod.name)
    if (hasMissing):
        errStr += 'Missing params:\n'
        for p in missingParams:
            errStr += '    {}\n'.format(p)
    if (hasExtra):
        errStr += 'Extra (unspecified) params:\n'
        for p in extraParams:
            errStr += '    {}\n'.format(p)
    if (hasBadParams):
        errStr += 'Incorrect param types:\n'
        for p in badParams:
            errStr += '    {:20}{:8}{}\n'.format(p.name, p.mode, p.data_type)
    return errStr

def __checkPorts(refMod, testMod):
    errStr = None
    refPorts = __getPortNames(refMod)
    testPorts = __getPortNames(testMod)

    missingPorts = refPorts.difference(testPorts)
    hasMissing = (len(missingPorts) > 0)
    extraPorts = testPorts.difference(refPorts)
    hasExtra = (len(extraPorts) > 0)

    badPorts = set()
    presentPorts = refPorts.intersection(testPorts)
    for portName in presentPorts:
        refPort = __searchPort(portName, refMod)
        testPort = __searchPort(portName, testMod)
        badMode = (refPort.mode != testPort.mode)
        badType = (refPort.data_type != testPort.data_type)
        if (badMode or badType):
            badPorts.add(testPort)
    hasBadPorts = (len(badPorts) > 0)

    hasErrs = (hasMissing or hasExtra or hasBadPorts)
    if (hasErrs):
        errStr = '** Port errors for {}:\n'.format(refMod.name)
    if (hasMissing):
        errStr += 'Missing ports:\n'
        for p in missingPorts:
            errStr += '    {}\n'.format(p)
    if (hasExtra):
        errStr += 'Extra (unspecified) ports:\n'
        for p in extraPorts:
            errStr += '    {}\n'.format(p)
    if (hasBadPorts):
        errStr += 'Incorrect port types:\n'
        for p in badPorts:
            errStr += '    {:20}{:8}{}\n'.format(p.name, p.mode, p.data_type)
    return errStr

def checkInterface(refFile, testFile, specificModules=None):
    errMsg = ''
    vlog_ex = vlog.VerilogExtractor()
    vlog_mods_ref = vlog_ex.extract_objects(refFile)
    vlog_mods_test = vlog_ex.extract_objects(testFile)

    # First we check if all modules are there
    modname_ref = __getModNames(vlog_mods_ref)
    # If we specify modules, then we should make sure the reference file has it
    if specificModules:
        missingRef = set(specificModules).difference(modname_ref)
        if (len(missingRef) > 0):
            errMsg += 'FATAL: specified modules not found in reference!'
            for mod in missingRef:
                errMsg += '    ' + str(mod) + '\n'
            return errMsg.strip()
        # Otherwise our new reference set is specified by specificModules
        else:
            modname_ref = set(specificModules)
    modname_test = __getModNames(vlog_mods_test)

    missingMods = modname_ref.difference(modname_test)
    if (len(missingMods) > 0):
        errMsg += 'Missing the following modules:\n'
        for mod in missingMods:
            errMsg += '    ' + str(mod) + '\n'
        errMsg += '\n'

    presentMods = modname_ref.intersection(modname_test)
    for mod in presentMods:
        refMod = __searchMod(mod, vlog_mods_ref)
        testMod = __searchMod(mod, vlog_mods_test)
        paramErr = __checkParams(refMod, testMod)
        portErr = __checkPorts(refMod, testMod)
        if (paramErr):
            errMsg += paramErr
        if (portErr):
            errMsg += portErr
        if (paramErr) or (portErr):
            errMsg += '\n'

    return errMsg.strip()

## Abaqus libraries
from odbAccess import *
import visualization
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

## Any extra supported libraries
import numpy as np
import matplotlib.pyplot as plt

## Name of the .odb file you would like to work with
odbName = 'Job-1.odb'
## Name of the target part (All caps)
partName = 'PART-1'
## Name of the target set
setName = 'SET-1'

## Creating a session
odb = session.openOdb(name=odbName)

## Selecting elements within indicated set
elementSet = odb.rootAssembly.instances[partName].elementSets[setName]
## Selecting nodes within indicated set
nodeSet = odb.rootAssembly.instances[partName].nodeSets[setName]


##############################################################################################
## Here, I defined a dictionary with label of each node as keys and corresponding coordinates as values.
nodeSetCoordinates = dict(map(lambda x : [int(x.label), list(x.coordinates)], nodeSet.nodes))
## Then, I defined a dictionary with label of each element as keys and connectivity of nodes within the element as values.
elementSetConnectivity = dict(map(lambda x : [int(x.label), list(x.connectivity)], elementSet.elements))

## Then, I defined maps the label of each element to its central coordinates (average of connected nodes)
elementSetCoordinates = dict(map(lambda element : [int(element.label), list(np.mean(map(lambda x : np.array(nodeSetCoordinates[x]), element.connectivity), axis = 0))], elementSet.elements))
##############################################################################################


##############################################################################################
## Seleting target step and the frame (here the last frame is selected)
currentFrame = odb.steps['Step-1'].frames[-1]

## Selecting the field variable of choice, if it's available (Here, I chose the stress 'S' and displacement 'U')
stress = currentFrame.fieldOutputs['S']
displacement = currentFrame.fieldOutputs['U']

## Depending on whether the variable is recored for an element or a node, you should select the region accordingly.
stressSet1 = variable.getSubset(region = elementSet)
displacementSet1 = variable.getSubset(region = nodeSet)

## Now you extract different measures of stress from stressSet1.values
## It's a good practice to always print out the object you're not familiar with to check it's attributes
stressSet1maxInPlanePrincipal = map(lambda x : x.maxInPlanePrincipal, stressSet1.values)

odb.close()


#symbolisation des details zonaux 
#symbolisation du bois:
bois = r"shapefile_output\bois\bois.shp"
layer = QgsVectorLayer(bois  , 'bois', 'ogr')
QgsProject.instance().addMapLayer(layer)
# Définir le mtif de hachures
hatch = QgsFillSymbol.createSimple({'style':'solid', 'color':'green'})
# Définir le symbole de remplissage
layer.renderer().setSymbol(hatch)
# Mettre à jour le moteur de rendu pour le calque
layer.triggerRepaint()
# Update renderer
layer.triggerRepaint()
symbol = QgsFillSymbol.createSimple({'color': 'green','outline':'black'})
renderer = QgsSingleSymbolRenderer(symbol)
layer.setRenderer(renderer)



#symbolisation des faubourgs 
faubourg = r"shapefile_output\faubourg\faubourg.shp"
layer = QgsVectorLayer(faubourg, 'faubourg', 'ogr')
QgsProject.instance().addMapLayer(layer)
# Définir le motif de hachures
hatch = QgsFillSymbol.createSimple({'style':'horizontal', 'color':'black'})
symbol = QgsFillSymbol.createSimple({'color': 'red','outline':'red8'})
# Définir le symbole de remplissage
layer.renderer().setSymbol(symbol)
# Mettre à jour le moteur de rendu pour le calque
layer.triggerRepaint()



# symbolisation de la petite cuvette 
cuvette = r"shapefile_output\petite cuvette\petite cuvette.shp"
layer = QgsVectorLayer(cuvette , 'cuvette', 'ogr')
QgsProject.instance().addMapLayer(layer)
# Définir le motif de hachures
hatch = QgsFillSymbol.createSimple({'style':'horizontal', 'color':'blue'})
# Définir le symbole de remplissage
layer.renderer().setSymbol(hatch)
# Mettre à jour le moteur de rendu pour le calque
layer.triggerRepaint()
##########
#traitement des couches lineaires  
#symbolisation des ruisseau temporaire 
layer = r"shapefile_output\ruisseau temporaire\ruisseau temporaire.shp"
layer = QgsVectorLayer(layer, 'riviere', 'ogr')
QgsProject.instance().addMapLayer(layer)
# Créez la couche de symboles pour la ligne 
symbol = QgsLineSymbol.createSimple({'color': 'blue', "width": "0.4" , "line_style" : "dash dot"})
renderer = QgsSingleSymbolRenderer(symbol)
layer.setRenderer(renderer)



# santier lyon  
santier_lyon = r"shapefile_output\santier-layon\santier-layon.shp"
layer = QgsVectorLayer(santier_lyon, 'santier_lyon', 'ogr')
QgsProject.instance().addMapLayer(layer)
# Créez la couche de symboles pour la ligne 
symbol = QgsLineSymbol.createSimple({'color': 'brown', "width": "0.5" , "style" : "solid"})
renderer = QgsSingleSymbolRenderer(symbol)
layer.setRenderer(renderer)
##points 
from qgis.core import QgsSvgMarkerSymbolLayer, QgsSingleSymbolRenderer
#couche de la mosquee 
mosque = r"shapefile_output\mosquee\mosquee.shp"
# Add vector layer
couche = iface.addVectorLayer(mosque, '', 'ogr') 
# Specify the file path to your SVG symbol
svg_path = r"svg\mosquee.svg"
# Create an SVG marker symbol layer
svg_layer = QgsSvgMarkerSymbolLayer(svg_path)
#
svg_layer.setSize(6) 
# Create a marker symbol and add the SVG layer
symbol = QgsMarkerSymbol()
symbol.changeSymbolLayer(0, svg_layer)
# Create a single symbol renderer
renderer = QgsSingleSymbolRenderer(symbol)
# Set the renderer for the layer
couche.setRenderer(renderer)
# Refresh the layer to apply the changes
couche.triggerRepaint()


#couche des oliviers 
olivier =r"shapefile_output\oliviers\oliviers.shp"
# Add vector layer
couche = iface.addVectorLayer(olivier, '', 'ogr') 
# Specify the file path to your SVG symbol
svg_path = r"svg\olivier.svg"
# Create an SVG marker symbol layer
svg_layer = QgsSvgMarkerSymbolLayer(svg_path)
# Create a marker symbol and add the SVG layer
symbol = QgsMarkerSymbol()
symbol.changeSymbolLayer(0, svg_layer)
# Create a single symbol renderer
renderer = QgsSingleSymbolRenderer(symbol)
# Set the renderer for the layer
couche.setRenderer(renderer)
# Refresh the layer to apply the changes
couche.triggerRepaint()


###couche des puits   
olivier = r"shapefile_output\puits\puits.shp"
# Add vector layer
couche = iface.addVectorLayer(olivier, '', 'ogr') 
# Specify the file path to your SVG symbol
svg_path = r"svg\puits.svg"
# Create an SVG marker symbol layer
svg_layer = QgsSvgMarkerSymbolLayer(svg_path)
# Create a marker symbol and add the SVG layer
symbol = QgsMarkerSymbol()
symbol.changeSymbolLayer(0, svg_layer)
# Create a single symbol renderer
renderer = QgsSingleSymbolRenderer(symbol)
# Set the renderer for the layer
couche.setRenderer(renderer)
# Refresh the layer to apply the changes
couche.triggerRepaint()

############################################################################################################################################

# Clase para convertir los datos del ASD a la salida de las bandas de los satélites Sentinel 2 y Landsat
import os
import pandas as pd
import numpy as np
import specdal
import matplotlib.pyplot as plt
#from specdal import Collection, Spectrum, read


class asd():

    """Comenzamos el proceso. En la instanciación vamos a pasar 3 parámetros: La ruta al excel con la Spectral Response de los sensores, la ruta
    a la carpeta donde están los archivos .txt y el satélite del que queremos obetenr la respuesta.
    Ideas: -La ruta a la tabla sensores podría quitarse y dejarla fija seguramente incluso que la lea de la web
           -No solo que trabaje con txt sino que use Specdal para usar directamente archivos .asd"""

    def __init__(self, sensores, spec_path, sat):

        self.sensores = sensores
        self.spec_path = spec_path

        #self.pref = pref

        self.sats = {'S2A': ['MSI', 1], 'S2B': ['MSI', 2], 'L8': ['OLI', 3], 'L9': ['OLI', 4], 'L7': ['ETM+', 7], 'L5': ['TM', 6], 'L4': ['TM', 5]}
        self.sensors = {'MSI':
            {"B1": [np.arange(412, 457), 443, 'Coastal blue'],
            "B2": [np.arange(456, 534), 490, 'Blue'],
            "B3": [np.arange(538, 584), 560, 'Green'],
            "B4": [np.arange(646, 685), 665, 'Red'],
            "B5": [np.arange(695, 715), 705, 'Red edge 1'],
            "B6": [np.arange(731, 760), 740, 'Red edge 2'],
            "B7": [np.arange(769, 798), 783, 'Red edge 3'],
            "B8": [np.arange(760, 908), 842, 'Nir'],
            "B8A": [np.arange(837, 882), 865, 'Nir 8A'],
            "B9": [np.arange(932, 959), 945, 'Water vapour'],
            "B10": [np.arange(1337, 1413), 1375, 'Cirrus'],
            "B11": [np.arange(1539, 1683), 1610, 'Swir 1'],
            "B12": [np.arange(2078, 2321), 2190, 'Swir 2']},
                'OLI': 
            {"B1": [np.arange(435, 451), 443, 'Coastal blue'],
            "B2": [np.arange(452, 512), 482, 'Blue'],
            "B3": [np.arange(533, 590), 562, 'Green'],
            "B8": [np.arange(503, 676), 590, 'Pan'],
            "B4": [np.arange(636, 673), 655, 'Red'],
            "B5": [np.arange(851, 879), 865, 'Nir'],
            "B9": [np.arange(1363, 1384), 1374, 'Cirrus'],
            "B6": [np.arange(1566, 1651), 1609, 'Swir 1'],
            "B7": [np.arange(2107, 2294), 2200, 'Swir 2']},
                'ETM+': 
            {"B1": [np.arange(441, 514), 478, 'Blue'],
            "B2": [np.arange(519, 601), 560, 'Green'],
            "B3": [np.arange(631, 692), 662, 'Red'],
            #"B8": [np.arange(515, 896), 705, 'Pan'],
            "B4": [np.arange(772, 898), 835, 'Nir'],
            "B5": [np.arange(1547, 1749), 1648, 'Swir 1'],
            "B7": [np.arange(2064, 2345), 2205, 'Swir 2']}, 
                'TM':  
            {"B1": [np.arange(441, 514), 478, 'Blue'],
            "B2": [np.arange(519, 601), 560, 'Green'],
            "B3": [np.arange(631, 692), 662, 'Red'],
            "B4": [np.arange(772, 898), 835, 'Nir'],
            "B5": [np.arange(1547, 1749), 1648, 'Swir 1'],
            "B7": [np.arange(2080, 2345), 2205, 'Swir 2']}}
        
        
        self.sat = sat
        if sat not in [i for i in self.sats.keys()]:
            print('Available satellites at the moment are "S2A", "S2B", "L8", "L9", "L7", L5" and "L4"')

        self.sensor = self.sats[self.sat][0]
        print("comenzamos!")
        
        self.sat_data = pd.read_excel(self.sensores, sheet_name=self.sats[self.sat][1]) #Indicamos la hoja del excel sensores en la que está el SRF

    
    def get_spectros(self, pref=None):

        """Suena terrorífico pero la idea es que este método devuelva una lista con los txt que hay en la carpeta y sobre esa lista
        vaya aplicando el proceso en bucle. Ideas:
        -No creo que se deba introducir el nombre de los espectros a mano como se hacía en el ejercicio, porque podemos tener un montón en cada carpeta,
        como mucho se podría indicar el prefijo a eliminar. Con ese en el ejemplo del curso se quiatría "curso" y los espectros se llamarían con el
        número que les toque. Ya luego quien esté analizando esto debería de saber que cosa es cada número. No se me ocurre otra manera"""

        
        specs = [os.path.join(self.spec_path, i.strip(pref)) for i in os.listdir(self.spec_path)]
        return specs  
        

    def txt2sat(self, spectra, name=None, plot=True):

        """La idea de este metodo es meter los archivos de txt con las reflectividades y sacar la respuesta espectral para el satelite elegido.
        Ideas: -Hacer otro para plotear (o plotearlos todos?)"""
        
        
        # Seleccionar la columna 1 de "Wavelength" y la columna 10 que se corresponde con "Vegetacion_fresca_hoja_haz" del dataset ASD
        #data_vegetacion = dataset_ASD[['Wavelength', 'Vegetacion_fresca_hoja_haz']]

        #Habría que hacer un bucle para ejecutar el proceso para cada uno de los espectros de de la carpeta
        # for s in self.get_spectros():

        
        if spectra.endswith('.txt'):
            datos_ASD = pd.read_csv(spectra, sep="\t",  decimal=".")  ##Indicamos que el separador decimal es ,
            #columna = datos_ASD.iloc[:, 1]
        elif spectra.endswith('.asd'):
            s = specdal.Spectrum(filepath = spectra)
            datos_ASD = s.measurement.to_frame()
            datos_ASD.reset_index(inplace=True)
        else:
            print('Sorry, but right now we can only process ".txt" and ".asd" files')
            
            
        
        if name != None:
            datos_ASD.columns = ["Wavelength", name]
        else:
            name = os.path.split(spectra)[1].split('.')[0]
            datos_ASD.columns = ["Wavelength", name]

        #print(datos_ASD)
        
        # Cambiar el nombre de las columnas por el que de cada espectro
        """nombres_columnas = ["Wavelength", "Panel_cal_blanco", "Panel_cal_gris1", "Panel_cal_gris2", "Panel_cal_gris3", 
                            "Baldosa_ceramica", "Baldosa_arcilla_seca", "Baldosa_arcilla_mojada", "Baldosa_arcilla_mojada2", 
                            "Vegetacion_fresca_hoja_haz", "Vegetacion_fresca_hoja_enves", "Vegetacion_fresca_hojas_superpuestas_haz", 
                            "Vegetacion_seca_hoja_haz", "Mezcla_veg_suelo_1", "Mezcla_veg_suelo_2", "Hoja_enferma", "Vegetacion_dosel_1",
                            "Vegetacion_dosel_2", "Materia_organica_seca", "Materia_organica_mojada", "Arena_seca", "Arena_mojada", 
                            "Materia_organica_arena_seca_seca", "Bolsa_negra"]
        dataset_ASD.columns = nombres_columnas"""

        # Eliminar banda < 400 nm
        datos_ASD = datos_ASD[datos_ASD['Wavelength'] >= 400]
        
        #print(datos_ASD)
                    
        
        # Crear una lista para almacenar los data frames cortados
        sat_data_cortados = []
        data_txt_cortados = []
        
        # Realizar el corte en ambos data frames para cada vector
        for banda, rango in self.sensors[self.sensor].items():
            #print(b, r[0]):
            sat_data_cortados.append(self.sat_data[(self.sat_data['SR_WL'] >= min(rango[0])) & (self.sat_data['SR_WL'] <= max(rango[0]))])
            data_txt_cortados.append(datos_ASD[(datos_ASD['Wavelength'] >= min(rango[0])) & (datos_ASD['Wavelength'] <= max(rango[0]))])
            
            
        # Especificar las columnas a mantener para cada data frame
        columnas_a_mantener = [[0, i] for i in range(1, len(self.sensors[self.sensor])+1)]
        
        
        # Aplicar la selección de columnas para cada data frame        
        for i in range(len(self.sensors[self.sensor])):
            sat_data_cortados[i] = sat_data_cortados[i].iloc[:, columnas_a_mantener[i]]
            #data_txt_cortados[i] = data_txt_cortados[i].iloc[:, columnas_a_mantener[i]]        
        
        # Crear una lista para almacenar los resultados de la media ponderada
        resultados_media_ponderada_sat = []
        
        # Realizar la media ponderada para cada par de data frames en las listas
        for i in range(len(self.sensors[self.sensor])):
            peso_sat = sat_data_cortados[i].iloc[:, 1]  # Usamos la segunda columna de data_sentinel_cortados como peso
            datos_txt = data_txt_cortados[i].iloc[:, 1]  # Usamos la segunda columna de data_vegetacion_cortados
        
            # Calcular la media ponderada
            media_ponderada_sat = np.average(datos_txt, weights=peso_sat)
            resultados_media_ponderada_sat.append(media_ponderada_sat)          
        
        # Crear un DataFrame a partir de los resultados de las medias ponderadas
        fname = 'MediaPonderada'+self.sat
        datos_sat_pond = pd.DataFrame({fname: resultados_media_ponderada_sat})        
        
        # Establecer los nombres de fila en el DataFrame
        nombres_filas = [k for k, v in self.sensors[self.sensor].items()]
        datos_sat_pond.index = nombres_filas
        
        # Crear una nueva columna con el centro de las longitudes de onda correspondientes a cada banda 
        wavelength = [v[1] for k, v in self.sensors[self.sensor].items()]
        datos_sat_pond['Wavelength'] = wavelength
        #dataset_Sentinel_L8 = dataset_Sentinel_L8.sort_values(['Wavelength'])
        # Visualizar el DataFrame con los nuevos nombres de fila
        print(datos_sat_pond)
        
        # Ploteamos los datos por defecto cuando estamos haciendo solo un perfil
        # La idea sería pasar plot=False cuando lo hagamos en bucle para todos los archivos de una carpeta
        if plot == True:
            
            # Crear el gráfico
            plt.figure(figsize=(10, 6))
            # Perfil espectral
            plt.plot(datos_ASD['Wavelength'], datos_ASD[name], label=name, color='green')
            # Sat values
            plt.ylim(0, 1)
            plt.plot(datos_sat_pond['Wavelength'], datos_sat_pond[fname], label=fname, color='red')
            plt.xlabel('Wavelength (nm)')
            plt.ylabel('Reflectance')
            title = 'Comparación ASD - ' + self.sat
            plt.title(title)
            plt.legend()
            plt.grid(True)
            plt.show()         
            
            
    def specs2sat(self):
        
        """Aqui habría que crear un dataframe con los valores de las bandas de un satelite para cada uno de los espectros """        
        pass
    
    
    def spec2sats(self):
        
        """Tabla para cada espectro con los valores de las bandas de todos los satélites.
        Hay que decidir si merece la pena meter estos dos como método, porque realmente se puede hacer construyendo la llamada con bucles"""
        pass
    

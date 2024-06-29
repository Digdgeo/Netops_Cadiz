import os
import pandas as pd
import numpy as np
import specdal
import matplotlib.pyplot as plt

class asd():

    def __init__(self, sensores, spec_path, sat):

        """Start the class creating an asd object

        Args:
            sensores (table): path to the provided excel file with the Spectral Response Functions stored_
            spec_path (path): Path to the folder whre spectrum files are stored
            sat (String): Satellite selected to get the expected bands values
        """

        self.sensores = sensores
        self.spec_path = spec_path
        self.sats = { 'S2A': ['MSI', 1, 'mediumblue'],'S2B': ['MSI', 2, 'deepskyblue'],'L8': ['OLI', 3, 'red'],'L9': ['OLI', 4, 'purple'],'L7': ['ETM+', 7, 'darkorange'],
                     'L5': ['TM', 6, 'deeppink'], 'L4': ['TM', 5, 'orchid'], 'SQ': ['Sequoia', 8, 'lime']}
        self.sensors = {'MSI': {"B1": [np.arange(412, 457), 443, 'Coastal blue'], "B2": [np.arange(456, 534), 490, 'Blue'], "B3": [np.arange(538, 584), 560, 'Green'], 
                                "B4": [np.arange(646, 685), 665, 'Red'], "B5": [np.arange(695, 715), 705, 'Red edge 1'], "B6": [np.arange(731, 760), 740, 'Red edge 2'], 
                                "B7": [np.arange(769, 798), 783, 'Red edge 3'], "B8": [np.arange(760, 908), 842, 'Nir'], "B8A": [np.arange(837, 882), 865, 'Nir 8A'], 
                                "B9": [np.arange(932, 959), 945, 'Water vapour'], "B10": [np.arange(1337, 1413), 1375, 'Cirrus'], "B11": [np.arange(1539, 1683), 1610, 'Swir 1'], 
                                "B12": [np.arange(2078, 2321), 2190, 'Swir 2']},
                        'OLI': {"B1": [np.arange(435, 451), 443, 'Coastal blue'], "B2": [np.arange(452, 512), 482, 'Blue'], "B3": [np.arange(533, 590), 562, 'Green'], 
                                "B8": [np.arange(503, 676), 590, 'Pan'], "B4": [np.arange(636, 673), 655, 'Red'], "B5": [np.arange(851, 879), 865, 'Nir'], 
                                "B9": [np.arange(1363, 1384), 1374, 'Cirrus'], "B6": [np.arange(1566, 1651), 1609, 'Swir 1'], "B7": [np.arange(2107, 2294), 2200, 'Swir 2']},
                        'ETM+': {"B1": [np.arange(441, 514), 478, 'Blue'], "B2": [np.arange(519, 601), 560, 'Green'], "B3": [np.arange(631, 692), 662, 'Red'], 
                                 "B4": [np.arange(772, 898), 835, 'Nir'], "B5": [np.arange(1547, 1749), 1648, 'Swir 1'], "B7": [np.arange(2064, 2345), 2205, 'Swir 2']},
                        'TM': {"B1": [np.arange(441, 514), 478, 'Blue'], "B2": [np.arange(519, 601), 560, 'Green'], "B3": [np.arange(631, 692), 662, 'Red'], 
                               "B4": [np.arange(772, 898), 835, 'Nir'], "B5": [np.arange(1547, 1749), 1648, 'Swir 1'], "B7": [np.arange(2080, 2345), 2205, 'Swir 2']},
                       'Sequoia': {"B1": [np.arange(510, 590), 550, 'Green'], "B2": [np.arange(620, 700), 660, 'Red'], "B3": [np.arange(725, 745), 735, 'Red edge 2'], 
                                   "B4": [np.arange(750, 830), 790, 'Nir']}}
        
        self.sat = sat
        if sat not in self.sats:
            print('Available satellites at the moment are "S2A", "S2B", "L8", "L9", "L7", L5" and "L4"')

        self.sensor = self.sats[self.sat][0]
        self.sat_data = pd.read_excel(self.sensores, sheet_name=self.sats[self.sat][1]) #Indicamos la hoja del excel sensores en la que está el SRF

    def get_spectros(self, pref=None):
        
        """Generate a list with the full path of all the txt or asd files in the selected folder (spec_path)

        Args:
            pref (String, optional): String to strip from the full name of the spectrum files. Defaults to None.

        Raises:
            NotADirectoryError: Check is the path is a directory

        Returns:
            List: list with the full path to all the spectrum in the selected folder
        """

        if not os.path.isdir(self.spec_path):
            raise NotADirectoryError(f"The provided path '{self.spec_path}' is not a directory.")
        specs = [os.path.join(self.spec_path, i.strip(pref)) for i in os.listdir(self.spec_path)]
        return specs 

    def spec2sat(self, spectra, name=None, plot=False, save_csv=False, csv_path=None, print_values=False):
        """
        Procesa el espectro para obtener los valores de las bandas especificadas en los sensores satelitales.
        Args:
            spectra (File): archivo .asd o .txt con los valores del espectro.
            name (String, optional): nombre deseado para el espectro ("vegetation", "soil", ...). Defaults to None.
            plot (bool, optional): Selecciona si deseas graficar tus datos. Defaults to True.
            save_csv (bool, optional): Selecciona si deseas guardar los valores de las bandas satelitales esperadas en un csv. Defaults to False.
            csv_path (Path, optional): Ruta para guardar el archivo csv. Defaults to None.
            print_values (bool, optional): Selecciona si deseas imprimir los valores de las bandas. Defaults to True.
        Returns:
            DataFrame: DataFrame con los valores esperados de las bandas satelitales.
        """
        # Reading data using pandas when input is a txt file and Specdal in case input is a asd file
        if spectra.endswith('.txt'):
            try:
                datos_ASD = pd.read_csv(spectra, sep="\t", decimal=".", encoding='utf-8', on_bad_lines='skip')
            except UnicodeDecodeError:
                datos_ASD = pd.read_csv(spectra, sep="\t", decimal=".", encoding='latin1', on_bad_lines='skip')
        elif spectra.endswith('.asd'):
            s = specdal.Spectrum(filepath=spectra)
            datos_ASD = s.measurement.to_frame()
            datos_ASD.reset_index(inplace=True)
        else:
            print('Sorry, but right now we can only process ".txt" and ".asd" files')
            return None
    
        if name:
            datos_ASD.columns = ["Wavelength", name]
        else:
            name = os.path.split(spectra)[1].split('.')[0]
            datos_ASD.columns = ["Wavelength", name]

        # Creating the final DF and exluding values below 400 nanometers
        datos_ASD = datos_ASD[datos_ASD['Wavelength'] >= 400]

        # Lists to store the data
        sat_data_cortados = []
        data_txt_cortados = []

        # Filling the lists with the data 
        for banda, rango in self.sensors[self.sensor].items():
            sat_data_cortados.append(self.sat_data[(self.sat_data['SR_WL'] >= min(rango[0])) & (self.sat_data['SR_WL'] <= max(rango[0]))])
            data_txt_cortados.append(datos_ASD[(datos_ASD['Wavelength'] >= min(rango[0])) & (datos_ASD['Wavelength'] <= max(rango[0]))])

        # Creating a list with the columns depending on the chosen satellite 
        columnas_a_mantener = [[0, i] for i in range(1, len(self.sensors[self.sensor]) + 1)]

        # Filling bands with values within the spectrum parts
        for i in range(len(self.sensors[self.sensor])):
            sat_data_cortados[i] = sat_data_cortados[i].iloc[:, columnas_a_mantener[i]]

        # List to store the weigthed mean
        resultados_media_ponderada_sat = []

        # Filling the weighthed data
        for i in range(len(self.sensors[self.sensor])):
            peso_sat = sat_data_cortados[i].iloc[:, 1]
            datos_txt = data_txt_cortados[i].iloc[:, 1]
            media_ponderada_sat = np.average(datos_txt, weights=peso_sat)
            resultados_media_ponderada_sat.append(media_ponderada_sat)

        # Creating the final DF
        fname = 'MediaPonderada' + self.sat
        datos_sat_pond = pd.DataFrame({fname: resultados_media_ponderada_sat})
        nombres_filas = [k for k, v in self.sensors[self.sensor].items()]
        datos_sat_pond.index = nombres_filas
        wavelength = [v[1] for k, v in self.sensors[self.sensor].items()]
        datos_sat_pond['Wavelength'] = wavelength

        # Print band values. Not really needed since returned in the method
        if print_values:
            print(datos_sat_pond)

        # Saving to csv
        if save_csv and csv_path:
            datos_sat_pond.to_csv(csv_path, index=True)
            print(f'Data saved to {csv_path}')

        # Plotting
        if plot:
            plt.figure(figsize=(10, 6))
            plt.plot(datos_ASD['Wavelength'], datos_ASD[name], label=name, color='green')
            plt.ylim(0, 1)
            plt.plot(datos_sat_pond['Wavelength'], datos_sat_pond[fname], label=fname, color='red')
            plt.xlabel('Wavelength (nm)')
            plt.ylabel('Reflectance')
            title = 'Comparación ASD - ' + self.sat
            plt.title(title)
            plt.legend()
            plt.grid(True)
            plt.show()
    
        return datos_sat_pond  # Return the DataFrame with expected values



    def plotSpecs(self, spectra_list, names=None, plot_expected=True, sats=None, print_values=False):

        """Method to plot several spectrums and satellite expected response together in the same graphic

        Args:
            spectra_list (List): List with the full path to the desired spectrums
            names (List, optional): List with the names for each spectrum in the list. Defaults to None.
            plot_expected (bool, optional): Select if you want to plot the expected values for some satellites. Defaults to True.
            sats (List, optional): List with the names of the satellite that you want to plot. Defaults to None.
            print_values (bool, optional): Select if you also want to see the bands values printed. Defaults to False.
        """

        if sats is None:
            sats = [self.sat]  # Plot expected data for the satellite specified during initialization by default

        plt.figure(figsize=(10, 6))
        for i, spectra in enumerate(spectra_list):
            name = names[i] if names and i < len(names) else None
            if spectra.endswith('.txt'):
                try:
                    datos_ASD = pd.read_csv(spectra, sep="\t", decimal=".", encoding='utf-8', on_bad_lines='skip')
                except UnicodeDecodeError:
                    datos_ASD = pd.read_csv(spectra, sep="\t", decimal=".", encoding='latin1', on_bad_lines='skip')
                name = os.path.split(spectra)[1].split('.')[0] if not name else name
                plt.plot(datos_ASD['Wavelength'], datos_ASD.iloc[:, 1], label=name)
            elif spectra.endswith('.asd'):
                s = specdal.Spectrum(filepath=spectra)
                datos_ASD = s.measurement.to_frame()
                datos_ASD.reset_index(inplace=True)
                name = os.path.split(spectra)[1].split('.')[0] if not name else name
                plt.plot(datos_ASD.iloc[:, 0], datos_ASD.iloc[:, 1], label=name)
            else:
                print(f'Skipping unsupported file format: {spectra}')
                continue

            if plot_expected:
                for sat in sats:
                    original_sat = self.sat  # Save the original satellite to restore later
                    self.sat = sat  # Temporarily set the satellite
                    self.sensor = self.sats[self.sat][0]
                    self.sat_data = pd.read_excel(self.sensores, sheet_name=self.sats[self.sat][1])

                    expected_data = self.spec2sat(spectra, name=name, plot=False, print_values=print_values)
                    color = self.sats[sat][2]
                    plt.plot(expected_data['Wavelength'], expected_data[f'MediaPonderada{self.sat}'], '--', label=f'Expected {self.sat} - {name}', color=color)
                    self.sat = original_sat  # Restore the original satellite
                    self.sensor = self.sats[self.sat][0]
                    self.sat_data = pd.read_excel(self.sensores, sheet_name=self.sats[self.sat][1])

        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Reflectance')
        plt.title('Comparación de múltiples perfiles espectrales')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def satTable(self, output_path):

        """Create a table with the values for all the spectrums with one selected satellite

        Args:
            output_path (Path): Path to store the csv with the values

        Raises:
            NotADirectoryError: _description_
        """

        if not os.path.isdir(os.path.dirname(output_path)):
            raise NotADirectoryError(f"The directory '{os.path.dirname(output_path)}' does not exist.")

        spectros = self.get_spectros()
        all_data = []

        for spectra in spectros:
            name = os.path.split(spectra)[1].split('.')[0]
            datos_sat_pond = self.spec2sat(spectra, name=name, plot=False, save_csv=False, print_values=False)
            datos_sat_pond = datos_sat_pond.rename(columns={f'MediaPonderada{self.sat}': name})
            all_data.append(datos_sat_pond[name])

        all_data_df = pd.concat(all_data, axis=1)
        all_data_df.to_csv(output_path, index=True)
        print(f'Data saved to {output_path}')

    def specsTable(self, output_dir):

        """Generate a csv for each spectrum with the expected bands values for all the satellites available

        Args:
            output_dir (Path): Path to store the csv files

        Raises:
            NotADirectoryError: Error message in case the path provided is not valid
        """

        if not os.path.isdir(output_dir):
            raise NotADirectoryError(f"The provided output directory '{output_dir}' does not exist.")

        spectros = self.get_spectros()
        for spectra in spectros:
            name = os.path.split(spectra)[1].split('.')[0]
            all_sat_data = []

            for sat in self.sats.keys():
                original_sat = self.sat
                self.sat = sat
                self.sensor = self.sats[self.sat][0]
                self.sat_data = pd.read_excel(self.sensores, sheet_name=self.sats[self.sat][1])

                datos_sat_pond = self.spec2sat(spectra, name=name, plot=False, save_csv=False, print_values=False)
                datos_sat_pond = datos_sat_pond.rename(columns={f'MediaPonderada{self.sat}': sat})
                all_sat_data.append(datos_sat_pond[sat])

                self.sat = original_sat
                self.sensor = self.sats[self.sat][0]
                self.sat_data = pd.read_excel(self.sensores, sheet_name=self.sats[self.sat][1])

            all_sat_data_df = pd.concat(all_sat_data, axis=1)
            output_path = os.path.join(output_dir, f'{name}_all_sats.csv')
            all_sat_data_df.to_csv(output_path, index=True)
            print(f'Data saved to {output_path}')


    def ndiCalc(self, spec_path, b1, b2):
        
        """
        Method to calculate Normalized Difference Index between 2 parts of the spectrums and its
        equivalents bands in the satellites.
    
        Args:
            spec_path (Path): Full path to the txt or asd spectrum file.
            b1 (List): List with the band 1 string name of the band/spectrum part, and lower and upper thresholds.
            b2 (List): List with the band 2 string name of the band/spectrum part, and lower and upper thresholds.
    
        Returns:
            Dict: Dict with the NDI values for the spectrum and all the satellites.
        """
    
        b1_name, b1_lower, b1_upper = b1
        b2_name, b2_lower, b2_upper = b2
    
        # Definir band_name_mapping dentro del método
        band_name_mapping = {
            'MSI': {
                'Coastal blue': 'B1',
                'Blue': 'B2',
                'Green': 'B3',
                'Red': 'B4',
                'Red edge 1': 'B5',
                'Red edge 2': 'B6',
                'Red edge 3': 'B7',
                'Nir': 'B8',
                'Nir 8A': 'B8A',
                'Water vapour': 'B9',
                'Cirrus': 'B10',
                'Swir 1': 'B11',
                'Swir 2': 'B12'
            },
            'OLI': {
                'Coastal blue': 'B1',
                'Blue': 'B2',
                'Green': 'B3',
                'Red': 'B4',
                'Nir': 'B5',
                'Cirrus': 'B9',
                'Swir 1': 'B6',
                'Swir 2': 'B7'
            },
            'ETM+': {
                'Blue': 'B1',
                'Green': 'B2',
                'Red': 'B3',
                'Nir': 'B4',
                'Swir 1': 'B5',
                'Swir 2': 'B7'
            },
            'TM': {
                'Blue': 'B1',
                'Green': 'B2',
                'Red': 'B3',
                'Nir': 'B4',
                'Swir 1': 'B5',
                'Swir 2': 'B7'
            },
            'Sequoia': {
                'Green': 'B1',
                'Red': 'B2',
                'Red edge 2': 'B3',
                'Nir': 'B4'
            }
        }
    
        # Empty dicts
        espectro_ndi = {}
        sat_ndis = {}
    
        # Spec values NOT self.sats
        try:
            # Reading spectrum
            if spec_path.endswith('.txt'):
                try:
                    datos_ASD = pd.read_csv(spec_path, sep="\t", decimal=".", encoding='utf-8', on_bad_lines='skip')
                except UnicodeDecodeError:
                    datos_ASD = pd.read_csv(spec_path, sep="\t", decimal=".", encoding='latin1', on_bad_lines='skip')
            elif spec_path.endswith('.asd'):
                s = specdal.Spectrum(filepath=spec_path)
                datos_ASD = s.measurement.to_frame()
                datos_ASD.reset_index(inplace=True)
            else:
                print('Sorry, but right now we can only process ".txt" and ".asd" files')
                return None
    
            # Rename Columns
            name = os.path.split(spec_path)[1].split('.')[0]
            datos_ASD.columns = ["Wavelength", name]
    
            # Selecting spectrum part between selected wavelengths 
            b1_espectro = datos_ASD[(datos_ASD['Wavelength'] >= b1_lower) & (datos_ASD['Wavelength'] <= b1_upper)]
            b2_espectro = datos_ASD[(datos_ASD['Wavelength'] >= b2_lower) & (datos_ASD['Wavelength'] <= b2_upper)]
    
            if b1_espectro.empty or b2_espectro.empty:
                raise ValueError(f"Cannot find data for the specified wavelength ranges: {b1_lower}-{b1_upper}, {b2_lower}-{b2_upper}")
    
            # Spectrum mean
            valor_b1_espectro = b1_espectro[name].mean()
            valor_b2_espectro = b2_espectro[name].mean()
    
            # Spectrum NDI
            ndi_espectro = (valor_b1_espectro - valor_b2_espectro) / (valor_b1_espectro + valor_b2_espectro)
            #print(f"NDI del espectro: {ndi_espectro}")
    
            # Saving spectrum NDI
            espectro_ndi['Espectro'] = ndi_espectro
    
        except Exception as e:
            print(f"Error durante la obtención de valores del espectro: {e}")
            espectro_ndi['Espectro'] = None
    
        # Save original vals for sat y sensor
        original_sat = self.sat
        original_sensor = self.sensor
    
        # Getting satellite data
        try:
            for sat, (sensor, sheet, color) in self.sats.items():
                self.sensor = sensor
                self.sat = sat
                self.sat_data = pd.read_excel(self.sensores, sheet_name=sheet)
    
                # Applying spec2sat to get values
                sat_vals = self.spec2sat(spec_path, plot=False, print_values=False)
                #print(f"sat_vals para {self.sat}:\n{sat_vals}")
    
                # Mapping names
                b1_real_name = band_name_mapping[sensor].get(b1_name)
                b2_real_name = band_name_mapping[sensor].get(b2_name)
    
                if b1_real_name is None or b2_real_name is None:
                    print(f"Cannot find band names: {b1_name}, {b2_name} for sensor {sensor}")
                    continue
    
                # Getting sat bands values
                valor_b1_sat = sat_vals.loc[b1_real_name, 'MediaPonderada' + self.sat]
                valor_b2_sat = sat_vals.loc[b2_real_name, 'MediaPonderada' + self.sat]
    
                # NDI Calculation
                ndi_sat = (valor_b1_sat - valor_b2_sat) / (valor_b1_sat + valor_b2_sat)
                sat_ndis[sat] = ndi_sat
                #print(f"NDI para {self.sat}: {ndi_sat}")
    
        except Exception as e:
            print(f"Error durante la obtención de valores de los satélites: {e}")
    
        finally:
            # Restart params
            self.sat = original_sat
            self.sensor = original_sensor
            self.sat_data = pd.read_excel(self.sensores, sheet_name=self.sats[self.sat][1])  # Restaurar self.sat_data también
    
        # Merging dicts with spec and sats NDI
        ndi_values = {**espectro_ndi, **sat_ndis}
    
        return ndi_values
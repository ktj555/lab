class Material:
    def __init__(self,info):
        self.Density=info['Density']
        self.Temperature=info['Temperature']
        self.Conductivity=info['Conductivity']
        self.Specificheat=info['Specificheat']

class Fluid(Material):
    def __init__(self,info):
        '''
        info : dict
        info's key : ['Density', 'Temperature', 'Conducitivity', 'Specificheat', 'Viscosity', 'Pressure']
        '''
        super().__init__(info)
        self.Viscosity=info['Viscosity']
        self.Pressure=info['Pressure']

class Solid(Material):
    def __init__(self,info):
        '''
        info : dict
        info's key : ['Density', 'Temperature', 'Conducitivity', 'Specificheat']
        '''
        super().__init__(info)

class SemiConductor(Material):
    def __init__(self,info):
        '''
        info : dict
        info's key : ['SeeBeck', 'Conducitivity', 'Resistance', 'SeeBecktype', 'Conductivitytype', 'Resistancetype']
        '''
        self.Seebeck=info['Seebeck']
        self.Conductivity=info['Conductivity']
        self.Resistance=info['Resistance']

        self.Seebecktype=info['Seebecktype']
        self.Conductivitytype=info['Conductivitytype']
        self.Resistancetype=info['Resistancetype']
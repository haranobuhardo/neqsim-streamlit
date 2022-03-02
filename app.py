import streamlit as st

from neqsim.neqsimpython import neqsim
from neqsim.thermo.thermoTools import fluid, phaseenvelope, TPflash, printFrame, dewt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

ThermodynamicOperations = neqsim.thermodynamicOperations.ThermodynamicOperations

def phaseenvelope(testSystem, plot=False):
    testFlash = ThermodynamicOperations(testSystem.clone())
    testFlash.calcPTphaseEnvelope()
    data = testFlash

    fig, ax = plt.subplots()
    ax.set_title('PT envelope')
    ax.set_xlabel('Temperature [K]')
    ax.set_ylabel('Pressure [bar]')
    ax.legend()
    if(plot):
        ax.plot(list(data.getOperation().get("dewT") ),list(data.getOperation().get("dewP")), label="dew point")
        ax.plot(list(data.getOperation().get("bubT")),list(data.getOperation().get("bubP")), label="bubble point")

        try:
            ax.plot(list(data.getOperation().get("dewT2")),list(data.getOperation().get("dewP2")), label="dew point2")
        except:
            pass
            #print("An exception occurred")

        try:
            ax.plot(list(data.getOperation().get("bubT2")),list(data.getOperation().get("bubP2")), label="bubble point2")
        except:
            pass
            #print("An exception occurred")
        
        
        # ax.legend()
        
    return fig


with st.sidebar:
    st.header('Dew Point and Phase Diagram Simulator with NEQSIM')
    num_of_compound = int(st.number_input('Number of component', 0, 10, 5))
    pressure_bara = st.number_input('Pressure (bara)', 0.0, 1000.0, 1.0)
    temperature_degC = st.number_input('Temperature (degC)', 0.0, 1000.0, 30.0)
    st.subheader('Created by Hardo')

col1, col2 = st.columns(2)

data_dict = defaultdict(lambda: defaultdict())


default_value = {
    'compound_1' : {'amount': 47.9450, 'name':'H2S'},
    'compound_2' : {'amount': 46.2990, 'name':'CO2'},
    'compound_3' : {'amount': 5.7490, 'name':'water'},
    'compound_4' : {'amount': 0.0060, 'name':'methane'},
    'compound_5' : {'amount': 0.0010, 'name':'ethane'},
}

with col2:
    for i in range(1, num_of_compound + 1):
        val = default_value.get('compound_' + str(i), {}).get('amount', 0.0)
        data_dict['compound_' + str(i)]['amount'] = st.number_input('%Vol. Amount ' + str(i), 0.0, 100.0, value=val)
with col1:
    for i in range(1, num_of_compound + 1):
        val = default_value.get('compound_' + str(i), {}).get('name', '')
        data_dict['compound_' + str(i)]['name'] = st.text_input('Compound ' + str(i), val)

fluid1 = fluid('SRK-EoS')

for i in range(1, num_of_compound + 1):
    try:
        if (len(data_dict['compound_' + str(i)]['name']) > 0 and data_dict['compound_' + str(i)]['amount'] > 0):
            fluid1.addComponent(data_dict['compound_' + str(i)]['name'], data_dict['compound_' + str(i)]['amount'])
    except Exception as e:
        st.exception(e)
        pass

fluid1.autoSelectMixingRule()

fluid1.setTemperature(temperature_degC, "C")
fluid1.setPressure(pressure_bara, "bara")

st.markdown('***')
st.title('Result')
st.pyplot(phaseenvelope(fluid1, True))
TPflash(fluid1)
# printFrame(fluid1)

dewPointT = dewt(fluid1)-273.15
# print(fluid1.Pressure)
print("dew point T ", dewPointT, " °C")
st.write('Dew Point:')
st.write(str(dewPointT) + " °C")
st.markdown('***')
try:
    st.text(pd.DataFrame(fluid1.createTable("")).to_string(header=False, index=False))
except:
    pass
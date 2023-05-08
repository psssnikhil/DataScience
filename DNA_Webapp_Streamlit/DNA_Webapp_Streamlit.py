import pandas as pd 
import streamlit as st ##for ui
import altair as alt
from PIL import Image #img



image=Image.open('logo.jpeg')
st.image(image,use_column_width=True)
st.write("""
# Testing Webapp with Streamlit


Count DNA composition with this APP
***""")

st.header('Enter DNA Seq')

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"


seq=st.text_area("SEQ INP",sequence_input,height=200)
seq=seq.splitlines()[1:]
seq="".join(seq)

st.write("""
***
***
""")

st.header('INPUT DNA Query')
seq

st.header('Output Count')
st.subheader('Print Dict')

def Count_Dna(seq):
    d = dict([
            ('A',seq.count('A')),
            ('T',seq.count('T')),
            ('G',seq.count('G')),
            ('C',seq.count('C'))
            ])
    return d
out=Count_Dna(seq)
out

### 2. Print text
st.subheader('2. Print text')
st.write('There are  ' + str(out['A']) + ' adenine (A)')
st.write('There are  ' + str(out['T']) + ' thymine (T)')
st.write('There are  ' + str(out['G']) + ' guanine (G)')
st.write('There are  ' + str(out['C']) + ' cytosine (C)')


### 3. Display DataFrame
df=pd.DataFrame.from_dict(out,orient="index")
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'nucleotide'})
st.write(df)

### 4. Display Bar Chart using Altair
st.subheader('4. Display Bar chart')

cha=alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
cha=cha.properties(
    width=alt.Step(100)

)
st.write(cha)

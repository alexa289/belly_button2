# import dependencies
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
import json
from flask import Flask, render_template, jsonify, request, redirect

#Setup the Flask

app = Flask(__name__)

#Setup sqlite DB
engine = create_engine("sqlite:///Data/belly_button_biodiversity.sqlite", echo=False)
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect = True)

# Print all of the classes mapped to the Base
Base.classes.keys()

# mapped classes are now created with names by default
# matching that of the tables names
Otu = Base.classes.otu
Samples = Base.classes.samples
Samples_Metadata = Base.classes.samples_metadata

#Create python session to DB
session = Session(engine)

#Setup Flask Routes
@app.route("/")
def home():
    print("WELCOME TO THE BELLY BUTTON BIODIVERSITY HOMEPAGE!< br/>"
          "Please find below the available routes:<br/"
          "/names<br/>"
          "/otu<br/>"
          "/metadata/<sample><br/>"
          "/wfreq/<sample><br/>"
          "/samples/<sample>")
    return(render_template("index.html"))

@app.route('/names')
def names():
    print("Returns a list of sample names in the format:'[BB_940...]'")
    #use method of iterating over sqlalchemy."self.__table__.columns will "only" give you the columns defined in that particular class, i.e. without inherited ones. if you need all, use self.__mapper__.columns."
    samples = Samples.__table__.columns.keys()
    names = samples[1:]
    ("Retrieving list of sample names")
    return(jsonify(names))

@app.route('/otu')
def otu():
    print("Return a list of OTU descriptions")
    descriptions_query = session.query(Otu.lowest_taxonomic_unit_found).all()
    rows = [x[0] for x in descriptions_query]
    print("Getting otu descriptions")
    return(jsonify(rows))

@app.route('/metadata/<sample>')
def metadata(sample):
    #Get the metadata for a given sample
    # sampleID = int(sample.split("_")[1])
    # sample_metadata_query = session.query(Samples_Metadata).filter(Samples_Metadata.SAMPLEID == sampleID)
    # sample_metadata = pd.read_sql(sample_metadata_query.statement,sample_metadata_query.session.bind)
    # return(jsonify(sample_metadata.to_dict()))
    #A better way to do the same
    sample_metadata_query = session.query(Samples_Metadata).filter(Samples_Metadata.SAMPLEID == sample[3:]).all()
    meta_dict = {}
    #print(sample_metadata_query)
    #.__dict__. holds the attributes which will describe the object
    for k,v in sample_metadata_query[0].__dict__.items():
        if ('SAMPLEID'in k or 'ETHNICITY' in k or 'GENDER' in k or 'AGE' in k or 'BBTYPE' in k or 'LOCATION' in k):
            #print(meta_dict)
            meta_dict[k] = v
    print("Getting metadata for a given <sample>")
    return jsonify(meta_dict)
    
@app.route('/wfreq/<sample>')
def wfreq(sample):
    # Get the weekly washing frequency.
    sampleID = int(sample.split("_")[1])
    wfreq_query = session.query(Samples_Metadata).filter(Samples_Metadata.SAMPLEID == sampleID)
    wfreq = int(pd.read_sql(wfreq_query.statement,wfreq_query.session.bind)['WFREQ'])
    return(jsonify(wfreq))


@app.route('/samples/<sample>')
def samples(sample):
    #Get the OTU IDs and Sample Values for a sample
   
    Samples_query = session.query(Samples)
    #Read samples in dataframe
    samples = pd.read_sql(Samples_query.statement, Samples_query.session.bind)
    #select otu_id
    otu_ids=samples[['otu_id',sample]]
    #Sort (OTU ID and Sample Value) in Descending Order by Sample Value
    otu_ids = otu_ids.loc[otu_ids[sample] > 0]
    otu_ids.columns = ['otu_id', 'samples']
    otu_ids = otu_ids.sort_values('samples', ascending=False)
    #Define empty lists to append values 
    otu_ids_list=[]
    samples_list=[]
    #loop through every row in table for all otu_ids and sample in samples table
    for i in range(0, len(otu_ids)):
        otu_ids_list.append(str(otu_ids['otu_id'].iloc[i]))
        samples_list.append(str(otu_ids['samples'].iloc[i]))
    #Appends lists to the list of dictionaries containing sorted lists  for `otu_ids`and `sample_values`
    otu_ids_dict=[{
        "otu_ids":otu_ids_list,
        "sample_values":samples_list
        }]
    return(jsonify(otu_ids_dict))

if __name__ == "__main__":
    app.run(debug=True)
           # <script src="{{ url_for('static', filename='js/app.js') }}"></script>

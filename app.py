from pandas_datareader import wb
import numpy as np
import statsmodels.formula.api as smf
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, render_template


def download_data(year):
    ind = ['SH.STA.ACSN', 'SE.PRM.CMPT.FE.ZS']
    dat = wb.download(indicator=ind, country='all', start=year, end=year).dropna()
    dat.columns = ['sanitation', 'completion']
    return dat


def create_plot(dat):

    sanitation = dat['sanitation']
    completion = dat['completion']

    plot = figure(x_axis_label="Improved sanitation facilities (%)",
                  y_axis_label="Primary completion rate, female (%)")

    mod = smf.ols("completion ~ sanitation", dat).fit()
    (intercept, slope) = mod.params
    x = np.array([min(sanitation), max(sanitation)])
    y = intercept + slope * x

    plot.scatter(x=sanitation, y=completion)
    plot.line(x, y, color='red')

    return components(plot)

app = Flask(__name__)


@app.route('/')
@app.route('/<int:year>')
def index(year=2013):
    dat = download_data(year)
    script, div = create_plot(dat)
    return render_template('index.html', div=div, script=script, year=year)

if __name__ == '__main__':
    app.run(debug=True)
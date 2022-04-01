# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import json

# Read the airline data into pandas dataframe
data =  pd.read_csv('UN_Energy.csv')

countries = ['Total, all countries or areas', 'Africa', 'North America',
       'South America', 'Asia', 'Europe', 'Oceania']
dfx = data[~data['Region/Country/Area'].isin(countries)]
count = dfx['Region/Country/Area'].unique()
c_lst = count.tolist()

continents = ['Africa', 'North America',
       'South America', 'Asia', 'Europe', 'Oceania']
df_c = data[data['Region/Country/Area'].isin(continents)]

df_t = data.loc[data['Region/Country/Area']=='Total, all countries or areas', :]


# Create a dash application
app = dash.Dash(__name__)

app.layout = html.Div(children=[
					html.Div([
						html.H1('La energía en el mundo'),
						html.H4('Portfolio de Nicolau Freitas')
						]),
					html.Div([
						html.Div([
							dcc.Dropdown(id='en_type',
										options=[
										{'label':'Producción de energía', 'value':'Primary energy production'},
										{'label':'Importación de energía', 'value':'Net imports [Imports - Exports - Bunkers]'},
										{'label':'Cambios en el stock', 'value':'Changes in stocks'},
										{'label':'Suministración total', 'value':'Total supply'},
										{'label':'Suministración per capta', 'value':'Supply per capita'}
										], placeholder='Seleccione el tipo',
										style={},
										value='Primary energy production'
									),
							dcc.Dropdown(id='year',
										options=[
										{'label':'1995', 'value':1995},
										{'label':'2000', 'value':2000},
										{'label':'2005', 'value':2005},
										{'label':'2010', 'value':2010},
										{'label':'2015', 'value':2015},
										{'label':'2016', 'value':2016},
										{'label':'2017', 'value':2017},
										{'label':'2018', 'value':2018}			
										],placeholder='Seleccione el año',
										style={},
										value= 1995
									),
							html.Div([
								html.P(id='cant1', children=[]),
								html.P(id='cant2', children=[], className='txt_dest'),
								html.P(id='cant3', children=[])
								], className='txt_info')							
							], className='item30'),
						html.Div(
							html.Div(dcc.Graph(id='map')),
							className='item70')
						], className='cont70_30'),
					html.Div([
							html.Div(dcc.Graph(id='bar1'), className='item50'),
							html.Div(dcc.Graph(id='line1'), className='item50')
							], className='cont70_30'),
					html.Div([
						html.H2('Análisis por país'),
						html.Hr(className='horbar')
						]),
					html.Div([
						html.Div(
							dcc.Dropdown(id='country',
										options=[
										{'label':i, 'value':i}	for i in c_lst		
										],placeholder='Seleccione el país',
										style={},
										value='Afghanistan'
									), className='item30'
							),
						html.Div(
							html.Div([
								html.Div(dcc.Graph(id='cg_01'), className='item50'),
								html.Div(dcc.Graph(id='cg_02'), className='item50'),
								html.Div(dcc.Graph(id='cg_03'), className='item50'),
								html.Div(dcc.Graph(id='cg_04'), className='item50'),
								html.Div(dcc.Graph(id='cg_05'), className='item50')
								], className='cont70_30'), className='item70'
							)
						], className='cont70_30')	
				])



@app.callback([
	Output(component_id='map', component_property='figure'),
	Output(component_id='bar1', component_property='figure'),
	Output(component_id='line1', component_property='figure'),
	Output(component_id='cant1', component_property='children'),
	Output(component_id='cant2', component_property='children'),
	Output(component_id='cant3', component_property='children')],[
	Input(component_id='en_type', component_property='value'),
	Input(component_id='year', component_property='value')]
	)

def draw_graphs(tipo, ano):

	if tipo == 'Primary energy production':
		entxt = 'Producción de energía'
		entxt2 = 'Producción mundial de energía'
	elif tipo == 'Net imports [Imports - Exports - Bunkers]':
		entxt = 'Importación de energía'
		entxt2 = 'Importación mundial de energía'
	elif tipo == 'Changes in stocks':
		entxt = 'Cambios en el stock'
		entxt2 = 'Cambios mundiales en el stock'
	elif tipo == 'Total supply':
		entxt = 'Suministración total'
		entxt2 = 'Suministración  mundial total'
	else:
		entxt = 'Suministración per capta'
		entxt2 = 'Suministración per capta m undial'

	if tipo == 'Supply per capita':
		lab_gr = 'Energía en gigajulios'
		unidad = 'gigajulios'
	else:
		lab_gr = 'Energia en petajulios'
		unidad = 'petajulios'


	


	df_m = dfx.loc[(dfx['Series']==tipo) & (dfx['Year']==ano)]
	df_cl = df_c.loc[(df_c['Series']==tipo) & (df_c['Year']==ano)]
	df_tl = df_t.loc[df_t['Series']==tipo]

	df_tx = data.loc[(data['Series'] == tipo) & (data['Year'] == ano) & (data['Region/Country/Area'] == 'Total, all countries or areas')]
	cant_tx = df_tx['Value']
	cant_tx = cant_tx.tolist()
	cant_tx = cant_tx[0]

	mapfig = px.choropleth(locationmode='country names', locations=df_m['Region/Country/Area'],
		color=df_m['Value'], scope='world', title='{} en {}'.format(entxt, str(ano)), 
		labels={'color':lab_gr})
	mapfig.update_layout(paper_bgcolor='black',
		geo_bgcolor='black',
		font_color='white',
		title=dict(
		font_size=20
		))

	contbar = px.bar(df_cl, x='Value', y='Region/Country/Area', orientation='h',
		title='{} por continente en {}'.format(entxt, str(ano)),
		labels={'Value': lab_gr, 'Region/Country/Area':'Continente'})
	contbar.update_layout(paper_bgcolor='black',
		plot_bgcolor='black',
		font_color='white',
		title=dict(
		font_size=20
		)),
	contbar.update_xaxes(gridcolor='Gray')
	contbar.update_yaxes(gridcolor='Gray')

	totline = px.line(df_tl, x='Year', y='Value', title='{} total a lo largo de los años'.format(entxt),
		labels={'Value': lab_gr, 'Year':'Año'})
	totline.update_layout(paper_bgcolor='black',
		plot_bgcolor='black',
		font_color='white',
		title=dict(
		font_size=20
		))
	totline.update_xaxes(gridcolor='Gray')
	totline.update_yaxes(gridcolor='Gray')

	canttext1 = '{} en {}:'.format(entxt2, ano)

	canttext2 = cant_tx

	canttext3 = unidad


	return [mapfig, contbar, totline, canttext1, canttext2, canttext3]

@app.callback([
	Output(component_id='cg_01', component_property='figure'),
	Output(component_id='cg_02', component_property='figure'),
	Output(component_id='cg_03', component_property='figure'),
	Output(component_id='cg_04', component_property='figure'),
	Output(component_id='cg_05', component_property='figure')],
	Input(component_id='country', component_property='value'))

def draw_grph02(pais):

	df_p = data.loc[data['Region/Country/Area']== pais, :]

	fig_c01 = px.line(df_p[df_p['Series']=='Primary energy production'], x='Year', y='Value',
		title='Producción de energía', labels={'Value': 'Energía en petajulios', 'Year':'Año'})
	fig_c01.update_layout(paper_bgcolor='black',
		plot_bgcolor='black',
		font_color='white',
		title=dict(
		font_size=20
		))
	fig_c01.update_xaxes(gridcolor='Gray')
	fig_c01.update_yaxes(gridcolor='Gray')

	fig_c02 = px.line(df_p[df_p['Series']=='Net imports [Imports - Exports - Bunkers]'],
		x='Year', y='Value', title='Importación de energía',
		labels={'Value': 'Energía en petajulios', 'Year':'Año'})
	fig_c02.update_layout(paper_bgcolor='black',
		plot_bgcolor='black',
		font_color='white',
		title=dict(
		font_size=20
		))
	fig_c02.update_xaxes(gridcolor='Gray')
	fig_c02.update_yaxes(gridcolor='Gray')

	fig_c03 = px.line(df_p[df_p['Series']=='Changes in stocks'], x='Year', y='Value',
		title='Cambios en el stock', labels={'Value': 'Energía en petajulios', 'Year':'Año'})
	fig_c03.update_layout(paper_bgcolor='black',
		plot_bgcolor='black',
		font_color='white',
		title=dict(
		font_size=20
		))
	fig_c03.update_xaxes(gridcolor='Gray')
	fig_c03.update_yaxes(gridcolor='Gray')

	fig_c04 = px.line(df_p[df_p['Series']=='Total supply'], x='Year', y='Value',
		title='Suministración total', labels={'Value': 'Energía en petajulios', 'Year':'Año'})
	fig_c04.update_layout(paper_bgcolor='black',
		plot_bgcolor='black',
		font_color='white',
		title=dict(
		font_size=20
		))
	fig_c04.update_xaxes(gridcolor='Gray')
	fig_c04.update_yaxes(gridcolor='Gray')

	fig_c05 = px.line(df_p[df_p['Series']=='Supply per capita'], x='Year', y='Value',
		title='Suministración per capta', labels={'Value': 'Energía en gigajulios', 'Year':'Año'})
	fig_c05.update_layout(paper_bgcolor='black',
		plot_bgcolor='black',
		font_color='white',
		title=dict(
		font_size=20
		))
	fig_c05.update_xaxes(gridcolor='Gray')
	fig_c05.update_yaxes(gridcolor='Gray')
	

	return [fig_c01, fig_c02, fig_c03, fig_c04, fig_c05]


# Run the app
if __name__ == '__main__':
    app.run_server()
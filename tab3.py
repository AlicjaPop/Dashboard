import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import datetime as dt

def render_tab(df):

    df['weekday']=df['tran_date'].dt.dayofweek
    df['weekday'].replace({0: 'Poniedziałek', 1: 'Wtorek', 2: 'Środa', 3: 'Czwartek', 4: 'Piątek', 5: 'Sobota', 6: 'Niedziela'}, inplace=True)

    fig=go.Figure()
    for Store_type in df['Store_type'].unique():
        grouped = df[df['Store_type'] == Store_type].groupby('weekday')['total_amt'].sum()
        fig.add_trace(go.Bar(x=grouped.index, y=grouped.values, name=Store_type, hoverinfo='text',
        hovertext=[f'{Store_type}:{y/1e3:.2f}k' for y in grouped.values]))

    fig.update_layout(title='Wysokość sprzedaży w poszczególne dni tygodnia w zależności od kanału sprzedaży',
                  xaxis=dict(title='Dzień tygodnia'),
                  yaxis=dict(title='Wysokość sprzedaży'))
    fig.update_xaxes(categoryorder='array', categoryarray=['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela'])


    layout = html.Div([
        html.H1('Kanały sprzedaży', style={'text-align':'center'}),
        html.Div([
            html.Div([dcc.Graph(id='bar-store-day', figure=fig)]),
            html.Div([
                dcc.Dropdown(
                    id='store_dropdown',
                    options=[{'label':Store_type,'value':Store_type} for Store_type in df['Store_type'].unique()],
                    value=df['Store_type'].unique()[0]
                ),
                dcc.Graph(id='bar-client-shop')
            ])
        ], style={'display':'flex', 'flex-direction':'column'}),
        html.Div(id='temp-out')
    ])

    return layout

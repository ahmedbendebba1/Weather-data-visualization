import altair as alt
import chart_studio.plotly as py
import plotly.graph_objs as go


def plot_temp(df):
    """
    df: pandas dataframe with columns ['year', 'month', 'day', 'avg_temp', 'min_temp', 'max_temp']
    returns: Plotly plot
    """

    df["Time"] = df["year"] + "-" + df["month"] + "-" + df["day"]
    # F to Celsius
    for temp in ['avg_temp', 'min_temp', 'max_temp']:
        df[temp] = (df[temp] - 32)*5/9


    upper_bound = go.Scatter(
        name="Max temperature",
        x=df["Time"],
        y=df["max_temp"],
        mode="lines",
        marker=dict(color="#444"),
        line=dict(width=0),
        fillcolor="rgba(68, 68, 68, 0.3)",
        fill="tonexty",
    )

    trace = go.Scatter(
        name="Avg temperature",
        x=df["Time"],
        y=df["avg_temp"],
        mode="lines",
        line=dict(color="rgb(31, 119, 180)"),
        fillcolor="rgba(68, 68, 68, 0.3)",
        fill="tonexty",
    )

    lower_bound = go.Scatter(
        name="Min temperature",
        x=df["Time"],
        y=df["min_temp"],
        marker=dict(color="#444"),
        line=dict(width=0),
        mode="lines",
    )

    # Trace order can be important
    # with continuous error bars
    data = [lower_bound, trace, upper_bound]

    layout = go.Layout(
        yaxis=dict(title="Temperature in C"),
        title="Temperature (avg, min, max) for selected year and department",
        # plot_bgcolor='#ffffff',
        showlegend=False,
    )

    fig = go.Figure(data=data, layout=layout)
    # fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='Grey')
    # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Grey')

    return fig



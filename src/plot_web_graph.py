import plotly.graph_objects as go
from plotly.subplots import make_subplots

from get_json import get_json
from get_ratings import ratings_daily_games

games = get_json('kewko', update=False)
dailygames = ratings_daily_games(games)
# df = pd.DataFrame(dailygames)
# df['MA'] = df.rolling(window=100)['daily_games'].mean()

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(x=dailygames['dates'], y=dailygames['ratings'], name='Ratings'),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=dailygames['weekly_starts'], y=dailygames['weekly_games'], name='Daily Games', fill='tozeroy'),
    secondary_y=True

)
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Ratings", secondary_y=False)
fig.update_yaxes(title_text="Daily Games", secondary_y=True)

fig.show()

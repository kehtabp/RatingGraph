import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from dateutil import parser

file = open('C:\\Users\\aleksandrovk\\Downloads\\lichess_kewko_2018-11-07.pgn', 'r')
text = file.read()
gamesText = text.split('\n\n\n')
games = []
for index, gameText in enumerate(gamesText):
    # if index == 100:
    #     break
    headers = gameText.split('\n')
    game = {}
    add_game = False
    for header in headers:
        title_value = header.split(' "')
        if len(title_value) == 2:
            title = title_value[0][1:]
            value = title_value[1][:-2]
            game[title] = value
            if value == 'kewko':
                game['Side'] = title
            if title == 'UTCTime':
                game['Timestamp'] = parser.parse(game['UTCDate'] + ' ' + value)
            # print(title_value)
        elif len(header) > 1:
            game['PGN'] = header
    if game.get('Event') == 'Rated Blitz game':
        games.append(game)
xData = []
yData = []
bothData = []
for game in games:
    timestamp = game['Timestamp']
    rating = int(game[game['Side'] + 'Elo'])
    # print(str(timestamp) + ' : ' + game[game['Side'] + 'Elo'])
    # xData.append(timestamp)
    yData.append(rating)
    bothData.append([timestamp, rating])

xData = list(range(len(yData)))
fig = plt.figure(figsize=(13, 9))
ax = plt.subplot(frameon=True, autoscale_on=True, position=[0.065, 0.065, 0.925, 0.925])

ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

plt.tick_params(axis="both", which="both", bottom=False, top=False,
                labelbottom=True, left=False, right=False, labelleft=True)

plt.xlabel("Game number", fontsize=16)
plt.ylabel("Lichess Blitz Rating", fontsize=16)

for y in range(800, 1520, 50):
    plt.plot(range(min(xData), max(xData)), [y] * len(range(min(xData), max(xData))), "--", lw=0.5, color="black",
             alpha=0.3)

ax.set(xlim=(min(xData), max(xData)), ylim=(min(yData), max(yData)))

xData = list(reversed(xData))
yData = list(reversed(yData))

firstGame = min(xData)
lastGame = max(xData)


def date_linspace(start, end, steps):
    delta = (end - start) / steps
    increments = range(0, steps) * np.array([delta] * steps)
    return start + increments


xData = date_linspace(firstGame, lastGame, len(xData))


def animate(i):
    if i >= len(yData) - 2:
        return
    ax.plot(xData[i:i + 2], yData[i:i + 2], color="#3F5D7D")

    currnetDay = xData[i + 2]
    xlimstart = firstGame
    if i > 500:
        xlimstart = xData[i - 500]

    x2 = xData[i + 2]
    ax.set(xlim=(xlimstart, x2))


anim = animation.FuncAnimation(
    fig, animate, interval=17, frames=len(xData) - 1)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=60, metadata=dict(artist='Me'), bitrate=100000)
# anim.save('my_blitzrating3.mp4')
#
plt.draw()
plt.show()

# print("Done")

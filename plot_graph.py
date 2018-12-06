from matplotlib import pyplot as plt, animation


def plot_graph(ratings: list, daily_games: list, username, export_video=False, show_graph=True, game_mode="Blitz",
               size="small"):
    if size == "small":
        fig = plt.figure()
        ax = plt.axes()
        ax2 = plt.twinx(ax)
    else:
        fig = plt.figure(figsize=(19.2, 10.8))
        ax = plt.axes(autoscale_on=True, position=[0.05, 0.05, 0.9, 0.95])
        ax2 = plt.twinx(ax)
        ax2.set_position([0.05, 0.05, 0.9, 0.95])

    line_color = "#3F5D7D"
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_ylabel("%s Lichess %s Rating" % (username, game_mode), color=line_color)
    ax.tick_params(labelcolor=line_color, left=False, bottom=False,)
    ax.set_xlabel("Game number")

    bar_color = 'grey'
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.set_ylabel('Games per day', color=bar_color)
    ax2.tick_params(labelcolor=bar_color, right=False, bottom=False)

    number_of_games = len(ratings)

    for y in range(800, 1520, 50):
        ax.plot(range(0, number_of_games),
                [y] * len(range(0, number_of_games)), "--", lw=0.5,
                color="black", alpha=0.3)

    ax.set(ylim=(round_to(min(ratings), 50), round_to(max(ratings), 50, False)))
    ax2.set(ylim=(0, round_to(max(daily_games), 5, False)))

    def animate(i):
        if i >= len(ratings) - 2:
            return

        if i > 0:
            ax.set(xlim=(0, i + 1))
            ax2.bar(i, daily_games[i], color="black", alpha=0.1, width=1.0)
            ax.plot([i - 1, i], ratings[i - 1:i + 1], color=line_color)

    anim = animation.FuncAnimation(fig, animate, interval=17, frames=number_of_games - 1)

    writer = animation.writers['ffmpeg']
    writer(fps=60, metadata=dict(artist='kewko'))

    if export_video:
        anim.save('export/%s_%s_Rating_fs.mp4' % (username, game_mode))
        print('Saved export/%s_%s_Rating_fs.mp4' % (username, game_mode))

    if show_graph:
        plt.draw()
        plt.show()


def round_to(x, base, down=True):
    if down:
        return x - (x % base)
    else:
        if x % base != 0:
            return x + base - (x % base)
        else:
            return x

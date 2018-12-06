from matplotlib import pyplot as plt, animation as animation


def plot_graph(ratings: list, dates: list, username, export_video=False, show_graph=True, game_mode="Blitz",
               size="small"):
    game_num = list(range(len(ratings)))
    if size == "small":
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=(19.2, 10.8))

    ax = plt.axes(frameon=True, autoscale_on=True, position=[0.065, 0.065, 0.925, 0.925])

    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    plt.tick_params(axis="both", which="both", bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)
    plt.xlabel("Game number", fontsize=16)
    plt.ylabel("%s Lichess %s Rating" % (username, game_mode), fontsize=16)

    first_game_num = min(game_num)
    last_game_num = max(game_num)

    for y in range(800, 1520, 50):
        plt.plot(range(first_game_num, last_game_num),
                 [y] * len(range(first_game_num, last_game_num)), "--", lw=0.5,
                 color="black", alpha=0.3)
    dates = list(reversed(dates))
    ratings = list(reversed(ratings))
    ax.set(xlim=(first_game_num, last_game_num), ylim=(min(ratings), max(ratings)))

    def animate(i):
        if i >= len(ratings) - 2:
            return
        ax.plot(game_num[i:i + 2], ratings[i:i + 2], color="#3F5D7D")

        currnet_game_number = game_num[i + 2]
        xlimstart = first_game_num

        # games_on_graph = 500

        # if i > games_on_graph:
        #     game_frequency = 1 / (dates[i] - dates[i - games_on_graph]).total_seconds()
        #     xlimstart = xData[i - games_on_graph]

        ax.set(xlim=(xlimstart, currnet_game_number))

    anim = animation.FuncAnimation(fig, animate, interval=17, frames=len(game_num) - 1)

    writer = animation.writers['ffmpeg']
    writer(fps=60, metadata=dict(artist='kewko'))

    if export_video:
        anim.save('export/%s_%s_Rating_fs.mp4' % (username, game_mode))
        print('Saved export/%s_%s_Rating_fs.mp4' % (username, game_mode))

    if show_graph:
        plt.draw()
        plt.show()

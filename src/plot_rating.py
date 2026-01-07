import os

import requests
from matplotlib import pyplot as plt, animation
from requests.auth import HTTPBasicAuth

from utils import logger


def plot_rating(ratings: list, daily_games: list, username, export_video=False, export_image=False,
                show_graph=True, game_mode="Blitz", big=False, upload=False):
    if big:
        fig = plt.figure(figsize=(16, 10))
        ax = plt.axes(autoscale_on=True, position=[0.06, 0.06, 0.88, 0.94])
        ax2 = plt.twinx(ax)
        ax2.set_position([0.06, 0.06, 0.88, 0.94])
        ax3 = plt.twinx(ax)
        ax.tick_params(labelsize=15)
        ax2.tick_params(labelsize=15)
        ax3.tick_params(labelsize=15)
        size = 'big'
    else:
        fig = plt.figure()
        ax = plt.axes()
        ax2 = plt.twinx(ax)
        ax3 = plt.twinx(ax)
        size = 'small'

    line_color = "#3F5D7D"
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_ylabel(f"{username}'s Lichess {game_mode} Rating", color=line_color, fontsize=15)
    ax.tick_params(labelcolor=line_color, left=False, bottom=False)
    ax.set_xlabel("Number of games", fontsize=15)

    ax3.spines["top"].set_visible(False)
    ax3.spines["bottom"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.spines["left"].set_visible(False)
    ax3.tick_params(labelright=False, left=False, bottom=False)

    bar_color = 'grey'
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.set_ylabel('Games per day', color=bar_color, fontsize=15)
    ax2.tick_params(labelcolor=bar_color, right=False, bottom=False)

    number_of_games = len(ratings)

    for y in range(800, 3000, 50):
        ax.plot(range(0, number_of_games),
                [y] * len(range(0, number_of_games)), "--", lw=0.5,
                color="black", alpha=0.3)

    ax.set(ylim=(round_to(min(ratings), 50), round_to(max(ratings), 50, False)))
    ax3.set(ylim=(round_to(min(ratings), 50), round_to(max(ratings), 50, False)))
    ax2.set(ylim=(0, round_to(max(daily_games), 5, False)))

    # Export static image with all data plotted
    if export_image:
        logger.info("Exporting image...")
        os.makedirs('export', exist_ok=True)
        # Plot all data for static image
        ax.set(xlim=(0, number_of_games))
        ax3.set(xlim=(0, number_of_games))
        # Draw all bars
        ax2.bar(range(number_of_games), daily_games, color="black", alpha=0.1, width=1.0)
        # Draw rating line
        ax.plot(range(number_of_games), ratings, color=line_color)
        # Draw 100-game moving average
        if number_of_games > 100:
            moving_avg = [sum(ratings[max(0, i-100):i]) / min(i, 100) if i > 0 else ratings[0]
                          for i in range(1, number_of_games + 1)]
            ax3.plot(range(100, number_of_games), moving_avg[100:], color='orange')

        image_path = f'export/ChessGraph_{username}_{game_mode}_{size}.png'
        fig.savefig(image_path, dpi=150, bbox_inches='tight')
        logger.info(f'Saved {image_path}')

        # Clear the plotted data if we also need to animate
        if export_video or show_graph:
            ax.cla()
            ax2.cla()
            ax3.cla()
            # Re-setup axes for animation
            ax.spines["top"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.set_ylabel(f"{username}'s Lichess {game_mode} Rating", color=line_color, fontsize=15)
            ax.tick_params(labelcolor=line_color, left=False, bottom=False)
            ax.set_xlabel("Number of games", fontsize=15)
            ax3.spines["top"].set_visible(False)
            ax3.spines["bottom"].set_visible(False)
            ax3.spines["right"].set_visible(False)
            ax3.spines["left"].set_visible(False)
            ax3.tick_params(labelright=False, left=False, bottom=False)
            ax2.spines["top"].set_visible(False)
            ax2.spines["bottom"].set_visible(False)
            ax2.spines["right"].set_visible(False)
            ax2.spines["left"].set_visible(False)
            ax2.set_ylabel('Games per day', color=bar_color, fontsize=15)
            ax2.tick_params(labelcolor=bar_color, right=False, bottom=False)
            for y in range(800, 3000, 50):
                ax.plot(range(0, number_of_games),
                        [y] * len(range(0, number_of_games)), "--", lw=0.5,
                        color="black", alpha=0.3)
            ax.set(ylim=(round_to(min(ratings), 50), round_to(max(ratings), 50, False)))
            ax3.set(ylim=(round_to(min(ratings), 50), round_to(max(ratings), 50, False)))
            ax2.set(ylim=(0, round_to(max(daily_games), 5, False)))

    def animate(i):
        if i >= len(ratings) - 2:
            return

        if i > 0:
            ax.set(xlim=(0, i + 1))
            ax3.set(xlim=(0, i + 1))
            ax2.bar(i, daily_games[i], color="black", alpha=0.1, width=1.0)
            ax.plot([i - 1, i], ratings[i - 1:i + 1], color=line_color)
            if i > 100:
                ax3.plot([i - 1, i], [sum(ratings[i-100-1:i-1])/100, sum(ratings[i - 100:i])/100], color='orange')

    if export_video or show_graph:
        anim = animation.FuncAnimation(fig, animate, interval=17, frames=number_of_games - 1)

        # Create FFmpeg writer with proper settings
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=60, metadata=dict(artist=username), bitrate=1800)

        if export_video:
            logger.info("Exporting video...")
            export_file_path = f'export/ChessGraph_{username}_{game_mode}_{size}.mp4'
            os.makedirs('export', exist_ok=True)
            # Pass the writer instance to anim.save()
            anim.save(export_file_path, writer=writer)
            logger.info(f'Saved {export_file_path}.')
            if upload:
                from secrets import streamable_password, streamable_username
                with open(export_file_path, 'rb') as f:
                    files = {'file': f}
                    logger.info("Uploading to streamable...")
                    response = requests.post(
                        'https://api.streamable.com/upload',
                        auth=HTTPBasicAuth(streamable_username, streamable_password),
                        files=files,
                        timeout=120
                    )
                graph_url = f"https://streamable.com/{response.json()['shortcode']}"
                logger.info(f"Uploaded: {graph_url}")
                return graph_url

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

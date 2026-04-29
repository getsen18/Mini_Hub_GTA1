import sys        # sys.argv for player names, sys.exit to close
import os         # for building file paths
import subprocess # to launch each game as a separate process
import pygame     # game window, drawing, and events
import matplotlib
matplotlib.use('Agg')  # non-interactive backend — renders to memory, not a separate window
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg  # lets us grab the chart as raw pixel data
from collections import Counter  # counts occurrences — used for game play frequency


if len(sys.argv) != 3:
    print("Usage: python3 game.py <player1> <player2>")
    sys.exit(1)

player1 = sys.argv[1]  # first player's name from command line
player2 = sys.argv[2]  # second player's name from command line

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.csv")  # path to match history in project root

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)  # resizable hub window
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("MINI HUB GTA")
clock = pygame.time.Clock()
bg_image  = pygame.transform.scale(pygame.image.load("home.png"), (WIDTH, HEIGHT))  # home screen background
bg_image2 = pygame.transform.scale(pygame.image.load("hom.png"),  (WIDTH, HEIGHT))  # background for sort/play-again screens
card_images = [
    pygame.transform.scale(pygame.image.load("tictactoe.png"), (280, 300)),  # thumbnail for tictactoe card
    pygame.transform.scale(pygame.image.load("othello.png"),   (280, 300)),  # thumbnail for othello card
    pygame.transform.scale(pygame.image.load("connect4.png"),  (280, 300)),  # thumbnail for connect4 card
]
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
BG_COLOR   = (20,  20,  40)   # dark background for non-menu screens
DARK_BLUE  = (0,   80,  100)  # button colour (normal)
LIGHT_BLUE = (0,   125, 255)  # button colour (hovered)
GOLD        = (255, 220, 0)    # title text colour
RUSTIC_GREY = (105, 105, 105)  # button normal colour for sort/play-again screens
SOFT_WHITE = (180, 180, 255)  # subtitle / player names text colour

font_large = pygame.font.SysFont("Arial", 52, bold=True)  # hub title font
font_med   = pygame.font.SysFont("Arial", 34)             # button and heading font
font_small = pygame.font.SysFont("Arial", 24)             # subtitle and small text font


def read_history():
    records = []
    if not os.path.exists(HISTORY_FILE):  # file doesn't exist yet — no games played
        return records
    with open(HISTORY_FILE) as f:
        for line in f:
            parts = line.strip().split(",")  # each line is: winner,loser,date,game
            if len(parts) == 4:              # skip malformed lines
                records.append({
                    "winner": parts[0],
                    "loser":  parts[1],
                    "date":   parts[2],
                    "game":   parts[3]
                })
    return records


def show_matplotlib_charts(sort_metric="wins"):
    records = read_history()
    if not records:  # no history yet — nothing to chart
        return

    game_counts = Counter(r["game"] for r in records)  # how many times each game was played

    # Build per-player stats
    stats = {}
    for r in records:
        w, l = r["winner"], r["loser"]
        stats.setdefault(w, {"wins": 0, "losses": 0})  # init entry if player seen for first time
        stats.setdefault(l, {"wins": 0, "losses": 0})
        stats[w]["wins"]   += 1
        stats[l]["losses"] += 1

    if sort_metric == "losses":
        top5 = sorted(stats.items(), key=lambda x: x[1]["losses"], reverse=True)[:5]  # top 5 by most losses
        bar_vals  = [s["losses"] for _, s in top5]
        bar_label = "Losses"
        bar_title = "Top 5 Players by Losses"
    elif sort_metric == "ratio":
        for p in stats:
            l = stats[p]["losses"]
            stats[p]["ratio"] = stats[p]["wins"] / l if l else stats[p]["wins"]  # avoid division by zero — treat 0 losses as ratio = wins
        top5 = sorted(stats.items(), key=lambda x: x[1]["ratio"], reverse=True)[:5]
        bar_vals  = [round(s["ratio"], 2) for _, s in top5]
        bar_label = "W/L Ratio"
        bar_title = "Top 5 Players by W/L Ratio"
    else:
        top5 = sorted(stats.items(), key=lambda x: x[1]["wins"], reverse=True)[:5]   # default — sort by wins
        bar_vals  = [s["wins"] for _, s in top5]
        bar_label = "Wins"
        bar_title = "Top 5 Players by Wins"

    dpi = 100
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(WIDTH / dpi, (HEIGHT - 120) / dpi), dpi=dpi)  # two side-by-side charts sized to window
    fig.patch.set_facecolor("#1a1a2e")  # dark background to match hub theme

    if top5:
        players = [p for p, _ in top5]
        colors = ["#FFD700", "#C0C0C0", "#CD7F32", "#4169E1", "#DC143C"][:len(players)]  # gold, silver, bronze, then two more
        ax1.bar(players, bar_vals, color=colors)
        ax1.set_title(bar_title, color="white", fontsize=13, fontweight="bold")
        ax1.set_xlabel("Player", color="white")
        ax1.set_ylabel(bar_label, color="white")
        ax1.set_facecolor("#16213e")
        ax1.tick_params(colors="white")
        for spine in ax1.spines.values():
            spine.set_edgecolor("white")  # white borders to show up on dark background

    if game_counts:
        labels = list(game_counts.keys())
        sizes  = list(game_counts.values())
        ax2.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90,
                colors=["#4169E1", "#DC143C", "#228B22"])  # pie chart — shows which game is played most
        ax2.set_title("Most Played Games", color="white", fontsize=13, fontweight="bold")

    plt.tight_layout()

    # Render figure into a pygame surface (no separate window)
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()                                              # raw RGBA pixel data from the chart
    chart_surf = pygame.image.frombuffer(buf, canvas.get_width_height(), "RGBA").copy()  # .copy() owns the pixels so plt.close won't corrupt them
    plt.close(fig)

    # Show chart inside pygame window with a Home button
    hom_bg    = pygame.transform.scale(pygame.image.load("hom.png"), (WIDTH, HEIGHT))  # fresh load for background
    home_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 90, 200, 55)
    font_btn  = pygame.font.SysFont("Arial", 28, bold=True)

    while True:
        screen.blit(hom_bg, (0, 0))       # hom.png background
        screen.blit(chart_surf, (0, 0))   # chart sits on top — covers upper portion, hom.png shows at bottom

        mouse = pygame.mouse.get_pos()
        btn_color = GOLD if home_rect.collidepoint(mouse) else RUSTIC_GREY  # rustic grey → gold on hover
        pygame.draw.rect(screen, btn_color, home_rect, border_radius=10)
        lbl = font_btn.render("HOME", True, WHITE)
        screen.blit(lbl, lbl.get_rect(center=home_rect.center))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if home_rect.collidepoint(mouse):
                    return  # go back to main loop


def draw_button(rect, text, hover, normal=DARK_BLUE, hovered=LIGHT_BLUE):
    color = hovered if hover else normal  # highlight button if mouse is over it
    pygame.draw.rect(screen, color, rect, border_radius=10)
    label = font_med.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))  # text centred inside button


def show_menu():
    card_w, card_h = 280, 300
    gap        = 60
    total_w    = 3 * card_w + 2 * gap              # total width of all 3 cards plus gaps
    start_x    = (WIDTH  - total_w) // 2           # x to start so cards are centred horizontally
    card_y     = HEIGHT // 2 - card_h // 2 - 30    # y to centre cards vertically with a little offset up
    cx         = WIDTH // 2                        # horizontal centre of window

    games = [
        {"label": "TIC TAC TOE", "file": "tictactoe.py", "desc1": "10 × 10 board",   "desc2": "5 in a row to win",  "accent": (220,  80,  80)},
        {"label": "OTHELLO",     "file": "othello.py",   "desc1": "8 × 8 board",     "desc2": "Flip your opponent", "accent": ( 60, 200,  90)},
        {"label": "CONNECT 4",   "file": "connect4.py",  "desc1": "7 × 7 board",     "desc2": "Drop 4 in a row",    "accent": (255, 200,   0)},
    ]

    cards = [(pygame.Rect(start_x + i * (card_w + gap), card_y, card_w, card_h), g)
             for i, g in enumerate(games)]  # pair each game dict with its screen rect

    quit_rect = pygame.Rect(cx - 110, card_y + card_h + 45, 220, 55)  # quit button below the cards

    while True:
        screen.blit(bg_image, (0, 0))
        mouse = pygame.mouse.get_pos()

        title = font_large.render("MINI HUB GTA1", True, GOLD)
        screen.blit(title, title.get_rect(centerx=cx, y=card_y - 110))

        sub = font_small.render(f"{player1}  vs  {player2}", True, SOFT_WHITE)
        screen.blit(sub, sub.get_rect(centerx=cx, y=card_y - 55))  # player names below title

        for i, (rect, g) in enumerate(cards):
            hover = rect.collidepoint(mouse)

            # card background + border
            pygame.draw.rect(screen, (45, 45, 75) if not hover else (65, 65, 105), rect, border_radius=16)  # lighter bg on hover
            pygame.draw.rect(screen, g["accent"] if hover else (70, 70, 110), rect, 3, border_radius=16)    # accent border on hover
            screen.blit(card_images[i], (rect.x, rect.y))  # game thumbnail image on top of card

        # quit button
        pygame.draw.rect(screen, LIGHT_BLUE if quit_rect.collidepoint(mouse) else DARK_BLUE, quit_rect, border_radius=10)
        lbl = font_med.render("QUIT", True, WHITE)
        screen.blit(lbl, lbl.get_rect(center=quit_rect.center))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, g in cards:
                    if rect.collidepoint(mouse):
                        return g["file"]      # return the chosen game's filename
                if quit_rect.collidepoint(mouse):
                    return "quit"


def show_sort_selection():
    bg = pygame.transform.scale(pygame.image.load("hom.png"), (WIDTH, HEIGHT))  # fresh load — avoids stale global
    btn_w, btn_h = 300, 60
    cx = WIDTH // 2
    options = [
        (pygame.Rect(cx - btn_w // 2, HEIGHT // 2 - 50,  btn_w, btn_h), "Sort by Wins",   "wins"),
        (pygame.Rect(cx - btn_w // 2, HEIGHT // 2 + 30,  btn_w, btn_h), "Sort by Losses", "losses"),
        (pygame.Rect(cx - btn_w // 2, HEIGHT // 2 + 110, btn_w, btn_h), "Sort by W/L",    "ratio"),
    ]
    while True:
        screen.blit(bg, (0, 0))  # hom.png background
        mouse = pygame.mouse.get_pos()

        title = font_med.render("Sort leaderboard by:", True, GOLD)
        screen.blit(title, title.get_rect(centerx=cx, y=HEIGHT // 2 - 130))

        for rect, label, _ in options:
            draw_button(rect, label, rect.collidepoint(mouse), normal=RUSTIC_GREY, hovered=GOLD)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, _, val in options:
                    if rect.collidepoint(mouse):
                        return val  # return "wins", "losses", or "ratio"


def show_play_again():
    bg = pygame.transform.scale(pygame.image.load("hom.png"), (WIDTH, HEIGHT))  # fresh load — avoids stale global after matplotlib
    btn_w, btn_h = 260, 60
    cx = WIDTH // 2
    buttons = [
        (pygame.Rect(cx - btn_w - 20, HEIGHT // 2 + 20, btn_w, btn_h), "PLAY AGAIN", True),   # True = play again
        (pygame.Rect(cx + 20,         HEIGHT // 2 + 20, btn_w, btn_h), "QUIT",       False),  # False = quit
    ]
    while True:
        screen.blit(bg, (0, 0))  # hom.png background
        mouse = pygame.mouse.get_pos()

        title = font_med.render("Play another game?", True, GOLD)
        screen.blit(title, title.get_rect(centerx=cx, y=HEIGHT // 2 - 60))

        for rect, label, _ in buttons:
            draw_button(rect, label, rect.collidepoint(mouse), normal=RUSTIC_GREY, hovered=GOLD)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, _, val in buttons:
                    if rect.collidepoint(mouse):
                        return val  # True if play again, False if quit


def restore_screen():
    global screen, WIDTH, HEIGHT, bg_image, bg_image2
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)  # recreate window after game subprocess closes it
    WIDTH, HEIGHT = screen.get_size()
    bg_image  = pygame.transform.scale(pygame.image.load("home.png"), (WIDTH, HEIGHT))  # reload — old surfaces can go stale after set_mode
    bg_image2 = pygame.transform.scale(pygame.image.load("hom.png"),  (WIDTH, HEIGHT))
    pygame.event.clear()  # flush stale events from when the hub was minimised


while True:
    game_file = show_menu()  # show home screen, get chosen game filename

    if game_file == "quit":
        break

    game_name = game_file.replace(".py", "")          # strip extension — used for leaderboard
    game_path = os.path.join("games", game_file)      # full relative path to the game script

    # Minimise hub so only the game window is visible
    pygame.display.iconify()

    # Blocking — waits here until the game subprocess exits
    subprocess.run([sys.executable, game_path, player1, player2])

    # Restore hub for sort selection screen
    restore_screen()
    sort_metric = show_sort_selection()  # player picks how to sort the leaderboard

    # Minimise hub so the terminal leaderboard is visible
    pygame.display.iconify()
    subprocess.run(["bash", "leaderboard.sh", game_name, sort_metric])  # print leaderboard to terminal

    # Restore hub for matplotlib and play-again
    restore_screen()
    show_matplotlib_charts(sort_metric)  # show bar chart + pie chart inside pygame window

    if not show_play_again():  # False means player chose quit
        break

pygame.quit()
sys.exit()

from __future__ import division
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Arc
import pandas as pd
import numpy as np

def plot_frame(df, frame=1, view_home=True, view_away=True, view_ball=True):
    
    '''Plot snapshot of match by frame.'''
    
    home = df[(df.type == '0') & (df.frame == frame)]
    away = df[(df.type == '1') & (df.frame == frame)]
    ball = df[(df.type == '7') & (df.frame == frame)]
    
    fig, ax = plt.subplots()
    fig.set_size_inches(10.5, 6.8)
    ax.set_aspect('equal')
    plt.xlim(-5250, 5250)
    plt.ylim(-3400, 3400)
    
    if view_home:
        plt.scatter(home.x.values, home.y.values, s=10)
    if view_away:
        plt.scatter(away.x.values, away.y.values, s=10, c='red')
    if view_ball:
        plt.scatter(ball.x.values, ball.y.values, s=20, c='purple')

    plt.plot([-5250, 5250], [-3400, -3400], color='black')
    plt.plot([-5250, 5250], [3400, 3400], color='black')
    plt.plot([-5250, -5250], [-3400, 3400], color='black')
    plt.plot([5250, 5250], [-3400, 3400], color='black')
    plt.plot([-5250, -3465], [-1965.2, -1965.2], color='black', lw=1)
    plt.plot([-5250, -3465], [1965.2, 1965.2], color='black', lw=1)
    plt.plot([-3465, -3465], [-1965.2, 1965.2], color='black', lw=1)
    plt.plot([5250, 3465], [-1965.2, -1965.2], color='black', lw=1)
    plt.plot([5250, 3465], [1965.2, 1965.2], color='black', lw=1)
    plt.plot([3465, 3465], [-1965.2, 1965.2], color='black', lw=1)
    plt.plot([5250, 4641], [-897.6, -897.6], color='black', lw=1)
    plt.plot([5250, 4641], [897.6, 897.6], color='black', lw=1)
    plt.plot([4641, 4641], [-897.6, 897.6], color='black', lw=1)
    plt.plot([-5250, -4641], [-897.6, -897.6], color='black', lw=1)
    plt.plot([-5250, -4641], [897.6, 897.6], color='black', lw=1)
    plt.plot([-4641, -4641], [-897.6, 897.6], color='black', lw=1)
    centre = plt.Circle((0, 0), 915, fill=0)
    theta = np.rad2deg(np.arcsin(5.5/(9.15/1.05)))
    semi1 = Arc((4042.5, 0), width=1830, height=1830, theta1=90+theta, theta2=270-theta, fill=0)
    semi2 = Arc((-4042.5, 0), width=1830, height=1830, theta1=270+theta, theta2=90-theta, fill=0)
    ax.add_artist(centre)
    ax.add_artist(semi1)
    ax.add_artist(semi2)

    plt.plot([0, 0], [-3400, 3400], color='black', lw=1)
    plt.scatter([0], [0], color='black')
    plt.scatter([-5250], [360.4], color='black', s=10)
    plt.scatter([-5250], [-360.4], color='black', s=10)
    plt.scatter([5250], [360.4], color='black', s=10)
    plt.scatter([5250], [-360.4], color='black', s=10)
    plt.scatter([4042.5], [0], color='black', s=10)
    plt.scatter([-4042.5], [0], color='black', s=10)
    
    plt.title('Ball possession: {}, ball in play: {}'.format(df[df.utc == df.utc[frame]].ballPossession.iloc[0],
                                                             bool(df[df.utc == df.utc[frame]].isBallInPlay.iloc[0])))

    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    return fig, ax


def plot_player(df, id='0', period=None):

    '''Plot trajectory of player/ball by period.'''

    player = df[(df.id == id) & (df.period == period)]

    if period == None:
    
        player = df[(df.id == id)]

    fig, ax = plt.subplots()
    fig.set_size_inches(10.5, 6.8)
    ax.set_aspect('equal')
    plt.xlim(-5250, 5250)
    plt.ylim(-3400, 3400)

    plt.scatter(player.x.values, player.y.values, s=1)

    plt.plot([-5250, 5250], [-3400, -3400], color='black')
    plt.plot([-5250, 5250], [3400, 3400], color='black')
    plt.plot([-5250, -5250], [-3400, 3400], color='black')
    plt.plot([5250, 5250], [-3400, 3400], color='black')
    plt.plot([-5250, -3465], [-1965.2, -1965.2], color='black', lw=1)
    plt.plot([-5250, -3465], [1965.2, 1965.2], color='black', lw=1)
    plt.plot([-3465, -3465], [-1965.2, 1965.2], color='black', lw=1)
    plt.plot([5250, 3465], [-1965.2, -1965.2], color='black', lw=1)
    plt.plot([5250, 3465], [1965.2, 1965.2], color='black', lw=1)
    plt.plot([3465, 3465], [-1965.2, 1965.2], color='black', lw=1)
    plt.plot([5250, 4641], [-897.6, -897.6], color='black', lw=1)
    plt.plot([5250, 4641], [897.6, 897.6], color='black', lw=1)
    plt.plot([4641, 4641], [-897.6, 897.6], color='black', lw=1)
    plt.plot([-5250, -4641], [-897.6, -897.6], color='black', lw=1)
    plt.plot([-5250, -4641], [897.6, 897.6], color='black', lw=1)
    plt.plot([-4641, -4641], [-897.6, 897.6], color='black', lw=1)
    centre = plt.Circle((0, 0), 915, fill=0)
    theta = np.rad2deg(np.arcsin(5.5/(9.15/1.05)))
    semi1 = Arc((4042.5, 0), width=1830, height=1830, theta1=90+theta, theta2=270-theta, fill=0)
    semi2 = Arc((-4042.5, 0), width=1830, height=1830, theta1=270+theta, theta2=90-theta, fill=0)
    ax.add_artist(centre)
    ax.add_artist(semi1)
    ax.add_artist(semi2)

    plt.plot([0, 0], [-3400, 3400], color='black', lw=1)
    plt.scatter([0], [0], color='black')
    plt.scatter([-5250], [360.4], color='black', s=10)
    plt.scatter([-5250], [-360.4], color='black', s=10)
    plt.scatter([5250], [360.4], color='black', s=10)
    plt.scatter([5250], [-360.4], color='black', s=10)
    plt.scatter([4042.5], [0], color='black', s=10)
    plt.scatter([-4042.5], [0], color='black', s=10)

    #plt.title('Player id: {}'.format(player.id.iloc[0]))

    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    return fig, ax